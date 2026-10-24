"""核实 NKDSBP2.dll 的 DeviceIoControl 调用：ioctl 码、结构体布局、缓冲区来源。"""
import struct

from capstone import CS_ARCH_X86, CS_MODE_32, Cs

P = r'C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\NKDSBP2.dll'
d = open(P, 'rb').read()

pe = struct.unpack_from('<I', d, 0x3C)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
optsz = struct.unpack_from('<H', d, pe + 20)[0]
base = struct.unpack_from('<I', d, pe + 24 + 28)[0]
secs = []
so = pe + 24 + optsz
for i in range(nsec):
    nm = d[so + i * 40: so + i * 40 + 8].rstrip(b'\x00').decode('latin1')
    vs, va, rs, ra = struct.unpack_from('<IIII', d, so + i * 40 + 8)
    secs.append((nm, va, vs, ra, rs))


def r2o(rva):
    for nm, v, vs, ra, rs in secs:
        if v <= rva < v + max(vs, rs):
            return ra + (rva - v)
    return None


def dis(va_start, va_end):
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    o = r2o(va_start - base)
    for ins in md.disasm(d[o:o + (va_end - va_start) + 32], va_start):
        if ins.address > va_end:
            break
        print('0x%08X  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))


# ---- 导出表（data directory 索引 0）----
ddoff = pe + 24 + (96 if struct.unpack_from('<H', d, pe + 24)[0] == 0x10b else 112)
erva, esz = struct.unpack_from('<II', d, ddoff)
print('导出目录 RVA = 0x%08X  size = 0x%X' % (erva, esz))
if erva:
    o = r2o(erva)
    (chars, ts, mv, nv, name_rva, base_ord, nfunc, nnames, af, an, ao) = \
        struct.unpack_from('<IIHHIIIIIII', d, o)
    dllname = d[r2o(name_rva):d.index(b'\x00', r2o(name_rva))].decode('latin1')
    print('  DLL 名: %s   导出函数数 %d  导出名数 %d' % (dllname, nfunc, nnames))
    no = r2o(an)
    oo = r2o(ao)
    for i in range(min(nnames, 60)):
        nr = struct.unpack_from('<I', d, no + 4 * i)[0]
        nm = d[r2o(nr):d.index(b'\x00', r2o(nr))].decode('latin1')
        ordi = struct.unpack_from('<H', d, oo + 2 * i)[0]
        fr = struct.unpack_from('<I', d, r2o(af) + 4 * ordi)[0]
        print('    [%3d] 0x%08X  %s' % (ordi, base + fr, nm))

print()
print('=== DeviceIoControl 调用点 0x10002B40–0x10002BB0 ===')
dis(0x10002B40, 0x10002BB0)

print()
print('=== 0x10002B20 附近（CreateFileA 包装）===')
dis(0x10002B10, 0x10002B48)
