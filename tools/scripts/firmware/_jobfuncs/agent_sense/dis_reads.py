"""反汇编包含 0x400436 读点的函数，追踪数据流。

读点清单（来自 search_400436.py 方法1）：
 0x0116A2 fn 0x0116A0 | 0x0118C4 fn 0x011882 | 0x012070 fn 0x011F36 | 0x012A7E fn ?
 0x020EA8 fn 0x020E86 | 0x0213BE fn 0x021418 | 0x02157E fn ?
 0x022AFE fn 0x022AD6 | 0x022C00 fn 0x022BF2

对每个函数：从入口递归反汇编（跟随无条件/条件分支、不展开 jsr/bsr），
输出到 asm 文件，并标注 0x400436 相关指令与 mulxu/add.l #0x01914A 模式。
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
import sys, json, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

FNS = [0x0116A0, 0x011882, 0x011F36, 0x020E86, 0x021418, 0x022AD6, 0x022BF2]

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except: return None
    return None

UNCOND = {'jmp', 'bra', 'bt'}
NEVER = {'bf'}
CALLS = {'jsr', 'bsr'}
BCC = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}

def disasm_fn(entry, max_insns=4000):
    seen = {}
    edges = []
    work = [entry - BASE]
    while work and len(seen) < max_insns:
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
            elif nm in CALLS:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'call', 'to': t, 'text': f'{nm} {a1}'})
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
                break
            elif nm in NEVER:
                edges.append({'from': pc + BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in BCC:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges

summary = []
for fn in FNS:
    seen, edges = disasm_fn(fn)
    lines = []
    for pc in sorted(seen):
        v = seen[pc]
        if v is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            txt = f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)
            mark = ''
            if '400436' in txt: mark = '   <<< 0x400436'
            if nm == 'mulxu' or (a1 and '0x01914a' in a1.lower()) or (a2 and '0x01914a' in str(a2).lower()): mark += ' [SENSE-TBL]'
            lines.append(txt + mark)
    open(os.path.join(OUT, f'f_{fn:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
    # 统计
    n_r = sum(1 for pc in seen if seen[pc] and '400436' in ' '.join(x for x in seen[pc][2:] if x))
    summary.append(f'fn 0x{fn:06X}: {len(seen)} insns, {len(edges)} edges, {n_r} refs to 0x400436')
    print(summary[-1])
    # 打印读点前后 12 条指令上下文
    for pc in sorted(seen):
        v = seen[pc]
        if v and '400436' in ' '.join(x for x in v[2:] if x):
            lo = max(0, pc - BASE - 24)
            print(f'  --- ctx around 0x{pc+BASE:06X} ---')
            for q in sorted(seen):
                if lo <= q <= pc + 24:
                    vv = seen[q]
                    if vv is None:
                        print(f'    0x{q+BASE:06X}  .byte 0x{d[q]:02X}')
                    else:
                        print(f'    0x{q+BASE:06X}  {vv[1]:<9} ' + ', '.join(x for x in vv[2:] if x))

json.dump({f'{fn:06X}': e for fn, (s, e) in zip(FNS, [disasm_fn(f) for f in FNS])},
          open(os.path.join(OUT, 'edges_read_fns.json'), 'w'), indent=1)
