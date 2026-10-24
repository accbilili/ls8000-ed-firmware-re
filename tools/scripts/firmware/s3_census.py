import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import sys, json, re
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries
BASE=0x10000
D=open(sample('LS8000_111_ROM.bin'),'rb').read()
H=H8(D, load_entries(sample('h8.lst')), base=BASE)
CFG=json.load(open(cfg('cfg_v4.json')))
INS=CFG['insns']; OWN=CFG['owner']
LO,HI=0x4003EC,0x40043F

def dec(a):
    return H.decode(a-BASE)

rows=[]
rej=[]
# 1) abs24 direct: pattern 00 40 03 xx / 00 40 04 0x
for hi in (0x4003,0x4004):
    for lo in range(0x00,0x100):
        tgt=(hi<<8)|lo
        if not (LO<=tgt<=HI): continue
        pat=tgt.to_bytes(4,'big')
        i=D.find(pat)
        while i>=0:
            a=i+BASE
            sz,nm,x,y,nxt=dec(a-2)
            txt='' if not nm else ', '.join(str(t) for t in (x,y) if t)
            if sz==6 and nm in ('mov.b','mov.w','mov.l') and (x==f'@0x{tgt:06x}' or y==f'@0x{tgt:06x}' or f'0x{tgt:06x}' in txt):
                rows.append((tgt,a-2,nm,x,y))
            else:
                rej.append((tgt,a,sz,nm,x,y))
            i=D.find(pat,i+1)

rows.sort()
print('=== 直接 abs24 访问点 ===')
cur=None
for tgt,a,nm,x,y in rows:
    if tgt!=cur: print(f'\n[0x{tgt:06X}]'); cur=tgt
    rw='W' if (y and str(y).startswith('@0x')) else ('R' if (x and str(x).startswith('@0x')) else ('PTR' if nm=='mov.l' else '?'))
    print(f'  0x{a:06X} {nm:<6} {str(x):<18} {str(y):<14} {rw}  owner={OWN.get(hex(a))}')
print('\n=== 未对齐/非操作数命中（离群） ===')
for t in rej: print('  tgt=0x%06X at 0x%06X sz=%s %s %s %s'%(t[0],t[1],t[2],t[3],t[4],t[5]))

# 2) 立即数装载指针 mov.l #0x00400xxx, erN
print('\n=== mov.l #0x00400xxx → erN（指针基址） ===')
for k,v in INS.items():
    if v[1]=='mov.l' and isinstance(v[2],str) and v[2].startswith('#0x00400'):
        val=int(v[2][1:],16)
        if LO-0x40<=val<=HI+0x80:
            print(f'  {k} {v[2]} -> {v[3]}  owner={OWN.get(k)}')
