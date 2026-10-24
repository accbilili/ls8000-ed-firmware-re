#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
"""
裁决冲突：R22 文档「er3 = payload[1..8] 重排相加」 vs 我方/verdict-400408「er3 = BE32(payload[1..4])」

方法：完整模拟解析层 0x026D10-0x026D74 的**两条**独立累加链：
  链A → er3   （payload[1..4]）
  链B → er0 → @(0xe,sp) （payload[5..8]）
关键问题：链B 的结果是否被加进 er3？
只读 ROM 字节 + 手工指令语义；H8 语义钉死：
  S1 ERn = (En << 16) | Rn           —— E 是高 16 位，R 是低 16 位
  S2 mov.w Rm, En 只写 En（高半），Rn 低半保持不变
  S3 mov.b r0l, r0h = 低字节复制到高字节
  S4 shll.l #2 = 左移 2 位（h8.lst: 1070 fff8 shll.l two r32l）
只读 D:。
"""
D = open(sample('LS8000_111_ROM.bin'), 'rb').read()
BASE = 0x10000


def raw(a, n):
    o = a - BASE
    return ' '.join('%02X' % b for b in D[o:o + n])


class M:
    """er[n] 32 位；R[n] = bits15:0，E[n] = bits31:16（S1）"""
    def __init__(self):
        self.er = [0] * 8
        self.stack = {}

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
    def mov_w_R_to_E(self, n): self.setE(n, self.R(n))     # S2：只写高半
    def sub_l(self, n): self.er[n] = 0
    def add_l(self, d, s): self.er[d] = (self.er[d] + self.er[s]) & 0xFFFFFFFF
    def shll_l2(self, n): self.er[n] = (self.er[n] << 2) & 0xFFFFFFFF   # S4


def parse_layer(payload):
    """
    完整复现 0x026D10-0x026D74。
    payload[i] = 第 i 个 payload 字节；er5 = sp+1，源字节在 @(k,er5) -> payload[k]
    """
    m = M()
    src = lambda k: payload[k]
    log = []

    # ---- 链A：er3 ← payload[1..4] ----
    m.sub_l(3)
    m.mov_b_to_RL(3, src(1)); m.mov_b_RL_to_RH(3); m.sub_b_RL(3)
    m.mov_w_R_to_E(3); m.sub_w_R(3)
    log.append(('链A p1 -> er3', m.er[3]))
    m.sub_l(0)
    m.mov_b_to_RL(0, src(2)); m.mov_w_R_to_E(0); m.sub_w_R(0)
    m.add_l(3, 0)
    log.append(('链A p2 -> er3', m.er[3]))
    m.sub_l(0)
    m.mov_b_to_RL(0, src(3))
    for _ in range(4):
        m.shll_l2(0)
    m.add_l(3, 0)
    log.append(('链A p3 -> er3', m.er[3]))
    m.sub_l(0)
    m.mov_b_to_RL(0, src(4)); m.add_l(3, 0)
    log.append(('链A p4 -> er3', m.er[3]))
    er3_after_chainA = m.er[3]

    # ---- 链B：er0 ← payload[5..8]，结果存 @(0xe,sp) ----
    m.sub_l(0)
    m.mov_b_to_RL(0, src(5)); m.mov_b_RL_to_RH(0); m.sub_b_RL(0)
    m.mov_w_R_to_E(0); m.sub_w_R(0)
    m.sub_l(1)
    m.mov_b_to_RL(1, src(6)); m.mov_w_R_to_E(1); m.sub_w_R(1)
    m.add_l(0, 1)
    m.sub_l(1)
    m.mov_b_to_RL(1, src(7))
    for _ in range(4):
        m.shll_l2(1)
    m.add_l(0, 1)
    m.sub_l(1)
    m.mov_b_to_RL(1, src(8)); m.add_l(0, 1)
    m.stack[0xe] = m.er[0]                      # 0x026D74 mov.l er0, @(0xe,sp)
    log.append(('链B -> er0 -> @(0xe,sp)', m.er[0]))

    return m, er3_after_chainA, m.stack[0xe], log


