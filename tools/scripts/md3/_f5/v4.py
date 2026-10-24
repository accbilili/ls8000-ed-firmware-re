"""F5 复核 4：子功能码工厂的跳转表 + [x+0x454/456/458/45C] 的读写点。"""
import sys, struct, collections
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

def rd32(va):
    b = read(va, 4)
    return struct.unpack('<I', b)[0] if len(b) == 4 else None

print('== jmp table A (0x40..0x45) @0x100AA43C')
for k in range(6):
    print('   case 0x%02X -> 0x%08X' % (0x40 + k, rd32(0x100AA43C + 4 * k)))

print('\n== index table 0x100AA47C (idx for 0x81..0xB3, 51 bytes)')
raw = read(0x100AA47C, 51)
idxA = list(raw)
tblA = [rd32(0x100AA454 + 4 * v) for v in idxA]
seen = []
for k, v in enumerate(idxA):
    code = 0x81 + k
    tgt = tblA[k]
    print('   0x%02X idx=%d -> 0x%08X' % (code, v, tgt))
    seen.append((code, tgt))
# 反查每个目标处的 sub 常量
print('\n== 目标处写入的 sub 常量')
for code, tgt in seen:
    i = D(tgt)
    j = D(tgt + i.size) if i else None
    print('   0x%02X -> 0x%08X: %s %s | next: %s %s' %
          (code, tgt, i.mnemonic, i.op_str, j.mnemonic if j else '?', j.op_str if j else ''))

print('\n== jmp table B (0xC0..0xD1) @0x100AA4B0 / idx @0x100AA4C4')
raw2 = read(0x100AA4C4, 18)
for k, v in enumerate(list(raw2)):
    print('   0x%02X idx=%d -> 0x%08X' % (0xC0 + k, v, rd32(0x100AA4B0 + 4 * v)))

print('\n== 全部 [x+0x454/+0x456/+0x458/+0x45C] 访问')
ins = sweep(TEXT_LO, TEXT_HI)
for i in ins:
    hit = False
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.disp in (0x454, 0x456, 0x458, 0x45C):
            hit = True
    if hit:
        print('   0x%08X  %-9s %s' % (i.address, i.mnemonic, i.op_str))
