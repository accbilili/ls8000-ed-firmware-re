import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, re, collections
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)


def dec(off):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        return None
    return sz, nm, ' '.join(x for x in (a1, a2) if x)


const = collections.defaultdict(list)
other = []
for off in range(0, len(d) - 8, 2):
    r = dec(off)
    if r is None:
        continue
    sz, nm, ops = r
    if '400436' not in ops.lower():
        continue
    if nm == 'mov.w' and ops.strip() == 'r0 @0x400436':
        got = None
        for back in (2, 4, 6):
            if off - back < 0:
                continue
            r2 = dec(off - back)
            if r2 and r2[0] == back:
                got = (off - back + BASE, r2[1], r2[2])
                break
        ok = False
        if got and got[1] == 'mov.w':
            m = re.match(r'#(0x[0-9a-f]{4}) r0$', got[2].strip())
            if m:
                const[int(m.group(1), 16)].append((off + BASE, got[0]))
                ok = True
        if not ok:
            other.append((off + BASE, nm, ops, got))

print('=== VERIFIED constant writes to 0x400436 ===')
for k in sorted(const):
    addrs = ', '.join('0x%06X' % a for a, _ in const[k])
    print('idx 0x%02X (%3d) : %2d  %s' % (k, k, len(const[k]), addrs))
print('distinct =', len(const), sorted('%02X' % k for k in const))

print()
print('=== unverified / register writes ===')
for a, nm, ops, g in other:
    print('0x%06X  %-8s %-26s || %s' % (a, nm, ops, ('0x%06X %s %s' % g) if g else '-'))
