# -*- coding: utf-8 -*-
"""G2 反例检查：在 md3 (x86 PE32) 中搜 85 个 host_code 常量。
方法：capstone 线性反汇编每个已识别函数，抽取立即数；另对 .rdata/.data 做 16 位 LE 字节匹配。
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
import json, struct, sys, collections
import pefile, capstone

M3 = sample('driver/LS8000.md3')
FUNCS = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\funcs.txt'
CAPS = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\dispatch_caps.json'

# ---- 1. 取 85 个 host_code ----
D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
hostcodes = []
for i in range(200):
    off = 0x03E390 - BASE + i * 4
    hc = struct.unpack('>H', D[off:off + 2])[0]
    if hc == 0:
        break
    hostcodes.append(hc)
print(f'[1] 0x03E390 host_code 共 {len(hostcodes)} 条')

# ---- 2. 与 md3 能力表 cap_id 比对 ----
caps = json.load(open(CAPS))['caps']
capmap = {c['cap_id']: c for c in caps}
hit_caps = [h for h in hostcodes if h in capmap]
print(f'[2] md3 能力表 cap_id 共 {len(caps)} 条；85 个 host_code 中命中 {len(hit_caps)} 个')
capgroups = collections.Counter(c['group'] for c in caps)
print('    md3 能力 group 分布（前 20）:', dict(list(capgroups.most_common(20))))

# ---- 3. PE 段 ----
pe = pefile.PE(M3)
secs = {s.Name.rstrip(b'\x00').decode(): s for s in pe.sections}
for n, s in secs.items():
    print(f'[3] 节 {n}: VA 0x{s.VirtualAddress+pe.OPTIONAL_HEADER.ImageBase:08X} '
          f'size 0x{s.Misc_VirtualSize:X} off 0x{s.PointerToRawData:X}')
raw = open(M3, 'rb').read()
IB = pe.OPTIONAL_HEADER.ImageBase


def v2o(va):
    for s in pe.sections:
        if s.VirtualAddress <= va - IB < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (va - IB - s.VirtualAddress)
    return None


# ---- 4. 函数表 ----
funcs = []
for line in open(FUNCS, encoding='utf-8', errors='replace'):
    p = line.split()
    if p and p[0].startswith('0x'):
        funcs.append((int(p[0], 16), p[4] if len(p) > 4 else ''))
funcs.sort()
print(f'[4] 函数表 {len(funcs)} 个')

# ---- 5. capstone 扫描 .text 立即数 ----
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
text = secs['.text']
tstart, tend = IB + text.VirtualAddress, IB + text.VirtualAddress + text.SizeOfRawData
tbuf = raw[text.PointerToRawData:text.PointerToRawData + text.SizeOfRawData]

HCSET = set(hostcodes)
immediate_hits = collections.defaultdict(list)   # hostcode -> [(va, func)]

faddrs = [f[0] for f in funcs]
fname = {f[0]: f[1] for f in funcs}


def fname_of(va):
    import bisect
    i = bisect.bisect_right(faddrs, va) - 1
    return faddrs[i] if i >= 0 else 0


def scan_range(va0, va1):
    off = v2o(va0)
    if off is None:
        return
    code = raw[off:off + (va1 - va0)]
    for ins in md.disasm(code, va0):
        if ins.mnemonic in ('jmp', 'call', 'ret', 'nop', 'lea'):
            pass
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_IMM:
                v = op.imm
                if v in HCSET:
                    immediate_hits[v].append((ins.address, fname_of(ins.address)))
                elif (v & 0xFFFF) in HCSET and v > 0xFFFF:
                    pass  # 32 位立即数不算（避免假阳性）


# 线性扫全 .text（x86 线性反汇编有噪声，只接受立即数命中，且后面按函数归属归并）
scan_range(tstart, tend)
print(f'[5] .text 线性反汇编完成，命中 {len(immediate_hits)} / {len(hostcodes)} 个 host_code')

# ---- 6. .rdata/.data 里的 16 位 LE 出现（结构体初始化/常量表）----
data_hits = collections.defaultdict(list)
for sname in ('.rdata', '.data'):
    s = secs[sname]
    buf = raw[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
    for hc in hostcodes:
        pat = struct.pack('<H', hc)
        start = 0
        while True:
            i = buf.find(pat, start)
            if i < 0:
                break
            data_hits[hc].append((IB + s.VirtualAddress + i, sname))
            start = i + 1
print(f'[6] 数据节 16 位 LE 匹配：命中 {len(data_hits)} / {len(hostcodes)} 个')

json.dump({
    'hostcodes': hostcodes,
    'caps_hit': hit_caps,
    'imm': {k: v for k, v in immediate_hits.items()},
    'data': {k: v for k, v in data_hits.items()},
}, open('md3_hits.json', 'w'), indent=1)

print('\n===== 逐条明细 =====')
for hc in hostcodes:
    im = immediate_hits.get(hc, [])
    dh = data_hits.get(hc, [])
    c = capmap.get(hc)
    cs = f"cap:{c['group']}/{c['sub']} hdl 0x{c['handler']:08X}" if c else '-'
    print(f'0x{hc:04X}  imm={len(im):<3} data={len(dh):<3} {cs}'
          + (f"  imm@{','.join(f'0x{a:08X}' for a, _ in im[:4])}" if im else ''))
