import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct

A = open(sample('driver/LS8000.md3'), 'rb').read()
B = open(r'C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\LS8000.md3', 'rb').read()

pe = struct.unpack_from('<I', A, 0x3C)[0]
print('PE signature offset = 0x%X  sig=%s' % (pe, A[pe:pe + 4]))

nsec = struct.unpack_from('<H', A, pe + 6)[0]
optsz = struct.unpack_from('<H', A, pe + 20)[0]
opt = pe + 24
magic = struct.unpack_from('<H', A, opt)[0]
print('OptionalHeader @0x%X  magic=0x%04X (%s)  size=%d' % (opt, magic, 'PE32' if magic == 0x10b else 'PE32+', optsz))

FIELDS = [
    (0x00, 2, 'Magic'), (0x02, 1, 'MajorLinkerVersion'), (0x03, 1, 'MinorLinkerVersion'),
    (0x04, 4, 'SizeOfCode'), (0x08, 4, 'SizeOfInitializedData'), (0x0C, 4, 'SizeOfUninitializedData'),
    (0x10, 4, 'AddressOfEntryPoint'), (0x14, 4, 'BaseOfCode'), (0x18, 4, 'BaseOfData'),
    (0x1C, 4, 'ImageBase'), (0x20, 4, 'SectionAlignment'), (0x24, 4, 'FileAlignment'),
    (0x28, 2, 'MajorOperatingSystemVersion'), (0x2A, 2, 'MinorOperatingSystemVersion'),
    (0x2C, 2, 'MajorImageVersion'), (0x2E, 2, 'MinorImageVersion'),
    (0x30, 2, 'MajorSubsystemVersion'), (0x32, 2, 'MinorSubsystemVersion'),
    (0x34, 4, 'Win32VersionValue'), (0x38, 4, 'SizeOfImage'), (0x3C, 4, 'SizeOfHeaders'),
    (0x40, 4, 'CheckSum'), (0x44, 2, 'Subsystem'), (0x46, 2, 'DllCharacteristics'),
    (0x48, 4, 'SizeOfStackReserve'), (0x4C, 4, 'SizeOfStackCommit'),
    (0x50, 4, 'SizeOfHeapReserve'), (0x54, 4, 'SizeOfHeapCommit'),
    (0x58, 4, 'LoaderFlags'), (0x5C, 4, 'NumberOfRvaAndSizes'),
]
print()
print('=== 偏移 0x184 落在哪个字段 ===')
for off, sz, nm in FIELDS:
    if opt + off <= 0x184 < opt + off + sz:
        rel = 0x184 - (opt + off)
        print('  -> %s (+%d, %d B)  字段绝对范围 0x%X–0x%X' % (nm, rel, sz, opt + off, opt + off + sz - 1))
        if sz == 2:
            print('     原版值 = 0x%04X   补丁值 = 0x%04X' % (
                struct.unpack_from('<H', A, 0x184)[0], struct.unpack_from('<H', B, 0x184)[0]))
        elif sz == 4:
            print('     原版值 = 0x%08X   补丁值 = 0x%08X' % (
                struct.unpack_from('<I', A, 0x184)[0], struct.unpack_from('<I', B, 0x184)[0]))

print()
print('=== 按节的差异统计 ===')
secs = []
so = opt + optsz
for i in range(nsec):
    nm = A[so + i * 40: so + i * 40 + 8].rstrip(b'\x00').decode('latin1')
    vs, va, rs, ra = struct.unpack_from('<IIII', A, so + i * 40 + 8)
    secs.append((nm, ra, rs))
secs.append(('PE头/对齐填充', 0, 0x1000))

for nm, ra, rs in secs:
    lo = ra
    hi = ra + rs
    d = sum(1 for i in range(len(A)) if lo <= i < hi and A[i] != B[i])
    tot = sum(1 for i in range(len(A)) if lo <= i < hi)
    flag = '  ★ 有差异' if d else ''
    print('  %-14s 0x%06X–0x%06X  %7d B  差异 %6d%s' % (nm, lo, hi, tot, d, flag))

print()
print('=== .text 逐字节校验 ===')
tlo, thi = 0x1000, 0x1000 + 0xBD000
d = [i for i in range(len(A)) if tlo <= i < thi and A[i] != B[i]]
print('  .text 区差异字节数 = %d  →  %s' % (len(d), '完全一致，我分析的代码就是设备运行的代码' if not d else '存在差异！'))
