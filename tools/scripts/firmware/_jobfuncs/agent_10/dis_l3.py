"""第三层：0x0390f2/0x0391c0（变体前置）、0x016022（记录字段读取器）、0x01605a、
0x02ED5A 的四个广播目标 0x02f496/0x02ed8a/0x03a18c/0x02ee6e。
只读 D:\，输出到 agent_10/。
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
import sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

TARGETS = [0x0390F2, 0x0391C0, 0x016022, 0x01605A,
           0x02F496, 0x02ED8A, 0x03A18C, 0x02EE6E]
STOPS = set(TARGETS)

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
                break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None
                break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts':
                break
            elif nm in CALLS:
                edges.append({'from': pc + BASE, 'kind': 'call', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
                break
            elif nm in NEVER:
                edges.append({'from': pc + BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in ('bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs',
                        'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble', 'brn'):
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges

for fn in TARGETS:
    seen, edges = disasm_fn(fn)
    lines = []
    for pc in sorted(seen):
        v = seen[pc]
        if v is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    open(os.path.join(OUT, f'f_{fn:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
    callees = sorted({e['to'] for e in edges if e['kind'] == 'call' and e['to'] is not None})
    print(f'0x{fn:06X}: {len(seen)} insns, callees={[hex(c) for c in callees]}')
