"""全镜像扫描 jsr/bsr/jmp(绝对/相对) 对目标函数集的引用。
编码（h8.lst h 档）：
  jsr abs24: 5E AA AA AA (4B, target=u32&0xffffff)
  jmp abs24: 5A AA AA AA (4B)
  bsr rel16: 5C 00 DD DD (4B, target=base+pc+4+s16(disp))
先字节模式粗筛，再用 h8dis.decode 复核确实是 call/jmp。
只读 D:\。
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
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
n = len(d)

TARGETS = {
    0x02BAA6: 'E0-0x81 job: 0x02BAA6',
    0x02CC04: 'E0-0x81 job: 0x02CC04',
    0x02B038: 'E0-0x81 job: 0x02B038',
    0x02A2F6: 'mover A (SCI3, 0x4202A4)',
    0x02BF00: 'mover B (SCI2, 0x4202EE)',
    0x02B276: 'mover C (SCI1, 0x4202E6)',
    0x02ADCE: 'film advance (ident chain)',
    0x029D2A: 'limit check',
    0x0289B4: 'carrier ident main',
    0x027DC4: 'load state machine',
    0x028648: 'E0-0x81 handler',
}

def s16(x): return x - 65536 if x >= 32768 else x

hits = {t: [] for t in TARGETS}
for p in range(0, n - 4, 2):
    b0 = d[p]
    t = None
    if b0 == 0x5E:      # jsr abs24
        t = ((d[p] << 24) | (d[p+1] << 16) | (d[p+2] << 8) | d[p+3]) & 0xffffff
    elif b0 == 0x5C and d[p+1] == 0x00:   # bsr rel16
        t = (BASE + p + 4 + s16((d[p+2] << 8) | d[p+3])) & 0xffffff
    elif b0 == 0x5A:    # jmp abs24
        t = ((d[p] << 24) | (d[p+1] << 16) | (d[p+2] << 8) | d[p+3]) & 0xffffff
    if t in TARGETS:
        # 复核：该偏移确实解出 call/jmp 且目标一致
        sz, nm, a1, a2, nxt = h.decode(p)
        if nm in ('jsr', 'bsr', 'jmp') and a1 is not None:
            try:
                tv = int(a1, 16)
            except ValueError:
                continue
            if tv == t:
                hits[t].append((p + BASE, nm, sz))

for t in sorted(TARGETS):
    lst = hits[t]
    print(f'--- 0x{t:06X} ({TARGETS[t]}): {len(lst)} refs')
    for a, nm, sz in lst:
        print(f'    {nm} @ 0x{a:06X} (size {sz})')
