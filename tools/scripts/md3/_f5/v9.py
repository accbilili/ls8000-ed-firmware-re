"""F5 复核 9：0xD1 可达性 —— 命令包装函数入口/调用者 + push 0xD1 现场。"""
import sys, json, collections
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

ins = sweep(TEXT_LO, TEXT_HI)
byaddr = {i.address: i for i in ins}
order = sorted(byaddr)

def entry_of(va, lim=0x400):
    idx = order.index(va); j = idx; start = va
    while j > 0 and va - order[j] < lim:
        p = order[j - 1]
        m = byaddr[p].mnemonic
        if m.startswith('ret') or m in ('nop', 'int3'):
            start = order[j]; break
        j -= 1
    return start

W = 0x100A1F07
e = entry_of(W)
print('包装函数入口 = 0x%08X (含 0x%08X)' % (e, W))

cal = json.load(open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb\callers.json'))
cl = cal.get('0x%x' % e, [])
print('调用者 %d 处: %s' % (len(cl), ['0x%08X' % x for x in cl]))

print('\n== push 0xD1 现场')
for v in (0x1001CFBF, 0x10037EEF, 0x100577A5, 0x10064F6F, 0x1007C21A):
    print('--- 0x%08X' % v)
    a = v
    for _ in range(10):
        i = byaddr.get(a)
        if i is None: break
        print('   0x%08X  %-9s %s' % (a, i.mnemonic, i.op_str))
        if i.mnemonic.startswith('ret'): break
        a += i.size
    # 回退 8 条
    out = []
    idx = order.index(v); j = idx
    while j > 0 and v - order[j] < 60:
        out.append(order[j]); j -= 1
    for x in sorted(out)[-8:]:
        i = byaddr[x]
        print('   0x%08X  %-9s %s  (前)' % (x, i.mnemonic, i.op_str))
