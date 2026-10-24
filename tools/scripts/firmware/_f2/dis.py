import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
B=0x10000
h=H8(d, load_entries(sample('h8.lst')), base=B)
def dis(lo,hi,limit=400):
    pc=lo; n=0
    while pc<hi and n<limit:
        sz,nm,a1,a2,nxt=h.decode(pc-B)
        nxt+=B
        if nm is None or nxt<=pc or sz>8:
            print('%06X  %-24s .byte 0x%02X'%(pc,' '.join('%02X'%b for b in d[pc-B:pc-B+2]),d[pc-B])); pc+=2; continue
        ops=', '.join(x for x in (a1,a2) if x)
        print('%06X  %-24s %-9s %s'%(pc,' '.join('%02X'%b for b in d[pc-B:nxt-B]), 'bra*' if nm=='bt' else nm, ops))
        pc=nxt; n+=1
if __name__=='__main__':
    import sys
    lo=int(sys.argv[1],16); hi=int(sys.argv[2],16)
    dis(lo,hi)
