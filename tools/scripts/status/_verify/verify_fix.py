"""核实解码器修复量：h8fix.py(修复版) vs h8tab.py(原版)。

只读 D:/DS/TEST/LS8000，产物只写本工作区 _verify/ 目录。
复刻 fix36.py 的算法（递归反汇编 + 新解出指令统计），并与
fix36_summary.txt 交叉验证：洞点数 / 函数数 / 新解出指令数。
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
import sys, os, json, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))                    # .../03_analysis/status/_verify
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, JOBS)
from h8dis import H8
from h8tab import load_entries
from h8fix import load_entries_fixed

BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
LST = sample('h8.lst')
CFG = cfg('cfg_v4.json')

old_ent = load_entries(LST)
new_ent = load_entries_fixed(LST)
h_old = H8(d, old_ent, base=BASE)
h_new = H8(d, new_ent, base=BASE)

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
    seen, edges = {}, []
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


def main():
    out = {}
    out['rom_bytes'] = len(d)
    out['entries_old'] = len(old_ent)
    out['entries_new'] = len(new_ent)
    out['entries_delta'] = len(new_ent) - len(old_ent)

    # 1) 全镜像 2 字节对齐点扫描：旧解不出、新解得出
    n_fix = 0
    sites = []
    for off in range(0, len(d) - 10, 2):
        if h_old.decode(off)[1] is None and h_new.decode(off)[1] is not None:
            n_fix += 1
            sites.append(off + BASE)
    out['image_2byte_align_fixed_sites'] = n_fix
    out['image_first_40_sites'] = ['0x%06X' % x for x in sites[:40]]

    # 2) cfg owner 洞点（fix36.py 同法）
    cfg = json.load(open(CFG))
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
    out['cfg_hole_functions'] = len(holes)
    out['cfg_hole_sites_total'] = sum(len(v) for v in holes.values())

    # 3) 逐函数复走（新解出指令数）
    rows = []
    total_new = 0
    total_seen = 0
    total_holes = 0
    for f in sorted(holes, key=lambda k: int(k, 16)):
        entry = int(f, 16)
        seen, edges = walk(entry, h_new)
        new_ins = [pc for pc in sorted(seen)
                   if seen[pc] is not None and h_old.decode(pc - BASE)[1] is None]
        # 旧版复走对比：同一入口用旧解码器走一遍，看能解多少
        seen_old, _ = walk(entry, h_old)
        total_new += len(new_ins)
        total_seen += len(seen)
        total_holes += len(holes[f])
        rows.append(dict(
            entry='0x%06X' % entry,
            holes=len(holes[f]),
            fix_ins=len(seen),
            new_decoded=len(new_ins),
            old_ins=len(seen_old),
            old_byte_breaks=sum(1 for v in seen_old.values() if v is None),
            new_byte_breaks=sum(1 for v in seen.values() if v is None),
            edges=len(edges),
            hole_addrs=['0x%06X' % a for a in sorted(holes[f])],
        ))
    out['rows'] = rows
    out['total_holes'] = total_holes
    out['total_fix_ins'] = total_seen
    out['total_new_decoded'] = total_new
    out['total_old_ins'] = sum(r['old_ins'] for r in rows)
    out['total_old_byte_breaks'] = sum(r['old_byte_breaks'] for r in rows)
    out['total_new_byte_breaks'] = sum(r['new_byte_breaks'] for r in rows)

    # 4) 与 fix36_summary.txt 交叉验证
    summary = os.path.join(JOBS, 'fix36_summary.txt')
    srows = []
    for l in open(summary, encoding='utf-8', errors='replace'):
        m = re.match(r'^fn 0x([0-9A-Fa-f]{6})\s+旧空洞\s+(\d+)\s+修复版指令\s+(\d+)\s+新解出\s+(\d+)', l)
        if m:
            srows.append(dict(entry='0x' + m.group(1).upper(), holes=int(m.group(2)),
                              fix_ins=int(m.group(3)), new_decoded=int(m.group(4))))
    out['summary_rows'] = srows
    out['summary_tot_holes'] = sum(r['holes'] for r in srows)
    out['summary_tot_fix_ins'] = sum(r['fix_ins'] for r in srows)
    out['summary_tot_new'] = sum(r['new_decoded'] for r in srows)

    # 逐函数一致性
    smap = {r['entry']: r for r in srows}
    mism = []
    for r in rows:
        s = smap.get(r['entry'])
        if s is None:
            mism.append((r['entry'], 'missing_in_summary'))
        elif (s['holes'], s['fix_ins'], s['new_decoded']) != (r['holes'], r['fix_ins'], r['new_decoded']):
            mism.append((r['entry'], f"summary=({s['holes']},{s['fix_ins']},{s['new_decoded']}) "
                                    f"rerun=({r['holes']},{r['fix_ins']},{r['new_decoded']})"))
    out['mismatches'] = mism
    out['consistent'] = (len(mism) == 0 and len(srows) == len(rows))

    # 5) 与 fix_*.asm 产物比对（行数 = 复走指令数）
    filecheck = []
    for r in rows:
        p = os.path.join(JOBS, 'fix_%s.asm' % r['entry'][2:])
        if os.path.exists(p):
            txt = open(p, encoding='utf-8', errors='replace').read()
            nl = len([x for x in txt.split('\n') if x.strip()])
            nb = len([x for x in txt.split('\n') if '.byte' in x])
            filecheck.append(dict(entry=r['entry'], file_lines=nl, expect=r['fix_ins'],
                                   byte_lines=nb, new_byte=r['new_byte_breaks'],
                                   match=(nl == r['fix_ins'])))
        else:
            filecheck.append(dict(entry=r['entry'], file_lines=None, expect=r['fix_ins'], missing=True))
    out['file_check'] = filecheck
    out['file_all_match'] = all(f.get('match') for f in filecheck)

    # 6) 关键解码器验证点
    probes = []
    for a in (0x03A6CE, 0x03A6E6):
        o = h_old.decode(a - BASE)
        n = h_new.decode(a - BASE)
        probes.append(dict(addr='0x%06X' % a,
                           old=(None if o[1] is None else f'{o[1]} {o[2]}'),
                           new=(None if n[1] is None else f'{n[1]} {n[2]}'),
                           old_size=o[0], new_size=n[0]))
    out['probes'] = probes

    with open(os.path.join(HERE, 'verify_result.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    print('=' * 70)
    print('解码器修复量核实（h8fix vs h8tab）')
    print('=' * 70)
    print(f"ROM bytes            : {out['rom_bytes']}")
    print(f"h8.lst 条目 old/new  : {out['entries_old']} / {out['entries_new']}  (delta {out['entries_delta']})")
    print(f"全镜像2字节对齐修复点: {out['image_2byte_align_fixed_sites']}")
    print(f"cfg owner 洞函数/洞点 : {out['cfg_hole_functions']} / {out['cfg_hole_sites_total']}")
    print(f"复走合计: 修复版指令 {out['total_fix_ins']}  新解出 {out['total_new_decoded']}")
    print(f"旧版复走: 指令 {out['total_old_ins']}  .byte 断点 {out['total_old_byte_breaks']}")
    print(f"新版复走: .byte 断点 {out['total_new_byte_breaks']}")
    print(f"summary 合计: 洞 {out['summary_tot_holes']}  指令 {out['summary_tot_fix_ins']}  新解出 {out['summary_tot_new']}")
    print(f"逐函数一致: {out['consistent']}   mismatches={out['mismatches']}")
    print(f"fix_*.asm 行数全匹配: {out['file_all_match']}")
    print(f"探针: {out['probes']}")
    print()
    print(f"{'entry':>10} {'holes':>6} {'fix_ins':>8} {'new':>6} {'old_ins':>8} {'oldBB':>6} {'newBB':>6} {'edges':>6}")
    for r in rows:
        print(f"{r['entry']:>10} {r['holes']:>6} {r['fix_ins']:>8} {r['new_decoded']:>6} "
              f"{r['old_ins']:>8} {r['old_byte_breaks']:>6} {r['new_byte_breaks']:>6} {r['edges']:>6}")


if __name__ == '__main__':
    main()
