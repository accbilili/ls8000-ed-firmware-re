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
d = json.load(open(cfg('cfg_v4.json')))
ins = d['insns']; owner = d['owner']
T = {0x02740A:'A0', 0x02753E:'B0', 0x027676:'C0', 0x0277CE:'D0', 0x027930:'E0',
     0x027A54:'WD', 0x027AFA:'E1b', 0x027B1E:'E2', 0x027DC4:'F0',
     0x027F24:'F1', 0x027F44:'F2', 0x02898C:'V2989C', 0x0288F6:'V288F6',
     0x0283DC:'V283DC', 0x03C31E:'T03C31E', 0x02896C:'V2896C'}
hits = {v: [] for v in T.values()}
for k, v in ins.items():
    pc = int(k, 16); kind = v[4]; tgt = v[5]
    if tgt is None: continue
    if tgt in T and pc != tgt and kind in ('call', 'jump', 'cond'):
        hits[T[tgt]].append((pc, kind, v[1], owner.get(hex(pc), '?')))
for name in T.values():
    lst = sorted(hits[name])
    print(f'== {name}: {len(lst)} edges')
    for pc, kind, mn, own in lst[:14]:
        print(f'   0x{pc:06X} [{kind:4}] {mn:6} in {own}')
