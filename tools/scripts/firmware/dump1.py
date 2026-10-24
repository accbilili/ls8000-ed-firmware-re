import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import sys
d = open(sample('LS8000_111_ROM.bin'),'rb').read()
BASE = 0x10000
def rd(a,n):
    o=a-BASE
    return d[o:o+n]
def u16(a): 
    b=rd(a,2); return (b[0]<<8)|b[1]
def u32(a):
    b=rd(a,4); return int.from_bytes(b,'big')

out=[]
def P(s=''):
    out.append(s)

# 16-byte rows over full range
P("=== 16B rows, 0x03E2E8..0x03F200 ===")
for a in range(0x03E2E8, 0x03F200, 16):
    b=rd(a,16)
    hx=' '.join(f'{x:02X}' for x in b)
    asc=''.join(chr(x) if 32<=x<127 else '.' for x in b)
    g4=' '.join(f'{u32(a+i):08X}' for i in (0,4,8,12))
    P(f'{a:06X}  {hx}  |{asc}|  {g4}')
open('dump16.txt','w',encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:8]))
print("lines", len(out))
