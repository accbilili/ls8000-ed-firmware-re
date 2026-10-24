import sys
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

ins = sweep(TEXT_LO, TEXT_HI)
byaddr = {i.address: i for i in ins}
order = sorted(byaddr)

def fwd(site, lim=0x60):
    out = []; a = site
    while a < site + lim:
        i = byaddr.get(a)
        if i is None: break
        out.append(i); a += i.size
        if i.mnemonic.startswith('ret'): break
    return out

def start_of(site):
    best = None
    prev = [x for x in order if x < site]
    # walk backwards through decoded instructions
    idx = order.index(site)
    j = idx
    while j > 0 and site - order[j] < 0x60:
        p = order[j-1]
        if byaddr[p].mnemonic.startswith('ret') or byaddr[p].mnemonic == 'nop' or byaddr[p].mnemonic == 'int3':
            best = order[j]; break
        j -= 1
    return best

def scan(want):
    print('=== cdb0 = 0x%02X' % want)
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type != X86_OP_MEM or d.size != 1 or s.type != X86_OP_IMM: continue
        if s.imm != want: continue
        if not (0 <= d.mem.disp <= 0x10): continue
        if d.mem.base == 0 or i.reg_name(d.mem.base) == 'esp': continue
        st = start_of(i.address)
        body = fwd(i.address)
        rets = [x for x in body if x.mnemonic.startswith('ret')]
        lens = [(x.address, x.operands[1].imm) for x in body
                if x.mnemonic == 'mov' and len(x.operands) == 2
                and x.operands[0].type == 1 and i.reg_name(x.operands[0].reg) in ('eax', 'ax')
                and x.operands[1].type == X86_OP_IMM]
        tag = 'BUILDER' if (rets and lens and lens[-1][0] > i.address) else ''
        print('  site=0x%08X disp=0x%-3X func=%s len=%s %s' %
              (i.address, d.mem.disp, ('0x%08X' % st) if st else 'None', lens, tag))

scan(0x03)
scan(0x17)
