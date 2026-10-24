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

targets = {0x0174BC, 0x011708, 0x0116A0, 0x011882, 0x016AB0, 0x016F46, 0x0211B6, 0x022AD6, 0x022BF2}
found = {t: [] for t in targets}
pc = 0
while pc < len(d) - 1:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        pc += 2
        continue
    ops = [x for x in (a1, a2) if x]
    o = ' '.join(ops)
    addr = pc + BASE
    if nm in ('jsr', 'jmp') and ops and ops[0].startswith('0x'):
        try:
            t = int(ops[0], 16)
        except ValueError:
            t = None
        if t in targets:
            found[t].append((addr, nm))
    elif nm == 'bsr' and ops:
        m = re.match(r'0x([0-9a-f]+)$', ops[0])
        if m:
            t = int(m.group(1), 16)
            if t in targets:
                found[t].append((addr, nm))
    pc = nxt

for t in sorted(targets):
    print('0x%06X <- %d : %s' % (t, len(found[t]), ', '.join('0x%06X(%s)' % a for a in found[t])))
