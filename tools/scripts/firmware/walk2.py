#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""只在真实指令边界上取调用点：CFG 指令集 ∪ 未覆盖段线性反汇编结果。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import json
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

sys.stdout.reconfigure(encoding='utf-8')
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
B = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=B)
cfg = json.load(open(cfg('cfg_v4.json')))
own = {int(k, 16): int(v, 16) for k, v in cfg['owner'].items()}
known = {int(k, 16): v for k, v in cfg['insns'].items()}


def u16(p):
    return (d[p] << 8) | d[p + 1]


def s16(x):
    return x - 65536 if x >= 32768 else x


def lin(lo, hi):
    """线性反汇编，返回 {addr:(mnem,o1,o2)}"""
    out = {}
    pc = lo - B
    while pc < hi - B:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            pc += 2
            continue
        out[pc + B] = (nm, a1, a2)
        pc = nxt
    return out


extra = {}
extra.update(lin(0x289B4, 0x28E30))
extra.update(lin(0x28E30, 0x290A0))

callsite = {}
for a, v in known.items():
    callsite[a] = (v[1], v[2], v[3])
for a, v in extra.items():
    callsite.setdefault(a, v)

calls = {}
for a, (nm, o1, o2) in callsite.items():
    p = a - B
    if nm == 'bsr':
        t = a + 4 + s16(u16(p + 2))
        calls.setdefault(t, []).append((a, 'bsr'))
    elif nm == 'jsr':
        t = (d[p + 1] << 16) | (d[p + 2] << 8) | d[p + 3]
        calls.setdefault(t, []).append((a, 'jsr'))
    elif nm == 'jmp':
        t = (d[p + 1] << 16) | (d[p + 2] << 8) | d[p + 3]
        calls.setdefault(t, []).append((a, 'jmp'))


def fs(a):
    return own.get(a)


def walk(start, depth=7):
    seen = {start}
    lvl = [start]
    for lv in range(depth):
        nxt = []
        for f in lvl:
            outs = []
            for s, k in calls.get(f, []):
                o = fs(s)
                outs.append(f'0x{s:06X}/{k}@0x{o:06X}' if o else f'0x{s:06X}/{k}@???')
                if o and o not in seen:
                    seen.add(o)
                    nxt.append(o)
            print(f'  L{lv} 0x{f:06X} <- ' + (', '.join(outs) if outs else '(无)'))
        lvl = nxt
        if not lvl:
            break


if __name__ == '__main__':
    for s in (0x289B4, 0x28E30, 0x290A0, 0x2753E, 0x27676, 0x27930):
        print(f'=== 0x{s:06X} 向上 ===')
        walk(s, 6)
