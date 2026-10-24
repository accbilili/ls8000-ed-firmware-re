"""F6: 找 call [0x100C2578]（NkDriverEntry 函数指针）的所有站点，及其前置 push 序列。"""
import sys, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_MEM, X86_OP_IMM

sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3')
from pe_md3 import PE

p = PE()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
TARGET = 0x100C2578

sites = []
va = TLO
while va < THI:
    buf = p.read(va, 16)
    if not buf:
        break
    one = next(md.disasm(buf, va, 1), None)
    if one is None:
        va += 1
        continue
    if one.mnemonic in ('call', 'jmp'):
        op = one.operands[0]
        if op.type == X86_OP_MEM and op.mem.disp == TARGET and not op.mem.index:
            sites.append(va)
    va += one.size

print('站点数 %d' % len(sites))
for s in sites:
    print('=' * 60)
    print('site 0x%08X' % s)
    lo = s - 0x40
    va = lo
    while va < s:
        b = p.read(va, 16)
        one = next(md.disasm(b, va, 1), None)
        if one is None:
            va += 1
            continue
        print('   0x%08X  %-8s %s' % (va, one.mnemonic, one.op_str))
        va += one.size
