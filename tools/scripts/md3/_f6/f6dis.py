"""F6: 定向反汇编若干区间。只读 D:\\。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from pe_md3 import PE

p = PE()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL


def dis(lo, hi, label=''):
    print('=' * 70)
    print('%s  0x%08X..0x%08X' % (label, lo, hi))
    va = lo
    while va < hi:
        buf = p.read(va, 16)
        if not buf:
            break
        one = next(md.disasm(buf, va, 1), None)
        if one is None:
            print('0x%08X  .db 0x%02X' % (va, buf[0]))
            va += 1
            continue
        print('0x%08X  %-8s %s' % (va, one.mnemonic, one.op_str))
        va += one.size


if __name__ == '__main__':
    spec = sys.argv[1:]
    for s in spec:
        lo, hi, lab = s.split(',')
        dis(int(lo, 0), int(hi, 0), lab)
