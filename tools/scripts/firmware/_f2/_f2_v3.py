import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg
import json
c=json.load(open(cfg('cfg_v4.json')))
ins={int(k,16) for k in c['insns']}
for a in (0x290A0,0x290E0,0x290F4,0x2915C,0x29160):
    print(hex(a), a in ins)
print('in 29000-29170:', len([a for a in ins if 0x29000<=a<0x29170]))
