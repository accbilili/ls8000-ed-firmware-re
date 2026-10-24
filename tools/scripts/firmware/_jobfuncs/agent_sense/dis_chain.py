"""反汇编关键区域，建立完整链路：
- 0x0114b8（E0 顶层处理入口，fn 0x020E86 调用它）
- 0x011400-0x011500（含 0x011464/0x0114AE/0x0114E0）
- 0x020B84 主循环附近（0x020B84-0x020C10）
- 0x020ec0（status==0 分支）
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
        if nm in ('bsr','jsr') and a1: mark += f'   [call]'
        print(txt + mark)
        pc = nxt

dis_range(0x011460, 0x0114E0, 'fn_011460 wrapper (calls 0x0116a0 + er6/er4=0x400436)')
dis_range(0x0114B8, 0x011540, 'fn_0114B8 E0 top handler')
dis_range(0x020B84, 0x020C10, 'main loop around 0x020B84')
dis_range(0x020EC0, 0x020F60, 'fn_020EC0 (status==0 branch)')
