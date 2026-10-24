"""G3: 85 个固件 host_code 在 md3 里的命中率普查。
- 线性扫描（100% .text 字节覆盖，含 resync）
- 遍历对齐扫描（g3cfg mark，可归属函数）
- .rdata/.data 的 u16 字面扫描
只写 _g3/ 下的小文件。
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
import struct, sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3cfg as G
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM

ROM = sample('LS8000_111_ROM.bin')
BASE = 0x10000
T390 = 0x03E390

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL


def host_codes():
    d = open(ROM, 'rb').read()
    out = []
    for i in range(200):
        hc, f2 = struct.unpack_from('>HH', d, T390 - BASE + i * 4)
        if hc == 0:
            break
        out.append((hc, f2))
    return out


HC = host_codes()
HCSET = set(h for h, _ in HC)
HCMAP = dict(HC)

# ---------- 1. 线性扫描 .text ----------
raw = G.DATA[G.TEXT['roff']: G.TEXT['roff'] + G.TEXT['rsize']]


def linear_hits():
    """decode from every byte position; keep decoded instrs with imm in HCSET."""
    out = []
    pos = 0
    n = len(raw)
    # 先用 1 字节步进解码，遇到合法指令且立即数命中就记录；仍逐字节步进（保证 100% 位置覆盖）
    i = 0
    while i < n:
        one = next(md.disasm(raw[i:i + 16], G.TLO + i, 1), None)
        if one is not None:
            for op in one.operands:
                if op.type == X86_OP_IMM:
                    v = op.imm & 0xFFFFFFFF
                    if v in HCSET:
                        out.append((one.address, one.mnemonic, one.op_str, v,
                                    one.size, one.bytes.hex()))
        i += 1
    return out


# ---------- 2. 遍历对齐扫描（用 g3cfg 的 mark） ----------
def marked_hits(mark, funcs):
    out = []
    # 归属函数：用有序 funcs 做二分
    import bisect
    lo = G.TLO
    for i, b in enumerate(mark):
        if not b:
            continue
        va = lo + i
        buf = G.read(va, 16)
        one = next(md.disasm(buf, va, 1), None)
        if one is None:
            continue
        for op in one.operands:
            if op.type == X86_OP_IMM:
                v = op.imm & 0xFFFFFFFF
                if v in HCSET:
                    k = bisect.bisect_right(funcs, va) - 1
                    fn = funcs[k] if k >= 0 else None
                    out.append((va, one.mnemonic, one.op_str, v, one.size,
                                one.bytes.hex(), fn))
        # 前进到下一条：依赖下一次循环，这里只逐字节跳
    return out


# ---------- 3. 数据区 u16 扫描 ----------
def data_u16_hits():
    res = []
    for secname in ('.rdata', '.data'):
        s = [x for x in G.SECS if x['name'] == secname][0]
        raw = G.DATA[s['roff']: s['roff'] + s['rsize']]
        for i in range(len(raw) - 1):
            v = struct.unpack_from('<H', raw, i)[0]
            if v in HCSET:
                res.append((secname, s['va'] + i, v,
                            raw[max(0, i - 4):i + 6].hex()))
    return res


if __name__ == '__main__':
    HC = host_codes()
    HCSET = set(h for h, _ in HC)
    print('host_code count:', len(HC))
    lin = linear_hits()
    print('linear hits (all positions):', len(lin))
    # 去重（同一地址只保留一次，线性扫描同地址只出现一次）
    uniq = {}
    for a, m, o, v, sz, hx in lin:
        uniq.setdefault(a, (a, m, o, v, sz, hx))
    print('unique address hits:', len(uniq))
    json.dump([{'a': '0x%08X' % a, 'm': m, 'o': o, 'v': '0x%04X' % v,
                'sz': sz, 'b': hx} for a, m, o, v, sz, hx in uniq.values()],
              open('imm_linear.json', 'w'), indent=0)
    cnt = collections.Counter(v for a, m, o, v, sz, hx in uniq.values())
    print('distinct host_code values hit:', len(cnt))
    for v in sorted(HCSET):
        print('  0x%04X -> %d' % (v, cnt.get(v, 0)))
    dh = data_u16_hits()
    print('data u16 raw hits:', len(dh))
    json.dump([{'sec': s, 'a': '0x%08X' % a, 'v': '0x%04X' % v, 'ctx': c}
               for s, a, v, c in dh], open('imm_data.json', 'w'), indent=0)
    dcnt = collections.Counter(v for s, a, v, c in dh)
    print('distinct host_code values in data:', len(dcnt), sorted('0x%04X' % v for v in dcnt))
