# -*- coding: utf-8 -*-
# st_refmap.py — .text 中所有指向 .rdata/.data 的 imm32，按目标地址聚类
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import re, struct, collections, json, os
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
text = d[0x1000:0x1000+0xBD000]; TV = 0x10001000
hits = collections.defaultdict(list)
for i in range(len(text)-4):
    v = struct.unpack_from('<I', text, i)[0]
    if 0x100BE000 <= v < 0x100E0000:
        hits[v].append(TV+i)
# 覆盖图
cover = bytearray(0x100E0000-0x100BE000)
for v in hits:
    base = v-0x100BE000
    cover[base:base+4] = b'\x01'*min(4, len(cover)-base)
# 找未被引用的连续块（>=16B）
segs = []
i = 0; n = len(cover)
while i < n:
    if not cover[i]:
        j = i
        while j < n and not cover[j]: j += 1
        if j-i >= 16: segs.append((0x100BE000+i, j-i))
        i = j
    else:
        i += 1
print('未被任何 imm32 指向的 .rdata/.data 区间（>=16B），共 %d 段' % len(segs))
for va, ln in segs:
    print('0x%08X len=%-5d' % (va, ln))
json.dump({'hits': {hex(k): [hex(x) for x in v] for k, v in hits.items()}}, open('st_refmap.json','w'))