def r22_formula(payload):
    """R22 文档 §1 声称的公式（逐条照抄其位段表）"""
    p = payload
    return ((p[1] << 8) + (p[2] << 8) + (p[3] << 16) + p[4]
            + (p[5] << 8) + (p[6] << 8) + (p[7] << 16) + p[8])


def r22_400408_formula(payload):
    """R22 文档 §5 声称的 0x400408 公式：(P2<<8) + (P3<<8) + (P4<<16) + P5，P1 不参与
    约定：R22 的 Pk = payload[k]"""
    p = payload
    return (p[2] << 8) + (p[3] << 8) + (p[4] << 16) + p[5]


def be32_of_first4(payload):
    return (payload[1] << 24) | (payload[2] << 16) | (payload[3] << 8) | payload[4]


PAY = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]

print('=' * 78)
print('步骤 1：ROM 原始字节 —— 解析层两条累加链的边界')
print('=' * 78)
print('链A 0x026D10-0x026D42 (er3 <- payload[1..4]):')
print('  ', raw(0x026D10, 0x026D42 - 0x026D10))
print('链B 0x026D42-0x026D76 (er0 <- payload[5..8] -> @(0xe,sp)):')
print('  ', raw(0x026D42, 0x026D76 - 0x026D42))
print()
print('注意 0x026D74 = "01 00 6B A2 ..." (mov.l er0,@(0xe,sp)) —— 链B 的终点是**栈**，')
print('     链B 结束后到 0x026DAE 分派表之间，er3 无任何再修改。')
print()

print('=' * 78)
print('步骤 2：完整模拟（payload[1..9] = 11 22 33 44 55 66 77 88）')
print('=' * 78)
m, er3, stack0e, log = parse_layer(PAY)
for nm, v in log:
    print('  %-26s er = 0x%08X' % (nm, v))
print()
print('  链A 结束时的 er3            = 0x%08X' % er3)
print('  链B 结果 @(0xe,sp)          = 0x%08X' % stack0e)
print('  模拟结束时 er3（未被链B改） = 0x%08X' % m.er[3])
print()

print('=' * 78)
print('步骤 3：三种说法对比')
print('=' * 78)
cands = [
    ('我方/verdict-400408: er3 = BE32(payload[1..4])', er3),
    ('R22 §1 声称的 8 字节重排相加公式', r22_formula(PAY)),
    ('BE32(payload[1..4]) 直算', be32_of_first4(PAY)),
]
for nm, v in cands:
    print('  %-52s = 0x%08X' % (nm, v))
print()
print('  模拟 er3 == BE32(payload[1..4]) ? %s' % ('YES' if er3 == be32_of_first4(PAY) else 'NO'))
print('  模拟 er3 == R22 的 8 字节公式 ? %s' % ('YES' if er3 == r22_formula(PAY) else 'NO'))
print('  模拟 er3 == R22 公式 ? 0x%08X vs 0x%08X' % (er3, r22_formula(PAY)))
print()

print('=' * 78)
print('步骤 4：R22 公式的内部自洽性检查')
print('=' * 78)
print('R22 §1 的位段表声称：')
print('  bit23-16 <- P2+P6 ; bit15-8 <- P1+P5 ; bit7-0 <- P3+P4+P7+P8')
print('但 R22 §1 自己的反解示例（§4）写：')
print('  bit23-16 = 0x3B -> payload[2] + payload[6] = 59')
print('  bit15-8  = 0xBF -> payload[1] + payload[5] = 191')
print('  bit7-0   = 0xFA -> payload[3]+payload[4]+payload[7]+payload[8] = 250')
print('→ R22 把 payload[1] 放在 bit15-8，即**权重 <<8**。')
print('   而按 S2（mov.w r0,e0 只写高半）+ 指令流实测，payload[1] 应在 bit31-24（权重 <<24）。')
print('   差 16 倍 —— 与 shll.l #2×4 的 8/16 位差是同一个错误源。')
print()

