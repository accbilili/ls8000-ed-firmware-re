"""
H8/300H 指令子集模拟器 —— 用于精确定案 E0 参数组装公式

为什么需要模拟器
----------------
人工推导 H8 的字节搬移 + 移位语义极易出错（本次就错了一次：
把 `shll.l #2` 连用 4 次当成移 16 位，实际是移 8 位）。
模拟器直接按指令语义执行，给出确定答案。

支持的指令子集（覆盖本项目用到的全部形态）
--------------------------------------------
  mov.b  Rm,@ERn          写 ERn 的低 8 位
  mov.b  Rm,@abs16/32     写绝对地址的低 8 位
  mov.b  @ERn,Rm          从 ERn 低 8 位读
  mov.b  @abs16/32,Rm     从绝对地址读
  mov.b  Rm,@d8(ERn)      写 ERn+d8 的低 8 位
  mov.b  @d8(ERn),Rm      读
  mov.w  Rm,ERn           写 ERn 高 16 位   ← H8 特有，易错点
  mov.w  Rm,@abs16/32     写绝对地址的 16 位
  mov.w  @ERn,Rm          读 ERn 低 16 位
  mov.l  ERm,@abs32       写绝对地址的 32 位
  mov.l  @abs32,ERm       读绝对地址的 32 位
  mov.l  ERm,ERn          32 位整体传送
  mov.b  Rm,Rh            字节搬移 Rm低字节 → Rh高字节
  sub.l  ERm,ERn          ERn -= ERm
  sub.w  Rm,Rn            16 位清零
  sub.b  Rm,Rn            8 位清零
  add.l  ERm,ERn          ERn += ERm
  shll.l #n,ERm           32 位逻辑左移 n 位
  extu.w Rm               零扩展 16→32（写 ERm 高16位，ERm 低16位不变）
  cmp.l  #imm32,ERm       比较
  cmp.b  #imm8,Rm
"""
import re


class H8Sim:
    def __init__(self, rom, base=0x10000):
        self.rom = rom
        self.base = base
        self.er = [0] * 8       # er0..er7 (32 位)
        self.pc = 0

    # ---- 寄存器视图 ----
    def get_er(self, n):
        return self.er[n]

    def set_er(self, n, v):
        self.er[n] = v & 0xFFFFFFFF

    def reg16(self, n):
        """ERn 的低 16 位（Rn）。"""
        return self.er[n] & 0xFFFF

    def set_reg16(self, n, v):
        self.er[n] = (self.er[n] & 0xFFFF0000) | (v & 0xFFFF)

    def reg8(self, n):
        """ERn 的低 8 位（RnL）。"""
        return self.er[n] & 0xFF

    def set_reg8(self, n, v):
        self.er[n] = (self.er[n] & 0xFFFFFF00) | (v & 0xFF)

    def reg8h(self, n):
        """ERn 低 16 位中的高字节（RnH）。"""
        return (self.er[n] >> 8) & 0xFF

    def set_reg8h(self, n, v):
        self.er[n] = (self.er[n] & 0xFFFF00FF) | ((v & 0xFF) << 8)

    def hi16(self, n):
        """ERn 的高 16 位（En）。"""
        return (self.er[n] >> 16) & 0xFFFF

    def set_hi16(self, n, v):
        self.er[n] = ((v & 0xFFFF) << 16) | (self.er[n] & 0xFFFF)

    # ---- 访存 ----
    def read8(self, addr):
        off = addr - self.base
        if 0 <= off < len(self.rom):
            return self.rom[off]
        return 0

    def write8(self, addr, v):
        # 只记录，不改 ROM
        pass

    def read16(self, addr):
        return (self.read8(addr) << 8) | self.read8(addr + 1)

    def read32(self, addr):
        return (self.read16(addr) << 16) | self.read16(addr + 2)

    def write16(self, addr, v):
        pass

    def write32(self, addr, v):
        pass


def _rn(tok):
    """er0..er7 → 索引；也接受 e0..e7（= ERn 的高 16 位）。"""
    m = re.match(r'^er(\d)$', str(tok))
    if m:
        return int(m.group(1))
    m = re.match(r'^e(\d)$', str(tok))
    if m:
        return int(m.group(1))
    return None


