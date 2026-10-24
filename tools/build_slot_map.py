"""
LS8000 固件逆向 —— E0/C1 参数槽位图谱生成器

用途
----
产出 `04_disasm/slot_map.json`：把 `0x400408`–`0x400414` 这组「参数暂存槽位」
的**全部读写点**逐条列出，并标注每个槽位是「32 位整体槽」还是「独立字节槽」。

为什么需要这个
--------------
这组槽位在旧文档里被当作单个字段描述，导致多处矛盾：
`0x400408` 被 3 个执行臂 + 1 个片夹区用**四种不同机制**写入；
`0x400411` 却没有独立写入点（它是被 32 位写覆盖的高 16 位）。
把全部引用点一次性摊开，矛盾就自然消解。

用法
----
    python build_slot_map.py [--json]
"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)


def _setup():
    """把包内 tools/ 与含 h8fix.py 的目录加入 sys.path（向上查找，避免写死层级）。"""
    cands = [os.path.join(PKG, 'tools')]
    # 向上查找含 h8fix.py 的目录
    p = HERE
    for _ in range(6):
        p = os.path.dirname(p)
        if not p:
            break
        cands.append(p)
        cands.append(os.path.join(p, 'tools', 'scripts', 'firmware', '_jobfuncs'))
        cands.append(os.path.join(p, '03_analysis', 'firmware', '_jobfuncs'))
    for d in cands:
        if d and os.path.isdir(d) and d not in sys.path:
            sys.path.insert(0, d)


def _rom_path():
    try:
        from paths import sample
        p = sample('LS8000_111_ROM.bin')
        if os.path.isfile(p):
            return p
    except Exception:
        pass
    c = os.environ.get('LS8000_SAMPLE_ROOT', 'D:/DS/TEST/LS8000')
    p = os.path.join(c.replace('\\', '/'), 'LS8000_111_ROM.bin')
    return p if os.path.isfile(p) else None


# 槽位 → 语义备注（均来自逐指令实测）
SLOT_NOTES = {
    '0x400408': '参数暂存主槽。4 个写点：C1臂/A0臂/B3臂(payload[2..5] 重排相加) + 片夹识别区(RAM 算术)',
    '0x40040A': '只读槽，被 6 处作业函数消费',
    '0x40040C': '32 位槽(=payload[7..9] 重排)。3 写 4 读，A0 作业链消费',
    '0x400410': '属于 0x40040C 的 32 位写的低 16 位区域，被 7 处消费',
    '0x400411': '是 0x40040C 那次 32 位写的高 16 位 ⇒ 无独立写点',
    '0x400412': '独立字节槽：B3臂存 payload[1]；组装器读出放到块 +0x0C',
    '0x400413': '独立字节槽：0x91/0x92 写入；组装器读出放到块 +0x0A',
    '0x400414': '独立字节槽：0x91/0x92 写入；组装器读出放到块 +0x0B',
}

SLOT_RE = re.compile(r'0x4004(0[89a-f]|1[0-4])\b')


def _find_h8lst():
    """向上查找 h8.lst（工作区在 _pkgtool/，包内在 tools/）。"""
    cands = [os.path.join(PKG, 'tools', 'h8.lst'), os.path.join(HERE, 'h8.lst')]
    p = HERE
    for _ in range(6):
        p = os.path.dirname(p)
        if not p:
            break
        cands.append(os.path.join(p, 'tools', 'h8.lst'))
        cands.append(os.path.join(p, '03_analysis', 'tools', 'h8.lst'))
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return cands[0]


def main():
    _setup()
    from h8dis import H8
    from h8fix import load_entries_fixed

    rom_path = _rom_path()
    if not rom_path:
        print('找不到 ROM 样本；请设置 LS8000_SAMPLE_ROOT')
        return 1

    rom = open(rom_path, 'rb').read()
    lst = _find_h8lst()
    if not os.path.isfile(lst):
        print('找不到 h8.lst（尝试过: %s）' % lst)
        return 1
    h = H8(rom, load_entries_fixed(lst), base=0x10000)

    refs = {}
    for off in range(len(rom) - 6):
        try:
            r = h.decode(off + 0x10000 - 0x10000)
        except Exception:
            continue
        if r[1] is None:
            continue
        txt = '%s %s %s' % (r[1], r[2], r[3])
        m = SLOT_RE.search(txt)
        if not m:
            continue
        slot = '0x4004' + m.group(1)
        # 判断读写方向：
        #   解码器输出格式为 "mnemonic <op1> <op2>"，其中 **目标操作数在前、源在后**
        #   （H8 的 dest 在前，与 x86 相反）：
        #       "mov.l er0 @0x400408"  → 写（er0 是源，@0x400408 是目标）
        #       "mov.b @0x400412 r0l"  → 读（@0x400412 是源）
        #   判据：该地址若带 @ 前缀（出现在 " @ADDR" 位置）⇒ 写；
        #        若是源位置（"@ADDR ..." 出现在操作数区开头）⇒ 读。
        is_write = bool(re.search(r'@\s*' + re.escape(slot) + r'\s*$', txt))
        refs.setdefault(slot, {'reads': [], 'writes': []})
        entry = {'addr': '0x%06X' % (off + 0x10000), 'insn': txt.strip()}
        refs[slot]['writes' if is_write else 'reads'].append(entry)

    out = {
        'note': 'E0/C1 参数暂存槽位引用图谱（0x400408–0x400414）',
        'rom': rom_path,
        'rom_sha256': __import__('hashlib').sha256(rom).hexdigest(),
        'decoder': 'h8fix.py（修复版，399 表项）',
        'slots': {},
    }
    print('=' * 68)
    print('LS8000 E0/C1 参数槽位图谱')
    print('=' * 68)
    for slot in sorted(refs):
        d = refs[slot]
        out['slots'][slot] = {
            'writes': d['writes'], 'reads': d['reads'],
            'write_count': len(d['writes']), 'read_count': len(d['reads']),
            'note': SLOT_NOTES.get(slot, ''),
        }
        print('%-10s 写 %d  读 %d   %s'
              % (slot, len(d['writes']), len(d['reads']),
                 SLOT_NOTES.get(slot, '')[:60]))

    print()
    print('【写点明细】')
    for slot in sorted(refs):
        for w in refs[slot]['writes']:
            print('  %-10s %s   %s' % (slot, w['addr'], w['insn']))

    print()
    print('【读点明细】')
    for slot in sorted(refs):
        for rd in refs[slot]['reads']:
            print('  %-10s %s   %s' % (slot, rd['addr'], rd['insn']))

    if '--json' in sys.argv:
        p = os.path.join(PKG, '04_disasm', 'slot_map.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
        print()
        print('已写出: %s' % p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
