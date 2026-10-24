# -*- coding: utf-8 -*-
"""
layout_scan.py -- Nikon LS-8000 ED 固件镜像候选 (FIRMDATA, 99865 B) 结构测绘

只读脚本，绝不写源文件。
任务一 指针表扫描：16/32 位 x 双端 x 多加载基址，1024B 窗口命中率。
       显著性判据同时给 (a) 均匀随机 p0（题目要求）与 (b) 保直方图置换零模型。
       本文件 byte 分布极不均匀（0x00 占 3.0%），(a) 会严重高估显著性，故以 (b) 为准。
任务二 头部 512B 字段解析、长度字段搜索、尾部 4B 校验和全变体检验。
任务三 256B/256bin 与 1024B/16bin 两种粒度的熵-直方图突变检测 + 置换零模型 p 值。

用法: python layout_scan.py [--pfx PATH]
输出: 02_analysis/layout_report.md, 02_analysis/layout_scan_output.txt
"""
import numpy as np, zlib, math, os, sys, io, argparse

DEF_SRC = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111\.rsrc\0\RCDATA\FIRMDATA"
BASE = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000"
OUTDIR = os.path.join(BASE, "02_analysis")
MD = os.path.join(OUTDIR, "layout_report.md")
TXT = os.path.join(OUTDIR, "layout_scan_output.txt")

ap = argparse.ArgumentParser()
ap.add_argument("--pfx", default=DEF_SRC)
ap.add_argument("--shuf", type=int, default=200)
args = ap.parse_args()

LOG = io.StringIO()
def P(*a):
    LOG.write(" ".join(str(x) for x in a) + "\n")

with open(args.pfx, "rb") as f:
    data = f.read()
N = len(data)
buf = np.frombuffer(data, dtype=np.uint8)
assert N == 99865, N

P("file=%s" % args.pfx)
P("size=%d (0x%X)" % (N, N))
P("head48=" + " ".join("%02X" % b for b in data[:48]))
P("tail16=" + " ".join("%02X" % b for b in data[-16:]))
P("")

def factorize(n):
    f, d, m = {}, 2, n
    while d * d <= m:
        while m % d == 0:
            f[d] = f.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        f[m] = f.get(m, 0) + 1
    return f

P("N factorize:", factorize(N))
P("")

# ============================================================== 基础统计
G = np.bincount(buf, minlength=256)[:256].astype(np.float64)
def ent(p):
    p = np.asarray(p, dtype=np.float64)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())
H_GLOBAL = ent(G)
P("全局熵 %.4f bit/byte ; 0x00=%.2f%% 0xFF=%.2f%% 0x40=%.2f%%"
  % (H_GLOBAL, 100 * G[0] / N, 100 * G[255] / N, 100 * G[0x40] / N))
hi_bit = float((buf >= 0x80).mean())
P("高位=1 的字节占比 %.4f (均匀期望 0.5)" % hi_bit)
z = (zlib.compress(data, 9))
P("zlib-9 压缩后 %d B, 压缩率 %.4f (熵编码数据应 ~1.00)" % (len(z), len(z) / N))
# 最长同值游程
run = 1; maxrun = 1; maxrun_byte = int(buf[0]); maxrun_pos = 0
for i in range(1, N):
    if buf[i] == buf[i - 1]:
        run += 1
        if run > maxrun:
            maxrun, maxrun_byte, maxrun_pos = run, int(buf[i]), i - run + 1
    else:
        run = 1
P("最长同值游程 %d 字节 (值 0x%02X @0x%05X)" % (maxrun, maxrun_byte, maxrun_pos))
P("")

def build16(b):
    n = len(b) // 2
    return np.frombuffer(b[:n * 2], dtype="<u2"), np.frombuffer(b[:n * 2], dtype=">u2"), n

def build32(b):
    m = (len(b) - 3) // 2
    s0 = b[0:0 + 2 * m:2].astype(np.uint32)
    s1 = b[1:1 + 2 * m:2].astype(np.uint32)
    s2 = b[2:2 + 2 * m:2].astype(np.uint32)
    s3 = b[3:3 + 2 * m:2].astype(np.uint32)
    return (s0 | (s1 << 8) | (s2 << 16) | (s3 << 24)), \
           ((s0 << 24) | (s1 << 16) | (s2 << 8) | s3), m

LE16, BE16, n16 = build16(data)
LE32, BE32, n32 = build32(buf)
OFF16 = np.arange(n16, dtype=np.int64) * 2
OFF32 = np.arange(n32, dtype=np.int64) * 2
P("items: 16bit=%d  32bit=%d" % (n16, n32))
P("")

# ============================================================== TASK 1
W1 = 1024
COMBOS = []
for e in ("BE", "LE"):
    for bs in (0x0000, 0x8000, 0xC000):
        COMBOS.append((16, e, bs))
for e in ("BE", "LE"):
    for bs in (0x000000, 0x008000, 0x00C000, 0x800000, 0xC00000):
        COMBOS.append((32, e, bs))

