"""Recursive-descent disassembly of LS8000.md3 from the 3 exports.

Outputs (small):
  recdesc_stats.txt  - counts
  indirect.txt       - every indirect jmp/call site (FF /4, FF /2) + reachability
  funcs.txt          - sorted function starts
"""
import sys, time
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM
from pe_md3 import PE

p = PE()
TEXT = p.sections[0]
TEXT_END = TEXT['va'] + TEXT['vsize']

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL

insn_va = {}      # va -> size  (all decoded instructions)
owner = {}        # va -> func start
funcs = {}        # start -> dict
work = []         # (addr, owner)
raw_jmp = {}      # va -> (mnemonic, op_str) for indirect control flow


def u32(va):
    return p.u32(va)


def run():
    exports = p.exports()
    for name, va, _ in exports:
        work.append((va, va))
    n = 0
    while work:
        start, own = work.pop()
        if start in funcs or not (TEXT['va'] <= start < TEXT_END):
            continue
        f = dict(start=start, insns=[], calls=set(), tail=set(), unresolved=[], name=None)
        funcs[start] = f
        for nm, va, _ in exports:
            if va == start:
                f['name'] = nm
        va = start
        while TEXT['va'] <= va < TEXT_END:
            if va in insn_va:
                if va != start:
                    f['tail'].add(va)
                break
            buf = p.read(va, 16)
            if not buf:
                f['unresolved'].append(va)
                break
            one = next(md.disasm(buf, va, 1), None)
            if one is None:
                f['unresolved'].append(va)
                break
            insn_va[va] = one.size
            owner[va] = start
            f['insns'].append((va, one.size, one.mnemonic, one.op_str))
            mn = one.mnemonic
            ops = one.operands
            if mn == 'ret' or mn == 'retn':
                break
            if mn == 'jmp':
                if ops and ops[0].type == X86_OP_IMM:  # IMM
                    t = ops[0].imm & 0xFFFFFFFF
                    work.append((t, t))
                    f['tail'].add(t)
                else:
                    raw_jmp[va] = (mn, one.op_str, one)
                break
            if mn == 'call':
                if ops and ops[0].type == X86_OP_IMM:
                    t = ops[0].imm & 0xFFFFFFFF
                    work.append((t, t))
                    f['calls'].add(t)
                    if t in funcs and t != start:
                        pass
                else:
                    raw_jmp[va] = ('call', one.op_str, one)
                va += one.size
                continue
            if mn.startswith('j') and ops and ops[0].type == X86_OP_IMM and mn != 'jmp':
                t = ops[0].imm & 0xFFFFFFFF
                work.append((t, start))
                va += one.size
                continue
            if mn in ('int3', 'hlt', 'ud2'):
                break
            va += one.size
            n += 1
            if n > 400000:
                break


t0 = time.time()
run()
# second pass: any function discovered but never expanded because worklist dedup by funcs
with open('recdesc_stats.txt', 'w', encoding='utf-8') as fh:
    fh.write('text va 0x%08X - 0x%08X\n' % (TEXT['va'], TEXT_END))
    fh.write('functions %d\n' % len(funcs))
    fh.write('instructions %d\n' % len(insn_va))
    tot = sum(s for s in insn_va.values())
    fh.write('bytes covered %d (%.1f%% of .text)\n' % (tot, 100.0 * tot / TEXT['vsize']))
    un = [(f['start'], f['unresolved']) for f in funcs.values() if f['unresolved']]
    fh.write('funcs with undecodable byte: %d\n' % len(un))
    for s, u in un[:40]:
        fh.write('  0x%08X -> 0x%08X\n' % (s, u[0]))

with open('funcs.txt', 'w', encoding='utf-8') as fh:
    for s in sorted(funcs):
        f = funcs[s]
        fh.write('0x%08X %4d insns  calls %3d  %s\n' % (
            s, len(f['insns']), len(f['calls']), f['name'] or ''))

with open('indirect.txt', 'w', encoding='utf-8') as fh:
    for va in sorted(raw_jmp):
        mn, ops, ins = raw_jmp[va]
        fh.write('0x%08X %-5s %-40s reachable=%s owner=0x%08X bytes=%s\n' % (
            va, mn, ops, 'Y' if va in owner else 'N',
            owner.get(va, 0), ins.bytes.hex()))
print(open('recdesc_stats.txt', encoding='utf-8').read())
print('indirect sites:', len(raw_jmp))
print('elapsed %.1fs' % (time.time() - t0))