def _rn_plain(tok):
    """r0..r7 → 索引。"""
    m = re.match(r'^r(\d)$', str(tok))
    return int(m.group(1)) if m else None


def _abs(tok):
    """@0x... 或 @(d:32,ERn) 之类，返回 ('abs', addr) 或 ('disp', eridx, disp)"""
    m = re.match(r'^@0x([0-9a-fA-F]+)$', tok)
    if m:
        return ('abs', int(m.group(1), 16))
    m = re.match(r'^@\(0x([0-9a-fA-F]+),er(\d)\)$', tok)
    if m:
        return ('disp', int(m.group(2)), int(m.group(1), 16))
    m = re.match(r'^@\((-?\d+),er(\d)\)$', tok)
    if m:
        return ('disp', int(m.group(2)), int(m.group(1)))
    return None


def simulate(sim, insns, mem=None, trace=False):
    """执行一组已解码的指令。

    insns: [(addr, name, a1, a2), ...]
    mem:   {addr: byte} 可写内存（RAM 模拟）
    """
    if mem is None:
        mem = {}

    def r8(a):
        if isinstance(a, tuple) and a[0] == 'abs':
            return mem.get(a[1], sim.read8(a[1]))
        if isinstance(a, tuple) and a[0] == 'disp':
            base = sim.get_er(a[1])
            return mem.get(base + a[2], sim.read8(base + a[2]))
        return None

    def w8(a, v):
        if isinstance(a, tuple) and a[0] == 'abs':
            mem[a[1]] = v & 0xFF
        elif isinstance(a, tuple) and a[0] == 'disp':
            base = sim.get_er(a[1])
            mem[base + a[2]] = v & 0xFF

    def r16(a):
        if isinstance(a, tuple) and a[0] == 'abs':
            hi = mem.get(a[1], sim.read8(a[1]))
            lo = mem.get(a[1] + 1, sim.read8(a[1] + 1))
            return (hi << 8) | lo
        return None

    def r32(a):
        if isinstance(a, tuple) and a[0] == 'abs':
            return sim.read32(a[1])
        return None

    log = []
    for addr, name, a1, a2 in insns:
        before = list(sim.er)
        note = ''

        if name == 'mov.b':
            # 形态：mov.b src, dst
            #   src ∈ {r0l..r7l, @(d,erN), @abs16/32}
            #   dst ∈ {r0l..r7l, r0h..r7h, @abs16/32}
            src, dst = a1, a2
            sval = None
            if re.match(r'^r\d[hl]$', str(src)):
                n = _rn_plain(str(src)[:2]) if str(src)[1] == 'l' else None
                sidx = int(str(src)[1])
                if str(src).endswith('l'):
                    sval = sim.reg8(sidx)
                else:
                    sval = sim.reg8h(sidx)
            elif isinstance(src, str) and src.startswith('@'):
                t = _abs(src)
                if t:
                    if t[0] == 'abs':
                        sval = mem.get(t[1], sim.read8(t[1]))
                    else:
                        base = sim.get_er(t[1])
                        sval = mem.get(base + t[2], sim.read8(base + t[2]))
            if sval is None:
                pass
            elif re.match(r'^r\d[hl]$', str(dst)):
                didx = int(str(dst)[1])
                if str(dst).endswith('l'):
                    sim.set_reg8(didx, sval)
                else:
                    sim.set_reg8h(didx, sval)
                note = '%s = 0x%02X' % (dst, sval)
            elif isinstance(dst, str) and dst.startswith('@'):
                t = _abs(dst)
                if t and t[0] == 'abs':
                    mem[t[1]] = sval & 0xFF
                    note = 'mem[0x%06X] = 0x%02X' % (t[1], sval)

        elif name == 'mov.w':
            # mov.w src, dst —— 关键：dst 若是 En 写 ERn 高 16 位
            src, dst = a1, a2
            if re.match(r'^r\d$', src):
                sv = sim.reg16(_rn_plain(src))
                if re.match(r'^e\d$', dst):
                    sim.set_hi16(_rn(dst), sv)
                    note = 'e%d = 0x%04X (ER%d 高16位)' % (_rn(dst), sv, _rn(dst))
                elif re.match(r'^r\d$', dst):
                    sim.set_reg16(_rn_plain(dst), sv)
                elif isinstance(dst, str) and dst.startswith('@'):
                    w8(_abs(dst), (sv >> 8) & 0xFF)
                    w8(('abs', _abs(dst)[1] + 1), sv & 0xFF)
            elif isinstance(src, str) and src.startswith('@'):
                t = _abs(src)
                if t and t[0] == 'abs':
                    sv = r16(t)
                    if re.match(r'^r\d$', dst):
                        sim.set_reg16(_rn_plain(dst), sv)

        elif name == 'mov.l':
            src, dst = a1, a2
            if isinstance(dst, str) and dst.startswith('@'):
                t = _abs(dst)
                v = None
                if re.match(r'^er\d$', src):
                    v = sim.get_er(_rn(src))
                elif isinstance(src, str) and src.startswith('@'):
                    t2 = _abs(src)
                    if t2 and t2[0] == 'abs':
                        v = r32(t2)
                if v is not None and t and t[0] == 'abs':
                    ad = t[1]
                    mem[ad] = (v >> 24) & 0xFF
                    mem[ad + 1] = (v >> 16) & 0xFF
                    mem[ad + 2] = (v >> 8) & 0xFF
                    mem[ad + 3] = v & 0xFF
                    note = 'mem[0x%06X..] = 0x%08X (BE)' % (ad, v)
            elif isinstance(src, str) and src.startswith('@'):
                t2 = _abs(src)
                if t2 and t2[0] == 'abs':
                    v = r32(t2)
                    if re.match(r'^er\d$', dst):
                        sim.set_er(_rn(dst), v)
            elif re.match(r'^er\d$', src) and re.match(r'^er\d$', dst):
                sim.set_er(_rn(dst), sim.get_er(_rn(src)))

        elif name == 'sub.l':
            if re.match(r'^er\d$', a1) and re.match(r'^er\d$', a2):
                sim.set_er(_rn(a2), sim.get_er(_rn(a2)) - sim.get_er(_rn(a1)))
                note = 'ER%d = 0x%08X' % (_rn(a2), sim.get_er(_rn(a2)))

        elif name == 'sub.w':
            if re.match(r'^r\d$', str(a1)) and re.match(r'^r\d$', str(a2)):
                sim.set_reg16(_rn_plain(a2), 0)
                note = 'r%d = 0' % _rn_plain(a2)

        elif name == 'sub.b':
            # a1/a2 可能是 r0l / r0h 形式
            for tok, op in ((a1, 'src'), (a2, 'dst')):
                pass
            s_tok, d_tok = str(a1), str(a2)
            if re.match(r'^r\d[hl]$', s_tok) and re.match(r'^r\d[hl]$', d_tok):
                didx = int(d_tok[1])
                if d_tok.endswith('l'):
                    sim.set_reg8(didx, 0)
                else:
                    sim.set_reg8h(didx, 0)
                note = '%s = 0' % d_tok
            elif re.match(r'^r\d$', s_tok) and re.match(r'^r\d$', d_tok):
                sim.set_reg16(_rn_plain(d_tok), 0)
                note = 'r%d = 0' % _rn_plain(d_tok)

        elif name == 'add.l':
            if re.match(r'^er\d$', a1) and re.match(r'^er\d$', a2):
                sim.set_er(_rn(a2), sim.get_er(_rn(a2)) + sim.get_er(_rn(a1)))
                note = 'ER%d = 0x%08X' % (_rn(a2), sim.get_er(_rn(a2)))

        elif name == 'shll.l':
            m = re.match(r'^#(\d+)$', a1)
            n = int(m.group(1)) if m else 1
            if re.match(r'^er\d$', a2):
                sim.set_er(_rn(a2), (sim.get_er(_rn(a2)) << n) & 0xFFFFFFFF)
                note = 'ER%d <<= %d → 0x%08X' % (_rn(a2), n, sim.get_er(_rn(a2)))

        elif name == 'extu.w':
            if re.match(r'^r\d$', a1):
                n = _rn_plain(a1)
                v = sim.reg16(n)
                sim.set_hi16(n, v)
                note = 'e%d = 0x%04X' % (n, v)

        elif name == 'cmp.b':
            pass

        if trace:
            log.append((addr, name, a1, a2, before, list(sim.er), note))

    return log
