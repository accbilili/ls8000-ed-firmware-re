"""md3 反汇编基础设施：PE 装载 + capstone 反汇编 + 函数范围扫描。"""
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
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OP_IMM, CS_OP_MEM, CS_OP_REG

PATH = sample('driver/LS8000.md3')
IMAGEBASE = 0x10000000

_pe = pefile.PE(PATH, fast_load=True)
_pe.parse_data_directories(directories=[])

def rva2off(rva):
    for s in _pe.sections:
        va = s.VirtualAddress
        if va <= rva < va + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return rva - va + s.PointerToRawData
    return None

def va2off(va):
    return rva2off(va - IMAGEBASE)

_data = open(PATH, 'rb').read()

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

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = 0  # intel

def disasm(va, count=1, stop_at_ret=True, max_bytes=20000):
    """从 va 线性反汇编 count 条指令。"""
    code = read(va, max_bytes)
    out = []
    n = 0
    for ins in md.disasm(code, va):
        out.append(ins)
        n += 1
        if count and n >= count:
            break
    return out

def fmt(ins):
    return '%08X  %-24s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str)

def show(va, count=40):
    for i in disasm(va, count):
        print(fmt(i))

def find_bytes(pat, start_va=0x10001000, end_va=0x100EB000):
    res = []
    o1, o2 = va2off(start_va), va2off(end_va)
    if o1 is None: o1 = 0
    if o2 is None: o2 = len(_data)
    idx = o1
    while True:
        i = _data.find(pat, idx, o2)
        if i < 0:
            break
        # 反算 VA
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
    try:
        return b.decode('latin1')
    except Exception:
        return repr(b)
