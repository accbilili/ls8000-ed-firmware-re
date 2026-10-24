"""dump 传参链关键指令字节，推断 CPU 寄存器配对。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

spots = [
    0x02B87C, 0x02B880, 0x02B8A4, 0x02B8B2, 0x02B8B4, 0x02B8C2, 0x02B8C4, 0x02B8C8, 0x02B8CA,
    0x02B8D6, 0x02B8D8,
    0x02B8EA, 0x02B8EE, 0x02B8F0, 0x02B8F2, 0x02B93A, 0x02B942, 0x02B948, 0x02B94A, 0x02B94C,
    0x02B94E, 0x02B950, 0x02B952, 0x02B954,
    0x02B276, 0x02B27A, 0x02B27C, 0x02B286, 0x02B296, 0x02B29C, 0x02B2A2, 0x02B2A8, 0x02B2AE,
    0x02C9E4, 0x02C9F2, 0x02C9F4, 0x02CA5C, 0x02CA60, 0x02CA62, 0x02CA64,
    0x02BE32, 0x02BE46, 0x02BE48, 0x02BE4A, 0x02BE4C, 0x02BE52, 0x02BEBA, 0x02BEC0,
    0x018E1E, 0x018E22, 0x018E24, 0x018E26, 0x018E28, 0x018E2A, 0x018E2C, 0x018E2E,
]
for a in spots:
    sz, nm, a1, a2, nxt = h.decode(a - BASE)
    raw = ' '.join(f'{b:02X}' for b in d[a-BASE:a-BASE+sz])
    print(f'0x{a:06X} [{raw:<16}] {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
