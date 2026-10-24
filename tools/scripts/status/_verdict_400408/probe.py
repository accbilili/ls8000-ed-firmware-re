import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, os, json
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries
BASE=0x10000
D=open(sample('LS8000_111_ROM.bin'),'rb').read()
H=H8(D, load_entries(sample('h8.lst')), base=BASE)

def dump(a0,a1):
    print('--- raw bytes 0x%06X-0x%06X ---'%(a0,a1))
    for a in range(a0,a1,8):
        off=a-BASE
        b=D[off:off+8]
        print('0x%06X: %s'%(a,' '.join('%02X'%x for x in b)))
    print('--- decode ---')
    pc=a0-BASE; end=a1-BASE
    while pc<end:
        sz,nm,a,b,nxt=H.decode(pc)
        if nm is None:
            print('0x%06X  .byte 0x%02X 0x%02X'%(pc+BASE,D[pc],D[pc+1])); pc+=2; continue
        print('0x%06X  %-8s %s'%(pc+BASE,nm,', '.join(x for x in (a,b) if x)))
        pc=nxt

def search32(val, name):
    pat=bytes([(val>>24)&255,(val>>16)&255,(val>>8)&255,val&255])
    hits=[]; i=0
    while True:
        i=D.find(pat,i)
        if i<0: break
        hits.append(i+BASE); i+=1
    print('search %s=0x%08X -> %d hits: %s'%(name,val,len(hits),' '.join('0x%06X'%h for h in hits)))
    return hits

if __name__=='__main__':
    a0=int(sys.argv[1],16); a1=int(sys.argv[2],16)
    dump(a0,a1)
