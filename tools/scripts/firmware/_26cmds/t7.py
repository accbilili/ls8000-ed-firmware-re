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
for t in (0x25A56,0x25B2C,0x25CC0,0x25ADA):
    pat=t.to_bytes(4,'big'); i=0; hits=[]
    while True:
        i=d.find(pat,i)
        if i<0:break
        hits.append(hex(i+BASE)); i+=1
    print(hex(t),hits)
