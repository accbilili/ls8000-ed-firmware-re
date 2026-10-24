# -*- coding: utf-8 -*-
# st_loadstr.py — 找 LoadStringA 调用点与其字符串 id 立即数
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import re, struct, os
from capstone import *
P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
def off(va): return va - 0x10000000 + (0x1000 if False else 0)  # .text 恒等映射
text = d[0x1000:0x1000+0xBD000]
TEXT_VA = 0x10001000
md = Cs(CS_ARCH_X86, CS_MODE_32)

for name, iat in (('LoadStringA', 0x100BE1AC), ('FindResourceA', 0x100BE07C),
                  ('LoadResource', 0x100BE078), ('GetProcAddress', 0x100BE024),
                  ('LoadLibraryA', 0x100BE028)):
    pat = b'\xff\x15' + struct.pack('<I', iat)
    hits = [m.start() for m in re.finditer(re.escape(pat), text)]
    print('== %s : %d 处 ==' % (name, len(hits)))
    for h in hits:
        va = TEXT_VA + h
        start = max(0, h - 20)
        print('  call @0x%08X' % va)
        for i in md.disasm(text[start:h+6], TEXT_VA+start):
            print('      %08X  %-22s %s %s' % (i.address, i.bytes.hex(), i.mnemonic, i.op_str))
    print()
