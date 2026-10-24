# -*- coding: utf-8 -*-
# st_rsrc.py — 解析 RT_STRING 表 / VS_VERSIONINFO / 自定义资源 1000
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import os, struct, json
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
def at(va, n): return d[va - 0x10000000: va - 0x10000000 + n]

print('== custom RT 1000 @0x100DAAE0 (18B) ==')
b = at(0x100DAAE0, 18)
print(' '.join('%02X' % c for c in b), '|', ''.join(chr(c) if 32 <= c < 127 else '.' for c in b))

print('\n== VS_VERSIONINFO @0x100DAAF8 ==')
vb = at(0x100DAAF8, 840)
# 逐层解析：wLength,wValueLength,wType, szKey(UTF16,4对齐), padding, Value, padding, children
def parse(buf, base, depth=0, out=None):
    if out is None: out = []
    p = 0
    while p + 6 <= len(buf):
        wLen, wVal, wType = struct.unpack_from('<HHH', buf, p)
        if wLen == 0: break
        q = p + 6
        # key
        k = q
        while k + 1 < len(buf) and buf[k:k+2] != b'\x00\x00':
            k += 2
        key = buf[q:k].decode('utf-16le', 'ignore')
        k = (k + 2 + 3) & ~3
        val_bytes = buf[k:k + wVal * (2 if wType == 1 else 1)]
        val = val_bytes.decode('utf-16le', 'ignore') if wType == 1 else val_bytes.hex()
        out.append((depth, hex(base + p), key, wLen, wVal, wType, val.strip('\x00')))
        # 递归剩余
        if depth < 3 and wLen > (k - p) + len(val_bytes):
            parse(buf[k + len(val_bytes): p + wLen], base + k + len(val_bytes), depth + 1, out)
        p += wLen
        while p % 4: p += 1
    return out
for depth, va, key, wl, wv, wt, val in parse(vb, 0x100DAAF8):
    print('%s%-22s va=%-10s len=%-4d type=%d %r' % ('  ' * depth, key, va, wl, wt, val))

print('\n== RT_STRING 全解（Japanese 1041）==')
# 资源块 id -> VA（来自 st_pe.json）
j = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st_pe.json')))
blocks = []
for r in j['resources']:
    if r['type'] == '6':
        blocks.append((int(r['lang']), r['va'], r['size']))
blocks.sort()
allstr = []
for bid, va, size in blocks:
    buf = at(int(va, 16), size)
    p = 0
    idx = 0
    while p + 2 <= len(buf):
        n = struct.unpack_from('<H', buf, p)[0]
        str_va = int(va, 16) + p + 2
        p += 2
        s = buf[p:p + n * 2].decode('utf-16le', 'ignore')
        p += n * 2
        sid = (bid - 1) * 16 + idx
        idx += 1
        if n:
            allstr.append({'id': sid, 'block': bid, 'va': hex(str_va), 'text': s})
print('共 %d 条非空字符串' % len(allstr))
for s in allstr:
    print('  #%-5d blk%-4d %s  %r' % (s['id'], s['block'], s['va'], s['text']))
json.dump(allstr, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st_strtab.json'), 'w'), indent=0, ensure_ascii=False)
