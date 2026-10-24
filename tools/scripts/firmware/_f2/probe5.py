import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg
import json,collections
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']; own=c['owner']
callers=collections.defaultdict(set)
for k,v in ins.items():
    if v[4]=='call':
        t=v[2]
        if isinstance(t,str) and t.startswith('0x'):
            callers[int(t,16)].add(int(k,16))
def owner_of(a):
    return int(own.get('0x%x'%a,0),16)
start=0x289B4
print('owner of 0x2799c =',hex(owner_of(0x2799c)))
# walk up BFS
front=[(start,0)]
seen={start}
for lvl in range(6):
    nxt=[]
    for fn,d in front:
        cs=sorted(callers.get(fn,[]))
        print('  '*lvl+f'fn 0x{fn:06X} called from: '+', '.join(f'0x{x:06X}' for x in cs[:12]))
        for x in cs:
            f2=owner_of(x)
            if f2 not in seen:
                seen.add(f2); nxt.append((f2,lvl+1))
    front=nxt
