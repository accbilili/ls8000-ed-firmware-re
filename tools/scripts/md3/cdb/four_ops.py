"""Formal hunt for the 4 '—' opcodes: TEST UNIT READY / REQUEST SENSE / RESERVE / RELEASE."""
import sys, os, struct, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

WANT = {0x00: 'TEST UNIT READY', 0x03: 'REQUEST SENSE', 0x16: 'RESERVE', 0x17: 'RELEASE'}

def ret_len(body):
    """does this function end with `mov eax, 6|10` before a ret (CDB length idiom)?"""
    got = set()
    for a in body:
        i = body[a]
        if i.mnemonic == 'mov' and len(i.operands) == 2:
            d, s = i.operands
            if d.type == X86_OP_REG and i.reg_name(d.reg) == 'eax' and s.type == X86_OP_IMM:
                if s.imm in (6, 10): got.add(s.imm)
    return got

def main():
    ins = sweep(TEXT_LO, TEXT_HI)
    # ---- Form A: byte imm store, any base, disp 0..0x40
    formA = collections.defaultdict(list)
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type != X86_OP_MEM or d.size != 1: continue
        if s.type != X86_OP_IMM: continue
        if 0 <= d.mem.disp <= 0x40 and s.imm in WANT:
            formA[s.imm].append((i.address, d.mem.base, d.mem.disp))
    # ---- Form B: packed dword
    formB = collections.defaultdict(list)
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type != X86_OP_MEM or d.size != 4 or s.type != X86_OP_IMM: continue
        for k in range(4):
            b = (s.imm >> (8*k)) & 0xFF
            if b in WANT: formB[b].append((i.address, d.mem.disp, k))
    # ---- Form C: reg-src byte store at disp 8
    formC = []
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type == X86_OP_MEM and d.size == 1 and d.mem.disp == 8 and s.type == X86_OP_REG:
            formC.append(i.address)

    import callers_helper as CH
    targets = CH.call_targets(ins)
    out = {}
    for op, name in sorted(WANT.items()):
        rows = []
        for va, base, disp in formA[op]:
            e = CH.entry_of(va, targets)
            body = cfg(e) if e else {}
            lens = ret_len(body)
            rows.append(dict(site=va, func=e, disp=disp, lens=sorted(lens)))
        valid = [r for r in rows if r['lens']]
        out[hex(op)] = dict(name=name, formA=len(rows), valid=len(valid), rows=rows,
                            formB=len(formB[op]))
        print('0x%02X %-18s FormA=%-4d valid=%-3d FormB=%-3d' % (op, name, len(rows), len(valid), len(formB[op])))
        for r in valid:
            print('      VALID site=0x%08X func=0x%08X disp=0x%X lens=%s'
                  % (r['site'], r['func'] or 0, r['disp'], r['lens']))
    print('FormC reg-src [x+8] stores:', len(formC), [hex(x) for x in formC])
    json.dump(out, open('four_ops.json', 'w'), indent=1, default=str)

if __name__ == '__main__':
    main()
