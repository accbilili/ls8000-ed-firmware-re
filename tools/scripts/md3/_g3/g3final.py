"""G3 续跑：只读既有 g3cfg/g3vtall/caps_feat，生成 268 条归类与复核统计。"""
import csv
import collections
import json
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import g3cfg as G
from capstone.x86_const import X86_OP_IMM


def main():
    with open(os.path.join(HERE, 'g3cfg.pkl'), 'rb') as f:
        cfg = pickle.load(f)
    with open(os.path.join(HERE, 'g3vtall.pkl'), 'rb') as f:
        vo = pickle.load(f)
    with open(os.path.join(HERE, 'caps_feat.json'), encoding='utf-8') as f:
        feats = json.load(f)
    with open(os.path.join(ROOT, 'dispatch_caps.json'), encoding='utf-8') as f:
        caps = json.load(f)['caps']
    with open(os.path.join(ROOT, 'cdb_sites.json'), encoding='utf-8') as f:
        sites = json.load(f)
    assert len(caps) == len(feats) == 268

    build = {int(x['func'], 16) for x in sites if x['func']}
    cdb_ctors = {
        0x1009FD20, 0x1009FE80, 0x1009FEC0, 0x1009FD60, 0x100A0020,
        0x1009FF10, 0x1009FDE0, 0x100A0120, 0x1009FD40, 0x1009FF50,
        0x1009FFE0, 0x1009FF90, 0x100AAB30, 0x100AAB90, 0x100AABF0,
        0x100AAC90, 0x100AAC40, 0x100AAE00, 0x100A0160, 0x100A00A0,
        0x100A00E0,
    }
    trans_vts = {0x100C25D0, 0x100C2620, 0x100C2660}
    trans = {0x1009A2E0}
    for vt, slots in vo['vts']:
        if vt in trans_vts:
            trans.update(slots)
    anchors = build | cdb_ctors | trans | {0x100A1EC0, 0x100AA1D0, 0x100A42E0}

    fwd = {f: set(d['dc']) for f, d in vo['sites'].items()}
    for a, b in cfg['edges']:
        fwd.setdefault(a, set()).add(b)
    vtables = dict(vo['vts'])
    rows = []
    for cap, feat in zip(caps, feats):
        assert cap['cap_hex'] == feat['cap_hex']
        ctor = int(cap['handler'], 16)
        # 0x548C/0x8007 共享内联臂 0x100734EF；dispatch.md 已给出 vtable。
        vt = 0x100C08F0 if ctor == 0x100734EF else (int(feat['vt'], 16) if feat['vt'] else None)
        methods = list(vtables.get(vt, [])) if vt else []
        seeds = {ctor} | set(methods)
        seen = set(seeds)
        cur = set(seeds)
        for _ in range(4):
            cur = {b for a in cur for b in fwd.get(a, ()) if b not in seen}
            seen.update(cur)
        hits = sorted(seen & anchors)
        if hits:
            cls = 'A'
            exit_desc = 'cdb_or_transport:' + '|'.join('0x%08X' % x for x in hits)
            evidence = '[实证] ctor+vtable 正向BFS4命中 ' + '|'.join('0x%08X' % x for x in hits)
        elif not methods:
            cls = 'C'
            exit_desc = 'constructor_only'
            evidence = '[推断] 未恢复vtable；ctor=0x%08X；BFS4无CDB/传输锚点' % ctor
        else:
            cls = 'B'
            exit_desc = 'local_vtable:0x%08X' % vt
            evidence = ('[推断] vt=0x%08X slots=%d；ctor+全部slots正向BFS4(%d节点)未抵18个BuildCDB/构造器/传输锚点；'
                        '未解析的他对象虚调用仍是覆盖边界') % (vt, len(methods), len(seen))
        rows.append({
            'cap_id': cap['cap_hex'], 'group': cap['group'],
            'handler': cap['handler'], 'class': cls,
            'exit': exit_desc, 'evidence': evidence,
        })

    out_csv = os.path.join(ROOT, 'cap_to_cdb.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['cap_id', 'group', 'handler', 'class', 'exit', 'evidence'])
        w.writeheader()
        w.writerows(rows)

    # 独立复核范围常量：只遍历缓存中已确认对齐的指令，不做字节模式语义搜索。
    wanted = {0x3BFA, 0x3BF9, 0x1C2, 0x1C1, 0xCD3, 0xCD2, 0x12C, 0x12B, 0xFED4}
    compare_hits = []
    immediate_hits = []
    nins = 0
    for i, marked in enumerate(cfg['mark']):
        if not marked:
            continue
        va = G.TLO + i
        one = next(G.md.disasm(G.read(va, 16), va, 1), None)
        if one is None:
            continue
        nins += 1
        for op in one.operands:
            if op.type != X86_OP_IMM:
                continue
            value = op.imm & 0xFFFFFFFF
            short_value = value & 0xFFFF
            if value in wanted or short_value in wanted:
                rec = {'va': '0x%08X' % va, 'insn': one.mnemonic + ' ' + one.op_str,
                       'value': '0x%X' % value}
                immediate_hits.append(rec)
                if one.mnemonic in ('cmp', 'test'):
                    compare_hits.append(rec)

    stats = {
        'counts': dict(collections.Counter(x['class'] for x in rows)),
        'group_counts': {g: dict(collections.Counter(x['class'] for x in rows if x['group'] == g))
                         for g in sorted({x['group'] for x in rows})},
        'anchor_count': len(anchors), 'build_count': len(build),
        'transport_count': len(trans), 'range_scan_insns': nins,
        'range_compare_hits': compare_hits, 'range_immediate_hits': immediate_hits,
        'coverage_note': 'A=命中锚点；B=恢复vtable且4跳未命中；C=未恢复任何方法。B不是动态全路径证明。',
    }
    with open(os.path.join(HERE, 'final_stats.json'), 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
