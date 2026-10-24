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
from h8dis import H8
from h8tab import load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

TAB = 0x01914A
N = 143

print('=== TABLE 0x01914A  %d entries ===' % N)
for i in range(N):
    off = TAB + i * 5 - BASE
    b = d[off:off + 5]
    print('%3d  0x%06X  %02X %02X %02X %02X %02X' % (i, TAB + i * 5, b[0], b[1], b[2], b[3], b[4]))

print()
print('=== tail after table ===')
off = TAB + N * 5 - BASE
print('0x%06X: %s' % (TAB + N * 5, ' '.join('%02X' % c for c in d[off:off + 32])))
print('0x%06X: %s' % (TAB + N * 5 - 20, ' '.join('%02X' % c for c in d[off - 20:off + 12])))

print()
print('=== immediate refs to 0x0001914A ===')
pat = bytes([0x00, 0x01, 0x91, 0x4A])
idx = 0
while True:
    p = d.find(pat, idx)
    if p < 0:
        break
    idx = p + 1
    # try decode a window backwards to find an instruction boundary containing p..p+3
    found = None
    for back in range(0, 10):
        st = p - back
        if st < 0:
            break
        pc = st
        for _ in range(4):
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                break
            ops = ' '.join(x for x in (a1, a2) if x)
            if pc <= p and pc + sz >= p + 4:
                if '1914a' in ops.lower() or '1914A' in ops:
                    found = (pc, nm, ops)
                    break
            pc = nxt
        if found:
            break
    if found:
        print('0x%06X  %s  %s' % (found[0] + BASE, found[1], found[2]))
    else:
        print('0x%06X  (no aligned instr)' % (p + BASE))
