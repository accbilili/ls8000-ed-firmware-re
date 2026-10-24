# `edges.json` 与 `dis_all.py` 的 `0x40` 组错址 —— 现状核验与修正建议

日期：2026-10-25 · 核验范围：`03_analysis\firmware\_jobfuncs\{dis_all.py, edges.json, f_*.asm}`
方法：隔离目录重跑 + 逐组逐边比对 · 脚本/产物在 `03_analysis\status\_verify\regen\`
**只读核验；未改动工作区任何文件。**

---

## 0. 结论（先说要点）

1. **`dis_all.py` 的源头错误已经在 00:31 被修正**（TARGETS 现为 `(0x40, 0x2AEAA)`，并加了 R5 更正注释）。
   → fw-reports 转达的「是否要修 `dis_all.py` 的 TARGETS」**已无需再修**。
2. **但 `edges.json` 只被改了「键名」、没被重新生成** → 当前工作区文件处于**「名实不符」的中间态**，比修正前更危险。
3. 现状实测：**键名已是 `40->02AEAA`，但该组 9 条边的内容仍是 `0x02AAAE` 的走查残留**（`from` 地址全部 < `0x02AEAA`）。
   → 下游若按「键名 = 该函数」理解，会把 `0x02AAAE` 的动作链当成 `0x02AEAA` 的动作链。**这是必须修的。**
4. 正确产物：**146 边**（call 72 / bcc 52 / jmp 22），`40->02AEAA` 组 = **13 边**。
5. 另有 1 个**孤儿文件** `f_02AAAE.asm`（修正前的错址产物），重跑不再生成。

---

## 1. 时间线（mtime 实测）

| 时刻 | 文件 | 变化 |
|---|---|---|
| 10-24 20:39 | `f_*.asm`（11 份，含 `f_02AAAE.asm`） | `dis_all.py` 原始产物（TARGETS 用错址） |
| 10-24 20:46 | `f_02AEAA.asm` | 事后单独补的正确版本 |
| 10-24 20:39 | `edges.json` | 原始产物，键名 `40->02AAAE` |
| **10-25 00:31** | **`dis_all.py`** | **TARGETS 改为 `(0x40, 0x2AEAA)`**，加 R5 更正注释 |
| **10-25 00:32** | **`edges.json`** | **键名被改为 `40->02AEAA`，但内容未重生成** |

---

## 2. 关键证据：当前 `edges.json` 的 0x40 组是「名实不符」

### 2.1 当前工作区文件（键名已改，内容未改）

```
键名: 40->02AEAA   （9 边）
  from 0x02AABA  call  bsr 0x02b196
  from 0x02AB0C  bcc   beq 0x02ab2a
  from 0x02AB1E  call  jsr 0x018e1e
  from 0x02AB28  call  jsr 0x01872e
  from 0x02AB32  call  bsr 0x02b1e4
  from 0x02AB44  call  bsr 0x02b22e
  from 0x02AB6A  jmp   jmp 0x02abd2
  from 0x02AB98  bcc   bne 0x02abf2
  from 0x02ABA4  call  bsr 0x02b11a
```

**判定依据（两条独立证据）**：

| 判据 | 实测 | 结论 |
|---|---|---|
| 该组全部 `from` 地址范围 | `0x02AABA` – `0x02ABE4`，**全部 < `0x02AEAA`** | 这些指令**不在** `0x02AEAA` 函数体内 → 是 `0x02AAAE` 的走查结果 |
| 6 条 call 目标 | `0x02B196` / `0x02B1E4` / `0x02B22E` / `0x02B11A` / `0x018E1E` / `0x01872E` | 与「`0x40` = 走片轴绝对移动」语义对不上（那应是 `0x02ADCE`/`0x02ACBA`/`0x02A2F6`） |

### 2.2 隔离重跑（`dis_all.py` 当前版本）→ 正确产物

```
key 0x40 fn 0x02AEAA: 62 insns, 13 edges
```
```
  from 0x02AEAC  bcc   bne 0x02aefa
  from 0x02AEBC  call  bsr 0x02adce    ← 走片轴定位
  from 0x02AEC2  call  bsr 0x02acba    ← 到位等待
  from 0x02AECE  bcc   bne 0x02aec0
  from 0x02AED0  jmp   bt  0x02af5a
  from 0x02AEDA  bcc   bls 0x02af0a
  from 0x02AEE6  jmp   bt  0x02af0e
  from 0x02AEF0  bcc   beq 0x02af62
  from 0x02AEF6  bcc   bls 0x02af24
  from 0x02AF00  jmp   bt  0x02af2a
  from 0x02AF1E  call  bsr 0x02a2f6    ← 相对步进
  from 0x02AF26  call  bsr 0x02acba    ← 到位等待
  from 0x02AF2E  bcc   bne 0x02aec0
