"""F5 复核 1：用 request+0x14(长度)/+0x18(CDB 指针) 配对重新独立定位 CDB 构造点。"""
import sys, os, json, struct, collections
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

ins = sweep(TEXT_LO, TEXT_HI)
print('insns =', len(ins))

# A. 所有 [reg+0x14] <- imm  且  [reg+0x18] <- imm  的函数（同一函数内配对）
LENIMM = {}
for i in ins:
    if i.mnemonic != 'mov' or len(i.operands) != 2: continue
    d, s = i.operands
    if d.type == X86_OP_MEM and s.type == X86_OP_IMM and d.mem.disp == 0x14:
        LENIMM.setdefault(i.address, (i.reg_name(d.mem.base) if d.mem.base else 'abs', s.imm))
print('[x+0x14]<-imm 总数:', len(LENIMM))
for a, (b, v) in sorted(LENIMM.items()):
    print('  0x%08X  [%s+0x14] = 0x%X (%d)' % (a, b, v, v))
