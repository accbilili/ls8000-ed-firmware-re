"""反汇编 ASIC 助手家族 0x02D000-0x02D340、0x03C1AE、0x03BD4A、0x018F06、0x03BFBE。只读 D:\。"""
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

def dis_linear(start, end, fname):
    lines = []
    pc = start - BASE
    while pc < end - BASE:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        pc = nxt
    open(os.path.join(OUT, fname), 'w').write('\n'.join(lines) + '\n')
    print(f'{fname}: {len(lines)} lines')

dis_linear(0x02D000, 0x02D340, 'asic_02D000.asm')
dis_linear(0x03C1AE, 0x03C194 + 0x60, 'f_03C1AE.asm')
dis_linear(0x03BD4A, 0x03BD4A + 0x200, 'f_03BD4a_full.asm')
dis_linear(0x018F06, 0x018F06 + 0x120, 'f_018F06.asm')
dis_linear(0x03BFBE, 0x03BFBE + 0x100, 'f_03BFBE.asm')
