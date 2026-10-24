"""Map any function VA to its vtable slot and owning class ctor."""
import sys, os, struct, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

def rd32(va):
    b = read(va, 4)
    return struct.unpack('<I', b)[0] if len(b) == 4 else None

def load():
    rows = json.load(open('vt_rows2.json'))
    vts = {}                       # vtable base -> ctor
    for r in rows:
        vts.setdefault(r['vtable'], r['ctor'])
    # index data dwords -> va
    idx = collections.defaultdict(list)
    for s in SECS:
        if s['name'] != '.rdata': continue
        raw = DATA[s['roff']:s['roff']+s['rsize']]
        for i in range(0, len(raw)-3, 4):
            v = struct.unpack_from('<I', raw, i)[0]
            if TEXT_LO <= v < TEXT_HI:
                idx[v].append(s['va']+i)
    return vts, idx, rows

def where(fn):
    vts, idx, rows = load()
    out = []
    for d in idx.get(fn, []):
        cands = [x for x in vts if x <= d < x + 0x28]
        if cands:
            x = max(cands)
            out.append((x, d - x, vts[x]))
        else:
            out.append((None, d, None))
    return out

if __name__ == '__main__':
    for fn in (0x100A5FA0, 0x100AA1D0, 0x100A3F30, 0x100A4270, 0x100A4320,
               0x100A44D0, 0x100A6A00, 0x1009FDE0):
        print('0x%08X -> %s' % (fn, [('vt=0x%08X slot=0x%X ctor=0x%08X' % (a, o, c) if a else 'data=0x%08X' % o) for a, o, c in where(fn)]))
