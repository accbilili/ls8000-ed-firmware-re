import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import json, sys
sys.path.insert(0, TOOLCHAIN_ROOT)
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
cfg = json.load(open(cfg('cfg_v4.json')))
ins = cfg['insns']

def raw(a0, a1):
    for a in range(a0, a1, 16):
        b = d[a - BASE:a - BASE + 16]
        print('0x%06X  %s  |%s|' % (a, ' '.join('%02X' % x for x in b),
              ''.join(chr(x) if 32 <= x < 127 else '.' for x in b)))

print('== 0x0108D0-0x0109A0 (dispatch-record table?)')
raw(0x108D0, 0x109A0)

print('== who references 0x010900-ish / 0x010920')
for a, v in ins.items():
    txt = ' '.join(str(x) for x in v[2:] if x)
    for t in ('0x10904', '0x10900', '0x108f', '0x1090'):
        if t in txt.lower():
            print(' ', t, a, v[1], v[2], v[3], v[4]); break

print('== all insns referencing key vars')
keys = ('0x4202a4', '0x4202a9', '0x4202b4', '0x4202a0', '0x4003fe', '0x4003fb', '0x4202b2')
for k in keys:
    hits = [(a, v[1], v[2], v[3]) for a, v in ins.items() if k in ' '.join(str(x) for x in v[2:4]).lower()]
    print('--', k, 'n=', len(hits))
    for h in sorted(hits)[:14]:
        print('   ', h)
