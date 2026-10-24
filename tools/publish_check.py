#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布卫生自检 / Publication hygiene self-check
=============================================

在提交或 CI 中运行，用于拦截三类"一旦推送就无法挽回"的问题：

    1. 本机隐私信息（用户路径、邮箱、密钥、Token）
    2. 二进制文件（固件 ROM / 驱动 / 转储）
    3. 未登记的仓库治理文件缺失

用法 / Usage
------------
    python tools/publish_check.py              # 扫描仓库根（自动向上查找 MANIFEST.txt）
    python tools/publish_check.py <目录>        # 扫描指定目录

退出码 / Exit codes
-------------------
    0 = 全部通过
    1 = 发现阻塞项
    2 = 发现警告项但无阻塞项

为什么需要它
------------
Git 历史是不可撤销的。含 `Users\\cheng` 的提交一旦被推送到公开仓库，
即便后续删除，历史对象仍可通过任意 clone / fork 永久检索。
唯一的防线是**在首次提交之前**拦截——这就是本脚本的作用。
"""
import os
import re
import sys

# ---------------------------------------------------------------- 扫描规则

# 阻塞项：命中即拦截
BLOCKERS = [
    ('本机用户路径 native user path',
     re.compile(r'Users[\\/]cheng', re.I)),
    ('邮箱地址 email',
     re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')),
    ('私钥 PEM private key',
     re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
    ('AWS Access Key',
     re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ('GitHub Token',
     re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b')),
    ('Slack Token',
     re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b')),
]

# 二进制扩展名：本仓库不应出现任何二进制
BINARY_EXT = {
    '.bin', '.rom', '.hex', '.mot', '.s19', '.img', '.fw',
    '.sys', '.dll', '.exe', '.msi', '.cab',
    '.dmp', '.mdmp',
    '.zip', '.7z', '.rar', '.gz', '.tar',
    '.so', '.pyd', '.pyc', '.pyo',
}

SKIP_DIRS = {'__pycache__', '.git'}
REQUIRED_FILES = ['README.md', 'LICENSE', 'LICENSE-DOCS', 'NOTICE',
                  'DISCLAIMER.md', '.gitignore']

# samples/ 下刻意收录的官方固件、驱动与文档原件 —— 属于预期二进制，不作警告
SAMPLES_EXPECTED_EXT = {
    '.bin', '.exe', '.dll', '.md3', '.pdf', '.rom', '.txt', '.md', '.json',
}

TEXT_EXT = {'.py', '.md', '.txt', '.ps1', '.json', '.csv', '.lst', '.asm',
            '.yml', '.yaml', '.sh', '.gitignore', ''}


def find_root(start):
    p = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(p, 'MANIFEST.txt')):
            return p
        q = os.path.dirname(p)
        if q == p:
            return None
        p = q


def main():
    start = sys.argv[1] if len(sys.argv) > 1 else '.'
    root = find_root(start) or os.path.abspath(start)
    os.chdir(root)

    blocker_hits = []
    bin_hits = []
    warn = []
    scanned = 0

    for dirpath, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = os.path.join(dirpath, f)
            rel = os.path.relpath(p, '.').replace('\\', '/')
            ext = os.path.splitext(f)[1].lower()

            # samples/ 下的官方固件/驱动/文档原件为刻意收录，见 samples/SOURCES.md
            if rel.startswith('samples/'):
                if ext in SAMPLES_EXPECTED_EXT:
                    continue
                warn.append((rel, 'samples/ 中出现非预期类型 unexpected type in samples/'))
                continue

            if ext in BINARY_EXT:
                bin_hits.append(rel)
                continue
            if ext not in TEXT_EXT and f not in ('LICENSE', 'LICENSE-DOCS', 'NOTICE'):
                warn.append((rel, '未知扩展名 unknown extension'))
                continue

            scanned += 1
            try:
                raw = open(p, 'rb').read()
            except OSError as e:
                warn.append((rel, '读取失败 %s' % e))
                continue
            if b'\x00' in raw[:4096]:
                bin_hits.append(rel)
                continue
            try:
                text = raw.decode('utf-8', errors='replace')
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                for label, rx in BLOCKERS:
                    if rx.search(line):
                        blocker_hits.append((label, rel, i, line.strip()[:70]))

    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]

    # ---------------------------------------------------------------- 报告
    print('=' * 62)
    print(' 发布卫生自检 / Publication hygiene self-check')
    print('=' * 62)
    print(' 根目录 root   : %s' % root)
    print(' 已扫描 scanned: %d 个文本文件' % scanned)
    print()

    print('--- 阻塞项 Blockers ---')
    if blocker_hits:
        for label, rel, ln, snip in blocker_hits[:30]:
            print('  ✗ [%s] %s:%d' % (label, rel, ln))
            print('        %r' % snip)
        if len(blocker_hits) > 30:
            print('  ... 另有 %d 处' % (len(blocker_hits) - 30))
    else:
        print('  ✓ 无隐私信息命中')
    print()

    print('--- 二进制文件 Binaries ---')
    if bin_hits:
        for rel in bin_hits[:20]:
            print('  ✗ %s' % rel)
    else:
        print('  ✓ 无二进制文件（与仓库承诺一致）')
    print()

    print('--- 治理文件 Governance files ---')
    if missing:
        for f in missing:
            print('  ✗ 缺失 missing: %s' % f)
    else:
        print('  ✓ 全部齐备 (%d/%d)' % (len(REQUIRED_FILES), len(REQUIRED_FILES)))
    print()

    if warn:
        print('--- 警告 Warnings (%d) ---' % len(warn))
        for rel, why in warn[:10]:
            print('  ! %s  %s' % (rel, why))
        print()

    bad = len(blocker_hits) + len(bin_hits) + len(missing)
    print('=' * 62)
    if bad:
        print(' 结果: ✗ 未通过 — %d 项需要处理' % bad)
        print(' RESULT: FAILED — %d issue(s) to resolve' % bad)
        print('=' * 62)
        return 1
    if warn:
        print(' 结果: ⚠ 通过（含 %d 项警告）' % len(warn))
        print(' RESULT: PASSED with warnings')
        print('=' * 62)
        return 2
    print(' 结果: ✓ 全部通过')
    print(' RESULT: PASSED')
    print('=' * 62)
    return 0


if __name__ == '__main__':
    sys.exit(main())
