"""F6: 找 call/jmp/lea/mov imm32 引用某 VA 的站点。"""
import sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM

sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3')
from pe_md3 import PE

p = PE()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
WANT = set(int(x, 0) for x in sys.argv[1:])

hits = []
va = TLO
while va < THI:
    buf = p.read(va, 16)
    if not buf:
        break
    one = next(md.disasm(buf, va, 1), None)
    if one is None:
        va += 1
        continue
    for i, op in enumerate(one.operands):
        if op.type == X86_OP_IMM and (op.imm & 0xFFFFFFFF) in WANT:
            hits.append((va, one.mnemonic, one.op_str))
        elif op.type == X86_OP_MEM and op.mem.disp in WANT:
            hits.append((va, one.mnemonic, one.op_str))
    va += one.size

for h in hits:
    print('0x%08X  %-8s %s' % h)
print('total', len(hits))
