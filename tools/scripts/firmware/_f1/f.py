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
from h8dis import H8
from h8tab import load_entries
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def dump(a0, a1, label=''):
    print('; ---- %s 0x%06X - 0x%06X' % (label, a0, a1))
    pc = a0 - BASE
    while pc < a1 - BASE:
        sz, nm, x1, x2, nxt = h.decode(pc)
        if nm is None:
            print('0x%06X  .byte 0x%02X' % (pc + BASE, d[pc])); pc += 2; continue
        print('0x%06X  %-9s %s' % (pc + BASE, nm, ', '.join(x for x in (x1, x2) if x)))
        pc = nxt

dump(0x039D30, 0x039D70, 'writes 0x4202b2')
cfg = json.load(open(cfg('cfg_v4.json')))
ins = cfg['insns']
print('== any imm operand in 0x4202a8..0x4202c4')
for a, v in sorted(ins.items(), key=lambda t: int(t[0], 16)):
    t = ' '.join(str(x) for x in v[2:4]).lower()
    for k in range(0x4202a8, 0x4202c5, 2):
        if '0x%06x' % k in t:
            print(' ', a, v[1], v[2], v[3]); break
