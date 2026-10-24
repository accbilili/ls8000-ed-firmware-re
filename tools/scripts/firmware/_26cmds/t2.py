import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys,re
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries
d = open(sample('LS8000_111_ROM.bin'),'rb').read()
BASE=0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
targets=[0x3EBC0,0x3E390]
for t in targets:
    pat=t.to_bytes(4,'big')
    print('== refs to',hex(t))
    i=0
    while True:
        i=d.find(pat,i)
        if i<0: break
        print('  fileoff',hex(i),'addr',hex(i+BASE))
        i+=1
