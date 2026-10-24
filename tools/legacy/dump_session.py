#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解压并导出指定 Codex 会话的可读正文（含 reasoning / tool call / output）。"""
import io
import json
import os
import sys

import zstandard as zstd

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis\codex_sessions'


def read_lines(path):
    if path.endswith('.zst'):
        with open(path, 'rb') as fh:
            with zstd.ZstdDecompressor().stream_reader(fh) as rdr:
                yield from io.TextIOWrapper(rdr, encoding='utf-8', errors='replace')
    else:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            yield from fh


def text_of(payload):
    """尽量从 payload 里取出可读文本。"""
    t = payload.get('type')
    if t == 'reasoning':
        # summary 数组
        parts = []
        for s in payload.get('summary', []) or []:
            if isinstance(s, dict):
                parts.append(s.get('text') or s.get('content') or '')
            else:
                parts.append(str(s))
        if payload.get('content'):
            for c in payload['content']:
                if isinstance(c, dict):
                    parts.append(c.get('text', ''))
        return '\n'.join(x for x in parts if x)
    if t in ('custom_tool_call', 'function_call'):
        name = payload.get('name', '')
        args = payload.get('arguments') or payload.get('input') or ''
        return f'[TOOL {name}] {args}'
    if t in ('custom_tool_call_output', 'function_call_output'):
        out = payload.get('output') or payload.get('content') or ''
        if isinstance(out, list):
            out = '\n'.join(str(x) for x in out)
        return f'[OUTPUT] {out}'
    if t in ('message', 'user_message', 'assistant_message'):
        c = payload.get('content')
        if isinstance(c, list):
            parts = []
            for x in c:
                if isinstance(x, dict):
                    parts.append(x.get('text', ''))
                else:
                    parts.append(str(x))
            return '\n'.join(parts)
        return str(c or '')
    return ''


def dump(path, tag):
    os.makedirs(OUT_DIR, exist_ok=True)
    lines = []
    n_ev = 0
    for line in read_lines(path):
        try:
            o = json.loads(line)
        except Exception:
            continue
        n_ev += 1
        payload = o.get('payload') or {}
        if not isinstance(payload, dict):
            continue
        txt = text_of(payload)
        if not txt.strip():
            continue
        ts = o.get('timestamp') or ''
        lines.append(f'\n===== [{n_ev}] {payload.get("type")} {ts} =====\n{txt}')
    out = os.path.join(OUT_DIR, f'{tag}.md')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print(f'{tag}: {n_ev} events -> {len(lines)} blocks, {os.path.getsize(out)} bytes')
    return out


if __name__ == '__main__':
    for path, tag in [
        (r'<HOME>\.codex\archived_sessions\rollout-2026-10-12T13-00-07-01a12e7b-7c22-7ae3-83dc-1f532d4beb31.jsonl.zst', '10-12_A_holder_2100'),
        (r'<HOME>\.codex\archived_sessions\rollout-2026-10-12T13-00-18-01a12e7b-a872-7072-82c8-4a0a79fed745.jsonl.zst', '10-12_B_holder_2118'),
    ]:
        if os.path.exists(path):
            dump(path, tag)
        else:
            print('MISSING:', path)
