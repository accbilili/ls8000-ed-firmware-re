"""
LS8000 —— 前轮专题报告一致性自动核对（打包阶段）

目的
----
`D:\\DS\\TEST\\LS8000\\` 顶层有 32 份前轮（10/4–10/5）专题报告。
本脚本逐份读取，与「当前权威口径」做机械比对，找出**仍写着已被推翻说法**的段落，
生成一份可核对的索引 + 修正清单。

已知需要检查的「已被推翻说法」（每条都对应回写总账里的 R 编号）：
  1. 引导块「不在镜像内 / 需另做 flash dump」
  2. `0x400408` 「只写不读」
  3. `0x4003FB` 语义「未证实 / 待识别」
  4. `0x74` = 「116 字节行距」
  5. `0x0269A6` = 「E0 执行层」（应为 C1/EXECUTE）
  6. 作业表 `0x40` → `0x02AAAE`（应为 `0x02AEAA`）
  7. 校验对象 = 「V1 = payload[1..4]（32 位 BE）」（R22 已证伪）
  8. `0x400408` = 「BE32(V1)」或「P1<<24+(P2+P3)<<16+P4」（R23 已证伪）
  9. flash 驱动「ROM 0x17AB4 起 336 B」（应为 `0x17708` 起 880 B）
 10. flash 芯片地址「0x6000」（应为 `0x60000`/`0x70000`）
 11. `0x400D79` = 「待识别标志」（应为「识别正常标志，1=正常」）
 12. 34.8mm 计数「3512/5480」（应为 3511/5479）
 13. `0x027F24` = 「本函数终点」（应为「真子函数」）

输出
----
`03_analysis/status/PRIOR_ROUND_INDEX.md` —— 逐份索引 + 命中清单。

注意
----
- 只读 D:\\ 盘，绝不写入。
- 命中不等于「该文档整体作废」，只表示**这几处表述需要按 R 编号更正**。
- 每条命中都给出文件名、行号、原文片段，便于人工复核。
"""
import os
import re
import sys
from datetime import datetime

SRC = os.environ.get('LS8000_SAMPLE_ROOT', 'D:/DS/TEST/LS8000')
# 输出到工作区的 status/ 目录（与其它索引并列）
_STATUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'status')
try:
    os.makedirs(_STATUS, exist_ok=True)
except Exception:
    pass
OUT = os.path.join(_STATUS, 'PRIOR_ROUND_INDEX.md')

# (检查编号, 简短名, 正则, 说明, 对应 R 编号)
CHECKS = [
    ('C1', '引导块不在镜像内',
     r'引导块.{0,20}(?:不在|未包含|不含|没有).{0,20}镜像|'
     r'(?:需|需要|待|要)(?:另做|再做|补充|额外).{0,10}(?:flash|dump|导出)|'
     r'boot\s*block.{0,30}(?:not in|missing from)\s*(?:the\s*)?(?:image|mirror)',
     '声称引导块不在镜像内、需另做 flash dump', 'A1/R（已关闭）'),
    ('C2', '0x400408 只写不读',
     r'0x400408.{0,40}(?:只写不读|3\s*写\s*0\s*读|三写零读|0\s*处读)',
     '声称 0x400408 只有写没有读', 'R13'),
    ('C3', '0x4003FB 语义未证',
     r'0x4003FB.{0,30}(?:未证实|待证|待识别|语义未知|不明)',
     '声称 0x4003FB 语义未证实', 'R（第三轮已定）'),
    ('C4', '0x74 = 116 字节行距',
     r'0x74.{0,30}116\s*(?:字节|B)|(?:116\s*(?:字节|B)).{0,30}0x74',
     '声称 0x74 是 116 字节行距（实为栈帧偏移）', 'R21'),
    ('C5', '0x0269A6 = E0 执行层',
     r'0x0269A6.{0,30}(?:E0\s*执行层|E0\s*handler|E0\s*处理)|'
     r'(?:E0\s*执行层|E0\s*处理函数).{0,30}0x0269A6',
     '称 0x0269A6 是 E0 执行层（应为 C1/EXECUTE）', 'R2'),
    ('C6', '作业表 0x40 → 0x02AAAE',
     r'0x40.{0,25}0x2AAAE|0x2AAAE.{0,25}0x40',
     '称作业表 0x40 项地址是 0x02AAAE（应为 0x02AEAA）', 'R5'),
    ('C7', 'V1 = payload[1..4]（32 位 BE）',
     r'V1\s*=\s*`?payload\[1\.\.4\]|payload\[1\.\.4\].{0,20}32\s*位大端|'
     r'32\s*位大端.{0,20}payload\[1\.\.4\]',
     '称校验对象是 payload[1..4] 的 32 位大端', 'R22'),
    ('C8', '0x400408 组装公式旧说',
     r'0x400408.{0,50}(?:BE32|BE\s*32)|P1<<24|P1\s*<<\s*24',
     '称 0x400408 存 BE32(V1) 或含 P1<<24', 'R23'),
    ('C9', 'flash 驱动旧地址',
     r'0x17AB4|0x17ab4',
     '称 flash 驱动在 ROM 0x17AB4 起 336 B（应为 0x17708 起 880 B）', '第五轮更正'),
    ('C10', 'flash 芯片地址 0x6000',
     r'(?:flash|FLASH).{0,30}(?:芯片|器件).{0,20}0x6000(?![0-9A-Fa-f])|'
     r'0x6000(?![0-9A-Fa-f]).{0,20}(?:flash|FLASH).{0,20}(?:芯片|器件)',
     '称 flash 芯片地址是 0x6000（应为 0x60000/0x70000）', '第五轮更正'),
    ('C11', '0x400D79 待识别',
     r'0x400D79.{0,30}(?:待识别|未识别|未知)',
     '称 0x400D79 是待识别标志（应为识别正常标志）', 'FW_DOC_INDEX §4.2 #7'),
    ('C12', '34.8mm 计数旧值',
     r'3512|5480',
     '称 34.8mm 计数为 3512/5480（应为 3511/5479）', 'FW_DOC_INDEX §4.2 #8'),
    ('C13', '0x027F24 是函数终点',
     r'0x027F24.{0,30}(?:终点|末尾|边界)|(?:终点|末尾|边界).{0,30}0x027F24',
     '称 0x027F24 是函数终点（应为真子函数）', 'FW_DOC_INDEX §4.2 #9'),
]

