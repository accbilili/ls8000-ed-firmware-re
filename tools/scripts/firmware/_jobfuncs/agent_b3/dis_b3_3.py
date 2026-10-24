"""第三轮：
1. 0x02740A-0x0275C0（请求块 0x400400 的消费者——通用 E0→flash 处理器）
2. 0x026900-0x026A90（执行层上下文，含 0x02692C 另一 0x6010 模板用户）
3. 0x031080-0x031140（0x03109E 0x6010 模板用户）
4. 0x02BAA6 头部（B3 尾部调用者）
5. 搜索谁调用 0x02BCCE / 0x017A80 / 0x016E8E / 0x02BAA6
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, os, json
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def disasm_range(start, end):
    lines = []
    pc = start - BASE
    while pc < end - BASE:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            lines.append(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        raw = d[pc:pc+sz].hex(' ')
        lines.append(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1,a2) if x) + f'   ; {raw}')
        pc += sz
    return lines

for name, start, end in [('fn_02740A', 0x02740A, 0x0275C0),
                         ('exec_026900', 0x026900, 0x026A90),
                         ('fn_03109E', 0x031080, 0x031140),
                         ('fn_02BAA6_head', 0x02BAA6, 0x02BB00)]:
    lines = disasm_range(start, end)
    open(os.path.join(OUT, f'{name}.asm'), 'w').write('\n'.join(lines) + '\n')
    print(f'{name}: {len(lines)} 行')

# 搜索 bsr/jsr 到指定地址：bsr rel16 = 5c xx xx, jsr abs24 = 5e xx xx xx
def find_calls(target):
    hits = []
    for off in range(0, len(d) - 4):
        if d[off] == 0x5c:  # bsr rel16
            rel = int.from_bytes(d[off+1:off+3], 'big', signed=True)
            if off + 3 + rel == target - BASE:
                hits.append(('bsr', off + BASE))
        elif d[off] == 0x5e:  # jsr abs24
            a = int.from_bytes(d[off+1:off+4], 'big')
            if a == target:
                hits.append(('jsr', off + BASE))
    return hits

for t in (0x02BCCE, 0x017A80, 0x016E8E, 0x02BAA6, 0x02BBAE, 0x017A78, 0x017A7C):
    hits = find_calls(t)
    print(f'call 0x{t:06X}: {hits}')
