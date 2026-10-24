"""抽样质量核验：对随机抽样的 fix_*.asm / boot_*.asm 做「重新解码 + 逐行 diff」。

流程：
1. 随机抽 3 个 fix_*.asm + 1 个 boot_*.asm
2. 用修复版解码器从该函数入口重新递归复走，重建 listing
3. 与磁盘上现有产物逐行 diff（容许末尾换行差异）
4. 统计 .byte 断点 / 非法助记符 / undefined 操作数残留
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
import sys, os, re, json, random, difflib

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


def walk(entry):
    seen = {}
    work = [entry - BASE]
    while work:
        pc = work.pop()
        while True:
            if pc in seen or pc < 0 or pc >= len(d):
                break
            sz, nm, a1, a2, nxt = h.decode(pc)
            if nm is None:
                seen[pc] = None
                break
            seen[pc] = (sz, nm, a1, a2)
            if nm == 'rts':
                break
            if nm in CALLS:
                pass
            elif nm in UNCOND:
                t = parse_tgt(a1)
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
                break
            elif nm in NEVER:
                pass
            elif nm in CONDS:
                t = parse_tgt(a1)
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen


def fmt(seen, pc):
    v = seen.get(pc)
    if v is None:
        return f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}'
    sz, nm, a1, a2 = v
    return f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)


# 合法助记符表（来自 h8.lst）
MNEM = set()
for l in open(sample('h8.lst'), encoding='utf-8', errors='replace'):
    m = re.match(r'^([0-9a-f]{2,16})\s+([0-9a-f]{2,16})\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)', l)
    if m:
        MNEM.add(m.group(4).lower())

LINE = re.compile(r'^(0x[0-9A-Fa-f]{6})\s+(\S+)\s*(.*)$')


def quality(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    lines = [l for l in txt.split('\n') if l.strip()]
    n_byte = sum(1 for l in lines if '.byte' in l)
    n_undef = sum(1 for l in lines if 'undefined' in l.lower())
    n_none = sum(1 for l in lines if re.search(r'\bNone\b', l))
    n_illegal = 0
    illegal = []
    for l in lines:
        m = LINE.match(l.strip())
        if not m:
            continue
        op = m.group(2).lower()
        if op != '.byte' and op not in MNEM:
            n_illegal += 1
            illegal.append(l.strip())
    # 地址单调性
    addrs = [int(LINE.match(l.strip()).group(1), 16) for l in lines if LINE.match(l.strip())]
    mono = all(addrs[i] < addrs[i + 1] for i in range(len(addrs) - 1))
    # 地址步进合理性：单条指令长度 2..10 且递增
    return dict(lines=len(lines), byte_breaks=n_byte, undefined=n_undef,
                none_literals=n_none, illegal_mnemonic=n_illegal, illegal_samples=illegal[:5],
                addr_monotonic=mono, n_addrs=len(addrs),
                first=lines[0] if lines else None, last=lines[-1] if lines else None)


def main():
    random.seed(20261025)
    fixs = sorted(f for f in os.listdir(JOBS) if re.match(r'^fix_[0-9A-Fa-f]{6}\.asm$', f))
    boots = sorted(f for f in os.listdir(JOBS) if re.match(r'^boot_.*\.asm$', f))
    picks = random.sample(fixs, 3) + [boots[0]]
    print('抽样（seed=20261025）:', picks)
    report = {}
    for p in picks:
        path = os.path.join(JOBS, p)
        q = quality(path)
        # 重新解码 diff（boot_*.asm 来自引导块样本，地址=文件偏移，不适用应用 ROM）
        diff = None
        if p.startswith('fix_'):
            entry = int(p[4:10], 16)
            seen = walk(entry)
            rebuilt = [fmt(seen, pc) for pc in sorted(seen)]
            orig = [l for l in open(path, encoding='utf-8', errors='replace').read().split('\n') if l.strip()]
            diff = dict(
                rebuilt_lines=len(rebuilt), orig_lines=len(orig),
                identical=(rebuilt == orig),
                diff_count=sum(1 for _ in difflib.unified_diff(orig, rebuilt, lineterm='')),
            )
            if rebuilt != orig:
                dl = list(difflib.unified_diff(orig, rebuilt, lineterm=''))[:20]
                diff['diff_head'] = dl
        print()
        print('=' * 70)
        print(p)
        print('=' * 70)
        for k, v in q.items():
            print(f'  {k}: {v}')
        if diff:
            print('  -- 重新解码 diff --')
            for k, v in diff.items():
                print(f'     {k}: {v}')
        report[p] = dict(quality=q, diff=diff)

    with open(os.path.join(HERE, 'sample_quality.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)

    ok = all(q['byte_breaks'] == 0 and q['undefined'] == 0 and q['none_literals'] == 0
             and q['illegal_mnemonic'] == 0 and q['addr_monotonic']
             for q in (r['quality'] for r in report.values()))
    d_ok = all((r['diff'] is None) or r['diff']['identical'] for r in report.values())
    print()
    print(f'抽样质量结论: {"全部通过" if ok else "存在异常"}   逐行重解码一致: {d_ok}')


if __name__ == '__main__':
    main()
