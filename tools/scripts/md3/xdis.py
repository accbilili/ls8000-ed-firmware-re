# -*- coding: utf-8 -*-
# 反汇编指定 VA 区间（32 位 x86），仅用于确认字符串引用点上下文
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import sys
from capstone import *
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
SEC = [('.text',0x1000,0xBD000,0x10001000),('.rdata',0xBE000,0x13000,0x100BE000),
       ('.data',0xD1000,0x8000,0x100D1000),('.rsrc',0xD9000,0x7000,0x100DA000)]
def va2off(va):
    for n,praw,rs,v in SEC:
        if v <= va < v+rs: return praw+(va-v)
    return None
def dis(va, n, stop_ret=True):
    off = va2off(va)
    buf = d[off:off+n]
    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail=False
    for i in md.disasm(buf, va):
        print('%08X  %-24s %s %s' % (i.address, i.bytes.hex(), i.mnemonic, i.op_str))
if __name__ == '__main__':
    va = int(sys.argv[1], 16); n = int(sys.argv[2], 16) if len(sys.argv)>2 else 0x100
    dis(va, n)
