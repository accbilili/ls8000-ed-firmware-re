""" dump 关键指令的原始字节，核对编码语义（只读 D:\）。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

for a in (0x026A94, 0x026A98, 0x026A9A, 0x026A9C, 0x026A9E, 0x026AA2, 0x026AA6,
          0x026AB2, 0x026AB4, 0x026AB6, 0x026AB8, 0x03A5D6, 0x03A5DE, 0x03A6CE, 0x03A6E6,
          0x03A4DA, 0x03A4D6, 0x03A4D8):
    sz, nm, a1, a2, nxt = h.decode(a - BASE)
    raw = ' '.join(f'{b:02X}' for b in d[a-BASE:a-BASE+sz])
    print(f'0x{a:06X}  sz={sz}  {nm:<10} {a1}, {a2}   bytes: {raw}')

# 查 h8.lst 里 mov.w / extu 相关条目
print('\n--- h8.lst mov.w/extu 相关条目（前 30 条）---')
n = 0
for l in open(sample('h8.lst'), encoding='utf-8', errors='replace'):
    if ('mov.w' in l or 'extu' in l.lower()) and n < 30:
        print(l.rstrip())
        n += 1
