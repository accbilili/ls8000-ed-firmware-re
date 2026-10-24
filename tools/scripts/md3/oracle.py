"""Byte-stepped decode oracle + recursive descent CFG, cached."""
import sys, os, pickle, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md3lib import *
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

_md = Cs(CS_ARCH_X86, CS_MODE_32); _md.detail = True
_cache = {}

def D(va):
    """Decode one instruction at va. None if invalid."""
    if va in _cache: return _cache[va]
    b = read(va, 16)
    r = None
    if b:
        for i in _md.disasm(b, va):
            r = i
            break
    _cache[va] = r
    return r

def _bytes(va, n):
    s = sec_of(va)
    if not s: return b''
    off = va - s['va']
    if off >= s['rsize']: return b''
    return DATA[s['roff']+off: s['roff']+min(off+n, s['rsize'])]

def sweep(lo, hi):
    """Byte-stepped sweep: yields (va, insn). On invalid byte, step 1."""
    a = lo; out = []
    while a < hi:
        i = D(a)
        if i is None or a + i.size > hi:
            a += 1; continue
        out.append(i); a += i.size
    return out

def cfg(entry, maxn=60000):
    seen = {}; work = [entry]; order = []
    while work:
        a = work.pop()
        while True:
            if a in seen: break
            if not (TEXT_LO <= a < TEXT_HI): break
            i = D(a)
            if i is None: break
            seen[a] = i; order.append(a)
            mn = i.mnemonic
            if mn.startswith('ret') or mn in ('int3','hlt','ud2','iretd','iret'):
                break
            ops = i.operands
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
                # fallthrough
            if len(seen) > maxn: break
            a = a + i.size
    return seen

if __name__ == '__main__':
    t0 = time.time()
    ins = sweep(TEXT_LO, TEXT_HI)
    print('sweep %d insns in %.1fs' % (len(ins), time.time()-t0))
    calls = [(i.address, i.operands[0].imm) for i in ins
             if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM
             and TEXT_LO <= i.operands[0].imm < TEXT_HI]
    print('call sites', len(calls), 'unique', len({c[1] for c in calls}))
    pickle.dump(dict(calls=calls), open('calls.pkl','wb'))
