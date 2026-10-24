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
    if 'mov.w' in nm and 'r0 @0x400436' in ops:
        # look back 1 instr
        got = None
        for back in (2, 4, 6):
            if off - back < 0:
                continue
            r2 = dec(off - back)
            if r2 and r2[0] == back:
                got = (off - back + BASE, r2[1], r2[2])
                break
        m = None
        if got:
            m = re.search(r'#(0x[0-9a-f]+)', got[2])
        if m:
            const[int(m.group(1), 16)].append((off + BASE, got[0]))
        else:
            other.append((off + BASE, nm, ops, got))
    else:
        other.append((off + BASE, nm, ops, None))

print('=== constant writes to 0x400436 (index set) ===')
tot = 0
for k in sorted(const):
    print('idx 0x%02X (%3d) : %d writes  %s' % (k, k, len(const[k]),
          ', '.join('0x%06X' % a for a, _ in const[k][:8])))
    tot += len(const[k])
print('distinct const idx =', len(const), ' total writes =', tot)
print('sorted idx:', ' '.join('%02X' % k for k in sorted(const)))

print()
print('=== other / non-const writes ===')
for a, nm, ops, g in other:
    print('0x%06X  %-8s %-26s || %s' % (a, nm, ops, ('0x%06X %s %s' % g) if g else '-'))
