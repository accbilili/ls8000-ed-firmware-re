# -*- coding: utf-8 -*-
# st_rsrc2.py — 正确 RVA->文件偏移映射后解析 .rsrc
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
IB = 0x10000000
SEC = [('.text',0x1000,0xBD000,0x10001000),('.rdata',0xBE000,0x13000,0x100BE000),
       ('.data',0xD1000,0x8000,0x100D1000),('.rsrc',0xD9000,0x7000,0x100DA000),
       ('.reloc',0xE0000,0xA000,0x100E1000)]
def va2off(va):
    for n,praw,rs,v in SEC:
        if v <= va < v+rs: return praw+(va-v)
    raise ValueError(hex(va))
def at(va,n): return d[va2off(va):va2off(va)+n]

# RT_STRING 块（type 6）：标准格式，16 个 u16 长度前缀条目
blocks = [(63,0x100DAE40,178),(64,0x100DAEF8,120),(65,0x100DAF70,268),(66,0x100DB080,166),
          (67,0x100DD690,178),(113,0x100DB128,56),(115,0x100DB9B0,452),(116,0x100DBB78,162),
          (117,0x100DB160,332),(118,0x100DBC20,144),(119,0x100DB2B0,194),(121,0x100DC220,146),
          (122,0x100DC2B8,774),(123,0x100DC5C0,164),(126,0x100DB378,106),(131,0x100DB3E8,1478),
          (132,0x100DBCB0,314),(137,0x100DBDF0,1070),(138,0x100DD808,102),(143,0x100DD870,522),
          (144,0x100DDA80,114),(149,0x100DDAF8,488),(151,0x100DC668,150),(157,0x100DDCE0,528),
          (313,0x100DDEF0,1656),(314,0x100DE568,3760),(315,0x100DF418,1276),(376,0x100DFD08,42),
          (407,0x100DFD38,52),(419,0x100DFD70,76),(432,0x100DFB00,78),(435,0x100DFAB0,74),
          (438,0x100DFB50,100),(439,0x100DFBB8,160),(440,0x100DFC58,56),(441,0x100DFC90,116),
          (501,0x100DC800,40),(503,0x100DC828,38),(506,0x100DC850,2490),(507,0x100DC700,126),
          (513,0x100DC780,124),(519,0x100DD210,72),(521,0x100DD258,214),(522,0x100DD330,720),
          (524,0x100DD600,86),(525,0x100DD658,56),(526,0x100DD748,88),(527,0x100DD7A0,102),
          (532,0x100DFA78,50),(704,0x100DFDC0,228),(705,0x100DFEA8,200),(720,0x100DFF70,152),
          (938,0x100DF918,210),(939,0x100DF9F0,132)]
out = []
for bid, va, size in blocks:
    buf = at(va, size)
    p = 0; idx = 0
    while p + 2 <= len(buf) and idx < 16:
        n = struct.unpack_from('<H', buf, p)[0]
        sva = va + p + 2
        p += 2
        s = buf[p:p+n*2].decode('utf-16le', 'ignore')
        p += n*2
        if n:
            out.append({'id': (bid-1)*16+idx, 'block': bid, 'va': hex(sva), 'text': s})
        idx += 1
print('RT_STRING 非空条目 %d' % len(out))
for s in out:
    print('#%-5d %s %r' % (s['id'], s['va'], s['text']))

print('\n== VS_VERSIONINFO ==')
vb = at(0x100DAAF8, 900)
print('first 16:', ' '.join('%02X'%c for c in vb[:16]))
def parse(buf, base, depth, out2):
    p = 0
    while p + 6 <= len(buf):
        wLen, wVal, wType = struct.unpack_from('<HHH', buf, p)
        if wLen < 6 or p + wLen > len(buf): break
        q = p + 6; k = q
        while k + 1 < len(buf) and buf[k:k+2] != b'\x00\x00': k += 2
        key = buf[q:k].decode('utf-16le','ignore'); k = (k+2+3)&~3
        nb = wVal*(2 if wType==1 else 1)
        raw = buf[k:k+nb]
        val = raw.decode('utf-16le','ignore').rstrip('\x00') if wType==1 else ' '.join('%02X'%c for c in raw)
        out2.append((depth, base+p, key, wLen, wType, val))
        if depth < 3:
            parse(buf[k+nb:p+wLen], base+k+nb, depth+1, out2)
        p = (p + wLen + 3) & ~3
v = []
parse(vb, 0x100DAAF8, 0, v)
for depth, va, key, wl, wt, val in v:
    print('%s%-20s @0x%08X len=%-4d t=%d %r' % ('  '*depth, key, va, wl, wt, val))

print('\n== 自定义 type 1000 @0x100DAAE0 ==')
print(repr(at(0x100DAAE0, 18).decode('utf-16le','replace')))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'st_strtab.json'),'w'), indent=0, ensure_ascii=False)
