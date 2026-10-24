# -*- coding: utf-8 -*-
# 扫描 .rdata / .rsrc 的 ASCII 与 UTF-16LE 字符串，并做 VA 引用反查
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import re, json, struct, sys

P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
IB = 0x10000000
SEC = [
    ('.text',  0x1000,  0xBD000, 0x10001000, 0xBCA9A),
    ('.rdata', 0xBE000, 0x13000, 0x100BE000, 0x127F8),
    ('.data',  0xD1000, 0x8000,  0x100D1000, 0x8E08),
    ('.rsrc',  0xD9000, 0x7000,  0x100DA000, 0x6008),
    ('.reloc', 0xE0000, 0xA000,  0x100E1000, 0x9F2E),
]
def va2off(va):
    for n, praw, rs, v, vs in SEC:
        if v <= va < v + vs:
            o = praw + (va - v)
            if o < praw + rs:
                return o
    return None
def off2va(off):
    for n, praw, rs, v, vs in SEC:
        if praw <= off < praw + rs:
            return v + (off - praw)
    return None

def scan_ascii(buf, base):
    res = []
    for m in re.finditer(rb'[\x20-\x7E]{4,}', buf):
        res.append((base + m.start(), m.group().decode('latin1')))
    return res
def scan_u16(buf, base):
    res = []
    for m in re.finditer(rb'(?:[\x20-\x7E]\x00){4,}', buf):
        res.append((base + m.start(), m.group().decode('utf-16le')))
    return res

strs = []
for name, praw, rs, v, vs in SEC:
    if name not in ('.rdata', '.rsrc', '.data'):
        continue
    buf = d[praw:praw + min(rs, vs)]
    for va, t in scan_ascii(buf, v):
        strs.append({'va': va, 'enc': 'A', 'sec': name, 'text': t})
    for va, t in scan_u16(buf, v):
        strs.append({'va': va, 'enc': 'U', 'sec': name, 'text': t})
strs.sort(key=lambda x: x['va'])

# 建立 .text 中 4 字节立即数索引（小端 VA）
text = d[0x1000:0x1000 + 0xBD000]
imm_idx = {}
for i in range(0, len(text) - 3):
    pass
# 用 regex 更快：对每个串做一次搜索太慢（数千×BD000）。改为一次性扫描所有 4 字节
# 收集所有 4 字节窗口中值落在 [0x10001000,0x100E2000) 的位置
hits = {}
pat = re.compile(rb'[\x00-\xff]{4}')
n = len(text)
# 用 numpy 加速
import numpy as np
arr = np.frombuffer(text, dtype=np.uint8)
w = (arr[0:n-3].astype(np.uint32)
     | (arr[1:n-2].astype(np.uint32) << 8)
     | (arr[2:n-1].astype(np.uint32) << 16)
     | (arr[3:n].astype(np.uint32) << 24))
mask = (w >= 0x10001000) & (w < 0x100E2000)
idxs = np.nonzero(mask)[0]
for i in idxs:
    val = int(w[i]); va = 0x10001000 + int(i)
    hits.setdefault(val, []).append(va)

# 同时扫 .rdata/.data 的指针表（4 字节 VA）
rd = d[0xBE000:0xBE000 + 0x127F8]
dat = d[0xD1000:0xD1000 + 0x8E08]
ptr_hits = {}
for name, buf, base in (('.rdata', rd, 0x100BE000), ('.data', dat, 0x100D1000)):
    a = np.frombuffer(buf, dtype=np.uint8)
    m = len(buf)
    ww = (a[0:m-3].astype(np.uint32) | (a[1:m-2].astype(np.uint32) << 8)
          | (a[2:m-1].astype(np.uint32) << 16) | (a[3:m].astype(np.uint32) << 24))
    mm = (ww >= 0x10001000) & (ww < 0x100E2000)
    for i in np.nonzero(mm)[0]:
        ptr_hits.setdefault(int(ww[i]), []).append(base + int(i))

out = []
for s in strs:
    va = s['va']
    refs = list(hits.get(va, []))
    ptrs = list(ptr_hits.get(va, []))
    pref = []
    for p in ptrs:
        pref += list(hits.get(p, []))
    out.append({'va': hex(va), 'enc': s['enc'], 'sec': s['sec'], 'text': s['text'],
                'refs': [hex(x) for x in refs], 'ptr': [hex(x) for x in ptrs],
                'refs2': [hex(x) for x in pref]})

json.dump(out, open('s2_strings.json', 'w'), indent=0, ensure_ascii=False)
print('total strings', len(out), 'ascii', sum(1 for x in out if x['enc'] == 'A'),
      'utf16', sum(1 for x in out if x['enc'] == 'U'))
print('with direct ref', sum(1 for x in out if x['refs']))
print('with ptr', sum(1 for x in out if x['ptr']))
