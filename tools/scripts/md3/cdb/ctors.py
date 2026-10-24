"""Resolve each vptr store to its enclosing constructor; list ctor callers."""
import sys, os, struct, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

def call_targets(ins):
    return sorted({i.operands[0].imm for i in ins
                   if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM
                   and TEXT_LO <= i.operands[0].imm < TEXT_HI})

def entry_of(va, targets):
    cands = [e for e in targets if e <= va]
    for e in reversed(cands):
        if va - e > 0x2000: break
        if va in cfg(e): return e
    return None

def main():
    ins = sweep(TEXT_LO, TEXT_HI)
    targets = call_targets(ins)
    rows = json.load(open('vt_rows.json'))
    byx = collections.defaultdict(list)
    for i in ins:
        if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM:
            byx[i.operands[0].imm].append(i.address)
    out = []
    for r in rows:
        ctor = entry_of(r['store'], targets)
        r['ctor'] = ctor
        r['ctor_callers'] = sorted(byx.get(ctor, [])) if ctor else []
        out.append(r)
        print('CDB0=0x%02X builder=0x%08X vtable=0x%08X ctor=0x%08X callers=%d %s'
              % (r['cdb0'], r['builder'], r['vtable'], ctor or 0,
                 len(r['ctor_callers']), [hex(x) for x in r['ctor_callers'][:8]]))
    json.dump(out, open('vt_rows2.json','w'), indent=1, default=str)

if __name__ == '__main__':
    main()
