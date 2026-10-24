import sys
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM

CONST = [15354, 450, 3283, 300, 0x3BFA, 0x1C2, 0xCD3, 0x12C, 15354-1, 3283-1]
ins = sweep(TEXT_LO, TEXT_HI)
print('insns', len(ins))
for i in ins:
    for op in i.operands:
        if op.type == X86_OP_IMM and op.imm in (0x3BFA, 0x1C2, 0xCD3, 0x12C):
            print('0x%08X  %-8s %s' % (i.address, i.mnemonic, i.op_str))
            break
