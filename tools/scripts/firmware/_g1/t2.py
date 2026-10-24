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

# scan 3-byte pattern 01 91 4A (abs24 / imm24 low) and validate by decoding
pat = bytes([0x01, 0x91, 0x4A])
seen = set()
idx = 0
while True:
    p = d.find(pat, idx)
    if p < 0:
        break
    idx = p + 1
    found = None
    for back in range(0, 12):
        st = p - back
        if st < 0:
            break
        pc = st
        for _ in range(5):
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                break
            ops = ' '.join(x for x in (a1, a2) if x)
            if pc <= p and pc + sz >= p + 3:
                if '1914a' in ops.lower():
                    found = (pc, nm, ops)
                    break
            pc = nxt
        if found:
            break
    if found and found[0] not in seen:
        seen.add(found[0])
        print('0x%06X  %-8s %s' % (found[0] + BASE, found[1], found[2]))
    elif not found:
        print('0x%06X  (unaligned)' % (p + BASE))

print()
print('=== bytes before table ===')
for a in range(0x019100, 0x01914A, 16):
    off = a - BASE
    print('0x%06X: %s' % (a, ' '.join('%02X' % c for c in d[off:off + 16])))
