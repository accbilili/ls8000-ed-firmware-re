import sys, json
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *

# (cdb0, name, builder_entry, site, len_val, len_site, vtable, ctor)
ROWS = [
 (0x00, 'TEST UNIT READY',    0x1009FEB0, 0x1009FEB0, 6,  0x1009FEB4, 0x100C28D4, 0x1009FD20),
 (0x03, 'REQUEST SENSE',      None,       None,       None,None,      None,       None),
 (0x12, 'INQUIRY',            0x100A01A0, 0x100A01A5, 6,  0x100A01BF, 0x100C299C, 0x1009FEC0),
 (0x15, 'MODE SELECT(6)',     0x1009FDB0, 0x1009FDBE, 6,  0x1009FDB9, 0x100C2924, 0x1009FD60),
 (0x15, 'MODE SELECT(6) [b]', 0x100A0070, 0x100A007E, 6,  0x100A0079, 0x100C2A64, 0x100A0020),
 (0x16, 'RESERVE(6)',         0x1009FF40, 0x1009FF40, 6,  0x1009FF44, 0x100C29C4, 0x1009FF10),
 (0x17, 'RELEASE(6)',         None,       None,       None,None,      None,       None),
 (0x1A, 'MODE SENSE(6)',      0x1009FE60, 0x1009FE69, 6,  0x1009FE74, 0x100C294C, 0x1009FDE0),
 (0x1B, 'START STOP UNIT',    0x100A0290, 0x100A0296, 6,  0x100A029A, 0x100C2ADC, 0x100A0120),
 (0x1D, 'SEND DIAGNOSTIC',    0x1009FF80, 0x1009FF80, 6,  0x1009FF88, 0x100C28FC, 0x1009FD40),
 (0x24, 'SET WINDOW',         0x100A0210, 0x100A021E, 10, 0x100A0229, 0x100C2A3C, 0x1009FFE0),
 (0x25, 'GET WINDOW',         0x100A01D0, 0x100A01E8, 10, 0x100A0205, 0x100C2A14, 0x1009FF90),
 (0x28, 'READ(10)',           0x100AAD00, 0x100AAD20, 10, 0x100AAD2B, 0x100C303C, 0x100AAB30),
 (0x2A, 'WRITE(10)',          0x100AAD50, 0x100AAD70, 10, 0x100AAD77, 0x100C3064, 0x100AABF0),
 (0x3B, 'WRITE BUFFER',       0x100AADC0, 0x100AADEC, 10, 0x100AADF3, 0x100C30B4, 0x100AAC90),
 (0x3C, 'READ BUFFER',        0x100AAD80, 0x100AADAC, 10, 0x100AADB3, 0x100C308C, 0x100AAC40),
 (0xC0, 'CANCEL',             0x100AAE20, 0x100AAE20, 6,  0x100AAE24, 0x100C30DC, 0x100AAE00),
 (0xC1, 'EXECUTE',            0x100A0190, 0x100A0190, 6,  0x100A0194, 0x100C2B04, 0x100A0160),
 (0xE0, 'MECHANISM CONTROL',  0x100A0230, 0x100A0244, 10, 0x100A024B, 0x100C2A8C, 0x100A00A0),
 (0xE1, 'READ STATUS',        0x100A0260, 0x100A0274, 10, 0x100A027B, 0x100C2AB4, 0x100A00E0),
]
cal = json.load(open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb\callers.json'))
out = []
for cdb0, name, ent, site, lval, lsite, vt, ctor in ROWS:
    if site:
        i = D(site); j = D(lsite)
        assert i.operands[1].imm == cdb0, hex(site)
        assert j.operands[1].imm == lval, hex(lsite)
    callers = []
    if ctor:
        for x in cal.get('0x%x' % ctor, []):
            callers.append('0x%08X' % x)
    out.append({'cdb0': '0x%02X' % cdb0, 'func': ('0x%08X' % ent) if ent else None,
                'site': ('0x%08X' % site) if site else None, 'sub': None,
                'callers': callers, 'name': name})
json.dump(out, open(r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb_sites.json', 'w'),
          indent=1, ensure_ascii=False)
print('rows', len(out))
for r in out:
    print(r['cdb0'], r['name'], r['func'], r['site'], len(r['callers']))