print('=' * 78)
print('步骤 5：语义判据（用模拟出的 er3）')
print('=' * 78)
tests = [
    ('V1 = 15354 (0x3BFA)', [0, 0x00, 0x00, 0x3B, 0xFA, 0, 0, 0, 0], lambda v: v == 15354),
    ('V1 = 450 (0x01C2)', [0, 0x00, 0x00, 0x01, 0xC2, 0, 0, 0, 0], lambda v: v == 450),
    ('V1 = 3283 (0x0CD3)', [0, 0x00, 0x00, 0x0C, 0xD3, 0, 0, 0, 0], lambda v: v == 3283),
    ('V1 = 10000 (0x2710) A0动态门限', [0, 0x00, 0x00, 0x27, 0x10, 0, 0, 0, 0], lambda v: v == 10000),
    ('V1 = 133 (0x85) stock 0x6000', [0, 0x00, 0x00, 0x00, 0x85, 0, 0, 0, 0], lambda v: v == 133),
    ('V1 = -300 (0xFFFFFED4) B3下界', [0, 0xFF, 0xFF, 0xFE, 0xD4, 0, 0, 0, 0], lambda v: (v - (1 << 32)) == -300),
]
allok = True
for nm, p, fn in tests:
    _, e3, _, _ = parse_layer(p)
    ok = fn(e3)
    allok = allok and ok
    print('  %-42s er3=0x%08X  %s' % (nm, e3, 'PASS' if ok else 'FAIL'))
print()
print('  全部语义判据通过? %s' % ('YES' if allok else 'NO'))
print()

print('=' * 78)
print('步骤 6：R22 公式在同一组判据上的表现')
print('=' * 78)
for nm, p, fn in tests:
    v = r22_formula(p)
    ok = fn(v)
    print('  %-42s R22=0x%08X  %s' % (nm, v, 'PASS' if ok else 'FAIL'))
print()
print('  ⇒ R22 公式在 payload[1..4] 语义判据上**全部失败**，因为它把 payload[5..8]')
print('    也算进了同一个 32 位量（而 payload[5..8] 走链B、落栈，不参与门限）。')


print()
print('=' * 78)
print('步骤 7：R22 §5 的 0x400408 公式核对')
print('=' * 78)
print('R22 §5 声称：0x400408 = (P2<<8) + (P3<<8) + (P4<<16) + P5，P1 不参与')
print('R22 自己的 §5 表把 0x400408 的位段写成「bit23-16 <- P2；bit23-16 <- P3；')
print('bit16-23 <- P4；bit7-0 <- P5」—— bit23-16 出现两次，表本身自相矛盾。')
print()
pay2 = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]
print('  payload[1..6] = 11 22 33 44 55 66')
print('  R22 §5 公式           = 0x%08X' % r22_400408_formula(pay2))
print('  实际 BE32(payload[1..4]) = 0x%08X' % be32_of_first4(pay2))
print('  一致? %s' % ('YES' if r22_400408_formula(pay2) == be32_of_first4(pay2) else 'NO'))
print()
print('  => R22 §5 把 p2 放到 bit8-15、p4 放到 bit16-23，与指令流不符：')
print('     A0 臂 p2 走「mov.w r1,e1」路径（e1 = 高半 => bits 23:16），')
print('     p3 走「shll.l #2 x4」路径（= <<8 => bits 15:8），')
print('     p4 走「add.l」路径（=> bits 7:0）。')
print('     R22 把 p2 与 p3 的路径搞混、又把 p3 的位移算成 <<16（实为 <<8）。')
print()
print('  R22 §5.1/§5.2/§5.3 的槽位引用图谱（0x400412 写点/读点、0x400411 无独立写点、')
print('  参数块组装器 0x02BC00 的 16 字节重拼）—— 经独立复核**成立**；')
print('  唯 §5.1 的「0x40040C = (payload[7]<<8)+(payload[8]<<16)+payload[9]」公式错误：')
print('  实际 A0 臂 V2 段读的是 @(0x6,er6)..@(0x9,er6) = payload[5..8]，')
print('  即 0x40040C = BE32(payload[5..8])。')
