"""扫描 .text 中所有 [base+disp] 形式的访问，按 (base,disp,width,rw) 统计。
只做统计与定位，不 dump 全量反汇编。"""
import lmd as L
from capstone import x86
from collections import defaultdict, Counter

lo, hi = 0x10001000, 0x100BE000
insns = list(L._md.disasm(L.read(lo, hi - lo), lo))
print('insn count', len(insns))

# 收集：[ebp+disp] 的访问，宽度与读写
stat = defaultdict(Counter)     # disp -> Counter(width|rw)
where = defaultdict(list)       # disp -> [va]
for ins in insns:
    for op in ins.operands:
        if op.type != x86.X86_OP_MEM:
            continue
        m = op.mem
        if m.base != x86.X86_REG_EBP or m.index != 0:
            continue
        if not (0 <= m.disp <= 0x48):
            continue
        if ins.id in (x86.X86_INS_LEA,):
            rw, w = 'addr', 4
        elif ins.id in (x86.X86_INS_MOV, x86.X86_INS_MOVZX, x86.X86_INS_MOVSX) and op is ins.operands[0]:
            rw = 'r'
            w = op.size
        elif ins.id in (x86.X86_INS_MOV,):
            rw = 'w'
            w = op.size
        elif ins.id in (x86.X86_INS_CMP, x86.X86_INS_TEST):
            rw = 'r'
            w = op.size
        else:
            rw = 'w'
            w = op.size
        key = '%s%d' % (rw, w)
        stat[m.disp][key] += 1
        where[m.disp].append(ins.address)

for d in sorted(stat):
    print('ebp+0x%02X  %s' % (d, dict(stat[d])))
