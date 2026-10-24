# -*- coding: utf-8 -*-
"""Dump listings for LS-8000 ED firmware functions using cfg_v4 instruction map."""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import sys, json
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

ROM = sample('LS8000_111_ROM.bin')
BASE = 0x10000
d = open(ROM, 'rb').read()
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
CFG = json.load(open(cfg('cfg_v4.json')))
INS = CFG['insns']
OWN = CFG['owner']
ADDR = sorted(int(a, 16) for a in INS)


def ins_at(pc):
    return INS.get('0x%05x' % pc)


def listing(lo, hi, title=None, labels=None, indent=''):
    """Linear listing of known instructions in [lo,hi)."""
    lines = []
    if title:
        lines.append('')
        lines.append('; ' + '=' * 70)
        lines.append('; %s' % title)
        lines.append('; range 0x%06X - 0x%06X' % (lo, hi))
        lines.append('; ' + '=' * 70)
    for pc in ADDR:
        if pc < lo or pc >= hi:
            continue
        v = INS['0x%05x' % pc]
        sz, nm, a1, a2 = v[0], v[1], v[2], v[3]
        if labels and pc in labels:
            lines.append('%s%s:' % (indent, labels[pc]))
        ops = ', '.join(x for x in (a1, a2) if x)
        raw = ' '.join('%02X' % b for b in d[pc - BASE:pc - BASE + sz])
        lines.append('%s%06X  %-14s %-8s %s' % (indent, pc, raw, nm, ops))
    return lines


def summary(lo, hi):
    n = sum(1 for pc in ADDR if lo <= pc < hi)
    return n
