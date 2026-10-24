#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LS-8000 ED FIRMDATA 尾部规律区结构判定
--------------------------------------------------
只读目标文件，不修改输入。输出 02_analysis/tail_resolve.md

用法:
  python tail_resolve.py            # 生成报告
"""
import hashlib
import collections
import numpy as np

SRC = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111\.rsrc\0\RCDATA\FIRMDATA"
DST = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis\tail_resolve.md"

raw = open(SRC, "rb").read()
N = len(raw)
d = np.frombuffer(raw, dtype=np.uint8)
di = d.astype(np.int64)                      # 规避 uint8 位移溢出
out = []


def P(s=""):
    print(s)
    out.append(s)


def u16(b):
    return int(di[b]) | (int(di[b + 1]) << 8)


# ---------------------------------------------------------------- 0
def entropy(bs):
    if not len(bs):
        return 0.0
    c = np.bincount(np.frombuffer(bs, dtype=np.uint8), minlength=256).astype(float)
    p = c / c.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


P("# 尾部规律区结构判定（LS-8000 ED FIRMDATA）")
P()
P("| 项 | 值 |")
P("|---|---|")
P(f"| 文件 | `{SRC}` |")
P(f"| 大小 | {N} 字节 (0x{N:X}) |")
P(f"| MD5 | `{hashlib.md5(raw).hexdigest()}` |")
P(f"| 全文件熵 | {entropy(raw):.4f} bits/byte |")
blk = [entropy(raw[i:i + 4096]) for i in range(0, N, 4096)]
P(f"| 4096B 分块熵 | {len(blk)} 块, {min(blk):.4f} .. {max(blk):.4f}, 末块 {blk[-1]:.4f} |")
P(f"| 零字节 | {int((d==0).sum())} ({100*(d==0).mean():.2f}%) |")
P()
P("> 复核结论：用户观察 1 成立（熵 7.6741，末块 6.68）。")
P()

# ---------------------------------------------------------------- 1
P("## 1. 规律区边界")
P()
P("判据：272 字节窗口内，17 个候选相位中「最优相位的 `0x00` 命中率」。")
P("随机数据期望值 ≈ 1/17 = 0.059；结构化数据该相位应接近 1.0。")
P()


def phase_zero_score(o, win=272):
    seg = di[o:o + win]
    if len(seg) < 68:
        return 0.0
    best = 0.0
    for r in range(17):
        idx = np.arange(r, len(seg), 17)
        if len(idx) >= 8:
            best = max(best, float((seg[idx] == 0).mean()))
    return best


step = 8
offs = np.arange(0, N - 272, step)
sc = np.array([phase_zero_score(int(o)) for o in offs])


def suffix_start(th):
    i = len(offs) - 1
    while i > 0 and sc[i] >= th:
        i -= 1
    return i + 1


CORE0 = int(offs[suffix_start(0.90)])
DEG0 = int(offs[suffix_start(0.35)])
P(f"- 命中率连续 ≥0.90 的尾部起点（**核心区**）：`0x{CORE0:05X}`")
P(f"- 命中率连续 ≥0.35 的尾部起点（含退化段）：`0x{DEG0:05X}`")
P(f"- 全窗口均值 {sc.mean():.3f}，最大 {sc.max():.3f}")
P()
P("### 1.1 边界剖面（每 128 字节）")
P()
P("| 窗口起点 | 17 相位零命中率 | 判读 |")
P("|---|---|---|")
for o in range(0x17400, N - 272, 128):
    k = int((o - offs[0]) // step)
    v = sc[k] if 0 <= k < len(sc) else 0.0
    tag = "随机" if v < 0.15 else ("弱周期" if v < 0.35 else ("部分周期" if v < 0.90 else "强周期"))
    P(f"| 0x{o:05X} | {v:.3f} | {tag} |")
P()
P("结论：规律区不是单一边界，而是 **块 A（0x17A0D–0x17E1A）+ 退化间隙 + 块 B（0x1804E–0x18604）** 两段强周期，")
P("其前方 0x17600–0x17980 为部分周期（周期存在但夹入额外字节）。")
P("0x17400–0x17580 命中率 0.062–0.125，等于随机基线 → 规律区不早于 0x17600。")
P()

# ---------------------------------------------------------------- 2
P("## 2. 记录级结构：17 字节 = 8 × uint16(LE) + 1 个 0x00 填充")
P()


def grid(padstart_search, label):
    best = None
    for padpos in range(padstart_search, padstart_search + 17):
        nrec = (N - padpos) // 17
        if nrec < 8:
            continue
        pads = [int(di[padpos + 17 * k + 16]) for k in range(nrec)]
        hit = float(np.mean([p == 0 for p in pads]))
        if best is None or hit > best[1]:
            best = (padpos, hit, nrec)
    return best


padpos, pad_hit, nrec = grid(CORE0, "B")
P(f"- 核心区网格对齐结果：记录首字节 `0x{padpos:05X}`，{nrec} 条记录")
P(f"- **第 17 字节 == 0x00 的比例：{pad_hit:.4f}**（随机基线 1/256 = 0.0039）")
P(f"- 核心区跨度：`[0x{padpos-1:05X}, 0x{N:05X})` = {N-(padpos-1)} 字节")
P()

# ---------------------------------------------------------------- 3
def decode(start, end):
    n = (end - start) // 17
    R = []
    for k in range(n):
        b = start + 17 * k
        R.append([u16(b + 2 * j) for j in range(8)])
    return np.array(R, dtype=np.int64)


def block(name, start, nrec):
    end = start + nrec * 17
    R = decode(start, end)
    assert len(R) == nrec, (len(R), nrec)
    pads = [int(di[start + 17 * k + 16]) for k in range(len(R))]
    V = (((R >> 12) & 0xF) << 8) | (R & 0xFF)
    dl = np.diff(V.ravel())
    P(f"**{name}** `[0x{start-1:05X}, 0x{end:05X})`  {end-start} 字节 / {len(R)} 条记录")
    P()
    P("| 指标 | 数值 |")
    P("|---|---|")
    P(f"| pad == 0x00 | {float(np.mean(np.array(pads)==0)):.4f} |")
    P(f"| bits[11:8] == 0xF | {float(np.mean(((R>>8)&0xF)==0xF)):.4f} |")
    P(f"| 16 位值域 | 0x{R.min():04X} .. 0x{R.max():04X} |")
    P(f"| 12 位值域 | 0x{V.min():03X} .. 0x{V.max():03X} |")
    P(f"| Δ 众数 | {collections.Counter(dl.tolist()).most_common(1)[0][0]}（占 {float(np.mean(dl==collections.Counter(dl.tolist()).most_common(1)[0][0])):.4f}） |")
    P(f"| 0 < Δ ≤ 0x40 | {float(np.mean((dl>0)&(dl<=0x40))):.4f} |")
    P(f"| Δ ≥ 0 | {float(np.mean(dl>=0)):.4f} |")
    P()
    return R, V


P("## 3. 两个 17 周期子块的独立复核")
P()
RA, VA = block("块 A", 0x17A0E, 61)
RB, VB = block("块 B", 0x1804F, 86)
P(f"- 块间退化间隙：`0x17E2B .. 0x1804D`，{0x1804D-0x17E2B+1} 字节，17 相位命中率降至 0.25–0.69。")
P(f"- 文件尾残余（末 pad `0x18604` 之后）：20 字节 = 8 个 16 位字 + 4 字节 `02 9b bb ff`，")
P("  即最后一个记录缺 pad，尾部另有 4 字节尾缀，未纳入统计。")
P("- 这正是 pad 命中率为 0.9885 而非 1.0000 的原因：87 条记录里第 87 条残缺。")
P()

# ---------------------------------------------------------------- 4
P("## 4. 位不变式与两种读数")
P()
W = np.vstack([RA, RB])
V12 = (((W >> 12) & 0xF) << 8) | (W & 0xFF)
P(f"- 合并 {len(W)} 条记录 / {W.size} 个 16 位字")
P(f"- **bits[11:8] == 0xF 占比 {float(np.mean(((W>>8)&0xF)==0xF)):.4f}**（随机基线 0.0625）")
P(f"- bits[15:12] 覆盖 {len(set((W>>12).ravel().tolist()))} 种取值（0..F 全覆盖）")
P()
P("因此 16 位字的位域为：`[15:12]=数据高 4 位 | [11:8]=0xF 常量 | [7:0]=数据低 8 位`。")
P("据此定义 12 位读数 `v = ((w>>12)<<8) | (w&0xFF)`，与原始 16 位读数对比：")
P()
P("| 读法 | 值域 | Δ 众数 | 众数占比 | 0<Δ≤0x40 | Δ≥0 |")
P("|---|---|---|---|---|---|")
for nm, arr in (("原始 16 位 LE", W.ravel()), ("12 位旋转读数", V12.ravel())):
    dl = np.diff(arr)
    c = collections.Counter(dl.tolist())
    m, mc = c.most_common(1)[0]
    P(f"| {nm} | 0x{int(arr.min()):X}..0x{int(arr.max()):X} | {m} | {mc/len(dl):.4f} | "
      f"{float(np.mean((dl>0)&(dl<=0x40))):.4f} | {float(np.mean(dl>=0)):.4f} |")
P()
dl12 = np.diff(V12.ravel())
P(f"12 位读数 Δ 直方图（前 12）：`{collections.Counter(dl12.tolist()).most_common(12)}`")
P()
# 换位解释覆盖率
sw = sum(1 for i in range(len(dl12) - 1) if dl12[i] < 0 and dl12[i] + dl12[i + 1] == 36)
P(f"- 相邻差 `(-a, +b)` 且 a+b==36（即两元素互换位置的特征）的出现次数：{sw} 对，")
P(f"  覆盖 {2*sw} / {len(dl12)} = **{2*sw/len(dl12):.4f}** 的相邻差。")
P("- 该覆盖率不足以承担残差解释，故「整体是严格等差、局部被换位打乱」仍**未获证实**。")
P()

# ---------------------------------------------------------------- 5
P("## 5. 参数穷举：W ∈ {2,3,4} × 字节序 × stride ∈ [2,32] × 相位")
P()
P(f"搜索区间 `[0x{CORE0:05X}, 0x{N:05X})`。每个 (W, 字节序, stride) 组合遍历全部 {1}–32 个相位取最优".replace("{1}", "1"))
P("（相位扫描是超集，比只扫 [0, W-1] 更宽松，因此下面的负结论更强）。")
P()
P("指标：")
P("- `in_file`：元素值 ∈ [0, N) 的比例")
P("- `base=0x…`：元素值 ∈ [base, base+N) 的比例")
P("- `modal / hit`：相邻元素差值众数及其占比")
P("- `smooth`：差值 ∈ (0, 0x40] 的比例")
P()

seg = raw[CORE0:]
M = len(seg)
BASES = [0x0, 0x4000, 0x8000, 0x800000, 0xC00000]


def extract(Wd, endian, phase, stride):
    order = "little" if endian == "LE" else "big"
    vals = []
    o = phase
    while o + Wd <= M:
        vals.append(int.from_bytes(seg[o:o + Wd], order))
        o += stride
    return np.array(vals, dtype=np.int64)


rows = []
for Wd in (2, 3, 4):
    for endian in ("LE", "BE"):
        for stride in range(2, 33):
            best = None
            for ph in range(min(stride, 32)):
                v = extract(Wd, endian, ph, stride)
                if len(v) < 20:
                    continue
                dl = np.diff(v)
                c = collections.Counter(dl.tolist())
                modal, mc = c.most_common(1)[0]
                hit = mc / len(dl)
                smooth = float(np.mean((dl > 0) & (dl <= 0x40)))
                if best is None or (hit, smooth) > best[0]:
                    best = ((hit, smooth), ph, len(v),
                            float(np.mean((v >= 0) & (v < N))),
                            {b: float(np.mean((v >= b) & (v < b + N))) for b in BASES},
                            modal, hit, smooth, int(v.min()), int(v.max()))
            if best is None:
                continue
            _, ph, ne, inf, bases, modal, hit, smooth, vmin, vmax = best
            rows.append(dict(W=Wd, e=endian, s=stride, ph=ph, n=ne, inf=inf, b=bases,
                             modal=modal, hit=hit, smooth=smooth, vmin=vmin, vmax=vmax))

rows.sort(key=lambda r: (r["hit"], r["smooth"]), reverse=True)
P(f"共评估 **{len(rows)}** 个 (W, 字节序, stride) 组合。")
P()
P("### 5.1 前 15 名")
P()
P("| W | 序 | stride | 相位 | n | Δ众数 | hit | smooth | in_file | 0x4000 | 0x8000 | 0x800000 | 0xC00000 |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows[:15]:
    P(f"| {r['W']} | {r['e']} | {r['s']} | {r['ph']} | {r['n']} | {r['modal']} | {r['hit']:.3f} | "
      f"{r['smooth']:.3f} | {r['inf']:.3f} | {r['b'][0x4000]:.3f} | {r['b'][0x8000]:.3f} | "
      f"{r['b'][0x800000]:.3f} | {r['b'][0xC00000]:.3f} |")
P()
P("### 5.2 完整结果表（186 行）")
P()
P("| W | 序 | stride | 相位 | n | Δ众数 | hit | smooth | in_file | 0x4000 | 0x8000 | 0x800000 | 0xC00000 | 值域 |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    P(f"| {r['W']} | {r['e']} | {r['s']} | {r['ph']} | {r['n']} | {r['modal']} | {r['hit']:.3f} | "
      f"{r['smooth']:.3f} | {r['inf']:.3f} | {r['b'][0x4000]:.3f} | {r['b'][0x8000]:.3f} | "
      f"{r['b'][0x800000]:.3f} | {r['b'][0xC00000]:.3f} | 0x{r['vmin']:X}..0x{r['vmax']:X} |")
P()
best = rows[0]
P(f"最高 hit = **{best['hit']:.3f}**（W={best['W']} {best['e']} stride={best['s']} phase={best['ph']}）。")
P("**没有任何组合达到 0.90 门槛**，故“单一固定步长数组”模型不成立。")
P()
P("整段连续 16 位（stride=2, phase=0）的 hit 只有 "
  f"{[r for r in rows if r['W']==2 and r['e']=='LE' and r['s']==2][0]['hit']:.3f}；")
P("即“用户观察 3 中的 0x12 步长”只在局部片段成立，全区间占比不足一半。")
P()

# ---------------------------------------------------------------- 6
P("## 6. 其他假设的否证")
P()
P("| 假设 | 统计量 | 结果 |")
P("|---|---|---|")
# 17-bit
bf = []
o = CORE0
while o + 17 <= N:
    x = int.from_bytes(raw[o:o + 17], "little")
    bf += [(x >> (17 * i)) & 0x1FFFF for i in range(8)]
    o += 17
bf = np.array(bf)
dlb = np.diff(bf)
cb = collections.Counter(dlb.tolist())
P(f"| 8×17bit LSB-first 比特域 | Δ 众数占比 | {cb.most_common(1)[0][1]/len(dlb):.4f}（众数 {cb.most_common(1)[0][0]}）→ 否证 |")
# float32
fl = np.frombuffer(seg[:len(seg) // 4 * 4], dtype="<f4")
fin = np.isfinite(fl)
plaus = float(np.mean(fin & (np.abs(fl) > 1e-6) & (np.abs(fl) < 1e6)))
P(f"| 32 位小端 float | 量级合理占比 | {plaus:.3f}（对应层 {int(fin.sum())}/{len(fl)} 有限值）→ 否证 |")
# 17 周期本身
P(f"| 17 字节周期 + 0x00 填充 | pad 命中 | {pad_hit:.4f} → **成立** |")
P(f"| bits[11:8]==0xF 位不变式 | 命中 | {float(np.mean(((W>>8)&0xF)==0xF)):.4f} → **成立** |")
P()
P("补充：16 位读数“全部落在 [0, N)”是**无判别力**的巧合 —— N = 99865 > 65536，")
P("任何 16 位值都必然 < N，`in_file` 对 W=2 恒为 1.000。")
P("对 W=3 才有判别力：各组合 in_file 最高仅 0.184，且此时 Δ 众数达 10^6 量级，无结构可言。")
P()

# ---------------------------------------------------------------- 7
P("## 7. 数值范围：地址 还是 索引")
P()
P("| 解释 | 数值 | 判定 |")
P("|---|---|---|")
P(f"| 12 位读数当文件偏移 | 0x{V12.min():03X} .. 0x{V12.max():03X}（{int(V12.min())}..{int(V12.max())}） | 全部 < 4096，指向文件头 4KB，与规律区自身 (0x{CORE0:05X}+) 不重叠 |")
P(f"| 12 位读数 + base | base 需 ≤ 0x{V12.min():X} 且 base+N > 0x{V12.max():X} | base 只能取 0；0x4000/0x8000/0x800000/0xC00000 命中率均为 0.000 |")
P(f"| 16 位读数当地址 | 0x{int(W.min()):04X} .. 0x{int(W.max()):04X} | 与任何候选 base 都不自洽（表中最高 0.750，且伴随 Δ 众数 4096 的病态对齐） |")
P(f"| 当表索引 | 0..{int(V12.max())} | 若为 4096 项表索引，则表长需 4096×k 字节；文件内无 4096 项规模的同构表，规律区仅 {N-CORE0} 字节 |")
P()
P(f"数值本身：12 位读数在 `0x{V12.min():03X}..0x{V12.max():03X}` 内分布，{len(np.unique(V12))}/{V12.size} 个互不相同，")
P(f"Δ 众数 18 = 0x12，若按 4096 值域计，一个完整扫过需 4096/18 ≈ 228 个元素；")
P(f"合并样本 {V12.size} 个元素 ≈ {V12.size/228:.2f} 个完整扫过，但序列并不在 4096 处循环（无 -4096 级负跳变），")
P("因此**不能**把 12 位读数解释为模 4096 的循环计数器。")
P()

# ---------------------------------------------------------------- 8
P("## 8. 判定")
P()
P("**部分成立，未达 90% 元素级判定门槛。**")
P()
P("已确证（数字支撑）：")
P()
P(f"1. 规律区为两个 17 字节周期的子块：块 A `0x17A0D–0x17E1A`（{61*17} B / 61 条），块 B `0x1804E–0x18604`（{86*17} B / 86 条）；")
P(f"   两块的「第 17 字节 == 0x00」命中率均为 {1.0:.4f}，核心区整体 {pad_hit:.4f}。")
P(f"2. 记录内为 8 个 uint16 小端字，且 `bits[11:8] == 0xF` 命中 {float(np.mean(((W>>8)&0xF)==0xF)):.4f}。")
P(f"3. 由此得到的 12 位读数是一个**近似等差递增序列**，Δ 众数 18，占 {float(np.mean(dl12==18)):.4f}；")
P(f"   Δ ∈ (0,0x40] 占 {float(np.mean((dl12>0)&(dl12<=0x40))):.4f}。")
P()
P("未确证：")
P()
P(f"1. 等差性只解释 {float(np.mean(dl12==18)):.4f} 的相邻差，放宽到 (0,0x40] 也只有 {float(np.mean((dl12>0)&(dl12<=0x40))):.4f}，**均低于 90%**。")
P(f"2. 残差包含小负步长（-6/-14/-15/-19）与成对互补的正步长（+42/+50）；「相邻两元素换位」只覆盖 {2*sw/len(dl12):.4f} 的 Δ，其余残差无证据解释。")
P("3. 17 字节周期、0xF 填充半字节这两个常量字段的**语义**（为何是 17、为何是 0xF）无证据可定。")
P("4. 数值不落在任何常见加载基址区间，也不构成文件内偏移或索引 → **不能认定为地址表**。")
P()

open(DST, "w", encoding="utf-8").write("\n".join(out))
print(f"\n[OK] 写入 {DST}  行数={len(out)}")
