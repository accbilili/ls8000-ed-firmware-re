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
ins=c['insns']; own=c['owner']
def show(a):
    for k in sorted((int(x,16) for x in ins)):
        if a<=k<a+0x18:
            v=ins['0x%x'%k]
            print(f'  0x{k:06X} {v[1]:<8}{str(v[2]):<14}{str(v[3]):<10}tag={v[4]}')
print('--- 0x2740A ---'); show(0x2740A)
print('--- 0x274B0 ---'); show(0x274B0)
print('--- 0x27930 head ---'); show(0x27930)
print('--- 0x27990 (jsr site) ---'); show(0x27990)
# who targets 0x2740A
for k,v in ins.items():
    if v[4] in ('call','jmp','cond') and isinstance(v[2],str) and v[2].startswith('0x'):
        if int(v[2],16) in (0x2740A,0x274BC): print('ref',k,v)
# 24-bit refs
p=bytes([0x02,0x74,0x0a]); i=d.find(p)
print('24bit 02740a hits:',[hex(i+B) for i in range(0)])
out=[]
j=d.find(p)
while j!=-1: out.append(j+B); j=d.find(p,j+1)
print('24bit hits',[hex(x) for x in out])
