# -*- coding: utf-8 -*-
"""G1: 生成 table_01914A.csv + 覆盖统计"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import csv, collections, io, sys

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
TAB = 0x01914A
N = 143

# ---- 1. 0x03E390 : 85 条 [u16 host_code][u16 field2] ----
H = 0x03E390
hosts = []
i = 0
while True:
    off = H + i * 4 - BASE
    hc = int.from_bytes(d[off:off + 2], 'big')
    f2 = int.from_bytes(d[off + 2:off + 4], 'big')
    if hc == 0:
        break
    hosts.append((hc, f2))
    i += 1

# ---- 2. 0x01914A 记录 ----
recs = []
for k in range(N):
    off = TAB + k * 5 - BASE
    b = d[off:off + 5]
    recs.append(b)

# ---- 3. 常量索引（写入 0x400436 的立即数，来自 t7.py） ----
CONST = [0x01, 0x04, 0x07, 0x08, 0x09, 0x0A, 0x0D, 0x4E, 0x50, 0x53, 0x55,
         0x56, 0x58, 0x59, 0x64, 0x6F, 0x76, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D]

f2set = collections.defaultdict(list)
for hc, f2 in hosts:
    f2set[f2].append(hc)

SK = {0: 'NO SENSE', 1: 'RECOVERED ERROR', 2: 'NOT READY', 3: 'MEDIUM ERROR',
      4: 'HARDWARE ERROR', 5: 'ILLEGAL REQUEST', 6: 'UNIT ATTENTION',
      7: 'DATA PROTECT', 8: 'BLANK CHECK', 9: 'VENDOR SPECIFIC',
      0xB: 'ABORTED COMMAND', 0xF: 'COMPLETED'}
ASC = {0x00: 'no additional sense', 0x03: 'peripheral device write fault',
       0x04: 'logical unit not ready', 0x08: 'logical unit communication failure',
       0x11: 'read retries exhausted / unrecovered read error',
       0x15: 'random positioning error', 0x25: 'logical unit not supported',
       0x3A: 'medium not present', 0x44: 'internal target failure',
       0x53: 'media load or eject failed', 0x80: 'vendor specific'}

def bits(f):
    s = []
    for b, m in ((7, 'bit7=抑制/不出sense'), (6, 'bit6=跳过011882'), (5, 'bit5=deferred(0xF0)+info'),
                 (4, 'bit4=sense[2]|=0x20'), (3, 'bit3=填sense-key-specific'),
                 (2, 'bit2=上报AA帧'), (1, 'bit1=可发布'), (0, 'bit0=需结果码2000/3000')):
        if f & (1 << b):
            s.append('b%d' % b)
    return '|'.join(s) if s else '-'

rows = []
for k in range(N):
    b = recs[k]
    f, sk, asc, ascq, vend = b
    hcs = f2set.get(k, [])
    src = []
    if hcs:
        src.append('host_code')
    if k in CONST:
        src.append('const@400436')
    if k == 0:
        src.append('默认/清零(未命中)')
    rows.append({
        'idx': k,
        'idx_hex': '0x%02X' % k,
        'addr': '0x%06X' % (TAB + k * 5),
        'b0_flags': '0x%02X' % f,
        'b1_SK': '0x%02X' % sk,
        'b2_ASC': '0x%02X' % asc,
        'b3_ASCQ': '0x%02X' % ascq,
        'b4_vendor': '0x%02X' % vend,
        'flags_bits': bits(f),
        'SK_txt': SK.get(sk, '?'),
        'ASC_txt': ASC.get(asc, 'vendor' if asc >= 0x40 else '?'),
        'sense': '%02X %02X %02X %02X' % (sk, asc, ascq, vend),
        'n_host_code': len(hcs),
        'host_codes': ' '.join('0x%04X' % x for x in hcs),
        'src': '+'.join(src) if src else 'NONE',
    })

with io.open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\table_01914A.csv',
             'w', newline='', encoding='utf-8-sig') as fp:
    w = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow(r)

# ---- 4. 统计 ----
print('host_code 条数 =', len(hosts))
print('field2 最小/最大 = 0x%02X / 0x%02X' % (min(f2 for _, f2 in hosts), max(f2 for _, f2 in hosts)))
print('field2 去重 =', len(f2set))
used = set(f2set) | set(CONST) | {0}
never = [k for k in range(N) if k not in used]
print('被引用 =', len(used), ' 从未被引用 =', len(never))
print('never list:', ' '.join('%02X' % k for k in never))
# 连续段
segs = []
for k in never:
    if segs and segs[-1][1] == k - 1:
        segs[-1][1] = k
    else:
        segs.append([k, k])
print('never 连续段:', ', '.join('0x%02X' % a if a == b else '0x%02X-0x%02X' % (a, b) for a, b in segs))
print()
print('flags 分布:', collections.Counter(r['b0_flags'] for r in rows))
print('SK 分布:', collections.Counter('%02X' % recs[k][1] for k in range(N)))
print('ASC 分布:', collections.Counter('%02X' % recs[k][2] for k in range(N)))
print()
hb = collections.Counter(hc >> 8 for hc, _ in hosts)
print('host_code 高字节分组:', ' '.join('%02X:%d' % (k, v) for k, v in sorted(hb.items())))
print('高字节种类 =', len(hb))
by_hb = collections.defaultdict(list)
for hc, f2 in hosts:
    by_hb[hc >> 8].append((hc, f2))
for k in sorted(by_hb):
    v = by_hb[k]
    ks = set('%02X%02X' % (recs[f2][1], recs[f2][2]) for _, f2 in v)
    fl = set('%02X' % recs[f2][0] for _, f2 in v)
    print('  0x%02X  n=%2d  low=%s  SK+ASC=%s  flags=%s' %
          (k, len(v), ' '.join('%02X' % (hc & 0xFF) for hc, _ in v), sorted(ks), sorted(fl)))
