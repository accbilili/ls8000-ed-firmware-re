"""F5 复核 8：固件范围约束常量全形态搜索 + 0xD1 可达性。"""
import sys, collections
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

VALS = {15354: '0x40上限', 15353: '0x40上限-1', 450: '0x41/0xC1上限', 449: '450-1',
        3283: '0x42上限', 3282: '3283-1', 300: 'B3上界', 299: '300-1',
        0xFED4: '-300', 0x3BFA: '', 0x1C2: '', 0xCD3: '', 0x12C: '', 0x12B: ''}
ins = sweep(TEXT_LO, TEXT_HI)
print('== 常量全形态出现点（任意操作数、任意指令）')
found = collections.defaultdict(list)
for i in ins:
    for op in i.operands:
        if op.type == X86_OP_IMM and op.imm in VALS:
            found[op.imm].append(i)
for v in sorted(VALS):
    lst = found.get(v, [])
    print('  %-6d (0x%X) %-12s : %d 处' % (v, v & 0xFFFFFFFF, VALS[v], len(lst)))
    for i in lst[:14]:
        print('      0x%08X  %-9s %s' % (i.address, i.mnemonic, i.op_str))

print('\n== 比较类指令中的范围常量 (cmp 立即数)')
for i in ins:
    if i.mnemonic != 'cmp': continue
    for op in i.operands:
        if op.type == X86_OP_IMM and op.imm in VALS:
            print('  0x%08X  cmp %s   ; %d' % (i.address, i.op_str, op.imm))

print('\n== 0xD1 相关')
for i in ins:
    for op in i.operands:
        if op.type == X86_OP_IMM and op.imm == 0xD1:
            print('  0x%08X  %-9s %s' % (i.address, i.mnemonic, i.op_str))
            break
