"""反汇编机构移动原语簇（agent-motor）。

目标（地址 = 文件偏移 + 0x10000，H8/300H 大端）：
  0x02B87C 绝对移动        0x02B8EA, 0x02B82A  其循环体两步
  0x02B276 相对移动(0x41)
  0x02B196, 0x02B1E4, 0x02B22E  0x40 电机三步
  0x02C9E4, 0x02C8B4  0x42 轮询体两步

控制流：线性流 + 分支目标进 worklist；jsr/bsr 记边不展开；jmp 跟随。
陷阱：h8.lst 的 bt(0x4000/0x5800 全掩码) = BRA 无条件；bf = BRN 永不跳。
只读 D:\，输出到本目录。
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
import sys, os, json
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

TARGETS = [0x02B87C, 0x02B8EA, 0x02B82A, 0x02B276,
           0x02B196, 0x02B1E4, 0x02B22E, 0x02C9E4, 0x02C8B4]
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

UNCOND = {'jmp', 'bra', 'bt'}   # bt = BRA 实锤
NEVER = {'bf'}                   # = BRN
CALLS = {'jsr', 'bsr'}
BCC = {'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs',
       'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble', 'brn'}

def disasm_fn(entry):
    seen, edges = {}, []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            if (pc + BASE) in STOPS and (pc + BASE) != entry:
                break  # 撞到另一目标入口，停
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
            elif nm in BCC:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges

report = {}
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
    report[f'{fn:06X}'] = {'n_insns': len(seen), 'edges': edges}
    print(f'0x{fn:06X}: {len(seen)} insns, {len(edges)} edges')
json.dump(report, open(os.path.join(OUT, 'motor_edges.json'), 'w'), indent=1)
