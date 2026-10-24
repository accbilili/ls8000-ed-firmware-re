import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import sys, struct, csv, os

sys.stdout.reconfigure(encoding="utf-8")

ROM = sample('LS8000_111_ROM.bin')
XREF = sample('xrefs_data.csv')
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
d = open(ROM, "rb").read()
B = 0x10000

lines = []
def w(s=""):
    lines.append(str(s)); print(s)

def u16(a):
    return struct.unpack(">H", d[a - B:a - B + 2])[0]

def u32(a):
    return struct.unpack(">I", d[a - B:a - B + 4])[0]

def f64(a):
    return struct.unpack(">d", d[a - B:a - B + 8])[0]

# ---------- 载入 xref，建立"谁引用了该地址" ----------
xref_by_target = {}
with open(XREF, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        try:
            t = int(row["target"], 16)
        except Exception:
            continue
        xref_by_target.setdefault(t, []).append((row["insn_addr"], row["function"], row["mnemonic"]))

def refs_near(addr, span):
    """找出落在 [addr, addr+span) 内的引用"""
    hits = []
    for t, rs in xref_by_target.items():
        if addr <= t < addr + span:
            for i, fn, mn in rs:
                hits.append((t, i, fn, mn))
    return sorted(hits)

w("=" * 78)
w("未分类数据表解析（Harness 待办 2）")
w("=" * 78)

# ---------- 1. 浮点表完整边界 ----------
w()
w("## 1. 0x03EB70 双精度表（确认边界与长度）")
start = 0x3EB70
vals = []
a = start
while a < 0x3EDE0:
    v = f64(a)
    if not (1e-9 < abs(v) < 1e6):
        break
    vals.append((a, v))
    a += 8
for addr, v in vals:
    w(f"  0x{addr:06X}  {v!r}")
w(f"  → 共 {len(vals)} 个 double，表结束于 0x{a:06X}")

# ---------- 2. 16 字节记录表 ----------
w()
w("## 2. 0x03EBC0 起的 16 字节记录表")
w("   （字段2 若落在 0x010000-0x047BF8 即为代码地址/函数指针）")
rec_start = 0x3EBC0
recs = []
addr = rec_start
while addr + 16 <= 0x3EDE0:
    f1, f2, f3, f4 = u32(addr), u32(addr + 4), u32(addr + 8), u32(addr + 12)
    recs.append((addr, f1, f2, f3, f4))
    addr += 16

w()
w(f"  {'addr':<10}{'f1':>12}{'f2':>12}{'f3':>10}{'f4':>10}   f2 是代码地址?")
code_cnt = 0
for addr, f1, f2, f3, f4 in recs:
    is_code = B <= f2 < B + len(d)
    if is_code:
        code_cnt += 1
    w(f"  0x{addr:06X}  0x{f1:08X}  0x{f2:08X}  0x{f3:06X}  0x{f4:06X}   {'YES' if is_code else '-'}")
w()
w(f"  记录数 {len(recs)}，其中 f2 为代码地址的 {code_cnt} 条 ({code_cnt/len(recs)*100:.0f}%)")

# f1 拆 u16
w()
w("## 3. f1 拆成 u16 观察规律")
for addr, f1, f2, f3, f4 in recs:
    hi, lo = (f1 >> 16) & 0xFFFF, f1 & 0xFFFF
    w(f"  0x{addr:06X}  hi=0x{hi:04X}({hi:>5})  lo=0x{lo:04X}({lo:>5})  f3={f3:>6}  f4={f4:>6}")

# f3/f4 值域
w()
w("## 4. f3 / f4 值域统计")
f3s = [r[3] for r in recs]
f4s = [r[4] for r in recs]
w(f"  f3: min=0x{min(f3s):X} max=0x{max(f3s):X} 唯一值 {len(set(f3s))}")
w(f"  f4: min=0x{min(f4s):X} max=0x{max(f4s):X} 唯一值 {sorted(set(f4s))[:12]}")

# ---------- 5. 表 0x03E508 ----------
w()
w("## 5. 0x03E508 表")
w("   前 16 字节为 4 个 u32：")
for i in range(4):
    v = u32(0x3E508 + i * 4)
    w(f"     0x{0x3E508+i*4:06X}  0x{v:08X}")
w("   其后按 8 字节分组：")
for i in range(4, 10):
    a2 = 0x3E508 + i * 4
    if a2 + 8 > len(d) + B:
        break
w()
for a2 in range(0x3E518, 0x3E558, 4):
    w(f"     0x{a2:06X}  u16=0x{u16(a2):04X}  u32=0x{u32(a2):08X}")

# ---------- 6. 引用关系 ----------
w()
w("## 6. 引用关系（谁读取这些表）")
for tbl, span, name in [(0x3E508, 0x50, "0x03E508"), (0x3EB70, 0x50, "0x03EB70"),
                        (0x3EBC0, 0x220, "0x03EBC0 记录表"),
                        (0x3EDE0, 0x80, "0x03EDE0"),
                        (0x3F7CE, 0x40, "0x03F7CE"), (0x3F830, 0x50, "0x03F830")]:
    hits = refs_near(tbl, span)
    w(f"  {name}: {len(hits)} 处引用")
    for t, i, fn, mn in hits[:8]:
        w(f"     from 0x{i} in func 0x{fn}  ({mn}) → 0x{t:06X}")

with open(os.path.join(OUT, "tables_resolved.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n[saved] tables_resolved.txt")
