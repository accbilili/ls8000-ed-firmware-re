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
want={0x289B4:'A 片夹识别主体',0x27930:'?',0x27676:'?',0x274BC:'?',0x2753E:'?',0x2740A:'?',0x2ADCE:'走片驱动'}
hits={t:[] for t in want}
for o in range(0,len(d)-4,2):
    b=d[o]
    if b in (0x5E,0x5A):
        t=int.from_bytes(d[o+1:o+4],'big')
        if t in hits: hits[t].append((hex(o+B),'jsr' if b==0x5E else 'jmp'))
for t in sorted(hits): print(hex(t), want[t], hits[t])
