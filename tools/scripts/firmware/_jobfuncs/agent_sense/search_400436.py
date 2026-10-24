"""搜索 0x400436 的全部引用（读点/写点）。

策略：
1. 全文件 2 字节对齐线性扫查 decode，收集操作数含 0x400436 的指令
   （覆盖 abs16 @0x400436 / abs32 @0x400436 / r32d32hh @(0x400436,erN) / imm32 #0x00400436）。
2. 原始字节搜索 40 04 36（abs16 尾字节）与 00 40 04 36（abs32 / r32d32hh / imm32），
   对每个命中尝试 X-2/X-4/X-6 起始 decode 反确认（防止线性扫查因未对齐边界漏掉）。
3. 也搜索 40 04 36 出现在数据表中的情况（非指令上下文）。
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
import sys, json
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
N = len(d)
print(f'file size = {N} bytes = 0x{N:X}; addr range 0x{BASE:06X}-0x{BASE+N:06X}')

TARGET = 0x400436

# ---- 方法1: 全文件 2 字节对齐线性扫查 ----
hits1 = []
for off in range(0, N - 8, 2):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        continue
    txt = ' '.join(x for x in (a1, a2) if x)
    if '400436' in txt:
        hits1.append((off + BASE, sz, nm, txt))

print(f'\n=== 方法1 线性扫查命中 {len(hits1)} 条 ===')
for a, sz, nm, txt in hits1:
    print(f'0x{a:06X}  {nm:<10} {txt}')

# ---- 方法2: 原始字节搜索 ----
def find_all(pat):
    res = []
    i = d.find(pat)
    while i != -1:
        res.append(i)
        i = d.find(pat, i + 1)
    return res

hits2 = []
for pat in (bytes.fromhex('400436'), bytes.fromhex('00400436')):
    for off in find_all(pat):
        for start in (off - 2, off - 4, off - 6):
            if start < 0:
                continue
            sz, nm, a1, a2, nxt = h.decode(start)
            if nm is None:
                continue
            txt = ' '.join(x for x in (a1, a2) if x)
            if '400436' in txt and (start + BASE) not in [x[0] for x in hits1]:
                hits2.append((start + BASE, sz, nm, txt, off))

print(f'\n=== 方法2 原始字节反确认（方法1 之外）命中 {len(hits2)} 条 ===')
for a, sz, nm, txt, raw in hits2:
    print(f'0x{a:06X}  {nm:<10} {txt}   (raw 0x{raw+BASE:06X})')

# ---- 方法3: 原始字节搜索全部命中点（含数据表上下文）----
print('\n=== 方法3 原始字节命中点全列表 ===')
for pat in (bytes.fromhex('400436'), bytes.fromhex('00400436')):
    for off in find_all(pat):
        # 上下文: 前后各 8 字节
        ctx = d[max(0, off - 8):off + len(pat) + 8]
        print(f'off 0x{off:06X} (addr 0x{off+BASE:06X}) pat={pat.hex()}: ctx={ctx.hex()}')

json.dump({'linear': hits1, 'raw': hits2}, open(
    r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs/agent_sense/hits_400436.json', 'w'), indent=1)
print('\nsaved hits_400436.json')
