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
print('base',cfg['base'])
print('n insns',len(cfg['insns']), 'n owner',len(cfg['owner']),'n handlers',len(cfg['handlers']))
k=list(cfg['insns'].items())[:3]; print(k)
k=list(cfg['owner'].items())[:5]; print(k)
k=list(cfg['handlers'].items())[:5]; print(k)
