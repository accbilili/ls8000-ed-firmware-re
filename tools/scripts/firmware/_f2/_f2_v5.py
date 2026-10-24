import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct
d=open(sample('LS8000_111_ROM.bin'),'rb').read(); B=0x10000
for i in range(20):
    o=0x3EAD4-B+4*i
    p=struct.unpack('>I',d[o:o+4])[0]
    s=''
    if B<=p<len(d)+B:
        e=d.find(b'\0', p-B)
        s=d[p-B:e-B].decode('latin1')
    print(' 0x%06X [%d] -> 0x%06X  %s'%(0x3EAD4+4*i,i,p,s))
