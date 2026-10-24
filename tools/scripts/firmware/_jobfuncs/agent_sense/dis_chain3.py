"""收尾核查：
1. 0x026EB2（0x026CDC jmp 目标）确认写出尾
2. 读点 0x0213BE / 0x02157E / 0x012070 上下文
3. fn 0x011000（直接写 0x011004）与 0x012AD6（读 0x012A7E 后的分支）
4. fn 0x022308 / 0x022434 调用者上下文（0x022AD6/0x022BF2 的宿主）
5. sense 表 0x01914A 相关索引字节：0x4F,0x50,0x51,0x56,0x65,0x70,0x7A,0x7B
6. 0x03E390 通路A表是否含 0x50/0x56（复核任务声明）
7. fn 0x011708 的 r1 用法（REQUEST SENSE 构造器第二参数）
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
import sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLCHAIN_ROOT)
sys.path.insert(0, r'<HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000/03_analysis/firmware/_jobfuncs')
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

def dis_range(lo, hi, label):
    print(f'\n===== {label}  0x{lo:06X}-0x{hi:06X} =====')
    pc = lo - BASE
    end = hi - BASE
    while pc < end:
        sz, nm, a1, a2, nxt = h.decode(pc)
        if nm is None:
            print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
            pc += 1
            continue
        txt = f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x)
        mark = '   <<< 0x400436' if '400436' in txt else ''
        print(txt + mark)
        pc = nxt

dis_range(0x026EA0, 0x026F00, '0x026EB2 write tail (from 0x026CDC)')
dis_range(0x0213A0, 0x0213E0, 'around read 0x0213BE')
dis_range(0x021560, 0x0215B0, 'around read 0x02157E')
dis_range(0x012050, 0x0120A0, 'around read 0x012070')
dis_range(0x011000, 0x011030, 'fn 0x011000 direct write 0x011004')
dis_range(0x012AC0, 0x012B40, 'after read 0x012A7E -> 0x012AD6')
dis_range(0x022300, 0x022310, 'caller of fn 0x022AD6 (0x022308)')
dis_range(0x02242C, 0x022440, 'caller of fn 0x022BF2 (0x022434)')

# sense 表条目
def rd(addr, n):
    off = addr - BASE
    return d[off:off+n]
print('\n===== sense table 0x01914A entries =====')
for idx in (0x02, 0x03, 0x4F, 0x50, 0x51, 0x56, 0x65, 0x70, 0x7A, 0x7B):
    a = 0x01914A + idx * 5
    print(f'  idx 0x{idx:02X} @ 0x{a:06X} = {rd(a,5).hex(" ")}')

# 通路A表 0x03E390 是否含 0x50/0x56
print('\n===== path-A table 0x03E390: contains 0x50/0x56? =====')
off = 0x03E390 - BASE
found = {}
for i in range(85):
    e = d[off+i*4: off+i*4+4]
    hc = (e[0] << 8) | e[1]
    if hc == 0:
        print(f'  terminator at entry {i}')
        break
    if hc in (0x50, 0x56):
        found[hc] = (i, (e[2] << 8) | e[3])
print('  0x50/0x56 in 0x03E390:', found if found else 'NOT FOUND (task claim confirmed)')

# fn 0x011708 r1 用法
print('\n===== fn 0x011708 first 40 insns (r1 usage) =====')
pc = 0x011708 - BASE
for i in range(40):
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        pc += 1
        continue
    print(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    pc = nxt
    if nm == 'rts':
        break
