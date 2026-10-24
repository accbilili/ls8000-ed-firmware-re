"""对关键 RAM 变量做全镜像访问点普查（字节模式 + 解码复核，覆盖 cfg 空洞）。"""
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

VARS = [0x4202A2, 0x4202B2, 0x4202B4, 0x4202EC, 0x4202FC, 0x4202FE,
        0x420301, 0x4202A4, 0x4202A8, 0x4202EE, 0x4202E6, 0x4202E0,
        0x440E60, 0x440E61, 0x440E62, 0x44080E, 0x44080F, 0x440E40]

for v in VARS:
    pat = v.to_bytes(4, 'big')
    rows = []
    i = d.find(pat)
    while i >= 0:
        a = i + BASE
        # 尝试在该位置前 2/4/6 字节（偶对齐）解指令，看操作数是否含该地址
        for back in (2, 4, 6, 8):
            p = i - back
            if p < 0 or p % 2:
                continue
            sz, nm, a1, a2, nxt = h.decode(p)
            if nm is None:
                continue
            txt = ' '.join(str(x) for x in (a1, a2) if x)
            if f'0x{v:06x}' in txt.lower() and p + sz >= i + 4 and p <= i:
                rw = 'W' if (a2 and str(a2).startswith('@0x')) else ('R' if (a1 and str(a1).startswith('@0x')) else '?')
                rows.append((p + BASE, nm, a1, a2, rw, sz))
                break
        i = d.find(pat, i + 1)
    print(f'=== 0x{v:06X}: {len(rows)} 处')
    for a, nm, a1, a2, rw, sz in sorted(rows):
        print(f'  0x{a:06X} {nm:<6} {str(a1):<22} {str(a2):<10} {rw} sz={sz}')
