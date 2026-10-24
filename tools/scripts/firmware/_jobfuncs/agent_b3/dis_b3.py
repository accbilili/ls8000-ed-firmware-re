"""反汇编 B3(0x02BBAE) 的被调函数链 + 全镜像立即数常量搜索。

目标函数（8 个）：
  0x017A80  初始化第 1 步
  0x016E8E  初始化第 2 步
  0x010BD2  疑似 DMA/传输原语 A
  0x010BD8  疑似 DMA/传输原语 B
  0x017A78 / 0x017A7C  外围两步
  0x02BCCE  0x02BBAE 尾部 bsr
  0x026B0A  执行层 0xB3 臂（经 0x026B46 写 0x400408）

立即数搜索（仅 4 字节大端常量，安全的）：
  0xFFDC30 / 0xFFDC34 / 0xFFFED2 / 0x400CA0 / 0x400408 / 0x400D38
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
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries  # 修复版

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
print(f'镜像长度 {len(d)} (0x{len(d):X})，覆盖地址 0x{BASE:X}..0x{BASE+len(d):X}')

TARGETS = [0x017A80, 0x016E8E, 0x010BD2, 0x010BD8, 0x017A78, 0x017A7C,
           0x02BCCE, 0x026B0A]

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

UNCOND = {'jmp', 'bra', 'bt'}     # bt = BRA（实锤）
NEVER = {'bf'}                    # = BRN
CALLS = {'jsr', 'bsr'}
BCC = {'bhi', 'bls', 'bcc', 'bcs', 'bne', 'beq', 'bvc', 'bvs',
       'bpl', 'bmi', 'bge', 'blt', 'bgt', 'ble', 'brn'}

def disasm_fn(entry, max_insns=4000):
    seen = {}
    edges = []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        steps = 0
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
            steps += 1
            if steps > max_insns:
                break
    return seen, edges

report = {}
all_edges = {}
for fn in TARGETS:
    seen, edges = disasm_fn(fn)
    all_edges[f'{fn:06X}'] = edges
    lines = []
    for pc in sorted(seen):
        v = seen[pc]
        if v is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        else:
            sz, nm, a1, a2 = v
            raw = d[pc:pc+sz].hex(' ')
            lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x) + f'   ; {raw}')
    open(os.path.join(OUT, f'f_{fn:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
    report[f'{fn:06X}'] = {'insns': len(seen), 'edges': len(edges)}
    print(f'0x{fn:06X}: {len(seen)} insns, {len(edges)} edges')

json.dump(all_edges, open(os.path.join(OUT, 'edges_b3.json'), 'w'), indent=1)

# ---- 立即数常量全镜像搜索（仅 4 字节大端立即数） ----
IMMS = {
    0xFFDC30: 'FFDC30 寄存器（← 0x400CA0 块地址）',
    0xFFDC34: 'FFDC34 寄存器（← 0x6000）',
    0xFFFED2: 'FFFED2 寄存器（&0xFFFC|3）',
    0x400CA0: '参数块基址',
    0x400408: '请求块（B3 源）',
    0x400D38: '0x21 字节（疑似命令字/类型码）',
}
imm_results = {}
for v, desc in IMMS.items():
    pat = v.to_bytes(4, 'big')
    hits = []
    start = 0
    while True:
        i = d.find(pat, start)
        if i < 0:
            break
        hits.append(i + BASE)
        start = i + 1
    imm_results[f'{v:08X}'] = {'desc': desc, 'hits': hits}
    print(f'imm 0x{v:08X} ({desc}): {len(hits)} 处: {[hex(x) for x in hits]}')

json.dump(imm_results, open(os.path.join(OUT, 'imm_refs.json'), 'w'), indent=1)
