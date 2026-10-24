#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""片夹识别链路：0x028B00-0x028E68 反汇编（修正 0x0100 前缀长指令）
h8dis 会把 `01 00 78 nd <d32> 6B20/6BA0`（MOV.L d:32 间接）误判成 2 字节，
这里先做显式匹配，再退回标准解码。
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
sys.stdout.reconfigure(encoding='utf-8')
from h8dis import H8
from h8tab import load_entries

ROM = sample('LS8000_111_ROM.bin')
BASE = 0x10000
d = open(ROM, 'rb').read()
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

R32 = ["er0", "er1", "er2", "er3", "er4", "er5", "er6", "sp"]


def dec(pc):
    """返回 (size, mnem, op1, op2)，pc 为文件偏移"""
    w0 = (d[pc] << 8) | d[pc + 1]
    if w0 == 0x0100:
        w1 = (d[pc + 2] << 8) | d[pc + 3]
        if (w1 & 0xFF00) == 0x7800:
            w2 = (d[pc + 4] << 8) | d[pc + 5]
            if (w2 & 0xFFF8) == 0x6B20:          # MOV.L @(d:32,ERn),ERd
                base = (w1 >> 4) & 7
                dst = (w1) & 7 if (w1 & 0x80) == 0 else (w1 & 7)
                disp = (d[pc + 6] << 24) | (d[pc + 7] << 16) | (d[pc + 8] << 8) | d[pc + 9]
                return 10, 'mov.l', f'@(0x{disp:08X},{R32[base]})', R32[w2 & 7]
            if (w2 & 0xFFF8) == 0x6BA0:          # MOV.L ERs,@(d:32,ERn)
                base = (w1 >> 4) & 7
                disp = (d[pc + 6] << 24) | (d[pc + 7] << 16) | (d[pc + 8] << 8) | d[pc + 9]
                return 10, 'mov.l', R32[w2 & 7], f'@(0x{disp:08X},{R32[base]})'
        if (w1 & 0xFF0F) == 0x6B00:              # MOV.L @(d:16,ERn),ERd
            base = (w1 >> 4) & 7
            disp = (d[pc + 4] << 8) | d[pc + 5]
            return 6, 'mov.l', f'@(0x{disp:04X},{R32[base]})', R32[w1 & 7]
        if (w1 & 0xFF0F) == 0x6B80:              # MOV.L ERs,@(d:16,ERn)
            base = (w1 >> 4) & 7
            disp = (d[pc + 4] << 8) | d[pc + 5]
            return 6, 'mov.l', R32[w1 & 7], f'@(0x{disp:04X},{R32[base]})'
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        return 2, None, None, None
    return sz, nm, a1, a2


def dis(lo, hi, out=None, tag=''):
    lines = [f'===== {tag} 0x{lo:06X} - 0x{hi:06X} =====']
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2 = dec(pc)
        if nm is None:
            lines.append(f'{pc + BASE:06X}  .byte   0x{d[pc]:02X}{d[pc + 1]:02X}')
            pc += 2
            continue
        ops = ', '.join(x for x in (a1, a2) if x)
        lines.append(f'{pc + BASE:06X}  {nm:<9}{ops}')
        pc += sz
    txt = '\n'.join(lines)
    if out:
        out.append(txt)
    else:
        print(txt)
    return txt


if __name__ == '__main__':
    import io
    buf = []
    dis(0x28800, 0x28C80, buf, 'A 识别前置 + 两阶段')
    dis(0x28E20, 0x28EA0, buf, 'B 0x028E30 序言与采集')
    open('_tmp_a.asm.txt', 'w', encoding='utf-8').write('\n'.join(buf))
    print('\n'.join(buf))
