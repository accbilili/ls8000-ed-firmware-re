"""最终 xref：fn 0x011460 / 0x021536 / 0x02151E / 0x0214A6 的调用者；
0x022100 宿主函数入口；sense[0x6F]。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
N = len(d)

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except: return None
    return None

CALLS = {'jsr', 'bsr', 'jmp', 'bra', 'bt'}
targets = {0x011460: 'wrapper2', 0x021536: 'merge_status', 0x02151E: 'merge_caller',
           0x0214A6: 'scsi_reset', 0x0114d8: 'cmd_dispatch', 0x0114b8: 'compute_509'}
xrefs = {t: [] for t in targets}
for off in range(0, N - 8, 2):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None: continue
    if nm in CALLS:
        t = parse_tgt(a1)
        if t in targets:
            xrefs[t].append((off + BASE, nm, a1))
for t, name in targets.items():
    print(f'xrefs to 0x{t:06X} ({name}): {len(xrefs[t])}')
    for a, nm, a1 in xrefs[t][:20]:
        print(f'   0x{a:06X}  {nm} {a1}')

def rd(addr, n):
    off = addr - BASE
    return d[off:off+n]
print('\nsense[0x6F] @ 0x019375 =', rd(0x019375, 5).hex(' '))
print('sense[0x64] @ 0x0192F2 =', rd(0x0192F2, 5).hex(' '))
print('sense[0x78] @ 0x01939C =', rd(0x01939C, 5).hex(' '))
print('sense[0x79] @ 0x0193A1 =', rd(0x0193A1, 5).hex(' '))
print('sense[0x7D] @ 0x0193BB =', rd(0x0193BB, 5).hex(' '))
print('sense[0x00] @ 0x01914A =', rd(0x01914A, 5).hex(' '))

# 0x022100 宿主函数入口：向前找 rts 后的入口
print('\n===== walk back from 0x022100 to find entry =====')
pc = 0x022100 - BASE
# 向前扫，找函数序言模式（stm.l / mov.l erN,@-sp 后紧跟的入口）
import json
cfg = json.load(open(cfg('cfg_v4.json')))
owner = cfg['owner']
for probe in (0x022100, 0x022308, 0x022434):
    o = owner.get('0x%x' % probe)
    print(f'0x{probe:06X} owner =', hex(int(o, 16)) if o else None)
