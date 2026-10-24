# -*- coding: utf-8 -*-
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

def scan(a0, a1, regs, title):
    print(f'\n### {title} 0x{a0:06X}-0x{a1:06X} 关注 {regs}')
    p = a0 - BASE; end = a1 - BASE; prev = []
    while p < end:
        sz, nm, op1, op2, nxt = h.decode(p)
        if nm is None:
            p += 2; continue
        s = f'{nm} {op1 or ""}, {op2 or ""}'
        if any(('@'+r) in s for r in regs):
            for q in prev[-3:]:
                print('    ' + q)
            print(f' >> 0x{p+BASE:06X}  {s}')
            prev = [f'   0x{p+BASE:06X}  {s}']
        else:
            prev.append(f'   0x{p+BASE:06X}  {s}')
            prev = prev[-4:]
        p = nxt

scan(0x023FA4, 0x0241B6, ['er3'], 'fn 0x023FA4 (er3=0x4003FB)')
scan(0x0241BC, 0x024336, ['er5'], 'fn 0x0241BC (er5=0x4003FB)')
scan(0x0289B4, 0x028B00, ['er6'], 'fn 0x0289B4 (er6=0x4003FB)')
scan(0x029C00, 0x029FE0, ['er6'], 'fn 0x029xxx (er6=0x4003FB)')
