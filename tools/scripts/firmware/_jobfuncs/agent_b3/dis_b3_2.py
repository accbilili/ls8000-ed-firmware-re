"""第二轮：展开 B3 相关的平行实现区与 RAM 例程源。

1. 0x12100-0x12800（FFDC30/34、FFFED2、400CA0、400D38 密集引用簇）——同构「命令块发送」实现
2. 0x27200-0x27420（另一簇）
3. 0x17AB4-0x17F04（0x017A80 拷贝到 RAM 0x400F5A 的例程源）
4. 0x010B56（设备就绪等待）
5. 补搜立即数：0x400F5A / 0x40121C / 0x006000 / 0x006010 / 0xFFFF48 / 0x4202A4 /
   0x440E50 / 0x4202E0 / 0x400402 / 0x00600D / 0x03F0F9 / 0x400400
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
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except ValueError: return None
    return None

UNCOND = {'jmp', 'bra', 'bt'}; NEVER = {'bf'}; CALLS = {'jsr', 'bsr'}
BCC = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}

def disasm_range(start, end):
    """线性反汇编 [start,end)，遇到 rts 继续（不停止），输出全部指令。"""
    lines = []
    pc = start - BASE
    while pc < end - BASE:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        raw = d[pc:pc+sz].hex(' ')
        lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1,a2) if x) + f'   ; {raw}')
        pc += sz
    return lines

def disasm_fn(entry, max_insns=4000):
    seen = {}; edges = []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        steps = 0
        while True:
            if pc in seen or pc < 0 or pc >= len(d): break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None; break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts': break
            elif nm in CALLS:
                edges.append({'from': pc+BASE, 'kind':'call', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append({'from': pc+BASE, 'kind':'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t-BASE < len(d): work.append(t-BASE)
                break
            elif nm in NEVER:
                edges.append({'from': pc+BASE, 'kind':'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in BCC:
                t = parse_tgt(a1)
                edges.append({'from': pc+BASE, 'kind':'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t-BASE < len(d): work.append(t-BASE)
            pc = nxt
            steps += 1
            if steps > max_insns: break
    return seen, edges

# 1-3: 线性区段
for name, start, end in [('region_121xx', 0x12100, 0x12800),
                         ('region_272xx', 0x27200, 0x27420),
                         ('ram_src_17AB4', 0x17AB4, 0x17F04)]:
    lines = disasm_range(start, end)
    open(os.path.join(OUT, f'{name}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(f'{name}: {len(lines)} 行')

# 4: 0x010B56 函数式
for fn in (0x010B56,):
    seen, edges = disasm_fn(fn)
    lines = []
    for pc in sorted(seen):
        v = seen[pc]
        if v is None: lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1,a2) if x) + f'   ; {d[pc:pc+sz].hex(" ")}')
    open(os.path.join(OUT, f'f_{fn:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(f'0x{fn:06X}: {len(seen)} insns')

# 5: 补搜立即数
IMMS = [0x00400F5A, 0x0040121C, 0x00006000, 0x00006010, 0x00FFFF48,
        0x004202A4, 0x00440E50, 0x004202E0, 0x00400402, 0x0000600D,
        0x0003F0F9, 0x00400400, 0x00400406, 0x0040040E]
res = {}
for v in IMMS:
    pat = v.to_bytes(4, 'big')
    hits = []; start = 0
    while True:
        i = d.find(pat, start)
        if i < 0: break
        hits.append(i + BASE); start = i + 1
    res[f'{v:08X}'] = hits
    print(f'imm 0x{v:08X}: {len(hits)} 处: {[hex(x) for x in hits]}')
json.dump(res, open(os.path.join(OUT, 'imm_refs2.json'), 'w'), indent=1)
