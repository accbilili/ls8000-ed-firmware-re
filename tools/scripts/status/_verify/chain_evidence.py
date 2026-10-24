"""核实 E0→C1→作业层 链路的字节级证据。

只读 D: 样本 + 工作区；产物写本 _verify。
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, JOBS)
from h8dis import H8
from h8fix import load_entries_fixed

BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
h = H8(d, load_entries_fixed(sample('h8.lst')), base=BASE)


def dis(a, n=40):
    out = []
    pc = a - BASE
    for _ in range(n):
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            out.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            break
        out.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
        pc = nxt
    return out


CHECKS = [
    ('E0 解析层入口 0x026BF8', 0x026BF8, 16),
    ('E0 六数值门限 0x026DF8', 0x026DF8, 20),
    ('E0 落存 0x400408 写点簇', 0x026A54, 10),
    ('C1 执行层 0x0269A6', 0x0269A6, 16),
    ('C1 公共尾 0x026BD2', 0x026BD2, 12),
    ('作业层查表 0x0275F2', 0x0275F2, 16),
    ('作业层 jsr @er4 0x027642', 0x02762E, 10),
]

out = {}
for title, a, n in CHECKS:
    print('=' * 74)
    print(title)
    print('=' * 74)
    for l in dis(a, n):
        print('   ', l)
    out[title] = dis(a, n)

# E0 门限段的实际指令（定位 6 个 cmp.l）
print()
print('=' * 74)
print('E0 段 0x026DF0–0x026EB0 全量（找 6 个 cmp.l 门限）')
print('=' * 74)
seg = dis(0x026DF0, 60)
for l in seg:
    print('   ', l)
out['E0_gates'] = seg

with open(os.path.join(HERE, 'chain_evidence.txt'), 'w', encoding='utf-8') as f:
    for k, v in out.items():
        f.write(f'### {k}\n')
        f.write('\n'.join(v) + '\n\n')
