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
regs = {}
rows = []
pcs = sorted(int(k, 16) for k in ins if 0x27400 <= int(k, 16) <= 0x27ea0)
for p in pcs:
    v = ins[hex(p)]
    sz, mn, o1, o2, kind = v[0], v[1], v[2] or '', v[3] or '', v[4]
    if mn.startswith('mov') and o1.startswith('#'):
        rows.append((p, mn, o1, o2))
    elif mn.startswith('mov') and o1 in ('r0', 'r0l', 'r0h') and o2.startswith('@'):
        rows.append((p, mn + '  <reg>', o1, o2))
print('--- immediate loads + reg stores ---')
for p, mn, o1, o2 in rows:
    print(f'0x{p:06X}  {mn:10} {o1:14} {o2}')
