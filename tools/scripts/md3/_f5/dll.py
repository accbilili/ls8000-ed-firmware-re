import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

def load(path):
    d = open(path, 'rb').read()
    pe = struct.unpack_from('<I', d, 0x3C)[0]
    n = struct.unpack_from('<H', d, pe + 6)[0]
    optsz = struct.unpack_from('<H', d, pe + 20)[0]
    base = struct.unpack_from('<I', d, pe + 24 + 28)[0]
    secs = []
    for i in range(n):
        o = pe + 24 + optsz + i * 40
        nm = d[o:o+8].rstrip(b'\0').decode('latin1')
        vs, va, rs, ro = struct.unpack_from('<IIII', d, o + 8)
        secs.append((nm, base + va, vs, rs, ro))
    return d, base, secs

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
WANT = {0x00, 0x03, 0x16, 0x17}
for f in (sample('driver/NKDUSCAN.dll'), sample('driver/NKDSBP2.dll')):
    d, base, secs = load(f)
    t = [s for s in secs if s[0] == '.text'][0]
    nm, va, vs, rs, ro = t
    code = d[ro:ro+rs]
    ins = list(md.disasm(code, va))
    print('== %s  base=0x%08X .text=0x%08X..0x%08X insns=%d' % (f.split('\\')[-1], base, va, va+vs, len(ins)))
    byaddr = {i.address: i for i in ins}
    hits = []
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        a, b = i.operands
        if a.type != X86_OP_MEM or a.size != 1 or b.type != X86_OP_IMM: continue
        if b.imm not in WANT: continue
        if not (0 <= a.mem.disp <= 0x10): continue
        bn = i.reg_name(a.mem.base) if a.mem.base else 'abs'
        if bn == 'esp': continue
        # look forward for mov eax, 6/10 within 0x40
        lens = []
        x = i.address
        for _ in range(24):
            j = byaddr.get(x)
            if j is None: break
            if j.mnemonic == 'mov' and len(j.operands) == 2 and j.operands[0].type == X86_OP_REG \
               and i.reg_name(j.operands[0].reg) in ('eax', 'ax') and j.operands[1].type == X86_OP_IMM:
                lens.append(j.operands[1].imm)
            if j.mnemonic.startswith('ret'): break
            x += j.size
        hits.append((i.address, b.imm, bn, a.mem.disp, lens))
    print('   cands=%d' % len(hits))
    for h in hits:
        print('   0x%08X cdb0=0x%02X [%s+0x%X] lens=%s' % h)
