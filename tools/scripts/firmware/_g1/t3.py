import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, re
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

# find all instructions whose operands mention 0x400436
hits = []
for off in range(0, len(d) - 8, 2):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        continue
    ops = ' '.join(x for x in (a1, a2) if x)
    if '400436' in ops.lower():
        hits.append((off + BASE, sz, nm, ops))

# dedupe overlapping by keeping first from a linear sweep of a plausible window
print('=== raw candidates %d ===' % len(hits))
# filter: keep those reachable by a linear decode from a nearby function-ish start
seen = set()
out = []
for addr, sz, nm, ops in hits:
    if addr in seen:
        continue
    seen.add(addr)
    out.append((addr, sz, nm, ops))

print('=== writes/reads of 0x400436 ===')
for addr, sz, nm, ops in out:
    # look back up to 3 instructions for an immediate load
    prev = []
    pc = addr - BASE
    # scan back up to 8 bytes
    for back in (2, 4, 6, 8):
        s2, n2, a12, a22, _ = h.decode(pc - back)
        if n2 is not None and s2 == back:
            prev.append('0x%06X %s %s' % (pc - back + BASE, n2, ' '.join(x for x in (a12, a22) if x)))
            break
    print('0x%06X  %-8s %-28s | prev: %s' % (addr, nm, ops, prev[0] if prev else '-'))
