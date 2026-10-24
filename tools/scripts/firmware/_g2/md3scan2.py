# -*- coding: utf-8 -*-
"""G2 反例检查 v2：md3 中 85 个 host_code 常量的可靠检索。
三种方法并行，互相印证：
 A. 滑动窗口立即数验证 —— 在 .text 里找 LE(V) 的每处出现，回溯 ≤8 字节找一个能
    解码出「立即数 == V」且覆盖该位置的指令起点。x86 立即数长度确定，此法可靠。
 B. 线性反汇编 .text（起始于每个函数入口）抽立即数。
 C. .rdata/.data 中的 16 位 LE 出现 + 「连续 u16 序列」检测（真表才有的特征）。
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import json, struct, collections, bisect
import pefile, capstone

M3 = sample('driver/LS8000.md3')
FUNCS = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\funcs.txt'
CAPS = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\dispatch_caps.json'

D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
hostcodes = []
for i in range(200):
    off = 0x03E390 - BASE + i * 4
    hc = struct.unpack('>H', D[off:off + 2])[0]
    if hc == 0:
        break
    hostcodes.append(hc)
HCSET = set(hostcodes)
print(f'host_code 共 {len(hostcodes)} 条')

caps = json.load(open(CAPS))['caps']
capmap = {c['cap_id']: c for c in caps}
hit_caps = [h for h in hostcodes if h in capmap]

pe = pefile.PE(M3)
IB = pe.OPTIONAL_HEADER.ImageBase
raw = open(M3, 'rb').read()
secs = {s.Name.rstrip(b'\x00').decode(): s for s in pe.sections}
text = secs['.text']
tva, tsz = IB + text.VirtualAddress, text.SizeOfRawData
toff = text.PointerToRawData

funcs = []
for line in open(FUNCS, encoding='utf-8', errors='replace'):
    p = line.split()
    if p and p[0].startswith('0x'):
        funcs.append((int(p[0], 16), p[4] if len(p) > 4 else ''))
funcs.sort()
faddrs = [f[0] for f in funcs]
fnames = {f[0]: (f[1] or f'0x{f[0]:08X}') for f in funcs}


def fname_of(va):
    i = bisect.bisect_right(faddrs, va) - 1
    return fnames.get(faddrs[i], f'0x{va:08X}') if i >= 0 else f'0x{va:08X}'


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

# ---------- A. 滑动窗口验证 ----------
imm_hits = collections.defaultdict(list)   # V -> [(va, mnemonic, func)]
for V in hostcodes:
    pat = struct.pack('<H', V)
    start = 0
    while True:
        i = raw.find(pat, toff, toff + tsz)
        if i < 0:
            break
        start = i + 1
        break
    # 逐处查找
    pos = toff
    while True:
        i = raw.find(pat, pos, toff + tsz)
        if i < 0:
            break
        pos = i + 1
        va_target = tva + (i - toff)
        found = None
        for back in range(0, 9):                 # 指令起点候选
            s = i - back
            if s < toff:
                break
            sva = tva + (s - toff)
            try:
                for ins in md.disasm(raw[s:s + 16], sva):
                    if ins.address <= va_target < ins.address + ins.size:
                        for op in ins.operands:
                            if op.type == capstone.x86.X86_OP_IMM and op.imm == V:
                                found = (ins.address, ins.mnemonic + ' ' + ins.op_str)
                                break
                    if ins.address > va_target:
                        break
            except Exception:
                pass
            if found:
                break
        if found:
            imm_hits[V].append((found[0], found[1], fname_of(found[0])))

print(f'[A] 滑动窗口立即数验证：{len(imm_hits)} / {len(hostcodes)} 个 host_code 在 md3 有立即数出现')

# ---------- B. 函数入口线性反汇编 ----------
lin_hits = collections.defaultdict(list)
for fa, _ in funcs:
    o = None
    for s in pe.sections:
        if s.VirtualAddress <= fa - IB < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            o = s.PointerToRawData + (fa - IB - s.VirtualAddress)
            break
    if o is None:
        continue
    for ins in md.disasm(raw[o:o + 4000], fa):
        if ins.mnemonic == 'ret' and len(lin_hits) > 0 and ins.address > fa + 400:
            break
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_IMM and op.imm in HCSET:
                lin_hits[op.imm].append((ins.address, ins.mnemonic + ' ' + ins.op_str, fname_of(ins.address)))
        if ins.address > fa + 4000:
            break
print(f'[B] 函数入口线性反汇编：{len(lin_hits)} / {len(hostcodes)} 个')

allimm = collections.defaultdict(list)
for d in (imm_hits, lin_hits):
    for k, v in d.items():
        seen = {x[0] for x in allimm[k]}
        for x in v:
            if x[0] not in seen:
                allimm[k].append(x)
                seen.add(x[0])
print(f'[A+B 合并] {len(allimm)} / {len(hostcodes)} 个 host_code 在 md3 .text 中作为立即数出现')

# ---------- C. 数据节 16 位 LE + 连续序列 ----------
data_hits = collections.defaultdict(list)
for sname in ('.rdata', '.data'):
    s = secs[sname]
    buf = raw[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
    sva = IB + s.VirtualAddress
    for hc in hostcodes:
        pat = struct.pack('<H', hc)
        p = 0
        while True:
            i = buf.find(pat, p)
            if i < 0:
                break
            data_hits[hc].append((sva + i, sname))
            p = i + 1

# 连续 u16 序列检测：host_code 里连续的值（如 0830..0834）是否相邻出现在同一处
runs = []
for k in range(len(hostcodes)):
    j = k
    while j + 1 < len(hostcodes) and hostcodes[j + 1] == hostcodes[j] + 1:
        j += 1
    if j - k >= 2:
        runs.append(hostcodes[k:j + 1])
print(f'[C] host_code 中的连续段（长度≥3）共 {len(runs)} 段: '
      + ', '.join(f'{r[0]:04X}..{r[-1]:04X}({len(r)})' for r in runs))

run_hits = []
for r in runs:
    for sname in ('.rdata', '.data'):
        s = secs[sname]
        buf = raw[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
        sva = IB + s.VirtualAddress
        pat = b''.join(struct.pack('<H', v) for v in r)
        p = 0
        while True:
            i = buf.find(pat, p)
            if i < 0:
                break
            run_hits.append((sva + i, sname, r[0], len(r)))
            p = i + 1
print(f'[C] 连续 u16 序列在数据节完整命中：{len(run_hits)} 处')

json.dump({'hostcodes': hostcodes, 'caps_hit': hit_caps,
           'imm': {str(k): v for k, v in allimm.items()},
           'data_counts': {str(k): len(v) for k, v in data_hits.items()},
           'run_hits': run_hits}, open('md3_hits.json', 'w'), indent=1)

print('\n===== 逐条明细（imm = 立即数出现次数, data = 数据节 16 位 LE 出现次数）=====')
for hc in hostcodes:
    im = allimm.get(hc, [])
    dh = len(data_hits.get(hc, []))
    c = capmap.get(hc)
    cs = f"cap {c['group']}/{c['sub']}" if c else ''
    tail = ''
    if im:
        tail = '  ' + '; '.join(f'0x{a:08X} {m} [{f}]' for a, m, f in im[:3])
    print(f'0x{hc:04X}  imm={len(im):<2} data={dh:<4} {cs}{tail}')
