"""展开 mover B 低层命令 0x02BE32、等待 0x02C8B4，并扫描一批 helper 的引用。"""
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
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def dis(lo, hi, name):
    lines = []
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        pc = nxt if nxt > pc else pc + 2
    open(os.path.join(OUT, f'{name}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(name, len(lines))

dis(0x02BE32, 0x02BE90, 'ctx_02BE32')
dis(0x02C8B4, 0x02C8E0, 'ctx_02C8B4')
dis(0x02B8EA, 0x02B98A, 'ctx_02B8EA')
dis(0x02ACBA, 0x02ACD0, 'ctx_02ACBA')

def s16(x): return x - 65536 if x >= 32768 else x
TARGETS = {0x02BE32:'moverB low cmd', 0x02C8B4:'wait B', 0x02C9E4:'moveB abs', 0x02CA78:'moveB rel',
           0x02CAB8:'moveB tbl', 0x02CB66:'E0 0x42 job', 0x02B0E8:'film return', 0x02BCCE:'holder engage',
           0x02ACBA:'settle', 0x02B8EA:'job41 helper', 0x02C9E4:'moveB abs', 0x027B1E:'load job fn'}
print('--- refs ---')
for p in range(0, len(d) - 4, 2):
    b0 = d[p]; t = None
    if b0 == 0x5E:
        t = ((d[p] << 24) | (d[p+1] << 16) | (d[p+2] << 8) | d[p+3]) & 0xffffff
    elif b0 == 0x5C and d[p+1] == 0x00:
        t = (BASE + p + 4 + s16((d[p+2] << 8) | d[p+3])) & 0xffffff
    elif b0 == 0x5A:
        t = ((d[p] << 24) | (d[p+1] << 16) | (d[p+2] << 8) | d[p+3]) & 0xffffff
    if t in TARGETS:
        sz, nm, a1, a2, nxt = h.decode(p)
        if nm in ('jsr', 'bsr', 'jmp') and a1:
            try:
                if int(a1, 16) == t:
                    print(f'  0x{t:06X} ({TARGETS[t]}): {nm} @ 0x{p+BASE:06X}')
            except ValueError:
                pass
