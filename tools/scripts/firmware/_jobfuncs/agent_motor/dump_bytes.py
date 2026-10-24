"""核验 0x01872E / 0x018708 / 0x02B196 关键指令的原始字节与操作数渲染。"""
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
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def dump(lo, hi, note=''):
    print(f'--- 0x{lo:06X}-0x{hi:06X} {note} ---')
    pc = lo - BASE
    while pc < hi - BASE:
        sz, nm, a1, a2, nxt = h.decode(pc)
        raw = ' '.join(f'{b:02X}' for b in d[pc:pc+sz])
        if nm is None:
            print(f'0x{pc+BASE:06X} [{raw:<14}] .byte 0x{d[pc]:02X}'); pc += 2
        else:
            print(f'0x{pc+BASE:06X} [{raw:<14}] {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)); pc = nxt

dump(0x01872E, 0x01876A, '0x01872E 无符号除法')
dump(0x018708, 0x01872E, '0x018708 有符号除法包装')
dump(0x02B196, 0x02B1E4, '0x02B196 查表')
dump(0x02B1E4, 0x02B22E, '0x02B1E4 定标')
dump(0x02B22E, 0x02B276, '0x02B22E 定时器装载')
