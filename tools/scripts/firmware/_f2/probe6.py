import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg, sample
import json,collections,struct
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
B=0x10000
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']
# 1) all control transfers (any tag) whose target in our chain
tg={0x2753E,0x27676,0x2774A,0x27930,0x2799C,0x289B4,0x28E30,0x290A0,0x28BB0}
for k,v in ins.items():
    if v[4] in ('call','jump','cond'):
        t=v[2]
        if isinstance(t,str) and t.startswith('0x') and int(t,16) in tg:
            print(f'{k} {v[1]} -> {t}  tag={v[4]}')
print('--- static table hits for 0x2753E (32-bit BE, data area >=0x3E000) ---')
pat=struct.pack('>I',0x2753E)
start=0x3E000-B
i=d.find(pat,start)
while i!=-1 and i< len(d):
    print(hex(i+B))
    i=d.find(pat,i+1)
print('--- 16-bit 0x0275 pattern not searched ---')
