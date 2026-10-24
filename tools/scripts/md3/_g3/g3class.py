"""G3 主分析：268 能力 ID → 出口归类 + host_code 命中率 + E0 payload。
输出 json/txt 到 _g3/，供 cap_to_cdb.md 引用。"""
import os, sys, json, collections, bisect, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3cfg as G
import g3vt as V
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

# ---------- 锚点 ----------
CDB_SITES = json.load(open(os.path.join(ROOT, 'cdb_sites.json')))
BUILD_FUNCS = set(int(x['func'], 16) for x in CDB_SITES if x['func'])
# 每条命令的构造函数（cdb_sites.md §1 ctor 列）
CDB_CTORS = set()
for x in CDB_SITES:
    pass
CDB_CTORS = {0x1009FD20, 0x1009FE80, 0x1009FEC0, 0x1009FD60, 0x100A0020, 0x1009FF10,
             0x1009FDE0, 0x100A0120, 0x1009FD40, 0x1009FF50, 0x1009FFE0, 0x1009FF90,
             0x100AAB30, 0x100AAB90, 0x100AABF0, 0x100AAC90, 0x100AAC40, 0x100AAE00,
             0x100A0160, 0x100A00A0, 0x100A00E0}
CMD_WRAP = {0x100A1EC0, 0x100AA1D0, 0x100A42E0}
TRANS_VT = {0x100C25D0, 0x100C2620, 0x100C2660}
TRANS_FUNCS = {0x1009A2E0}


def vt_of_ctor(c):
    return {'0x00': 0x100C28D4, '0x12': 0x100C299C, '0x15a': 0x100C2924,
            '0x15b': 0x100C2A64, '0x16': 0x100C29C4, '0x1A': 0x100C294C,
            '0x1B': 0x100C2ADC, '0x1D': 0x100C28FC, '0x24': 0x100C2A3C,
            '0x25': 0x100C2A14, '0x28': 0x100C303C, '0x2A': 0x100C3064,
            '0x3B': 0x100C30B4, '0x3C': 0x100C308C, '0xC0': 0x100C30DC,
            '0xC1': 0x100C2B04, '0xE0': 0x100C2A8C, '0xE1': 0x100C2AB4}


def main():
    r = G.load()
    fwd, rev = G.graph(r['edges'])
    funcs = r['funcs']
    caps = json.load(open(os.path.join(ROOT, 'dispatch_caps.json')))['caps']

    # 传输层函数集合 = 三张传输 vtable 的全部槽
    trans = set(TRANS_FUNCS)
    for vt in TRANS_VT:
        for s in V.vt_slots(vt, 64):
            trans.add(s)
    anchors = set(BUILD_FUNCS) | CDB_CTORS | CMD_WRAP | trans
    print('anchors: build=%d ctor=%d wrap=%d trans=%d total=%d'
          % (len(BUILD_FUNCS), len(CDB_CTORS), len(CMD_WRAP), len(trans), len(anchors)))

    # 反向 BFS：谁离锚点近
    def bwd(seed, depth):
        cur = set(seed)
        seen = set()
        for _ in range(depth):
            nxt = set()
            for f in cur:
                for c in rev.get(f, ()):
                    if c not in seen:
                        seen.add(c)
                        nxt.add(c)
            cur = nxt
            if not nxt:
                break
        return seen

    near3 = bwd(anchors, 3)
    near5 = bwd(anchors, 5)
    print('backward depth3=%d depth5=%d' % (len(near3), len(near5)))

    # 正向 BFS
    def fwd_reach(seeds, depth, cap=20000):
        cur = set(seeds)
        seen = set(seeds)
        for _ in range(depth):
            nxt = set()
            for f in cur:
                for c in fwd.get(f, ()):
                    if c not in seen:
                        seen.add(c)
                        nxt.add(c)
            cur = nxt
            if not nxt or len(seen) > cap:
                break
        return seen

    # 通用 helper（被很多 ctor 调用）
    rows = []
    vtcount = collections.Counter()
    for c in caps:
        ctor = int(c['handler'], 16)
        ins, recs = V.ctor_vtables(ctor)
        eff0 = [x for x in recs if x[1] == 0]
        prim = eff0[-1][2] if eff0 else None
        methods = V.vt_slots(prim, 64) if prim else []
        seeds = {ctor} | set(methods)
        fr = fwd_reach(seeds, 3)
        hit_a = fr & near3           # 双向合计 ≤6 跳
        d1 = fr & anchors
        direct = sorted(fwd.get(ctor, ()))
        rows.append(dict(cap_hex=c['cap_hex'], cap_id=c['cap_id'], group=c['group'],
                         ctor='0x%08X' % ctor, vt='0x%08X' % prim if prim else None,
                         nmeth=len(methods), ncallee=len(direct),
                         callees=['0x%08X' % x for x in direct],
                         reach3=len(fr), hitA=sorted('0x%08X' % x for x in hit_a),
                         directA=sorted('0x%08X' % x for x in d1)))
        if prim:
            vtcount[prim] += 1
    json.dump(rows, open(os.path.join(HERE, 'caps_feat.json'), 'w'), indent=0)

    na = sum(1 for x in rows if x['hitA'])
    print('=== A 类（≤6 跳触达 CDB/传输层）: %d / %d' % (na, len(rows)))
    for x in rows:
        if x['hitA']:
            print('  %s ctor=%s vt=%s meth=%d hits=%s'
                  % (x['cap_hex'], x['ctor'], x['vt'], x['nmeth'], x['hitA'][:4]))
    # callee 频次
    cc = collections.Counter()
    for x in rows:
        for k in x['callees']:
            cc[k] += 1
    print('=== 被 ≥15 个 ctor 调用的通用 helper ===')
    for k, v in cc.most_common(20):
        print('   %s  %d' % (k, v))
    print('=== 主 vtable 复用 ===')
    for k, v in vtcount.most_common(10):
        print('   0x%08X %d' % (k, v))
    # 无主 vtable 的
    print('=== 无主 vtable 的 cap ===')
    for x in rows:
        if not x['vt']:
            print('   %s -> %s' % (x['cap_hex'], x['ctor']))


if __name__ == '__main__':
    main()
