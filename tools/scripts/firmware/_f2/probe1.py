import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg
import json
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']; own=c['owner']
for a in ['0x28bb0','0x28b0a','0x28e30','0x28e3e','0x290a0','0x28d44']:
    print(a, ins.get(a), 'owner=',own.get(a))
print('--- ranges ---')
import re
def h(x): return int(x,16)
addrs=sorted(h(k) for k in ins)
lo,hi=0x28900,0x29130
sel=[a for a in addrs if lo<=a<hi]
print('insn count in range',len(sel),'first',hex(sel[0]),'last',hex(sel[-1]))
# find gaps
gaps=[]
for a,b in zip(sel,sel[1:]):
    sz=ins['0x%x'%a][0]
    if a+sz!=b: gaps.append((hex(a),sz,hex(b)))
print('gaps',gaps)
print('--- owners in range ---')
owns=sorted({h(v) for v in own.values() if lo<=h(v)<hi})
print([hex(x) for x in owns])
print('owner values covering 28b00-28e68:')
seen={}
for k,v in own.items():
    if 0x28b00<=h(k)<0x28e68: seen.setdefault(v,0); seen[v]+=1
print(seen)
