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
CFG=json.load(open(cfg('cfg_v4.json')))['insns']

def dis(a0,a1,label=''):
    print(f'\n===== {label} 0x{a0:06X}-0x{a1:06X} =====')
    pc=a0-BASE
    end=a1-BASE
    while pc<end:
        cached=CFG.get(hex(pc+BASE))
        sz,nm,a,b,nxt=H.decode(pc)
        mark=''
        if cached and cached[1]=='mov.l' and isinstance(cached[3],str) and cached[3].startswith('er'):
            mark=f'   ; #{cached[2]}'
        if nm is None:
            print(f'0x{pc+BASE:06X}  .byte 0x{D[pc]:02X}')
            pc+=2
            continue
        print(f'0x{pc+BASE:06X}  {nm:<8} ' + ', '.join(x for x in (a,b) if x) + mark)
        pc=nxt
if __name__=='__main__':
    a0=int(sys.argv[1],16); a1=int(sys.argv[2],16)
    dis(a0,a1,sys.argv[3] if len(sys.argv)>3 else '')
