# -*- coding: utf-8 -*-
"""解析 out_census.txt：0x4003EC-0x40043F 的读写矩阵 + 逐点文本核对。"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

s = open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\out_census.txt',
         encoding='utf-8', errors='replace').read()
sec = s.split('=== 未对齐')[0]
cur = None
rows = []
for line in sec.splitlines():
    m = re.match(r'\[0x([0-9A-F]{6})\]', line.strip())
    if m:
        cur = int(m.group(1), 16); continue
    m = re.match(r'\s+0x([0-9A-F]{6})\s+(\S+)\s+(.*?)\s{2,}([RW])\s+owner=(\S+)', line)
    if m and cur is not None:
        rows.append(dict(tgt=cur, pc=int(m.group(1), 16), mn=m.group(2),
                         ops=m.group(3).strip(), rw=m.group(4), owner=m.group(5)))

print('总行数', len(rows))
tgt = sorted({r['tgt'] for r in rows})
print('地址数', len(tgt), '范围 0x%06X-0x%06X' % (tgt[0], tgt[-1]))

print('\n### 0x4003EC-0x40043F 读写矩阵')
print('| 地址 | W | R | 写点（函数） |')
print('|---|---|---|---|')
for a in tgt:
    if not (0x4003EC <= a <= 0x40043F):
        continue
    ws = [r for r in rows if r['tgt'] == a and r['rw'] == 'W']
    rs = [r for r in rows if r['tgt'] == a and r['rw'] == 'R']
    wtxt = ', '.join(f"0x{r['pc']:06X}({r['owner']})" for r in ws) or '-'
    print(f"| 0x{a:06X} | {len(ws)} | {len(rs)} | {wtxt} |")

print('\n### 0x4003FB 全部直接访问点')
for r in rows:
    if r['tgt'] == 0x4003FB:
        print(f"0x{r['pc']:06X}  {r['mn']:<8} {r['ops']:<24} {r['rw']} owner={r['owner']}")
