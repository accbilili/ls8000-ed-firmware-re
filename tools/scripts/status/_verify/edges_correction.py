"""补算 edges.json 中作业表 0x40 项的正确条目。

背景：dis_all.py 的 TARGETS 用 (0x40, 0x2AAAE)（前序错址），
作业表 0x03EDE8 实测字节为 `40 00 00 02 AE AA` → 正确处理函数是 0x02AEAA。
edges.json 里仍是旧组 `40->02AAAE`；f_02AEAA.asm 是事后单独补的（mtime 更晚）。
本脚本用 dis_all.py 同算法补算正确条目，并给出差异。
产物写本 _verify。
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
import sys, os, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, JOBS)
from h8dis import H8
from h8fix import load_entries_fixed

BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
h = H8(d, load_entries_fixed(sample('h8.lst')), base=BASE)

UNCOND = {'jmp', 'bra', 'bt'}
NEVER = {'bf'}
CALLS = {'jsr', 'bsr'}
CONDS = {'bhi','bls','bcc','bcs','bne','beq','bvc','bvs','bpl','bmi','bge','blt','bgt','ble','brn'}

TARGETS = [
    (0x10, 0x35598), (0x40, 0x2AAAE), (0x41, 0x2B98A), (0x42, 0x2CB66),
    (0x81, 0x28648), (0xA0, 0x3A3D4), (0xB0, 0x27F24), (0xC1, 0x2BA24),
    (0xD0, 0x2866E), (0x80, 0x28722), (0xB3, 0x2BBAE), (0x00, 0x28722),
]
STOPS = {t for _, t in TARGETS}


def parse_tgt(s):
    if s is None:
        return None
    s = s.strip()
    if s.startswith('0x'):
        try:
            return int(s, 16)
        except ValueError:
            return None
    return None


def disasm_fn(entry):
    seen, edges = {}, []
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            if (pc + BASE) in STOPS and (pc + BASE) != entry:
                break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None
                break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts':
                break
            elif nm in CALLS:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'call', 'to': t, 'text': f'{nm} {a1}'})
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'jmp', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
                break
            elif nm in NEVER:
                edges.append({'from': pc + BASE, 'kind': 'never', 'to': parse_tgt(a1), 'text': f'{nm} {a1}'})
            elif nm in CONDS:
                t = parse_tgt(a1)
                edges.append({'from': pc + BASE, 'kind': 'bcc', 'to': t, 'text': f'{nm} {a1}'})
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges


old = json.load(open(os.path.join(JOBS, 'edges.json'), encoding='utf-8'))
kinds_old = collections.Counter()
for g, es in old.items():
    for x in es:
        kinds_old[x['kind']] += 1

print('=' * 74)
print('edges.json 现状（未更正）')
print('=' * 74)
print(f'组数 {len(old)}  边总数 {sum(len(v) for v in old.values())}  类型 {dict(kinds_old)}')
oldg = old.get('40->02AAAE', [])
print(f'组 40->02AAAE: {len(oldg)} 边')
for x in oldg:
    print('   ', x)

print()
print('=' * 74)
print('补算正确条目 40->02AEAA')
print('=' * 74)
seen, edges = disasm_fn(0x2AEAA)
kinds = collections.Counter(x['kind'] for x in edges)
print(f'指令 {len(seen)}  边 {len(edges)}  类型 {dict(kinds)}')
for x in edges:
    print('   ', x)

# 差异
old_calls = {(x['from'], x['to'], x['text']) for x in oldg if x['kind'] == 'call'}
new_calls = {(x['from'], x['to'], x['text']) for x in edges if x['kind'] == 'call'}
print()
print('--- call 边差异 ---')
print('旧组独有:', sorted(old_calls - new_calls))
print('新组独有:', sorted(new_calls - old_calls))
print('共有:', len(old_calls & new_calls))

# 全量重算（含更正）
print()
print('=' * 74)
print('全量重算（把 0x40 项换成 0x02AEAA）')
print('=' * 74)
TARGETS2 = [(k, (0x2AEAA if v == 0x2AAAE else v)) for k, v in TARGETS]
STOPS2 = {t for _, t in TARGETS2}
all_edges = {}
for key, fn in TARGETS2:
    s, e = disasm_fn(fn)
    all_edges[f'{key:02X}->{fn:06X}'] = e
k2 = collections.Counter()
for g, es in all_edges.items():
    for x in es:
        k2[x['kind']] += 1
print(f'组数 {len(all_edges)}  边总数 {sum(len(v) for v in all_edges.values())}  类型 {dict(k2)}')
print('旧 40->02AAAE 组边数:', len(oldg), '  新 40->02AEAA 组边数:', len(all_edges.get('40->02AEAA', [])))
print('净变化:', sum(len(v) for v in all_edges.values()) - sum(len(v) for v in old.values()))

with open(os.path.join(HERE, 'edges_correction.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(
        old_total=sum(len(v) for v in old.values()), old_kinds=dict(kinds_old),
        new_total=sum(len(v) for v in all_edges.values()), new_kinds=dict(k2),
        old_40_group=oldg, new_40_group=all_edges.get('40->02AEAA'),
        old_only_calls=sorted(old_calls - new_calls),
        new_only_calls=sorted(new_calls - old_calls),
        full_new=all_edges), f, indent=1, ensure_ascii=False)
