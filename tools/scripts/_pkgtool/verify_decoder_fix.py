"""
LS8000 固件逆向 —— 解码器缺陷量化核验脚本

用途
----
独立复现「自建 H8 解码器的模式表正则缺陷导致 10 字节指令永不解出」这一结论，
并给出可机读的证据文件。

背景
----
`h8tab.py`（原版）的表项加载正则上限是 8 位十六进制：
    re.match(r"^([0-9a-f]{2,8})\\s+([0-9a-f]{2,8})\\s+...", line)
而 6 字节模式表项的 val/mask 是 **12 位十六进制**，整行被 `if not m: continue` 跳过，
导致 6 条模式丢失 —— 其中包含 `mov.l @(d:32,ERn),ERm` 这族 **10 字节指令**。

`h8fix.py`（修复版）把正则放宽到 16 位并补齐 `len(M)==6` 分支的 `vv` 赋值，
表项数由 393 增至 399。

本脚本做两件事：
  1. 列出新增的 6 条表项（应当全部 size=10）
  2. 全 ROM 扫描，找出「原版解不出 / 修复版可解」的全部位置

用法
----
    python verify_decoder_fix.py            # 打印结果
    python verify_decoder_fix.py --json     # 同时写出 decoder_fix_sites.json
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)


def _setup():
    """把包内 tools/ 与 _jobfuncs/ 加入 sys.path。"""
    for d in (os.path.join(PKG, 'tools'),
              os.path.join(PKG, 'tools', 'scripts', 'firmware', '_jobfuncs')):
        if os.path.isdir(d):
            sys.path.insert(0, d)


def _sample_root():
    try:
        from paths import sample
        return sample('LS8000_111_ROM.bin')
    except Exception:
        return sample('LS8000_111_ROM.bin')


def main():
    _setup()
    from h8dis import H8
    from h8tab import load_entries
    from h8fix import load_entries_fixed

    lst = os.path.join(PKG, 'tools', 'h8.lst')
    rom_path = _sample_root()
    if not os.path.isfile(rom_path):
        print('找不到 ROM 样本: %s' % rom_path)
        print('请设置环境变量 LS8000_SAMPLE_ROOT 指向样本目录')
        return 1
    rom = open(rom_path, 'rb').read()

    old_entries = load_entries(lst)
    new_entries = load_entries_fixed(lst)

    print('=' * 68)
    print('LS8000 解码器缺陷量化核验')
    print('=' * 68)
    print('  ROM 样本   : %s (%d B)' % (rom_path, len(rom)))
    print('  模式表     : %s' % lst)
    print('  原版表项   : %d' % len(old_entries))
    print('  修复版表项 : %d   (差额 %d)' % (len(new_entries),
                                             len(new_entries) - len(old_entries)))
    print()

    # 1) 新增表项
    oldset = {(e['name'], e['am1'], e['am2'], e['vm'], e['vv']) for e in old_entries}
    added = [e for e in new_entries
             if (e['name'], e['am1'], e['am2'], e['vm'], e['vv']) not in oldset]
    print('【1】新增表项 %d 条' % len(added))
    for e in added:
        print('    %-10s %-11s %-11s size=%-3d vm=%08X vv=%08X'
              % (e['name'], e['am1'], e['am2'], e['size'], e['vm'], e['vv']))
    all10 = all(e['size'] == 10 for e in added)
    print('    ⇒ 全部 size=10 : %s' % ('是' if all10 else '否'))
    print()

    # 2) 全 ROM 扫描
    old = H8(rom, old_entries, base=0x10000)
    new = H8(rom, new_entries, base=0x10000)

    def dec(h, off):
        try:
            r = h.decode(off + 0x10000)
        except Exception:
            return None
        return None if r[1] is None else (r[0], r[1], r[2], r[3])

    rows = []
    for off in range(len(rom) - 10):
        if dec(old, off) is None and dec(new, off) is not None:
            n = dec(new, off)
            rows.append((off + 0x10000, n[0], n[1], n[2]))

    print('【2】全 ROM 扫描「原版解不出 / 修复版可解」位置')
    print('    命中数 : %d' % len(rows))
    if rows:
        sizes = Counter(r[1] for r in rows)
        mns = Counter(r[2] for r in rows)
        print('    指令长度分布 : %s' % dict(sizes))
        print('    助记符分布   : %s' % dict(mns))
        print('    前 10 处:')
        for a, sz, mn, a1 in rows[:10]:
            print('      0x%06X  size=%-3d %s %s' % (a, sz, mn, a1))
    print()

    print('【3】结论')
    print('    缺陷根因 : 原版正则上限 8 位十六进制，装不下 12 位的 6 字节模式行')
    print('    直接后果 : %d 条模式丢失 → 10 字节指令族永不解出' % len(added))
    print('    实测影响 : %d 处指令位置在原版下不可见' % len(rows))
    print('    复走收益 : 36 个带洞函数递归复走，合计多解出 1299 条指令')
    print('               （见 04_disasm/fix36_summary.txt）')

    if '--json' in sys.argv:
        out = {
            'note': '原版 h8tab.py 解不出、修复版 h8fix.py 可解出的指令位置',
            'rom': rom_path,
            'rom_sha256': __import__('hashlib').sha256(rom).hexdigest(),
            'old_entries': len(old_entries),
            'fixed_entries': len(new_entries),
            'added_entries': [
                {'name': e['name'], 'am1': e['am1'], 'am2': e['am2'],
                 'size': e['size'], 'vm': e['vm'], 'vv': e['vv']}
                for e in added],
            'hit_count': len(rows),
            'all_size_10': all(r[1] == 10 for r in rows),
            'by_size': {str(k): v for k, v in Counter(r[1] for r in rows).items()},
            'by_mnemonic': {str(k): v for k, v in Counter(r[2] for r in rows).items()},
            'sites': [{'addr': '0x%06X' % a, 'size': sz, 'mnemonic': mn,
                       'arg1': str(a1)} for a, sz, mn, a1 in rows],
        }
        p = os.path.join(PKG, '04_disasm', 'decoder_fix_sites.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
        print()
        print('已写出: %s' % p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
