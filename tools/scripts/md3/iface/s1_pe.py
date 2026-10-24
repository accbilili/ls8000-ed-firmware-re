"""md3 PE 基础信息：节、导出、导入。只读 D:\，输出到 stdout（重定向由调用方控制）。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import pefile, sys, hashlib

p = sample('driver/LS8000.md3')
pe = pefile.PE(p, fast_load=True)
pe.parse_data_directories(directories=[
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE'],
])

print('ImageBase 0x%08X  EntryPoint 0x%08X  Machine 0x%04X' % (
    pe.OPTIONAL_HEADER.ImageBase, pe.OPTIONAL_HEADER.AddressOfEntryPoint, pe.FILE_HEADER.Machine))
print('Subsystem %d  DllCharacteristics 0x%04X' % (
    pe.OPTIONAL_HEADER.Subsystem, pe.OPTIONAL_HEADER.DllCharacteristics))
print('SizeOfImage 0x%X' % pe.OPTIONAL_HEADER.SizeOfImage)
print('--- sections ---')
for s in pe.sections:
    nm = s.Name.rstrip(b'\x00').decode('latin1')
    print('%-10s VA 0x%08X vsize 0x%-8X raw 0x%-8X rsize 0x%-8X flags 0x%08X' % (
        nm, pe.OPTIONAL_HEADER.ImageBase + s.VirtualAddress, s.Misc_VirtualSize,
        s.PointerToRawData, s.SizeOfRawData, s.Characteristics))

print('--- exports ---')
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    e = pe.DIRECTORY_ENTRY_EXPORT
    print('DLL name:', e.name.decode() if e.name else None, 'base ordinal', e.struct.Base)
    for s in e.symbols:
        print('  ord %-4d VA 0x%08X  %s' % (s.ordinal, s.address, s.name.decode() if s.name else '(noname)'))
else:
    print('  none')

print('--- imports ---')
def dump(entries):
    for entry in entries:
        print('DLL:', entry.dll.decode())
        for imp in entry.imports:
            print('    VA 0x%08X  %s' % (imp.address, imp.name.decode() if imp.name else 'ord#%d' % imp.ordinal))

if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    dump(pe.DIRECTORY_ENTRY_IMPORT)
if hasattr(pe, 'DIRECTORY_ENTRY_DELAY_IMPORT'):
    print('--- delay imports ---')
    dump(pe.DIRECTORY_ENTRY_DELAY_IMPORT)

print('--- resources ---')
if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        print('  type', t.id, t.name)
        if hasattr(t, 'directory'):
            for n in t.directory.entries:
                if hasattr(n, 'directory'):
                    for l in n.directory.entries:
                        print('    name/id', n.id, 'lang', l.id, 'size', l.data.struct.Size)
