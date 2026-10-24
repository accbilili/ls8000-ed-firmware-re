import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import sys, json
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries
BASE=0x10000
D=open(sample('LS8000_111_ROM.bin'),'rb').read()
H=H8(D, load_entries(sample('h8.lst')), base=BASE)
CFG=json.load(open(cfg('cfg_v4.json')))
INS=CFG['insns']; OWN=CFG['owner']

def dec(a):
    sz,nm,x,y,nxt=H.decode(a-BASE)
    return sz,nm,x,y,nxt
def txt(sz,nm,x,y):
    if nm is None: return '.byte'
    return nm+' '+', '.join(str(t) for t in (x,y) if t)

hits=[]
i=D.find(bytes.fromhex('004003FB'))
while i>=0:
    hits.append(i+BASE); i=D.find(bytes.fromhex('004003FB'),i+1)
print(f'32bit pattern hits: {len(hits)}')
sites=[]
for h in hits:
    a=h-2
    sz,nm,x,y,nxt=dec(a)
    ok = (sz==6 and nm and x=='@0x4003fb')
    incfg = hex(a) in INS
    sites.append((a,nm,x,y,ok,incfg))
    print(f'0x{a:06X} dec={txt(sz,nm,x,y):<34} ok={ok} cfg={incfg} owner={OWN.get(hex(a))}')
json.dump([s[0] for s in sites],open('sites.json','w'))
