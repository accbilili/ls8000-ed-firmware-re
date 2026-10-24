#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
裁决 0x400408 / er3 的 32 位组装公式（FW_DOC_INDEX §4.2 冲突组 6）
方法：只读 ROM 字节 + 手工实现该指令子集，逐指令模拟三条臂的装配。
两个候选半映射假设：
  H_BE  : E0-E7 = ER0-ER7 的高半, R0-R7 = 低半
  H_LOW : E0-E7 = 低半,          R0-R7 = 高半
指令流源（全部只读自样本）：
  A0 臂   0x026A92-0x026AC4   agent_a0/f_026A92.asm
  B3 臂   0x026B14-0x026B46   agent_a0/exec_layer_0269A6.asm
  解析层  0x026D10-0x026D40   agent_a0/parse_layer_026BF8.asm
只读 D:，不写任何样本。
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
from h8dis import H8
from h8tab import load_entries
BASE = 0x10000
D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
H = H8(D, load_entries(sample('h8.lst')), base=BASE)

M32 = 0xFFFFFFFF


class Regs:
    """只实现该指令子集用到的操作。er[] = 32 位 ER 寄存器。"""

    def __init__(self, e_is_high=True):
        self.e_is_high = e_is_high
        self.er = [0] * 8

    def _halves(self, n):
        v = self.er[n]
        if self.e_is_high:
            return (v & 0xFFFF, (v >> 16) & 0xFFFF)   # (R 低半, E 高半)
        return ((v >> 16) & 0xFFFF, v & 0xFFFF)         # (R 高半, E 低半)

    def _join(self, n, r16, e16):
        if self.e_is_high:
            self.er[n] = ((e16 & 0xFFFF) << 16) | (r16 & 0xFFFF)
        else:
            self.er[n] = ((r16 & 0xFFFF) << 16) | (e16 & 0xFFFF)

    def set_r(self, n, v):
        r, e = self._halves(n); self._join(n, v, e)

    def set_e(self, n, v):
        r, e = self._halves(n); self._join(n, r, v)

    def get_r(self, n):
        return self._halves(n)[0]

    def set_rl(self, n, v):                 # mov.b src, rNl
        r, e = self._halves(n); self._join(n, (r & 0xFF00) | (v & 0xFF), e)

    def get_rl(self, n):
        return self._halves(n)[0] & 0xFF

    def set_rh(self, n, v):                 # mov.b rNl, rNh
        r, e = self._halves(n); self._join(n, (r & 0x00FF) | ((v & 0xFF) << 8), e)

    def sub_w_r(self, n):                   # sub.w Rn, Rn
        r, e = self._halves(n); self._join(n, 0, e)

    def sub_b_rl(self, n):                  # sub.b rNl, rNl
        r, e = self._halves(n); self._join(n, r & 0xFF00, e)

    def add_l(self, d, s):
        self.er[d] = (self.er[d] + self.er[s]) & M32

    def shll_l(self, n, cnt):
        self.er[n] = (self.er[n] << cnt) & M32


def sim(payload, e_is_high, arm):
    """
    payload[i] = 第 i 个 payload 字节。
    A0/B3/C1 臂：er6 = 0x400C55，源字节在 @(k,er6) → payload[k-1]
    解析层     ：er5 = sp+1，   源字节在 @(k,er5) → payload[k]
    """
    g = Regs(e_is_high)
    if arm in ('A0', 'B3', 'C1'):
        off = lambda k: payload[k - 1]     # @(2,er6)=payload[1] .. @(5,er6)=payload[4]
        ks = [2, 3, 4, 5]
    else:                                   # PARSE
        off = lambda k: payload[k]         # @(1,er5)=payload[1] .. @(4,er5)=payload[4]
        ks = [1, 2, 3, 4]
    g.er[0] = 0
    g.set_rl(0, off(ks[0])); g.set_rh(0, g.get_rl(0)); g.sub_b_rl(0)
    g.set_e(0, g.get_r(0)); g.sub_w_r(0)
    g.er[1] = 0
    g.set_rl(1, off(ks[1])); g.set_e(1, g.get_r(1)); g.sub_w_r(1)
    g.add_l(0, 1)
    g.er[1] = 0
    g.set_rl(1, off(ks[2]))
    for _ in range(4):
        g.shll_l(1, 2)
    g.add_l(0, 1)
    g.er[1] = 0
    g.set_rl(1, off(ks[3]))
    g.add_l(0, 1)
    return g.er[0]


