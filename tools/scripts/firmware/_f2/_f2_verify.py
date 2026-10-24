import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg, sample
import json
c=json.load(open(cfg('cfg_v4.json')))
ins={int(k,16):v for k,v in c['insns'].items()}
own={int(k,16):v for k,v in c['owner'].items()}
lo,hi=0x28A00,0x28F00
addrs=sorted(a for a in ins if lo<=a<hi)
prev=None; holes=[]
for a in addrs:
    if prev is not None and a!=prev:
        holes.append((prev,a))
    prev=a+ (ins[a][0] if isinstance(ins[a][0],int) else 2)
print('holes:',[(hex(a),hex(b),b-a) for a,b in holes])
print('first',hex(addrs[0]),'last',hex(addrs[-1]))
print('owners in 28B00-28E68:',[(hex(a),hex(v)) for a,v in sorted(own.items()) if 0x28A00<=a<0x28F00])
d=open(sample('LS8000_111_ROM.bin'),'rb').read(); B=0x10000
for a in (0x28A2E,0x28AF2,0x28E34,0x28E36):
    print(hex(a), d[a-B:a-B+12].hex(' '))
print('tbl 3EEF0:')
import struct
for i in range(16):
    o=0x3EEF0-B+4*i
    v=struct.unpack('>I',d[o:o+4])[0]
    print(' ',hex(0x3EEF0+4*i),'code 0x%02X -> 0x%06X'%(0x10+i,v))
