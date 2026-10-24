import sys, os, math, collections, struct

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111\.rsrc\0\RCDATA\FIRMDATA"
data = open(SRC, "rb").read()
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
lines = []
def w(s=""):
    lines.append(str(s)); print(s)

def ent(b):
    if not b: return 0.0
    c = collections.Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

w("=" * 78)
w("字长与周期性分析")
w("=" * 78)

for width, label in ((2, "16-bit"), (4, "32-bit")):
    if width == 2:
        hi = data[1::2]; lo = data[0::2]
    else:
        hi = data[3::4]; lo = data[0::4]
    w(f"{label}: 高字节熵={ent(hi):.3f}  低字节熵={ent(lo):.3f}  差={abs(ent(hi)-ent(lo)):.3f}")

w()
w("-- 每隔 N 字节取样的熵（检测块结构）--")
for stride in (256, 512, 1024, 2048, 4096, 8192):
    vals = [ent(data[i:i+stride]) for i in range(0, len(data)-stride, stride)]
    w(f"  stride={stride:>5}  n={len(vals):>3}  min={min(vals):.3f} max={max(vals):.3f} 均值={sum(vals)/len(vals):.3f}")

w()
w("-- 16 位字模式：高字节直方图 top 16 --")
hi = data[1::2]
c = collections.Counter(hi)
for b, n in c.most_common(16):
    w(f"  0x{b:02X}  {n:>5}  {n/len(hi)*100:5.2f}%")

w()
w("-- 尾部规律区边界探测（从末尾向前，统计 xx9F/xxAF/xxBF 型 2 字节项）--")
# 检查 pattern: 低字节任意, 高字节 in {9F,AF,BF}
def tail_pattern_ratio(off, span=512):
    seg = data[off:off+span]
    if len(seg) < 4: return 0
    hits = 0; tot = 0
    for i in range(0, len(seg)-1, 2):
        tot += 1
        if seg[i+1] in (0x9F, 0xAF, 0xBF, 0x8F, 0xFF):
            hits += 1
    return hits/tot if tot else 0

step = 256
rows = []
for off in range(0, len(data)-512, step):
    r = tail_pattern_ratio(off)
    rows.append((off, r))
high = [(o, r) for o, r in rows if r > 0.5]
if high:
    w(f"  高命中区（>50%）共 {len(high)} 个 256 字节窗口：")
    # 合并连续区间
    runs = []
    cur = [high[0][0], high[0][0]]
    for o, r in high[1:]:
        if o - cur[1] <= step:
            cur[1] = o
        else:
            runs.append(tuple(cur)); cur = [o, o]
    runs.append(tuple(cur))
    for a, b in runs:
        w(f"    0x{a:06X} - 0x{b+256:06X}  ({(b+256-a)} 字节)")
else:
    w("  未发现连续高命中区")

w()
w("-- 末尾 1024 字节按 2 字节分组（大端/小端对照，前 48 项）--")
tail = data[-1024:]
w("  BE 解释:")
w("   " + " ".join(f"{tail[i]:02X}{tail[i+1]:02X}" for i in range(0, 96, 2)))
w("  LE 解释:")
w("   " + " ".join(f"{tail[i+1]:02X}{tail[i]:02X}" for i in range(0, 96, 2)))

w()
w("-- 重复 2 字节序列统计（前 12）--")
c2 = collections.Counter()
for i in range(0, len(data)-1):
    c2[data[i:i+2]] += 1
for k, n in c2.most_common(12):
    w(f"  {k.hex()}  x{n}")

w()
w("-- 疑似地址表检测：查找大端 16 位值落在 0x8000-0xFFFF 且单调的比例 --")
mono = 0; tot = 0
prev = None
for i in range(len(data)-2*(len(data)//2), 0):
    pass
# 简化：对尾部 4KB 做单调性检查
seg = data[-4096:]
vals_be = [struct.unpack(">H", seg[i:i+2])[0] for i in range(0, len(seg)-1, 2)]
inc = sum(1 for i in range(1, len(vals_be)) if vals_be[i] > vals_be[i-1])
w(f"  尾部 4KB 大端 16 位值递增比例: {inc/len(vals_be)*100:.1f}%")
vals_le = [struct.unpack("<H", seg[i:i+2])[0] for i in range(0, len(seg)-1, 2)]
inc2 = sum(1 for i in range(1, len(vals_le)) if vals_le[i] > vals_le[i-1])
w(f"  尾部 4KB 小端 16 位值递增比例: {inc2/len(vals_le)*100:.1f}%")

with open(os.path.join(OUT, "firm_struct.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n[saved] firm_struct.txt")
