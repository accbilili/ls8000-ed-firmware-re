"""查找间接引用：mov.l #imm 形式加载 0x0269A6/0x0275F2/0x026BF8/0x026EFC/0x03A3D4 的指令，
以及 0x028DC2 调用 jobA0 的上下文。只读 D:\。"""
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
sys.path.insert(0, os.path.dirname(OUT))
from h8dis import H8
from h8fix import load_entries_fixed as load_entries

d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000
h = H8(d, load_entries(sample('h8.lst')), base=BASE)

targets = {0x0269A6: 'exec', 0x0275F2: 'joblayer', 0x026BF8: 'parseA', 0x026EFC: 'parseB',
           0x03A3D4: 'jobA0', 0x028DC2: 'caller_of_jobA0'}

print('=== mov.l #imm / jsr / bsr 等直接引用目标地址的指令 ===')
pc = 0
while pc < len(d) - 16:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        pc += 2
        continue
    for t, tag in targets.items():
        for x in (a1, a2):
            if x and x.strip() == f'0x{t:06x}':
                print(f'0x{pc+BASE:06X}  {nm:<9} {x}')
    # mov.l #imm32, erX 形式
    if nm == 'mov.l' and a1 and a1.startswith('#0x'):
        try:
            v = int(a1[1:], 16)
            if v in targets:
                print(f'0x{pc+BASE:06X}  mov.l     #0x{v:06X}, {a2}   -> {targets[v]}')
        except ValueError:
            pass
    pc = nxt if sz and sz > 0 else pc + 2

print('\n=== 0x028DC2 上下文（jobA0 调用者）===')
pc = 0x028D80 - BASE
while pc < 0x028E20 - BASE:
    sz, nm, a1, a2, nxt = h.decode(pc)
    if nm is None:
        print(f'0x{pc+BASE:06X}  .byte 0x{d[pc]:02X}')
        pc += 1
        continue
    print(f'0x{pc+BASE:06X}  {nm:<9} ' + ', '.join(x for x in (a1, a2) if x))
    pc = nxt
