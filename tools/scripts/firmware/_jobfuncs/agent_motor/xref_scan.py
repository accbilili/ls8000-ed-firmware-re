"""固件级交叉引用扫描：找出关键 RAM/IO 地址的所有访问点。

方法：对镜像每个 2 字节对齐点解码一条指令，若操作数中含目标地址则记录。
只读 D:\，输出到本目录。
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
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

TARGETS = {
    0x4202E0: '轴1位置(cur)', 0x4202DE: '轴1速度', 0x4202E2: '轴1增量',
    0x4202E4: '轴1e1', 0x4202E6: '轴1状态', 0x4202E7: '轴1方向',
    0x4202E8: '轴1等待标志', 0x4202E9: '轴1高速模式',
    0x4202EC: '轴2位置(cur)', 0x4202EA: '轴2速度', 0x4202EE: '轴2状态',
    0x4202F3: '轴2等待标志', 0x4202F4: '轴2超时', 0x4202FC: '轴2位置镜像',
    0x440E42: 'pushed高字节副本', 0x440E43: 'DMA buf ptr', 0x440E50: '0x02B2D4入参',
    0x440E52: 'ptr', 0x440E58: '定时器参数', 0x440E5E: '脉冲计数?',
    0x440811: '表长', 0x440812: '传感器表', 0x440846: '0x40结果字节',
    0x44084C: '0x40指数', 0x44084E: '0x40周期', 0x440FDA: '0x42钳位目标',
    0x440FCE: '0x42 ramp', 0x440E63: '轴2方向', 0x440E64: '轴2标志4',
    0x400410: '请求块+8', 0x40040A: '请求块+2', 0x400408: '请求块',
    0x400402: '状态码A', 0x400404: '状态码B', 0x400D75: '0x42 busy',
    0x4003FE: '0x40 flag', 0x4003FF: '0x02B2D4 flag', 0x40041B: 'IO镜像',
    0x420301: '0x029D2A标志', 0x4202FF: '0x029D2A越界', 0x4202A2: '走片位置',
    0x4003FB: '片夹代码', 0x4003EC: 'ready-wait模式',
}

hits = {a: [] for a in TARGETS}
for off in range(0, len(d) - 8, 2):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        continue
    for x in (a1, a2):
        if not x:
            continue
        x = x.strip()
        if x.startswith('@'):
            x = x[1:]
        if not x.startswith('0x'):
            continue
        try:
            v = int(x, 16)
        except ValueError:
            continue
        if v in TARGETS:
            hits[v].append((off + BASE, nm, a1, a2))

lines = []
for a in sorted(hits):
    tag = TARGETS[a]
    lines.append(f'=== 0x{a:06X} ({tag}) : {len(hits[a])} 处 ===')
    for addr, nm, a1, a2 in hits[a]:
        lines.append(f'  0x{addr:06X}  {nm:<9} ' + ', '.join(y for y in (a1, a2) if y))
open(os.path.join(OUT, 'xrefs.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(l for l in lines if l.startswith('===')))
