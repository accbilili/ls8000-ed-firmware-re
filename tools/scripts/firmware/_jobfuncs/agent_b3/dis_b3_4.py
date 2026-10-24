"""第四轮：补齐上下文
1. 0x027C60-0x027D40（0x027CAC 调用 0x02BCCE 的上下文）
2. 0x026500-0x026760（flash 助手 0x0272D6/0x027362/0x02726E 的调用者——执行层其他臂）
3. 0x016D60-0x016F40（0x016E8E 的姊妹调用者 0x016D80/0x016EE2）
4. fn_03109E 已 dump；再读 0x012080-0x012100 找 0x121xx 主函数入口
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

def disasm_range(start, end):
    lines = []
    pc = start - BASE
    while pc < end - BASE:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        raw = d[pc:pc+sz].hex(' ')
        lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1,a2) if x) + f'   ; {raw}')
        pc += sz
    return lines

for name, start, end in [('ctx_027Cxx', 0x027C60, 0x027D40),
                         ('ctx_0265xx', 0x026500, 0x026760),
                         ('ctx_016Dxx', 0x016D60, 0x016F40),
                         ('entry_0120xx', 0x012080, 0x012100)]:
    lines = disasm_range(start, end)
    open(os.path.join(OUT, f'{name}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(f'{name}: {len(lines)} 行')
