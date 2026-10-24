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


def dec(off):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        return None
    return sz, nm, ' '.join(x for x in (a1, a2) if x), nxt


print('=== 0x400436 access points (linear sweep, 2-byte aligned) ===')
n = 0
for off in range(0, len(d) - 8, 2):
    r = dec(off)
    if r is None:
        continue
    sz, nm, ops, nxt = r
    if '400436' not in ops.lower():
        continue
    n += 1
    ctx = []
    pc = off
    for _ in range(4):
        # walk back one instruction guess: try back 2,4,6
        got = None
        for back in (2, 4, 6):
            if off - back < 0:
                continue
            r2 = dec(off - back)
            if r2 and r2[0] == back:
                got = r2
                break
        if got:
            ctx.append('0x%06X %s %s' % (off - back + BASE, got[1], got[2]))
            off2 = off - back
            # go one more back
            got2 = None
            for back2 in (2, 4, 6):
                if off2 - back2 < 0:
                    continue
                r3 = dec(off2 - back2)
                if r3 and r3[0] == back2:
                    got2 = r3
                    break
            if got2:
                ctx.append('0x%06X %s %s' % (off2 - back2 + BASE, got2[1], got2[2]))
            break
        break
    print('0x%06X  %-8s %-26s || %s' % (off + BASE, nm, ops, ' ; '.join(reversed(ctx))))
print('total', n)
