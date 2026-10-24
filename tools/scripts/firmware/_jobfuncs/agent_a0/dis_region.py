"""反汇编 0x028A00-0x028E80 区域，定位含 0x028DC2 的函数入口；并找其调用者。只读 D:\。"""
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

lines = []
pc = 0x028A00 - BASE
while pc < 0x028E80 - BASE:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        pc += 1
        continue
    lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    pc = nxt
open(os.path.join(OUT, 'region_028A00.asm'), 'w').write('\n'.join(lines) + '\n')
print(f'{len(lines)} lines -> region_028A00.asm')

# 全镜像找 jsr/bsr/jmp 到 0x028xxx 的调用（在 0x027000-0x02A000 范围内搜目标）
print('\n=== 对 0x028000-0x029200 的调用/跳转 ===')
pc = 0
while pc < len(d) - 16:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        pc += 2
        continue
    if nm in ('jsr', 'bsr', 'jmp') and a1 and a1.startswith('0x'):
        try:
            t = int(a1, 16)
            if 0x028000 <= t < 0x029200:
                print(f'0x{pc+BASE:06X}  {nm:<5} -> 0x{t:06X}')
        except ValueError:
            pass
    pc = nxt if sz and sz > 0 else pc + 2
