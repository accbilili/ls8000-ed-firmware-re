#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证片夹光学识别返回码的落地地址与消费方。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg, sample
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

CFG = cfg('cfg_v4.json')
ROM = sample('LS8000_111_ROM.bin')
B = 0x10000

d = json.load(open(CFG, encoding='utf-8'))
ins = d['insns']
own = d['owner']


def rows_in(lo, hi):
    out = []
    for k, v in own.items():
        a = int(k, 16)
        if lo <= a <= hi:
            out.append((a, v))
    out.sort()
    return out


def show(lo, hi, title):
    print(f'\n===== {title}  0x{lo:06X}-0x{hi:06X} =====')
    for a, fn in rows_in(lo, hi):
        rec = ins.get(f'0x{a:x}') or ins.get(hex(a))
        if not rec:
            continue
        sz, mn, o1, o2, kind, _ = rec
        ops = ' '.join(x for x in (o1, o2) if x)
        print(f'  0x{a:06X}  [f 0x{int(fn,16):06X}]  {mn:<10} {ops}')


if __name__ == '__main__':
    # 识别函数
    show(0x28E30, 0x28E60, 'identify 入口')
    show(0x28F80, 0x290A0, '位映射 + 解码器 + Unknown 出口')
    # 调用者：GR 两阶段
    show(0x28B90, 0x28C20, 'identify 调用者（GR 两阶段）')

    # 全镜像搜索 0x028E30 的调用点
    rom = open(ROM, 'rb').read()
    print('\n===== 0x028E30 的 bsr/jsr 调用点 =====')
    tgt = (0x028E30).to_bytes(4, 'big')
    i = 0
    hits = []
    while True:
        i = rom.find(tgt, i)
        if i < 0:
            break
        hits.append(B + i - 1)
        i += 1
    for h in hits:
        op = rom[h - B]
        print(f'  0x{h - 1:06X}  opcode=0x{op:02X}  -> 目标 0x028E30')
    if not hits:
        print('  无直接 32 位地址引用')
