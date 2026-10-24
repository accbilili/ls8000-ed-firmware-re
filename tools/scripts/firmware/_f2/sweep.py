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
targets={0x2740A,0x274BC,0x2753E,0x27676,0x27930,0x289B4,0x28BB0,0x28E30,0x290A0}
print('== 5E abs24 (jsr) ==')
for t in sorted(targets):
    p=b'\x5E'+bytes([(t>>16)&0xff,(t>>8)&0xff,t&0xff])
    i=d.find(p); hits=[]
    while i!=-1:
        hits.append(i+B); i=d.find(p,i+1)
    print(hex(t),len(hits),[hex(x) for x in hits][:10])
print('== 5C bsr d16 ==')
for t in sorted(targets):
    hits=[]
    for o in range(0,len(d)-4,2):
        if d[o]==0x5C:
            ads=o+B
            disp=struct.unpack('>h',d[o+2:o+4])[0]
            if ads+2+disp==t: hits.append(ads)
    print(hex(t),len(hits),[hex(x) for x in hits][:12])
