# -*- coding: utf-8 -*-
"""Helper: locate function ranges by owner key."""
from dis27dc4 import ADDR, OWN, INS


def rng(owner):
    addrs = [pc for pc in ADDR if OWN.get('%#07x' % pc) == owner]
    if not addrs:
        return None
    return min(addrs), max(addrs), len(addrs)


def funcs_report(addrs):
    for a in addrs:
        k = '0x%05x' % a
        o = OWN.get(k)
        info = rng(o) if o else None
        print('entry 0x%06X  owner=%s  %s' % (a, o, ('%06X-%06X n=%d' % info) if info else 'NOT IN CFG'))


if __name__ == '__main__':
    funcs_report([0x29cd8, 0x2898c, 0x27a54, 0x27f24, 0x2adce, 0x2ace6, 0x2c9e4, 0x2c8e0])
