"""通用递归反汇编器（agent_15354）——基于 dis_all.py 控制流策略。

用法: python dis_fn.py <entry_hex> [more entries...] [--depth N]
输出: <entry>.asm 到本目录，含调用边注释。
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

entries = [int(x, 16) for x in sys.argv[1:] if not x.startswith('-')]

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
CONDS = ('bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs', 'bpl', 'bmi',
         'bge', 'blt', 'bgt', 'ble', 'brn')

def disasm_fn(entry, max_insns=4000):
    seen = {}
    edges = []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d) or len(seen) >= max_insns:
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
            elif nm in CONDS:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges

for entry in entries:
    seen, edges = disasm_fn(entry)
    lines = []
    lines.append(f'; ==== function 0x{entry:06X} ({len(seen)} insns) ====')
    lines.append(f'; call/jmp edges:')
    for e in sorted(edges, key=lambda x: x['from']):
        lines.append(f";   0x{e['from']:06X} {e['kind']:5s} -> {'0x%06X' % e['to'] if e['to'] is not None else '?':>8s}  {e['text']}")
    for pc in sorted(seen):
        v = seen[pc]
        a = pc + BASE
        if v is None:
            lines.append(f'0x{a:06X}:  .byte <undecodable>')
            continue
        sz, nm, a1, a2 = v
        raw = ' '.join(f'{d[pc+i]:02X}' for i in range(sz))
        ops = []
        if a1 is not None:
            ops.append(a1)
        if a2 is not None:
            ops.append(a2)
        lines.append(f'0x{a:06X}:  {nm:8s} {", ".join(ops):40s} ; [{raw}]')
    fn = os.path.join(OUT, f'f_{entry:06X}.asm')
    open(fn, 'w').write('\n'.join(lines) + '\n')
    print(f'wrote {fn}  ({len(seen)} insns)')
