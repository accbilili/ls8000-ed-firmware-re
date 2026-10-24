"""B17 续：引导块全量清点。
 1. 从复位入口 0x180 递归走完整块，统计可达代码量、函数入口（按序言识别）
 2. 全部 0xFFDCxx / 0xFFDxxx 寄存器引用 + 0x4xxxxx RAM 引用（带指令上下文）
 3. 检查 ldc/stc VBR、以及对 0x0000-0x017F 向量表的读取
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
import sys, os, re
from collections import defaultdict
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h8dis import H8
from h8fix import load_entries_fixed

d = open(sample('LS8000_bootblock.bin'), 'rb').read()
h = H8(d, load_entries_fixed(sample('h8.lst')), base=0)
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


def walk(entry):
    seen = {}
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
                pass
            elif nm in UNCOND:
                t = parse_tgt(a1)
                if t is not None and 0 <= t < len(d):
                    work.append(t)
                break
            elif nm in NEVER:
                pass
            elif nm in CONDS:
                t = parse_tgt(a1)
                if t is not None and 0 <= t < len(d):
                    work.append(t)
            pc = nxt
    return seen


def fmt(seen, pc):
    v = seen.get(pc)
    if v is None:
        return f'0x{pc:06X}  .byte 0x{d[pc]:02X}'
    sz, nm, a1, a2 = v
    return f'0x{pc:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)


seen = walk(0x180)
addrs = sorted(a for a in seen if seen[a] is not None)
print('=' * 78)
print(f'引导块可达代码：{len(addrs)} 条指令，地址区间 0x{addrs[0]:06X}–0x{addrs[-1]:06X}')
print(f'字节覆盖：{addrs[-1]-addrs[0]+1} B / 65536 B')
open(os.path.join(OUT, 'boot_reachable.asm'), 'w').write(
    '\n'.join(fmt(seen, a) for a in addrs) + '\n')

# 函数入口：被 jsr/bsr 调用、或被 jmp 进入的地址
targets = defaultdict(list)
for a in addrs:
    sz, nm, a1, a2 = seen[a]
    if nm in CALLS:
        t = parse_tgt(a1)
        if t is not None:
            targets[t].append(('call', a))
    elif nm in UNCOND:
        t = parse_tgt(a1)
        if t is not None:
            targets[t].append(('jmp', a))
print(f'\n被调用/跳转的入口 {len(targets)} 个：')
for t in sorted(targets):
    kinds = defaultdict(int)
    for k, _ in targets[t]:
        kinds[k] += 1
    print(f'   0x{t:06X}   {dict(kinds)}')

# 地址引用统计
print('\n--- 全块内的绝对地址引用（mov.l #imm / abs 寻址）---')
refs = defaultdict(list)
for a in addrs:
    sz, nm, a1, a2 = seen[a]
    for op in (a1, a2):
        if not op:
            continue
        m = re.fullmatch(r'@?(0x[0-9a-f]{6})', op)
        if m:
            v = int(m.group(1), 16)
            refs[v].append(a)
        m2 = re.fullmatch(r'@(0x[0-9a-f]{4})', op)
        if m2:
            v = int(m2.group(1), 16)
            refs[v].append(a)
for v in sorted(refs):
    if v >= 0xFF0000 or 0x400000 <= v < 0x450000 or v < 0x1000:
        print(f'   0x{v:08X}  x{len(refs[v]):<3} 例: ' + ', '.join(f'0x{x:06X}' for x in refs[v][:6]))

# ldc/stc 与 VBR
print('\n--- ldc / stc 指令 ---')
for a in addrs:
    sz, nm, a1, a2 = seen[a]
    if nm in ('ldc', 'stc'):
        print(f'   {fmt(seen, a)}')
