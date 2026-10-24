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
mn=collections.Counter(v[1] for v in ins.values())
print(mn.most_common(12))
# sample of call-ish
for k,v in ins.items():
    if v[1] in ('bsr','jsr','jmp','bra','bcc','bne'):
        print(k,v); break
for k,v in ins.items():
    if v[1]=='bsr':
        print('bsr ex',k,v); break
