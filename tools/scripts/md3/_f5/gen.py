"""F5 定稿：生成 cdb_sites.json（20 行：18 落点 + 2 条未构造）。"""
import sys, json
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *

# cdb0, name, builder_entry, site, len_val, len_site, sub(CDB[2] 写入点)
ROWS = [
 (0x00, 'TEST UNIT READY',     0x1009FEB0, 0x1009FEB0, 6,  0x1009FEB4, None),
 (0x03, 'REQUEST SENSE',       None,       None,       None, None,      None),
 (0x12, 'INQUIRY',             0x100A01A0, 0x100A01A5, 6,  0x100A01BF, None),
 (0x15, 'MODE SELECT(6)',      0x1009FDB0, 0x1009FDBE, 6,  0x1009FDB9, None),
 (0x15, 'MODE SELECT(6) [b]',  0x100A0070, 0x100A007E, 6,  0x100A0079, None),
 (0x16, 'RESERVE(6)',          0x1009FF40, 0x1009FF40, 6,  0x1009FF44, None),
 (0x17, 'RELEASE(6)',          None,       None,       None, None,      None),
 (0x1A, 'MODE SENSE(6)',       0x1009FE60, 0x1009FE69, 6,  0x1009FE74, None),
 (0x1B, 'START STOP UNIT',     0x100A0290, 0x100A0296, 6,  0x100A029A, None),
 (0x1D, 'SEND DIAGNOSTIC',     0x1009FF80, 0x1009FF80, 6,  0x1009FF88, None),
 (0x24, 'SET WINDOW',          0x100A0210, 0x100A021E, 10, 0x100A0229, None),
 (0x25, 'GET WINDOW',          0x100A01D0, 0x100A01E8, 10, 0x100A0205, None),
 (0x28, 'READ(10)',            0x100AAD00, 0x100AAD20, 10, 0x100AAD2B, None),
 (0x2A, 'WRITE(10)',           0x100AAD50, 0x100AAD70, 10, 0x100AAD77, None),
 (0x3B, 'WRITE BUFFER',        0x100AADC0, 0x100AADEC, 10, 0x100AADF3, None),
 (0x3C, 'READ BUFFER',         0x100AAD80, 0x100AADAC, 10, 0x100AADB3, None),
 (0xC0, 'CANCEL',              0x100AAE20, 0x100AAE20, 6,  0x100AAE24, None),
 (0xC1, 'EXECUTE',             0x100A0190, 0x100A0190, 6,  0x100A0194, None),
 (0xE0, 'MECHANISM CONTROL',   0x100A0230, 0x100A0244, 10, 0x100A024B, 0x100A0233),
 (0xE1, 'READ STATUS',         0x100A0260, 0x100A0274, 10, 0x100A027B, 0x100A0263),
]

v10 = json.load(open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\_f5\v10.json'))
cmap = {}
for r in v10:
    cmap[(r['cdb0'], r['builder'])] = r['callers']

def fb(cdb0, ent):
    if ent is None: return []
    return cmap.get(('0x%02X' % cdb0, '0x%08X' % ent), [])

out = []
for cdb0, name, ent, site, lv, ls, sub in ROWS:
    if site is not None:
        i = D(site)
        assert i.mnemonic == 'mov' and i.operands[1].imm == cdb0, (hex(site), i.op_str)
        j = D(ls)
        assert j.mnemonic == 'mov' and j.operands[1].imm == lv, (hex(ls), j.op_str)
    callers = fb(cdb0, ent)
    out.append({'cdb0': '0x%02X' % cdb0,
                'func': ('0x%08X' % ent) if ent else None,
                'site': ('0x%08X' % site) if site else None,
                'sub': ('0x%08X' % sub) if sub else None,
                'callers': callers[:5],
                'name': name})

P = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb_sites.json'
json.dump(out, open(P, 'w'), indent=1, ensure_ascii=False)
print('wrote', P, len(out), 'rows;', sum(1 for r in out if r['site']), 'with site')
for r in out:
    print('  ', r['cdb0'], r['name'], r['func'], r['site'], r['sub'], len(r['callers']))
