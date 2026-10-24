"""F6 续 v3：反汇编含 DeviceIoControl/CreateFileA 调用点的外层函数，追 request 字段。只读 D:\\。"""
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

SITES = {
    sample('driver/NKDUSCAN.dll'): [0x10003BBE, 0x100054D6, 0x1000323E, 0x10003023, 0x10002DA0],
    sample('driver/NKDSBP2.dll'): [0x10002B66],
}


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


def prologue(pe, sec, va, back=0x600):
    """向上找 push ebp / mov ebp,esp 组合"""
    start = max(va - back, sec and sec[0][0] or 0)
    data = rd(pe, sec, start, va - start)
    if not data:
        return va
    best = None
    for ins in md.disasm(data, start):
        if ins.mnemonic == 'push' and ins.op_str == 'ebp':
            cand = ins.address
            nx = rd(pe, sec, ins.address + ins.size, 4)
            try:
                one = next(md.disasm(nx, ins.address + ins.size, 1))
                if one.mnemonic == 'mov' and one.op_str == 'ebp, esp':
                    best = cand
            except StopIteration:
                pass
    return best if best else va


for path, sites in SITES.items():
    pe, ib, iat, sec = setup(path)
    print('=' * 78)
    print(path)
    for site in sites:
        fn = prologue(pe, sec, site)
        end = site + 0x140
        data = rd(pe, sec, fn, end - fn)
        print('-' * 70)
        print('DeviceIoControl @0x%08X  enclosing fn @0x%08X' % (site, fn))
        for ins in md.disasm(data, fn):
            if ins.address > end:
                break
            line = '0x%08X  %-7s %s' % (ins.address, ins.mnemonic, ins.op_str)
            for op in ins.operands:
                if op.type == 3 and op.mem.base == 0 and op.mem.index == 0 and op.mem.disp in iat:
                    line += '   ; %s' % iat[op.mem.disp]
            if ins.address == site:
                line += '   <<<< DeviceIoControl HERE'
            print(line)
