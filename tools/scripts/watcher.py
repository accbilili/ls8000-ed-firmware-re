import json, os, time, glob

BASE = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis'
STAT = os.path.join(BASE, 'status')
if not os.path.isdir(STAT):
    os.makedirs(STAT)

TASKS = [
    ('F1', '17.2 进片状态机 0x027DC4',      ['firmware/statemachine_27DC4.md']),
    ('F2', '17.2 片夹识别 0x028BB0',        ['firmware/film_ident_28BB0.md']),
    ('F3', '17.x 校准链路 0x02753E',        ['firmware/calib_2753E.md']),
    ('F4', '17.3 变量 0x4003FB',            ['firmware/var_4003FB.md']),
    ('F5', 'md3 CDB 构造点全集',            ['md3/cdb_sites.md', 'md3/cdb_sites.json']),
    ('F6', 'md3 导出与结构体契约',          ['md3/exports.md']),
    ('G1', '17.1 表 0x01914A 解码',         ['firmware/table_01914A.md']),
    ('G2', '17.1 host_code 来源与语义',     ['firmware/hostcode_source.md']),
    ('G3', '17.1 能力ID→CDB 对接面',        ['md3/cap_to_cdb.md']),
    ('G4', '17.1 E0/SCSI→host_code 桥',     ['firmware/e0_bridge.md']),
]

START = time.time()

while True:
    rows = []
    for tid, label, dels in TASKS:
        flags = sorted(glob.glob(os.path.join(STAT, tid + '_*.flag')))
        msg = ''
        if flags:
            try:
                msg = open(flags[-1], encoding='utf-8', errors='replace').read().strip().replace('\n', ' ')[:110]
            except Exception:
                msg = ''
        have = [d for d in dels if os.path.exists(os.path.join(BASE, d))]
        n, tot = len(have), len(dels)
        if n == tot:
            state, pct = 'done', 100
        elif flags:
            state = 'running'
            pct = int(round(100 * (n / tot * 0.85 + 0.15)))
        else:
            state, pct = 'queued', 0
        rows.append({
            'id': tid, 'label': label, 'state': state, 'pct': pct,
            'msg': msg, 'steps': len(flags),
            'deliverables': [{'name': d, 'ok': os.path.exists(os.path.join(BASE, d))} for d in dels],
        })

    done = sum(1 for r in rows if r['state'] == 'done')
    running = sum(1 for r in rows if r['state'] == 'running')
    total_pct = int(round(sum(r['pct'] for r in rows) / len(rows)))
    payload = {
        'ts': time.strftime('%H:%M:%S'), 'elapsed': int(time.time() - START),
        'done': done, 'running': running, 'total': len(rows),
        'overall': total_pct, 'tasks': rows,
    }
    tmp = os.path.join(STAT, 'progress.json.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    os.replace(tmp, os.path.join(STAT, 'progress.json'))
    time.sleep(1.5)
