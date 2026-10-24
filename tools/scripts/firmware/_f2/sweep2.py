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
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
B=0x10000
targets={0x2740A:0,0x274BC:0,0x2753E:0,0x27676:0,0x27930:0,0x289B4:0,0x28BB0:0,0x28E30:0,0x290A0:0}
hits={t:[] for t in targets}
for o in range(0,len(d)-4,2):
    if d[o]==0x5C:
        ads=o+B
        disp=struct.unpack('>h',d[o+2:o+4])[0]
        t=ads+4+disp
        if t in hits: hits[t].append(ads)
for t in sorted(hits): print('bsr->',hex(t),len(hits[t]),[hex(x) for x in hits[t]])
