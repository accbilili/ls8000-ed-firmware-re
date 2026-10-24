"""E0 六数值立即数全镜像搜索（agent_15354）。

两层搜索：
A. CFG 层：cfg_v4.json insns 中所有立即数字指令（a1/a2 以 # 开头）解析数值，比对目标值。
B. 原始字节层：全镜像搜大端立即数字节模式，命中点回溯 2/4/6/8/10 字节试解码，
   确认是否为 cmp/add/sub/mov 等指令的立即数且数值匹配。
只读 D:\，输出 stdout + hits json。
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, cfg, sample
import sys, json, os, re
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)
cfg = json.load(open(cfg('cfg_v4.json')))
insns = cfg['insns']; owner = cfg['owner']

# 目标值 -> 说明
TARGETS = {
    0x3BFA: '15354',
    0x01C2: '450',
    0x0CD3: '3283',
    0x012C: '300',
    0xFED4: '-300(16bit)',
    0xFFFFFFD4: '-300(32bit)',
    0x00003BFA: '15354(32)',
    0x000001C2: '450(32)',
    0x00000CD3: '3283(32)',
    0x0000012C: '300(32)',
    0xC2: '450 low byte',
    0xD3: '3283 low byte',
    0x2C: '300 low byte',
    0x00FA: '450>>8? no',  # placeholder ignore
}
del TARGETS[0x00FA]

def immval(s):
    """'#0x1234' -> int; 失败返回 None"""
    if not isinstance(s, str) or not s.startswith('#'):
        return None
    try:
        return int(s[1:], 0)
    except ValueError:
        return None

# ---------- A. CFG 层 ----------
print('=== A. CFG 层立即数扫描 ===')
cfg_hits = []
for addr_s, content in insns.items():
    a = int(addr_s, 16)
    for op in (content[2], content[3]):
        v = immval(op)
        if v is None:
            continue
        if v in TARGETS:
            cfg_hits.append((a, content[1], op, owner.get(addr_s, '?')))
cfg_hits.sort()
print(f'命中 {len(cfg_hits)} 条（含所有指令类型，不限 cmp）')
for a, nm, op, ow in cfg_hits:
    print(f'  0x{a:06X} {nm:10s} {op:14s} owner=0x{int(ow,16):06X}' if isinstance(ow, str) else f'  0x{a:06X} {nm} {op} owner={ow}')

# ---------- B. 原始字节层 ----------
print()
print('=== B. 原始字节模式扫描（大端）===')
PATS = {
    b'\x3b\xfa': '15354',
    b'\x01\xc2': '450',
    b'\x0c\xd3': '3283',
    b'\x01\x2c': '300',
    b'\xfe\xd4': '-300',
    b'\xc2': '450_low8',
    b'\xd3': '3283_low8',
    b'\x2c': '300_low8',
}
raw_hits = {name: [] for name in set(PATS.values())}
for pat, name in PATS.items():
    start = 0
    while True:
        o = d.find(pat, start)
        if o < 0:
            break
        raw_hits[name].append(o)
        start = o + 1
for name in ('15354', '450', '3283', '300', '-300'):
    print(f'{name}: {len(raw_hits[name])} 处 2 字节模式')
for name in ('450_low8', '3283_low8', '300_low8'):
    print(f'{name}: {len(raw_hits[name])} 处单字节')

# 对 2 字节模式命中点，回溯试解码确认是否指令立即数
print()
print('=== B2. 2 字节模式命中点回溯解码（只看 cmp/add/sub/mov/and/or/xor）===')
IMM_OPS = ('cmp.b', 'cmp.w', 'cmp.l', 'add.b', 'add.w', 'add.l',
           'sub.b', 'sub.w', 'sub.l', 'mov.b', 'mov.w', 'mov.l',
           'and.b', 'and.w', 'or.b', 'or.w', 'xor.b', 'xor.w',
           'adds', 'subs', 'addx', 'subx', 'cmp')
confirmed = []
for name in ('15354', '450', '3283', '300', '-300'):
    for o in raw_hits[name]:
        a = o + BASE
        # 试各种指令起点（2 字节对齐为主，也试奇数）
        for back in (2, 4, 6, 8, 10, 3, 5, 7):
            p = o - back
            if p < 0:
                continue
            try:
                sz, nm, a1, a2, nxt = h.decode(p)
            except Exception:
                continue
            if nm is None:
                continue
            # 指令是否覆盖 offset o 且 o 是立即数字节
            if p + sz < o + 2:
                continue
            for op in (a1, a2):
                v = immval(op)
                if v is None:
                    continue
                # 立即数所在字节位置验证：imm 在指令中的偏移
                if v in TARGETS and v != 0x00FA:
                    # 验证立即数确实落在 offset o
                    # 简化：解码出的 imm 数值匹配目标即记录
                    if nm.split('.')[0] in ('cmp', 'add', 'sub', 'mov', 'and', 'or', 'xor', 'adds', 'subs', 'addx', 'subx'):
                        confirmed.append(dict(addr=a, off=o, name=name, insn=f'0x{p+BASE:06X} {nm} {a1}, {a2}',
                                              ins_addr=p + BASE, mnem=nm, imm=op))
                        break
seen = set()
uniq = []
for c in confirmed:
    k = (c['ins_addr'], c['imm'])
    if k in seen:
        continue
    seen.add(k)
    uniq.append(c)
print(f'确认 {len(uniq)} 条指令级命中：')
for c in uniq:
    own = owner.get(hex(c['ins_addr']), None)
    print(f"  [{c['name']:>5}] {c['insn']}   (CFG owner: {own})")

json.dump(dict(cfg_hits=cfg_hits, confirmed=uniq,
               raw_counts={k: len(v) for k, v in raw_hits.items()}),
          open(os.path.join(OUT, 'imm_hits.json'), 'w'), indent=1)
print('saved imm_hits.json')
