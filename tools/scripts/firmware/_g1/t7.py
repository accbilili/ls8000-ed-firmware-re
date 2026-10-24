"""线性全镜像扫一遍，跟踪寄存器常量，找所有对 0x400436 的写入值。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, re, collections
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

regs = {}          # name -> int or None
TARGET = 0x400436
const_hits = collections.defaultdict(list)
dyn_hits = []
lookup_hits = []

pc = 0
count = 0
while pc < len(d) - 1:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        regs.clear()
        pc += 2
        continue
    ops = [x for x in (a1, a2) if x]
    o = ' '.join(ops)
    addr = pc + BASE

    def inv(name):
        regs.pop(name, None)

    # --- detect stores to TARGET ---
    if nm == 'mov.w' and len(ops) == 2:
        src, dst = ops
        tgt = None
        if dst.strip().lower() == '@0x00400436' or dst.strip().lower() == '@0x400436':
            tgt = True
        else:
            m = re.match(r'@er(\d)$', dst.strip())
            if m and regs.get('er' + m.group(1)) == TARGET:
                tgt = True
        if tgt:
            s = src.strip()
            m = re.match(r'r(\d)$', s)
            if m and regs.get('r' + m.group(1)) is not None:
                const_hits[regs['r' + m.group(1)]].append(addr)
            elif s == 'r0' and regs.get('__jsr211b6'):
                lookup_hits.append(addr)
            else:
                dyn_hits.append((addr, o))

    # --- track register values ---
    if nm == 'mov.l' and len(ops) == 2 and ops[0].startswith('#'):
        m = re.match(r'er(\d)$', ops[1].strip())
        if m:
            v = int(ops[0][1:], 16)
            regs['er' + m.group(1)] = v
            inv('r' + m.group(1)); inv('e' + m.group(1))
    elif nm == 'mov.w' and len(ops) == 2 and ops[0].startswith('#'):
        m = re.match(r'r(\d)$', ops[1].strip())
        if m:
            regs['r' + m.group(1)] = int(ops[0][1:], 16)
            inv('er' + m.group(1))
        else:
            m = re.match(r'e(\d)$', ops[1].strip())
            if m:
                inv('er' + m.group(1))
    elif nm == 'mov.w' and len(ops) == 2:
        m = re.match(r'(r\d|e\d|er\d)$', ops[1].strip())
        if m:
            inv(m.group(1))
            if m.group(1).startswith('r'):
                inv('er' + m.group(1)[1:])
    elif nm == 'jsr' and '211b6' in o.lower():
        regs['__jsr211b6'] = True
    elif nm in ('rts', 'rte', 'jmp', 'bra', 'bt'):
        pass
    else:
        # any other mnemonic writing r0..r7/e0..e7 -> conservative invalidate of dest
        if len(ops) == 2:
            m = re.match(r'(r\d|e\d|er\d)$', ops[1].strip())
            if m:
                inv(m.group(1))
                if m.group(1).startswith('r'):
                    inv('er' + m.group(1)[1:])
    pc = nxt
    count += 1

print('=== constant values stored into 0x400436 ===')
for k in sorted(const_hits):
    print('0x%02X (%3d) : %2d' % (k, k, len(const_hits[k])))
print('distinct const:', sorted('%02X' % k for k in const_hits))
print()
print('=== via 0x0211B6 lookup (value = field2 of 0x03E390) ===', len(lookup_hits))
print(', '.join('0x%06X' % a for a in lookup_hits))
print()
print('=== dynamic/unresolved stores ===', len(dyn_hits))
seen = set()
for a, o in dyn_hits:
    if o in seen:
        continue
    seen.add(o)
    print('  %-24s e.g. 0x%06X' % (o, a))
