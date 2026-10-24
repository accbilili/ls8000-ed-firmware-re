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
print('--- refs to 0x400c55 ---')
for k,v in ins.items():
    if '400c55' in ' '.join(str(x) for x in v[2:5]).lower():
        print(k,v,'owner',own.get(k))
print('--- refs to 0x4206ec (E0 busy flag?) ---')
n=0
for k,v in sorted(ins.items(), key=lambda t:int(t[0],16)):
    if '4206ec' in ' '.join(str(x) for x in v[2:5]).lower():
        print(k,v,'owner',own.get(k)); n+=1
        if n>12: break
