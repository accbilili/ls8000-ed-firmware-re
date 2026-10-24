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
def find32(v):
    p=struct.pack('>I',v); out=[]; i=d.find(p)
    while i!=-1: out.append(i+B); i=d.find(p,i+1)
    return out
def find24(v):
    p=bytes([(v>>16)&0xff,(v>>8)&0xff,v&0xff]); out=[]; i=d.find(p)
    while i!=-1: out.append(i+B); i=d.find(p,i+1)
    return out
for v in (0x274BC,0x2753E,0x27676,0x27930,0x2799C,0x289B4,0x28E30,0x290A0,0x2D700):
    print(hex(v),'32bit:',[hex(x) for x in find32(v)][:8],'24bit:',len(find24(v)),[hex(x) for x in find24(v)][:6])
print()
print('tbl 0x3EDB8:', d[0x3EDB8-B:0x3EE00-B].hex(' '))
print('tbl 0x3E2E8:', d[0x3E2E8-B:0x3E338-B].hex(' '))
