"""F5 复核 6：固件约束常量 450/3283/300/15354 在主机侧的上下文。"""
import sys
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *

def back(va, n=18):
    for k in range(1, 80):
        s = va - k
        a = s; ins = []; ok = True
        while a < va:
            i = D(a)
            if i is None or a + i.size > va: ok = False; break
            ins.append(i); a += i.size
        if ok and ins and a == va:
            return ins[-n:]
    return []

def ctx(va, n=18, m=14):
    print('---- 0x%08X' % va)
    for i in back(va, n):
        print('   0x%08X  %-9s %s' % (i.address, i.mnemonic, i.op_str))
    a = va
    i = D(a)
    if i:
        print('   0x%08X  %-9s %s   <<<' % (a, i.mnemonic, i.op_str)); a += i.size
    for _ in range(m):
        i = D(a)
        if not i: break
        print('   0x%08X  %-9s %s' % (a, i.mnemonic, i.op_str)); a += i.size

for v in (0x100104E1, 0x1002A97C, 0x100A5DBB, 0x100A8AC7, 0x10096187, 0x10078200, 0x1004A9D8):
    ctx(v)
    print()
