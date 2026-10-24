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
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
B=0x10000
h=H8(d, load_entries(sample('h8.lst')), base=B)
pc=0x289B4; end=0x28E30
while pc<end:
    sz,nm,a1,a2,nxt=h.decode(pc-B); nxt+=B
    if nm is None or nxt<=pc or sz>8:
        pc+=2; continue
    ops=(a1 or '')+','+(a2 or '')
    if 'er6' in ops or '400d79' in ops.lower() or '4003fb' in ops.lower():
        print('%06X  %-9s %s'%(pc,nm,', '.join(x for x in (a1,a2) if x)))
    pc=nxt
