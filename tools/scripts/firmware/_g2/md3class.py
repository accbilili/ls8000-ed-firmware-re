# -*- coding: utf-8 -*-
"""把 md3 命中按“是否特征值”分类：低字节非 0 且非整百/整千的才是可判别常量。"""
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

funcs = []
for line in open(FUNCS, encoding='utf-8', errors='replace'):
    p = line.split()
    if p and p[0].startswith('0x'):
        funcs.append((int(p[0], 16), p[4] if len(p) > 4 else ''))
funcs.sort()
faddrs = [f[0] for f in funcs]
fnames = {f[0]: (f[1] or '') for f in funcs}


def fname_of(va):
    i = bisect.bisect_right(faddrs, va) - 1
    if i < 0:
        return ''
    n = fnames.get(faddrs[i], '')
    return n or f'sub_{faddrs[i]:08X}'


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

hits = collections.defaultdict(list)
for V in hostcodes:
    pat = struct.pack('<H', V)
    pos = toff
    while True:
        i = raw.find(pat, pos, toff + tsz)
        if i < 0:
            break
        pos = i + 1
        va_target = tva + (i - toff)
        for back in range(0, 9):
            s = i - back
            if s < toff:
                break
            sva = tva + (s - toff)
            got = None
            for ins in md.disasm(raw[s:s + 16], sva):
                if ins.address <= va_target < ins.address + ins.size:
                    for op in ins.operands:
                        if op.type == capstone.x86.X86_OP_IMM and op.imm == V:
                            got = (ins.address, ins.mnemonic, ins.op_str)
                if ins.address > va_target:
                    break
            if got:
                hits[V].append(got + (fname_of(got[0]),))
                break


def distinctive(v):
    lo = v & 0xFF
    return lo != 0 and (v & 0x00FF) not in (0x00,) and not (v & 0x0F00 == 0 and lo == 0)


d_hit = {v: h for v, h in hits.items() if distinctive(v)}
r_hit = {v: h for v, h in hits.items() if not distinctive(v)}

print('=' * 78)
print('A. 特征值命中（低字节非 0，非整千/整百，可判别）')
print('=' * 78)
for v in hostcodes:
    if v in d_hit:
        hs = d_hit[v]
        fns = collections.Counter(h[3] for h in hs)
        print(f'0x{v:04X}  x{len(hs):<3} 函数: ' + ', '.join(f'{k}({c})' for k, c in fns.most_common(6)))
        for a, m, o, f in hs[:4]:
            print(f'        0x{a:08X}  {m} {o}   [{f}]')
print(f'\n小计：特征值命中 {len(d_hit)} / {len([v for v in hostcodes if distinctive(v)])} 个特征值')

print('\n' + '=' * 78)
print('B. 整值命中（0x1000/0x2000/... —— 通用常量，判定为噪声，仅供参考）')
print('=' * 78)
for v in hostcodes:
    if v in r_hit:
        print(f'0x{v:04X}  x{len(r_hit[v]):<3} (视为噪声)')
print(f'\n小计：整值命中 {len(r_hit)} 个（全部判为噪声）')

print('\n' + '=' * 78)
print(f'总计：85 个 host_code 中，作为 x86 立即数出现在 md3 .text 的 = {len(hits)} 个；'
      f'其中可判别（非通用常量）的 = {len(d_hit)} 个')
print('=' * 78)
json.dump({'distinctive': {f'0x{v:04X}': [[a, m, o, f] for a, m, o, f in h] for v, h in d_hit.items()},
           'round': {f'0x{v:04X}': len(h) for v, h in r_hit.items()}},
          open('md3_class.json', 'w'), indent=1)
