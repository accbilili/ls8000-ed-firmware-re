"""G3: 枚举 md3 内所有「跳表 + 字节重映射 + 上界比较」开关，并解析 key->arm 映射。
形态：cmp rN, IMM / ja default ; movzx rM, byte [rN + BMAP] ; jmp dword [rM*4 + TAB]
用途：判定这些开关的键空间（是否 = SCSI opcode）。
"""
import os, sys, json, struct, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3cfg as G
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
HERE = os.path.dirname(os.path.abspath(__file__))


def find_switch_sites():
    """全 .text 扫 FF 24 mod=01/10 rm=100 scale=4 的 jmp [reg*4+disp32]。"""
    raw = G.DATA[G.TEXT['roff']: G.TEXT['roff'] + G.TEXT['rsize']]
    out = []
    i = 0
    n = len(raw)
    while True:
        i = raw.find(b'\xff\x24', i)
        if i < 0 or i + 6 > n:
            break
        modrm = raw[i + 2]
        mod = modrm >> 6
        rm = modrm & 7
        if rm == 4 and mod in (1, 2):
            if mod == 1:
                disp = raw[i + 3]
                if disp & 0x80:
                    disp -= 256
                dlen = 1
            else:
                disp = struct.unpack_from('<i', raw, i + 3)[0]
                dlen = 4
            idxreg = (raw[i + 3 + (0 if mod == 2 else 0)] if False else None)
            out.append((G.TLO + i, disp, dlen))
        i += 1
    # 只保留 disp 落在 .text 的（表也在 .text）
    return [(a, d) for a, d, _ in out if G.in_text(d)]


def analyze():
    raw = G.DATA[G.TEXT['roff']: G.TEXT['roff'] + G.TEXT['rsize']]
    res = []
    i = 0
    n = len(raw)
    while True:
        i = raw.find(b'\xff\x24', i)
        if i < 0 or i + 6 > n:
            break
        sib = raw[i + 2]
        if (sib >> 6) != 2:            # scale != 4 → 不是 [r*4+tab]
            i += 1
            continue
        tab = struct.unpack_from('<I', raw, i + 3)[0]
        site = G.TLO + i
        if not G.in_text(tab):
            i += 1
            continue
        # 不要求指令连续（可能有填充/跳转），直接在 site 前 64 字节窗口里
        # 取「最接近 site 的 movzx rM, byte [rN+imm]」与其配套的 cmp rN, imm
        WS = 64
        base = site - WS
        win = G.read(base, WS)
        mv = []
        cp = []
        for j in range(WS):
            one = next(md.disasm(win[j:j + 16], base + j, 1), None)
            if one is None or one.address + one.size > site:
                continue
            ops = one.operands
            if one.mnemonic == 'movzx' and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_MEM:
                m = ops[1].mem
                if m.base and not m.index and one.size >= 6:
                    mv.append((one.address, m.base, m.disp & 0xFFFFFFFF))
            elif one.mnemonic == 'cmp' and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_IMM:
                cp.append((one.address, ops[0].reg, ops[1].imm & 0xFFFFFFFF))
        mv.sort()
        cp.sort()
        bmap = None
        bound = None
        keyreg = None
        if mv:
            _, keyreg, bmap = mv[-1]
            for a, r, v in reversed(cp):
                if r == keyreg:
                    bound = v
                    break
        res.append(dict(site='0x%08X' % site, tab='0x%08X' % tab,
                        bmap='0x%08X' % bmap if bmap else None, bound=bound))
        i += 1
    return res


def keymap(tab, bmap, bound, ntab):
    """key -> arm 地址"""
    if bmap is None or bound is None:
        return None
    bm = G.read(bmap, bound + 1)
    if not bm:
        return None
    out = {}
    for k in range(bound + 1):
        j = bm[k]
        if j >= ntab:
            continue
        t = G.rd32(tab + 4 * j)
        out[k] = t
    return out


if __name__ == '__main__':
    sw = analyze()
    print('FF24/4 站点（表在 .text）:', len(sw))
    withb = [s for s in sw if s['bmap'] and s['bound']]
    print('带 bmap+bound 的:', len(withb))
    for s in withb:
        tab = int(s['tab'], 16)
        # 表长：连续指针
        tl = 0
        while tl < 300 and G.in_text(G.rd32(tab + 4 * tl) or 0):
            tl += 1
        km = keymap(tab, int(s['bmap'], 16), s['bound'], tl)
        if not km:
            continue
        groups = collections.defaultdict(list)
        for k, v in km.items():
            groups[v].append(k)
        print('site %s tab %s(%d) bmap %s bound 0x%X'
              % (s['site'], s['tab'], tl, s['bmap'], s['bound']))
        for v, ks in sorted(groups.items()):
            print('    0x%08X <- keys %s' % (v, ' '.join('0x%02X' % k for k in sorted(ks))))
