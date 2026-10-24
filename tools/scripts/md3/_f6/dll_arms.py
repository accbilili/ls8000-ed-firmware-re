"""F6 续 v5：对 Nk*.dll 的 NkDriverEntry 各点钟函数做简洁指针跟踪，
检查 request(=arg1) 是否被按 +0x14/+0x18/+0x1C/+0x20 解读。只读 D:\\。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

ARM_INTEREST = {0x14, 0x18, 0x1C, 0x20}

CASES = [
    (sample('driver/NKDUSCAN.dll'), 0x10003C40, 0x10003DC8, 9, 'NKDUSCAN'),
    (sample('driver/NKDSBP2.dll'), 0x100041D0, 0x10004358, 9, 'NKDSBP2'),
]
# NKDUSCAN 各点钟内部函数（手工从 NkDriverEntry 机读）
ARMS = {
    'NKDUSCAN': {1: 0x10003E30, 2: 0x10004240, 3: 0x10004290, 4: 0x100042E0,
                 5: 0x10003FD0, 6: 0x10003F90, 7: 0x10003F10, 8: 0x100040C0},
}


def setup(path):
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
    ib = pe.OPTIONAL_HEADER.ImageBase
    iat = {}
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        for imp in e.imports:
            iat.setdefault(imp.address, imp.name.decode() if imp.name else 'ord#%d' % imp.ordinal)
    sec = []
    for s in pe.sections:
        sec.append((ib + s.VirtualAddress, ib + s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
                    s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b'\0').decode()))
    return pe, ib, iat, sec


def rd(pe, sec, va, ln):
    for (lo, hi, praw, sraw, nm) in sec:
        if lo <= va < hi:
            off = praw + (va - lo)
            return pe.__data__[off:off + ln]
    return b''


def track(pe, sec, iat, fn, max_insn=400):
    """返回 (行, [(va, base, disp)]) —— 简洁跟踪 arg1"""
    lines, hits = [], []
    state = {}          # reg -> tag
    stackoff = {}       # esp-rel -> tag (未用)
    ebp_off = {}        # ebp+X -> tag
    data = rd(pe, sec, fn, 0x1800)
    n = 0
    for ins in md.disasm(data, fn):
        if n >= max_insn:
            break
        n += 1
        m, ops = ins.mnemonic, ins.operands
        note = []
        # 识别 prologue: push ebp ; mov ebp,esp
        if m == 'mov' and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
            pass
        # mov reg, [X]
        if m in ('mov', 'lea') and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM:
            src = ops[1].mem
            tag = None
            if ins.reg_name(src.base) in ('esp', 'ebp') and src.index == 0:
                if src.base and ins.reg_name(src.base) == 'ebp':
                    tag = ebp_off.get(src.disp)
                else:
                    tag = 'LOCAL' if src.disp >= 8 else None
            elif ins.reg_name(src.base) in state:
                tag = state[ins.reg_name(src.base)]
            if tag:
                state[ins.reg_name(ops[0].reg)] = tag if ins.mnemonic == 'mov' else tag
        # mov reg2, reg1
        if m == 'mov' and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
            if ins.reg_name(ops[1].reg) in state:
                state[ins.reg_name(ops[0].reg)] = state[ins.reg_name(ops[1].reg)]
            elif ins.reg_name(ops[0].reg) in state:
                del state[ins.reg_name(ops[0].reg)]
        # 访问
        for op in ops:
            if op.type == X86_OP_MEM:
                mm = op.mem
                b = ins.reg_name(mm.base) if mm.base else None
                tag = state.get(b)
                if b not in ('esp', 'ebp') and mm.disp in ARM_INTEREST:
                    hits.append((ins.address, b, mm.disp, tag))
                    note.append('[disp+0x%02X base=%s tag=%s]' % (mm.disp, b, tag))
        # ebp 基址框架：把 [ebp+8]->ARG1, [ebp+0xC]->ARG2 记下来
        for op in ops:
            if op.type == X86_OP_MEM and op.mem.base and ins.reg_name(op.mem.base) == 'ebp':
                pass
        ln = '0x%08X  %-7s %s' % (ins.address, m, ins.op_str)
        for op in ops:
            if op.type == X86_OP_MEM and op.mem.base == 0 and op.mem.index == 0 and op.mem.disp in iat:
                ln += '   ; %s' % iat[op.mem.disp]
        if note:
            ln += '   <<< ' + ' '.join(note)
        lines.append(ln)
        if m == 'ret':
            break
    return lines, hits


for path, entry, tbl, cnt, tag in CASES:
    pe, ib, iat, sec = setup(path)
    print('=' * 78)
    print('%s  NkDriverEntry 0x%08X' % (tag, entry))
    for sel in range(1, cnt + 1):
        fn = None
        if tag in ARMS and sel in ARMS[tag]:
            fn = ARMS[tag][sel]
        else:
            continue
        lines, hits = track(pe, sec, iat, fn)
        print('-' * 70)
        print('selector %d -> 0x%08X   (%d insns)' % (sel, fn, len(lines)))
        for h in hits:
            print('    HIT 0x%08X  base=%s disp=+0x%02X tag=%s' % h)
        # 只打印命中的上下文（前后 6 行）
        shown = set()
        for h in hits:
            for i, ln in enumerate(lines):
                if ln.startswith('0x%08X' % h[0]):
                    for j in range(max(0, i - 6), min(len(lines), i + 4)):
                        shown.add(j)
        if shown:
            for j in sorted(shown):
                print('   ', lines[j])