```

**与 fw-reports 独立读出的 `f_02AEAA.asm` 指令链逐条吻合**：
`0x02AEC8` 取 `0x400408` → `0x02AEE0` 读 `+2` → `0x02AEE4 bsr 0x02ADCE` → `0x02AEEA bsr 0x02ACBA` → `0x02AEFE cmp.w #0x43E1` → `0x02AF46 bsr 0x02A2F6` → `0x02AF4E bsr 0x02ACBA` → `0x02AF5C mov.w r0,@0x4202B2`。

### 2.3 逐组比对：只有 0x40 组不同

| 组 | 工作区 | 重跑 | |
|---|---|---|---|
| `00->028722` | 0 边 | 0 边 | 相同 |
| `10->035598` | 26 | 26 | 相同 |
| **`40->02AEAA`** | **9** | **13** | **★不同** |
| `41->02B98A` | 11 | 11 | 相同 |
| `42->02CB66` | 4 | 4 | 相同 |
| `80->028722` | 0 | 0 | 相同 |
| `81->028648` | 3 | 3 | 相同 |
| `A0->03A3D4` | 59 | 59 | 相同 |
| `B0->027F24` | 4 | 4 | 相同 |
| `B3->02BBAE` | 10 | 10 | 相同 |
| `C1->02BA24` | 15 | 15 | 相同 |
| `D0->02866E` | 1 | 1 | 相同 |

**总量**：工作区 **142** 边（call 74 / bcc 48 / jmp 20）→ 重跑 **146** 边（call **72** / bcc **52** / jmp **22**）。
⇒ 其余 11 组**逐边完全相同**，差异**只**集中在 `0x40` 组。

### 2.4 `f_*.asm` 逐文件比对：11/12 相同，1 个孤儿

| 文件 | 重跑 vs 工作区 |
|---|---|
| `f_027F24.asm` / `f_028648.asm` / `f_02866E.asm` / `f_028722.asm` / `f_02AEAA.asm` / `f_02B98A.asm` / `f_02BA24.asm` / `f_02BBAE.asm` / `f_02CB66.asm` / `f_035598.asm` / `f_03A3D4.asm` | **逐字节相同** |
| `f_02AAAE.asm` | **工作区独有**，重跑不再生成（修正前的错址产物） |

⇒ 修正后的 `dis_all.py` 应生成 **11 份** `f_*.asm`（TARGETS 12 条 → 唯一入口 11 个，`0x80`/`0x00` 共用 `0x028722`）。
工作区现有 **12 份**，多出的正是那个孤儿 `f_02AAAE.asm`。

**重要**：`f_02AEAA.asm`（工作区版）与重跑版**逐字节相同** → 20:46 那份单独补的产物本来就是对的，与 `dis_all.py` 修正后的输出一致。两处不存在冲突。

---

## 3. 为什么会出现「只改键名不改内容」

追查到两处相关代码：

### 3.1 `03_analysis\_pkgtool\build_package.py` 的 `_fix_edges()`（第 501–565 行）

```python
def _fix_edges(dst_root):
    """用 ROM 实测真值校验并修正包内 edges.json 的作业表键值。"""
    ...
    for k in list(e.keys()):
        kn, fn = k.split('->', 1)
        t2 = truth.get(kn)
        if t2 and t2 != fn:
            fixed.append((k, '%s->%s' % (kn, t2)))
            e['%s->%s' % (kn, t2)] = e.pop(k)     # ★ 只换键名，不重算该组的边
```

它做的是**键名映射**（`40->02AAAE` → `40->02AEAA`），**不重新走查该函数**，所以搬过去的 9 条边仍是 `0x02AAAE` 的。
（该函数作用于**打包输出目录** `dst_root/07_data/edges.json`，本身是合理设计——打包时统一改键名。但若把这个改法直接套用到工作区源文件，就会产生本文档记录的名实不符状态。）

**判别依据**：当前工作区 `edges.json` **不含** `_note` / `_corrections` 字段（`_fix_edges` 会写入这两个），故工作区文件**不是**由 `_fix_edges` 产生的；它是**被另一处改动直接改了键名**。无论来源如何，**结果一样：键名对、内容错**。

