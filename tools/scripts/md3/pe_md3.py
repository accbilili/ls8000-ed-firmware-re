"""Minimal PE32 reader for LS8000.md3 (read-only)."""
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

PATH = sample('driver/LS8000.md3')


class PE:
    def __init__(self, path=PATH):
        self.data = open(path, 'rb').read()
        d = self.data
        e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
        assert d[e_lfanew:e_lfanew + 4] == b'PE\0\0'
        coff = e_lfanew + 4
        self.machine, self.nsec = struct.unpack_from('<HH', d, coff)
        optsz = struct.unpack_from('<H', d, coff + 16)[0]
        opt = coff + 20
        self.imagebase = struct.unpack_from('<I', d, opt + 28)[0]
        self.entry = self.imagebase + struct.unpack_from('<I', d, opt + 16)[0]
        self.ddir_rva = opt + 96
        self.sections = []
        s = opt + optsz
        for i in range(self.nsec):
            name = d[s:s + 8].rstrip(b'\0').decode('latin1')
            vsize, va, rawsize, rawptr = struct.unpack_from('<IIII', d, s + 8)
            self.sections.append(dict(name=name, va=self.imagebase + va, vsize=vsize,
                                      rawptr=rawptr, rawsize=rawsize))
            s += 40

    def sec_of(self, va):
        for s in self.sections:
            if s['va'] <= va < s['va'] + (s['vsize'] or s['rawsize']):
                return s
        return None

    def read(self, va, n):
        s = self.sec_of(va)
        if s is None:
            return None
        delta = va - s['va']
        if delta + n > s['rawsize']:
            return None
        off = s['rawptr'] + delta
        if off + n > len(self.data):
            return None
        return self.data[off:off + n]

    def u16(self, va):
        b = self.read(va, 2)
        return None if b is None or len(b) < 2 else struct.unpack('<H', b)[0]

    def u32(self, va):
        b = self.read(va, 4)
        return None if b is None or len(b) < 4 else struct.unpack('<I', b)[0]

    def exports(self):
        rva, size = struct.unpack_from('<II', self.data, self.ddir_rva)
        if rva == 0:
            return []
        base = self.imagebase + rva
        nfun, nname, afun, aname, aord = struct.unpack('<IIIII', self.read(base + 20, 20))
        out = []
        for i in range(nname):
            nrva = self.u32(self.imagebase + aname + 4 * i)
            name = self.read(self.imagebase + nrva, 64).split(b'\0')[0].decode('latin1')
            ordv = self.u16(self.imagebase + aord + 2 * i)
            frva = self.u32(self.imagebase + afun + 4 * ordv)
            out.append((name, self.imagebase + frva, ordv))
        return out


if __name__ == '__main__':
    p = PE()
    print('ImageBase 0x%08X entry 0x%08X' % (p.imagebase, p.entry))
    for s in p.sections:
        print('%-8s va 0x%08X vsize %7d raw 0x%06X size %7d' %
              (s['name'], s['va'], s['vsize'], s['rawptr'], s['rawsize']))
    print('exports:')
    for n, va, o in p.exports():
        print('  %-40s 0x%08X ord %d' % (n, va, o))
