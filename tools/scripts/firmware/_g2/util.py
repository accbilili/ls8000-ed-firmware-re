import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import json, sys, collections
sys.path.insert(0, TOOLCHAIN_ROOT)
from h8dis import H8
from h8tab import load_entries

D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
H = H8(D, load_entries(sample('h8.lst')), base=BASE)
CFG = json.load(open(cfg('cfg_v4.json')))
INS = {int(k, 16) if isinstance(k, str) else k: v for k, v in CFG['insns'].items()}
OWNER = {int(k, 16) if isinstance(k, str) else k: (int(v, 16) if isinstance(v, str) else v)
         for k, v in CFG['owner'].items()}


def dis(addr, n=200, until=None):
    pc = addr - BASE
    out = []
    for _ in range(n):
        if pc < 0 or pc + 1 >= len(D):
            break
        r = H.decode(pc)
        if r is None or r[1] is None:
            out.append((pc + BASE, '.byte', f'0x{D[pc]:02X}'))
            pc += 2
            continue
        sz, nm, a1, a2, nxt = r
        ops = ', '.join(x for x in (a1, a2) if x)
        out.append((pc + BASE, nm, ops))
        if until and pc + BASE == until:
            break
        pc = nxt
    return out


def pdis(addr, n=200, until=None):
    for a, nm, ops in dis(addr, n, until):
        print(f'0x{a:06X}  {nm:<9} {ops}')


def owner(a):
    return OWNER.get(a)


def callers_of(target):
    """扫描全反汇编，找调用 target 的指令（jsr/bsr/jmp 绝对地址或 @addr）"""
    res = []
    for a, v in INS.items():
        nm = v[1]
        if nm not in ('jsr', 'bsr', 'jmp'):
            continue
        ops = ' '.join(str(x) for x in v[2:4])
        for tok in (v[2], v[3]):
            if tok is None:
                continue
            s = str(tok).lstrip('@')
            try:
                val = int(s, 16)
            except ValueError:
                continue
            if val == target:
                res.append((a, nm, ops))
    return sorted(res)
