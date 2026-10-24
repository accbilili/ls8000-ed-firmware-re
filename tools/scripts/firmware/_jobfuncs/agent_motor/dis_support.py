"""反汇编支撑被调者 + 关键指令原始字节验证。

支撑函数：
  0x02BE32  0x42 轴移动驱动（0x02C9E4 调）
  0x02B442, 0x02B2D4  0x02B276 调的设置/启动
  0x01872E  32 位除   0x018E1E  32 位乘   0x010B56  设备就绪等待
  0x029D2A  0x02C8B4 等完后调   0x02B11A  0x40 错误路径调
另：打印关键指令原始字节以核验操作数。
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
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

SUPPORT = [0x02BE32, 0x02B442, 0x02B2D4, 0x01872E, 0x018E1E, 0x010B56, 0x029D2A, 0x02B11A]
STOPS = set(SUPPORT)

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except ValueError: return None
    return None

UNCOND = {'jmp', 'bra', 'bt'}; NEVER = {'bf'}; CALLS = {'jsr', 'bsr'}
BCC = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}

def disasm_fn(entry):
    seen, edges = {}, []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d): break
            if (pc + BASE) in STOPS and (pc + BASE) != entry: break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None; break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts': break
            elif nm in CALLS: edges.append({'from': pc+BASE, 'kind': 'call', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in UNCOND:
                t = parse_tgt(a1); edges.append({'from': pc+BASE, 'kind': 'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d): work.append(t - BASE)
                break
            elif nm in NEVER: edges.append({'from': pc+BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in BCC:
                t = parse_tgt(a1); edges.append({'from': pc+BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d): work.append(t - BASE)
            pc = nxt
    return seen, edges

for fn in SUPPORT:
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
    print(f'0x{fn:06X}: {len(seen)} insns, edges: ' + '; '.join(e["text"] for e in edges))

print()
print('=== 关键指令原始字节核验 ===')
for addr, note in [
    (0x02B8BC, '0x02B87C 内 mov.b r0l,r0l?'),
    (0x02BA16, '0x02B98A 内 mov.b r0l,r0l?'),
    (0x02B9FA, '0x02B98A push 参数字'),
    (0x02B948, '0x02b8ea push 参数字'),
    (0x02B1C4, '0x02B196 sub.l er0,er0?'),
    (0x02B1C8, '0x02B196 add.l er0,er4?'),
    (0x02B1CA, '0x02B196 sub.l er1,er1?'),
    (0x02CB80, '0x02CB66 sub.b r0l,r0l?'),
    (0x02B82C, '0x02B82A 读 0x4202e8'),
    (0x02C8B6, '0x02C8B4 读 0x4202f3'),
    (0x02B29C, '0x02B276 mov.b r0h,@0x4202e8'),
]:
    sz, nm, a1, a2, nxt = h.decode(addr - BASE)
    raw = ' '.join(f'{b:02X}' for b in d[addr-BASE:addr-BASE+sz])
    print(f'0x{addr:06X} [{raw:<14}] {nm} {a1}' + (f', {a2}' if a2 else '') + f'   ; {note}')
