"""检查兄弟模块 NKDUSCAN.dll / NKDSBP2.dll 的导出与导入，判定调用方向。只读。"""
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

for p in [sample('driver/NKDUSCAN.dll'),
          sample('driver/NKDSBP2.dll'),
          sample('driver/ICEDLL.dll')]:
    pe = pefile.PE(p, fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
    ])
    print('=' * 70)
    print(p)
    print('ImageBase 0x%08X  EP 0x%08X  sections %d' % (
        pe.OPTIONAL_HEADER.ImageBase, pe.OPTIONAL_HEADER.AddressOfEntryPoint, len(pe.sections)))
    ts = pe.FILE_HEADER.TimeDateStamp
    print('TimeDateStamp 0x%08X' % ts)
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        e = pe.DIRECTORY_ENTRY_EXPORT
        print('DLL name:', e.name.decode() if e.name else None)
        for s in e.symbols:
            print('  EXP 0x%08X %s' % (s.address, s.name.decode() if s.name else 'ord#%d' % s.ordinal))
    print('IMPORTS:')
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            print('  [%s]' % entry.dll.decode())
            for imp in entry.imports:
                print('     %s' % (imp.name.decode() if imp.name else 'ord#%d' % imp.ordinal))
    # 字符串里提到 md3 / NkCtrl 的地方
    data = open(p, 'rb').read()
    for kw in (b'LS8000', b'.md3', b'NkCtrlEntry', b'MAIDEntryPoint', b'NkMDCtrlEntry'):
        idx = data.find(kw)
        print('  str %-14s %s' % (kw.decode(), 'found@0x%X' % idx if idx >= 0 else 'absent'))
