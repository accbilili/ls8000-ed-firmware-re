"""反汇编 LS8000.md3 指定 VA 区间，用于推导各命令的 CDB 构造字节。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct
import sys

from capstone import CS_ARCH_X86, CS_MODE_32, Cs

MD3 = sample('driver/LS8000.md3')
d = open(MD3, 'rb').read()

pe = struct.unpack_from('<I', d, 0x3C)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
optsz = struct.unpack_from('<H', d, pe + 20)[0]
base = struct.unpack_from('<I', d, pe + 24 + 28)[0]
so = pe + 24 + optsz
secs = []
for i in range(nsec):
    nm = d[so + i * 40: so + i * 40 + 8].rstrip(b'\x00').decode('latin1')
    vs, va, rs, ra = struct.unpack_from('<IIII', d, so + i * 40 + 8)
    secs.append((nm, base + va, vs, ra, rs))


def va2off(va):
    for nm, v, vs, ra, rs in secs:
        if v <= va < v + max(vs, rs):
            return ra + (va - v)
    return None


def dis(va_start, va_end):
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = False
    o = va2off(va_start)
    code = d[o: o + (va_end - va_start) + 64]
    for ins in md.disasm(code, va_start):
        if ins.address > va_end:
            break
        print('0x%08X  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))


if __name__ == '__main__':
    a = int(sys.argv[1], 16)
    b = int(sys.argv[2], 16)
    print('=== LS8000.md3  0x%08X – 0x%08X ===' % (a, b))
    dis(a, b)
