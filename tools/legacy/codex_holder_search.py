#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在 Codex 全部会话（含 zst 压缩）中搜索片夹类型码相关证据。"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

HOME = os.path.expanduser('~')
ROOT = os.path.join(HOME, '.codex')

KEYS = [
    'holder', 'Holder', 'HOLDER',
    '片夹', '夹片',
    'FH-869', 'FH-835', 'FH-816', 'FH-8G1',
    'film type', 'FilmType', 'film holder',
    'MAID',
]

try:
    import zstandard as zstd
    HAS_ZSTD = True
except Exception:
    HAS_ZSTD = False


def iter_files():
    for sub in ('sessions', 'archived_sessions'):
        base = os.path.join(ROOT, sub)
        for dirpath, _, files in os.walk(base):
            for f in files:
                if f.endswith('.jsonl') or f.endswith('.jsonl.zst'):
                    yield os.path.join(dirpath, f)


def read_lines(path):
    if path.endswith('.zst'):
        if not HAS_ZSTD:
            return
        with open(path, 'rb') as fh:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(fh) as rdr:
                buf = io.TextIOWrapper(rdr, encoding='utf-8', errors='replace')
                for line in buf:
                    yield line
    else:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            for line in fh:
                yield line


def main():
    print('zstandard 可用:', HAS_ZSTD)
    hits = {}
    for path in sorted(iter_files()):
        rel = os.path.relpath(path, ROOT)
        size = os.path.getsize(path)
        n = 0
        found = []
        try:
            for line in read_lines(path):
                n += 1
                low = line
                for k in KEYS:
                    if k in low:
                        found.append((n, k, line))
                        break
        except Exception as e:
            print(f'  [ERR] {rel}: {e}')
            continue
        if found:
            hits[rel] = (size, n, found)
            print(f'>>> {rel}  (size={size}, lines={n}, hits={len(found)})')

    print()
    print('=' * 70)
    total = sum(len(v[2]) for v in hits.values())
    print(f'命中文件 {len(hits)} 个，命中行 {total} 条')
    print('=' * 70)

    out_path = os.path.join(
        r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis',
        'codex_holder_hits.txt')
    with open(out_path, 'w', encoding='utf-8') as out:
        for rel, (size, n, found) in hits.items():
            out.write(f'\n########## {rel} (size={size}, lines={n}) ##########\n')
            for ln, k, line in found:
                snippet = line.strip()
                if len(snippet) > 4000:
                    snippet = snippet[:4000] + ' ...[TRUNC]'
                out.write(f'--- line {ln} [key={k}] ---\n{snippet}\n')
    print('已写出:', out_path)


if __name__ == '__main__':
    main()
