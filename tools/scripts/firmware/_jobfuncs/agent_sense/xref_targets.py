"""1) 全文件线性扫查，找所有跳转/调用到指定目标的指令（xref）。
2) 验证 0x01914A sense 表在 idx 0x50 / 0x56 处的字节。
3) 输出调用 0x0116A0 / 0x011882 的位置。
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
import sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
N = len(d)

def parse_tgt(s):
    if s is None: return None
    s = s.strip()
    if s.startswith('0x'):
        try: return int(s, 16)
        except: return None
    return None

CALLS = {'jsr', 'bsr', 'jmp', 'bra', 'bt'}
BCC = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}

targets = {0x0116A0: 'flush_parse_status', 0x011882: 'ret_400436_getter', 0x011708: 'REQUEST_SENSE_ctor',
           0x0211B6: 'lookup_0x03E390', 0x01750E: 'pathA_caller', 0x021418: 'fn_021418',
           0x020E86: 'fn_020E86', 0x022AD6: 'fn_022AD6', 0x022BF2: 'fn_022BF2'}

xrefs = {t: [] for t in targets}
for off in range(0, N - 8, 2):
    sz, nm, a1, a2, nxt = h.decode(off)
    if nm is None: continue
    if nm in CALLS or nm in BCC:
        t = parse_tgt(a1)
        if t in targets:
            xrefs[t].append((off + BASE, nm, a1))

for t, name in targets.items():
    print(f'--- xrefs to 0x{t:06X} ({name}): {len(xrefs[t])} ---')
    for a, nm, a1 in xrefs[t]:
        print(f'  0x{a:06X}  {nm} {a1}')

# 验证 sense 表 0x01914A: idx 0x50 与 0x56
def rd(addr, n):
    off = addr - BASE
    return d[off:off+n]
for idx in (0x50, 0x56):
    a = 0x01914A + idx * 5
    print(f'sense[{idx:#04x}] @ 0x{a:06X} = {rd(a,5).hex(" ")}')
# 对照通路A样本
for idx in (0x05, 0x8E, 0x30, 0x93):
    a = 0x01914A + idx * 5
    print(f'sense[{idx:#04x}] @ 0x{a:06X} = {rd(a,5).hex(" ")}')
