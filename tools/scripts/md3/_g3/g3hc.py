"""G3: 固件 0x03E390 的 85 个 host_code 在 LS8000.md3 中的命中普查。
- 文本段：按 g3cfg 遍历得到的指令边界逐条解码（对齐可靠），按立即数比对
- 数据段：.rdata/.data 的 u16 字面扫描（含任意对齐）
输出 _g3/hc_hits.json + hc_hits.txt
"""
import os, sys, json, struct, collections, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3cfg as G
import g3imm as I
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
HERE = os.path.dirname(os.path.abspath(__file__))

HC = I.host_codes()
HCSET = set(h for h, _ in HC)


def main():
    r = G.load()
    funcs = r['funcs']
    mark = r['mark']
    lo = G.TLO
    hits = []
    nins = 0
    for i in range(len(mark)):
        if not mark[i]:
            continue
        va = lo + i
        buf = G.read(va, 16)
        if not buf:
            continue
        one = next(md.disasm(buf, va, 1), None)
        if one is None:
            continue
        nins += 1
        for op in one.operands:
            if op.type != X86_OP_IMM:
                continue
            v = op.imm & 0xFFFFFFFF
            if v in HCSET:
                k = bisect.bisect_right(funcs, va) - 1
                hits.append(dict(a='0x%08X' % va, m=one.mnemonic, o=one.op_str,
                                 v='0x%04X' % v, sz=one.size, b=one.bytes.hex(),
                                 fn='0x%08X' % funcs[k] if k >= 0 else None))
    print('decoded insns (aligned traversal):', nins)
    print('raw immediate hits:', len(hits))
    byval = collections.Counter(h['v'] for h in hits)
    print('distinct host_code values hit: %d / 85' % len(byval))
    # 形态分类
    form = collections.Counter()
    for h in hits:
        m = h['m']
        o = h['o']
        if m == 'push':
            f = 'push'
        elif m == 'cmp':
            f = 'cmp'
        elif m == 'mov' and 'word ptr' in o:
            f = 'mov_word'
        elif m == 'mov':
            f = 'mov_imm'
        elif m == 'add' or m == 'sub':
            f = 'arith'
        elif m == 'imul' or m == 'shl' or m == 'and' or m == 'or' or m == 'xor':
            f = 'bitop'
        else:
            f = m
        form[f] += 1
    print('forms:', dict(form))
    # 数据段
    dh = []
    for secname in ('.rdata', '.data', '.rsrc'):
        ss = [x for x in G.SECS if x['name'] == secname]
        if not ss:
            continue
        s = ss[0]
        raw = G.DATA[s['roff']: s['roff'] + s['rsize']]
        for j in range(len(raw) - 1):
            v = struct.unpack_from('<H', raw, j)[0]
            if v in HCSET:
                dh.append(dict(sec=secname, a='0x%08X' % (s['va'] + j),
                               v='0x%04X' % v, ctx=raw[max(0, j - 4):j + 6].hex()))
    print('data u16 hits:', len(dh))
    dby = collections.Counter(h['v'] for h in dh)
    print('distinct values in data: %d  %s' % (len(dby), sorted(dby)))
    json.dump(dict(nins=nins, hits=hits, data=dh), open(os.path.join(HERE, 'hc_hits.json'), 'w'), indent=0)
    # 明细（按值分组，每值最多 6 条）
    out = ['# host_code 命中明细（md3，%d 条指令，%d 条命中）' % (nins, len(hits)), '']
    for v in sorted(HCSET, key=lambda x: -byval.get('0x%04X' % x, 0)):
        key = '0x%04X' % v
        c = byval.get(key, 0)
        out.append('## %s  命中 %d' % (key, c))
        for h in [x for x in hits if x['v'] == key][:8]:
            out.append('   %s  %-6s %-24s %s   [fn %s]'
                       % (h['a'], h['m'], h['o'], h['b'], h['fn']))
    open(os.path.join(HERE, 'hc_hits.txt'), 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote hc_hits.json / hc_hits.txt')


if __name__ == '__main__':
    main()
