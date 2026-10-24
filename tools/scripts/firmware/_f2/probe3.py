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
ins=c['insns']
tgt={0x28E30:'ident',0x289B4:'entry28BB0chain',0x28BB0:'28BB0',0x290A0:'typecode_consume',
     0x2D700:'capture',0x27DC4:'insert_sm',0x2753E:'holder_read'}
calls=collections.defaultdict(list)
for k,v in ins.items():
    if v[4] in ('call',) or v[1] in ('jsr','bsr','jmp'):
        t=v[2]
        if isinstance(t,str) and t.startswith('0x'):
            calls[int(t,16)].append((int(k,16),v[1]))
for a,name in tgt.items():
    print(f'== {name} 0x{a:06X} callers:')
    for site,mn in sorted(calls.get(a,[])):
        print('   ',hex(site),mn)
print()
print('all jmp targets:',[(hex(k),v[2]) for k,v in ins.items() if v[1]=='jmp'][:10])
print('n calls',len(calls))