### 3.2 `dis_all.py` 的修正（已生效，00:31）

```python
# R5 更正：0x40 项原记 0x02AAAE，末两字节错位（AE AA → AA AE）。
#   此处保留修正值，使重跑产出的 edges.json 与 ROM 实测一致。
TARGETS = [
    (0x10, 0x35598), (0x40, 0x2AEAA), ...
]
```
**源头已修好**。任何现在重跑 `dis_all.py` 的人都会得到正确的 146 边 / 13 边的 `40->02AEAA` 组。

---

## 4. 建议的修正动作（按影响面排序）

### 方案 A（推荐）：重跑 `dis_all.py` 重新生成工作区产物

```bash
cd LS8000/03_analysis/firmware/_jobfuncs
python dis_all.py        # 只读 D:\，产物写本目录
```
- `edges.json` → 146 边，`40->02AEAA` = 13 边（正确内容）
- 11 份 `f_*.asm` → 逐字节与现有相同（**不会覆盖出差异**，已实测）
- 唯一副作用：`f_02AAAE.asm` 成为孤儿，需另作处置（见下）

### 方案 B：只替换 `edges.json` 的那一个组

用 `_verify\regen\edges.json`（重跑产物）替换工作区 `edges.json`，或仅取其 `40->02AEAA` 组替换旧组。
- 风险更低（不动 f_*.asm），但 `edges.json` 会与「重跑 dis_all.py 的结果」不完全同源

### 孤儿文件 `f_02AAAE.asm` 的处置（三选一）

| 选项 | 说明 |
|---|---|
| **删除** | 它是修正前的错址产物，`dis_all.py` 不再生成，且内容是函数中间段（入口 `extu.w r1`，非序言）。删除后 `f_*.asm` 回到 11 份 = TARGETS 唯一入口数，**自洽** |
| **保留但标注** | 移到 `_deprecated/` 之类，并在文件名或旁注标明「错址产物，已被 `f_02AEAA.asm` 取代」 |
| **原地保留不动** | 现状。风险：下游按 `f_*.asm` 数量对齐 TARGETS 时会多算 1 份，且可能误取到错址内容 |

**我的倾向：删除或移到标注目录。** 理由——它没有任何独有信息（正确版本 `f_02AEAA.asm` 已完整覆盖，且逐字节可从重跑复现），留着只会让「`f_*.asm` 份数」这一统计口径持续失真（我先前报给 fw-reports 的「12 份」正是因此而来——**我那个数字需要按此更正为「12 份，其中 1 份是孤儿，修正后应为 11 份」**）。

---

## 5. 对 fw-reports 已发布内容的影响

fw-reports 已把 `FW_DOC_INDEX.md` 按「旧版 142 边 / 正确应为 146 边」改写，方向正确。但有两处需要随本次修正微调：

| fw-reports 现在的表述 | 需改为 |
|---|---|
| 「`edges.json`（13,803 B）\| 12 组处理函数控制流边。⚠️ **旧版 142 边**，其中 `0x40` 组用错址 `40->02AAAE`（9 边）；**正确应为 146 边**，新组 `40->02AEAA` = 62 指令 / 13 边」 | 工作区文件**键名已是 `40->02AEAA`**（00:32 改的），但**组内 9 条边仍是 `0x02AAAE` 残留** → 应描述为「**键名已更正、组内容待重生成**」，而非「用错址 `40->02AAAE`」 |
| §2.1「`f_*.asm`（**12 份**）」 | 「**12 份，其中 `f_02AAAE.asm` 为错址孤儿产物；`dis_all.py` 修正后应生成 11 份**」 |

---

## 6. 复现方式

```bash
cd LS8000/03_analysis/status/_verify/regen
cp ../../../firmware/_jobfuncs/{dis_all.py,h8fix.py} .
python dis_all.py          # 生成 146 边的 edges.json + 11 份 f_*.asm
python - <<'EOF'
import json,collections
new=json.load(open('edges.json')); old=json.load(open('../../../firmware/_jobfuncs/edges.json'))
print('工作区', sum(len(v) for v in old.values()), '重跑', sum(len(v) for v in new.values()))
for g in sorted(new):
    if old.get(g)!=new[g]: print('★不同', g, len(old.get(g,[])), '->', len(new[g]))
EOF
```
