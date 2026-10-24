"""F6: 全 .text 线性扫描，找「同一 256B 窗口内同一基址寄存器同时出现 +0x14/+0x18/+0x1C/+0x20」的位置。"""
import sys, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_MEM

sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3')
from pe_md3 import PE

p = PE()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
WANT = (0x14, 0x18, 0x1C, 0x20)

win = collections.defaultdict(list)
va = TLO
while va < THI:
    buf = p.read(va, 16)
    if not buf:
        break
    one = next(md.disasm(buf, va, 1), None)
    if one is None:
        va += 1
        continue
    for i, op in enumerate(one.operands):
        if op.type == X86_OP_MEM and not op.mem.index:
            b = one.reg_name(op.mem.base) if op.mem.base else None
            if b and op.mem.disp in WANT:
                win[(va >> 8, b)].append((va, op.mem.disp, i, op.size, one.mnemonic + ' ' + one.op_str))
    va += one.size

rows = []
for k, v in win.items():
    offs = set(x[1] for x in v)
    if len(offs) >= 3:
        rows.append((len(offs), min(x[0] for x in v), k, v))
rows.sort(reverse=True)
print('候选窗口 %d 个' % len(rows))
for n, lo, k, v in rows[:40]:
    print('-' * 60)
    print('窗口 base=0x%08X reg=%s 覆盖 %d/4 个偏移' % (lo & ~0xFF, k[1], n))
    for x in sorted(v):
        print('   0x%08X  +0x%02X %s w%d  %s' % (x[0], x[1], 'dst' if x[2] == 0 else 'src', x[3], x[4]))
