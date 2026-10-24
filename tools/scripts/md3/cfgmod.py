"""Iterative CFG with jump-table resolution. Importable."""
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from pe_md3 import PE

p = PE()
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL


def table_targets(tab, cap=1024):
    out = []
    for i in range(cap):
        v = p.u32(tab + 4 * i)
        if v is None or not (TLO <= v < THI):
            break
        out.append(v)
    return out


def build(extra_seeds=()):
    insn = {}
    owner = {}
    funcs = {}
    parent = {}
    dispatches = []
    work = [(va, va) for _, va, _ in p.exports()]
    work += [(a, a) for a in extra_seeds]
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
                    parent.setdefault(t, va)
                    work.append((t, t))
                else:
                    rec = dict(site=va, func=start, text=one.op_str, bytes=one.bytes.hex())
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
                            for x in tg:
                                parent.setdefault(x, va)
                                work.append((x, x))
                    dispatches.append(rec)
                break
            if mn == 'call':
                if ops and ops[0].type == X86_OP_IMM:
                    t = ops[0].imm & 0xFFFFFFFF
                    f['calls'].add(t)
                    parent.setdefault(t, va)
                    work.append((t, t))
                va += one.size
                continue
            if mn.startswith('j') and ops and ops[0].type == X86_OP_IMM:
                t = ops[0].imm & 0xFFFFFFFF
                parent.setdefault(t, va)
                work.append((t, start))
                va += one.size
                continue
            va += one.size
    return dict(insn=insn, owner=owner, funcs=funcs, parent=parent, dispatches=dispatches)


def seq_before(insn, start, site, n=12):
    items = [(a, v) for a, v in insn.items() if start <= a < site]
    items.sort()
    tail = []
    expect = site
    for a, v in reversed(items):
        if a + v[0] == expect:
            tail.append((a, v[1], v[2]))
            expect = a
        elif a + v[0] < expect:
            break
    return list(reversed(tail))[-n:]


def path(s, target, parent, limit=40):
    out = []
    cur = target
    for _ in range(limit):
        if cur == s or cur not in parent:
            out.append(cur)
            break
        out.append(cur)
        cur = parent[cur]
    return list(reversed(out))
