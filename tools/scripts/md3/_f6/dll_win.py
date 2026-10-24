"""F6 续 v4：定点区间反汇编 + DLL 选择子跳转表。只读 D:\\。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct, pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

RANGES = [
    (sample('driver/NKDUSCAN.dll'), 0x10003A80, 0x10003C40, 'NKDUSCAN fn@~3B10 (DeviceIoControl 3BBE)'),
    (sample('driver/NKDUSCAN.dll'), 0x10003DC8, 0x10003E30, 'NKDUSCAN NkDriverEntry jump table'),
    (sample('driver/NKDSBP2.dll'), 0x10004358, 0x100043C0, 'NKDSBP2 NkDriverEntry jump table'),
    (sample('driver/NKDSBP2.dll'), 0x10002A80, 0x10002C40, 'NKDSBP2 fn (DeviceIoControl 2B66)'),
    (sample('driver/NKDUSCAN.dll'), 0x10005480, 0x10005580, 'NKDUSCAN fn (DeviceIoControl 54D6)'),
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


cur = None
for path, lo, hi, label in RANGES:
    if cur != path:
        pe, ib, iat, sec = setup(path)
        cur = path
    print('=' * 78)
    print('%s  %s' % (label, path))
    data = rd(pe, sec, lo, hi - lo)
    if b'' == data:
        print('  (no data)')
        continue
    va = lo
    # 若是跳转表区域，先按 dword 打印
    if 'jump table' in label:
        for i in range(0, len(data) - 3, 4):
            t = struct.unpack_from('<I', data, i)[0]
            print('  0x%08X  [%d] -> 0x%08X' % (lo + i, i // 4, t))
        continue
    while va < hi:
        one = next(md.disasm(rd(pe, sec, va, 16), va, 1), None)
        if one is None:
            print('0x%08X  .db 0x%02X' % (va, data[va - lo]))
            va += 1
            continue
        line = '0x%08X  %-7s %s' % (one.address, one.mnemonic, one.op_str)
        for op in one.operands:
            if op.type == 3 and op.mem.base == 0 and op.mem.index == 0 and op.mem.disp in iat:
                line += '   ; %s' % iat[op.mem.disp]
        print(line)
        va += one.size
