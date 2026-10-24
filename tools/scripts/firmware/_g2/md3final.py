# -*- coding: utf-8 -*-
"""G2 反例检查（定稿）：只用 md3 CFG 已确认函数体（cfg_funcs.txt，1241 个，含精确指令数）
做 capstone 反汇编，抽取立即数。这样每一条命中都落在已知指令边界上，不再是误解码。
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
CFG = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cfg_funcs.txt'
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

pe = pefile.PE(M3)
IB = pe.OPTIONAL_HEADER.ImageBase
raw = open(M3, 'rb').read()
secs = {s.Name.rstrip(b'\x00').decode(): s for s in pe.sections}


def v2o(va):
    for s in pe.sections:
        if s.VirtualAddress <= va - IB < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (va - IB - s.VirtualAddress)
    return None


fnlist = []
for line in open(CFG, encoding='utf-8', errors='replace'):
    p = line.split()
    if len(p) >= 2 and p[0].startswith('0x'):
        fnlist.append((int(p[0], 16), int(p[1])))
print(f'CFG 函数体 {len(fnlist)} 个')

named = {}
for line in open(FUNCS, encoding='utf-8', errors='replace'):
    p = line.split()
    if p and p[0].startswith('0x') and len(p) > 4 and p[4]:
        named[int(p[0], 16)] = p[4]
faddrs = sorted(named)
exports = {int(p[0], 16) for p in [l.split() for l in open(FUNCS)] if p and p[0].startswith('0x')}


def fname(va):
    i = bisect.bisect_right(faddrs, va) - 1
    if i >= 0:
        return named.get(faddrs[i], f'sub_{faddrs[i]:08X}')
    return f'sub_{va:08X}'


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

hits = collections.defaultdict(list)
nins = 0
for fa, cnt in fnlist:
    if cnt <= 0:
        continue
    o = v2o(fa)
    if o is None:
        continue
    buf = raw[o:o + cnt * 16 + 32]
    try:
        for k, ins in enumerate(md.disasm(buf, fa)):
            if k >= cnt:
                break
            nins += 1
            for op in ins.operands:
                if op.type == capstone.x86.X86_OP_IMM and op.imm in HCSET:
                    hits[op.imm].append((ins.address, ins.mnemonic, ins.op_str, fname(ins.address)))
    except Exception:
        pass
print(f'已解码 {nins} 条指令（CFG 覆盖），命中 host_code 立即数 {len(hits)} / {len(hostcodes)} 个')

# 分类：整值（低字节 0 或整百）视为通用常量噪声
def is_round(v):
    return (v & 0xFF) == 0


dist = {v: h for v, h in hits.items() if not is_round(v)}
rnd = {v: h for v, h in hits.items() if is_round(v)}
print(f'  其中可判别（低字节≠0）{len(dist)} 个；整值（0xN00，通用常量噪声）{len(rnd)} 个')

caps = json.load(open(CAPS))['caps']
capmap = {c['cap_id']: c for c in caps}
hit_caps = [h for h in hostcodes if h in capmap]
print(f'\n与 md3 能力表 cap_id 精确相同的 host_code：{len(hit_caps)} 个 '
      + ', '.join(f'0x{h:04X}({capmap[h]["group"]}/{capmap[h]["sub"]})' for h in hit_caps))

print('\n===== 可判别命中明细 =====')
for v in hostcodes:
    if v in dist:
        hs = dist[v]
        fns = collections.Counter(h[3] for h in hs)
        print(f'0x{v:04X}  x{len(hs)}   ' + ', '.join(f'{k}×{c}' for k, c in fns.most_common(5)))
        for a, m, o, f in hs[:3]:
            print(f'        0x{a:08X}  {m} {o}   [{f}]')
print('\n===== 整值命中（噪声，仅计数）=====')
print('  ' + ', '.join(f'0x{v:04X}×{len(rnd[v])}' for v in hostcodes if v in rnd))

print('\n===== 未命中（md3 .text 中无立即数）=====')
miss = [v for v in hostcodes if v not in hits]
print(f'  共 {len(miss)} 个: ' + ' '.join(f'0x{v:04X}' for v in miss))

json.dump({'n_hostcodes': len(hostcodes),
           'imm_distinctive': {f'0x{v:04X}': [[a, m, o, f] for a, m, o, f in h] for v, h in dist.items()},
           'imm_round': {f'0x{v:04X}': len(h) for v, h in rnd.items()},
           'missing': [f'0x{v:04X}' for v in miss],
           'caps_hit': [f'0x{h:04X}' for h in hit_caps]},
          open('md3_final.json', 'w'), indent=1)
