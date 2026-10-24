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
    if v[4] in ('call','jmp'):
        t=v[2]
        if isinstance(t,str) and t.startswith('0x'):
            callers[int(t,16)].add((int(k,16),v[1]))
def o(a): return int(own.get('0x%x'%a,0),16)
front=[0x274BC]; seen={0x274BC}
for lvl in range(5):
    nxt=[]
    for fn in front:
        cs=sorted(callers.get(fn,[]))
        print('  '*lvl+f'0x{fn:06X} <- '+', '.join(f'0x{x:06X}/{m}' for x,m in cs))
        for x,m in cs:
            n=o(x)
            if n not in seen: seen.add(n); nxt.append(n)
    front=nxt
    if not front: break
