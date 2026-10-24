#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确的 H8 反汇编辅助（修正 decode() 取**文件偏移**而非绝对地址的约定）。
供 verify_r22_conflict.py 与人工核对使用。只读 D:。
"""
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
sys.path.insert(0, '<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed

BASE = 0x10000
D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
H = H8(D, load_entries_fixed(sample('h8.lst')), base=BASE)


def raw(a, n):
    o = a - BASE
    return ' '.join('%02X' % b for b in D[o:o + n])


def dis(a, n, tag=''):
    """a = 绝对地址；输出 n 条指令"""
    if tag:
        print('  --- %s' % tag)
    pc = a - BASE
    for _ in range(n):
        sz, nm, x, y, nxt = H.decode(pc)
        if nm is None:
            print('   0x%06X  .byte 0x%02X' % (pc + BASE, D[pc]))
            pc += 2
            continue
        print('   0x%06X  %-9s %s' % (pc + BASE, nm, ', '.join(z for z in (x, y) if z)))
        pc = nxt


if __name__ == '__main__':
    import re
    a = int(sys.argv[1], 16)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    dis(a, n)
