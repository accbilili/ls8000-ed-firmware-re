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
d = open(sample('LS8000_111_ROM.bin'),'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
a = int(sys.argv[1],16); end = int(sys.argv[2],16); out = sys.argv[3]
pc = a - BASE; end -= BASE
lines=[]
while pc < end:
    sz, nm, a1, a2, nxt = h.decode(pc)
    b = d[pc:pc+(sz if sz else 2)].hex(' ')
    if nm is None:
        lines.append(f'0x{pc+BASE:06X}  {b:<16} .word 0x{d[pc]:02X}{d[pc+1]:02X}')
        pc += 2; continue
    ops = ', '.join(x for x in (a1,a2) if x)
    lines.append(f'0x{pc+BASE:06X}  {b:<16} {nm:<9} {ops}')
    pc = nxt
open(out,'w').write('\n'.join(lines))
print(len(lines),'lines ->',out)
