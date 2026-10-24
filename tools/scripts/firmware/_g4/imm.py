import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg
import json,sys
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']; owner=c['owner']
pat=sys.argv[1]
for a,v in ins.items():
    if not isinstance(v,list): continue
    s=' '.join(str(x) for x in v)
    if pat in s.lower():
        ops=', '.join(x for x in v[2:4] if x)
        print(f'0x{int(a,16):06X}  [fn 0x{int(owner[a],16):06X}]  {v[1]:<9} {ops}')
