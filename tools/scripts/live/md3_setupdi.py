"""定位 md3 中 SetupDiGetDeviceRegistryPropertyA 的调用点，确定它请求的注册表属性索引。"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import struct

from capstone import CS_ARCH_X86, CS_MODE_32, Cs

P = sample('driver/LS8000.md3')
d = open(P, 'rb').read()
pe = struct.unpack_from('<I', d, 0x3C)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
optsz = struct.unpack_from('<H', d, pe + 20)[0]
BASE = 0x10000000
secs = []
so = pe + 24 + optsz
for i in range(nsec):
    nm = d[so + i * 40: so + i * 40 + 8].rstrip(b'\x00').decode('latin1')
    vs, va, rs, ra = struct.unpack_from('<IIII', d, so + i * 40 + 8)
    secs.append((nm, BASE + va, vs, ra, rs))


def r2o(rva):
    for nm, v, vs, ra, rs in secs:
        if v - BASE <= rva < v - BASE + max(vs, rs):
            return ra + (rva - (v - BASE))
    return None


def va2o(va):
    for nm, v, vs, ra, rs in secs:
        if v <= va < v + max(vs, rs):
            return ra + (va - v)
    return None


# 目标：IAT 槽（以 CFG 用的 base 0x20000000 记录）
IAT = {
    'SetupDiGetDeviceRegistryPropertyA': 0x200be164,
    'SetupDiEnumDeviceInfo': 0x200be168,
    'SetupDiGetClassDevsA': 0x200be16c,
    'SetupDiClassGuidsFromNameA': 0x200be170,
    'SetupDiDestroyDeviceInfoList': 0x200be174,
}
CFG_BASE = 0x20000000

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = False

for name, slot in IAT.items():
    # call dword ptr [slot]  →  FF 15 <slot LE>
    pat = b'\xFF\x15' + struct.pack('<I', slot)
    i = 0
    hits = []
    while True:
        i = d.find(pat, i)
        if i < 0:
            break
        hits.append(i)
        i += 1
    if not hits:
        print('%-34s 无直接 call [IAT] 命中' % name)
        continue
    print('=' * 76)
    print('%s   IAT 0x%08X   %d 处 call' % (name, slot, len(hits)))
    for h in hits[:4]:
        va = None
        for nm, v, vs, ra, rs in secs:
            if ra <= h < ra + rs:
                va = v + (h - ra)
        if va is None:
            continue
        # 反汇编前 40 字节看压栈参数
        start = max(va - 44, 0x10001000)
        o = va2o(start)
        print('  --- 调用点 VA 0x%08X ---' % va)
        for ins in md.disasm(d[o:o + (va - start) + 8], start):
            if ins.address > va + 6:
                break
            mark = '  <<<' if ins.address == va else ''
            print('    0x%08X  %-8s %s%s' % (ins.address, ins.mnemonic, ins.op_str, mark))
        print()
