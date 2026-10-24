"""最后收尾：
1. 反汇编 0x021200-0x021600：识别含读点 0x0213BE / 0x02157E 的函数入口与调用者
2. 反汇编 0x022100-0x022320 找 0x022308 的宿主函数；0x022380-0x022440 找 0x022434 宿主
3. sense[0x01] 条目（fn 0x011000 写 0x0001）
4. 0x026BF8 parse 层入口上下文（er6=0x400436 @0x026C14）
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

dis_range(0x0212C0, 0x021420, 'fn containing read 0x0213BE')
dis_range(0x0214A0, 0x0215A0, 'fn containing read 0x02157E (pathA->400436 merge)')
dis_range(0x022100, 0x022320, 'host of 0x022308 (calls fn 0x022AD6)')
dis_range(0x022380, 0x022440, 'host of 0x022434 (calls fn 0x022BF2)')
dis_range(0x026BF8, 0x026C40, 'parse layer 0x026BF8 (er6=0x400436 @0x026C14)')

def rd(addr, n):
    off = addr - BASE
    return d[off:off+n]
print('\nsense[0x01] @ 0x01914F =', rd(0x01914F, 5).hex(' '))
