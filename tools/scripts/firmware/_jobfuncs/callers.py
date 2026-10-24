"""通用：全镜像找某函数的调用者（jsr 绝对 + bsr 相对都覆盖）。
用法：python callers.py 0x02D4CC [0x013776 ...]
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
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h8dis import H8
from h8fix import load_entries_fixed

BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
h = H8(d, load_entries_fixed(sample('h8.lst')), base=BASE)


def callers(target):
    """返回 [(call_addr, kind)]，kind ∈ jsr/bsr"""
    out = []
    for off in range(0, len(d) - 5, 2):
        sz, nm, a1, a2, nxt = h.decode(off)
        if nm is None:
            continue
        if nm == 'jsr' and a1 and a1.startswith('0x'):
            try:
                if int(a1, 16) == target:
                    out.append((off + BASE, 'jsr'))
            except ValueError:
                pass
        elif nm == 'bsr':
            # bsr d:16，目标 = pc + 4 + disp16（从指令尾读两字节大端）
            disp = (d[off + 2] << 8) | d[off + 3]
            if disp >= 0x8000:
                disp -= 0x10000
            tgt = (off + BASE) + 4 + disp
            if tgt == target:
                out.append((off + BASE, 'bsr'))
    return out


def show(start, n=14):
    pc = start - BASE
    lines = []
    for _ in range(n):
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'   0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}'); pc += 2; continue
        lines.append(f'   0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        pc = nxt
        if nm == 'rts':
            break
    return '\n'.join(lines)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        t = int(arg, 16)
        cl = callers(t)
        print('=' * 78)
        print(f'0x{t:06X} 的调用者：{len(cl)} 处')
        for a, k in cl:
            print(f'  --- {k} @0x{a:06X}')
            print(show(a))
