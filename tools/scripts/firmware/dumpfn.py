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
CFG=json.load(open(cfg('cfg_v4.json')))
INS=CFG['insns']; OWN=CFG['owner']
own=sys.argv[1].lower()
rows=[(int(k,16),v) for k,v in INS.items() if OWN.get(k)==own or k==own]
rows.sort()
print(f'# function {own}: {len(rows)} insns')
for a,v in rows:
    print(f'0x{a:06X}  {v[1]:<8} '+', '.join(str(x) for x in v[2:4] if x and str(x)!='None')+f'   [{v[4]}]')
