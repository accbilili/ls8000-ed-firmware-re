# -*- coding: utf-8 -*-
# st_idxtab.py — 找 [base + idx*4] / [+idx*2] 形式的静态表引用
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import re, struct, collections
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
text = d[0x1000:0x1000+0xBD000]; TV = 0x10001000
# ModRM mod=00 rm=100 (SIB) 的常见形式；reg 任意
pats = []
for op, desc, scale in ((0x8, 'u32', 4),):
    pass
res = collections.defaultdict(list)
for rm in (0x85, 0x8D, 0x95, 0xB5, 0xBD):      # eax*4, ecx*4, edx*4, esi*4, edi*4
    pat = bytes([0x8B, 0x04, rm])
    for m in re.finditer(re.escape(pat), text):
        imm = struct.unpack_from('<I', text, m.start()+3)[0]
        if 0x100BE000 <= imm < 0x100E0000:
            res[(imm, 4)].append(TV+m.start())
for rm in (0x45, 0x4D, 0x55, 0x75, 0x7D):      # eax*2 ...
    for pre in (b'\x66\x8b\x04', b'\x0f\xb7\x04'):
        for m in re.finditer(re.escape(pre + bytes([rm])), text):
            imm = struct.unpack_from('<I', text, m.start()+4)[0]
            if 0x100BE000 <= imm < 0x100E0000:
                res[(imm, 2)].append(TV+m.start())
for rm in (0x85, 0x8D, 0x95, 0xB5, 0xBD):
    for pre in (b'\x8b\x04', b'\x8d\x04'):
        pass
print('候选基址 %d 个' % len(res))
for (imm, w), sites in sorted(res.items()):
    print('0x%08X w=%d refs=%d %s' % (imm, w, len(sites), [hex(x) for x in sites[:6]]))
