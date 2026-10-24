import sys, os
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *

def dump(lo, hi, label=''):
    print('==== %s 0x%08X-0x%08X' % (label, lo, hi))
    a = lo
    while a < hi:
        i = D(a)
        if i is None:
            print('  0x%08X  .byte 0x%02X' % (a, read(a, 1)[0])); a += 1; continue
        print('  0x%08X  %-8s %s' % (a, i.mnemonic, i.op_str))
        a += i.size

if __name__ == '__main__':
    lo = int(sys.argv[1], 16); n = int(sys.argv[2], 16)
    dump(lo, lo + n)
