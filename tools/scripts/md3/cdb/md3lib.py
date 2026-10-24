"""md3 PE loader + recursive-descent CFG builder + xref index.
Read-only on D:\DS\TEST\LS8000\driver\LS8000.md3
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct, json, os, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OP_IMM, CS_OP_MEM, CS_OP_REG
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

MD3 = sample('driver/LS8000.md3')

def load():
    data = open(MD3, 'rb').read()
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    nsec = struct.unpack_from('<H', data, pe + 6)[0]
    optsz = struct.unpack_from('<H', data, pe + 20)[0]
    base = struct.unpack_from('<I', data, pe + 24 + 28)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + optsz + i * 40
        name = data[o:o+8].rstrip(b'\0').decode('latin1')
        vsize, va, rsize, roff = struct.unpack_from('<IIII', data, o + 8)
        chars = struct.unpack_from('<I', data, o + 36)[0]
        secs.append(dict(name=name, vsize=vsize, va=base+va, rsize=rsize, roff=roff, chars=chars))
    return data, base, secs

DATA, IMAGEBASE, SECS = load()

def sec_of(va):
    for s in SECS:
        if s['va'] <= va < s['va'] + max(s['vsize'], s['rsize']):
            return s
    return None

def read(va, n):
    s = sec_of(va)
    if not s: return None
    off = va - s['va']
    if off >= s['rsize']: return None
    return DATA[s['roff']+off: s['roff']+off+n]

TEXT = [s for s in SECS if s['name'] == '.text'][0]
TEXT_LO = TEXT['va']
TEXT_HI = TEXT['va'] + TEXT['vsize']

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

def insns(va, count=1):
    b = read(va, 16 * count)
    if not b: return []
    out = []
    for i in md.disasm(b, va):
        out.append(i)
        if len(out) >= count: break
    return out

def text_bytes():
    return DATA[TEXT['roff']: TEXT['roff']+TEXT['vsize']]

if __name__ == '__main__':
    print('ImageBase 0x%08X' % IMAGEBASE)
    for s in SECS:
        print('%-10s va=0x%08X vsize=%7d rsize=%7d roff=0x%06X chars=0x%08X'
              % (s['name'], s['va'], s['vsize'], s['rsize'], s['roff'], s['chars']))
