"""Iterative CFG with jump-table resolution -> dispatch inventory."""
import json
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
from pe_md3 import PE

p = PE()
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL

insn = {}      # va -> (size, mn, op, bytes)
owner = {}
funcs = {}
work = [(va, va) for _, va, _ in p.exports()]
dispatches = []
seen_tab = {}


def table_targets(tab, cap=1024):
    out = []
    for i in range(cap):
        v = p.u32(tab + 4 * i)
        if v is None or not (TLO <= v < THI):
            break
        out.append(v)
    return out


def ctx_before(start, site, n=10):
    """Return instructions preceding site within same function block."""
    seq = [(a, s, m, o) for a, (s, m, o, b) in insn.items()
           if start <= a < site]
    seq.sort()
    # keep only the last contiguous run
    tail = []
    expect = site
    for a, s, m, o in reversed(seq):
        if a + s == expect:
            tail.append((a, m, o))
            expect = a
        elif a + s < expect:
            break
        else:
            continue
    return list(reversed(tail))[-n:]


while work:
    start, own = work.pop()
    if start in funcs or not (TLO <= start < THI):
        continue
    f = dict(start=start, insns=[], calls=set(), name=None)
    funcs[start] = f
    for nm, va, _ in p.exports():
        if va == start:
            f['name'] = nm
    va = start
    while TLO <= va < THI:
        if va in insn:
            break
        buf = p.read(va, 16)
        if not buf:
            break
        one = next(md.disasm(buf, va, 1), None)
        if one is None:
            break
        insn[va] = (one.size, one.mnemonic, one.op_str, one.bytes)
        owner[va] = start
        f['insns'].append(va)
        mn, ops = one.mnemonic, one.operands
        if mn in ('ret', 'retn', 'int3', 'hlt', 'ud2'):
            break
        if mn == 'jmp':
            if ops and ops[0].type == X86_OP_IMM:
                t = ops[0].imm & 0xFFFFFFFF
                work.append((t, t))
            else:
                rec = dict(site=va, func=start, kind='jmp', text=one.op_str, bytes=one.bytes.hex())
                if ops and ops[0].type == X86_OP_MEM:
                    m = ops[0].mem
                    rec['index'] = one.reg_name(m.index) if m.index else None
                    rec['scale'] = m.scale
                    rec['disp'] = m.disp & 0xFFFFFFFF
                    rec['base'] = one.reg_name(m.base) if m.base else None
                    if m.index and m.scale == 4 and m.base == 0:
                        tab = m.disp & 0xFFFFFFFF
                        tg = table_targets(tab)
                        rec['table'] = tab
                        rec['raw_entries'] = len(tg)
                        rec['valid_entries'] = sum(1 for x in tg if TLO <= x < THI)
                        rec['guard'] = ctx_before(start, va)
                        rec['targets'] = tg
                        for x in tg:
                            if TLO <= x < THI:
                                work.append((x, x))
                dispatches.append(rec)
            break
        if mn == 'call':
            if ops and ops[0].type == X86_OP_IMM:
                t = ops[0].imm & 0xFFFFFFFF
                f['calls'].add(t)
                work.append((t, t))
            va += one.size
            continue
        if mn.startswith('j') and ops and ops[0].type == X86_OP_IMM:
            t = ops[0].imm & 0xFFFFFFFF
            work.append((t, start))
            va += one.size
            continue
        va += one.size

# ---- report ----
rows = []
for d in dispatches:
    g = ' | '.join('0x%08X %s %s' % x for x in d.get('guard', []))
    rows.append(dict(site='0x%08X' % d['site'], func='0x%08X' % d['func'],
                     text=d['text'], table=('0x%08X' % d['table']) if 'table' in d else None,
                     n=d.get('raw_entries'), valid=d.get('valid_entries'),
                     index=d.get('index'), scale=d.get('scale'),
                     guard=g))

with open('cfg_stats.txt', 'w', encoding='utf-8') as fh:
    fh.write('functions %d\ninstructions %d\nbytes %d (%.1f%% .text)\n' % (
        len(funcs), len(insn), sum(v[0] for v in insn.values()),
        100.0 * sum(v[0] for v in insn.values()) / T['vsize']))
    fh.write('dispatch sites %d\n' % len(dispatches))
    fh.write('jump-table sites %d\n' % sum(1 for d in dispatches if d.get('table')))
    fh.write('total table entries %d\n' % sum(d.get('raw_entries', 0) for d in dispatches))
    fh.write('invalid entries %d\n' % sum(d.get('raw_entries', 0) - d.get('valid_entries', 0) for d in dispatches))

with open('cfg_dispatch.txt', 'w', encoding='utf-8') as fh:
    for d in dispatches:
        fh.write('%s func=%s %-42s tab=%s n=%s valid=%s idx=%s\n   guard: %s\n' % (
            d['site'], d['func'], d['text'], d.get('table'), d.get('raw_entries'),
            d.get('valid_entries'), d.get('index'), d.get('guard', '')))

with open('cfg_funcs.txt', 'w', encoding='utf-8') as fh:
    for s in sorted(funcs):
        f = funcs[s]
        fh.write('0x%08X %4d %s\n' % (s, len(f['insns']), f['name'] or ''))

json.dump(rows, open('cfg_dispatch.json', 'w', encoding='utf-8'), indent=0)
print(open('cfg_stats.txt', encoding='utf-8').read())
