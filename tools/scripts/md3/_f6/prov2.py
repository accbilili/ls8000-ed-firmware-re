"""F6: request 指针来源传播（局部 + 单参数调用下沉）。
给定若干 (函数VA, {寄存器: 'Q'}) 种子，记录 [req+0..0x60] 的读写点。
只读；输出 stdout。
"""
import sys, os, collections, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3')
from pe_md3 import PE

p = PE()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
ALL = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp']
Q = 'REQ'
UNK = None

acc = collections.defaultdict(list)      # off -> [(va, 'R'/'W', size, text, func)]
done = set()
queue = []
calllog = []


def decode_func(start, limit=600):
    out = []
    va = start
    while len(out) < limit:
        buf = p.read(va, 16)
        if not buf:
            break
        one = next(md.disasm(buf, va, 1), None)
        if one is None:
            break
        out.append(one)
        if one.mnemonic.startswith('ret') or one.mnemonic in ('int3', 'hlt', 'ud2', 'jmp'):
            break
        va += one.size
    return out


def scan(fva, seedregs, pin=True):
    key = (fva, frozenset(seedregs.items()))
    if key in done:
        return
    done.add(key)
    insns = decode_func(fva)
    if not insns:
        return
    env = {r: UNK for r in ALL}
    for r in seedregs:
        env[r] = Q
    for idx, ins in enumerate(insns):
        mn, ops = ins.mnemonic, ins.operands
        for i in range(len(ops)):
            m = ops[i].type == X86_OP_MEM and ops[i].mem
            if not m or m.index:
                continue
            b = ins.reg_name(m.base) if m.base else None
            if b and env.get(b) == Q and 0 <= m.disp <= 0x60:
                acc[m.disp].append((ins.address, 'W' if i == 0 else 'R', ops[i].size,
                                    mn + ' ' + ins.op_str, fva))
        if mn == 'push':
            continue
        if mn in ('mov', 'movzx', 'movsx'):
            d = ops[0]
            if d.type == X86_OP_REG:
                dn = ins.reg_name(d.reg)
                v = UNK
                if len(ops) > 1:
                    s = ops[1]
                    if s.type == X86_OP_REG:
                        v = env.get(ins.reg_name(s.reg))
                    elif s.type == X86_OP_MEM and not s.mem.index:
                        b = ins.reg_name(s.mem.base) if s.mem.base else None
                        if b and env.get(b) == Q:
                            v = Q if s.mem.disp == 0 else ('P', s.mem.disp)
                if not (pin and dn in seedregs):
                    env[dn] = v
            continue
        if mn == 'lea':
            d, s = ops[0], ops[1]
            if d.type == X86_OP_REG and s.type == X86_OP_MEM and not s.mem.index:
                b = ins.reg_name(s.mem.base) if s.mem.base else None
                env[ins.reg_name(d.reg)] = (('FLD', s.mem.disp) if b and env.get(b) == Q else UNK)
            continue
        if mn == 'call':
            t = ops[0].type == X86_OP_IMM and ops[0].imm & 0xFFFFFFFF
            if t and TLO <= t < THI:
                # 回溯连续 push
                args = []
                k = idx - 1
                while k >= 0 and insns[k].mnemonic == 'push' and len(args) < 8:
                    pi = insns[k]
                    v = UNK
                    if pi.operands[0].type == X86_OP_REG:
                        v = env.get(pi.reg_name(pi.operands[0].reg))
                    elif pi.operands[0].type == X86_OP_MEM and not pi.operands[0].mem.index:
                        b = pi.reg_name(pi.operands[0].mem.base) if pi.operands[0].mem.base else None
                        if b and env.get(b) == Q:
                            v = ('P', pi.operands[0].mem.disp)
                    args.append(v)
                    k -= 1
                hit = [(j, v) for j, v in enumerate(args) if v == Q]
                calllog.append((ins.address, t, len(args), hit))
                if hit and len(args) == 1:
                    # 被调函数唯一参数 = req：找其入口的 mov R,[esp+4] / [ebp+8]
                    callee = decode_func(t, 20)
                    reg = None
                    for ci in callee:
                        if ci.mnemonic == 'mov' and ci.operands[0].type == X86_OP_REG \
                                and ci.operands[1].type == X86_OP_MEM and ci.operands[1].mem.disp == 4 \
                                and ci.operands[1].mem.base and ci.reg_name(ci.operands[1].mem.base) == 'esp':
                            reg = ci.reg_name(ci.operands[0].reg)
                            break
                    if reg:
                        scan(t, {reg: Q})
            for r in ('eax', 'ecx', 'edx'):
                env[r] = UNK
            continue
        if mn.startswith('j') or mn in ('cmp', 'test', 'nop') or not ops:
            continue
        d = ops[0]
        if d.type == X86_OP_REG and mn not in ('cmp', 'test'):
            env[ins.reg_name(d.reg)] = UNK


SEEDS = [
    (0x10091D50, {'ebp': Q}),    # NkCtrlEntry 分派器
    (0x10091CF0, {'edi': Q}),    # 前置 map 查表
    (0x1000B220, {'esi': Q}),    # NkMDCtrlEntry sel1
    (0x1000B270, {'eax': Q}),    # sel2
    (0x1000B2A0, {'esi': Q}),    # sel3
    (0x1000B3A0, {'esi': Q}),    # sel4
    (0x10092770, {'ebp': Q}),    # vt[2] sel1 -> 0x10092770
    (0x10092EE0, {'esi': Q}),    # vt[5]
    (0x10091C70, {'esi': Q}),    # vt[11]
    (0x10091CB0, {'esi': Q}),    # vt[12]
    (0x10091C10, {'eax': Q}),    # vt[4]
    (0x10091AE0, {'esi': Q}),    # vt[7]
]

for f, s in SEEDS:
    scan(f, s)

print('### 按偏移汇总（req+off, 0..0x60）')
for off in sorted(acc):
    rows = acc[off]
    w = sum(1 for r in rows if r[1] == 'W')
    print('+0x%02X  n=%-3d  W=%-3d R=%-3d' % (off, len(rows), w, len(rows) - w))
    for r in rows[:8]:
        print('     0x%08X %s/%d %-40s in 0x%08X' % r)

print()
print('### 单参数调用下沉记录（只列有 req 作为唯一实参的）')
for c in calllog:
    if c[3] and c[2] == 1:
        print('call@0x%08X -> 0x%08X' % (c[0], c[1]))
