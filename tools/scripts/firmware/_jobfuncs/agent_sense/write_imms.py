"""收尾：枚举所有写点的立即数；确认 0x020B84 主循环与 fn 0x011000 的调用者。"""
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
N = len(d)

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except: return None
    return None

CALLS = {'jsr', 'bsr', 'jmp', 'bra', 'bt'}
# 主循环/SCSI handler 调用者
for tgt in (0x020B84, 0x011000, 0x011162):
    xs = []
    for off in range(0, N - 8, 2):
        sz, nm, a1, a2, nxt = h.decode(off)
        if nm in CALLS and parse_tgt(a1) == tgt:
            xs.append((off + BASE, nm, a1))
    print(f'xrefs to 0x{tgt:06X}: {len(xs)}')
    for a, nm, a1 in xs[:10]:
        print(f'   0x{a:06X}  {nm} {a1}')

# 写点立即数枚举：对每个直接写点，回看前 1-2 条指令
writes = [0x011004, 0x0116AA, 0x011AB6, 0x011ADC, 0x011B04, 0x011B96, 0x011BBC, 0x011BE4,
          0x011CF6, 0x011D0C, 0x011D28, 0x011D48, 0x011DCA, 0x011E54, 0x011E7E, 0x011EDC,
          0x011F00, 0x011F20, 0x011FEA, 0x01201A, 0x012030, 0x012050, 0x012894, 0x0128FA,
          0x01291E, 0x012950, 0x01297E, 0x0129A4, 0x0129CC, 0x0129E4, 0x012A2E, 0x0133E8,
          0x013412, 0x01348C, 0x0134B6, 0x013A26, 0x013B8E, 0x013D2C, 0x013E2A, 0x013FD6,
          0x014176, 0x0171C6, 0x020B2C, 0x020E88, 0x021476, 0x0214EE, 0x02158A, 0x0217A6,
          0x021D34, 0x024102, 0x0255E4, 0x025AA6, 0x025DA0, 0x025E94, 0x0261DC]
print('\n=== write-site immediates (instruction before write) ===')
from collections import Counter
vals = Counter()
for w in writes:
    # 回退找紧邻指令：尝试 w-4, w-2, w-6 起点 decode，取落在 w 前的
    best = None
    for back in (2, 4, 6, 8):
        st = w - back - BASE
        if st < 0: continue
        sz, nm, a1, a2, nxt = h.decode(st)
        if nm and (st + BASE + sz) == w:
            best = (nm, a1, a2)
            break
    if best:
        nm, a1, a2 = best
        txt = f'{nm} ' + ', '.join(x for x in (a1, a2) if x)
        print(f'0x{w:06X}: {txt}')
        if a1 and a1.startswith('#'):
            try: vals[int(a1[1:], 16)] += 1
            except: pass
    else:
        print(f'0x{w:06X}: <no immediate found>')
print('\nvalue histogram:', {hex(k): v for k, v in sorted(vals.items())})
