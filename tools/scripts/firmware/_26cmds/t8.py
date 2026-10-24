import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
BASE=0x10000
for a in (0x25D76,0x25D80,0x25AF0,0x25B36):
    o=a-BASE
    print(hex(a),' '.join(f'{b:02X}' for b in d[o:o+4]))