# 主题关键词 → 分类
TOPIC = [
    ('引导块/flash', r'引导块|boot\s*block|flash|擦写|0x6000'),
    ('协议/命令', r'协议|CDB|E0|C1|命令|ioctl|Nikon_CommandMap'),
    ('机构/运动', r'机构|运动|电机|步进|轴|Mechanism|Focus|对焦'),
    ('片夹识别', r'片夹|holder|FilmCode|光学编码|孔位'),
    ('图像/几何', r'图像|像素|行距|ImageLayout|扫描几何|buffer'),
    ('主机侧', r'HostSide|主机|md3|驱动|dll|入口'),
    ('配置/表', r'cfg|CFG|表|Table|收敛|解析'),
    ('架构/总览', r'架构|总览|MASTER|Architecture|Map|EntryChain|OtherFirmware|FlashMap'),
]

AUTHORITATIVE = [
    ('REPORT_全面分析总结-20261024.md', '唯一总入口'),
    ('REPORT_回写总账-20261024.md', '唯一查证入口（R1–R23）'),
    ('REPORT_L3-交接定稿.md', 'L3 主报告'),
    ('LS8000-全案总结.md', '浓缩版'),
    ('HANDOFF.md', '交接入口单'),
]


def classify(text):
    tags = []
    for name, pat in TOPIC:
        if re.search(pat, text, re.I):
            tags.append(name)
    return tags or ['其它']


