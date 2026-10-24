"""B17 续②：多入口并集走查（线性扫描取候选入口，再递归并集）。
目标：给出引导块真实代码分布、函数入口表、全部地址引用。
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
ALL_BRANCH = UNCOND | NEVER | CONDS | CALLS


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


def walk(entry, seen, edges):
    work = [entry]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            sz, nm, a1, a2 = h.decode(pc)
            if nm is None:
                seen[pc] = None
                break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts':
                edges.setdefault('ret', []).append(pc)
                break
            if nm in CALLS:
                t = parse_tgt(a1)
                edges.setdefault('call', []).append((pc, t))
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.setdefault('jmp', []).append((pc, t))
                if t is not None and 0 <= t < len(d):
                    work.append(t)
                break
            elif nm in NEVER:
                edges.setdefault('never', []).append((pc, parse_tgt(a1)))
            elif nm in CONDS:
                t = parse_tgt(a1)
                edges.setdefault('bcc', []).append((pc, t))
                if t is not None and 0 <= t < len(d):
                    work.append(t)
            pc = nxt


def fmt(seen, pc):
    v = seen.get(pc)
    if v is None:
        return f'0x{pc:06X}  .byte 0x{d[pc]:02X}'
    sz, nm, a1, a2 = v
    return f'0x{pc:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)


# --- 线性扫描：收集候选入口 ---
cand = set()
rts_pos = []
call_tgts = set()
jmp_tgts = set()
for off in range(0, len(d) - 1, 2):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None:
        continue
    if nm == 'rts':
        rts_pos.append(off)
    if nm in CALLS:
        t = parse_tgt(a1)
        if t is not None and 0 < t < len(d):
            call_tgts.add(t)
    if nm in UNCOND:
        t = parse_tgt(a1)
        if t is not None and 0 < t < len(d):
            jmp_tgts.add(t)
print(f'[扫描] 线性解码 64 KB：rts {len(rts_pos)} 处，call 目标 {len(call_tgts)} 个，jmp 目标 {len(jmp_tgts)} 个')

seeds = {0x180, 0x192, 0x280, 0x284} | call_tgts | jmp_tgts
seen = {}
edges = {}
for s in sorted(seeds):
    if s in seen:
        continue
    walk(s, seen, edges)
ins = sorted(a for a in seen if seen[a] is not None)
print(f'[走查] 种子 {len(seeds)} 个 → 可达指令 {len(ins)} 条，覆盖 {ins[-1]-ins[0]+1} B')

# 按 0x1000 区间统计代码分布
buckets = defaultdict(int)
for a in ins:
    buckets[a >> 12] += 1
print('\n[分布] 每 4 KB 区间的指令数：')
for k in sorted(buckets):
    print(f'   0x{k*0x1000:05X}-0x{(k+1)*0x1000-1:05X} : {buckets[k]:5d} 条')

open(os.path.join(OUT, 'boot_reachable.asm'), 'w').write('\n'.join(fmt(seen, a) for a in ins) + '\n')

# 函数入口（被 call 的目标 + jmp 的目标 + rts 前一条）
entries = sorted(call_tgts | {pc for pc, t in edges.get('jmp', []) if t is not None and 0 < t < len(d)})
print(f'\n[入口] {len(entries)} 个候选函数入口：')
for e in entries:
    print(f'   0x{e:06X}')

# 地址引用
print('\n[地址引用] 全块内出现的绝对地址：')
refs = defaultdict(list)
for a in ins:
    sz, nm, a1, a2 = seen[a]
    for op in (a1, a2):
        if not op:
            continue
        m = re.fullmatch(r'@?(0x[0-9a-f]{6})', op)
        if m:
            refs[int(m.group(1), 16)].append(a)
for v in sorted(refs):
    print(f'   0x{v:08X}  x{len(refs[v]):<3} ' + ', '.join(f'0x{x:06X}' for x in refs[v][:8]))
