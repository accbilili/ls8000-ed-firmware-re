"""反汇编 E0 0x81 作业函数 0x028648 的三个被调函数（+一层被调）。

- 目标：0x02BAA6 / 0x02CC04 / 0x02B038
- 控制流：线性 + 条件/无条件分支目标进 worklist；jsr/bsr 目标若在 ROM 内且非共享助手，
  作为 level-1 函数展开（再往里只记边）。
- 共享助手不展开：0x010B56(设备就绪等待) 0x018E1E(32位乘) 0x01872E(32位除) 0x01876A(双精度转整)
- 陷阱：bt = BRA（无条件），bf = BRN（永不跳）。H8/300H 大端。
只读 D:\，输出到 agent_81/。
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

TARGETS = [0x02BAA6, 0x02CC04, 0x02B038]
SHARED = {0x010B56, 0x018E1E, 0x01872E, 0x01876A}

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

UNCOND = {'jmp', 'bra', 'bt'}
NEVER = {'bf'}
CALLS = {'jsr', 'bsr'}
COND = {'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs',
        'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble', 'brn'}

def disasm_fn(entry, follow_calls, stop_at=None):
    seen = {}
    edges = []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            if stop_at and (pc + BASE) in stop_at:
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
                if follow_calls and t is not None and 0 <= t - BASE < len(d) and t not in SHARED:
                    work.append(t - BASE)
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
                break
            elif nm in NEVER:
                edges.append({'from': pc + BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in COND:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges

def dump(seen, path):
    lines = []
    for pc in sorted(seen):
        v = seen[pc]
        if v is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    open(os.path.join(OUT, path), 'w').write('\n'.join(lines) + '\n')

all_edges = {}
# 第一遍：三个目标，跟一层被调
for fn in TARGETS:
    seen, edges = disasm_fn(fn, follow_calls=True)
    dump(seen, f'f_{fn:06X}.asm')
    all_edges[f'{fn:06X}'] = edges
    print(f'0x{fn:06X}: {len(seen)} insns, {len(edges)} edges')

json.dump(all_edges, open(os.path.join(OUT, 'edges_l1.json'), 'w'), indent=1)
