"""F6 续 v8：命令行区间反汇编。用法: dll_dump.py <dllname> <lohex> <hihex>"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import sys, pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

name, lo, hi = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16)
path = sample('driver/%s') % name

pe = pefile.PE(path, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
ib = pe.OPTIONAL_HEADER.ImageBase
iat = {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in e.imports:
        iat.setdefault(imp.address, imp.name.decode() if imp.name else 'ord#%d' % imp.ordinal)
sec = []
for s in pe.sections:
    sec.append((ib + s.VirtualAddress, ib + s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
                s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b'\0').decode()))


def rd(va, ln):
    for (l, h, praw, sraw, nm) in sec:
        if l <= va < h:
            off = praw + (va - l)
            return pe.__data__[off:off + ln]
    return b''


va = lo
while va < hi:
    one = next(md.disasm(rd(va, 16), va, 1), None)
    if one is None:
        print('0x%08X  .db 0x%02X' % (va, rd(va, 1)[0]))
        va += 1
        continue
    line = '0x%08X  %-7s %s' % (one.address, one.mnemonic, one.op_str)
    for op in one.operands:
        if op.type == 3 and op.mem.base == 0 and op.mem.index == 0 and op.mem.disp in iat:
            line += '   ; %s' % iat[op.mem.disp]
    print(line)
    va += one.size
