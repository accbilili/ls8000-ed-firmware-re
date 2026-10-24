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
cfg=json.load(open(cfg('cfg_v4.json')))
ins=cfg['insns']; own=cfg['owner']
for a in ('0x25A56','0x25A6A','0x25B2C','0x25D08','0x264C2'):
    print(a, ins.get(a), own.get(a))
# instructions whose target points into 0x25a56..0x25b00
hits=[(a,v) for a,v in ins.items() if len(v)>5 and isinstance(v[5],str)]
for a,v in hits:
    t=int(v[5],16)
    if 0x25A00<=t<=0x25B40: print('ref',a,v)
