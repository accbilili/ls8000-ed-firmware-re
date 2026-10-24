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
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
B=0x10000
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']
print('hex 0x108F8-0x10960:')
o=0x108F8-B
for i in range(0,0x68,8):
    print(hex(0x108F8+i), d[o+i:o+i+8].hex(' '))
print()
for k,v in ins.items():
    s=' '.join(str(x) for x in v[2:4])
    if '46ff' in s.lower() or '4700' in s.lower():
        print(k,v)
