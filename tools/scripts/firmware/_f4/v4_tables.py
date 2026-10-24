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
    print(f'\n########## {title} 0x{a0:06X}-0x{a1:06X} ##########')
    p = a0 - BASE; end = a1 - BASE
    while p < end:
        sz, nm, op1, op2, nxt = h.decode(p)
        if nm is None:
            print(f'0x{p+BASE:06X}  .byte 0x{d[p]:02X}'); p += 2; continue
        print(f'0x{p+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (op1, op2) if x))
        p = nxt if nxt > p else p + 2


dump(0x0289B4, 0x028A50, 'fn 0x0289B4 (er6=0x4003FB 去向)')

# 表 0x3E86C：0x13 字节/记录
print('\n########## 表 0x3E86C（0x13 B/记录，index=v-0x10） ##########')
base = 0x3E86C - BASE
for i in range(8):
    off = base + i * 0x13
    print(f'  rec[{i:2d}] v=0x{0x10+i:02X} @0x{off+BASE:06X}: ' +
          ' '.join(f'{d[off+j]:02X}' for j in range(0x13)))

# 表 0x3EE10：word 索引
print('\n########## 表 0x3EE10（word，索引 = 0x4003FB 值） ##########')
b2 = 0x3EE10 - BASE
for i in range(0x14):
    print(f'  idx 0x{i:02X} @0x{b2+2*i+BASE:06X}: 0x{(d[b2+2*i]<<8)|d[b2+2*i+1]:04X}')
