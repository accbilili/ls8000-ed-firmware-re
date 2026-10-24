"""补充反汇编：
- fn 0x0114D8 全体（命令分派表 0x19102，er4=0x400436 写出尾 0x011624/0x011638）
- 0x021150-0x021200（写出尾 0x021198；读点 0x0213BE/0x02157E 上下文）
- 0x026B80-0x026D20（0x026BCA default 臂写 0x56；0x026CDC 写 0x50）
- fn 0x022AD6 / 0x022BF2（读点 0x022AFE/0x022C00）
- 读点 0x012A7E 上下文
"""
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

def dis_range(lo, hi, label):
    print(f'\n===== {label}  0x{lo:06X}-0x{hi:06X} =====')
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        txt = f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)
        mark = '   <<< 0x400436' if '400436' in txt else ''
        print(txt + mark)
        pc = nxt

dis_range(0x0114D8, 0x0116A0, 'fn_0114D8 command dispatch (er4=0x400436)')
dis_range(0x021150, 0x0211D0, 'status write tail 0x021198')
dis_range(0x026B80, 0x026BE0, 'around 0x026BCA (0x56 write, exec default arm)')
dis_range(0x026C80, 0x026D10, 'around 0x026CDC (0x50 write)')
dis_range(0x022AD6, 0x022B40, 'fn_022AD6 (read 0x022AFE)')
dis_range(0x022BF2, 0x022C60, 'fn_022BF2 (read 0x022C00)')
dis_range(0x012A40, 0x012AC0, 'around read 0x012A7E')
