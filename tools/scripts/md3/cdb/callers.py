"""Callers of each command-class ctor / builder; emit cdb_sites table."""
import sys, os, json, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

CTORS = {
 0x1009FD10:'15a', 0x1009FE8F:'1A', 0x1009FEB0+0x10:'00a', 0x1009FEC0:'12',
 0x1009FF10:'16', 0x1009FF50:'1D', 0x1009FF90:'25', 0x1009FFE0:'24',
 0x100A0020:'15b', 0x100A00A0:'E0', 0x100A00E0:'E1', 0x100A0120:'1B',
 0x100A0160:'C1', 0x100AAE00:'C0', 0x100AAB40:'28', 0x100AABE0:'2A',
 0x100AAC40:'3C', 0x100AAC90:'3B',
}

def main():
    ins = sweep(TEXT_LO, TEXT_HI)
    calls = [(i.address, i.operands[0].imm) for i in ins
             if i.mnemonic == 'call' and i.operands and i.operands[0].type == X86_OP_IMM]
    import collections
    byx = collections.defaultdict(list)
    for a, t in calls: byx[t].append(a)
    # candidate ctor list: functions that store a .rdata ptr to [reg+0] and are called
    res = {}
    for t in sorted(byx):
        n = len(byx[t])
        if 1 <= n <= 40:
            res[t] = (n, byx[t][:40])
    # print callers for the known ctors
    for c, tag in sorted(CTORS.items()):
        cl = sorted(byx.get(c, []))
        print('ctor 0x%08X [%s] callers=%d %s' % (c, tag, len(cl), [hex(x) for x in cl[:12]]))
    json.dump({hex(k): v for k, v in byx.items()}, open('callers.json', 'w'))

if __name__ == '__main__':
    main()
