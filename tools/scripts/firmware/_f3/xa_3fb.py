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
print('--- insns referencing 0x4003fb / 0x4003fc ---')
for k in sorted(ins, key=lambda x: int(x, 16)):
    v = ins[k]
    s = ' '.join(x for x in v[2:4] if x)
    if '0x4003fb' in s or '0x4003fc' in s:
        print(f'0x{int(k,16):06X}  {v[1]:8} {s:26} in {d["owner"].get(k)}')
