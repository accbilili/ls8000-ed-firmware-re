"""构建合并调用图：edges.json(job 11+1) + 36 个 fix_*.asm 的 jsr/bsr 目标。

输出：跨函数簇的关键调用关系 + E0→C1→作业层 链路图。
只读工作区产物。
"""
import os, re, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')

JOB = {
    '0x035598': '10→0x035598 扫描预处理',
    '0x02AEAA': '40→0x02AEAA 走片轴绝对移动',
    '0x02B98A': '41→0x02B98A 轴1 相对移动',
    '0x02CB66': '42→0x02CB66 轴2 绝对移动',
    '0x028648': '81→0x028648 夹具归位三连',
    '0x03A3D4': 'A0→0x03A3D4 扫描启动',
    '0x027F24': 'B0→0x027F24 固定工位往返',
    '0x02BBAE': 'B3→0x02BBAE 设置写+重定位',
    '0x02BA24': 'C1→0x02BA24 轴1 绝对移动',
    '0x02866E': 'D0→0x02866E 进片状态机',
    '0x028722': '80/00→0x028722 空操作',
    '0x02AAAE': '40→0x02AAAE (旧错址, 已由 f_02AEAA.asm 更正)',
}
# 36 个 fix 函数在 cfg_v4 owner 里的簇名（按地址归组）
CLUSTER = {
    '0x022F4E': 'SCSI 0x28 处理函数簇(0x022EC2)', '0x023066': 'SCSI 0x28 处理函数簇(0x022EC2)',
    '0x023A3A': 'SCSI 0x2A 处理函数簇(0x023A3A)', '0x023F68': 'SCSI 0x2A 处理函数簇(0x023A3A)',
    '0x02401C': 'SCSI 0x12 处理函数簇(0x023FA4)',
    '0x02510C': 'SCSI 0x24 处理函数簇(0x02510C)',
    '0x02582C': 'SCSI 0x25 处理函数簇(0x0254F6)',
    '0x025A22': 'SCSI 0x25 处理函数簇(0x0254F6)',
    '0x026534': 'SCSI 0x3B 处理函数簇(0x026534)',
    '0x0267AA': 'SCSI 0x3C 处理函数簇(0x0267AA)',
    '0x0289B4': '片夹识别簇(0x0289B4/0x028E30/0x0290A0)',
    '0x028AA0': '片夹识别簇(0x0289B4/0x028E30/0x0290A0)',
    '0x02D700': '扫描参数装配簇(0x02D700/0x02DC4A/0x02F496/0x02F8D4)',
    '0x02DC4A': '扫描参数装配簇(0x02D700/0x02DC4A/0x02F496/0x02F8D4)',
    '0x02F496': '扫描参数装配簇(0x02D700/0x02DC4A/0x02F496/0x02F8D4)',
    '0x02F8D4': '扫描参数装配簇(0x02D700/0x02DC4A/0x02F496/0x02F8D4)',
    '0x030000': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x030538': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x030D12': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x030E86': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x030F1A': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x0315A8': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x031924': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x031B2A': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x0328DE': '通道/位深表簇(0x0328DE–0x0332EE)',
    '0x032BB8': '通道/位深表簇(0x0328DE–0x0332EE)',
    '0x032BDC': '通道/位深表簇(0x0328DE–0x0332EE)',
    '0x032D2C': '通道/位深表簇(0x0328DE–0x0332EE)',
    '0x0332EE': '通道/位深表簇(0x0328DE–0x0332EE)',
    '0x034B8E': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x0354DE': '图像/曝光表簇(0x030000–0x0354DE)',
    '0x03A21E': '位深/gamma 表簇(0x03A21E/0x03A284/0x03A2D8)',
    '0x03A284': '位深/gamma 表簇(0x03A21E/0x03A284/0x03A2D8)',
    '0x03A2D8': '位深/gamma 表簇(0x03A21E/0x03A284/0x03A2D8)',
    '0x03B87C': '位置表簇(0x03B87C)',
    '0x03C9E4': '区域/位置表簇(0x03C9E4)',
}


def main():
    edges = json.load(open(os.path.join(JOBS, 'edges.json'), encoding='utf-8'))
    # 1) edges.json 统计
    tot = 0
    kinds = collections.Counter()
    for g, es in edges.items():
        tot += len(es)
        for x in es:
            kinds[x['kind']] += 1

    # 2) fix_*.asm 的调用目标
    fixcalls = collections.defaultdict(collections.Counter)
    for f in sorted(os.listdir(JOBS)):
        if not re.match(r'^fix_[0-9A-Fa-f]{6}\.asm$', f):
            continue
        src = '0x' + f[4:10].upper()
        for l in open(os.path.join(JOBS, f), encoding='utf-8', errors='replace'):
            m = re.match(r'^0x[0-9A-Fa-f]{6}\s+(jsr|bsr)\s+(0x[0-9a-fA-F]+)', l.strip())
            if m:
                fixcalls[src][m.group(2).lower()] += 1

    # 3) 合并：调用者 → 被调者
    merged = collections.Counter()
    src_label = {}
    for g, es in edges.items():
        src = '0x' + g.split('->')[1].upper()
        src_label[src] = JOB.get(src, f'job:{src}')
        for x in es:
            if x['kind'] == 'call' and x['to'] is not None:
                merged[(src, '0x%06X' % x['to'])] += 1
    for src, tg in fixcalls.items():
        src_label[src] = CLUSTER.get(src, f'fix:{src}')
        for t, n in tg.items():
            merged[(src, '0x' + t[2:].upper())] += n

    # 4) 跨簇调用
    def cluster(a):
        if a in CLUSTER:
            return CLUSTER[a]
        if a in JOB:
            return JOB[a]
        return None

    print('=' * 78)
    print(f'edges.json: 组数 {len(edges)}  边总数 {tot}  类型分布 {dict(kinds)}')
    print(f'fix_*.asm 调用边（合并后总 call 边）: {sum(merged.values())}')
    print()
    print('=== 跨簇/跨函数簇 的 call 关系（≥1 次）===')
    xc = []
    for (s, t), n in merged.items():
        cs, ct = cluster(s), cluster(t)
        if cs and ct and cs != ct:
            xc.append((n, s, cs, t, ct))
        elif cs and not ct:
            xc.append((n, s, cs, t, '(簇外助手)'))
    for n, s, cs, t, ct in sorted(xc, key=lambda x: (-x[0], x[1])):
        print(f'  x{n:<3d} {s} [{cs}]  --->  {t} [{ct}]')
    print()
    print('=== 被调最多的簇外助手（跨簇复用度）===')
    help_cnt = collections.Counter()
    for (s, t), n in merged.items():
        if cluster(t) is None:
            help_cnt[t] += n
    for t, n in help_cnt.most_common(25):
        print(f'  {t}  x{n}')

    out = dict(edges_groups=len(edges), edges_total=tot, kinds=dict(kinds),
               merged_calls=sum(merged.values()),
               cross=[dict(n=n, src=s, src_cluster=cs, dst=t, dst_cluster=ct) for n, s, cs, t, ct in sorted(xc, key=lambda x: (-x[0], x[1]))],
               helpers=help_cnt.most_common(30))
    with open(os.path.join(HERE, 'callgraph.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
