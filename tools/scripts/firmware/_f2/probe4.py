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
def q(a):
    o=a-B
    raw=d[o:o+8]
    return raw.hex(), struct.unpack('>d',raw)[0]
for a in (0x3EDE0,0x3EF30,0x3EF38,0x3EF40,0x3EF48,0x3EF50,0x3EF58,0x3EF60,0x3EF68,0x3EF70,0x3EF78):
    print(hex(a),q(a))
print()
v=struct.unpack('>d',d[0x3EDE0-B:0x3EDE0-B+8])[0]
g=struct.unpack('>d',d[0x3EF38-B:0x3EF38-B+8])[0]
print('prod',repr(v*g),'trunc',int(v*g),'round',round(v*g))
for x in (10.0,11.5,8.0,1.7,26.0,15.5,22.3,12.5):
    print(x, repr(v*x), int(v*x), hex(int(v*x)))
print('5480/157.4803=',5480/v, 5479/v, 3511/v, 3512/v)
print('1968/v=',1968/v)
print('bytes @28af0..:',d[0x28af0-B:0x28b00-B].hex(' '))
print('bytes @28e2e..:',d[0x28e2e-B:0x28e46-B].hex(' '))
