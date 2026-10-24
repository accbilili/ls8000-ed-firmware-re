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
def refs(t):
    pat=t.to_bytes(4,'big'); i=0; out=[]
    while True:
        i=d.find(pat,i)
        if i<0: break
        out.append(i+BASE); i+=1
    return [hex(x) for x in out]
for t in (0x400316,0x400680,0x400C64,0x400C78,0x400C8C,0x400436,0x4007BE,0x4003FB,0x400EC6,0x400ECE):
    print(hex(t),refs(t))
