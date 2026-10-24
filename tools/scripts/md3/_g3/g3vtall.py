"""G3: 全 .rdata vtable 枚举 + 反向索引（slot -> (vt,idx)）+ 虚调用站点索引。"""
import os, sys, json, pickle, struct, collections, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3cfg as G
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'g3vtall.pkl')


def vtc_from_ctor_writes(mark, mincontig=2):
    """VTC = 被 .text 里 `mov dword ptr [r+d], imm32` 写入的 .rdata 地址（vt/数据指针候选）。
    只统计指令对齐位置（g3cfg mark）。返回按地址排序的候选集合。"""
    lo = G.TLO
    cand = set()
    for i in range(len(mark)):
        if not mark[i]:
            continue
        va = lo + i
        buf = G.read(va, 16)
        one = next(md.disasm(buf, va, 1), None) if buf else None
        if one is None:
            continue
        if one.mnemonic != 'mov' or len(one.operands) != 2:
            continue
        d, s = one.operands
        if d.type != X86_OP_MEM or s.type != X86_OP_IMM or d.size != 4:
            continue
        imm = s.imm & 0xFFFFFFFF
        if G.in_rdata(imm):
            cand.add(imm)
    return sorted(cand)


def contig_len(vt, cap=200):
    n = 0
    while n < cap:
        v = G.rd32(vt + 4 * n)
        if v is None or not G.in_text(v):
            break
        n += 1
    return n


def all_vtables(mark, minslots=2):
    """vtable 枚举：以 ctor 写入地址为候选基址，长度截断到「下一个候选基址」处。
    这样相邻 vtable（.rdata 里连续排布）不会被错误合并。"""
    cand = vtc_from_ctor_writes(mark)
    out = []
    for k, vt in enumerate(cand):
        cl = contig_len(vt)
        if cl < minslots:
            continue
        nxt = cand[k + 1] if k + 1 < len(cand) else None
        lim = (nxt - vt) // 4 if nxt else cl
        n = cl if lim <= 0 else min(cl, lim)
        if n < minslots:
            continue
        out.append((vt, [G.rd32(vt + 4 * i) for i in range(n)]))
    return out


def scan_virtual_sites(funcs, mark=None, maxins=3000, maxbytes=12000):
    """对每个函数收集：直接调用 + 虚调用站点 disp + 构造的 vtable。
    只用 g3cfg 遍历的 insn 起始位置做顺序解码（保证对齐）。"""
    res = {}
    lo = G.TLO
    addrs = []
    for i, b in enumerate(mark):
        if b:
            addrs.append(lo + i)
    # 归属
    own = {}
    for a in addrs:
        pass
    idx = {}
    for k, f in enumerate(funcs):
        idx[f] = k
    # 逐函数解码：从 funcs 出发顺序解码到终止
    for f in funcs:
        cur = f
        vcalls = []
        dcalls = []
        n = 0
        while G.in_text(cur) and n < maxins:
            buf = G.read(cur, 16)
            one = next(md.disasm(buf, cur, 1), None) if buf else None
            if one is None:
                break
            n += 1
            mn = one.mnemonic
            ops = one.operands
            if mn in ('call', 'jmp') and ops:
                if mn == 'call' and ops[0].type == X86_OP_IMM:
                    dcalls.append(ops[0].imm & 0xFFFFFFFF)
                elif ops[0].type == X86_OP_MEM:
                    m = ops[0].mem
                    if not m.index and m.base and not m.disp:
                        vcalls.append(('R', m.base))
                    elif not m.index and m.base:
                        vcalls.append(('D', m.disp & 0xFFFFFFFF))
                    elif m.index and m.scale == 4:
                        vcalls.append(('T', m.disp & 0xFFFFFFFF))
            if mn in ('ret', 'retn', 'int3', 'hlt', 'ud2'):
                break
            if mn == 'jmp' and ops and ops[0].type == X86_OP_IMM:
                break
            cur += one.size
        res[f] = dict(dc=dcalls, vc=vcalls, nins=n)
    return res


def build():
    r = G.load()
    vts = all_vtables(r['mark'])
    slot_index = collections.defaultdict(list)   # func -> [(vt, idx)]
    for vta, slots in vts:
        for i, f in enumerate(slots):
            slot_index[f].append((vta, i))
    sites = scan_virtual_sites(r['funcs'], r['mark'])
    obj = dict(vts=vts, slot_index=dict(slot_index), sites=sites)
    with open(CACHE, 'wb') as fh:
        pickle.dump(obj, fh, 2)
    return obj


def load():
    if os.path.exists(CACHE):
        with open(CACHE, 'rb') as f:
            return pickle.load(f)
    return build()


if __name__ == '__main__':
    o = load()
    print('vtables:', len(o['vts']))
    ln = collections.Counter(len(s) for _, s in o['vts'])
    print('slot-length histogram (top):', sorted(ln.items())[:12])
    print('functions with a vtable slot:', len(o['slot_index']))
    nvc = sum(1 for v in o['sites'].values() if v['vc'])
    print('functions with virtual call sites: %d / %d' % (nvc, len(o['sites'])))
    dispc = collections.Counter()
    for v in o['sites'].values():
        for k, d in v['vc']:
            if k in ('D',):
                dispc[d] += 1
    print('top virtual disp:', ['0x%X:%d' % (d, c) for d, c in dispc.most_common(15)])