def be32(v):
    return ((v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF)


def s32(v):
    return v - (1 << 32) if v & 0x80000000 else v


print('=' * 76)
print('判据 A：字节位段是否互不重叠（p1 与 p3 是否落在同一段并被 add 污染）')
print('=' * 76)
pay = [0, 0x11, 0x22, 0x33, 0x44]
for hyp, name in ((True, 'H_BE  E=高半'), (False, 'H_LOW E=低半')):
    v = sim(pay, hyp, 'A0')
    b = be32(v)
    def pos(x):
        for i, byte in enumerate(b):
            if byte == x:
                return 'bits%d-%d' % (24 - 8 * i, 31 - 8 * i)
        return 'LOST'
    print('%-14s payload[1..4]=11 22 33 44 -> er=0x%08X bytes=%s'
          % (name, v, ' '.join('%02X' % x for x in b)))
    print('%-14s   p1@%s  p2@%s  p3@%s  p4@%s   位段相撞? %s'
          % ('', pos(0x11), pos(0x22), pos(0x33), pos(0x44),
             'YES -> add.l 互相污染' if pos(0x11) == pos(0x33) else 'no'))

print()
print('=' * 76)
print('判据 B：数值门限 —— V1 <= 15354 (0x3BFA)；payload = 00 00 3B FA')
print('=' * 76)
pay = [0, 0x00, 0x00, 0x3B, 0xFA]
for hyp, name in ((True, 'H_BE  E=高半'), (False, 'H_LOW E=低半')):
    v = sim(pay, hyp, 'A0')
    print('%-14s V1=0x%08X (%d)  <=15354? %s' % (name, v, v, 'YES' if v <= 15354 else 'NO'))

print()
print('=' * 76)
print('判据 C（决定性）：B3 的有符号下界 cmp.l #0xFFFFFED4 (=-300) + blt')
print('   若 V1 永远非负，则「V1 < -300 -> 退化 333」是死代码')
print('=' * 76)
pay = [0, 0xFF, 0xFF, 0xFE, 0xD4]     # BE32 = -300 (0xFFFFFED4)
for hyp, name in ((True, 'H_BE  E=高半'), (False, 'H_LOW E=低半')):
    v = sim(pay, hyp, 'A0')
    print('%-14s payload=FF FF FF D4 -> er=0x%08X  signed=%d  可为负? %s'
          % (name, v, s32(v), 'YES' if s32(v) < 0 else 'NO -> 下界分支永不可达'))

print()
print('=' * 76)
print('判据 D：A0 动态门限 res=4000 -> V1 <= 4000*10000/4000 = 10000 = 0x2710')
print('=' * 76)
pay = [0, 0x00, 0x00, 0x27, 0x10]
for hyp, name in ((True, 'H_BE  E=高半'), (False, 'H_LOW E=低半')):
    v = sim(pay, hyp, 'A0')
    print('%-14s payload=00 00 27 10 -> er=0x%08X (%d)  ==10000? %s'
          % (name, v, v, 'YES' if v == 10000 else 'NO'))

print()
print('=' * 76)
print('判据 E：flash 回读自洽 —— 0x400408 的 4 字节 -> 0x6000，0x02BD10 按 BE32 读回')
print('=' * 76)
pay = [0, 0x00, 0x00, 0x00, 0x85]      # stock: V1 = 133
for hyp, name in ((True, 'H_BE  E=高半'), (False, 'H_LOW E=低半')):
    v = sim(pay, hyp, 'A0')
    b = be32(v)
    print('%-14s V1=133 -> 0x400408 bytes=%s  与 stock 0x6000 (00 00 00 85) 一致? %s'
          % (name, ' '.join('%02X' % x for x in b),
             'YES' if b == (0x00, 0x00, 0x00, 0x85) else 'NO'))

print()
print('=' * 76)
print('判据 F：shll.l #2 的位宽 —— 4 条连用 = 多少位？（raw bytes）')
print('=' * 76)
raw = D[0x026B34 - BASE:0x026B3C - BASE]
print('0x026B34-0x026B3C raw: %s' % ' '.join('%02X' % b for b in raw))
print('h8.lst: 1070 fff8 0 shll.l two r32l s20  -> immediate = 2 bits')
print('4 条连用 = 2*4 = 8 位 -> p3 落 bits 8-15')
print('agent_b3 §2.8 记 "4xshll = <<16"、"p3 落 bits16-23" -> 与指令流不符')
print()
raw2 = D[0x026D30 - BASE:0x026D38 - BASE]
print('解析层 0x026D30-0x026D38 raw: %s  (同构)' % ' '.join('%02X' % b for b in raw2))