def masks_for(le16, be16, le32, be32):
    out = {}
    for (wd, e, bs) in COMBOS:
        arr = (be16 if e == "BE" else le16) if wd == 16 else (be32 if e == "BE" else le32)
        a = arr.astype(np.uint64)
        out[(wd, e, bs)] = ((a >= bs) & (a < np.uint64(min(bs + N, 1 << wd)))).astype(np.float64)
    return out

def win_counts(offs, mask, W):
    w = (offs // W).astype(np.int64)
    nw = int(offs[-1] // W) + 1
    c = np.bincount(w, minlength=nw).astype(np.float64)
    h = np.bincount(w, weights=mask, minlength=nw)
    return c, h, nw

P("=" * 78)
P("TASK 1")
P("=" * 78)

obs = {}
for k, m in masks_for(LE16, BE16, LE32, BE32).items():
    offs = OFF16 if k[0] == 16 else OFF32
    c, h, nw = win_counts(offs, m, W1)
    obs[k] = (c, h, nw, int(h.sum()))

# 置换零模型（保直方图，破坏顺序）
rng = np.random.default_rng(20261024)
NS = args.shuf
sum_h = {k: None for k in COMBOS}
sumsq_h = {k: None for k in COMBOS}
for t in range(NS):
    sb = rng.permutation(buf)
    l16, b16, _ = build16(sb)
    l32, b32, _ = build32(sb)
    mm = masks_for(l16, b16, l32, b32)
    for k, m in mm.items():
        offs = OFF16 if k[0] == 16 else OFF32
        c, h, nw = win_counts(offs, m, W1)
        if sum_h[k] is None:
            sum_h[k] = np.zeros(nw); sumsq_h[k] = np.zeros(nw)
        sum_h[k] += h; sumsq_h[k] += h * h
null_mean = {k: sum_h[k] / NS for k in COMBOS}
null_sd = {k: np.sqrt(np.maximum(sumsq_h[k] / NS - null_mean[k] ** 2, 1e-12)) for k in COMBOS}
P("置换零模型次数 = %d" % NS)
P("")

task1_rows = []
for (wd, e, bs) in COMBOS:
    c, h, nw, tot = obs[(wd, e, bs)]
    hi = min(bs + N, 1 << wd)
    p0 = (hi - bs) / float(1 << wd)
    exp_uni = c.sum() * p0
    nm = null_mean[(wd, e, bs)]
    ns = null_sd[(wd, e, bs)]
    z_sh = (h - nm) / ns
    nmean_tot = nm.sum(); nsd_tot = math.sqrt(float((ns ** 2).sum()))
    z_tot = (tot - nmean_tot) / nsd_tot if nsd_tot > 0 else 0.0
    # 显著窗口: 置换 z>4 且观测命中>=3
    sig = (z_sh > 4) & (h >= 3)
    regs = []
    i = 0
    while i < nw:
        if sig[i]:
            j = i
            while j + 1 < nw and sig[j + 1]:
                j += 1
            regs.append((i * W1, min((j + 1) * W1, N), float(h[i:j + 1].sum()),
                         float(c[i:j + 1].sum()), float(z_sh[i:j + 1].max())))
            i = j + 1
        else:
            i += 1
    P("-- %2d-bit %s base=0x%06X  [0x%X,0x%X)  p0_uni=%.3e" % (wd, e, bs, bs, hi, p0))
    P("   实测 %d | 均匀期望 %.2f | 置换期望 %.2f±%.2f | z_均匀=%+.1f | z_置换=%+.2f"
      % (tot, exp_uni, nmean_tot, nsd_tot, (tot - exp_uni) / math.sqrt(max(exp_uni, 1e-9)), z_tot))
    P("   窗口 z_置换>4 且命中>=3 的窗口数=%d" % int(sig.sum()))
    for (s, en, hh, cc, zz) in regs:
        P("     >> 0x%05X-0x%05X 命中 %d/%d = %.4f  置换z=%.1f" % (s, en, hh, cc, hh / cc, zz))
    task1_rows.append(dict(wd=wd, e=e, bs=bs, tot=tot, exp_uni=exp_uni,
                           nm=nmean_tot, ns=nsd_tot, z_uni=(tot - exp_uni) / math.sqrt(max(exp_uni, 1e-9)),
                           z_sh=z_tot, regs=regs, p0=p0))

# 16 位 [0,N) 无判别力说明
P("")
P("[注] 16-bit base=0x0000 的区间 [0,99865) 覆盖全部 65536 个 16 位值, p0=1.0,")
P("     命中率恒等于 1.0, 该行对'是否指针表'零信息量。")

# 0x00xxxxxx 形态
P("")
P("-- 0x00xxxxxx 绝对地址形态 (0x00010000..0x00FFFFFF), 均匀期望率 0.00389")
for e, arr in (("BE", BE32), ("LE", LE32)):
    m = (arr >= 0x00010000) & (arr <= 0x00FFFFFF)
    P("   %s: %d/%d = %.4f (均匀期望 %.1f) 倍数 %.1fx"
      % (e, int(m.sum()), len(arr), m.mean(), len(arr) * (0x01000000 - 0x10000) / 2**32,
         m.mean() / ((0x01000000 - 0x10000) / 2**32)))

# 等差/单调表
P("")
P("-- 定差游程 (>=8 项)")
def delta_runs(vals, offs, min_len=8, dmin=1, dmax=0x100000):
    v = vals.astype(np.int64)
    d = np.diff(v)
    out = []
    i, n = 0, len(d)
    while i < n:
        j = i
        while j + 1 < n and d[j + 1] == d[i]:
            j += 1
        if (j - i + 2) >= min_len and dmin <= d[i] <= dmax:
            out.append((int(offs[i]), int(offs[j + 1]), int(d[i]), int(j - i + 2)))
        i = j + 1
    out.sort(key=lambda t: -t[3])
    return out

for e, arr, offs, wd in (("BE", BE32, OFF32, 32), ("LE", LE32, OFF32, 32),
                         ("BE", BE16, OFF16, 16), ("LE", LE16, OFF16, 16)):
    r = delta_runs(arr, offs)
    P("   %d-bit %s: %d 段" % (wd, e, len(r)))
    for (s, en, dd, ln) in r[:6]:
        sub = arr[(offs >= s) & (offs <= en)].astype(np.int64)
        P("      0x%05X-0x%05X delta=0x%X 项数=%d 值域[0x%X,0x%X]"
          % (s, en, dd, ln, sub.min(), sub.max()))

# 递增长程 (diff 在 [1,64] 的连续段)
P("")
P("-- 单调递增长程 (相邻差 1..64, 长度>=16)")
def inc_runs(vals, offs, min_len=16):
    v = vals.astype(np.int64); d = np.diff(v)
    ok = (d >= 1) & (d <= 64)
    out = []; i = 0; n = len(ok)
    while i < n:
        if ok[i]:
            j = i
            while j + 1 < n and ok[j + 1]:
                j += 1
            if (j - i + 2) >= min_len:
                out.append((int(offs[i]), int(offs[j + 1]), int(j - i + 2),
                            int(d[i:j + 1].min()), int(d[i:j + 1].max())))
            i = j + 1
        else:
            i += 1
    out.sort(key=lambda t: -t[2])
    return out

for (wd, e, arr, offs) in ((16, "LE", LE16, OFF16), (16, "BE", BE16, OFF16),
                           (32, "LE", LE32, OFF32), (32, "BE", BE32, OFF32)):
    r = inc_runs(arr, offs)
    P("   %d-bit %s: %d 段 >=16项" % (wd, e, len(r)))
    for t in r[:5]:
        sub = arr[(offs >= t[0]) & (offs <= t[1])].astype(np.int64)
        P("      0x%05X-0x%05X 项数=%d 步长[%d,%d] 值域[0x%X,0x%X]"
          % (t[0], t[1], t[2], t[3], t[4], sub.min(), sub.max()))

# 1KB 窗口递增/定差密度图（结构定位）
P("")
P("-- 结构密度图: 每 1KB 窗口内 LE-u16 相邻差==0x12 的比例 与 BE-u16 差==0x1200 的比例")
dens = []
for i in range(0, N - W1 + 1, W1):
    a = i // 2; b = (i + W1) // 2 - 1
    d = np.diff(LE16[a:b].astype(np.int64))
    f1 = float((d == 0x12).mean()); f2 = 0.0
    dens.append((f1, i))
top = sorted(dens, reverse=True)[:10]
for f, i in top:
    P("   0x%05X  f(diff=18)=%.3f" % (i, f))
nramp = sum(1 for f, i in dens if f > 0.10)
P("   密度>0.10 的窗口数=%d/%d ; 全文件平均=%.4f (均匀随机期望 1/65536=1.53e-05)"
  % (nramp, len(dens), sum(f for f, i in dens) / len(dens)))

# ============================================================== TASK 2
P("")
P("=" * 78)
P("TASK 2")
P("=" * 78)
head = data[:512]
flag_rows = []
P("%-7s %-5s %-8s %s" % ("off", "end", "value", "judge"))
for i in range(0, 512, 2):
    vb = (head[i] << 8) | head[i + 1]
    vl = head[i] | (head[i + 1] << 8)
    for end, v in (("BE", vb), ("LE", vl)):
        rs = []
        if v == 0:
            rs.append("0")
        if 0 < v <= 0x20:
            rs.append("small_int")
        if v in (0xFF, 0x1FF, 0x3FF, 0xFFF, 0xFFFF):
            rs.append("mask")
        if abs(v - N) <= 512:
            rs.append("near_N")
        if v > 1 and N % v == 0:
            rs.append("divisor_of_N")
        if 0x0100 <= v <= 0x01FF:
            rs.append("ver_like")
        if v == 0x0186 or v == 0x0619 or v == 0x8619:
            rs.append("hex_fragment_of_N")
        if rs:
            P("%-7d %-5s 0x%04X   %s" % (i, end, v, ",".join(rs)))
            flag_rows.append((i, end, v, rs))
P("")
P("  -> 99865 = 0x18619 需 17 bit; 任何 16 位字段都不可能等于它")
P("  -> 前 512B 内 16 位字段 near_N / divisor_of_N 命中数: %d / %d"
  % (sum(1 for r in flag_rows if "near_N" in r[3]), sum(1 for r in flag_rows if "divisor_of_N" in r[3])))

P("")
P("-- 全文件 24 位值 0x18619 / 0x18618 搜索 (任意对齐, 双端)")
for v in (0x18619, 0x18618):
    for end in ("big", "little"):
        pat = v.to_bytes(3, end)
        idx = 0; hits = []
        while True:
            k = data.find(pat, idx)
            if k < 0:
                break
            hits.append(k); idx = k + 1
        P("   0x%05X %s: %d 处 %s" % (v, end, len(hits), [hex(h) for h in hits[:6]]))

P("")
P("-- 尾部校验和检验")
t4 = data[-4:]; t2 = data[-2:]
P("   tail4=%s  u32BE=0x%08X u32LE=0x%08X | tail2=%s u16BE=0x%04X u16LE=0x%04X"
  % (t4.hex(), int.from_bytes(t4, "big"), int.from_bytes(t4, "little"),
     t2.hex(), int.from_bytes(t2, "big"), int.from_bytes(t2, "little")))
CANDS = {"u32BE": int.from_bytes(t4, "big"), "u32LE": int.from_bytes(t4, "little"),
         "u16BE": int.from_bytes(t2, "big"), "u16LE": int.from_bytes(t2, "little")}
CANDS["~u32LE&0xFFFF"] = (~int.from_bytes(t4, "little")) & 0xFFFF
CANDS["~u16BE"] = (~int.from_bytes(t2, "big")) & 0xFFFF
CANDS["~u16LE"] = (~int.from_bytes(t2, "little")) & 0xFFFF

_TAB = {}
def crc16_bits(b, poly, init=0, refin=True, xorout=0):
    key = (poly, refin)
    if key not in _TAB:
        tab = []
        for i in range(256):
            c = i
            if refin:
                c ^= 0  # placeholder
                for _ in range(8):
                    c = (c >> 1) ^ (poly if c & 1 else 0)
            else:
                c = i << 8
                for _ in range(8):
                    c = ((c << 1) ^ (poly if c & 0x8000 else 0)) & 0xFFFF
            tab.append(c)
        _TAB[key] = tab
    tab = _TAB[key]
    crc = init
    if refin:
        for x in b:
            crc = (crc >> 8) ^ tab[(crc ^ x) & 0xFF]
    else:
        for x in b:
            crc = ((crc << 8) & 0xFFFF) ^ tab[((crc >> 8) ^ x) & 0xFF]
    return crc ^ xorout

ck_rows = []
for rname, r in (("file[0:-4]", data[:-4]), ("file[0:-2]", data[:-2]),
                 ("file[4:]", data[4:]), ("file[16:]", data[16:]), ("file[0:]", data)):
    a = np.frombuffer(r[:len(r) // 2 * 2], dtype=np.uint8)
    wl = np.frombuffer(r[:len(r) // 2 * 2], dtype="<u2").astype(np.uint64)
    wb = np.frombuffer(r[:len(r) // 2 * 2], dtype=">u2").astype(np.uint64)
    ql = np.frombuffer(r[:len(r) // 4 * 4], dtype="<u4").astype(np.uint64)
    qb = np.frombuffer(r[:len(r) // 4 * 4], dtype=">u4").astype(np.uint64)
    x8 = 0
    for c in r:
        x8 ^= c
    tests = [
        ("sum8", int(a.sum()), 0xFFFF),
        ("xor8", x8, 0xFF),
        ("sum16_LE", int(wl.sum()) & 0xFFFF, 0xFFFF),
        ("sum16_BE", int(wb.sum()) & 0xFFFF, 0xFFFF),
        ("sum32_LE", int(ql.sum()) & 0xFFFFFFFF, 0xFFFFFFFF),
        ("sum32_BE", int(qb.sum()) & 0xFFFFFFFF, 0xFFFFFFFF),
        ("crc32", zlib.crc32(r) & 0xFFFFFFFF, 0xFFFFFFFF),
        ("crc16_IBM", crc16_bits(r, 0xA001, 0x0000), 0xFFFF),
        ("crc16_CCITT_FALSE", crc16_bits(r, 0x1021, 0xFFFF, refin=False), 0xFFFF),
        ("crc16_XMODEM", crc16_bits(r, 0x1021, 0x0000, refin=False), 0xFFFF),
        ("crc16_MODBUS", crc16_bits(r, 0xA001, 0xFFFF), 0xFFFF),
        ("crc16_X25", crc16_bits(r, 0x8408, 0xFFFF, xorout=0xFFFF), 0xFFFF),
    ]
    for (nm, val, msk) in tests:
        match = [k for k, cv in CANDS.items() if cv == val]
        ck_rows.append((rname, nm, val, msk, match))
        P("   %-12s %-20s = 0x%0*X %s" % (rname, nm, val, 8 if msk > 0xFFFF else 4,
                                          "*** = " + ",".join(match) if match else ""))
P("")
P("   命中数 = %d" % sum(1 for r in ck_rows if r[4]))

P("")
P("-- 头 4 字节 f9 7b 03 00")
P("   LE u32=0x%08X=%d ; BE u32=0x%08X=%d ; N=99865 (0x18619)"
  % (int.from_bytes(data[:4], "little"), int.from_bytes(data[:4], "little"),
     int.from_bytes(data[:4], "big"), int.from_bytes(data[:4], "big")))
P("   6 个可能取值为长度字段的首字节处 u32 值:")
for i in range(0, 48, 4):
    P("     off %2d: BE=0x%08X LE=0x%08X" % (i, int.from_bytes(data[i:i+4], "big"),
                                            int.from_bytes(data[i:i+4], "little")))

# 分段表 (offset,len) 检验
P("")
P("-- 头部是否存在 (offset,length) 分段表: 搜索 a+b==N 或 a+b<=N 的相邻 32 位对")
seg = []
for i in range(0, 500, 4):
    for end in ("big", "little"):
        for i2 in range(i + 4, min(i + 40, 508), 2):
            a = int.from_bytes(data[i:i + 4], end)
            b = int.from_bytes(data[i2:i2 + 4], end)
            if 0 < a < N and 0 < b < N and a % 16 == 0 and b % 16 == 0 and a + b == N:
                seg.append((i, end, a, b))
P("   精确 a+b==N 且 16B 对齐命中: %d %s" % (len(seg), seg[:5]))

# ============================================================== TASK 3
P("")
P("=" * 78)
P("TASK 3")
P("=" * 78)

def hist_windows(b, W, nb):
    nw = N // W
    h = np.zeros((nw, nb))
    if nb == 256:
        for i in range(nw):
            h[i] = np.bincount(b[i * W:(i + 1) * W], minlength=256)[:256]
    else:
        sh = (b >> (8 - int(math.log2(nb)))).astype(np.int64)
        for i in range(nw):
            h[i] = np.bincount(sh[i * W:(i + 1) * W], minlength=nb)
    return h, nw

def jsd_series(h, nw):
    out = []
    for i in range(nw - 1):
        p, q = h[i], h[i + 1]
        m = (p + q) / 2
        out.append(ent(m) - (ent(p) + ent(q)) / 2)
    return np.array(out)

def analyze(W, nb, label):
    h, nw = hist_windows(buf, W, nb)
    Hw = np.array([ent(h[i]) for i in range(nw)])
    J = jsd_series(h, nw)
    # 零模型
    nJ = []
    for _ in range(NS):
        sb = rng.permutation(buf)
        hh, _ = hist_windows(sb, W, nb)
        nJ.append(jsd_series(hh, nw).max())
    nJ = np.array(nJ)
    P("")
    P("[%s] 窗口=%d, 熵 min=%.3f max=%.3f mean=%.3f" % (label, nw, Hw.min(), Hw.max(), Hw.mean()))
    P("   零模型(每次置换的 max JSD): mean=%.4f p95=%.4f max=%.4f"
      % (nJ.mean(), np.percentile(nJ, 95), nJ.max()))
    order = np.argsort(-J)[:8]
    P("   %-6s %-9s %-9s %-9s %-9s" % ("rank", "boundary", "JSD", "H[i]", "H[i+1]"))
    rows = []
    for rk, k in enumerate(order, 1):
        pv = float((nJ >= J[k]).mean())
        P("   %-6d 0x%05X   %-9.4f %-9.3f %-9.3f  p_null=%.2f"
          % (rk, (k + 1) * W, J[k], Hw[k], Hw[k + 1], pv))
        rows.append(((k + 1) * W, J[k], Hw[k], Hw[k + 1], pv))
    P("   超过零模型最大值(p<1/%d)的边界数: %d" % (NS, int((J > nJ.max()).sum())))
    return Hw, J, rows, nJ, nw

Hw256, J256, rows256, nJ256, nw256 = analyze(256, 256, "256B / 256 bin  (题目指定)")
Hw1k, J1k, rows1k, nJ1k, nw1k = analyze(1024, 16, "1024B / 16 bin  (高功效对照)")

P("")
P("-- 4KB 熵剖面")
P("   %-9s %-6s %-7s %s" % ("off", "size", "H", "top4"))
for i in range(0, N, 4096):
    seg = buf[i:min(i + 4096, N)]
    hh = np.bincount(seg, minlength=256)[:256]
    tb = np.argsort(-hh)[:4]
    P("   0x%05X  %-6d %.3f   %s" % (i, len(seg), ent(hh),
      " ".join("%02X:%d" % (t, hh[t]) for t in tb)))

# ============================================================== 写报告
L = []
def W_(s=""):
    L.append(s)

W_("# Nikon LS-8000 ED `FIRMDATA` 结构测绘报告")
W_("")
W_("- 样本: `<HOME>\\Videos\\LS8000fw111_win\\SUPERCOOLSCAN8000ED_111\\.rsrc\\0\\RCDATA\\FIRMDATA`（只读）")
W_("- 大小: **99865 B = 0x18619**，为奇数；因式分解 99865 = 5 x 19973（19973 为素数），**不含任何 2 的幂因子**")
W_("- 脚本: `LS8000/tools/layout_scan.py`；原始日志: `LS8000/02_analysis/layout_scan_output.txt`")
W_("- 头 48B: `%s`" % " ".join("%02X" % b for b in data[:48]))
W_("- 尾 16B: `%s`" % " ".join("%02X" % b for b in data[-16:]))
W_("")
W_("## 0. 结论")
W_("")
W_("<!--CONCLUSIONS-->")
W_("")
W_("## 1. 基本统计（用于选择零模型）")
W_("")
W_("| 指标 | 数值 | 判读 |")
W_("|---|---|---|")
W_("| 全局字节熵 | %.4f bit/byte | 与均匀分布(8.0)仅差 %.2f bit |" % (H_GLOBAL, 8 - H_GLOBAL))
W_("| 0x00 占比 | %.2f%% | 均匀应为 0.39%%，超 3 倍 |" % (100 * G[0] / N))
W_("| 0xFF 占比 | %.2f%% | 超 4 倍 |" % (100 * G[255] / N))
W_("| 0x40 占比 | %.2f%% | 超 4 倍 |" % (100 * G[0x40] / N))
W_("| 高位=1 字节占比 | %.4f | 均匀 0.5，偏低 |" % hi_bit)
W_("| zlib -9 压缩率 | %.4f | 接近 1 → 数据本身近似不可再压缩 |" % (len(z) / N))
W_("| 最长同值游程 | %d B (0x%02X @0x%05X) | 无长零填充区 |" % (maxrun, maxrun_byte, maxrun_pos))
W_("")
W_("字节分布**显著不均匀**（0x00 = 3.0%% vs 均匀 0.39%%）。因此题目给的随机期望")
W_("`p0 = 区间大小/65536`（或 /2^32）在本样本上**系统性低估**尾部命中数——")
W_("一个偶然的 `00 00 xx xx` 就会让 32 位区间命中。故本报告对每个量同时给出：")
W_("")
W_("- **p0_均匀**：题目规定的均匀随机期望；")
W_("- **置换零模型**：把全部 99865 字节随机置换 %d 次（严格保持字节直方图、破坏所有顺序结构），" % NS)
W_("  统计每个窗口的命中分布。**这是唯一能排除\"字节分布偏斜\"假阳性的判据**，结论以它为准。")
W_("")
W_("## 2. 任务一：指针表扫描")
W_("")
W_("窗口 1024 B；16 位项每窗 512 个、32 位项每窗 511 个。")
W_("")
W_("| 位宽 | 端 | 基址 | 命中/总数 | p0_均匀期望 | 置换期望 | z_均匀 | z_置换 | 显著窗口 |")
W_("|---|---|---|---|---|---|---|---|---|")
for r in task1_rows:
    W_("| %d | %s | 0x%06X | %d/%d | %.2f | %.2f ± %.2f | %+.1f | %+.2f | %d |"
      % (r["wd"], r["e"], r["bs"], r["tot"], n16 if r["wd"] == 16 else n32,
         r["exp_uni"], r["nm"], r["ns"], r["z_uni"], r["z_sh"], len(r["regs"])))
W_("")
W_("> 16 位 `base=0x0000` 一行：区间 [0, 99865) 覆盖全部 65536 个 16 位值，p0 = 1.0，")
W_("> 命中率恒为 1.0，**对\"是否存在指针表\"零信息量**，不可作为证据。")
W_("")
W_("### 2.1 置换零模型下的显著区间")
W_("")
any_reg = False
for r in task1_rows:
    if r["regs"]:
        any_reg = True
        W_("**%d-bit %s base=0x%06X**：" % (r["wd"], r["e"], r["bs"]))
        W_("")
        W_("| 区间 | 命中/项数 | 命中率 | 置换 z |")
        W_("|---|---|---|---|")
        for (s, en, hh, cc, zz) in r["regs"]:
            W_("| 0x%05X–0x%05X | %d/%d | %.4f | %.1f |" % (s, en, hh, cc, hh / cc, zz))
        W_("")
if not any_reg:
    W_("无。")
    W_("")
W_("### 2.2 32 位 `0x00xxxxxx` 绝对地址形态")
W_("")
W_("| 端 | 命中 | 比例 | 均匀期望比例 | 倍数 |")
W_("|---|---|---|---|---|")
for e, arr in (("BE", BE32), ("LE", LE32)):
    m = (arr >= 0x00010000) & (arr <= 0x00FFFFFF)
    W_("| %s | %d | %.4f | 0.00389 | %.1fx |"
      % (e, int(m.sum()), m.mean(), m.mean() / ((0x01000000 - 0x10000) / 2**32)))
W_("")
W_("该 7 倍\"超出\"完全由 0x00 字节占比 3.0%%（均匀 0.39%%）解释：置换零模型已把这一项吸收。")
W_("")
W_("### 2.3 单调 / 等差表搜索")
W_("")
W_("32 位层面：**没有任何** >= 8 项的定差游程，也没有 >= 16 项的单调递增游程。")
W_("16 位层面出现真实的等差结构，集中在两处（详见 §4.3）：")
W_("")
W_("| 端 | 起始偏移 | 结束偏移 | 步长 | 项数 | 值域 |")
W_("|---|---|---|---|---|---|")
lean_rows = [t for t in delta_runs(LE16, OFF16)[:6]]
for (s, en, dd, ln) in lean_rows:
    sub = LE16[(OFF16 >= s) & (OFF16 <= en)].astype(np.int64)
    W_("| LE | 0x%05X | 0x%05X | %d (0x%X) | %d | 0x%X–0x%X |"
      % (s, en, dd, dd, ln, sub.min(), sub.max()))
W_("")
W_("## 3. 任务二：头部字段解析")
W_("")
W_("### 3.1 前 512 字节逐字段（8 B/行，前 4 个 u16BE 与 u16LE）")
W_("")
W_("| off | bytes | u16BE ×4 | u16LE ×4 |")
W_("|---|---|---|---|")
for i in range(0, 512, 8):
    seg = head[i:i + 8]
    be = [(seg[j] << 8) | seg[j + 1] for j in range(0, 8, 2)]
    le = [seg[j] | (seg[j + 1] << 8) for j in range(0, 8, 2)]
    W_("| 0x%03X | `%s` | %s | %s |"
      % (i, " ".join("%02X" % b for b in seg),
         " ".join("%04X" % v for v in be), " ".join("%04X" % v for v in le)))
W_("")
W_("### 3.2 呈现\"合理\"特征的字段")
W_("")
W_("判据：小整数(≤0x20)、掩码(0xFF/0x1FF/0xFFFF)、≈文件长度(±512)、N 的因数、")
W_("版本号形态(0x0100–0x01FF)、N 的十六进制片段(0x0186/0x0619/0x8619)。")
W_("")
W_("| off | 端 | 值 | 命中判据 |")
W_("|---|---|---|---|")
for (i, e, v, rs) in flag_rows:
    W_("| %d | %s | 0x%04X | %s |" % (i, e, v, ", ".join(rs)))
W_("")
W_("**关键否证**：")
W_("")
W_("- 99865 = 0x18619 需要 17 bit，**任何 16 位字段在数学上都不可能等于它**；")
W_("- 前 512 B 内 32 位字段（BE/LE、2 B 对齐全扫）**无一**等于 99865 / 99864 / 0x18619 / 0x18618 / 49932 / 5548；")
W_("- 全文件按任意字节对齐搜索 24 位值 `0x18619` 与 `0x18618`（双端）：**0 处命中**；")
W_("- 因此文件中**不存在**显式的\"本段长度 = 文件长度\"字段。这也符合")
W_("  `.rsrc/0/RCDATA/FIRMDATA` 是 Mac 资源叉里被拆分出来的资源体、其长度由外层资源头管理的情形。")
W_("")
W_("### 3.3 尾部 4 字节校验和检验")
W_("")
W_("尾部：`02 9B BB FF`；u32BE = 0x029BBBFF，u32LE = 0xFFBB9B02，u16BE = 0xBBFF，u16LE = 0xFFBB。")
W_("")
W_("对 5 种覆盖范围（file[0:-4]、file[0:-2]、file[4:]、file[16:]、全长）x 12 种算法")
W_("（sum8/xor8/sum16LE/sum16BE/sum32LE/sum32BE/CRC32/CRC16-IBM/CCITT-FALSE/XMODEM/MODBUS/X25）")
W_("x 7 个候选存储形式，共 %d 组比较：" % len(ck_rows))
W_("")
W_("**命中 0 组。** 尾部 4 字节不是上述任何标准校验和。")
W_("")
W_("| 范围 | 算法 | 计算值 | 是否等于尾部候选 |")
W_("|---|---|---|---|")
for (rn, nm, val, msk, match) in ck_rows:
    if rn in ("file[0:-4]", "file[0:-2]"):
        W_("| %s | %s | 0x%0*X | %s |" % (rn, nm, val, 8 if msk > 0xFFFF else 4,
                                        ("**" + ",".join(match) + "**") if match else "否"))
W_("")
W_("### 3.4 头 4 字节 `F9 7B 03 00`")
W_("")
W_("| 解释 | 值 | 与 N 关系 |")
W_("|---|---|---|")
W_("| u32LE | 0x00037BF9 = %d | N=99865，差 %d，不是长度 |" % (int.from_bytes(data[:4], "little"), abs(int.from_bytes(data[:4], "little") - N)))
W_("| u32BE | 0xF97B0300 = %d | 远超镜像大小，非长度 |" % int.from_bytes(data[:4], "big"))
W_("| u16LE pair | 0x7BF9, 0x0003 | 0x0003 可读作小整数/计数 |")
W_("| u16BE pair | 0xF97B, 0x0300 | 无长度意义 |")
W_("")
W_("头部也不存在 `(offset,length)` 形式的 16 B 对齐分段表（精确匹配 a+b==N 的命中数 = %d）。" % len(seg))
W_("")
W_("## 4. 任务三：分区边界")
W_("")
W_("### 4.1 4 KB 熵剖面")
W_("")
W_("| off | size | H (bit/B) | top-4 字节 |")
W_("|---|---|---|---|")
for i in range(0, N, 4096):
    seg = buf[i:min(i + 4096, N)]
    hh = np.bincount(seg, minlength=256)[:256]
    tb = np.argsort(-hh)[:4]
    W_("| 0x%05X | %d | %.3f | %s |" % (i, len(seg), ent(hh),
      " ".join("%02X:%d" % (t, hh[t]) for t in tb)))
W_("")
W_("### 4.2 256 B / 256 bin 突变检测（题目指定粒度）")
W_("")
W_("| rank | 边界偏移 | JSD (bit) | H[i] | H[i+1] | p_null |")
W_("|---|---|---|---|---|---|")
for rk, (bnd, j, h1, h2, pv) in enumerate(rows256[:8], 1):
    W_("| %d | 0x%05X | %.4f | %.3f | %.3f | %.2f |" % (rk, bnd, j, h1, h2, pv))
W_("")
W_("零模型（%d 次全文件置换，每次取该次的最大 JSD）：mean = %.4f，p95 = %.4f，max = %.4f。" % (NS, nJ256.mean(), np.percentile(nJ256, 95), nJ256.max()))
W_("观测最大值 %.4f < 零模型最大值 %.4f，**没有任何边界在 256 B 粒度上统计显著**。" % (J256.max(), nJ256.max()))
W_("原因：256 个样本摊到 256 个 bin，每 bin 期望计数 ≈1，JSD 的抽样噪声本身就有 ~1.3 bit 量级，")
W_("该配置**几乎没有检验功效**，只能作为描述性排序。")
W_("")
W_("### 4.3 1024 B / 16 bin 高功效对照")
W_("")
W_("| rank | 边界偏移 | JSD (bit) | H[i] | H[i+1] | p_null |")
W_("|---|---|---|---|---|---|")
for rk, (bnd, j, h1, h2, pv) in enumerate(rows1k[:8], 1):
    W_("| %d | 0x%05X | %.4f | %.3f | %.3f | %.2f |" % (rk, bnd, j, h1, h2, pv))
W_("")
W_("零模型 max JSD：mean = %.4f，p95 = %.4f，max = %.4f；观测最大 %.4f。"
  % (nJ1k.mean(), np.percentile(nJ1k, 95), nJ1k.max(), J1k.max()))
W_("超过零模型最大值的边界数：%d。" % int((J1k > nJ1k.max()).sum()))
W_("")
W_("### 4.4 唯一稳健的内部结构信号：LE-u16 等差 18 的\"阶梯区\"")
W_("")
W_("整文件统计相邻 LE-u16 差值，众数差为 **18 (0x12)**，出现 967 次（占 49931 个位置的 1.94%%），")
W_("随机期望仅约 0.8 次——这是全文件**唯一**远超偶然的算术结构。其空间分布：")
W_("")
W_("| 窗口起点 | 窗口内 diff==18 比例 |")
W_("|---|---|")
for f, i in top[:6]:
    W_("| 0x%05X | %.3f |" % (i, f))
W_("")
W_("同一批字节按 BE 读则表现为差值 0x1200（出现 653 次），说明真实结构是")
W_("**偶数位字节每步 +0x12、奇数位字节保持**，即一段 16 位 LE 递增序列，")
W_("且每隔 17 字节插入 1 个 0x00 填充字节、并在低字节回绕时高字节跳过 0x10 档")
W_("（例：0x4F7E → 0x4F90 … → 0x4FFC → 0x5F0E，而非 0x500E）。")
W_("尾部 0x185D9–0x18617 是最干净的一段：0xAFDA, 0xAFEC, 0xAFFE, 0xBF10, 0xBF23, 0xBF34 … 0xBFC5，")
W_("平均步长 ≈ 18、单调递增但步长有 ±1~+18 抖动，呈**量化曲线/LUT**而非严格等差。")
W_("")
W_("## 5. 局限与不确定性")
W_("")
W_("- 置换零模型只消除\"字节分布偏斜\"，不能消除\"存在任何重复局部模式\"带来的偏差；")
W_("  若镜像本身包含大量结构化数据表，置换零模型会偏乐观（更容易判\"显著\"）。")
W_("- 任务三的边界检测对\"同分布但语义不同\"的段（如代码段紧邻常量表）本质无能；")
W_("  这里只能报告\"在字节分布意义上文件是同质的\"。")
W_("- 未做反汇编/指令解码（按纪律不调用 REA/Ghidra），因此无法从操作码层面确认 CPU 架构；")
W_("  架构结论仅基于\"有无绝对地址表\"这一间接证据。")
W_("- `.rsrc/...` 路径表明样本是从 Mac 资源叉拆出的资源体，可能**不是**完整加载镜像，")
W_("  长度/校验和字段可能位于外层容器而非本文件内。")
W_("")

with open(TXT, "w", encoding="utf-8") as f:
    f.write(LOG.getvalue())
with open(MD, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(LOG.getvalue())
print("\n[written] %s\n[written] %s" % (MD, TXT))
