"""展开若干上下文区间，确认轴语义与调用顺序。"""
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

RANGES = [
    (0x02ADCE, 0x02AF80, 'ctx_02ADCE_filmadv'),      # 走片命令包装
    (0x027930, 0x027A60, 'ctx_027930_job'),          # 调 0x02B038+0x02CC04+0x0289B4 的作业函数
    (0x027C60, 0x027D20, 'ctx_027CA0'),              # 另一个 0x02B038 调用点
    (0x02BCB0, 0x02BD00, 'ctx_02BCEC'),              # 另一个 0x02BAA6 调用点
    (0x02B98A, 0x02BA30, 'ctx_02B98A_job41'),        # E0 0x41 作业（用 mover C）
    (0x03EE10, 0x03EE40, 'tab_03EE10'),              # 片夹阈值表
    (0x03F0E8, 0x03F108, 'tab_03F0E8'),              # mover A 包表
    (0x03F0F8, 0x03F118, 'tab_03F0F8'),              # mover B/C 包表
]
for lo, hi, name in RANGES:
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
    print(name, len(lines), 'insns')
