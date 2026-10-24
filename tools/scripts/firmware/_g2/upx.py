"""用 xrefs_data.csv 做向上调用链（含相对分支），比纯 jsr 扫描更全。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import csv, sys
from util import owner

B = 0x10000
EDGES = []
for r in csv.DictReader(open(sample('xrefs_data.csv'))):
    if r['mnemonic'].lower() == 'mnemonic':
        continue
    try:
        src = int(r['insn_addr'], 16) + B   # insn_addr/function 是文件偏移，需 +0x10000
        dst = int(r['target'], 16)          # target 已是绝对地址，不再加基址
    except ValueError:
        continue
    EDGES.append((src, dst, r['mnemonic'], r['kind'], int(r['function'], 16) + B))

KNOWN = {0x020E86: 'SCSI 分派器', 0x020B84: '主循环(段2)', 0x025A56: '参数块引擎',
         0x011078: '主循环(段1)', 0x011000: '段1 顶层', 0x02159C: 'SCSI 0x00 TUR',
         0x022D9A: 'SCSI 0x1D SEND DIAG', 0x02510C: 'SCSI 0x24 SET WINDOW',
         0x026BF8: 'SCSI 0xE0', 0x026EFC: 'SCSI 0xE1'}


def callers(t):
    return [(s, m, k) for s, d, m, k, f in EDGES if d == t]


def walk(t, depth=0, seen=None, maxd=14, out=None):
    if seen is None:
        seen = set()
    out = [] if out is None else out
    if depth > maxd or t in seen:
        return out
    seen.add(t)
    cs = callers(t)
    tag = KNOWN.get(t, '')
    nm = f'  <<{tag}>>' if tag else ''
    if not cs:
        out.append(f'{"  "*depth}0x{t:06X}{nm}   [顶层/无调用者]')
    else:
        out.append(f'{"  "*depth}0x{t:06X}{nm}')
    for s, m, k in cs:
        ow = owner(s) or s
        out.append(f'{"  "*depth}   <- {m} @0x{s:06X} (in 0x{ow:06X})')
        walk(ow, depth + 2, seen, maxd, out)
    return out


if __name__ == '__main__':
    lines = walk(int(sys.argv[1], 16), maxd=int(sys.argv[2]) if len(sys.argv) > 2 else 14)
    print('\n'.join(lines))
