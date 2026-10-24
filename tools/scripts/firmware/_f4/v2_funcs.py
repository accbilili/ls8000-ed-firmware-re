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

def dump(a0, a1, title):
    print(f'\n########## {title}  0x{a0:06X}-0x{a1:06X} ##########')
    p = a0 - BASE
    end = a1 - BASE
    while p < end:
        sz, nm, op1, op2, nxt = h.decode(p)
        if nm is None:
            print(f'0x{p+BASE:06X}  .byte 0x{d[p]:02X}')
            p += 2
            continue
        print(f'0x{p+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (op1, op2) if x))
        if nxt <= p:
            p += 2
        else:
            p = nxt

dump(0x027520, 0x0275C0, 'fn 0x02753E 调用方/判据')
dump(0x027900, 0x027B70, 'fn 0x027930 写点 0x027B50 上下文')
dump(0x027DC4, 0x027ED0, 'fn 0x027DC4 写点 0x027E20/EA0/EB4')
dump(0x02842C, 0x0285C0, 'fn 0x02842C 写点 0x02859E')
dump(0x023FA0, 0x023FD0, 'ptr 0x023FB2 (er3=0x4003FB)')
dump(0x0241B0, 0x0241E0, 'ptr 0x0241C2 (er5=0x4003FB)')
dump(0x0289B0, 0x0289F0, 'ptr 0x0289C6 (er6=0x4003FB)')
dump(0x029DF0, 0x029E40, 'ptr 0x029E0E (er6=0x4003FB)')
