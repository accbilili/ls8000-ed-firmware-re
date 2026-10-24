"""从 Nikon 传输层 DLL 里挖出：设备路径字符串 + DeviceIoControl 的真实 ioctl 码与参数。"""
import struct

from capstone import CS_ARCH_X86, CS_MODE_32, Cs

FILES = {
    'NKDSBP2': r'C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\NKDSBP2.dll',
    'NKDUSCAN': r'C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\NKDUSCAN.dll',
}
WANT = ('CreateFileA', 'CreateFileW', 'DeviceIoControl', 'WriteFile', 'ReadFile',
        'CloseHandle', 'SetupDiGetClassDevsA', 'SetupDiEnumDeviceInterfaces',
        'SetupDiGetDeviceInstanceIdA', 'CreateServiceA', 'StartServiceA', 'OpenServiceA')


class PE:
    def __init__(self, data):
        d = data
        self.d = d
        self.pe = struct.unpack_from('<I', d, 0x3C)[0]
        self.nsec = struct.unpack_from('<H', d, self.pe + 6)[0]
        self.optsz = struct.unpack_from('<H', d, self.pe + 20)[0]
        self.base = struct.unpack_from('<I', d, self.pe + 24 + 28)[0]
        self.mach = struct.unpack_from('<H', d, self.pe + 24)[0]
        self.secs = []
        so = self.pe + 24 + self.optsz
        for i in range(self.nsec):
            nm = d[so + i * 40: so + i * 40 + 8].rstrip(b'\x00').decode('latin1')
            vs, va, rs, ra = struct.unpack_from('<IIII', d, so + i * 40 + 8)
            self.secs.append({'name': nm, 'rva': va, 'vs': vs, 'ra': ra, 'rs': rs})
        ddoff = self.pe + 24 + (96 if self.mach == 0x10b else 112)
        self.ddoff = ddoff
        self.imports = {}
        self._parse_imports()

    def r2o(self, rva):
        """RVA -> 文件偏移"""
        for s in self.secs:
            if s['rva'] <= rva < s['rva'] + max(s['vs'], s['rs']):
                return s['ra'] + (rva - s['rva'])
        return None

    def va2o(self, va):
        return self.r2o(va - self.base)

    def _parse_imports(self):
        d = self.d
        imp_rva, _sz = struct.unpack_from('<II', d, self.ddoff + 8)
        o = self.r2o(imp_rva)
        if o is None:
            return
        while True:
            oft, ts, fc, nmrva, iat = struct.unpack_from('<IIIII', d, o)
            if not nmrva:
                break
            no = self.r2o(nmrva)
            dll = d[no:d.index(b'\x00', no)].decode('latin1')
            to = self.r2o(oft or iat)
            funcs = []
            while True:
                v = struct.unpack_from('<I', d, to)[0]
                if v == 0:
                    break
                if v & 0x80000000:
                    funcs.append(('ord%d' % (v & 0xFFFF), None))
                else:
                    ho = self.r2o(v)
                    funcs.append((d[ho + 2:d.index(b'\x00', ho + 2)].decode('latin1'), v))
                to += 4
            self.imports[dll] = funcs
            o += 20

    def strings(self, minlen=5):
        out = []
        for s in self.secs:
            blob = self.d[s['ra']: s['ra'] + s['rs']]
            cur = bytearray()
            start = 0
            for i, b in enumerate(blob):
                if 32 <= b < 127:
                    if not cur:
                        start = i
                    cur.append(b)
                else:
                    if len(cur) >= minlen:
                        out.append((s['name'], self.base + s['rva'] + start, bytes(cur)))
                    cur = bytearray()
            if len(cur) >= minlen:
                out.append((s['name'], self.base + s['rva'] + start, bytes(cur)))
        return out


def cstr_at(pe, va):
    o = pe.va2o(va)
    if o is None:
        return None
    end = pe.d.index(b'\x00', o)
    return pe.d[o:end]


def main():
    for tag, path in FILES.items():
        d = open(path, 'rb').read()
        pe = PE(d)
        print('=' * 78)
        print('%s   %d B   ImageBase 0x%08X' % (tag, len(d), pe.base))
        print('=' * 78)
        iat = {}
        for dll, funcs in pe.imports.items():
            keep = [(n, v) for n, v in funcs if n in WANT]
            if keep:
                print('  %-22s %s' % (dll, ', '.join(n for n, _ in keep)))
                for n, v in keep:
                    if v is not None:
                        iat[n] = pe.base + pe.ddoff  # 占位
        # 真正的 IAT 槽地址
        for dll, funcs in pe.imports.items():
            pass
        print()
        print('  --- 关键字符串 ---')
        for sec, va, s in pe.strings(5):
            try:
                t = s.decode('ascii')
            except Exception:
                continue
            if any(k in t for k in ('\\.', 'SBP', '1394', 'USB', 'SCSI', 'Scanner', 'scsi', 'NIKON')):
                print('    %-8s 0x%08X  %r' % (sec, va, t))
        print()


if __name__ == '__main__':
    main()
