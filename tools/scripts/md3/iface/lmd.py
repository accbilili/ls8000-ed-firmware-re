"""接口组私有反汇编库（不与并行子任务共享文件名）。"""
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
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

PATH = sample('driver/LS8000.md3')
IMAGEBASE = 0x10000000

_pe = pefile.PE(PATH, fast_load=True)
_data = open(PATH, 'rb').read()

def va2off(va):
    rva = va - IMAGEBASE
    for s in _pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            o = rva - s.VirtualAddress + s.PointerToRawData
            return o if 0 <= o < len(_data) else None
    return None

def read(va, n):
    o = va2off(va)
    if o is None:
        return b''
    return _data[o:o + n]

def u32(va):
    b = read(va, 4)
    return int.from_bytes(b, 'little') if len(b) == 4 else None

def u16(va):
    b = read(va, 2)
    return int.from_bytes(b, 'little') if len(b) == 2 else None

_md = Cs(CS_ARCH_X86, CS_MODE_32)
_md.detail = True
_md.syntax = 0

def dis(va, count=1, maxb=40000):
    out = []
    for ins in _md.disasm(read(va, maxb), va):
        out.append(ins)
        if count and len(out) >= count:
            break
    return out

def f(ins):
    return '%08X  %-22s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str)

def show(va, count=40):
    for i in dis(va, count):
        print(f(i))

def find_imm(val, lo=0x10001000, hi=0x100BE000):
    """在 .text 中搜 32 位立即数/地址。"""
    import struct
    pat = struct.pack('<I', val)
    res = []
    o1, o2 = va2off(lo), va2off(hi)
    idx = o1
    while True:
        i = _data.find(pat, idx, o2)
        if i < 0:
            break
        for s in _pe.sections:
            if s.PointerToRawData <= i < s.PointerToRawData + s.SizeOfRawData:
                res.append(IMAGEBASE + s.VirtualAddress + (i - s.PointerToRawData))
                break
        idx = i + 1
    return res

def cstr(va, maxlen=200):
    b = read(va, maxlen)
    z = b.find(b'\x00')
    if z >= 0:
        b = b[:z]
    return b.decode('latin1', 'replace')

def callers_of(target):
    """粗搜 E8 rel32 调用 target 的位置。"""
    res = []
    lo, hi = 0x10001000, 0x100BE000
    o1, o2 = va2off(lo), va2off(hi)
    for i in range(o1, o2 - 5):
        if _data[i] == 0xE8:
            rel = int.from_bytes(_data[i + 1:i + 5], 'little', signed=True)
            src = IMAGEBASE + _pe.sections[0].VirtualAddress + (i - _pe.sections[0].PointerToRawData) if False else None
            # 计算该字节的 VA
            for s in _pe.sections:
                if s.PointerToRawData <= i < s.PointerToRawData + s.SizeOfRawData:
                    va = IMAGEBASE + s.VirtualAddress + (i - s.PointerToRawData)
                    if va + 5 + rel == target:
                        res.append(va)
                    break
    return res

def ptrs_to(val):
    """在整镜像（含 data/rdata）中找指向 val 的 4 字节指针。"""
    import struct
    pat = struct.pack('<I', val)
    res = []
    idx = 0
    while True:
        i = _data.find(pat, idx)
        if i < 0:
            break
        for s in _pe.sections:
            if s.PointerToRawData <= i < s.PointerToRawData + s.SizeOfRawData:
                res.append(IMAGEBASE + s.VirtualAddress + (i - s.PointerToRawData))
                break
        idx = i + 1
    return res

_cache = None

def iter_all(lo=0x10001000, hi=0x100BE000):
    """带重同步的全 .text 线性扫描（结果缓存）。"""
    global _cache
    if _cache is not None and _cache[0] == (lo, hi):
        return _cache[1]
    code = read(lo, hi - lo)
    out = []
    off = 0
    n = len(code)
    while off < n:
        got = False
        for ins in _md.disasm(code[off:off + 16], lo + off):
            out.append(ins)
            off += ins.size
            got = True
            break
        if not got:
            off += 1
    _cache = ((lo, hi), out)
    return out

def find_bytes(pat, lo=0x10001000, hi=0x100EB000):
    res = []
    o1, o2 = va2off(lo), va2off(hi)
    if o1 is None:
        o1 = 0
    if o2 is None:
        o2 = len(_data)
    idx = o1
    while True:
        i = _data.find(pat, idx, o2)
        if i < 0:
            break
        for s in _pe.sections:
            if s.PointerToRawData <= i < s.PointerToRawData + s.SizeOfRawData:
                res.append(IMAGEBASE + s.VirtualAddress + (i - s.PointerToRawData))
                break
        idx = i + 1
    return res
