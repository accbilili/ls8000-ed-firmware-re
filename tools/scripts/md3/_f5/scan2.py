import sys, os, json
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

SUBS = {0x40,0x41,0x42,0x80,0x81,0x91,0x92,0xA0,0xB0,0xB3,0xC1,0xD0,0xD1}

def main():
    ins = sweep(TEXT_LO, TEXT_HI)
    print('total insns', len(ins))
    # 1) direct CDB[2] = [reg+0xa] imm
    print('\n== A: byte store [reg+0xa], imm (CDB[2])')
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type == X86_OP_MEM and d.size == 1 and s.type == X86_OP_IMM and s.imm in SUBS:
            if 0 <= d.mem.disp <= 0x20:
                print('  0x%08X  %-6s %s   ; imm=0x%02X disp=0x%X' % (i.address, i.mnemonic, i.op_str, s.imm, d.mem.disp))
    # 2) word store [reg+0x456]
    print('\n== B: store to [reg+0x456] (subfunc slot)')
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type == X86_OP_MEM and d.mem.disp == 0x456:
            v = ('0x%X' % s.imm) if s.type == X86_OP_IMM else ('reg:'+i.reg_name(s.reg) if s.type == X86_OP_REG else 'mem')
            print('  0x%08X  %-6s %s   ; src=%s' % (i.address, i.mnemonic, i.op_str, v))
    # 3) imm 0xd1 anywhere
    print('\n== C: immediate 0xD1 as byte-store source (any disp)')
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if s.type == X86_OP_IMM and s.imm == 0xD1 and d.type == X86_OP_MEM and d.size == 1:
            print('  0x%08X  %-6s %s' % (i.address, i.mnemonic, i.op_str))

main()
