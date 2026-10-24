"""Symbolic walk of the capability factory 0x10071A60 for every 16-bit capId."""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
from pe_md3 import PE

p = PE()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL

LO, HI = 0x10071A60, 0x100737F0
code = {}


def dis_at(va):
    if va in code:
        return code[va]
    buf = p.read(va, 16)
    one = next(md.disasm(buf, va, 1), None) if buf else None
    code[va] = one
    return one


def step(va, eax, flags):
    """Execute one instruction symbolically on eax. Returns (next_va|None, eax, flags, stop_tag)."""
    i = dis_at(va)
    if i is None:
        return None, eax, flags, 'bad'
    mn, ops = i.mnemonic, i.operands
    nxt = va + i.size
    if mn == 'mov' and ops[0].type == X86_OP_REG and i.reg_name(ops[0].reg) == 'eax':
        if ops[1].type == X86_OP_IMM:
            return nxt, ops[1].imm & 0xFFFFFFFF, flags, None
        return nxt, eax, flags, None
    if mn in ('movzx', 'movsx') and i.reg_name(ops[0].reg) == 'eax' and ops[1].type == X86_OP_MEM:
        m = ops[1].mem
        ea = (eax if m.index and i.reg_name(m.index) == 'eax' else 0) + m.disp
        b = p.read(ea, 1)
        if b is None:
            return None, eax, flags, 'badmem'
        return nxt, struct.unpack('<B', b)[0], flags, None
    if mn in ('add', 'sub') and ops[0].type == X86_OP_REG and i.reg_name(ops[0].reg) == 'eax' and ops[1].type == X86_OP_IMM:
        v = ops[1].imm & 0xFFFFFFFF
        eax = (eax + v) if mn == 'add' else (eax - v)
        return nxt, eax & 0xFFFFFFFF, flags, None
    if mn == 'lea' and i.reg_name(ops[0].reg) == 'eax' and ops[1].type == X86_OP_MEM:
        m = ops[1].mem
        return nxt, (eax + m.disp) & 0xFFFFFFFF, flags, None
    if mn == 'cmp' and ops[0].type == X86_OP_REG and i.reg_name(ops[0].reg) == 'eax' and ops[1].type == X86_OP_IMM:
        return nxt, eax, (eax, ops[1].imm & 0xFFFFFFFF), None
    if mn in ('je', 'jz', 'jne', 'jnz', 'ja', 'jae', 'jb', 'jbe', 'jg', 'jge', 'jl', 'jle', 'js', 'jns', 'jp', 'jnp'):
        if flags is None:
            return nxt, eax, flags, 'noflag'
        a, b = flags
        ua, ub = a & 0xFFFFFFFF, b & 0xFFFFFFFF
        cond = {
            'je': ua == ub, 'jz': ua == ub, 'jne': ua != ub, 'jnz': ua != ub,
            'ja': ua > ub, 'jae': ua >= ub, 'jb': ua < ub, 'jbe': ua <= ub,
            'jg': a > b, 'jge': a >= b, 'jl': a < b, 'jle': a <= b,
        }.get(mn)
        if cond is None:
            return nxt, eax, flags, 'cond'
        if cond:
            return ops[0].imm & 0xFFFFFFFF, eax, flags, None
        return nxt, eax, flags, None
    if mn == 'jmp':
        if ops[0].type == X86_OP_IMM:
            return ops[0].imm & 0xFFFFFFFF, eax, flags, None
        if ops[0].type == X86_OP_MEM:
            m = ops[0].mem
            tab = m.disp & 0xFFFFFFFF
            v = p.u32(tab + 4 * eax)
            return v, eax, flags, 'table' if v else 'badtab'
    if mn == 'call':
        if '0x100ab280' in i.op_str:
            return va, eax, flags, 'new'
        return nxt, eax, flags, 'call'
    if mn in ('ret', 'retn'):
        return None, eax, flags, 'ret'
    return nxt, eax, flags, None


def run(cap):
    va, eax, flags, tag = 0x10071A60, cap, None, None
    for _ in range(300):
        if not (LO <= (va or 0) < HI):
            break
        va, eax, flags, tag = step(va, eax, flags)
        if tag in ('new', 'ret', 'bad', 'badmem', 'badtab', 'cond', 'noflag'):
            break
    return va, tag


def ctor_after(va):
    out = None
    for j in md.disasm(p.read(va + 5, 0x60), va + 5):
        if j.mnemonic == 'call' and j.op_str.startswith('0x'):
            t = int(j.op_str, 16)
            if t == 0x100AB280:
                continue
            out = (t, j.address)
            break
        if j.mnemonic in ('jmp', 'ret', 'retn'):
            break
    return out


if __name__ == '__main__':
    res = {}
    for cap in range(0x10000):
        arm, tag = run(cap)
        if tag == 'new':
            res.setdefault(arm, []).append(cap)

    print('arms:', len(res), 'ids:', sum(len(v) for v in res.values()))
    rows = []
    for arm, ids in sorted(res.items()):
        c = ctor_after(arm)
        rows.append((arm, c, ids))
    with open('factory_ids.txt', 'w', encoding='utf-8') as fh:
        for arm, c, ids in rows:
            fh.write('arm 0x%08X ctor %s  ids(%d): %s\n' % (
                arm,
                ('0x%08X@0x%08X' % c) if c else '-', len(ids),
                ','.join('0x%04X' % x for x in ids)))
    print(open('factory_ids.txt', encoding='utf-8').read()[:4000])
