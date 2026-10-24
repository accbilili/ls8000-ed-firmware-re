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

# H8/300H: 5E = JSR @aa:16, 5A = JMP @aa:16(:24)
jsr_targets = collections.Counter()
jmp_targets = collections.Counter()
jsr_sites = collections.defaultdict(list)
jmp_sites = collections.defaultdict(list)

for i in range(len(data) - 3):
    b = data[i]
    if b == 0x5E or b == 0x5A:
        tgt = struct.unpack(">H", data[i+1:i+3])[0]
        if BASE <= tgt < END:
            addr = BASE + i
            if b == 0x5E:
                jsr_targets[tgt] += 1
                jsr_sites[tgt].append(addr)
            else:
                jmp_targets[tgt] += 1
                jmp_sites[tgt].append(addr)

w("=" * 78)
w("H8 调用/跳转目标扫描（5E=JSR @aa:16, 5A=JMP @aa:16）")
w("=" * 78)
w(f"5E 命中（目标在镜像内）: {sum(jsr_targets.values())} 次，唯一目标 {len(jsr_targets)}")
w(f"5A 命中（目标在镜像内）: {sum(jmp_targets.values())} 次，唯一目标 {len(jmp_targets)}")

w()
w("-- JSR 目标 top 40（最可能是公共函数）--")
for t, c in jsr_targets.most_common(40):
    w(f"  0x{t:06X}  x{c:<4} sites: {[hex(s) for s in jsr_sites[t][:3]]}")

w()
w("-- JMP 目标 top 25 --")
for t, c in jmp_targets.most_common(25):
    w(f"  0x{t:06X}  x{c:<4} sites: {[hex(s) for s in jmp_sites[t][:3]]}")

w()
w("-- 目标区间分布（按 4KB 桶）--")
buckets = collections.Counter((t >> 12) << 12 for t in list(jsr_targets) + list(jmp_targets))
for k in sorted(buckets):
    w(f"  0x{k:06X}-0x{k+0xFFF:06X}  {buckets[k]:>4} 个不同目标")

# 输出种子清单供 Ghidra 使用
seeds = sorted(set(list(jsr_targets) + list(jmp_targets)))
with open(os.path.join(OUT, "call_seeds.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(hex(s) for s in seeds))
w()
w(f"已导出 {len(seeds)} 个候选函数入口 -> call_seeds.txt")

with open(os.path.join(OUT, "call_scan.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# 分析 0x3EAD8 附近的字符串指针表
w()
w("=" * 78)
w("字符串指针表分析（0x3EAD8 起）")
w("=" * 78)
start_off = 0x3EAD8 - BASE
w("偏移  地址        值(大端4B)   指向字符串")
for n in range(26):
    off = start_off + n * 4
    if off + 4 > len(data):
        break
    v = struct.unpack(">I", data[off:off+4])[0]
    s = ""
    if BASE <= v < END:
        so = v - BASE
        raw = data[so:so+40]
        s = raw.split(b"\x00")[0].decode("latin1", "replace")
    w(f"{off:06X}  0x{BASE+off:06X}  0x{v:08X}  {s}")
