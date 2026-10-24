"""F6: 从三个导出做 request 指针来源传播，收集 [req+off] 访问点。
只读。输出到 stdout（重定向到 _f6/prov.txt）。
"""
import sys, os, collections
import capstone
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

REGS = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp']
REQ, UNK = 'Q', None


def decode_func(start, limit=4000):
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
        if one.mnemonic.startswith('ret') or one.mnemonic in ('int3', 'hlt', 'ud2'):
            break
        if one.mnemonic == 'jmp':
            break
        va += one.size
    return out


def mem_of(ins, i):
    ops = ins.operands
    if i < len(ops) and ops[i].type == X86_OP_MEM:
        return ops[i].mem
    return None


def reg_of(ins, i):
    ops = ins.operands
    if i < len(ops) and ops[i].type == X86_OP_REG:
        return ins.reg_name(ops[i].reg)
    return None


def imm_of(ins, i):
    ops = ins.operands
    if i < len(ops) and ops[i].type == X86_OP_IMM:
        return ops[i].imm
    return None


def size_of(ins, i):
    ops = ins.operands
    return ops[i].size if i < len(ops) else 0


# 访问记录: off -> list of (va, w/r, size, text)
acc = collections.defaultdict(list)
visited = {}          # (func, entryreqregs) -> None
worklist = []         # (func_va, frozenset(req regs at entry))


def add(fva, regs):
    key = (fva, frozenset(regs))
    if key in visited or not (TLO <= fva < THI):
        return
    visited[key] = True
    worklist.append((fva, set(regs)))


def scan(fva, reqregs):
    insns = decode_func(fva)
    env = {r: UNK for r in REGS}
    for r in reqregs:
        env[r] = REQ
    for ins in insns:
        mn = ins.mnemonic
        # 记录内存访问
        for i in range(len(ins.operands)):
            m = mem_of(ins, i)
            if m is None or m.index:
                continue
            b = ins.reg_name(m.base) if m.base else None
            if b and env.get(b) == REQ:
                mode = 'W' if i == 0 else 'R'
                acc[m.disp].append((ins.address, mode, size_of(ins, i), ins.mnemonic + ' ' + ins.op_str))
        # 传播
        if mn == 'push':
            continue
        if mn == 'pop':
            r = reg_of(ins, 0)
            if r:
                env[r] = UNK
            continue
        if mn in ('mov', 'movzx', 'movsx'):
            d = reg_of(ins, 0)
            if d:
                s = reg_of(ins, 1) if len(ins.operands) > 1 else None
                m = mem_of(ins, 1)
                v = UNK
                if s:
                    v = env.get(s)
                elif m is not None and not m.index:
                    b = ins.reg_name(m.base) if m.base else None
                    if b and env.get(b) == REQ and m.disp == 0:
                        v = REQ
                    elif b and env.get(b) == REQ:
                        v = ('PTR', m.disp)
                    elif b and isinstance(env.get(b), tuple):
                        v = ('PTR2', env[b][1], m.disp)
                env[d] = v
            continue
        if mn == 'lea':
            d = reg_of(ins, 0)
            m = mem_of(ins, 1)
            if d:
                v = UNK
                if m is not None and not m.index:
                    b = ins.reg_name(m.base) if m.base else None
                    if b and env.get(b) == REQ:
                        v = ('FIELD', m.disp)
                env[d] = v
            continue
        if mn in ('add', 'sub', 'xor', 'and', 'or'):
            d = reg_of(ins, 0)
            if d:
                env[d] = UNK
            continue
        if mn == 'call':
            t = imm_of(ins, 0)
            if t is not None and 0 < t < 0x100000000:
                # 回溯 push 序列，找哪个参数是 req
                regs = []
                j = len(insns) - 1
                # 用地址索引：找到当前 ins 之前连续的 push
                idx = insns.index(ins)
                k = idx - 1
                while k >= 0 and insns[k].mnemonic == 'push' and len(regs) < 8:
                    pi = insns[k]
                    r = reg_of(pi, 0)
                    m2 = mem_of(pi, 0)
                    v = UNK
                    if r:
                        v = env.get(r)
                    elif imm_of(pi, 0) is not None:
                        v = ('IMM', imm_of(pi, 0))
                    elif m2 is not None and not m2.index:
                        b = ins.reg_name(m2.base) if m2.base else None
                        if b and env.get(b) == REQ:
                            v = ('PTR', m2.disp)
                    regs.append(v)
                    k -= 1
                for j2, v in enumerate(regs):
                    if v == REQ:
                        # stdcall 参数顺序: 第一个 push 是最后一个参数；这里无法确定数量
                        # 用保守法：所有被 push 的 req 都视作「该函数有 req 参数」
                        add(t, {'esi', 'edi', 'ebx', 'ebp', 'eax', 'ecx', 'edx'})
                        # 记录到 target 的种子：用「第 n 个参数」不可知，故用全寄存器保守种子
                        reqseeds.setdefault(t, []).append((ins.address, len(regs) - j2, len(regs)))
                        break
            # 清空易失寄存器
            for r in ('eax', 'ecx', 'edx'):
                env[r] = UNK
            continue
        if mn.startswith('j'):
            continue
        # 其它：目的寄存器作废
        d = reg_of(ins, 0)
        if d and mn not in ('cmp', 'test'):
            env[d] = UNK


reqseeds = {}

# 三个导出：request 所在寄存器
add(0x10027600, {'esi', 'edi', 'ebx', 'ebp', 'eax', 'ecx', 'edx'})  # 占位，下面单独处理
worklist.clear(); visited.clear()

# 手工种子（依据前轮 dispatch.md 的参数位点）
seeds = [
    (0x10091D50, ['ebp']),   # NkCtrlEntry 分派器: ebp = request
    (0x1000B520, ['eax', 'ecx', 'edx']),  # 占位
]
print('=== manual seed 1: NkCtrlEntry dispatcher ===')
scan(0x10091D50, ['ebp'])
print('OK')
