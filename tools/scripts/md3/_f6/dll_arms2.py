"""F6 续 v6：定点反汇编 Nk*.dll 的 NkDriverEntry 各点钟函数。只读 D:\\。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

RANGES = [
    (sample('driver/NKDUSCAN.dll'), [
        (0x10003E30, 0x10003ED0, 'sel1 fn'),
        (0x10004240, 0x100042C0, 'sel2 fn'),
        (0x10004290, 0x10004310, 'sel3 fn'),
        (0x100042E0, 0x10004330, 'sel4 fn'),
        (0x10003FD0, 0x10004060, 'sel5 fn'),
        (0x10003F90, 0x10004000, 'sel6 fn'),
        (0x10003F10, 0x10003F80, 'sel7 fn'),
        (0x100040C0, 0x10004150, 'sel8 fn'),
        (0x10003D8B, 0x10003DB0, 'sel9 head'),
    ]),
    (sample('driver/NKDSBP2.dll'), [
        (0x100041F3, 0x100041D0 + 0x1C0, 'arms 1..9'),
    ]),
]


def setup(path):
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
    return pe, ib, iat, sec


def rd(pe, sec, va, ln):
    for (lo, hi, praw, sraw, nm) in sec:
        if lo <= va < hi:
            off = praw + (va - lo)
            return pe.__data__[off:off + ln]
    return b''


for path, rs in RANGES:
    pe, ib, iat, sec = setup(path)
    print('=' * 78)
    print(path)
    for lo, hi, label in rs:
        print('-' * 70)
        print('%s  0x%08X..0x%08X' % (label, lo, hi))
        va = lo
        while va < hi:
            one = next(md.disasm(rd(pe, sec, va, 16), va, 1), None)
            if one is None:
                print('0x%08X  .db 0x%02X' % (va, rd(pe, sec, va, 1)[0]))
                va += 1
                continue
            line = '0x%08X  %-7s %s' % (one.address, one.mnemonic, one.op_str)
            for op in one.operands:
                if op.type == 3 and op.mem.base == 0 and op.mem.index == 0 and op.mem.disp in iat:
                    line += '   ; %s' % iat[op.mem.disp]
            print(line)
            va += one.size
            if one.mnemonic == 'ret':
                break
