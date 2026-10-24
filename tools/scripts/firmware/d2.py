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
BASE=0x10000
h=H8(d, load_entries(sample('h8.lst')), base=BASE)
def dis(a0,a1,out):
    pc=a0-BASE
    while pc < a1-BASE:
        sz,nm,o1,o2,nxt=h.decode(pc)
        if nm is None:
            out.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc+=2; continue
        out.append(f'0x{pc+BASE:06X}  {nm:<9} '+', '.join(x for x in (o1,o2) if x))
        pc=nxt
if __name__=='__main__':
    a0=int(sys.argv[1],16); a1=int(sys.argv[2],16)
    out=[]
    dis(a0,a1,out)
    print('\n'.join(out))
