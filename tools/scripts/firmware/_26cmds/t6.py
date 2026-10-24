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
# function starts
starts=sorted(set(own.values()))
lo=0x25000; hi=0x26600
print('funcs in range:')
for s in starts:
    if lo<=int(s,16)<=hi: print('  ',s)
# who jumps to 0x25A56 / 0x25ADA / 0x25B2C
for t in ('0x25A56','0x25ADA','0x25B2C','0x25C4C','0x25B8A'):
    hits=[(a,v) for a,v in ins.items() if len(v)>5 and isinstance(v[5],str) and v[5].lower()==t.lower()]
    print('target',t,hits[:6])
