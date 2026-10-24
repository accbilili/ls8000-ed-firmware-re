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
d = json.load(open(cfg('cfg_v4.json')))
ins = d['insns']
def dump(start, maxn=44, label=''):
    print(f'===== {label} 0x{start:06X} =====')
    p = start
    for _ in range(maxn):
        v = ins.get(hex(p))
        if v is None:
            print(f'  0x{p:06X}  <gap>'); return
        print(f'  0x{p:06X}  {v[1]:8} {(v[2] or ""):14} {(v[3] or "")}')
        p += v[0]
        if v[1] in ('rts','jmp'): return
for a,l in [(0x028148,'28148'),(0x02896C,'2896C'),(0x0281B2,'281B2')]:
    dump(a,40,l)
