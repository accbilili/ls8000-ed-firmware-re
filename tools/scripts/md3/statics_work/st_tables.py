# -*- coding: utf-8 -*-
# st_tables.py — 在 .rdata/.data 中找「单调递增数值序列」「规律步长数组」「指针表」
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct, os, json
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
SEC = [('.rdata',0xBE000,0x13000,0x100BE000,0x127F8),
       ('.data', 0xD1000,0x8000, 0x100D1000,0x8E08)]

def runs_u16(buf, base, lo, hi, minlen=5):
    res = []
    i = 0; n = len(buf)//2
    vals = struct.unpack_from('<%dH' % n, buf, 0)
    while i < n:
        j = i
        while j+1 < n and lo <= vals[j+1] <= hi and vals[j+1] > vals[j] and vals[j+1]-vals[j] < 6000:
            j += 1
        if j-i+1 >= minlen:
            res.append((base+i*2, list(vals[i:j+1])))
            i = j+1
        else:
            i += 1
    return res
def runs_u32(buf, base, lo, hi, minlen=5):
    res = []
    n = len(buf)//4
    vals = struct.unpack_from('<%dI' % n, buf, 0)
    i = 0
    while i < n:
        j = i
        while j+1 < n and lo <= vals[j+1] <= hi and vals[j+1] > vals[j] and vals[j+1]-vals[j] < 100000:
            j += 1
        if j-i+1 >= minlen:
            res.append((base+i*4, list(vals[i:j+1])))
            i = j+1
        else:
            i += 1
    return res

for name, praw, rs, v, vs in SEC:
    buf = d[praw:praw+min(rs,vs)]
    print('########## %s ##########' % name)
    print('--- u16 递增序列 (>=5 项, 20..20000) ---')
    for va, vals in runs_u16(buf, v, 20, 20000):
        if len(vals) >= 6 or (len(vals) >= 5 and vals[0] < 5000):
            print('0x%08X n=%-3d %s' % (va, len(vals), vals[:24]))
    print('--- u32 递增序列 ---')
    for va, vals in runs_u32(buf, v, 20, 100000):
        print('0x%08X n=%-3d %s' % (va, len(vals), vals[:20]))
