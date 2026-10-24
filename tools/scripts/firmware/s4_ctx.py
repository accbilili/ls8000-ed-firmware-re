import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, json
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries
BASE=0x10000
D=open(sample('LS8000_111_ROM.bin'),'rb').read()
H=H8(D, load_entries(sample('h8.lst')), base=BASE)
sites=json.load(open('sites.json'))
def dec(a):
    sz,nm,x,y,nxt=H.decode(a-BASE)
    return (sz,nm,x,y,nxt)
def show(a0,a1):
    pc=a0-BASE; out=[]
    while pc<a1-BASE:
        sz,nm,x,y,nxt=dec(pc+BASE)
        if nm is None:
            out.append(f'0x{pc+BASE:06X}  .byte 0x{D[pc]:02X}'); pc+=2; continue
        out.append(f'0x{pc+BASE:06X}  {nm:<7} '+', '.join(str(t) for t in (x,y) if t)); pc=nxt
    return out
for s in sites:
    print(f'\n##### 0x{s:06X}')
    for L in show(s-14,s+16): print('   '+L)
