#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0x400408 / er3 装配公式的【独立】字节级复核（不依赖 sim_400408.py 的寄存器抽象）
方法：直接按 H8/300H 语义手工走每一条指令，逐位记录 er 的 32 位值。
只用 ROM 原始字节 + 手工写的指令语义；与 sim_400408.py 是两套独立实现，互证。
只读 D:。
"""
D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000


def raw(a, n):
    o = a - BASE
    return ' '.join('%02X' % b for b in D[o:o + n])


def bits32(v):
    return ''.join('1' if (v >> b) & 1 else '0' for b in range(31, -1, -1))


class M:
    """er[n] 32 位。R[n] = 低 16 位，E[n] = 高 16 位。"""
    def __init__(self):
        self.er = [0] * 8

    def R(self, n):  return self.er[n] & 0xFFFF
    def E(self, n):  return (self.er[n] >> 16) & 0xFFFF
    def setR(self, n, v): self.er[n] = (self.er[n] & 0xFFFF0000) | (v & 0xFFFF)
    def setE(self, n, v): self.er[n] = (self.er[n] & 0x0000FFFF) | ((v & 0xFFFF) << 16)

    def mov_b_to_RL(self, n, byte): self.setR(n, (self.R(n) & 0xFF00) | (byte & 0xFF))
    def mov_b_RL_to_RH(self, n):
        b = self.R(n) & 0xFF
        self.setR(n, (self.R(n) & 0x00FF) | (b << 8))
    def sub_b_RL(self, n): self.setR(n, self.R(n) & 0xFF00)
    def sub_w_R(self, n): self.setR(n, 0)
    def mov_w_R_to_E(self, n): self.setE(n, self.R(n))
    def sub_l(self, n): self.er[n] = 0
    def add_l(self, d, s): self.er[d] = (self.er[d] + self.er[s]) & 0xFFFFFFFF
    def shll_l2(self, n): self.er[n] = (self.er[n] << 2) & 0xFFFFFFFF


# 四条臂的源字节取法（er6/er5 相对偏移 -> payload 下标）
#   C1/A0/B3: er6 = 0x400C55，@(k,er6) -> payload[k-1]
#   PARSE   : er5 = sp+1，   @(k,er5) -> payload[k]
ARM_SRC = {
    'C1':    [2, 3, 4, 5],
    'A0':    [2, 3, 4, 5],
    'B3':    [2, 3, 4, 5],
    'PARSE': [1, 2, 3, 4],
}
# 目标寄存器 / 辅助寄存器
ARM_REG = {'C1': (0, 1), 'A0': (0, 1), 'B3': (0, 1), 'PARSE': (3, 0)}


def trace_arm(payload, arm, log=None):
    """返回 32 位结果。log 非空则填入逐步快照。"""
    m = M()
    reg, aux = ARM_REG[arm]
    ks = ARM_SRC[arm]
    src = lambda k: payload[k - 1] if arm != 'PARSE' else payload[k]

    # p1: mov.b src,r0l / mov.b r0l,r0h / sub.b r0l,r0l / mov.w r0,e0 / sub.w r0,r0
    m.sub_l(reg)
    m.mov_b_to_RL(reg, src(ks[0]))
    m.mov_b_RL_to_RH(reg)
    m.sub_b_RL(reg)
    m.mov_w_R_to_E(reg)
    m.sub_w_R(reg)
    if log is not None:
        log.append(('p1', m.er[reg]))

    # p2: sub.l er1,er1 / mov.b src,r1l / mov.w r1,e1 / sub.w r1,r1 / add.l er1,er0
    m.sub_l(aux)
    m.mov_b_to_RL(aux, src(ks[1]))
    m.mov_w_R_to_E(aux)
    m.sub_w_R(aux)
    m.add_l(reg, aux)
    if log is not None:
        log.append(('p2', m.er[reg]))

    # p3: sub.l er1,er1 / mov.b src,r1l / shll.l #2 x4 / add.l er1,er0
    m.sub_l(aux)
    m.mov_b_to_RL(aux, src(ks[2]))
    for _ in range(4):
        m.shll_l2(aux)
    m.add_l(reg, aux)
    if log is not None:
        log.append(('p3', m.er[reg]))

    # p4: sub.l er1,er1 / mov.b src,r1l / add.l er1,er0
    m.sub_l(aux)
    m.mov_b_to_RL(aux, src(ks[3]))
    m.add_l(reg, aux)
    if log is not None:
        log.append(('p4', m.er[reg]))

    return m.er[reg]


PAY = [0x00, 0x11, 0x22, 0x33, 0x44]

print('=' * 78)
print('步骤 1：ROM 原始字节 —— 三条执行层臂 + 解析层，四段装配是否同构')
print('=' * 78)
for k, (a, b) in {
    'C1 臂  0x026A54-0x026A90': (0x026A54, 0x026A90),
    'A0 臂  0x026A92-0x026ACE': (0x026A92, 0x026ACE),
    'B3 臂  0x026B14-0x026B50': (0x026B14, 0x026B50),
    '解析层 0x026D10-0x026D4C': (0x026D10, 0x026D4C),
}.items():
    print('%-26s %s' % (k, raw(a, b - a)))
print()
print('四条 shll.l #2 原始字节 (0x026B34-0x026B3C): %s' % raw(0x026B34, 8))
print('  h8.lst: 1070/1071 = shll.l #2 (two) erN  ->  每次左移 2 位')
print('  4 条连用 = 左移 8 位  =>  p3 落 bits 8-15')
print('  解析层同构字节 (0x026D30-0x026D38): %s' % raw(0x026D30, 8))
print()

print('=' * 78)
print('步骤 2：逐位追踪（payload[1..4] = 11 22 33 44）')
print('=' * 78)
for arm in ('PARSE', 'C1', 'A0', 'B3'):
    lg = []
    v = trace_arm(PAY, arm, lg)
    print('%-7s 最终 er=0x%08X  bits=%s' % (arm, v, bits32(v)))
    for nm, x in lg:
        print('        %s 后 er=0x%08X  %s' % (nm, x, bits32(x)))
    print()

print('=' * 78)
print('步骤 3：与 sim_400408.py 交叉核对（两套独立实现）')
print('=' * 78)
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import importlib.util
spec = importlib.util.spec_from_file_location(
    'simmod', r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\status\_verify400408\sim_400408.py')
sim = importlib.util.module_from_spec(spec)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(sim)
for arm in ('PARSE', 'A0', 'B3'):
    a = trace_arm(PAY, arm)
    b = sim.sim(PAY, True, arm)
    print('%-7s 独立实现=0x%08X   sim=0x%08X   一致? %s'
          % (arm, a, b, 'YES' if a == b else 'NO'))
print()

print('=' * 78)
print('步骤 4：语义判据（用独立实现的值）')
print('=' * 78)
tests = [
    ('V1 = 15354 (0x3BFA)  [0x40 上限]', [0, 0x00, 0x00, 0x3B, 0xFA], lambda v: v == 15354),
    ('V1 = 10000 (0x2710)  [A0 动态门限 res=4000]', [0, 0x00, 0x00, 0x27, 0x10], lambda v: v == 10000),
    ('V1 = 450 (0x01C2)    [0x41/0xC1 上限]', [0, 0x00, 0x00, 0x01, 0xC2], lambda v: v == 450),
    ('V1 = 3283 (0x0CD3)   [0x42 上限]', [0, 0x00, 0x00, 0x0C, 0xD3], lambda v: v == 3283),
    ('V1 = 133 (0x85)      [stock 0x6000 = 00 00 00 85]', [0, 0x00, 0x00, 0x00, 0x85], lambda v: v == 133),
    ('V1 = -300 (0xFFFFFED4) [B3 下界]', [0, 0xFF, 0xFF, 0xFE, 0xD4], lambda v: (v - (1 << 32)) == -300),
]
allpass = True
for name, p, fn in tests:
    v = trace_arm(p, 'PARSE')
    ok = fn(v)
    allpass = allpass and ok
    print('%-52s -> 0x%08X   %s' % (name, v, 'PASS' if ok else 'FAIL'))
print()
print('全部语义判据通过? %s' % ('YES' if allpass else 'NO'))
