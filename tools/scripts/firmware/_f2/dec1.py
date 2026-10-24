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
for a in (0x28BB0,0x28BFE,0x28BB6,0x28C10,0x28C0,0x27670):
    sz,nm,a1,a2,nxt=h.decode(a-B)
    print(hex(a),'size',sz,'next',hex(nxt+B) if nxt is not None else None,nm,a1,a2,d[a-B:a-B+6].hex(' '))
