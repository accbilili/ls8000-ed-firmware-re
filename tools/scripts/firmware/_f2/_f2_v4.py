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
ins={int(k,16):v for k,v in c['insns'].items()}
own=c['owner']
xs=sorted(a for a in ins if 0x29000<=a<0x29170)
print('first/last:',hex(xs[0]),hex(xs[-1]))
print([hex(a) for a in xs[:20]])
print('owners:',sorted({(hex(a),own.get(hex(a))) for a in xs}, key=lambda t:int(t[0],16))[:10])
