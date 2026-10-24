"""反汇编兄弟 DLL 的 NkDriverEntry（唯一导出），用于从接收端反推 request 结构。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import pefile, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

P = sys.argv[1] if len(sys.argv) > 1 else sample('driver/NKDUSCAN.dll')
VA = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x10003C40
N = int(sys.argv[3]) if len(sys.argv) > 3 else 60

pe = pefile.PE(P, fast_load=True)
ib = pe.OPTIONAL_HEADER.ImageBase
data = open(P, 'rb').read()

def va2off(va):
    rva = va - ib
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return rva - s.VirtualAddress + s.PointerToRawData
    return None

def read(va, n):
    o = va2off(va)
    return data[o:o + n] if o is not None else b''

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = 0
print('# %s base 0x%08X' % (P, ib))
for i, ins in enumerate(md.disasm(read(VA, 4000), VA)):
    print('%08X  %-22s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))
    if i + 1 >= N:
        break
