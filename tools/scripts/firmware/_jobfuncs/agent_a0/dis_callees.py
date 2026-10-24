"""反汇编 agent_a0 的关键被调函数（修复版解码器，只读 D:\）。
线性流 + 分支目标进 worklist；jsr/bsr/jmp 记为边但不展开。
bt(4000/5800)=BRA 无条件；bf=BRN 永不跳。H8/300H 大端。
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
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

TARGETS = {
    0x03A994: 'selfcheck?',
    0x033422: 'callee_success1',
    0x034782: 'callee_success2',
    0x03D474: 'callee_success3',
    0x02D1DC: 'callee_success4',
    0x03B58E: 'paramcalc',
    0x03C194: 'callee_pos',
    0x03ADF6: 'callee_move?',
    0x026A92: 'exec_arm_A0',
    # 附加小助手（只为确认调用约定/常量）
    0x018EDE: 'helper_dbl?',
    0x0188D2: 'helper_dblcmp?',
    0x018E9E: 'helper_div32b',
    0x0185EE: 'helper_x',
    0x018860: 'helper_y',
    0x03B546: 'callee_move2?',
    0x03BD4A: 'callee_x2',
}

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except ValueError: return None
    return None

UNCOND = {'jmp', 'bra', 'bt'}
NEVER = {'bf'}
CALLS = {'jsr', 'bsr'}
BCC = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}

def disasm_fn(entry, maxins=1200):
    seen = {}; edges = []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        n = 0
        while True:
            if pc in seen or pc < 0 or pc >= len(d): break
            if n > maxins: break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None; break
            n += 1
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts':
                break
            elif nm in CALLS:
                t = parse_tgt(a1)
                edges.append({'from': pc+BASE, 'kind': 'call', 'to': t, 'text': f'{nm} {a1}'})
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append({'from': pc+BASE, 'kind': 'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d): work.append(t - BASE)
                break
            elif nm in NEVER:
                edges.append({'from': pc+BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in BCC:
                t = parse_tgt(a1)
                edges.append({'from': pc+BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d): work.append(t - BASE)
            pc = nxt
    return seen, edges

all_edges = {}
for fn, tag in TARGETS.items():
    seen, edges = disasm_fn(fn)
    all_edges[f'{fn:06X}'] = {'tag': tag, 'edges': edges}
    lines = [f'# fn 0x{fn:06X} ({tag}) : {len(seen)} insns']
    for pc in sorted(seen):
        v = seen[pc]
        if v is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    open(os.path.join(OUT, f'f_{fn:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(f'0x{fn:06X} ({tag}): {len(seen)} insns, {len(edges)} edges')

json.dump(all_edges, open(os.path.join(OUT, 'agent_a0_edges.json'), 'w'), indent=1)
print('done')
