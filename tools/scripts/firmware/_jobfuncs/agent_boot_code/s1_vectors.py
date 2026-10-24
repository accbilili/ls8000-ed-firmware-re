# agent_boot-code 公共分析脚本：向量表 + 复位入口 + 0x192 缝隙函数
# 只读 D:\。base=0（地址=文件偏移）。
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
from h8dis import H8, s8, s16, R32, R16
from h8fix import load_entries_fixed

BB = open(sample('LS8000_bootblock.bin'), 'rb').read()
FULL = open(sample('LS8000_full_512K.bin'), 'rb').read()
ENT = load_entries_fixed(sample('h8.lst'))
h = H8(BB, ENT, base=0)

def cls_target(t):
    """目标地址分类"""
    if t == 0:
        return 'zero'
    if t < 0x10000:
        return 'bootblock'
    if t < 0x10000 + 228345:
        return 'app(111_ROM)'
    if t < 0x200000:
        return 'gap'
    if 0x200000 <= t < 0x300000:
        return 'ASIC/FPGA'
    if 0x400000 <= t < 0x440000:
        return 'RAM'
    if t >= 0xFFFF00:
        return 'IO'
    return 'other'

def dump_vectors():
    print("=== 向量表 256 项（0x0-0x3FF，每项 u32 大端）===")
    print("idx  addr     vec_addr  -> target   class")
    vecs = []
    for i in range(256):
        off = i * 4
        v = (BB[off] << 24) | (BB[off+1] << 16) | (BB[off+2] << 8) | BB[off+3]
        vecs.append(v)
        c = cls_target(v)
        print(f"vec[{i:3d}] 0x{off:04X} -> 0x{v:06X}  {c}")
    return vecs

def cluster(vecs):
    from collections import defaultdict
    cl = defaultdict(list)
    for i, v in enumerate(vecs):
        cl[v].append(i)
    print("\n=== 聚类（按目标地址）===")
    for v in sorted(cl):
        idxs = cl[v]
        print(f"0x{v:06X} ({cls_target(v)}): vec idx {idxs}")
    return cl

def disasm(start, end, label=''):
    print(f"\n=== 反汇编 0x{start:06X}..0x{end:06X} {label} ===")
    pc = start
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if sz is None:
            print(f"0x{pc:06X}: .byte {BB[pc]:02X}          {BB[pc+1]:02X}")
            pc += 2
            continue
        ops = ''
        if a1 is not None and a2 is not None:
            ops = f"{a1}, {a2}"
        elif a1 is not None:
            ops = a1
        raw = ' '.join(f'{BB[pc+k]:02X}' for k in range(sz))
        print(f"0x{pc:06X}: {raw:<20} {nm} {ops}")
        pc = nxt

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('vec', 'all'):
        vecs = dump_vectors()
        cluster(vecs)
    if what in ('reset', 'all'):
        disasm(0x180, 0x284, 'reset/NMI area')
    if what in ('192', 'all'):
        disasm(0x192, 0x210, '0x192 gap fn')
