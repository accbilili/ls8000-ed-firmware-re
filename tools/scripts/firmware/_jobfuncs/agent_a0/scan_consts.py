"""全镜像搜索（只读 D:\）：
1. 所有 cmp.w #imm 与立即数 0x01C2/0x03E8/0x01E0 相关的指令；
2. 所有对 0x200102 的写入（ASIC 命令词）；
3. 所有对 0x200182/4/6/8 的写入。
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
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

IMMS = {'0x01c2': '450', '0x03e8': '1000', '0x01e0': '480', '0x01ba': '442',
        '0x0780': '1920', '0x0950': 'err2384', '0x0930': 'err2352', '0x0920': 'err2336', '0x0940': 'err2368'}
ADDRS = ['0x200102', '0x200182', '0x200184', '0x200186', '0x200188', '0x2001a4', '0x2001c2', '0x2001c4']

hits_imm = {}
hits_addr = {a: [] for a in ADDRS}

pc = 0
while pc < len(d) - 16:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        pc += 2
        continue
    txt = ' '.join(x for x in (a1, a2) if x)
    for imm, tag in IMMS.items():
        if imm in txt:
            hits_imm.setdefault(tag, []).append((pc + BASE, nm, txt))
    for a in ADDRS:
        if a in txt:
            hits_addr[a].append((pc + BASE, nm, txt))
    pc = nxt if sz and sz > 0 else pc + 2

print('=== 立即数 450/1000/480/442/1920 及错误码相关指令 ===')
for tag in ('450', '1000', '480', '442', '1920'):
    print(f'--- {tag} ({len(hits_imm.get(tag, []))} 处) ---')
    for a, nm, txt in hits_imm.get(tag, [])[:40]:
        print(f'  0x{a:06X}  {nm:<9} {txt}')

print('\n=== 0x200102 写入（ASIC 命令寄存器）===')
for a, nm, txt in hits_addr['0x200102']:
    print(f'  0x{a:06X}  {nm:<9} {txt}')

print('\n=== 0x200182/4/6/8 写入 ===')
for a in ('0x200182', '0x200184', '0x200186', '0x200188'):
    print(f'--- {a} ({len(hits_addr[a])} 处) ---')
    for x, nm, txt in hits_addr[a][:20]:
        print(f'  0x{x:06X}  {nm:<9} {txt}')

print('\n=== 0x2001a4 / 0x2001c2 / 0x2001c4 ===')
for a in ('0x2001a4', '0x2001c2', '0x2001c4'):
    print(f'--- {a} ({len(hits_addr[a])} 处) ---')
    for x, nm, txt in hits_addr[a][:20]:
        print(f'  0x{x:06X}  {nm:<9} {txt}')
