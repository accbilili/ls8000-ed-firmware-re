"""Resolve function entries for anchor VAs; dump CFG + callers."""
import sys, os, pickle, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md3lib import *
from cfg import linear_sweep, descend

ANCHORS = {
 0x100A01A0:'INQUIRY 0x12', 0x1009FDB0:'MODE SELECT 0x15', 0x1009FE60:'MODE SENSE 0x1A',
 0x100A0290:'START STOP 0x1B', 0x100A0210:'SET WINDOW 0x24', 0x100A01D0:'GET WINDOW 0x25',
 0x100AAD00:'READ 0x28', 0x100AAD50:'WRITE 0x2A', 0x100AADC0:'WRITE BUFFER 0x3B',
 0x100AAD80:'READ BUFFER 0x3C', 0x100AAE10:'CANCEL 0xC0', 0x100A0190:'EXECUTE 0xC1',
 0x100A0230:'E0', 0x100A0260:'E1',
}

def main():
    ins = linear_sweep()
    starts = {i.address: i for i in ins}
    seeds = sorted({i.operands[0].imm for i in ins
                    if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM
                    and TEXT_LO <= i.operands[0].imm < TEXT_HI})
    print('seeds', len(seeds))
    # callers map: target -> [caller va]
    callers = {}
    for i in ins:
        if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM:
            t = i.operands[0].imm
            callers.setdefault(t, []).append(i.address)

    out = {}
    for a, name in sorted(ANCHORS.items()):
        cands = [s for s in seeds if s <= a]
        entry = None
        for c in reversed(cands):
            if a - c > 0x4000:      # function won't be >16KB
                # keep trying a few more
                pass
            cfg = descend(c, starts)
            if a in cfg:
                entry = c
                break
            if a - c > 0x20000:
                break
        out[a] = dict(name=name, entry=entry)
        print('0x%08X %-18s -> entry 0x%08X  callers=%d' %
              (a, name, entry or 0, len(callers.get(entry, []))))
    json.dump({('0x%08X'%k):v for k,v in out.items()},
              open('anchors.json','w'), indent=1)

if __name__ == '__main__':
    main()
