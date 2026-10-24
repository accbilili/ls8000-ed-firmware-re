# -*- coding: utf-8 -*-
"""F4 复核：从原镜像逐点反汇编 0x4003FB 的访问点。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, io
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from h8dis import H8
from h8tab import load_entries

ROM = sample('LS8000_111_ROM.bin')
BASE = 0x10000
d = open(ROM, 'rb').read()
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def dec(off):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        return ('.byte', '0x%02X' % d[off], '', off + 2)
    return (nm, a1 or '', a2 or '', nxt)

def show(addr, after=6):
    off = addr - BASE
    p = off
    for k in range(after):
        nm, a1, a2, nxt = dec(p)
        tag = '>>' if k == 0 else '  '
        print(f'{tag}0x{p+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        p = nxt
        if p <= off: break
    print('-' * 72)

DIRECT = [0x016C16,0x016C20,0x016C2A,0x02236E,0x02322E,0x023D22,0x024256,0x024332,
          0x02474E,0x02491A,0x0249AE,0x0249EC,0x024A2A,0x025F32,0x02759E,0x027B50,
          0x027E20,0x027EA0,0x027EB4,0x028590,0x02859E,0x028D6E,0x0290E0,0x029D06,
          0x029D98,0x03719E,0x03A50C]

print('########## A. 逐点反汇编（主指令 + 后续） ##########')
for a in DIRECT:
    print(f'### 0x{a:06X}')
    show(a, after=6)
