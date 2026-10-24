"""转储 E0 相关表 + 反汇编作业层区域（只读 D:\）。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import sys, os, struct
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def off(a): return a - BASE

print('=== 0x03EDB8 子功能表（12 条 × 2 字节: code, len?）===')
for i in range(12):
    a = 0x03EDB8 + 2*i
    print(f'  [{i:2d}] 0x{a:06X}: code=0x{d[off(a)]:02X}  b2=0x{d[off(a)+1]:02X}')

print('\n=== 0x03EDE8 作业表（键→函数指针，逐 4 字节扫到 0x03EE60）===')
a = 0x03EDE8
while a < 0x03EE60:
    v = struct.unpack('>I', d[off(a):off(a)+4])[0]
    mark = ''
    if 0x026000 <= v < 0x040000:
        mark = '  <-- ROM 函数指针'
    print(f'  0x{a:06X}: 0x{v:08X}{mark}')
    a += 4

print('\n=== 双精度常量 ===')
for a in (0x03EDE0,):
    v = struct.unpack('>d', d[off(a):off(a)+8])[0]
    print(f'  0x{a:06X}: {v!r}')
print('  0x03EB70 起 10 个双精度:')
for i in range(10):
    a = 0x03EB70 + 8*i
    v = struct.unpack('>d', d[off(a):off(a)+8])[0]
    print(f'  0x{a:06X}: {v!r}')

print('\n=== 0x03F9B4 双精度常量（jobA0 里 0x0188D2 的比较常量）===')
v = struct.unpack('>d', d[off(0x03F9B4):off(0x03F9B4)+8])[0]
print(f'  0x03F9B4: {v!r}')

print('\n=== 作业层区域 0x0275F2-0x0276A0 ===')
pc = 0x0275F2 - BASE
while pc < 0x0276A0 - BASE:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        pc += 1
        continue
    print(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    pc = nxt
