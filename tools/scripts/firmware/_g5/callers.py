import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()

# H8/300H: JSR d:24 = 0x5E + 3 字节；BSR d:16 = 0x5C + 2 字节
targets = [
    ('0x011900  READ暂存拷贝', bytes([0x01, 0x19, 0x00])),
    ('0x013d98  暂存拷贝主体', bytes([0x01, 0x3d, 0x98])),
    ('0x013872  拷到0x8DC000', bytes([0x01, 0x38, 0x72])),
    ('0x013EA0  地址分派版', bytes([0x01, 0x3e, 0xa0])),
    ('0x012bc4  拷贝例程', bytes([0x01, 0x2b, 0xc4])),
]

for name, tgt in targets:
    jsr, bsr = [], []
    i = 0
    while True:
        i = d.find(tgt, i)
        if i < 0:
            break
        if i >= 1 and d[i - 1] == 0x5E:
            jsr.append(i - 1 + 0x10000)
        if i >= 1 and d[i - 1] == 0x5C:
            bsr.append(i - 1 + 0x10000)
        i += 1
    print('%-22s jsr %2d 处 %s' % (name, len(jsr), ['0x%06X' % x for x in jsr[:14]]))
    if bsr:
        print('%-22s bsr %2d 处 %s' % ('', len(bsr), ['0x%06X' % x for x in bsr[:14]]))

print()
print('=== READ BUFFER handler 里那次调用的上下文 ===')
print('  0x026894  mov.w r5, r1        ; r1 = 被白名单裁剪后的长度')
print('  0x026896  mov.l er6, er0       ; er0 = 白名单校验通过的 offset')
print('  0x026898  jsr 0x011900         ; → 0x013d98 → 0x013872 → 拷到 0x008DC000')
print('  0x02689C  jmp 0x026940         ; 返回')
print()
print('=== 长度上限 ===')
print('  0x011906  mov.w r1, r4  →  长度按 16 位取，单次上限 65535 B')
print('  0x02687A  白名单 end 高 16 位做上界裁剪 → 不可能读到名单外')
