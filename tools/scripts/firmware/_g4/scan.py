import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg
import json, sys, re
sys.path.insert(0, TOOLCHAIN_ROOT)
c=json.load(open(cfg('cfg_v4.json')))
ins=c['insns']; owner=c['owner']
HEX=re.compile(r'0x([0-9a-fA-F]{2,8})')
targets=set(int(t,16) for t in sys.argv[1:])
lo=min(targets); hi=max(targets)
hits=[]
for a,v in ins.items():
    if not isinstance(v,list): continue
    ops=v[2:4]
    vals=set()
    for o in ops:
        if not isinstance(o,str): continue
        for m in HEX.finditer(o):
            vals.add(int(m.group(1),16))
    for t in vals:
        if lo<=t<=hi:
            hits.append((int(a,16), v[1], v[2] if len(v)>2 else '', v[3] if len(v)>3 else '', owner.get(a)))
hits.sort()
for a,nm,o1,o2,ow in hits:
    ops=', '.join(x for x in (o1,o2) if x)
    print(f'0x{a:06X}  [fn 0x{int(ow,16):06X}]  {nm:<8} {ops}')
print(f'-- {len(hits)} hits (range 0x{lo:X}..0x{hi:X})')
