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
for pat in ('400d86','400d7e','400d84','42029e'):
    print('===',pat)
    for k,v in sorted(ins.items(), key=lambda t:int(t[0],16)):
        if pat in ' '.join(str(x) for x in v[1:4]).lower():
            print('  0x%s %-8s %-20s %-11s owner=%s'%(k[2:].rjust(6,'0'),v[1],str(v[2]),str(v[3]),own.get(k)))
