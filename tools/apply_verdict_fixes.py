"""
LS8000 —— 打包阶段实测更正的批量回写脚本

对下列文档中「校验对象 = V1 = payload[1..4]（32 位 BE）」这类已被打包阶段
逐指令实测证伪的表述，做精准更正并留下痕迹。

背景
----
打包阶段逐条反汇编 `0x026D10`–`0x026D74`（`er3` 装载链）后确认：

    er3 = (payload[1]<<8) + (payload[2]<<8) + (payload[3]<<16) + payload[4]
        + (payload[5]<<8) + (payload[6]<<8) + (payload[7]<<16) + payload[8]

即 **8 个 payload 字节经「重排 + 相加」拼成的 32 位模式**，不是 payload[1..4] 的大端。
同时 `0x026DAE` 起是**按子功能号（CDB[2]）分派的校验表**（12 分支），
「六数值门限依次校验同一个 V1」这个描述同样不准确。

本脚本只做「字符串级精准替换」，不重写段落结构；每条替换都要求原串唯一存在，
匹配不到就跳过并报告，绝不盲改。
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# 脚本位于 <工作区>/03_analysis/_pkgtool/ → 工作区根是上两级
ROOT = os.path.dirname(os.path.dirname(_HERE))

# (相对路径, [(原串, 新串), ...])
FIXES = [
    ('REPORT_全面分析总结-20261024.md', [
        ('**校验对象 = 32 位大端参数 V1 = `payload[1..4]`**（不是 CDB 字节、不是子功能码）：',
         '**校验对象 = `er3`，由 payload[1..8] 经「重排 + 相加」拼成的 32 位模式**'
         '（位段：bit23-16 ← P2+P6，bit15-8 ← P1+P5，bit7-0 ← P3+P4+P7+P8）；'
         '**不是** `payload[1..4]` 的 32 位大端：'
         '\n\n> **打包阶段实测更正（R22）**：`er3` 的真实装载链在 `0x026D10`–`0x026D74`，'
         '且 `0x026DAE` 起是**按子功能号（CDB[2]）分派的校验表**（12 分支、6 个校验值、'
         '其中 `0x80`/`0x81`/`0xB0`/`0xD0` 完全不校验）。'
         '证据与复现命令见 `03_analysis/firmware/E0子功能分派与校验表-实测补全.md`。'),
    ]),

    ('REPORT_回写总账-20261024.md', [
        ('**校验对象 = V1 = `payload[1..4]`（32 位 BE）**；越界 → `0x53`',
         '**校验对象 = `er3` = payload[1..8] 重排相加（**打包阶段 R22 实测更正**：'
         '非 `payload[1..4]` 的 32 位 BE）；越界 → `0x53`'),
    ]),

    ('03_analysis/firmware/_jobfuncs/交叉结论-给实机验证线-20261024.md', [
        ('**关键点（纠正一个容易踩的坑）**：被比较的量 `er3` **不是 CDB 字节**，而是 **32 位大端参数 V1 = payload[1..4]**：',
         '**关键点（纠正一个容易踩的坑）**：被比较的量 `er3` **不是 CDB 字节**，'
         '而是 **payload[1..8] 经「重排 + 相加」拼成的 32 位模式**'
         '（bit23-16 ← P2+P6，bit15-8 ← P1+P5，bit7-0 ← P3+P4+P7+P8）；'
         '**打包阶段实测更正**：不是 payload[1..4] 的 32 位大端 ——'),
        ('| 3 | 若要抓参数，抓 **data-out 缓冲**（不是 CDB） | 零 | V1 = payload[1..4] |',
         '| 3 | 若要抓参数，抓 **data-out 缓冲**（不是 CDB） | 零 | '
         '`er3` 由 payload[1..8] 重排相加（R22 实测更正） |'),
        ('| 数值门限对象不明 | **V1 = payload[1..4]（32 位 BE）**，在 data-out 里 |',
         '| 数值门限对象不明 | **`er3` = payload[1..8] 重排相加**（R22 实测更正），在 data-out 里 |'),
    ]),
]


def apply_one(path, pairs):
    if not os.path.isfile(path):
        return ('SKIP', 0, ['文件不存在: %s' % path])
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    orig = src
    notes = []
    changed = 0
    for old, new in pairs:
        n = src.count(old)
        if n == 0:
            notes.append('未匹配（跳过）: %s' % (old[:48] + ('…' if len(old) > 48 else '')))
            continue
        if n > 1:
            notes.append('出现 %d 次，跳过（需人工确认）: %s'
                         % (n, old[:48] + ('…' if len(old) > 48 else '')))
            continue
        src = src.replace(old, new)
        changed += 1
        notes.append('OK: %s' % (old[:48] + ('…' if len(old) > 48 else '')))
    if src != orig:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(src)
    return ('DONE' if changed else 'NOCHANGE', changed, notes)


def main():
    print('=' * 66)
    print('打包阶段实测更正 —— 批量回写')
    print('=' * 66)
    total = 0
    for rel, pairs in FIXES:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        status, changed, notes = apply_one(p, pairs)
        print()
        print('[%s] %s  (%d 处)' % (status, rel, changed))
        for n in notes:
            print('    %s' % n)
        total += changed
    print()
    print('合计更正 %d 处' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
