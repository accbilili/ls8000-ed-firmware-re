"""带重同步的线性扫描 + 结构体字段共现分析。"""
import lmd as L
from capstone import x86
from collections import defaultdict, Counter

LO, HI = 0x10001000, 0x100BE000
code = L.read(LO, HI - LO)
insns = []
off = 0
n = len(code)
while off < n:
    got = False
    for ins in L._md.disasm(code[off:off + 16], LO + off):
        insns.append(ins)
        off += ins.size
        got = True
        break
    if not got:
        off += 1
print('insn count', len(insns))

REGS = {'ebp': x86.X86_REG_EBP, 'esi': x86.X86_REG_ESI, 'edi': x86.X86_REG_EDI,
        'ebx': x86.X86_REG_EBX, 'eax': x86.X86_REG_EAX}

def access(ins):
    """返回 [(regname, disp, width, rw)]"""
    out = []
    if not ins.operands:
        return out
    for i, op in enumerate(ins.operands):
        if op.type != x86.X86_OP_MEM or op.mem.index != 0:
            continue
        base = None
        for k, v in REGS.items():
            if op.mem.base == v:
                base = k
        if base is None:
            continue
        if ins.id == x86.X86_INS_LEA:
            rw = 'a'
        elif ins.id in (x86.X86_INS_CMP, x86.X86_INS_TEST):
            rw = 'r'
        elif i == 0 and ins.id in (x86.X86_INS_MOV, x86.X86_INS_MOVZX, x86.X86_INS_MOVSX):
            rw = 'r'
        elif i == 0:
            rw = '?'
        else:
            rw = 'w'
        out.append((base, op.mem.disp & 0xffffffff, op.size, rw))
    return out

# 按 (base, disp) 统计宽度/读写
stat = defaultdict(Counter)
locs = defaultdict(list)
for ins in insns:
    for (b, d, w, rw) in access(ins):
        if d > 0x8000:  # 负偏移
            continue
        stat[(b, d)]['%s%d' % (rw, w)] += 1
        locs[(b, d)].append(ins.address)

import json
out = {}
for k in sorted(stat):
    out['%s+0x%X' % k] = {'cnt': dict(stat[k]), 'n': sum(stat[k].values())}
json.dump(out, open('field_stat.json', 'w'), indent=0)
print('written field_stat.json', len(out))

# 目标偏移集合
TARGET = {0x14, 0x18, 0x1C, 0x20, 0x10, 0x0C, 0x24, 0x28}
for b in ('esi', 'edi', 'ebx', 'ebp'):
    print('== base', b)
    for d in sorted(TARGET):
        c = stat.get((b, d))
        if c:
            print('   +0x%02X %s  n=%d  样例 %s' % (d, dict(c), sum(c.values()),
                  ' '.join(hex(x) for x in locs[(b, d)][:6])))
