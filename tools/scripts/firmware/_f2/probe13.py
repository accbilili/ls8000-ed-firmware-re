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
def refs(pat):
    print('--- refs to',pat,'---')
    for k,v in sorted(ins.items(), key=lambda t:int(t[0],16)):
        if pat in ' '.join(str(x) for x in v[2:4]).lower():
            print(' ',k,v,'owner',own.get(k))
refs('4207f8'); refs('470000')
print('owner of 0x10af0:',own.get('0x10af0'))
import collections
callers=collections.defaultdict(set)
for k,v in ins.items():
    if v[4]=='call' and isinstance(v[2],str) and v[2].startswith('0x'):
        callers[int(v[2],16)].add(int(k,16))
print('callers of 0x10a90..:',[(hex(k),hex(x)) for k,v in list(callers.items()) if 0x10a00<k<0x10b20 for x in v][:10])
# find function start containing 0x10af0
o=own.get('0x10af0'); print('containing fn',o)
print('its callers',[hex(x) for x in callers.get(int(o,16),[])])
