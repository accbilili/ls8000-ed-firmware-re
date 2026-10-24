import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
H = H8(D, load_entries(sample('h8.lst')), base=BASE)


def dis(addr, n=200, stop_on_rts=False):
    """从 addr 开始反汇编 n 条指令。返回行列表。"""
    pc = addr - BASE
    out = []
    for _ in range(n):
        if pc < 0 or pc + 1 >= len(D):
            break
        r = H.decode(pc)
        if r is None or r[1] is None:
            out.append(f'0x{pc+BASE:06X}  .byte 0x{D[pc]:02X}')
            pc += 2
            continue
        sz, nm, a1, a2, nxt = r
        ops = ', '.join(x for x in (a1, a2) if x)
        out.append(f'0x{pc+BASE:06X}  {nm:<9} {ops}')
        if stop_on_rts and nm in ('rts', 'rte', 'jmp', 'bra'):
            break
        pc = nxt
    return out


if __name__ == '__main__':
    a = int(sys.argv[1], 16)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    for l in dis(a, n):
        print(l)
