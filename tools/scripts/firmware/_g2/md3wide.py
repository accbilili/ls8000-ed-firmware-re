# -*- coding: utf-8 -*-
"""扩覆盖版：以 cfg_funcs.txt 的函数入口 + calls.pkl 的全部 call 目标为种子，
按“遇到 ret / 非法指令即停”的规则反汇编，提高 .text 覆盖率后再抽立即数。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import json, struct, collections, bisect, pickle
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

pe = pefile.PE(M3)
IB = pe.OPTIONAL_HEADER.ImageBase
raw = open(M3, 'rb').read()
secs = {s.Name.rstrip(b'\x00').decode(): s for s in pe.sections}
text = secs['.text']
tva, tsz, toff = IB + text.VirtualAddress, text.SizeOfRawData, text.PointerToRawData


def v2o(va):
    for s in pe.sections:
        if s.VirtualAddress <= va - IB < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (va - IB - s.VirtualAddress)
    return None


seeds = set()
for line in open(CFG, encoding='utf-8', errors='replace'):
    p = line.split()
    if p and p[0].startswith('0x'):
        seeds.add(int(p[0], 16))
cl = pickle.load(open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\calls.pkl', 'rb'))
for s, d in cl['calls']:
    if tva <= d < tva + tsz:
        seeds.add(d)
print(f'种子 {len(seeds)} 个（cfg 入口 + call 目标）')

named = {}
for line in open(FUNCS, encoding='utf-8', errors='replace'):
    p = line.split()
    if p and p[0].startswith('0x') and len(p) > 4 and p[4]:
        named[int(p[0], 16)] = p[4]
faddrs = sorted(named)


def fname(va):
    i = bisect.bisect_right(faddrs, va) - 1
    return named.get(faddrs[i], f'sub_{faddrs[i]:08X}') if i >= 0 else f'sub_{va:08X}'


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
hits = collections.defaultdict(list)
covered = bytearray(tsz)
nins = 0
for fa in sorted(seeds):
    o = v2o(fa)
    if o is None:
        continue
    end = min(toff + tsz, o + 8000)
    for ins in md.disasm(raw[o:end], fa):
        nins += 1
        covered[ins.address - tva:ins.address - tva + ins.size] = b'\x01' * ins.size
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_IMM and op.imm in HCSET:
                hits[op.imm].append((ins.address, ins.mnemonic, ins.op_str, fname(ins.address)))
        if ins.mnemonic == 'ret':
            break
cov = covered.count(1)
print(f'解码 {nins} 条指令，覆盖 .text {cov} 字节 ({cov*100/tsz:.1f}%)')

dist = {v: h for v, h in hits.items() if (v & 0xFF) != 0}
rnd = {v: h for v, h in hits.items() if (v & 0xFF) == 0}
print(f'命中 {len(hits)} / {len(hostcodes)} 个 host_code；可判别(低字节≠0) {len(dist)} 个，整值 {len(rnd)} 个')

caps = json.load(open(CAPS))['caps']
capmap = {c['cap_id']: c for c in caps}
hit_caps = [h for h in hostcodes if h in capmap]
print(f'与 md3 cap_id 精确相同：{len(hit_caps)} 个 '
      + ', '.join(f'0x{h:04X}' for h in hit_caps))

print('\n===== 可判别命中明细 =====')
for v in hostcodes:
    if v in dist:
        hs = dist[v]
        fns = collections.Counter(h[3] for h in hs)
        print(f'0x{v:04X}  x{len(hs)}   ' + ', '.join(f'{k}×{c}' for k, c in fns.most_common(5)))
        for a, m, o, f in hs[:4]:
            print(f'        0x{a:08X}  {m} {o}   [{f}]')
print('\n===== 整值命中（通用常量，噪声）=====')
print('  ' + ', '.join(f'0x{v:04X}×{len(rnd[v])}' for v in hostcodes if v in rnd))
print('\n===== 未命中 =====')
miss = [v for v in hostcodes if v not in hits]
print(f'  共 {len(miss)} 个')
json.dump({'coverage_pct': round(cov * 100 / tsz, 1), 'nins': nins,
           'distinctive': {f'0x{v:04X}': [[a, m, o, f] for a, m, o, f in h] for v, h in dist.items()},
           'round': {f'0x{v:04X}': len(h) for v, h in rnd.items()},
           'missing': [f'0x{v:04X}' for v in miss],
           'caps_hit': [f'0x{h:04X}' for h in hit_caps]},
          open('md3_wide.json', 'w'), indent=1)
