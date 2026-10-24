"""F6 续 v9：在 LS8000.md3 里定位 NkDriverEntry 函数指针的实际调用点。
思路：找 `mov R1,[R2+4]` 之后 40 条指令内出现 `call R1` 的位点。只读 D:\\。"""
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
from capstone.x86 import X86_OP_MEM, X86_OP_REG

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

P = sample('driver/LS8000.md3')
pe = pefile.PE(P, fast_load=True)
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

tx = [s for s in sec if s[4] == '.text'][0]
lo, hi, praw, sraw, nm = tx
data = pe.__data__[praw:praw + sraw]
insns = list(md.disasm(data, lo))
print('.text insns %d' % len(insns))

WIN = 40
found = []
for i, ins in enumerate(insns):
    if ins.mnemonic != 'mov' or len(ins.operands) != 2:
        continue
    dst, src = ins.operands
    if dst.type != X86_OP_REG or src.type != X86_OP_MEM:
        continue
    if src.mem.index or src.mem.disp != 4 or not src.mem.base:
        continue
    dstreg = ins.reg_name(dst.reg)
    # 向后找 call dstreg
    for j in range(i + 1, min(i + WIN, len(insns))):
        nj = insns[j]
        if nj.mnemonic in ('call', 'jmp') and len(nj.operands) == 1 and nj.operands[0].type == X86_OP_REG:
            if nj.reg_name(nj.operands[0].reg) == dstreg:
                found.append((ins.address, nj.address, ins.reg_name(src.mem.base), dstreg))
                break
        # 若目标寄存器被其它 mov 覆盖则放弃
        if nj.mnemonic == 'mov' and len(nj.operands) == 2 and nj.operands[0].type == X86_OP_REG:
            if nj.reg_name(nj.operands[0].reg) == dstreg:
                break
        if nj.mnemonic in ('pop',):
            pass
print('候选 %d 处' % len(found))
seen = set()
for src_va, call_va, basereg, reg in found:
    key = (call_va & ~0xFFF)
    print('0x%08X mov %s,[%s+4]   0x%08X call %s' % (src_va, reg, basereg, call_va, reg))
print('--- 唯一 call 位点所在 4K 页 ---')
pages = sorted(set(c >> 12 for _, c, _, _ in found))
print(', '.join('0x%05X000' % p for p in pages[:40]))
