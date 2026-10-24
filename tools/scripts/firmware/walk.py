#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 0x0289B4 向上追调用链（jsr 24bit / bsr d:16 / jmp 24bit），用 CFG owner 归并到函数。"""
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

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
B = 0x10000
cfg = json.load(open(cfg('cfg_v4.json')))
own = cfg['owner']


def u16(p):
    return (d[p] << 8) | d[p + 1]


def s16(x):
    return x - 65536 if x >= 32768 else x


calls = {}   # target -> [(site, kind)]


def add(t, site, kind):
    if 0 < t < 0x100000:
        calls.setdefault(t, []).append((site, kind))


for p in range(0, len(d) - 6, 2):
    a = p + B
    if d[p] == 0x5C and d[p + 1] == 0x00:
        add(a + 4 + s16(u16(p + 2)), a, 'bsr')
    elif d[p] == 0x5E:
        add((d[p + 1] << 16) | (d[p + 2] << 8) | d[p + 3], a, 'jsr')
    elif d[p] == 0x5A:
        add((d[p + 1] << 16) | (d[p + 2] << 8) | d[p + 3], a, 'jmp')


def fstart(a):
    return own.get('0x%06x' % a)


def walk(start, depth=6, seen=None):
    seen = seen if seen is not None else set()
    lvl = [start]
    for lv in range(depth):
        nxt = []
        for f in lvl:
            sites = calls.get(f, [])
            outs = []
            for s, k in sites:
                o = fstart(s)
                outs.append(f'0x{s:06X}({k}) in {o}')
                if o and o not in seen:
                    seen.add(o)
                    nxt.append(int(o, 16))
            print(f'  [L{lv}] func 0x{f:06X} <- ' + (', '.join(outs) if outs else '(无直接调用者)'))
        lvl = [x for x in dict.fromkeys(nxt) if x != start]
        if not lvl:
            break


if __name__ == '__main__':
    print('=== 0x0289B4 向上 ===')
    walk(0x289B4, 6)
