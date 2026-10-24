import sys, os, struct, collections

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\TEST\LS8000-firmware-REA-20261021-reviewed\firmware.decoded.bin"
A = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
data = open(SRC, "rb").read()
BASE = 0x10000
END = BASE + len(data)

# ---- 1. 函数边界，用于过滤跨函数地址差 ----
funcs = []
for line in open(os.path.join(A, "h8", "functions.txt"), encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 3 or p[0].startswith("#"):
        continue
    try:
        a = int(p[0].split(":")[-1], 16); sz = int(p[2])
    except Exception:
        continue
    funcs.append((a, a + max(sz, 1)))
funcs.sort()

def func_of(a):
    for s, e in funcs:
        if s <= a < e:
            return (s, e)
        if a < s:
            return None
    return None

# ---- 2. 从已知指令反推 首字节 -> 长度 的统计 ----
ins = []
for line in open(os.path.join(A, "h8", "disasm_all.txt"), encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 2 or not p[0].startswith("ram:"):
        continue
    try:
        a = int(p[0].split(":")[-1], 16)
    except Exception:
        continue
    ins.append(a)
ins.sort()

len_stat = collections.defaultdict(collections.Counter)
for i, a in enumerate(ins):
    off = a - BASE
    if not (0 <= off < len(data)):
        continue
    first = data[off]
    f = func_of(a)
    if not f:
        continue
    # 下一条指令地址（同一函数内才有效）
    nxt = None
    if i + 1 < len(ins) and ins[i+1] < f[1] and ins[i+1] > a:
        nxt = ins[i+1]
    else:
        # 用函数末尾推断
        nxt = f[1] if f[1] > a else None
    if nxt is None:
        continue
    ln = nxt - a
    if 2 <= ln <= 8:
        len_stat[first][ln] += 1

# 取每个首字节的众数长度
len_table = {}
for b, c in len_stat.items():
    len_table[b] = c.most_common(1)[0][0]

print(f"从 {len(ins)} 条已知指令推导出 {len(len_table)}/256 个首字节的长度")
known = sum(sum(c.values()) for c in len_stat.values())
print(f"参与统计的样本: {known}")

# ---- 3. 线性扫描找连贯代码区（每 2 字节起点，连续合法即视为代码）----
UNKNOWN_LEN = 2  # 未知首字节按 2 字节推进

def scan_from(start_off, min_run=40):
    off = start_off
    run_start = off
    count = 0
    while off < len(data) - 1:
        b = data[off]
        if b not in len_table:
            break
        ln = len_table[b]
        if off + ln > len(data):
            break
        off += ln
        count += 1
        if count >= 4000:
            break
    return count, off - run_start

# 以 0x200 为网格，尝试每个网格内的偶数偏移，找最长连贯段
print()
print("线性扫描：按 2KB 网格寻找最长合法指令串")
grid = 2048
best_segments = []
for g in range(0, len(data) - 64, grid):
    best = (0, 0, 0)  # count, off, length
    for delta in range(0, 64, 2):
        so = g + delta
        if so >= len(data) - 32:
            break
        cnt, ln = scan_from(so, 20)
        if cnt > best[0]:
            best = (cnt, so, ln)
    if best[0] >= 30:
        best_segments.append((g, best[1], best[2], best[0]))

# 合并相邻
merged = []
for g, so, ln, cnt in best_segments:
    if merged and so <= merged[-1][1]:
        merged[-1] = (merged[-1][0], max(merged[-1][1], so + ln), merged[-1][2], merged[-1][3] + cnt)
    elif merged and so - merged[-1][1] <= grid * 2:
        merged[-1] = (merged[-1][0], max(merged[-1][1], so + ln), merged[-1][2], merged[-1][3] + cnt)
    else:
        merged.append((so, so + ln, ln, cnt))

print()
print(f"发现 {len(merged)} 个连贯代码段")
total_code = 0
out_lines = []
for s, e, ln, cnt in merged:
    if e - s < 256:
        continue
    total_code += (e - s)
    out_lines.append(f"{BASE+s:#08x} - {BASE+e:#08x}  {(e-s):>6} 字节  {cnt} 条指令")

for l in out_lines:
    print("  " + l)

print()
print(f"连贯代码段总字节: {total_code}")
print(f"占镜像: {total_code/len(data)*100:.1f}%")

# ---- 4. 已反汇编覆盖 vs 扫描出的代码区 ----
covered = sum(e - s for s, e in funcs)
print(f"已识别函数字节: {covered}")
print(f"扫描代码段 / 已识别 = {covered/total_code*100:.1f}%")

with open(os.path.join(A, "code_regions.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
    f.write(f"\n\ntotal_code_bytes={total_code}\ncovered={covered}\n")
print("\n[saved] code_regions.txt")
