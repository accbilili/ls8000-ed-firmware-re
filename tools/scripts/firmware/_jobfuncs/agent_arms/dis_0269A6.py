"""展开 E0 执行层 0x0269A6 全函数，重点 0xA0 臂(0x026A92) 与 0xB3 臂(0x026B0A)。

控制流策略（沿用 dis_all.py 实锤）：
- bt(0x4000/0x5800) = BRA 无条件；bf = BRN 永不跳
- 线性流 + 条件分支目标进 worklist；jsr/bsr 记为 call 边
- H8/300H 大端，地址 = 文件偏移 + 0x10000
只读 D:\，输出到 agent_arms/。
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

ENTRY = 0x0269A6
# 已知臂落点（用于标注 arm 归属）
ARMS = {
    0x026A2E: 'ARM_0x80', 0x026A3E: 'ARM_40_41_42', 0x026A54: 'ARM_0xC1',
    0x026A92: 'ARM_0xA0', 0x026B0A: 'ARM_0xB3', 0x026BB2: 'ARM_0x91',
    0x026BBE: 'ARM_0x92', 0x026BCA: 'DEFAULT', 0x026BD2: 'ARM_81_B0_D0',
    0x026BEE: 'FINISH',
}

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
BCC = {'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs',
       'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble', 'brn'}

seen = {}      # off -> (sz, nm, a1, a2)
edges = []     # dict(from, kind, to, text)
work = [ENTRY - BASE]
rts_at = []

while work:
    pc = work.pop()
    while True:
        if pc in seen or pc < 0 or pc >= len(d):
            break
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            seen[pc] = None
            edges.append({'from': pc + BASE, 'kind': 'undec', 'to': None, 'text': f'.byte 0x{d[pc]:02X}'})
            break
        seen[pc] = (sz, nm, a1, a2)
        if nm == 'rts':
            rts_at.append(pc + BASE)
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

lines = []
cur_arm = 'HEADER'
for pc in sorted(seen):
    addr = pc + BASE
    if addr in ARMS:
        cur_arm = ARMS[addr]
    v = seen[pc]
    tag = f'[{cur_arm}]'
    if v is None:
        lines.append(f'0x{addr:06X}  .byte 0x{d[pc]:02X}      {tag}')
        continue
    sz, nm, a1, a2 = v
    raw = ' '.join(f'{d[pc+i]:02X}' for i in range(sz))
    op = ', '.join(x for x in (a1, a2) if x)
    lines.append(f'0x{addr:06X}  {raw:<18} {nm:<9} {op:<28} {tag}')

open(os.path.join(OUT, 'f_0269A6_full.asm'), 'w').write('\n'.join(lines) + '\n')

with open(os.path.join(OUT, 'edges_0269A6.txt'), 'w') as f:
    for e in sorted(edges, key=lambda x: x['from']):
        f.write(f"0x{e['from']:06X} {e['kind']:<6} -> {('0x%06X' % e['to']) if e['to'] else '-':<10} {e['text']}\n")

print(f'insns={len(seen)} edges={len(edges)} rts_at={[hex(x) for x in rts_at]}')
print('undec:', [hex(e['from']) for e in edges if e['kind'] == 'undec'])
calls = sorted({e['to'] for e in edges if e['kind'] == 'call' and e['to']})
print('call targets:', [hex(x) for x in calls])
