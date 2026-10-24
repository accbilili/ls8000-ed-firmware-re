"""B17：引导块代码侧分析（bootblock.bin，地址 = 文件偏移 0x0-0xFFFF）。

目标：
 1. 向量表 256 项全貌 + 分类
 2. 复位入口 0x000180
 3. 应用↔引导块唯一缝隙函数 0x000192（应用主循环每轮 jsr 一次）
 4. 找写 0x40043C（CDB 落地）与读 0x400408（请求块消费方）的代码
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
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h8dis import H8
from h8fix import load_entries_fixed

BASE = 0
d = open(sample('LS8000_bootblock.bin'), 'rb').read()
h = H8(d, load_entries_fixed(sample('h8.lst')), base=BASE)
OUT = os.path.dirname(os.path.abspath(__file__))

UNCOND = {'jmp', 'bra', 'bt'}
NEVER = {'bf'}
CALLS = {'jsr', 'bsr'}
CONDS = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}


def parse_tgt(s):
    if s is None:
        return None
    s = s.strip()
    if s.startswith('0x'):
        try:
            return int(s, 16)
        except ValueError:
            return None
    return None


def walk(entry, h):
    seen = {}
    edges = []
    work = [entry]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None
                break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts':
                break
            if nm in CALLS:
                edges.append((pc, 'call', parse_tgt(a1)))
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append((pc, 'jmp', t))
                if t is not None and 0 <= t < len(d):
                    work.append(t)
                break
            elif nm in NEVER:
                edges.append((pc, 'never', parse_tgt(a1)))
            elif nm in CONDS:
                t = parse_tgt(a1)
                edges.append((pc, 'bcc', t))
                if t is not None and 0 <= t < len(d):
                    work.append(t)
            pc = nxt
    return seen, edges


def fmt(seen, pc):
    v = seen.get(pc)
    if v is None:
        return f'0x{pc:06X}  .byte 0x{d[pc]:02X}'
    sz, nm, a1, a2 = v
    return f'0x{pc:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)


def dump(entry, name):
    seen, edges = walk(entry, h)
    lines = [fmt(seen, pc) for pc in sorted(seen)]
    path = os.path.join(OUT, f'boot_{name}_{entry:06X}.asm')
    open(path, 'w').write('\n'.join(lines) + '\n')
    calls = sorted({e[2] for e in edges if e[1] == 'call' and e[2] is not None})
    return seen, edges, calls, path


print('=' * 78)
print('B17 引导块代码侧')
print('=' * 78)

# ---------- 1. 向量表 ----------
print('\n[1] 向量表 @0x0000（256 项 u32 BE）')
vt = [struct.unpack_from('>I', d, i * 4)[0] for i in range(256)]
from collections import Counter
cnt = Counter(vt)
print('  目标去重后 %d 个；出现次数最多的 8 个：' % len(cnt))
for tgt, n in cnt.most_common(8):
    print(f'    0x{tgt:06X}  x{n}')
print('\n  前 32 项：')
for i in range(32):
    print(f'    vec[{i:3d}] @0x{i*4:04X} = 0x{vt[i]:06X}')
# 异常项（非 0x180 / 0x280 / 0x284 家族）
print('\n  与默认值不同的项（0x180/0x280/0x284 之外）：')
for i, v in enumerate(vt):
    if v not in (0x000180, 0x000280, 0x000284):
        print(f'    vec[{i:3d}] @0x{i*4:04X} = 0x{v:06X}')

# ---------- 2/3. 复位入口 + 缝隙函数 ----------
for entry, name in ((0x000180, 'reset'), (0x000192, 'seam')):
    seen, edges, calls, path = dump(entry, name)
    print(f'\n[{name}] 0x{entry:06X}: {len(seen)} 条指令 -> {os.path.basename(path)}')
    print('  调用的子程序：' + ', '.join(f'0x{c:06X}' for c in calls[:24]))
    # 打印前 60 条
    for pc in sorted(seen)[:60]:
        print('    ' + fmt(seen, pc))

# ---------- 4. 关键 RAM 地址引用 ----------
print('\n[4] 关键 RAM 地址在引导块中的引用')
KEYS = {
    0x0040043C: 'CDB 缓冲',
    0x00400408: 'E0/C1 请求块（V1 等）',
    0x00400402: '状态码',
    0x00400436: 'sense 索引',
    0x00400C55: 'E0 子功能码',
    0x00FFFED2: 'flash 控制字',
    0x00FFDC30: 'flash 源指针',
    0x00FFDC34: 'flash 目的指针',
}
for addr, lbl in KEYS.items():
    pat4 = struct.pack('>I', addr)
    pat2 = struct.pack('>H', addr & 0xFFFF)
    hits4 = []
    i = d.find(pat4)
    while i != -1 and len(hits4) < 12:
        hits4.append(i)
        i = d.find(pat4, i + 1)
    hits2 = []
    i = d.find(pat2)
    while i != -1 and len(hits2) < 12:
        hits2.append(i)
        i = d.find(pat2, i + 1)
    print(f'  0x{addr:08X} {lbl}')
    print(f'     4 字节立即数模式命中: {[hex(x) for x in hits4]}')
    print(f'     2 字节低 16 位模式命中: {[hex(x) for x in hits2]}')
