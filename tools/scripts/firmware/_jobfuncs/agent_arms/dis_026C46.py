"""反汇编解析层 0x026C46（E0 payload -> 工作区 0x400C55 的拷贝），确认 CDB 源地址。"""
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
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

START = 0x026C46
END = 0x026D80   # 线性扫描上限
lines = []
pc = START - BASE
n = 0
while pc < END - BASE and n < 160:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        break
    raw = ' '.join(f'{d[pc+i]:02X}' for i in range(sz))
    op = ', '.join(x for x in (a1, a2) if x)
    lines.append(f'0x{pc+BASE:06X}  {raw:<20} {nm:<9} {op}')
    if nm == 'rts':
        break
    pc = nxt
    n += 1
open(os.path.join(OUT, 'f_026C46_parse.asm'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines[:80]))
