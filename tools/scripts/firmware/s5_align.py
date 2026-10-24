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
cfg=json.load(open(cfg('cfg_v4.json'))); INS=cfg['insns']; OWN=cfg['owner']
sites=json.load(open('sites.json'))
def walk(a0,limit=40):
    pc=a0-BASE; n=0
    while n<limit:
        sz,nm,x,y,nxt=H.decode(pc)
        if nm is None: return None
        if pc+BASE==a0+ (0): pass
        pc=nxt; n+=1
        yield pc+BASE
print('site      inCFG  prevCFG  resync(from)  reachSite')
for s in sites:
    incfg = hex(s) in INS
    # find nearest cfg instruction before s within 64 bytes
    cand=None
    for d in range(2,64,2):
        if hex(s-d) in INS: cand=s-d; break
    ok='-'
    if cand:
        seen=set(); 
        for a in walk(cand):
            if a==s: ok='YES'; break
            if a in seen: break
            seen.add(a)
            if a>s+8: ok='NO'; break
    print(f'0x{s:06X}  {str(incfg):5}  0x{(cand or 0):06X}  {ok}')
