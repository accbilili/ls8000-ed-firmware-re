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
pcs = sorted(int(k, 16) for k in ins)

def const(s):
    if not s or not s.startswith('#'): return None
    try: return int(s[1:], 16)
    except Exception: return None

regs = {}
out = []
for p in pcs:
    v = ins[hex(p)]
    sz, mn, o1, o2 = v[0], v[1], (v[2] or ''), (v[3] or '')
    fn = owner.get(hex(p))
    # kill / set tracking
    if mn == 'mov.l' and o1.startswith('#') and o2.startswith('er'):
        regs[o2] = const(o1)
    elif mn == 'mov.w' and o1.startswith('#') and o2 in ('r0','e0','r1','r2','r3','r4','r5','r6'):
        regs[o2] = const(o1)
    if mn.startswith('mov') and o2.startswith('@'):
        dst = o2
        if dst in ('@er5','@er6','@er4','@er3','@er0','@er1','@er2'):
            addr = regs.get(dst[1:], None)
            if addr in (0x400404, 0x400402):
                val = regs.get(o1, None)
                out.append((p, fn, addr, val, o1))
        elif dst in ('@0x400404', '@0x400402'):
            out.append((p, fn, int(dst[1:], 16), regs.get(o1), o1))
    # invalidate dest regs on generic writes
    for r in ('r0','r0l','r0h','r1','r2','r3','r4','r5','r6','er0','er1','er2','er3','er4','er5','er6'):
        if o2 == r and not (mn == 'mov.l' and o1.startswith('#')):
            regs.pop(r, None)

print(f'{"insn":10} {"in fn":10} {"target":8} {"value":8} src')
for p, fn, addr, val, o1 in out:
    vs = f'0x{val:04X}' if val is not None else '---'
    print(f'0x{p:06X}  {fn:10} 0x{addr:06X} {vs:8} {o1}')
print('total', len(out))
