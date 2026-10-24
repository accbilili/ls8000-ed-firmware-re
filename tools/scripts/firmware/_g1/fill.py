# -*- coding: utf-8 -*-
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import io, collections

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
TAB = 0x01914A
N = 143
H = 0x03E390
CONST = [0x01, 0x04, 0x07, 0x08, 0x09, 0x0A, 0x0D, 0x4E, 0x50, 0x53, 0x55,
         0x56, 0x58, 0x59, 0x64, 0x6F, 0x76, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D]

hosts = []
i = 0
while True:
    off = H + i * 4 - BASE
    hc = int.from_bytes(d[off:off + 2], 'big')
    if hc == 0:
        break
    hosts.append((hc, int.from_bytes(d[off + 2:off + 4], 'big')))
    i += 1
f2set = collections.defaultdict(list)
for hc, f2 in hosts:
    f2set[f2].append(hc)

SK = {0: 'NO SENSE', 1: 'RECOVERED ERR', 2: 'NOT READY', 3: 'MEDIUM ERR',
      4: 'HARDWARE ERR', 5: 'ILLEGAL REQ', 6: 'UNIT ATTENTION',
      7: 'DATA PROTECT', 8: 'BLANK CHECK', 9: 'VENDOR SPEC', 0xB: 'ABORTED CMD'}

out = []
for k in range(N):
    off = TAB + k * 5 - BASE
    b = d[off:off + 5]
    hcs = f2set.get(k, [])
    src = []
    if hcs:
        src.append('host')
    if k in CONST:
        src.append('400436')
    if k == 0:
        src.append('default')
    s = '+'.join(src) if src else '**空槽**'
    hc = ' '.join('%04X' % x for x in hcs) if hcs else '-'
    out.append('| 0x%02X | 0x%06X | %02X | %02X | %02X | %02X | %02X | %s | %s | %s |'
               % (k, TAB + k * 5, b[0], b[1], b[2], b[3], b[4],
                  SK.get(b[1], '?%02X' % b[1]), s, hc))

p = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\table_01914A.md'
txt = io.open(p, encoding='utf-8').read()
txt = txt.replace('@@ROWS@@', '\n'.join(out))
io.open(p, 'w', encoding='utf-8').write(txt)
print('rows', len(out), 'lines now', txt.count('\n') + 1)
