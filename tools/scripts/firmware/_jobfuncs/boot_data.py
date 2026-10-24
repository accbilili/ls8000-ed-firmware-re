"""B18：引导块数据侧清点。
 1. 0x0000-0xFFFF 非零区域地图（run-length）
 2. 0x170-0x220 与 0x280/0x284 的反汇编
 3. 0x6000-0x607F 记录区与 0x6010 模板的字节级解读
 4. 全块内的 u32 指针/常量表探测（0x1xxx 区）
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
import sys, os, struct
from collections import Counter
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h8dis import H8
from h8fix import load_entries_fixed

d = open(sample('LS8000_bootblock.bin'), 'rb').read()
h = H8(d, load_entries_fixed(sample('h8.lst')), base=0)
OUT = os.path.dirname(os.path.abspath(__file__))

print('=' * 78)
print('B18 引导块数据侧')
print('=' * 78)

# ---------- 1. 非零区域地图 ----------
print('\n[1] 非零区域地图（按 64B 块）')
blocks = []
for b in range(0, len(d), 64):
    chunk = d[b:b + 64]
    if any(chunk):
        blocks.append(b)
# 合并相邻
runs = []
for b in blocks:
    if runs and b == runs[-1][1]:
        runs[-1][1] = b + 64
    else:
        runs.append([b, b + 64])
for a, b in runs:
    print(f'   0x{a:05X}-0x{b-1:05X}  ({b-a:5d} B)  非零 {sum(1 for x in d[a:b] if x):5d} 字节')

# ---------- 2. 0x170-0x220 / 0x280 / 0x284 反汇编 ----------
def dis_range(s, e, title):
    print(f'\n[{title}] 0x{s:05X}-0x{e-1:05X}')
    pc = s
    while pc < e:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print(f'   0x{pc:06X}  .byte 0x{d[pc]:02X}'); pc += 2
        else:
            print(f'   0x{pc:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)); pc = nxt
        if nm == 'rts':
            break

dis_range(0x170, 0x220, '2a 0x170-0x220（向量表尾 + 复位 + 缝隙）')
dis_range(0x280, 0x290, '2b 0x280/0x284（两个桩）')
dis_range(0x220, 0x280, '2c 0x220-0x280')

# ---------- 3. 0x6000 记录区 ----------
print('\n[3] 0x6000-0x607F 记录区（可写 flash 设置记录）')
for a in range(0x6000, 0x6080, 16):
    print(f'   0x{a:05X}: {d[a:a+16].hex(" ")}')

print('\n  0x6010 模板 17 B 逐字节（按 u16 BE 配对解释）：')
tpl = d[0x6010:0x6021]
print('   原始:', tpl.hex(' '))
words = [struct.unpack_from('>H', tpl, i)[0] for i in range(0, 16, 2)]
print('   u16 BE 配对:', ' '.join(f'0x{w:04X}({w})' for w in words), f' 余 1 字节 0x{tpl[16]:02X}({tpl[16]})')

print('\n  0x6000 记录前 16 B 逐 u16：')
rec = d[0x6000:0x6010]
for i in range(0, 16, 2):
    w = struct.unpack_from('>H', rec, i)[0]
    print(f'   +0x{i:02X}: 0x{w:04X} ({w})')
print('   前 4 字节作 u32 BE =', struct.unpack_from('>I', rec, 0)[0])

# ---------- 4. 0x17xx 区（flash 选择器附近） ----------
print('\n[4] 0x17C0-0x1A0 字节')
for a in range(0x17C0, 0x01A0, 16):
    print(f'   0x{a:05X}: {d[a:a+16].hex(" ")}')
print('   @0x17E =', hex(d[0x17E]), '（flash 命令集选择器，实测 0x53）')

# ---------- 5. 全块 u32 值频次（找常量表） ----------
print('\n[5] 数据区（0x0210-0xFFFF）里最常见的 u32 值')
cnt = Counter()
for a in range(0x0210, len(d) - 3, 2):
    cnt[struct.unpack_from('>I', d, a)[0]] += 1
for v, n in cnt.most_common(18):
    if v == 0:
        continue
    print(f'   0x{v:08X} ({v:<10}) x{n}')
