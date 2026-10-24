"""Function-entry resolution for arbitrary in-function VAs."""
import sys, os, pickle, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md3lib import *
from oracle import D, cfg, sweep

_pk = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calls.pkl')
CALLS = pickle.load(open(_pk,'rb'))['calls']

def ptr_targets():
    """dwords in .rdata/.data that point into .text"""
    out = set()
    for s in SECS:
        if s['name'] not in ('.rdata', '.data'): continue
        raw = DATA[s['roff']: s['roff']+s['rsize']]
        for i in range(0, len(raw)-3, 4):
            v = struct.unpack_from('<I', raw, i)[0]
            if TEXT_LO <= v < TEXT_HI:
                out.add(v)
    return out

PTRS = None
def entries():
    global PTRS
    if PTRS is None: PTRS = ptr_targets()
    return sorted({t for _, t in CALLS} | PTRS)

def callers_of(target):
    return sorted(a for a, t in CALLS if t == target)

def entry_of(va):
    """largest candidate entry <= va whose CFG covers va"""
    cands = [e for e in entries() if e <= va]
    for e in reversed(cands):
        if va - e > 0x8000:
            break
        if va in cfg(e):
            return e
    return None

if __name__ == '__main__':
    print('candidates', len(entries()), 'ptrs', len(PTRS))
    for a in (0x100A01A0, 0x1009FDB0, 0x100AAD00, 0x100A0230, 0x1009FE60):
        print('0x%08X -> 0x%08X' % (a, entry_of(a) or 0))
