#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""用 Harness 自带的 h8dis 反汇编片夹识别调用区，验证返回码落地。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys

sys.path.insert(0, TOOLCHAIN_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

import importlib

h8dis = importlib.import_module('h8dis')
h8tab = importlib.import_module('h8tab')

ROM = sample('LS8000_111_ROM.bin')
BASE = 0x10000
data = open(ROM, 'rb').read()

# entries 可能叫别的名字
ENTRIES = None
for cand in ('ENTRIES', 'TAB', 'TABLE', 'OPS', 'ENC'):
    if hasattr(h8tab, cand):
        ENTRIES = getattr(h8tab, cand)
        print(f'h8tab.{cand}: {len(ENTRIES)} entries')
        break
if ENTRIES is None:
    print('h8tab 属性:', [x for x in dir(h8tab) if not x.startswith('_')])
    sys.exit(1)

h = h8dis.H8(data, ENTRIES, base=BASE)


def dis(lo, hi, title):
    print(f'\n===== {title} 0x{lo:06X} - 0x{hi:06X} =====')
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print(f'  0x{pc + BASE:06X}  .byte 0x{data[pc]:02X}   <-- 无法解码')
            pc += 2
            continue
        ops = ', '.join(x for x in (a1, a2) if x)
        print(f'  0x{pc + BASE:06X}  {nm:<9} {ops}')
        pc = nxt


if __name__ == '__main__':
    dis(0x28BA0, 0x28C40, 'identify 调用与 GR 两阶段')
    dis(0x28C80, 0x28CB0, '下排返回码消费')
