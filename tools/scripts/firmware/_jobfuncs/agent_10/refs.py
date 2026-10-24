"""全固件引用分析：对给定 RAM 地址，找所有引用它的指令并分类读/写。
方法：字节模式预筛（H8 大端，地址字节原样出现在指令流），再回溯 2 字节对齐起点
用修复版解码器验证该指令操作数中含此地址，并按指令助记符分类读写。
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
import sys, re
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def addr_bytes(a):
    return a.to_bytes(4, 'big')[1:]  # 低 3 字节，如 0x400406 -> 40 04 06

def find_refs(addr):
    pat = addr_bytes(addr)
    astrs = {f'0x{addr:06x}', f'0x{addr:08x}'}  # 操作数 6 位、立即数 8 位
    hits = []
    start = 0
    while True:
        i = d.find(pat, start)
        if i < 0:
            break
        start = i + 1
        # 回溯：尝试从 i-11..i 的偶数对齐起点解码，看哪条指令覆盖该地址且操作数含它
        for back in range(0, 12):
            s = i - back
            if s < 0 or s % 2:
                continue
            sz, nm, a1, a2, nxt = h.decode(s)
            if nm is None:
                continue
            text = ' '.join(x for x in (a1, a2) if x)
            if any(a in text for a in astrs) and (s + sz) > i:
                hits.append((s + BASE, nm, text, sz))
                break
    return hits

TARGETS = {
    0x400406: '状态字（0x10/0x11..0x15/0x20 子状态码载体）',
    0x400D77: '父函数置 1（识别正常?）',
    0x400D78: '父函数置 1',
    0x400D7A: '模式字节（holder 格式）',
    0x400DB4: '分支选择（0x3708E vs 0x37084）',
    0x400D7C: 'X 坐标',
    0x400D7E: 'Y 坐标',
    0x4202F8: '电机目标位置',
    0x40064E: 'holder 记录表基址',
    0x400DA0: 'holder 标志',
    0x400DB7: '0x03C030 门禁',
}
for addr, desc in TARGETS.items():
    hits = find_refs(addr)
    # 去重（同一指令多次命中）
    uniq = {}
    for pc, nm, text, sz in hits:
        uniq[pc] = (nm, text, sz)
    print(f'=== 0x{addr:06X} ({desc}): {len(uniq)} 条引用指令 ===')
    for pc in sorted(uniq):
        nm, text, sz = uniq[pc]
        print(f'  0x{pc:06X}  {nm:<9} {text}')
