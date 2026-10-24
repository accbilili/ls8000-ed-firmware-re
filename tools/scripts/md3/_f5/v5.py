"""F5 复核 5：vtable 0x100C2F58 / 工厂 callers / [x+0x64] 写入点。"""
import sys, struct, collections
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

def rd32(va):
    b = read(va, 4)
    return struct.unpack('<I', b)[0] if len(b) == 4 else None

VT = 0x100C2F58
print('== vtable 0x%08X' % VT)
for k in range(16):
    v = rd32(VT + 4 * k)
    print('   slot 0x%02X -> 0x%08X' % (k * 4, v))

BUILDERS = {0x100A0230: 'E0', 0x100A0260: 'E1', 0x100A0190: 'C1', 0x100A01A0: '12',
            0x100A01D0: '25', 0x100A0210: '24', 0x100A0290: '1B', 0x100AAD00: '28',
            0x100AAD50: '2A', 0x100AAD80: '3C', 0x100AADC0: '3B', 0x100AAE20: 'C0',
            0x1009FDB0: '15a', 0x100A0070: '15b', 0x1009FE60: '1A', 0x1009FEB0: '00',
            0x1009FF40: '16', 0x1009FF80: '1D'}
for k in range(16):
    v = rd32(VT + 4 * k)
    if v in BUILDERS:
        print('   >>> slot 0x%02X = %s builder 0x%08X' % (k * 4, BUILDERS[v], v))

ins = sweep(TEXT_LO, TEXT_HI)
print('\n== mov [x+0x64], <src>  (CDB[2] 源字段 0x64)')
for i in ins:
    if i.mnemonic != 'mov' or len(i.operands) != 2: continue
    d, s = i.operands
    if d.type != X86_OP_MEM or d.mem.disp != 0x64: continue
    src = ('0x%X' % s.imm) if s.type == X86_OP_IMM else (
        'reg:' + i.reg_name(s.reg) if s.type == X86_OP_REG else 'mem')
    print('   0x%08X  %-9s %-30s ; src=%s size=%d' % (i.address, i.mnemonic, i.op_str, src, d.size))

print('\n== callers of factory 0x100AA1D0')
for i in ins:
    if i.mnemonic == 'call' and i.operands and i.operands[0].type == X86_OP_IMM:
        if i.operands[0].imm == 0x100AA1D0:
            print('   0x%08X' % i.address)
