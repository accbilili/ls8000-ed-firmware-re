"""F6 续 v2：用真实 ImageBase 扫 DLL 的 .text，收集所有 call/jmp [abs] 目标并按 IAT 归属。只读 D:\\。"""
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

DLLS = [sample('driver/NKDUSCAN.dll'), sample('driver/NKDSBP2.dll')]


def abs_targets_from(pe, bounds, name):
    ib = pe.OPTIONAL_HEADER.ImageBase
    out = []
    for (lo, hi, praw, sraw, sname) in bounds:
        if sname != name:
            continue
        data = pe.__data__[praw:praw + sraw]
        for ins in md.disasm(data, lo):
            if ins.mnemonic not in ('call', 'jmp'):
                continue
            for op in ins.operands:
                if op.type == 3 and op.mem.base == 0 and op.mem.index == 0 and op.mem.segment == 0:
                    out.append((ins.address, ins.mnemonic, op.mem.disp & 0xFFFFFFFF))
    return out


for path in DLLS:
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
    ])
    ib = pe.OPTIONAL_HEADER.ImageBase
    bounds = []
    for s in pe.sections:
        bounds.append((ib + s.VirtualAddress, ib + s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
                       s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b'\0').decode()))
    iat = {}
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        for imp in entry.imports:
            nm = imp.name.decode() if imp.name else 'ord#%d' % imp.ordinal
            iat.setdefault(imp.address, nm)
    print('=' * 78)
    print('%s  ImageBase 0x%08X' % (path, ib))
    exp = pe.DIRECTORY_ENTRY_EXPORT
    print('  exports: ' + ', '.join('%s=0x%08X' % (s.name.decode(), ib + s.address) for s in exp.symbols))
    res = abs_targets_from(pe, bounds, '.text')
    # 归口 IAT
    named = {}
    for va, mn, tgt in res:
        if tgt in iat:
            named.setdefault(iat[tgt], []).append((va, mn))
    for nm in sorted(named):
        lst = named[nm]
        print('  %-20s %3d: %s' % (nm, len(lst), ', '.join('%s@0x%08X' % (m, v) for v, m in lst[:20])))
    # thunk 表：jmp [iat_slot] 的位置
    thunks = {}
    for va, mn, tgt in res:
        if mn == 'jmp' and tgt in iat:
            thunks[va] = iat[tgt]
    print('  --- jmp thunks (%d) ---' % len(thunks))
    for va, nm in sorted(thunks.items()):
        print('    0x%08X -> %s' % (va, nm))
