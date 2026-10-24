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
BASE=0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
print('len',len(d))
# dump table 0x03EBC0 26*16
for i in range(26):
    a=0x3EBC0+i*16
    b=d[a-BASE:a-BASE+16]
    op=int.from_bytes(b[0:2],'big'); ln=int.from_bytes(b[2:4],'big')
    hd=int.from_bytes(b[4:8],'big'); lo=int.from_bytes(b[8:12],'big'); hi=int.from_bytes(b[12:16],'big')
    print(i,hex(op),ln,hex(hd),lo,hi)
