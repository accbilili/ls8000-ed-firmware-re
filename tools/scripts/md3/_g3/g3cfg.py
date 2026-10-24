"""G3 core: PE load + full-.text recursive-descent CFG (direct call graph).
Read-only on D:\DS\TEST\LS8000\driver\LS8000.md3
Usage: import g3cfg  ->  g3cfg.load()['edges'] etc.
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
import struct, os, pickle, heapq, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

MD3 = sample('driver/LS8000.md3')
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g3cfg.pkl')


def _load_pe():
    data = open(MD3, 'rb').read()
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    nsec = struct.unpack_from('<H', data, pe + 6)[0]
    optsz = struct.unpack_from('<H', data, pe + 20)[0]
    base = struct.unpack_from('<I', data, pe + 24 + 28)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + optsz + i * 40
        name = data[o:o + 8].rstrip(b'\0').decode('latin1')
        vsize, va, rsize, roff = struct.unpack_from('<IIII', data, o + 8)
        secs.append(dict(name=name, vsize=vsize, va=base + va, rsize=rsize, roff=roff))
    return data, base, secs


DATA, IMAGEBASE, SECS = _load_pe()
TEXT = [s for s in SECS if s['name'] == '.text'][0]
RDATA = [s for s in SECS if s['name'] == '.rdata'][0]
DATASEC = [s for s in SECS if s['name'] == '.data'][0]
TLO, THI = TEXT['va'], TEXT['va'] + TEXT['vsize']
TSIZE = TEXT['vsize']
RLO, RHI = RDATA['va'], RDATA['va'] + RDATA['vsize']

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL


def sec_of(va):
    for s in SECS:
        if s['va'] <= va < s['va'] + max(s['vsize'], s['rsize']):
            return s
    return None


def read(va, n):
    s = sec_of(va)
    if not s:
        return b''
    off = va - s['va']
    if off + n > s['rsize']:
        return b''
    return DATA[s['roff'] + off: s['roff'] + off + n]


def rd32(va):
    b = read(va, 4)
    return struct.unpack('<I', b)[0] if len(b) == 4 else None


def in_text(va):
    return TLO <= va < THI


def in_rdata(va):
    return RLO <= va < RHI


def exports():
    e_lfanew = struct.unpack_from('<I', DATA, 0x3C)[0]
    opt = e_lfanew + 24
    ddir = opt + 96
    rva = struct.unpack_from('<I', DATA, ddir)[0]
    if rva == 0:
        return []
    base = IMAGEBASE + rva
    nfun, nname, afun, aname, aord = struct.unpack('<IIIII', read(base + 20, 20))
    out = []
    for i in range(nname):
        nrva = rd32(IMAGEBASE + aname + 4 * i)
        nm = read(IMAGEBASE + nrva, 64).split(b'\0')[0].decode('latin1')
        ov = struct.unpack('<H', read(IMAGEBASE + aord + 2 * i, 2))[0]
        frva = rd32(IMAGEBASE + afun + 4 * ov)
        out.append((nm, IMAGEBASE + frva))
    return out


def sweep_call_targets():
    """Raw sweep for E8 rel32 whose target lands in .text. Cheap, may be noisy."""
    raw = DATA[TEXT['roff']: TEXT['roff'] + TEXT['rsize']]
    n = len(raw)
    out = set()
    i = 0
    while True:
        i = raw.find(b'\xe8', i)
        if i < 0 or i + 5 > n:
            break
        rel = struct.unpack_from('<i', raw, i + 1)[0]
        tgt = TLO + i + 5 + rel
        if TLO <= tgt < THI:
            out.add(tgt)
        i += 1
    return out


def text_jump_tables():
    """.text 内跳转表（FF 24 <SIB scale4> <disp32>）的全部表项。"""
    raw = DATA[TEXT['roff']: TEXT['roff'] + TEXT['rsize']]
    n = len(raw)
    out = set()
    i = 0
    while True:
        i = raw.find(b'\xff\x24', i)
        if i < 0 or i + 7 > n:
            break
        sib = raw[i + 2]
        if (sib >> 6) == 2:
            tab = struct.unpack_from('<I', raw, i + 3)[0]
            if TLO <= tab < THI:
                for k in range(1024):
                    v = rd32(tab + 4 * k)
                    if v is None or not (TLO <= v < THI):
                        break
                    out.add(v)
        i += 1
    return out


def text_ptr_runs(minrun=3):
    """.text 内连续 .text 指针游程（≥minrun）的全部元素（函数指针表/跳转表）。"""
    raw = DATA[TEXT['roff']: TEXT['roff'] + TEXT['rsize']]
    out = set()
    vals = [struct.unpack_from('<I', raw, j)[0] for j in range(0, len(raw) - 3, 4)]
    isp = [TLO <= v < THI for v in vals]
    i = 0
    L = len(vals)
    while i < L:
        if isp[i]:
            j = i
            while j < L and isp[j]:
                j += 1
            if j - i >= minrun:
                out.update(TLO + 4 * k for k in range(i, j))
            i = j
        else:
            i += 1
    return out


def rdata_text_ptrs():
    """All .rdata slots holding a pointer into .text (= vtable entries etc.)."""
    raw = DATA[RDATA['roff']: RDATA['roff'] + RDATA['rsize']]
    out = set()
    for i in range(0, len(raw) - 3, 4):
        v = struct.unpack_from('<I', raw, i)[0]
        if TLO <= v < THI:
            out.add(v)
    return out


def table_targets(tab, cap=512):
    out = []
    for i in range(cap):
        v = rd32(tab + 4 * i)
        if v is None or not in_text(v):
            break
        out.append(v)
    return out


def build(seeds):
    """Recursive descent, seeds processed in ascending address order.
    Returns dict(mark=bytearray, edges=list[(caller,callee)], funcs=sorted list)."""
    work = [(a, a) for a in seeds if in_text(a)]
    heapq.heapify(work)
    mark = bytearray(TSIZE)
    edges = set()
    funcs = set()
    nins = 0
    while work:
        start, own = heapq.heappop(work)
        if start in funcs:
            continue
        funcs.add(start)
        va = start
        while TLO <= va < THI:
            idx = va - TLO
            if mark[idx]:
                break
            mark[idx] = 1
            buf = read(va, 16)
            if len(buf) < 1:
                break
            one = next(md.disasm(buf, va, 1), None)
            if one is None:
                break
            nins += 1
            mn = one.mnemonic
            ops = one.operands
            if mn in ('ret', 'retn', 'int3', 'hlt', 'ud2'):
                break
            if mn == 'jmp':
                if ops and ops[0].type == X86_OP_IMM:
                    t = ops[0].imm & 0xFFFFFFFF
                    if in_text(t):
                        heapq.heappush(work, (t, t))
                elif ops and ops[0].type == X86_OP_MEM:
                    m = ops[0].mem
                    # .text 内跳转表：jmp dword ptr [reg*4 + disp32]
                    if m.index and m.scale == 4 and not m.base:
                        for x in table_targets(m.disp & 0xFFFFFFFF, 1024):
                            heapq.heappush(work, (x, own))
                break
            if mn == 'call':
                if ops and ops[0].type == X86_OP_IMM:
                    t = ops[0].imm & 0xFFFFFFFF
                    if in_text(t):
                        edges.add((own, t))
                        heapq.heappush(work, (t, t))
                va += one.size
                continue
            if mn[0] == 'j' and ops and ops[0].type == X86_OP_IMM:
                t = ops[0].imm & 0xFFFFFFFF
                if in_text(t):
                    heapq.heappush(work, (t, own))
                va += one.size
                continue
            va += one.size
    return dict(mark=mark, edges=edges, funcs=funcs, nins=nins)


def graph(edges):
    fwd = {}
    rev = {}
    for a, b in edges:
        fwd.setdefault(a, set()).add(b)
        rev.setdefault(b, set()).add(a)
    return fwd, rev


def save(obj, path=CACHE):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, 2)


def load(path=CACHE, rebuild=False):
    if os.path.exists(path) and not rebuild:
        with open(path, 'rb') as f:
            return pickle.load(f)
    ex = [va for _, va in exports()]
    sw = sorted(sweep_call_targets())
    rp = sorted(rdata_text_ptrs())
    tj = sorted(text_jump_tables())
    tr = sorted(text_ptr_runs())
    seeds = set(ex) | set(sw) | set(rp) | set(tj) | set(tr)
    sys.stderr.write('seeds: exports=%d sweep=%d rdata=%d textjt=%d textrun=%d union=%d\n' %
                     (len(ex), len(sw), len(rp), len(tj), len(tr), len(seeds)))
    r = build(seeds)
    r['seeds'] = len(seeds)
    r['edges'] = sorted(r['edges'])
    r['funcs'] = sorted(r['funcs'])
    save(r, path)
    return r


if __name__ == '__main__':
    r = load(rebuild=True)
    print('funcs=%d edges=%d insns=%d' % (len(r['funcs']), len(r['edges']), r['nins']))
    covered = sum(r['mark'])
    print('instruction start bytes marked: %d / %d (%.1f%%)' %
          (covered, TSIZE, 100.0 * covered / TSIZE))
