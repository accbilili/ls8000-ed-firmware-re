import math, sys, os, collections, re

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111\.rsrc\0\RCDATA\FIRMDATA"
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
data = open(SRC, "rb").read()

lines = []
def w(s=""):
    lines.append(str(s))
    print(s)

def entropy(b):
    if not b:
        return 0.0
    cnt = collections.Counter(b)
    n = len(b)
    return -sum((c / n) * math.log2(c / n) for c in cnt.values())

w("=" * 72)
w(f"FIRMDATA  size={len(data)} (0x{len(data):X})")
w("=" * 72)
w(f"整体熵: {entropy(data):.4f} bits/byte")
z = data.count(0)
f = data.count(0xFF)
w(f"0x00 占比: {z/len(data)*100:.2f}%   0xFF 占比: {f/len(data)*100:.2f}%")
w(f"唯一字节值数量: {len(set(data))}/256")

w()
w("-- 分块熵 (每 4096 字节) --")
BS = 4096
for i in range(0, len(data), BS):
    blk = data[i:i+BS]
    e = entropy(blk)
    bar = "#" * int(e * 8)
    w(f"0x{i:06X} ({i//BS:>2})  ent={e:5.3f}  {bar}")

w()
w("-- 滑窗熵 (每 1024 字节, 仅显示 <6.0 或 >7.8 的异常块) --")
WS = 1024
anom = []
for i in range(0, len(data) - WS + 1, WS):
    e = entropy(data[i:i+WS])
    if e < 6.0 or e > 7.85:
        anom.append((i, e))
if anom:
    for i, e in anom[:60]:
        w(f"0x{i:06X}  ent={e:5.3f}")
    w(f"(共 {len(anom)} 个异常块)")
else:
    w("无显著异常")

w()
w("-- 字节频率 top 12 --")
cnt = collections.Counter(data)
for b, c in cnt.most_common(12):
    w(f"  0x{b:02X}  {c:>6}  {c/len(data)*100:5.2f}%")

w()
w("-- 长零/长FF 区段 (>=64) --")
run_re = re.compile(rb"\x00{64,}|\xff{64,}")
n = 0
for m in run_re.finditer(data):
    if n > 20:
        w("  ...")
        break
    w(f"  0x{m.start():06X} len={m.end()-m.start()} byte=0x{m.group()[0]:02X}")
    n += 1
if n == 0:
    w("  无")

w()
w("-- ASCII 字符串 (>=6, 仅可打印) --")
found = re.findall(rb"[\x20-\x7e]{6,}", data)
w(f"  数量: {len(found)}")
for s in found[:40]:
    w(f"    0x{data.find(s):06X}  {s.decode('latin1')[:90]}")

w()
w("-- UTF-16LE 字符串 (>=5) --")
u16 = re.findall(rb"(?:[\x20-\x7e]\x00){5,}", data)
w(f"  数量: {len(u16)}")
for s in u16[:20]:
    w(f"    {s.decode('utf-16le')[:80]}")

w()
w("-- 头部 384 字节 --")
for i in range(0, min(384, len(data)), 16):
    chunk = data[i:i+16]
    hx = " ".join(f"{b:02x}" for b in chunk)
    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    w(f"{i:06X}  {hx:<48}  {asc}")

w()
w("-- 尾部 256 字节 --")
start = max(0, len(data) - 256)
for i in range(start, len(data), 16):
    chunk = data[i:i+16]
    hx = " ".join(f"{b:02x}" for b in chunk)
    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    w(f"{i:06X}  {hx:<48}  {asc}")

w()
w("-- 16 位字对齐自相关 (值越低越像 16 位字流) --")
def autocorr(b, isa):
    # 相邻单元异或后零字节比例 -> 结构重复度
    same = 0
    tot = 0
    for i in range(0, len(b) - isa * 2, isa):
        if b[i:i+isa] == b[i+isa:i+isa*2]:
            same += 1
        tot += 1
    return same / tot if tot else 0

for stride in (2, 4):
    # 高字节相似度：偶数位与奇数位分布差异
    hi = data[1::2] if stride == 2 else data
    lo = data[0::2] if stride == 2 else data
    w(f"  stride={stride}: 相邻重复率={autocorr(data, stride):.4f}")

even = data[0::2]
odd = data[1::2]
w(f"  偶地址熵={entropy(even):.3f}  奇地址熵={entropy(odd):.3f}  (差异大=>16位字宽架构)")

w()
w("-- 常见固件魔数扫描 --")
magics = {
    b"\x1f\x8b": "gzip", b"PK\x03\x04": "zip", b"\x89PNG": "png",
    b"BZh": "bzip2", b"\x5d\x00\x00": "lzma", b"\x28\xb5\x2f\xfd": "zstd",
    b"LZ": "lz?", b"\x00\x00\x00\x00": "zeros",
}
for m, nm in magics.items():
    p = data.find(m)
    if p >= 0:
        w(f"  {nm:<8} at 0x{p:06X}")

with open(os.path.join(OUT, "firm_probe.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print("\n[saved] firm_probe.txt")
