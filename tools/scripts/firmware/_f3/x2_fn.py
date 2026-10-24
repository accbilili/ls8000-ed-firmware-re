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
pcs = sorted(int(k,16) for k in ins)
# 1) function starts (owner[k]==k) in 0x27000..0x27a00
starts = [p for p in pcs if d['owner'].get(hex(p)) == hex(p) and 0x27000 <= p <= 0x27b00]
print('fn starts:', [hex(x) for x in starts])
print('gap before 0x2740A:')
for p in pcs:
    if 0x273c0 <= p <= 0x27420:
        v = ins[hex(p)]
        print(f'  0x{p:06X} {v[1]:8} {v[2] or "":12} {v[3] or ""}')
print()
print('entry text at 0x27670 / 0x2740a / 0x27532:')
for k in ['0x27670','0x2740a','0x27532','0x27538']:
    print('  ', k, ins.get(k))
