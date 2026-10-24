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
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000

def raw(a0, a1):
    for a in range(a0, a1, 16):
        b = d[a - BASE:a - BASE + 16]
        print('0x%06X  %s  |%s|' % (a, ' '.join('%02X' % x for x in b),
              ''.join(chr(x) if 32 <= x < 127 else '.' for x in b)))

print('== 0x3EDF0-0x3EE60')
raw(0x3EDF0, 0x3EE60)
print('== 0x4003F0-0x400400 (0x4003FB neighbours)')
raw(0x4003F0, 0x400400)

print('== word table view 0x3EE10 + 2*k')
for k in range(0, 20):
    a = 0x3EE10 + 2 * k
    w = (d[a - BASE] << 8) | d[a - BASE + 1]
    print('k=%2d (0x%02X) addr=0x%06X word=%5d 0x%04X' % (k, k, a, w, w))

print("== callers context: 0x10920-0x10950, 0x10AE0-0x10B00")
raw(0x10920, 0x10950)
raw(0x10AE0, 0x10B00)
