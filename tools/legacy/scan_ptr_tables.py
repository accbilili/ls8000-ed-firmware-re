import sys, os, struct, collections

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\TEST\LS8000-firmware-REA-20261021-reviewed\firmware.decoded.bin"
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
data = open(SRC, "rb").read()
BASE = 0x10000
END = BASE + len(data)

lines = []
def w(s=""):
    lines.append(str(s)); print(s)

# 已覆盖区间（来自 functions.txt）
covered = []
for line in open(os.path.join(OUT, "h8", "functions.txt"), encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 3 or p[0].startswith("#"):
        continue
    try:
        a = int(p[0].split(":")[-1], 16); sz = int(p[2])
    except Exception:
        continue
    if sz > 0:
        covered.append((a, a + sz))
covered.sort()

def is_covered(a):
    for s, e in covered:
        if s <= a < e:
            return True
        if a < s:
            return False
    return False

w("=" * 78)
w("函数指针表扫描（4 字节大端值落在镜像地址区间）")
w("=" * 78)

# 收集所有"像地址"的 4 字节值
hits = {}
for i in range(0, len(data) - 4, 2):
    v = struct.unpack(">I", data[i:i + 4])[0]
    if BASE <= v < END:
        hits[i] = v

w(f"候选 4 字节对齐位置（步长2）: {len(hits)}")

# 聚成连续 run（相邻命中间隔 <= 8）
runs = []
cur = []
for off in sorted(hits):
    if not cur:
        cur = [off]
    elif off - cur[-1] <= 8:
        cur.append(off)
    else:
        runs.append(cur); cur = [off]
if cur:
    runs.append(cur)

big = [r for r in runs if len(r) >= 3]
w(f"连续成表（>=3 项）: {len(big)} 张")

w()
w("-- 主要指针表 --")
table_entries = set()
for r in sorted(big, key=lambda x: -len(x))[:25]:
    start = BASE + r[0]
    span = r[-1] - r[0] + 4
    vals = [hits[o] for o in r]
    uniq = len(set(vals))
    w(f"  @0x{start:06X}  项数={len(r):<3} 跨度={span:<5} 唯一目标={uniq:<3} 首项={hex(vals[0])}")
    for o in r:
        table_entries.add(hits[o])

w()
w(f"指针表内唯一函数目标总数: {len(table_entries)}")
new_targets = sorted(t for t in table_entries if not is_covered(t))
w(f"其中当前未被识别为函数代码的: {len(new_targets)}")
for t in new_targets[:40]:
    w(f"    0x{t:06X}")

# 与既有 JSR/JMP 种子合并
old = set()
p = os.path.join(OUT, "call_seeds.txt")
if os.path.exists(p):
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line:
            old.add(int(line, 16))
merged = sorted(old | table_entries)
w()
w(f"原种子 {len(old)} + 指针表目标 {len(table_entries)} → 合并去重 {len(merged)}")

with open(os.path.join(OUT, "call_seeds_v2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(hex(x) for x in merged))

# 覆盖热图（按 4KB）
w()
w("-- 当前覆盖率（按 4KB 块，已识别函数字节占比）--")
for blk in range(BASE, END, 4096):
    blk_end = min(blk + 4096, END)
    cov = 0
    for s, e in covered:
        lo = max(s, blk); hi = min(e, blk_end)
        if hi > lo:
            cov += hi - lo
    pct = cov / (blk_end - blk) * 100
    bar = "#" * int(pct / 5)
    w(f"  0x{blk:06X}  {pct:5.1f}%  {bar}")

with open(os.path.join(OUT, "ptr_tables.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n[saved] ptr_tables.txt / call_seeds_v2.txt")
