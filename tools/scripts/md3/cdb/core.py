"""Self-contained md3 analysis core (isolated copy: no shared modules)."""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import cfg, sample
import struct, os
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

MD3 = sample('driver/LS8000.md3')
DATA = open(MD3, 'rb').read()
_pe = struct.unpack_from('<I', DATA, 0x3C)[0]
_nsec = struct.unpack_from('<H', DATA, _pe + 6)[0]
_optsz = struct.unpack_from('<H', DATA, _pe + 20)[0]
IMAGEBASE = struct.unpack_from('<I', DATA, _pe + 24 + 28)[0]
SECS = []
for _i in range(_nsec):
    _o = _pe + 24 + _optsz + _i * 40
    _nm = DATA[_o:_o+8].rstrip(b'\0').decode('latin1')
    _vs, _va, _rs, _ro = struct.unpack_from('<IIII', DATA, _o + 8)
    SECS.append(dict(name=_nm, vsize=_vs, va=IMAGEBASE+_va, rsize=_rs, roff=_ro))
TEXT = [s for s in SECS if s['name'] == '.text'][0]
TEXT_LO, TEXT_HI = TEXT['va'], TEXT['va'] + TEXT['vsize']

def sec_of(va):
    for s in SECS:
        if s['va'] <= va < s['va'] + max(s['vsize'], s['rsize']): return s
    return None

def read(va, n):
    s = sec_of(va)
    if not s: return b''
    off = va - s['va']
    if off >= s['rsize']: return b''
    return DATA[s['roff']+off: s['roff']+min(off+n, s['rsize'])]

_md = Cs(CS_ARCH_X86, CS_MODE_32); _md.detail = True
_c = {}
def D(va):
    if va in _c: return _c[va]
    r = None
    b = read(va, 16)
    if b:
        for i in _md.disasm(b, va):
            r = i; break
    _c[va] = r
    return r

def sweep(lo, hi):
    a = lo; out = []
    while a < hi:
        i = D(a)
        if i is None or a + i.size > hi:
            a += 1; continue
        out.append(i); a += i.size
    return out

def cfg(entry, maxn=60000):
    seen = {}; work = [entry]
    while work:
        a = work.pop()
        while True:
            if a in seen or not (TEXT_LO <= a < TEXT_HI): break
            i = D(a)
            if i is None: break
            seen[a] = i
            mn = i.mnemonic; ops = i.operands
            if mn.startswith('ret') or mn in ('int3','hlt','ud2','iretd','iret'): break
            if mn == 'jmp':
                if ops and ops[0].type == X86_OP_IMM: a = ops[0].imm; continue
                break
            if mn.startswith('j') and ops and ops[0].type == X86_OP_IMM:
                t = ops[0].imm
                if TEXT_LO <= t < TEXT_HI: work.append(t)
                a = a + i.size; continue
            if mn == 'call' and ops and ops[0].type == X86_OP_IMM:
                t = ops[0].imm
                if TEXT_LO <= t < TEXT_HI: work.append(t)
            if len(seen) > maxn: break
            a = a + i.size
    return seen
