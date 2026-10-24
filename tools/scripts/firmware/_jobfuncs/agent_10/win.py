"""反汇编指定地址窗口（线性，不跟分支），用于人工分析上下文。
只读 D:\。
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
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

WINDOWS = [
    (0x028560, 0x028610, 'w_0285_400406_bit4'),
    (0x027750, 0x0277E0, 'w_0277_d77d78'),
    (0x027E20, 0x027EB0, 'w_027E_d77d78'),
    (0x03C560, 0x03C5C0, 'w_03C5_400406'),
    (0x03CC90, 0x03CCF0, 'w_03CC_400406'),
    (0x02EE80, 0x02EF60, 'w_02EE_d7c_reader'),
    (0x02FFD0, 0x030010, 'w_02FF_4202f8'),
    (0x0301B0, 0x030210, 'w_0301_4202f8'),
    (0x028CF0, 0x028E00, 'w_028D_4202f8'),
    (0x03A8F0, 0x03A990, 'w_03A9_d77d78_db7'),
]
for lo, hi, name in WINDOWS:
    print(f'===== {name}: 0x{lo:06X}-0x{hi:06X} =====')
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        print(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        pc = nxt if nxt else pc + sz
    print()
