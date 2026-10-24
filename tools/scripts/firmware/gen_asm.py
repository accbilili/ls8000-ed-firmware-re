#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成 film_ident_28BB0.asm.txt：片夹识别链路完整反汇编（含字节列）。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import hashlib
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.stdout.reconfigure(encoding='utf-8')
import dis28B as m

ROM = sample('LS8000_111_ROM.bin')
B = 0x10000
d = m.d

SECTIONS = [
    ('A. 函数 0x0289B4（含 0x028BB0 两阶段主体）', 0x289B4, 0x28E30),
    ('B. 函数 0x028E30（采样式识别，含判定树）', 0x28E30, 0x290A0),
    ('C. 0x0290A0 类型码消费（入口 0x0290A0-0x029120）', 0x290A0, 0x29120),
    ('D1. 双精度相减取绝对差 0x017FD2', 0x17FD2, 0x18010),
    ('D2. 双精度转整数（截断）0x01876A', 0x1876A, 0x187E8),
    ('D3. 双精度乘法 0x018AA0（入口片段）', 0x18AA0, 0x18B00),
    ('D4. memcpy 0x018E54', 0x18E54, 0x18E68),
    ('D5. 整数转双精度 0x018E68（入口片段）', 0x18E68, 0x18EA0),
    ('D6. 走片启动 0x02ADCE', 0x2ADCE, 0x2AE20),
    ('D7. 走片等待 0x02ACBA', 0x2ACBA, 0x2ACF0),
    ('D8. 行采集 0x02D700（入口片段）', 0x2D700, 0x2D7E0),
    ('D9. 采集前置配置 0x02D1DC', 0x2D1DC, 0x2D200),
]


def dump(lo, hi):
    out = []
    pc = lo - B
    while pc < hi - B:
        sz, nm, a1, a2 = m.dec(pc)
        raw = ' '.join(f'{b:02X}' for b in d[pc:pc + sz]) if nm else f'{d[pc]:02X} {d[pc + 1]:02X}'
        if nm is None:
            out.append(f'{pc + B:06X}  {raw:<18} .byte')
            pc += 2
            continue
        ops = ', '.join(x for x in (a1, a2) if x)
        out.append(f'{pc + B:06X}  {raw:<18} {nm:<9}{ops}')
        pc += sz
    return out


def main():
    sha = hashlib.sha256(d).hexdigest()
    L = [f'# LS-8000 ED 固件 片夹识别链路 反汇编',
         f'# ROM  : {ROM}  ({len(d)} B)',
         f'# SHA256: {sha}',
         f'# 基址 : 地址 = 文件偏移 + 0x{B:05X}',
         '# 解码 : h8dis + 本目录 dis28B.py 修正（补 0x0100 前缀 MOV.L d:32/d:16 形式）',
         '# 注意 : 解码器把 0x40 标成 bt，实为 BRA d:8（无条件）',
         '']
    for t, lo, hi in SECTIONS:
        L.append('')
        L.append('; ' + '=' * 76)
        L.append(f'; {t}   0x{lo:06X} - 0x{hi:06X}')
        L.append('; ' + '=' * 76)
        L.extend(dump(lo, hi))
    txt = '\n'.join(L) + '\n'
    open('film_ident_28BB0.asm.txt', 'w', encoding='utf-8').write(txt)
    print('lines', len(L), 'bytes', len(txt.encode('utf-8')))


if __name__ == '__main__':
    main()
