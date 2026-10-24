"""F5 复核 2：逐个 dump 声称的 CDB 构造函数（entry..ret），验证 CDB[0] 与长度常量。"""
import sys, os, json
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *

FN = [
 (0x00, 'TEST UNIT READY',   0x1009FEB0, 0x1009FEB0),
 (0x12, 'INQUIRY',           0x100A01A0, 0x100A01A5),
 (0x15, 'MODE SELECT(6) a',  0x1009FDB0, 0x1009FDBE),
 (0x15, 'MODE SELECT(6) b',  0x100A0070, 0x100A007E),
 (0x16, 'RESERVE(6)',        0x1009FF40, 0x1009FF40),
 (0x1A, 'MODE SENSE(6)',     0x1009FE60, 0x1009FE69),
 (0x1B, 'START STOP UNIT',   0x100A0290, 0x100A0296),
 (0x1D, 'SEND DIAGNOSTIC',   0x1009FF80, 0x1009FF80),
 (0x24, 'SET WINDOW',        0x100A0210, 0x100A021E),
 (0x25, 'GET WINDOW',        0x100A01D0, 0x100A01E8),
 (0x28, 'READ(10)',          0x100AAD00, 0x100AAD20),
 (0x2A, 'WRITE(10)',         0x100AAD50, 0x100AAD70),
 (0x3B, 'WRITE BUFFER',      0x100AADC0, 0x100AADEC),
 (0x3C, 'READ BUFFER',       0x100AAD80, 0x100AADAC),
 (0xC0, 'CANCEL',            0x100AAE20, 0x100AAE20),
 (0xC1, 'EXECUTE',           0x100A0190, 0x100A0190),
 (0xE0, 'MECHANISM CONTROL', 0x100A0230, 0x100A0244),
 (0xE1, 'READ STATUS',       0x100A0260, 0x100A0274),
]

def dump(entry, site, maxn=90):
    a = entry; n = 0
    while n < maxn:
        i = D(a)
        if i is None:
            print('   0x%08X  ??' % a); return n
        mark = ' <<<' if a == site else ''
        print('   0x%08X  %-9s %s%s' % (a, i.mnemonic, i.op_str, mark))
        a += i.size; n += 1
        if i.mnemonic.startswith('ret'): break
    return n

for cdb0, name, ent, site in FN:
    print('\n===== 0x%02X %s  entry=0x%08X site=0x%08X' % (cdb0, name, ent, site))
    dump(ent, site)
