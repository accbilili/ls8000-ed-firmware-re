import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg, sample
import json, sys, re
BASE=0x10000
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
print('image',len(d))

def findall(pat):
    out=[]; i=d.find(pat)
    while i>=0:
        out.append(i); i=d.find(pat,i+1)
    return out

for name,pat in [('4B 00 40 03 FB',bytes.fromhex('004003FB')),
                 ('3B 40 03 FB',bytes.fromhex('4003FB')),
                 ('2B 03 FB',bytes.fromhex('03FB'))]:
    hits=findall(pat)
    print(f'\n== {name} : {len(hits)} hits')
    for h in hits[:400]:
        a=h+BASE
        print(f'  off 0x{h:05X} addr 0x{a:06X} ctx {d[max(0,h-6):h+8].hex(" ")}')

cfg=json.load(open(cfg('cfg_v4.json')))
ins=cfg['insns']
print('\n== cfg operand contains 4003FB')
n=0
for k,v in ins.items():
    ops=' '.join(str(x) for x in v[2:4] if x)
    if re.search(r'4003fb',ops,re.I):
        n+=1; print(f'  {k} {v} owner={cfg["owner"].get(k)}')
print('cfg hits',n)
