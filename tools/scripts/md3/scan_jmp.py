"""Linear scan for jmp/call dword ptr [reg*4+disp32] (FF 24 85/8D/95/9D/A5/AD/B5/BD)."""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from pe_md3 import PE

p = PE()
T = p.sections[0]
data = p.data
start_off = T['rawptr']
end_off = T['rawptr'] + T['vsize']
blob = data[start_off:end_off]
mods = {0x85: 'eax', 0x8d: 'ecx', 0x95: 'edx', 0x9d: 'ebx',
        0xa5: 'esp', 0xad: 'ebp', 0xb5: 'esi', 0xbd: 'edi'}
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.syntax = CS_OPT_SYNTAX_INTEL
hits = []
for i in range(len(blob) - 6):
    if blob[i] == 0xFF and blob[i + 1] == 0x24 and blob[i + 2] in mods:
        va = T['va'] + i
        disp = struct.unpack_from('<i', blob, i + 3)[0] & 0xFFFFFFFF
        hits.append((va, mods[blob[i + 2]], disp))
print('candidate sites:', len(hits))
# verify by decoding exactly at site
ok = []
for va, reg, disp in hits:
    one = next(md.disasm(p.read(va, 8), va, 1), None)
    if one and one.mnemonic == 'jmp' and one.size == 7:
        ok.append((va, reg, disp, one.op_str))
print('decoded as 7-byte jmp:', len(ok))
with open('jmp_scan.txt', 'w', encoding='utf-8') as fh:
    for va, reg, disp, ops in ok:
        sec = p.sec_of(disp)
        fh.write('0x%08X idx=%s table=0x%08X sectab=%s %s\n' %
                 (va, reg, disp, sec['name'] if sec else '-', ops))
