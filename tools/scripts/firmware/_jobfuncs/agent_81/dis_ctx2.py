"""展开 0x02C9E4-0x02CE80 区段（0x4202EC/0x4202FC 使用家族）与 0x02B0E8 附近。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

RANGES = [
    (0x02C9E4, 0x02CBA4, 'ctx_02C9E4'),
    (0x02CBA4, 0x02CC04, 'ctx_02CBA4'),
    (0x02CE44, 0x02CE74, 'ctx_02CE44'),
    (0x02B0E8, 0x02B11A, 'ctx_02B0E8'),
]
for lo, hi, name in RANGES:
    lines = []
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        pc = nxt if nxt > pc else pc + 2
    open(os.path.join(OUT, f'{name}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(name, len(lines))
