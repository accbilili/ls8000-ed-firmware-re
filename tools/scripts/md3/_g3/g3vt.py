"""G3: vtable 抽取 + ctor->vtable 归属。"""
import os, sys, json, struct, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3cfg as G
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_ECX

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g3vt.pkl')


def vt_slots(vt, cap=64):
    out = []
    for i in range(cap):
        v = G.rd32(vt + 4 * i)
        if v is None or not G.in_text(v):
            break
        out.append(v)
    return out


def walk_func(va, maxins=4000, maxbytes=20000):
    """从 va 顺序解码到 ret/jmp，返回指令列表 (addr,mnem,opstr,size,hex,operands)。"""
    out = []
    cur = va
    n = 0
    while G.in_text(cur) and n < maxins and (cur - va) < maxbytes:
        buf = G.read(cur, 16)
        if not buf:
            break
        one = next(md.disasm(buf, cur, 1), None)
        if one is None:
            break
        out.append((one.address, one.mnemonic, one.op_str, one.size,
                    one.bytes.hex(), one.operands))
        n += 1
        if one.mnemonic in ('ret', 'retn', 'int3', 'hlt', 'ud2'):
            break
        if one.mnemonic == 'jmp' and one.operands and one.operands[0].type == X86_OP_IMM:
            break
        cur += one.size
    return out


def ctor_vtables(va, maxins=4000):
    """函数体内的 vtable 写入记录。
    追踪 this 指针寄存器偏移（mov rX, this / lea rY,[rX+d]），
    返回 (insns, vt_recs)；vt_recs = [(insn_addr, eff_disp, imm)]，eff_disp 是相对对象头的偏移。
    """
    ins = walk_func(va, maxins)
    if not ins:
        return [], []
    # 找 this 寄存器：第一个 mov r32, ecx（ecx 为 thiscall 的 this）
    thisreg = None
    for a, mn, op, sz, hx, ops in ins:
        if mn == 'mov' and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_REG and ops[1].reg == X86_REG_ECX:
            thisreg = ops[0].reg
            break
    off = {}          # reg_id -> 相对对象头的偏移
    if thisreg is not None:
        off[thisreg] = 0
        off[X86_REG_ECX] = 0
    recs = []
    for a, mn, op, sz, hx, ops in ins:
        if mn == 'lea' and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM:
            m = ops[1].mem
            b = m.base
            if b in off:
                off[ops[0].reg] = off[b] + (m.disp & 0xFFFFFFFF)
            continue
        if mn == 'mov' and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
            if ops[1].reg in off:
                off[ops[0].reg] = off[ops[1].reg]
            continue
        if mn != 'mov' or len(ops) != 2:
            continue
        dst, src = ops
        if dst.type != X86_OP_MEM or src.type != X86_OP_IMM or dst.size != 4:
            continue
        imm = src.imm & 0xFFFFFFFF
        if not G.in_rdata(imm):
            continue
        b = dst.mem.base
        if b in off:
            recs.append((a, off[b] + (dst.mem.disp & 0xFFFFFFFF), imm))
    return ins, recs


if __name__ == '__main__':
    r = G.load()
    caps = json.load(open(os.path.join(os.path.dirname(CACHE), '..', 'dispatch_caps.json')))['caps']
    print('caps', len(caps))
    missing = [c for c in caps if int(c['handler'], 16) not in set(r['funcs'])]
    print('ctors not in cfg funcs:', len(missing))
    vtmap = {}
    for c in caps[:24]:
        va = int(c['handler'], 16)
        ins, vts = ctor_vtables(va)
        prim = [x for x in vts if x[1] == 0]
        allv = [x for x in vts]
        print('%s -> %s  n=%d  eff0=%s  all=%s' %
              (c['cap_hex'], c['handler'], len(vts),
               ['0x%08X' % x[2] for x in prim],
               [(hex(x[1]), '0x%08X' % x[2]) for x in allv]))
