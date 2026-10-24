"""全镜像扫描（只读 D:\）：
1. 所有引用 0x400400 的指令（找写入者）；
2. 所有对 0x0269A6(exec)/0x0275F2(job)/0x026BF8(parseA)/0x026EFC(parseB) 的调用/跳转。
线性扫描 + 修复版解码器。"""
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

hits_400400 = []
calls = {0x0269A6: 'exec', 0x0275F2: 'joblayer', 0x026BF8: 'parseA', 0x026EFC: 'parseB',
         0x03A3D4: 'jobA0', 0x026A92: 'armA0'}
call_hits = []

pc = 0
while pc < len(d) - 16:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        pc += 2
        continue
    txt = ' '.join(x for x in (a1, a2) if x)
    if '0x400400' in txt or '0x00400400' in txt:
        hits_400400.append((pc + BASE, nm, txt))
    if nm in ('jsr', 'bsr', 'jmp'):
        for t, tag in calls.items():
            if a1 and a1.strip() == f'0x{t:06x}':
                call_hits.append((pc + BASE, nm, tag, t))
    pc = nxt if sz and sz > 0 else pc + 2

print('=== 引用 0x400400 的指令 ===')
for a, nm, txt in hits_400400:
    print(f'0x{a:06X}  {nm:<9} {txt}')
print(f'\n=== 层间调用/跳转 ===')
for a, nm, tag, t in call_hits:
    print(f'0x{a:06X}  {nm:<5} -> 0x{t:06X} ({tag})')
