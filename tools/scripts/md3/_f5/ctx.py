import sys, os, json
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *

def back(va, n=14):
    """linear-decode backwards by trying increasing start offsets"""
    for k in range(1, 60):
        s = va - k
        ins = []
        a = s
        ok = True
        while a < va:
            i = D(a)
            if i is None or a + i.size > va:
                ok = False; break
            ins.append(i); a += i.size
        if ok and ins and a == va:
            return ins[-n:]
    return []

def ctx(va, n=14, m=3):
    print('--- call at 0x%08X' % va)
    for i in back(va, n):
        print('   0x%08X  %-8s %s' % (i.address, i.mnemonic, i.op_str))
    a = va
    i = D(a)
    if i:
        print('   0x%08X  %-8s %s   <<<' % (a, i.mnemonic, i.op_str))
        a += i.size
    for _ in range(m):
        i = D(a)
        if not i: break
        print('   0x%08X  %-8s %s' % (a, i.mnemonic, i.op_str)); a += i.size

if __name__ == '__main__':
    cal = json.load(open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb\callers.json'))
    tgt = int(sys.argv[1], 16)
    key = '0x%x' % tgt
    sites = cal.get(key) or []
    print('target 0x%08X callers=%d' % (tgt, len(sites)))
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    for s in sites[:lim]:
        ctx(s)
