"""F6 续 v7：在两个 Nk*.dll 的 .text 里找「同一基址寄存器、同窗口内同时读
+0x14/+0x18/+0x1C/+0x20」的位置，用于核验 REPORT §13.1 的 request 布局。只读 D:\\。"""
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
from capstone.x86 import X86_OP_MEM

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
md.detail = True

DLLS = [sample('driver/NKDUSCAN.dll'), sample('driver/NKDSBP2.dll')]
INTEREST = {0x14, 0x18, 0x1C, 0x20}
WIN = 40


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


for path in DLLS:
    pe, ib, iat, sec = setup(path)
    tx = [s for s in sec if s[4] == '.text'][0]
    lo, hi, praw, sraw, nm = tx
    data = pe.__data__[praw:praw + sraw]
    insns = []
    for ins in md.disasm(data, lo):
        insns.append(ins)
    print('=' * 78)
    print('%s  .text %d insns' % (path, len(insns)))
    # 收集 (idx, base, disp)
    cands = []
    for i, ins in enumerate(insns):
        for op in ins.operands:
            if op.type == X86_OP_MEM:
                b = ins.reg_name(op.mem.base) if op.mem.base else ''
                if op.mem.disp in INTEREST and op.mem.index == 0:
                    cands.append((i, b, op.mem.disp, ins.address))
    # 按 (base) 分桶滑窗
    from collections import defaultdict
    bybase = defaultdict(list)
    for i, b, d, va in cands:
        bybase[b].append((i, d, va))
    scored = []
    for b, lst in bybase.items():
        lst.sort()
        for k in range(len(lst)):
            j = k
            has = {}
            while j < len(lst) and lst[j][0] - lst[k][0] <= WIN:
                has.setdefault(lst[j][1], lst[j][2])
                j += 1
            if len(has) == 4:
                scored.append((lst[k][2], b, has))
    scored.sort()
    print('  候选窗口 %d 个' % len(scored))
    for rank, (va, b, has) in enumerate(scored[:6]):
        print('-' * 70)
        print('#%d base=%s  start=0x%08X  +0x14@0x%08X +0x18@0x%08X +0x1C@0x%08X +0x20@0x%08X'
              % (rank + 1, b, va, has[0x14], has[0x18], has[0x1C], has[0x20]))
        i0 = insns.index(next(x for x in insns if x.address == va))
        for ins in insns[max(0, i0 - 24):i0 + 30]:
            line = '0x%08X  %-7s %s' % (ins.address, ins.mnemonic, ins.op_str)
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == 0 and op.mem.index == 0 and op.mem.disp in iat:
                    line += '   ; %s' % iat[op.mem.disp]
            print('   ', line)
