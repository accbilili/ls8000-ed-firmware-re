import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg
import json, sys
d = json.load(open(cfg('cfg_v4.json')))
ins = d['insns']
for k in ['0x2753e','0x27544','0x2755e','0x27676','0x276ee','0x27dc4']:
    print(k, repr(ins.get(k)))
print('--- count in region', sum(1 for k in ins if 0x27400 <= int(k,16) <= 0x27a60))
