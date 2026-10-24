"""Resolve vtable -> builder, find ctors (write vptr), and callers."""
import sys, os, struct, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

BUILD_OFF = 0x24   # vtable slot holding BuildCDB

def rd32(va):
    b = read(va, 4)
    return struct.unpack('<I', b)[0] if len(b) == 4 else None

def is_code(v):
    return TEXT_LO <= v < TEXT_HI

def main():
    ins = sweep(TEXT_LO, TEXT_HI)
    # 1. all vptr stores: mov dword ptr [reg+disp], imm  where imm points into .rdata
    vptr_stores = []
    for i in ins:
        if i.mnemonic != 'mov' or len(i.operands) != 2: continue
        d, s = i.operands
        if d.type != X86_OP_MEM or s.type != X86_OP_IMM: continue
        if d.size != 4: continue
        v = s.imm
        s2 = sec_of(v)
        if s2 and s2['name'] == '.rdata':
            vptr_stores.append((i.address, d.mem.base, d.mem.disp, v))
    print('vptr stores into .rdata:', len(vptr_stores))

    # 2. keep those whose vtable[0x24] is code
    cands = []
    for va, base, disp, vt in vptr_stores:
        f = rd32(vt + BUILD_OFF)
        if f and is_code(f):
            cands.append((va, vt, f))
    print('stores where vtable+0x24 is code:', len(cands))

    # 3. classify builder: does it do `mov byte ptr [reg+8], imm8`?
    def build_info(fn):
        body = cfg(fn)
        if len(body) > 80: return None
        cdb0 = None; length = None; other = []
        for a in sorted(body):
            i = body[a]
            if i.mnemonic == 'mov' and len(i.operands) == 2:
                d, s = i.operands
                if d.type == X86_OP_MEM and d.mem.base and d.mem.disp >= 8 and d.mem.disp <= 0x12:
                    if s.type == X86_OP_IMM and d.size == 1:
                        off = d.mem.disp - 8
                        if off == 0: cdb0 = (a, s.imm)
                        else: other.append((a, off, s.imm))
                    elif s.type == 0x1:  # reg
                        off = d.mem.disp - 8
                        other.append((a, off, 'reg:' + i.reg_name(s.reg)))
                if d.type == 0 and i.reg_name(d.reg) == 'eax' and s.type == X86_OP_IMM:
                    length = s.imm
        return dict(fn=fn, size=len(body), cdb0=cdb0, len=length, fields=other)

    rows = []
    for va, vt, f in cands:
        bi = build_info(f)
        if not bi or not bi['cdb0']: continue
        rows.append(dict(store=va, vtable=vt, builder=bi['fn'], size=bi['size'],
                         cdb0=bi['cdb0'][1], cdb0_site=bi['cdb0'][0],
                         cdb_len=bi['len'], fields=bi['fields']))
    rows.sort(key=lambda r: r['cdb0'])
    for r in rows:
        print('CDB0=0x%02X vt=0x%08X builder=0x%08X site=0x%08X len=%s ctorstore=0x%08X'
              % (r['cdb0'], r['vtable'], r['builder'], r['cdb0_site'], r['cdb_len'], r['store']))
    json.dump(rows, open('vt_rows.json', 'w'), indent=1, default=str)

if __name__ == '__main__':
    main()
