"""dump 关键表：0x03EDB8 (2B/条 子功能表), 0x03E5D8 (6B/条), 0x03EBC0 (16B/条 lo/hi 校验表)。
只读 D:\。
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
import sys
sys.path.insert(0, TOOLCHAIN_ROOT)
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000

def dump(addr, n, stride, fmt, label):
    print(f'--- {label} @0x{addr:06X} ({n} 条 x {stride}B) ---')
    for i in range(n):
        o = addr - BASE + i * stride
        chunk = d[o:o + stride]
        if len(chunk) < stride:
            break
        print(f'  [{i:2d}] 0x{addr + i*stride:06X}: ' + ' '.join(f'{b:02X}' for b in chunk) + '   ' + fmt(chunk, i))

# 0x03EDB8: 2 字节/条 [id][code], 0xFF 终止（从反汇编推断）
dump(0x03EDB8, 20, 2, lambda c, i: f'id=0x{c[0]:02X} code=0x{c[1]:02X}' + ('  <-- 终止' if c[0] == 0xFF else ''), '子功能 ID 表 (0x03EDB8)')

# 0x03E5D8: 6 字节/条, 0xFF 终止
dump(0x03E5D8, 24, 6, lambda c, i: ' '.join(f'{b:02X}' for b in c), '参数描述表 (0x03E5D8)')

# 0x03EBC0: 16 字节/条 [op:u16][len:u16][handler:u32][lo:u32][hi:u32]
def fmt16(c, i):
    op = (c[0] << 8) | c[1]
    ln = (c[2] << 8) | c[3]
    hd = (c[4] << 24) | (c[5] << 16) | (c[6] << 8) | c[7]
    lo = (c[8] << 24) | (c[9] << 16) | (c[10] << 8) | c[11]
    hi = (c[12] << 24) | (c[13] << 16) | (c[14] << 8) | c[15]
    return f'op=0x{op:04X} len=0x{ln:04X} handler=0x{hd:06X} lo=0x{lo:08X} hi=0x{hi:08X}'
dump(0x03EBC0, 26, 16, fmt16, '参数块字段描述符 (0x03EBC0)')

# 0x03E518: 12 字节/条 [id:u8][flags:u8][size:u32][addr:u32][mask:u16]
def fmt12(c, i):
    idd = c[0]; fl = c[1]
    size = (c[2] << 24) | (c[3] << 16) | (c[4] << 8) | c[5]
    ad = (c[6] << 24) | (c[7] << 16) | (c[8] << 8) | c[9]
    mask = (c[10] << 8) | c[11]
    return f'id=0x{idd:02X} flags=0x{fl:02X} size=0x{size:08X} addr=0x{ad:06X} mask=0x{mask:04X}'
dump(0x03E518, 10, 12, fmt12, '参数描述表 (0x03E518)')
