# -*- coding: utf-8 -*-
"""扫描：以 0x4003xx 为基址寄存器 + 位移 的间接访问，找出被直接普查漏掉的 0x4003FB 命中。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, io, re
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from h8dis import H8
from h8tab import load_entries

ROM = sample('LS8000_111_ROM.bin')
BASE = 0x10000
d = open(ROM, 'rb').read()
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
TARGET = 0x4003FB

ins = []   # (addr, mn, op1, op2, size)
p = 0
END = len(d) - 8
while p < END:
    sz, nm, o1, o2, nxt = h.decode(p)
    if nm is None:
        ins.append((p + BASE, '.byte', '', '', 2)); p += 2; continue
    ins.append((p + BASE, nm, o1 or '', o2 or '', nxt - p))
    p = nxt if nxt > p else p + 2

pat_imm = re.compile(r'#0x([0-9a-f]{8})')
pat_idx = re.compile(r'@\(0x([0-9a-f]+),er(\d)\)')
pat_ind = re.compile(r'@er(\d)')

hits = []
for k, (a, nm, o1, o2, sz) in enumerate(ins):
    m = pat_imm.match(o1)
    if not m or not nm.startswith('mov.l'):
        continue
    imm = int(m.group(1), 16)
    if not (0x4003D0 <= imm <= 0x400420):
        continue
    rm = re.match(r'er(\d)$', o2.strip())
    if not rm:
        continue
    reg = rm.group(1)
    base = imm
    for j in range(k + 1, min(k + 260, len(ins))):
        a2, nm2, x1, x2, _ = ins[j]
        if nm2 in ('rts', 'jmp') or (nm2 == 'jmp' and '@' in x1):
            break
        if nm2.startswith('jsr') or nm2 == 'bsr':
            # 调子程序后 er 可能被破坏：若寄存器是 er0-er3 则保守中断
            if reg in '0123':
                break
        txt = f'{nm2} {x1}, {x2}'
        tgt = None
        if f'@er{reg}' in txt:
            mi = pat_idx.search(txt)
            if mi:
                tgt = base + int(mi.group(1), 16)
            else:
                tgt = base
        if tgt == TARGET:
            hits.append((a2, txt, base))
        # 该寄存器被重新赋值 → 停止跟踪
        if re.search(rf'(^|,\s*)er{reg}$', x2.strip()) and nm2.startswith(('mov', 'add', 'sub', 'and', 'or', 'xor', 'shl', 'shr', 'extu', 'exts')) and not txt.startswith('mov.b @'):
            if not (nm2.startswith('mov') and f'#0x' in x1):
                break

print('### 基址+位移 命中 0x4003FB 的间接访问：')
seen = set()
for a, t, b in hits:
    if (a, t) in seen:
        continue
    seen.add((a, t))
    print(f'  0x{a:06X}  {t}   (base=0x{b:06X})')
print('count', len(seen))
