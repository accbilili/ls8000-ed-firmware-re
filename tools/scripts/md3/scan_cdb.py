"""Global scan for CDB-byte write patterns in .text."""
import sys, os, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md3lib import *
from oracle import D, sweep
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

SCSI = {0x00,0x01,0x03,0x04,0x07,0x08,0x0A,0x0B,0x12,0x15,0x16,0x17,0x1A,0x1B,
        0x1C,0x1D,0x1E,0x24,0x25,0x28,0x2A,0x2E,0x2F,0x35,0x3B,0x3C,
        0xC0,0xC1,0xE0,0xE1}

def is_mem(op):
    return op.type == X86_OP_MEM

def main():
    ins = sweep(TEXT_LO, TEXT_HI)
    hits = []
    for i in ins:
        if i.mnemonic != 'mov': continue
        if len(i.operands) != 2: continue
        d, s = i.operands
        if not is_mem(d): continue
        m = d.mem
        if m.index != 0: continue        # only [base+disp]
        if m.base == 0: continue
        disp = m.disp
        if disp < 0 or disp > 0x40: continue
        if s.type == X86_OP_IMM:
            v = s.imm
            if d.size == 1 and 0 <= v <= 0xFF:
                hits.append((i.address, m.base, disp, 1, v))
            elif d.size == 4:
                hits.append((i.address, m.base, disp, 4, v & 0xFFFFFFFF))
        elif s.type == X86_OP_REG:
            hits.append((i.address, m.base, disp, d.size, None))
    pickle.dump(hits, open('memwr.pkl','wb'))
    print('mem-write hits', len(hits))
    # filter: byte writes at disp<=0x14 with SCSI-ish imm
    filt = [h for h in hits if h[3]==1 and h[2] <= 0x14 and h[4] in SCSI]
    print('candidate CDB[0] byte writes (disp<=0x14, imm in SCSI set):', len(filt))
    by = collections.Counter(h[4] for h in filt)
    for k in sorted(by):
        print('  imm 0x%02X : %d' % (k, by[k]))

if __name__ == '__main__':
    main()
