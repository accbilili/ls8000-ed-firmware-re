"""递归反汇编 0x03EDE8 作业表的 11 个处理函数。
控制流策略：
- 线性流 + 条件/无条件分支目标进 worklist；jsr/bsr/jmp-indirect 记为边但不展开（callee 是共享助手）。
- 陷阱实锤：h8.lst 的 4000 ff00 "bt rel8" / 5800 ffff "bt rel16" 是全掩码单指令 = BRA（无条件）；
  4100/5810 "bf" = BRN（永不跳）。按此跟随，不按 T 置位判。
- H8/300H 大端。
只读 D:\，输出到 _jobfuncs/。
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
sys.path.insert(0, OUT)
from h8dis import H8
from h8fix import load_entries_fixed as load_entries  # 修复版：原版正则丢 12 位十六进制行

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

# 作业表 0x03EDE8 的 12 个条目，key → 处理函数。
# 实测校核：表项字节形如 [u8 key][u8 0][u32 BE 处理函数]，
#   key=0x40 的条目字节为 `40 00 00 02 AE AA` → 处理函数 = 0x02AEAA。
# R5 更正：0x40 项原记 0x02AAAE，末两字节错位（AE AA → AA AE）。
#   此处保留修正值，使重跑产出的 edges.json 与 ROM 实测一致。
TARGETS = [
    (0x10, 0x35598), (0x40, 0x2AEAA), (0x41, 0x2B98A), (0x42, 0x2CB66),
    (0x81, 0x28648), (0xA0, 0x3A3D4), (0xB0, 0x27F24), (0xC1, 0x2BA24),
    (0xD0, 0x2866E), (0x80, 0x28722), (0xB3, 0x2BBAE), (0x00, 0x28722),
]
STOPS = {t for _, t in TARGETS}

def parse_tgt(s):
    if s is None:
        return None
    s = s.strip()
    if s.startswith('0x'):
        try:
            return int(s, 16)
        except ValueError:
            return None
    return None  # 寄存器间接等

UNCOND = {'jmp', 'bra', 'bt'}          # bt = BRA（实锤）
NEVER = {'bf'}                          # = BRN
CALLS = {'jsr', 'bsr'}

def disasm_fn(entry):
    seen = {}
    edges = []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            if (pc + BASE) in STOPS and (pc + BASE) != entry:
                break  # 撞到另一个作业函数入口，停
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
                break  # 无条件，不线性下落
            elif nm in NEVER:
                edges.append({'from': pc + BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in ('bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs', 'bpl', 'bmi',
                        'bge', 'blt', 'bgt', 'ble', 'brn'):
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges

report = []
all_edges = {}
for key, fn in TARGETS:
    seen, edges = disasm_fn(fn)
    all_edges[f'{key:02X}->{fn:06X}'] = edges
    lines = []
    for pc in sorted(seen):
        v = seen[pc]
        if v is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    open(os.path.join(OUT, f'f_{fn:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
    report.append(f'key 0x{key:02X} fn 0x{fn:06X}: {len(seen)} insns, {len(edges)} edges')

json.dump(all_edges, open(os.path.join(OUT, 'edges.json'), 'w'), indent=1)
print('\n'.join(report))
