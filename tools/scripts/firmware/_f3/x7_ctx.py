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
def ctx(addr, n=8, tag=''):
    print(f'--- {tag} around 0x{addr:06X}')
    pcs = [int(k,16) for k in ins if addr-0x40 <= int(k,16) <= addr+0x20]
    for p in sorted(pcs):
        v = ins[hex(p)]
        mark = ' <<<' if p == addr else ''
        print(f'  0x{p:06X} {v[1]:8} {(v[2] or ""):14} {(v[3] or "")}{mark}')
for a, t in [(0x0285E2,'2842c'), (0x02B02C,'2aff4'), (0x02CC22,'2cc04'), (0x0275C8,'2753e'), (0x0216E6,'2159c')]:
    ctx(a, 8, t)
