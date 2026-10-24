import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg, sample
import json,struct
c=json.load(open(cfg('cfg_v4.json')))
own=c['owner']
print('owners 28A00-28F00:',[(k,v) for k,v in sorted(own.items(),key=lambda t:int(t[0],16)) if 0x28A00<=int(k,16)<0x28F00])
d=open(sample('LS8000_111_ROM.bin'),'rb').read(); B=0x10000
for a in (0x28A2E,0x28AF2,0x28E34,0x28E36):
    print(hex(a), d[a-B:a-B+12].hex(' '))
for i in range(16):
    o=0x3EEF0-B+4*i
    v=struct.unpack('>I',d[o:o+4])[0]
    print(' 0x%06X code 0x%02X -> 0x%06X'%(0x3EEF0+4*i,0x10+i,v))
print('3EE70 doubles:')
for i in range(16):
    o=0x3EE70-B+8*i
    print('  0x%02X %s'%(0x10+i,struct.unpack('>d',d[o:o+8])[0]))
