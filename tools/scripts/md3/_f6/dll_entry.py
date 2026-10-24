"""F6 续：反汇编 NKDUSCAN/NKDSBP2 的 NkDriverEntry，找 request 结构 +0x14/+0x18/+0x1C/+0x20。只读 D:\\。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import sys, pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

TARGETS = {
    sample('driver/NKDUSCAN.dll'): 'NkDriverEntry',
    sample('driver/NKDSBP2.dll'): 'NkDriverEntry',
}

# x86 modrm memory operand: base/index/disp extraction
def mem_info(ins, op):
    m = op.mem
    disp = m.disp
    base = m.base
    index = m.index
    scale = m.scale
    return base, index, scale, disp


def scan(path, fname, max_insn=2500):
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    ib = pe.OPTIONAL_HEADER.ImageBase
    ent = None
    for s in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if s.name and s.name.decode() == fname:
            ent = ib + s.address
    print('=' * 72)
    print('%s  %s @ 0x%08X (imagebase 0x%08X)' % (path, fname, ent or 0, ib))
    if ent is None:
        return

    def va2off(va):
        for s in pe.sections:
            if s.VirtualAddress <= va - ib < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
                return s.PointerToRawData + (va - ib - s.VirtualAddress)
        return None

    off = va2off(ent)
    data = pe.get_data(ent - ib, 0x4000)
    print('file off 0x%X' % off)
    n = 0
    hits = {}
    for ins in md.disasm(data, ent):
        if n >= max_insn:
            break
        n += 1
        txt = '0x%08X  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str)
        for op in ins.operands:
            if op.type == 3:  # X86_OP_MEM
                base, index, scale, disp = mem_info(ins, op)
                if disp in (0x14, 0x18, 0x1C, 0x20) and index == 0 and scale == 0:
                    bn = ins.reg_name(base) if base else 'none'
                    hits.setdefault((bn, disp), []).append(ins.address)
                    txt += '   <<< [%s%+d]' % (bn, disp)
        print(txt)
        # stop at ret
        if ins.mnemonic == 'ret':
            if len(hits):
                break
    print('--- struct-ish hits (base_reg, disp) -> first VA list ---')
    for k, v in sorted(hits.items(), key=lambda x: (x[0][0], x[0][1])):
        print('  %s +0x%02X : %d hits, first %s' % (k[0], k[1], len(v), ', '.join('0x%08X' % a for a in v[:6])))


for p, f in TARGETS.items():
    scan(p, f)
