import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
def u16(a): o = a - BASE; return (d[o] << 8) | d[o+1]
print('table 0x03E390 dump:')
rows = []
for i in range(0, 100):
    a = 0x03E390 + i*4
    h, ix = u16(a), u16(a+2)
    rows.append((i, a, h, ix))
    if h == 0 and ix == 0 and i > 80:
        print(f'  [{i}] @0x{a:06X} host=0x{h:04X} idx=0x{ix:04X}  <-- terminator?')
        break
print('  count =', len(rows), 'last @', hex(rows[-1][1]))
print('  entry47:', rows[47])
print('  entry48:', rows[48])
print()
print('codes of interest present?')
want = {0x0E00, 0x0E10, 0x1100, 0x2000, 0x3000, 0x5000, 0x9000, 0x1000, 0x4000, 0x0000}
for i, a, h, ix in rows:
    if h in want:
        print(f'  host=0x{h:04X} -> idx={ix:3d} (0x{ix:02X})  [entry {i}] @0x{a:06X}')
