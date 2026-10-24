import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg
import json,sys,re
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']; owner=c['owner']
fns=set(int(x,16) for x in sys.argv[2:])
reg=sys.argv[1]
for a,v in ins.items():
    if not isinstance(v,list): continue
    if owner.get(a) and int(owner[a],16) in fns:
        ops=[x for x in v[2:4] if isinstance(x,str)]
        if any(o.startswith('@'+reg) or reg in o for o in ops):
            print(f'0x{int(a,16):06X}  [fn 0x{int(owner[a],16):06X}]  {v[1]:<9} ' + ', '.join(ops))
