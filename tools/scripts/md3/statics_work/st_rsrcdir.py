# -*- coding: utf-8 -*-
# 手动解析 .rsrc 目录（不依赖 pefile），并输出每块真实起止
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct, sys
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
IB = 0x10000000
RSRC_VA = 0x100DA000
RSRC_OFF = 0xD9000
base = d[RSRC_OFF:]

def u16(o): return struct.unpack_from('<H', base, o)[0]
def u32(o): return struct.unpack_from('<I', base, o)[0]

def name_of(o):
    # o 指向 IMAGE_RESOURCE_DIR_STRING_U
    n = u16(o)
    return base[o+2:o+2+n*2].decode('utf-16le', 'ignore')

def walk(off, level, path):
    nnamed = u16(off+12); nid = u16(off+14)
    for i in range(nnamed + nid):
        e = off + 16 + i*8
        nm, tgt = u32(e), u32(e+4)
        label = name_of(off + (nm & 0x7FFFFFFF)) if nm & 0x80000000 else str(nm)
        if tgt & 0x80000000:
            walk(tgt & 0x7FFFFFFF, level+1, path+[label])
        else:
            ds = tgt
            rva, size, cp, rsv = struct.unpack_from('<IIII', base, ds)
            print('%-6s %-8s %-8s rva=0x%06X va=0x%08X size=%-6d cp=%d' % (
                path[0], path[1] if len(path)>1 else '', label, rva, IB+rva, size, cp))
            print('        raw@file0x%X' % (RSRC_OFF + (rva - (RSRC_VA - IB))))
walk(0, 0, [])