def main():
    if not os.path.isdir(SRC):
        print('找不到前轮报告目录: %s' % SRC)
        return 1

    files = sorted(f for f in os.listdir(SRC)
                   if f.startswith('REPORT_') and f.endswith('.md'))
    print('前轮报告 %d 份' % len(files))

    rows = []
    all_hits = []
    for f in files:
        p = os.path.join(SRC, f)
        try:
            txt = open(p, encoding='utf-8', errors='replace').read()
        except Exception as ex:
            rows.append((f, 0, ['读取失败'], ['其它'], []))
            continue
        size = os.path.getsize(p)
        hits = []
        for cid, cname, pat, desc, rno in CHECKS:
            for m in re.finditer(pat, txt, re.I):
                ln = txt.count('\n', 0, m.start()) + 1
                snippet = txt[max(0, m.start() - 40):m.end() + 40]
                snippet = ' '.join(snippet.split())
                hits.append((cid, cname, ln, snippet, rno, desc))
                all_hits.append((f, cid, cname, ln, snippet, rno))
        rows.append((f, size, hits, classify(txt), []))

    # 统计
    by_file = {}
    for f, cid, cname, ln, snip, rno in all_hits:
        by_file.setdefault(f, []).append((cid, ln, rno))
    total_hits = len(all_hits)
    clean = [r for r in rows if not r[2]]

    lines = []
    lines.append('# 前轮专题报告一致性索引（打包阶段自动核对）')
    lines.append('')
    lines.append('> 生成时间：%s' % datetime.now().strftime('%Y-%m-%d %H:%M'))
    lines.append('> 来源目录：`%s`（只读，未做任何修改）' % SRC)
    lines.append('> 生成方式：机械正则比对 + 人工复核')
    lines.append('')
    lines.append('## 0. 结论')
    lines.append('')
    lines.append('| 项 | 数 |')
    lines.append('|---|---:|')
    lines.append('| 前轮报告总份数 | **%d** |' % len(rows))
    lines.append('| 命中「已被推翻说法」的报告 | **%d** |' % len(by_file))
    lines.append('| 未命中的报告 | **%d** |' % len(clean))
    lines.append('| 命中处次（总） | **%d** |' % total_hits)
    lines.append('')
    lines.append('> **命中 ≠ 该文档整体作废**：多数前轮报告的技术内容仍然有效，')
    lines.append('> 只是个别段落残留着已被后续轮次推翻的说法，需按对应 R 编号更正。')
    lines.append('> 完整的修正权威源是 `REPORT_回写总账-20261024.md`（R1–R23）。')
    lines.append('')
    lines.append('## 1. 当前权威口径（冲突时以此为准）')
    lines.append('')
    lines.append('| 文档 | 定位 |')
    lines.append('|---|---|')
    for a, b in AUTHORITATIVE:
        lines.append('| `%s` | %s |' % (a, b))
    lines.append('')
    lines.append('## 2. 逐份索引')
    lines.append('')
    lines.append('| 文件 | 字节 | 主题 | 命中 | 说明 |')
    lines.append('|---|---:|---|---|---|')
    for f, size, hits, tags, _ in rows:
        if hits:
            ids = sorted(set(h[0] for h in hits))
            cnt = '%d 处（%s）' % (len(hits), ','.join(ids))
            note = '**含已被推翻说法，需按 R 编号更正**'
        else:
            cnt = '0'
            note = '未命中已知作废说法'
        lines.append('| `%s` | %s | %s | %s | %s |'
                     % (f, '{:,}'.format(size), ' / '.join(tags), cnt, note))
    lines.append('')
    lines.append('## 3. 命中明细（按检查项）')
    lines.append('')
    lines.append('| # | 检查项 | 命中文件 | 行号 | 原文片段 | 对应修正 |')
    lines.append('|---|---|---|---:|---|---|')
    for cid, cname, pat, desc, rno in CHECKS:
        hits = [h for h in all_hits if h[1] == cid]
        if not hits:
            lines.append('| %s | %s | — | — | **无命中** | %s |' % (cid, cname, rno))
            continue
        for i, (f, _, _, ln, snip, _) in enumerate(hits):
            snip2 = snip.replace('|', '\\|')
            if len(snip2) > 110:
                snip2 = snip2[:110] + '…'
            lines.append('| %s | %s | `%s` | %d | %s | %s |'
                         % (cid if i == 0 else '', cname if i == 0 else '',
                            f, ln, snip2, rno))
    lines.append('')
    lines.append('## 4. 检查项定义')
    lines.append('')
    lines.append('| # | 检查项 | 判据 | 对应修正 |')
    lines.append('|---|---|---|---|')
    for cid, cname, pat, desc, rno in CHECKS:
        lines.append('| %s | %s | %s | %s |' % (cid, cname, desc, rno))
    lines.append('')
    lines.append('## 5. 复核指引')
    lines.append('')
    lines.append('对每条命中：')
    lines.append('')
    lines.append('1. 打开 `REPORT_回写总账-20261024.md`，查对应 R 编号的**修正后结论**')
    lines.append('2. 用修正后结论替换命中处；若该文档整体结论已过时，在开头加一行「已被 R## 更正」')
    lines.append('3. **不要删除原始段落** —— 保留痕迹比抹干净更有价值')
    lines.append('')

    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')

    print('写出: %s' % OUT)
    print('前轮 %d 份；命中 %d 份 / %d 处'
          % (len(rows), len(by_file), total_hits))
    for cid, cname, pat, desc, rno in CHECKS:
        n = len([h for h in all_hits if h[1] == cid])
        print('  %-4s %-24s %d 处   (%s)' % (cid, cname, n, rno))
    return 0


if __name__ == '__main__':
    sys.exit(main())
