"""B16：36 个「解码空洞」函数用修复版解码器复走。
- 旧解码器（h8tab.py）丢弃 6 条 6 字节模式表项 → 10 字节指令 `mov.l @(d:32,ERn),ERm`
  等永不解出，反汇编出现 .byte 断点并漏跟后续代码。
- 本脚本用 h8fix.py 的修复版做递归反汇编，输出：
  (a) 每个函数的完整 listing
  (b) 旧版不可解、新版可解的指令清单（含前后各 3 条上下文，便于判断语义）
只读 D:\，产物写入本目录。
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
import sys, os, json
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h8dis import H8
from h8tab import load_entries
from h8fix import load_entries_fixed

BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
h_old = H8(d, load_entries(sample('h8.lst')), base=BASE)
h_new = H8(d, load_entries_fixed(sample('h8.lst')), base=BASE)
OUT = os.path.dirname(os.path.abspath(__file__))
CFG = cfg('cfg_v4.json')

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


def walk(entry, h):
    """递归反汇编：线性流 + 分支目标入队，rts 停，jsr/bsr 记边不展开。"""
    seen = {}
    edges = []
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
                edges.append((pc + BASE, 'call', parse_tgt(a1)))
            elif nm in UNCOND:
                t = parse_tgt(a1)
                edges.append((pc + BASE, 'jmp', t))
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
                break
            elif nm in NEVER:
                edges.append((pc + BASE, 'never', parse_tgt(a1)))
            elif nm in CONDS:
                t = parse_tgt(a1)
                edges.append((pc + BASE, 'bcc', t))
                if t is not None and 0 <= t - BASE < len(d):
                    work.append(t - BASE)
            pc = nxt
    return seen, edges


def fmt(seen, pc):
    v = seen.get(pc)
    if v is None:
        return f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}'
    sz, nm, a1, a2 = v
    return f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)


def main():
    cfg = json.load(open(CFG))
    own = cfg['owner']
    funcs = {}
    for a, f in own.items():
        funcs.setdefault(f, []).append(int(a, 16))

    # 找出带洞函数：旧版解不出、新版能解出的指令所在函数
    holes = {}
    for f, addrs in funcs.items():
        for a in addrs:
            off = a - BASE
            if h_old.decode(off)[1] is None and h_new.decode(off)[1] is not None:
                holes.setdefault(f, []).append(a)

    report = []
    total_new = 0
    for f in sorted(holes, key=lambda k: int(k, 16)):
        entry = int(f, 16)
        seen, edges = walk(entry, h_new)
        new_ins = [pc for pc in sorted(seen)
                   if seen[pc] is not None and h_old.decode(pc - BASE)[1] is None]
        total_new += len(new_ins)
        lines = [fmt(seen, pc) for pc in sorted(seen)]
        open(os.path.join(OUT, f'fix_{entry:06X}.asm'), 'w').write('\n'.join(lines) + '\n')
        # 新解出指令 + 上下文
        ctx = []
        for pc in new_ins:
            i = sorted(seen).index(pc)
            lo = max(0, i - 3)
            hi = min(len(seen), i + 4)
            ctx.append('    ---')
            for j in range(lo, hi):
                mark = '>>' if sorted(seen)[j] == pc else '  '
                ctx.append(f'    {mark} ' + fmt(seen, sorted(seen)[j]))
        report.append((entry, len(holes[f]), len(seen), len(new_ins), ctx))

    print('=' * 78)
    print('B16 复走结果（修复版解码器）')
    print('=' * 78)
    print(f'{"函数":>12} {"旧空洞":>6} {"修复版指令":>10} {"新解出":>6}')
    for entry, nh, nseen, nnew, ctx in report:
        print(f'  0x{entry:06X} {nh:>6} {nseen:>10} {nnew:>6}')
    print(f'\n带洞函数 {len(report)} 个，新解出指令合计 {total_new} 条\n')

    for entry, nh, nseen, nnew, ctx in report:
        if not ctx:
            continue
        print('-' * 78)
        print(f'fn 0x{entry:06X}  （新解出 {nnew} 条）')
        print('\n'.join(ctx))

    with open(os.path.join(OUT, 'fix36_summary.txt'), 'w') as f:
        f.write('B16 复走结果\n')
        for entry, nh, nseen, nnew, ctx in report:
            f.write(f'\nfn 0x{entry:06X}  旧空洞 {nh}  修复版指令 {nseen}  新解出 {nnew}\n')
            f.write('\n'.join(ctx) + '\n')


if __name__ == '__main__':
    main()
