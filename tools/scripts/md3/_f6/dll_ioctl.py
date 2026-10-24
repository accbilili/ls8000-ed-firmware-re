"""F6 续：在两个 Nk*.dll 里定位 DeviceIoControl/CreateFileA 的调用点与外层函数，
并从 request(=arg1) 追踪 +0x14/+0x18/+0x1C/+0x20 的读取。只读 D:\\。"""
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

DLLS = [sample('driver/NKDUSCAN.dll'), sample('driver/NKDSBP2.dll')]
WANT = {'DeviceIoControl', 'CreateFileA', 'CreateFileW', 'CloseHandle'}


def load(path):
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
    ])
    return pe


def imports(pe):
    """返回 {slot_va: name}"""
    ib = pe.OPTIONAL_HEADER.ImageBase
    out = {}
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entry.dll.decode()
        for imp in entry.imports:
            nm = imp.name.decode() if imp.name else 'ord#%d' % imp.ordinal
            out[ib + imp.address] = '%s!%s' % (dll, nm)
    return out


def sec_bounds(pe):
    ib = pe.OPTIONAL_HEADER.ImageBase
    b = []
    for s in pe.sections:
        b.append((ib + s.VirtualAddress, ib + s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
                  s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b'\0').decode()))
    return b


def readva(pe, bounds, va, ln):
    ib = pe.OPTIONAL_HEADER.ImageBase
    for (lo, hi, praw, sraw, nm) in bounds:
        if lo <= va < hi:
            off = praw + (va - lo)
            return pe.__data__[off:off + ln]
    return b''


for path in DLLS:
    pe = load(path)
    ib = pe.OPTIONAL_HEADER.ImageBase
    bounds = sec_bounds(pe)
    imps = imports(pe)
    # 反查 name -> slot
    wanted = {v.split('!')[1]: k for k, v in imps.items() if v.split('!')[1] in WANT}
    print('=' * 76)
    print(path)
    print('  imports of interest:', {hex(k): n for n, k in wanted.items()})

    # 扫 .text 找 call [slot]
    for nm, slot in wanted.items():
        hits = []
        for (lo, hi, praw, sraw, sname) in bounds:
            if sname not in ('.text',):
                continue
            data = pe.__data__[praw:praw + sraw]
            va = lo
            for ins in md.disasm(data, lo):
                if ins.mnemonic != 'call':
                    continue
                for op in ins.operands:
                    if op.type == 3 and op.mem.base == 0 and op.mem.index == 0 and \
                       op.mem.disp == slot and op.mem.segment == 0:
                        hits.append(ins.address)
        print('  %-16s %d call site(s): %s' % (nm, len(hits),
              ', '.join('0x%08X' % h for h in hits[:24])))
