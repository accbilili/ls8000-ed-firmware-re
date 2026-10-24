"""F5 复核 10：独立重算 18 个 CDB 类的 vtable / 构造函数 / 上层调用者。"""
import sys, struct, collections, json
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

def rd32(va):
    b = read(va, 4)
    return struct.unpack('<I', b)[0] if len(b) == 4 else None

BUILDERS = [(0x00, 'TEST UNIT READY', 0x1009FEB0, 0x1009FEB0, 6, 0x1009FEB4),
            (0x12, 'INQUIRY', 0x100A01A0, 0x100A01A5, 6, 0x100A01BF),
            (0x15, 'MODE SELECT(6)[a]', 0x1009FDB0, 0x1009FDBE, 6, 0x1009FDB9),
            (0x15, 'MODE SELECT(6)[b]', 0x100A0070, 0x100A007E, 6, 0x100A0079),
            (0x16, 'RESERVE(6)', 0x1009FF40, 0x1009FF40, 6, 0x1009FF44),
            (0x1A, 'MODE SENSE(6)', 0x1009FE60, 0x1009FE69, 6, 0x1009FE74),
            (0x1B, 'START STOP UNIT', 0x100A0290, 0x100A0296, 6, 0x100A029A),
            (0x1D, 'SEND DIAGNOSTIC', 0x1009FF80, 0x1009FF80, 6, 0x1009FF88),
            (0x24, 'SET WINDOW', 0x100A0210, 0x100A021E, 10, 0x100A0229),
            (0x25, 'GET WINDOW', 0x100A01D0, 0x100A01E8, 10, 0x100A0205),
            (0x28, 'READ(10)', 0x100AAD00, 0x100AAD20, 10, 0x100AAD2B),
            (0x2A, 'WRITE(10)', 0x100AAD50, 0x100AAD70, 10, 0x100AAD77),
            (0x3B, 'WRITE BUFFER', 0x100AADC0, 0x100AADEC, 10, 0x100AADF3),
            (0x3C, 'READ BUFFER', 0x100AAD80, 0x100AADAC, 10, 0x100AADB3),
            (0xC0, 'CANCEL', 0x100AAE20, 0x100AAE20, 6, 0x100AAE24),
            (0xC1, 'EXECUTE', 0x100A0190, 0x100A0190, 6, 0x100A0194),
            (0xE0, 'MECHANISM CONTROL', 0x100A0230, 0x100A0244, 10, 0x100A024B),
            (0xE1, 'READ STATUS', 0x100A0260, 0x100A0274, 10, 0x100A027B)]

ins = sweep(TEXT_LO, TEXT_HI)
# 1) vtable 反查：哪个 .rdata 地址的 +0x24 是该 builder
RD = [s for s in SECS if s['name'] == '.rdata'][0]
raw = DATA[RD['roff']:RD['roff'] + RD['rsize']]
vt_of = {}
for i in range(0, len(raw) - 0x28, 4):
    v = struct.unpack_from('<I', raw, i)[0]
    for cdb0, nm, ent, site, lv, ls in BUILDERS:
        if v == ent and rd32(RD['va'] + i - 0x24) == ent:
            pass
for cdb0, nm, ent, site, lv, ls in BUILDERS:
    cands = []
    for i in range(0, len(raw) - 0x28, 4):
        if struct.unpack_from('<I', raw, i)[0] == ent:
            cands.append(RD['va'] + i - 0x24)
    vt_of[ent] = cands

# 2) 找写入该 vtable 的构造函数
vptr_w = collections.defaultdict(list)
for i in ins:
    if i.mnemonic != 'mov' or len(i.operands) != 2: continue
    d, s = i.operands
    if d.type == X86_OP_MEM and d.size == 4 and s.type == X86_OP_IMM and d.mem.disp == 0:
        vptr_w[s.imm].append(i.address)
byx = collections.defaultdict(list)
for i in ins:
    if i.mnemonic == 'call' and i.operands and i.operands[0].type == X86_OP_IMM:
        byx[i.operands[0].imm].append(i.address)

def entry_of(va, lim=0x400):
    order = sorted({x for x in _ORD})
    idx = order.index(va); j = idx; start = va
    while j > 0 and va - order[j] < lim:
        m = D(order[j - 1]).mnemonic
        if m.startswith('ret') or m in ('nop', 'int3'):
            start = order[j]; break
        j -= 1
    return start

_ORD = {i.address for i in ins}

print('%-22s %-11s %-11s %-11s %-6s %s' % ('name', 'builder', 'vtable', 'ctor', 'len', 'callers(<=5)'))
out = []
for cdb0, nm, ent, site, lv, ls in BUILDERS:
    vts = vt_of.get(ent, [])
    ctors = []
    for v in vts:
        for a in vptr_w.get(v, []):
            ctors.append(entry_of(a))
    ctors = sorted(set(ctors))
    callers = []
    for c in ctors:
        callers += byx.get(c, [])
    callers = sorted(set(callers))
    print('%-22s 0x%08X  %-11s %-11s %-6d %s' % (
        nm, ent, ('0x%08X' % vts[0]) if vts else '-',
        ('0x%08X' % ctors[0]) if ctors else '-', lv,
        ['0x%08X' % x for x in callers[:5]]))
    out.append(dict(cdb0='0x%02X' % cdb0, name=nm, builder='0x%08X' % ent,
                    site='0x%08X' % site, len=('%d@0x%08X' % (lv, ls)),
                    vtable=['0x%08X' % v for v in vts],
                    ctors=['0x%08X' % c for c in ctors],
                    callers=['0x%08X' % x for x in callers]))
json.dump(out, open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\_f5\v10.json', 'w'),
          indent=1, ensure_ascii=False)
print('\nwrote v10.json', len(out))
