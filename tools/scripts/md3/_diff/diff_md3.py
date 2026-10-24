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

A = open(sample('driver/LS8000.md3'), 'rb').read()
B = open(r'C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\LS8000.md3', 'rb').read()
print('原版 %d B / 补丁版 %d B' % (len(A), len(B)))
assert len(A) == len(B)


def sections(d):
    pe = struct.unpack_from('<I', d, 0x3C)[0]
    n = struct.unpack_from('<H', d, pe + 6)[0]
    opt = struct.unpack_from('<H', d, pe + 20)[0]
    base = struct.unpack_from('<I', d, pe + 24 + 28)[0]
    out = []
    so = pe + 24 + opt
    for i in range(n):
        nm = d[so + i * 40: so + i * 40 + 8].rstrip(b'\x00').decode('latin1')
        vs, va, rs, ra = struct.unpack_from('<IIII', d, so + i * 40 + 8)
        out.append((nm, va, vs, ra, rs))
    return base, out


base, secs = sections(B)
print('ImageBase 0x%08X' % base)
for nm, va, vs, ra, rs in secs:
    print('  %-8s VA 0x%08X  VSz 0x%06X  RAW 0x%06X  RSz 0x%06X' % (nm, base + va, vs, ra, rs))


def off2va(o):
    for nm, va, vs, ra, rs in secs:
        if ra <= o < ra + rs:
            return base + va + (o - ra)
    return None


diffs = [i for i in range(len(A)) if A[i] != B[i]]
print()
print('差异字节: %d / %d (%.4f%%)' % (len(diffs), len(A), 100.0 * len(diffs) / len(A)))

regs = []
for i in diffs:
    if regs and i - regs[-1][1] <= 64:
        regs[-1][1] = i
    else:
        regs.append([i, i])
print('差异区块: %d' % len(regs))
print()
print('%-4s %-12s %-12s %-7s %s' % ('#', '文件偏移', 'VA', '字节数', '节'))
for k, (s, e) in enumerate(regs[:60]):
    va = off2va(s) or 0
    sec = [nm for nm, v, vs, ra, rs in secs if ra <= s < ra + rs]
    print('%-4d 0x%08X   0x%08X   %-7d %s' % (k + 1, s, va, e - s + 1, sec[0] if sec else '?'))

print()
print('=== 每块前后字节对比（原版 → 补丁版）===')
for k, (s, e) in enumerate(regs[:14]):
    lo = max(0, s - 6)
    hi = min(len(A), e + 7)
    print('块%02d @文件 0x%08X  VA 0x%08X  (%d B)' % (k + 1, s, off2va(s) or 0, e - s + 1))
    print('   原版: ' + ' '.join('%02X' % x for x in A[lo:hi]))
    print('   补丁: ' + ' '.join('%02X' % x for x in B[lo:hi]))
