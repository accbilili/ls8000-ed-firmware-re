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

def dump(start, stop, label=''):
    print('; ---- %s 0x%06X - 0x%06X' % (label, start, stop))
    pc = start - BASE
    while pc < stop - BASE:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print('0x%06X  .byte 0x%02X' % (pc + BASE, d[pc]))
            pc += 2
            continue
        print('0x%06X  %-9s %s' % (pc + BASE, nm, ', '.join(x for x in (a1, a2) if x)))
        pc = nxt

dump(0x02A2F6, 0x02A3C0, 'axis-A primitive (extended)')
dump(0x029D2A, 0x029D80, '0x029D2A')
dump(0x02BE32, 0x02BF40, 'axis-B primitive (extended)')

print('; ---- table 0x03EE10 words[0..0x20]')
for i in range(0, 0x24, 2):
    off = 0x03EE10 - BASE + i
    print('0x%06X  %04X' % (0x03EE10 + i, (d[off] << 8) | d[off + 1]))

print('; ---- pointer search (32-bit BE) for 0x02740A/0x02753E/0x027DC4')
for target in (0x02740A, 0x02753E, 0x027DC4, 0x027676):
    pat = target.to_bytes(4, 'big')
    hits = []
    i = 0
    while True:
        i = d.find(pat, i)
        if i < 0:
            break
        hits.append(0x10000 + i)
        i += 1
    print('0x%06X -> %s' % (target, [hex(x) for x in hits[:12]]), 'n=', len(hits))
