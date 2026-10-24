"""按地址区间线性反汇编（辅助证据：ISR、位置写入者、校准应用、小助手）。"""
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

RANGES = [
    (0x027F24, 0x027F70, 'B0 处理函数(读 0x4202E0)'),
    (0x018708, 0x01872E, '0x018708 除法变体'),
    (0x02B11A, 0x02B160, '0x02B11A 延时'),
    (0x02B450, 0x02B490, '0x02B450 方向设置'),
    (0x02B600, 0x02B650, '0x02B618 区域'),
    (0x02B650, 0x02B840, '轴1 ISR/脉冲状态机区'),
    (0x02BB40, 0x02BBE0, '轴1 位置写入区'),
    (0x02BD40, 0x02BD90, '0x02BD5A 位置写入区'),
    (0x02AB3E, 0x02AC80, '校准应用区(440846/84C/84E)'),
    (0x02BF00, 0x02C000, '0x02BFA8 区域'),
    (0x02C0E2, 0x02C180, '0x02C0E2 区域'),
    (0x02C300, 0x02C400, '0x02C376 区域'),
    (0x02C5E0, 0x02C700, '轴2 ISR 区1'),
    (0x02C700, 0x02C8B4, '轴2 ISR 区2'),
    (0x02CB20, 0x02CB70, '0x400410 读取区'),
    (0x02CD40, 0x02CE80, '轴2 位置/状态写入区'),
    (0x03AF00, 0x03AF40, '0x03AF1A 写 0x4202E9 区'),
]

for lo, hi, tag in RANGES:
    print(f'########## {tag}  0x{lo:06X}-0x{hi:06X} ##########')
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}'); pc += 2
        else:
            print(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)); pc = nxt
    print()
