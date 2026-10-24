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
ins=c['insns']; own=c['owner']
print('0x27670:',ins.get('0x27670'))
for k in sorted((int(x,16) for x in ins)):
    if 0x27510<=k<=0x27570 or 0x27650<=k<=0x27690:
        v=ins['0x%x'%k]
        print(f'0x{k:06X} {v[1]:<8}{str(v[2]):<14}{str(v[3]):<10}tag={v[4]:<6}owner={own.get("0x%x"%k)}')
