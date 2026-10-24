"""核算 36 份 fix_*.asm 的「去重覆盖」与「新解出指令去重数」。

背景：36 个「函数」实为 cfg_v4 owner 的 36 个伪入口分组，其中若干区间互相重叠
（同一段代码被多份文件重复列出）。因此：
- 36 份文件的指令条数之和 = 8927（含重复）
- 去重后的实际覆盖指令数 = ?
- 「新解出 1299」在去重后是多少？

本脚本重跑修复版解码器，收集全部新解出指令的地址集合，做去重统计。
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
import sys, os, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, JOBS)
from h8dis import H8
from h8tab import load_entries
from h8fix import load_entries_fixed

BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
h_old = H8(d, load_entries(sample('h8.lst')), base=BASE)
h_new = H8(d, load_entries_fixed(sample('h8.lst')), base=BASE)

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


def main():
    cfg = json.load(open(cfg('cfg_v4.json')))
    own = cfg['owner']
    funcs = {}
    for a, f in own.items():
        funcs.setdefault(f, []).append(int(a, 16))
    holes = {}
    for f, addrs in funcs.items():
        for a in addrs:
            off = a - BASE
            if h_old.decode(off)[1] is None and h_new.decode(off)[1] is not None:
                holes.setdefault(f, []).append(a)

    all_seen = set()
    all_new = set()
    per = {}
    for f in sorted(holes, key=lambda k: int(k, 16)):
        entry = int(f, 16)
        seen = walk(entry, h_new)
        new = {pc for pc in seen if seen[pc] is not None and h_old.decode(pc - BASE)[1] is None}
        all_seen |= set(seen)
        all_new |= new
        per['0x%06X' % entry] = dict(n_seen=len(seen), n_new=len(new),
                                     new_addrs=sorted('0x%06X' % (p + BASE) for p in new))

    # 汇总
    sum_seen = sum(v['n_seen'] for v in per.values())
    sum_new = sum(v['n_new'] for v in per.values())
    # 洞点数
    n_hole_sites = sum(len(v) for v in holes.values())
    hole_addr_set = set()
    for v in holes.values():
        hole_addr_set |= set(v)

    print('=' * 74)
    print('36 组覆盖与「新解出」去重核算')
    print('=' * 74)
    print(f'36 组伪入口（cfg_v4 owner 分组）      : {len(per)}')
    print(f'洞点数（有洞函数内，旧解不出新解得出）  : {n_hole_sites}  (去重地址 {len(hole_addr_set)})')
    print(f'各组指令数之和（含跨组重复）             : {sum_seen}')
    print(f'各组「新解出」之和（含跨组重复）         : {sum_new}')
    print(f'去重后覆盖指令总数（36 组并集）         : {len(all_seen)}')
    print(f'去重后「新解出」指令总数                : {len(all_new)}')
    print(f'重复率：指令 {sum_seen}/{len(all_seen)} = {sum_seen/len(all_seen):.2f}x')
    print(f'        新解出 {sum_new}/{len(all_new)} = {sum_new/len(all_new):.2f}x')
    print()
    print('=== 42 个洞点地址（去重）===')
    for a in sorted(hole_addr_set):
        print(f'  0x{a:06X}   (旧解不出 → 新解出 10 字节指令)')

    with open(os.path.join(HERE, 'dedup.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(
            groups=len(per), hole_sites=n_hole_sites, hole_addr_count=len(hole_addr_set),
            sum_seen=sum_seen, sum_new=sum_new,
            union_seen=len(all_seen), union_new=len(all_new),
            hole_addrs=sorted('0x%06X' % a for a in hole_addr_set),
            per=per), f, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
