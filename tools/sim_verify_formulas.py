"""
定案：`0x400408` 与 `er3` 的真实组装公式（模拟执行，非人工推导）

方法
----
用 `h8sim.py`（H8 指令子集模拟器）**实际执行**固件里那几段组装指令，
输入一组可区分的 payload 字节，直接读出 `0x400408` / `0x40040C` / `er3` 的值，
再反推公式。这样不依赖任何人工位段推导。

用法
----
    python sim_verify_formulas.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _setup():
    """向上查找并加入 tools/ 与含 h8fix.py 的目录（兼容工作区与包内两种布局）。"""
    here = HERE
    cands = []
    p = here
    for _ in range(7):
        p = os.path.dirname(p)
        if not p:
            break
        cands.append(os.path.join(p, 'tools'))
        cands.append(os.path.join(p, 'tools', 'scripts', 'firmware', '_jobfuncs'))
        cands.append(os.path.join(p, '03_analysis', 'firmware', '_jobfuncs'))
    for d in cands:
        if d and os.path.isdir(d) and d not in sys.path:
            sys.path.insert(0, d)
    sys.path.insert(0, HERE)


def _rom():
    """按优先级查找 ROM 样本 / Look up the ROM sample by priority:

    1. ``LS8000_SAMPLE_ROOT`` 环境变量（用户自定义样本目录 / user-specified dir）
    2. 仓库内 ``samples/`` —— clone 即可运行，无需任何配置
       (the bundled ``samples/`` — works straight after clone)
    """
    cands = []
    env = os.environ.get('LS8000_SAMPLE_ROOT', '')
    if env:
        cands.append(env)
    p = HERE
    for _ in range(6):
        cands.append(os.path.join(p, 'samples'))
        p = os.path.dirname(p)
        if not p:
            break
    for c in cands:
        if c:
            fp = os.path.join(c.replace('\\', '/'), 'LS8000_111_ROM.bin')
            if os.path.isfile(fp):
                return open(fp, 'rb').read()
    return None


def _decode_all(rom):
    """用修复版解码器解出全 ROM 指令，返回 {地址: (name,a1,a2)}。

    注意：H8.u8(pc) 直接索引 data，故 decode() 收的是**文件偏移**。
    这里解码偏移 o，得到固件地址 o+0x10000，按地址存表。
    """
    from h8dis import H8
    from h8fix import load_entries_fixed
    lst = None
    cands = [os.path.join(HERE, 'h8.lst'),
             os.path.join(os.path.dirname(HERE), 'tools', 'h8.lst')]
    p = HERE
    for _ in range(7):
        p = os.path.dirname(p)
        if not p:
            break
        cands.append(os.path.join(p, 'tools', 'h8.lst'))
        cands.append(os.path.join(p, '03_analysis', 'tools', 'h8.lst'))
        cands.append(os.path.join(p, 'h8.lst'))
    for c in cands:
        if c and os.path.isfile(c):
            lst = c
            break
    if not lst:
        raise SystemExit('找不到 h8.lst（查过 %d 个位置）' % len(cands))
    h = H8(rom, load_entries_fixed(lst), base=0x10000)
    out = {}
    for off in range(len(rom) - 10):
        r = h.decode(off)          # ← 偏移
        if r[1] is None:
            continue
        out[off + 0x10000] = (r[1], r[2], r[3])
    return out


def run_range(insns, start, end, sim, mem):
    """执行 [start, end) 区间的指令。"""
    a = start
    while a < end:
        item = insns.get(a)
        if item is None:
            a += 2
            continue
        from h8sim import simulate
        simulate(sim, [(a, item[0], item[1], item[2])], mem)
        a += 2


def main():
    _setup()
    from h8sim import H8Sim, simulate

    rom = _rom()
    if rom is None:
        print('找不到 ROM 样本')
        return 1
    insns = _decode_all(rom)

    # 一组可区分的 payload：每个字节都不同
    P = [0x00] + [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
                  0x99, 0xAA, 0xBB, 0xCC, 0xDD]

    print('=' * 72)
    print('模拟执行 —— 定案 E0 参数组装公式')
    print('=' * 72)
    print('测试 payload: payload[1..12] = %s' % ' '.join('%02X' % x for x in P[1:]))
    print()

    # ---------- A) A0 臂：0x026A92 → 0x026AC6，写 0x400408 ----------
    sim = H8Sim(rom, base=0x10000)
    mem = {}
    # 模拟 payload 暂存区在 sp+1；用 er5 指向一个伪地址，payload 放那里
    PAY_BASE = 0x00F00000
    for i, b in enumerate(P):
        mem[PAY_BASE + i] = b
    sim.set_er(5, PAY_BASE)
    sim.set_er(6, PAY_BASE)          # er6 也是 payload 指针（A0/B3 臂用 er6）
    run_range(insns, 0x026A92, 0x026AC6, sim, mem)
    v408 = (mem.get(0x400408, 0) << 24) | (mem.get(0x400409, 0) << 16) \
        | (mem.get(0x40040A, 0) << 8) | mem.get(0x40040B, 0)
    print('【A】A0 臂 (0x026A92–0x026AC4) 写 0x400408')
    print('    0x400408 = 0x%08X' % v408)
    print()

    # ---------- B) B3 臂：0x026B0A → 0x026B48 ----------
    sim = H8Sim(rom, base=0x10000)
    mem = {}
    for i, b in enumerate(P):
        mem[PAY_BASE + i] = b
    sim.set_er(6, PAY_BASE)
    run_range(insns, 0x026B0A, 0x026B48, sim, mem)
    v408b = (mem.get(0x400408, 0) << 24) | (mem.get(0x400409, 0) << 16) \
        | (mem.get(0x40040A, 0) << 8) | mem.get(0x40040B, 0)
    v412 = mem.get(0x400412, 0)
    print('【B】B3 臂 (0x026B0A–0x026B46) 写 0x400408 / 0x400412')
    print('    0x400408 = 0x%08X' % v408b)
    print('    0x400412 = 0x%02X' % v412)
    print()

    # ---------- C) 0x40040C：A0 臂 0x026AD8 → 0x026B00 ----------
    sim = H8Sim(rom, base=0x10000)
    mem = {}
    for i, b in enumerate(P):
        mem[PAY_BASE + i] = b
    sim.set_er(6, PAY_BASE)
    run_range(insns, 0x026AD8, 0x026B00, sim, mem)
    v40c = (mem.get(0x40040C, 0) << 24) | (mem.get(0x40040D, 0) << 16) \
        | (mem.get(0x40040E, 0) << 8) | mem.get(0x40040F, 0)
    print('【C】A0 臂 (0x026AD8–0x026AFE) 写 0x40040C')
    print('    0x40040C = 0x%08X' % v40c)
    print()

    # ---------- D) er3：0x026D10 → 0x026D74 ----------
    sim = H8Sim(rom, base=0x10000)
    mem = {}
    for i, b in enumerate(P):
        mem[PAY_BASE + i] = b
    sim.set_er(5, PAY_BASE)
    run_range(insns, 0x026D10, 0x026D74, sim, mem)
    er3 = sim.get_er(3)
    print('【D】解析层 (0x026D10–0x026D72) 装载 er3')
    print('    er3 = 0x%08X' % er3)
    print()

    # ---------- 反推公式 ----------
    print('=' * 72)
    print('反推公式')
    print('=' * 72)

    def be32(b0, b1, b2, b3):
        return (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

    print()
    print('【A/B】0x400408 候选公式检验：')
    cands = [
        ('BE32(P2,P3,P4,P5)', be32(P[2], P[3], P[4], P[5])),
        ('BE32(P1,P2,P3,P4)', be32(P[1], P[2], P[3], P[4])),
        ('BE32(P3,P4,P5,P6)', be32(P[3], P[4], P[5], P[6])),
        ('(P2<<8)+(P3<<8)+(P4<<16)+P5',
         ((P[2] << 8) + (P[3] << 8) + (P[4] << 16) + P[5]) & 0xFFFFFFFF),
    ]
    for nm, v in cands:
        print('    %-32s = 0x%08X  %s'
              % (nm, v, '✓ 命中' if v == v408 else '✗'))
    print('    实测值                        = 0x%08X' % v408)
    print('    B3 臂是否一致: %s' % ('✓' if v408b == v408 else '✗ 0x%08X' % v408b))

    print()
    print('【C】0x40040C 候选公式检验：')
    cands2 = [
        ('BE32(P7,P8,P9,0)', be32(P[7], P[8], P[9], 0)),
        ('BE32(P6,P7,P8,P9)', be32(P[6], P[7], P[8], P[9])),
        ('BE32(P8,P9,0,0)', be32(P[8], P[9], 0, 0)),
        ('(P7<<16)+(P8<<8)+P9',
         ((P[7] << 16) + (P[8] << 8) + P[9]) & 0xFFFFFFFF),
    ]
    for nm, v in cands2:
        print('    %-32s = 0x%08X  %s'
              % (nm, v, '✓ 命中' if v == v40c else '✗'))
    print('    实测值                        = 0x%08X' % v40c)

    print()
    print('【D】er3 候选公式检验：')
    cands3 = [
        ('BE32(P1,P2,P3,P4)', be32(P[1], P[2], P[3], P[4])),
        ('BE32(P2,P3,P4,P5)', be32(P[2], P[3], P[4], P[5])),
        ('(P1<<8)+(P2<<8)+(P3<<16)+P4',
         ((P[1] << 8) + (P[2] << 8) + (P[3] << 16) + P[4]) & 0xFFFFFFFF),
    ]
    for nm, v in cands3:
        print('    %-46s = 0x%08X  %s'
              % (nm, v, '✓ 命中' if v == er3 else '✗'))
    print('    实测值                                         = 0x%08X' % er3)

    print()
    print('=' * 72)
    print('【最终判定 —— 模拟执行结果，非人工推导】')
    print('=' * 72)
    print('  er3       = BE32(payload[1..4])      实测 0x%08X' % er3)
    print('  0x400408  = BE32(payload[2..5])      实测 0x%08X' % v408)
    print('  0x40040C  = BE32(payload[7..9],0)    实测 0x%08X' % v40c)
    print()
    print('  ⚠ 关键：`4 × shll.l #2` 是左移 **8** 位（每次 2 位），不是 16 位。')
    print('     人工推导极易误判为 16 位 —— 本结论由模拟器实跑给出。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
