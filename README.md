# Nikon LS-8000 ED 固件逆向 · 工具链与分析记录

**Nikon LS-8000 ED Firmware Reverse Engineering — Toolkit & Analysis Notes**

![CI](https://github.com/accbilili/ls8000-ed-firmware-re/actions/workflows/ci.yml/badge.svg)
![Files](https://img.shields.io/badge/files-725-blue)
![Size](https://img.shields.io/badge/size-13.0MB-blue)
![Win11 driver](https://img.shields.io/badge/Win11%20driver-included-green)
![Samples](https://img.shields.io/badge/samples-included-green)
![Provenance](https://img.shields.io/badge/provenance-official%20Nikon%20updater-brightgreen)
![License](https://img.shields.io/badge/code-GPL--3.0-blue)
![Docs](https://img.shields.io/badge/docs-CC%20BY--SA%204.0-lightgrey)
![Status](https://img.shields.io/badge/status-personal%20study-orange)

---

## 📖 这一切是怎么开始的 / How this started

我只是个普通的电脑爱好者和胶片爱好者，**两样都很一般**。

前阵子偶然淘到一台 Nikon SUPER COOLSCAN 8000 ED。
它的画质真的很棒——这是我最在意的一点。唯一的问题是：**在 Windows 11 上用起来非常痛苦。**

后来 AI 浪潮起来了，我就萌生了一个念头：**能不能用 AI 把这套老软件的兼容性优化一下？**

于是东一榔头西一棒槌地开始折腾。先是拿 Nikon Scan 4 下手，想直接把它改好，
结果失败了——它牵扯到最底层的东西，不是改改表层就能解决的。

就这样跟着 AI 一路往下摸，稀里糊涂地摸到了**固件**这一层。
一轮一轮地问，一轮一轮地试，最后走到了现在这个样子。

## 🌀 但我得说实话：到后来，我迷路了

到了后期，我进入了一种混沌状态。

不知道目标是什么，也不知道该往哪里走。只是跟着 AI 一轮一轮地分析下去——
它给一个方向，我就去跑；跑出结果，又牵出下一个方向。

更难的是，**连 AI 自己好像也迷路了**。对话越来越长，上下文被不断压缩，
它开始重复、遗忘、自相矛盾。两个"人"就这样一起，在一个越走越窄的隧道里打转。

那种感觉，大概就是普通人面对 AI 时的无力感——
你既判断不了它说得对不对，也判断不了自己该不该继续。
到后来，连"知其然而不知其所以然"都算不上：
**我甚至说不清自己到底在做什么，那些十六进制的数字究竟意味着什么。**

所以，这个仓库里的很多东西——**我自己也没有真正理解**。

**整个过程里最成功的一件事**，是给原厂的 1394（FireWire）驱动做了 Windows 11 兼容，
而且**改动很小**——成果就放在 [`win11-driver/`](win11-driver)。
那也是本仓库**最可能对别人有实际用处**的部分。

> ⚠️ 但要说清楚：**每台电脑的环境都不一样，我不保证它在你的机器上也能完美兼容。**
> 请先读 [`win11-driver/README.md`](win11-driver/README.md) 再决定是否使用。

---

I'm just an ordinary computer hobbyist and film shooter — **mediocre at both**.

I picked up a Nikon SUPER COOLSCAN 8000 ED second-hand. The image quality is genuinely
excellent — that's what I cared about. The problem: **getting it to work on Windows 11
was painful.**

Then the AI wave came, and a thought occurred to me: **could I use AI to fix this old
software's compatibility?**

So I started poking around, knocking on one door after another. I went at Nikon Scan 4
first, trying to patch it directly. That failed — it reaches into the low-level layers,
and no surface tweak would do.

Following AI down that rabbit hole, I wandered into the **firmware**. One round of
questions after another, one round of testing after another — and here we are.

## 🌀 But in honesty: later on, I got lost

At some point I slipped into a state of pure confusion.

I no longer knew what the goal was, or which way to go. I just kept going through round
after round of analysis with the AI — it suggested a direction, I ran it; whatever came
out pointed to the next direction.

What made it harder: **the AI itself seemed to get lost too.** The conversation grew
longer, the context kept getting compacted, and it started repeating itself, forgetting
things, contradicting itself. Two "minds" circling together inside a narrowing tunnel.

That feeling is probably what powerlessness looks like for an ordinary person facing AI —
you can't tell whether it's right, and you can't tell whether you should keep going.
In the end it wasn't even a case of "knowing the what but not the why":
**I couldn't say what I was actually doing, or what those hex numbers really meant.**

So — much of what's in this repository, **I do not genuinely understand myself.**

**The single most useful outcome** is a minimal Windows 11 compatibility fix for the
original 1394 (FireWire) driver, in [`win11-driver/`](win11-driver). That directory is
probably the part most likely to actually help someone.

> ⚠️ To be clear: **every machine differs, and I cannot guarantee it works on yours.**
> Read [`win11-driver/README.md`](win11-driver/README.md) before using it.

---

## 📢 请先读完这一段 / Please Read This First

### 关于作者：我是新手，这是 AI 辅助的产物

> **中文**  
> 我必须在一开始就说清楚：**我是逆向工程和编程方面的新手（纯小白）**，对汇编语言、Windows 驱动、  
> 固件体系结构的理解都很浅，**写不了真正的产品级代码**。
>
> 这个仓库里**几乎没有一行代码是我"从零写出来"的**。全部内容是在 **AI 助手辅助**下完成的——  
> 方式是**一轮一轮提问 → AI 给出假设 → 我用脚本/模拟器去跑 → 推翻 → 再提问**，这样迭代累积出来的。  
> 中间经历了 **25 轮较大的修正（R1–R25）**，其中还包括几次**自我推翻**已写进文档的结论。
>
> 所以我请你：**把这里的所有结论当作"待验证的线索"，而不是"权威结论"**。真正能站住脚的，  
> 是那些能被脚本重复跑出来、且脚本就在本仓库里的部分。
>
> **English**  
> I am **not** a professional reverse engineer or programmer. My understanding of assembly,  
> Windows drivers and firmware architecture is shallow, and I cannot write production-grade code.
>
> **Almost no line here was written from scratch by me.** Everything was produced with the assistance of an  
> **AI assistant**, through many rounds of: ask → AI proposes → I run a script/simulator to test →  
> disprove → ask again. The notes record **25 rounds (R1–R25)** of correction, including several  
> instances of **retracting my own previously "confirmed" conclusions**.
>
> **Please treat every conclusion here as a lead to verify, not as established fact.**  
> What is trustworthy is the part you can re-run yourself — and the scripts are here.

### 为什么仍然值得看 / Why it may still be useful

有一件事我认为**不因作者水平而打折**：本项目的关键结论是**用指令级模拟器实跑验证**的，  
而不是靠人（或 AI）通读代码后得出的推理。

这也正好回应了上面那段"迷路"的经历：
**当你无法判断 AI 说得对不对时，唯一能依靠的东西是"可复现"。**
不是去相信谁的分析更可信，而是自己跑一遍脚本，让机器把答案吐出来。
这正是本仓库坚持把每条关键结论都做成可执行验证的原因——它绕开了"我不懂"这个事实。

Why this survives the author's skill level: the load-bearing conclusions were produced by an  
**instruction-level simulator executing the actual firmware code**, not by anyone reasoning about it.

| 结论                  | 人工/AI 推导的版本          | 模拟器实跑的正确答案                  |
| ------------------- | -------------------- | --------------------------- |
| `er3`（校验对象）         | payload[1..8] 重排相加 ❌ | **`BE32(payload[1..4])`** ✅ |
| 四条 `shll.l #2` 的位移量 | 以为是左移 16 位 ❌         | **实为左移 8 位（2 位 ×4）** ✅      |
| `@(0x2,er6)` 的含义    | 以为是 payload[1] ❌     | **实为 payload[2]**（下标基准不同）✅  |

复现方法只需一行：

```bash
python tools/sim_verify_formulas.py
```

> 这也是本项目最想留下的经验：**凡是涉及位段、移位、字节序的结论，永远不要用推导，用模拟执行。**  
> 因为推理链条上任何一层出错，结果看起来仍然自洽——它不会报错，只会静静地错。

---

## ⚠️ 非官方声明 / Official Disclaimer

> **本仓库是非官方的个人学习项目，与 Nikon Corporation 没有任何关联，未获得其授权、支持或背书。**  
> **This is an unofficial personal study project. It is not affiliated with, authorized by,  
> endorsed by, or supported by Nikon Corporation in any way.**
>
> **`samples/` 收录了 Nikon 官方公开发布的固件更新软件包及其中的 ROM 镜像**——  
> 即尼康自己提供给用户、用于升级扫描仪固件的那份安装程序（Ver. 1.11，2002-12-26 发布）。  
> 这不是泄露件或内部渠道，来源已通过**三层可复现方法**验证，  
> 任何人都能自行核实，详见 [`samples/SOURCES.md`](samples/SOURCES.md)。
>
> 分析本体仍以纯文本为主：`.md` / `.py` / `.asm` / `.txt` / `.json` / `.csv` / `.ps1`。  
> 本仓库**不涉及**任何需登录、付费或非公开渠道才能取得的固件。
>
> 详见 [`NOTICE`](NOTICE) 与 [`DISCLAIMER.md`](DISCLAIMER.md)。

---

## 这是什么 / What this is

面向 **Hitachi H8/300H** 单片机的一套静态分析工具链，以及针对 Nikon LS-8000 ED 底片扫描仪固件的  
结构化分析记录。分析对象主要是一个 **228,345 字节的 ROM 镜像**与其 Windows 驱动侧的 ioctl 接口。

A static-analysis toolkit for the **Hitachi H8/300H** MCU, plus structured analysis notes on the firmware  
of the Nikon LS-8000 ED film scanner — primarily a **228,345-byte ROM image** and the Windows driver's  
ioctl surface.

**你会得到 / What you get**

| # | 产出                                        | 说明                                                                                              |
| - | ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1 | **H8 反汇编工具链** `h8dis` / `h8tab` / `h8sim` | 纯 Python，无第三方依赖，零 `ctypes`/`struct`                                                             |
| 2 | **解码器缺陷的量化修复**                            | 原版指令表 393 项 → 修复版 399 项；全 ROM 多检出 **211 处** 此前不可解的 `mov.l`（均为 size=10）                          |
| 3 | **指令级模拟器**                                | 可执行真实指令读出寄存器值——本项目最重要的纠错手段                                                                      |
| 4 | **200 个带洞函数的递归复走**                        | 36 个带洞函数额外解出 **1,299 条**指令                                                                      |
| 5 | **ioctl `0x190012` 的完整判定**                | 穷举 Function×Method×Access 后的**唯一解**：`CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)` |
| 6 | **25 轮修正的完整记录**                           | 含 4 次自我推翻——难得的"错误档案"，见 `docs/REPORT_回写总账-20261024.md`                                           |
| 7 | **12 组 / 146 条调用边**                       | 由实测而非猜测得出                                                                                       |
| 8 | ⭐ **Windows 11 驱动适配包** [`win11-driver/`](win11-driver) | LS-8000 ED / 9000 ED 在 Win11 x64 上被正确识别；不含任何驱动二进制，INF 仅 1,217 B |
> ⭐ **如果你只想要一件能直接用的东西**：看 [`win11-driver/`](win11-driver)。
> 其余部分是逆向分析记录，主要用于研究与参考。
>
> If you only want one immediately usable thing: see [`win11-driver/`](win11-driver).
> Everything else is reverse-engineering notes, mainly for study and reference.

**这不是 / What this is NOT**

- ❌ 不是官方产物：与 Nikon 无关联，未获授权（见 [`NOTICE`](NOTICE)）
- ❌ 不是可用替代品：没有开源驱动、不能替代官方软件、不提供可刷写镜像
- ❌ 不是完整逆向：结论覆盖 ROM 的一小部分，大量区域仍未分析
- ❌ 不是权威资料：见开头关于作者能力与 AI 辅助的说明
- ⚠️ `samples/other/` 下的 LS-2000 等**其它机型**固件仅供格式交叉参考，与本项目主题无关

> 关于样本完整性 On sample integrity：`samples/` 收录的是**完整未改动的官方发布原件**，  
> 而非改造过的或来源不明的镜像。所有文件的 SHA256 均登记在 `MANIFEST.txt`，  
> 可用 `python tools/verify_package.py` 一键核对是否被改动。  
> The samples are complete, unmodified official originals — not altered or  
> unattributable dumps. Every SHA256 is recorded in MANIFEST.txt.

---

## 目录地图 / Repository map

目录保留了原始工作区的编号，以确保与既有文档中的路径引用一致。

Directories keep their original workspace numbering so they match the path references throughout the existing documents.

| 目录                     |     文件 | 内容                 | Contents                                |
| ---------------------- | -----: | ------------------ | --------------------------------------- |
| `01_docs/`             |     14 | 主报告与综述             | Main reports & overviews                |
| `02_reports/firmware/` |     22 | 固件专题报告             | Firmware topic reports                  |
| `02_reports/live/`     |      1 | 实机协议报告             | Live-hardware protocol report           |
| `03_indexes/`          |      9 | 产物索引与裁决记录          | Artifact indexes & verdicts             |
| `04_disasm/jobfuncs/`  |    200 | 按函数拆分的反汇编          | Per-function disassembly                |
| `04_disasm/`           |     10 | 全 ROM 反汇编等         | Whole-ROM disassembly, etc.             |
| `05_hostside/`         |     11 | 主机/驱动侧数据           | Host/driver-side data                   |
| `06_live/`             |     14 | 实机验证脚本 ⚠️          | Live-hardware scripts ⚠️                |
| `07_data/`             |     15 | 统计数据               | Census/statistics data                  |
| `tools/`               |     12 | 核心工具               | Core tools (see below)                  |
| `tools/scripts/`       |    339 | 一次性分析脚本            | One-off analysis scripts                |
| `tools/legacy/`        |     23 | 早期探索脚本             | Early exploratory scripts               |
| **`win11-driver/`**   |     11 | **Win11 驱动适配包（独立）**  | **Win11 driver package (standalone)** |
| **`samples/`**         | **27** | **固件样本 + 官方安装包原件** | **Firmware samples + official updater** |

`samples/` 结构 / layout：

```
samples/
├── LS8000_111_ROM.bin            228,345 B  ← 逆向主对象（Ver. 1.11）
├── LS8000_bootblock.bin           65,536 B  引导块
├── LS8000_full_512K.bin          524,288 B  整机全镜像
├── FIRMDATA.bin                   99,865 B  updater 内嵌资源
├── decoded.bin                   228,345 B  与 ROM 同哈希（历史命名）
├── SOURCES.md                               来源证明与三层验证方法
├── official_package/                        官方发布包原件（逐字节未改动）
│   ├── SUPERCOOLSCAN8000ED_111.exe 196,608 B
│   ├── ReadMe.txt                    2,389 B
│   └── LS8000fw111.pdf             47,659 B
├── driver/                              6 件 Windows 驱动组件
└── other/                              13 件 其它机型与更新工具
```

**核心工具 / Core tools**（`tools/`）

`h8dis.py` 反汇编器 · `h8tab.py` 指令表 · `h8sim.py` 指令级模拟器 · `paths.py` 路径/样本解析 ·  
`verify_package.py` 完整性校验 · `verify_decoder_fix.py` 解码器缺陷复现 · `sim_verify_formulas.py` 三公式验证

### 旧路径对照表 / Legacy path mapping

老文档里提到的 `03_analysis/` 与 `02_analysis/` 是**重组前的目录名**，现已不存在。  
对照如下（首次整理时未同步更新这些引用，属已知遗留问题）：

Old references to `03_analysis/` and `02_analysis/` point to pre-reorganization paths that no longer exist:

| 文档中的旧路径                     | 现在的位置                                       |
| --------------------------- | ------------------------------------------- |
| `03_analysis/status/*.md`   | `03_indexes/*.md`                           |
| `03_analysis/firmware/*.md` | `02_reports/firmware/*.md`                  |
| `02_analysis/*.md`          | `01_docs/*.md` 或 `02_reports/firmware/*.md` |

---

## 快速上手 / Quick start

### 前置条件 / Prerequisites

- Python **3.9+**（纯标准库，无需 pip install；已在 64 位 Python 3.13 实测通过）
- **样本已随仓库提供，clone 即可运行** 🎉 —— `samples/` 目录含全部分析用 ROM 镜像与官方安装包原件，  
  来源与校验方法见 [`samples/SOURCES.md`](samples/SOURCES.md)

Samples ship with the repo — just clone and run. Provenance: `samples/SOURCES.md`.

如果你希望改用自己持有的样本（例如别的固件版本），可指向自己的目录：

```bash
export LS8000_SAMPLE_ROOT=/path/to/your/samples      # Linux / macOS / Git Bash
$env:LS8000_SAMPLE_ROOT = "D:\path\to\your\samples"  # Windows PowerShell
```

- 用 `samples_manifest.txt` 中的 **SHA256** 核对样本版本是否与分析所用一致（防止张冠李戴）
- 引导脚本见 [`bootstrap.sh`](bootstrap.sh) / [`bootstrap.ps1`](bootstrap.ps1)

### 复现命令 / Reproduce

```bash
python tools/verify_package.py            # 完整性校验，应输出 全部通过（0 缺失/0 不符/0 未收录）
python tools/verify_decoder_fix.py        # 解码器缺陷：原版 393 / 修复版 399 / 命中 211
python tools/sim_verify_formulas.py       # 三公式（模拟器实跑，非人工推导）
python paths.py                           # 自检：SAMPLE_ROOT + 14 个样本是否齐备
```

> **Windows 用户请注意**：`显示与编码问题只影响实机线的 PowerShell 脚本`。固件分析脚本是纯 Python，  
> 64 位下可正常运行。**"必须使用 32 位宿主"的要求仅针对实机线**（x86 驱动指针指针对齐），  
> 这一点在早期文档中误写成了全局要求，现已更正。

### 三公式速查 / Three formulas (simulator-verified)

测试 payload = `11 22 33 44 55 66 77 88 99 AA BB CC DD`

| 目标         | 公式                                                | 实测值          |
| ---------- | ------------------------------------------------- | ------------ |
| `er3`      | `BE32(payload[1..4])`                             | `0x11223344` |
| `0x400408` | `BE32(payload[2..5])`                             | `0x22334455` |
| `0x40040C` | `(payload[7]<<16) + (payload[8]<<8) + payload[9]` | `0x00778899` |

**请勿重新推导这三条**——早期版本曾把它写成"重排相加"，已被模拟器证伪并撤销（见 R22/R23 → R25）。

---

## 🔴 实机安全须知 / Hardware safety (read before touching `06_live/`)

这一节的严重性**高于**仓库里其它任何内容。

This section is more important than anything else in this repo.

`06_live/` 与 `tools/scripts/live/` 下的 **19 个 PowerShell 脚本会向真实的扫描仪硬件发送原始命令**。  
它们是抓取证据用的探针，**不是工具软件**。

```
┌───────────────────────────────────────────────────────────────┐
│  已发生的真实事故 / REAL INCIDENT THAT ALREADY HAPPENED        │
│                                                               │
│  ps_probe6.ps1 曾导致宿主蓝屏：                                │
│      0xD1  DRIVER_IRQL_NOT_LESS_OR_EQUAL                      │
│      疑似发生于 sbp2port.sys（IEEE-1394 协议栈）               │
│                                                               │
│  根因尚未定位。在此之前，实机命令白名单保持冻结。               │
│  Root cause NOT yet identified → the command whitelist        │
│  remains FROZEN.                                              │
└───────────────────────────────────────────────────────────────┘
```

**冻结中的白名单 / Frozen whitelist**

| 允许 Allowed                           | 禁止 Forbidden                                  |
| ------------------------------------ | --------------------------------------------- |
| `INQUIRY` 标准页 0                      | 一切 VPD 页                                      |
| CDB `12 00 00 00 24 00`（alloc 36 字节） | `MODE SENSE` / `READ BUFFER` / `WRITE BUFFER` |
|                                      | `E0` / `E1` 自定义命令 / `TUR`                     |

**风险分级 / Script risk levels**（每个脚本头部均已标注）

| 级别        | 脚本                             | 说明                                        |
| --------- | ------------------------------ | ----------------------------------------- |
| 🟢 LOW    | `ps_readonly.ps1`              | 唯一相对安全的脚本，`SAFE_ONLY=$true`，仅发 `0x190012` |
| 🟠 MEDIUM | `ps_probe{,2,3,4,5}.ps1`       | 中间演进版本，未完整验证                              |
| 🔴 HIGH   | `ps_probe6.ps1`、`ps_brute.ps1` | **已知致蓝屏** / 含 `0x190024` 等宽 ioctl 码       |


> 这些脚本按用户要求**原位保留**，未做功能修改，仅追加了醒目的危险说明头。
> 保留它们是为了让证据链完整；**保留 ≠ 推荐运行**。完整说明见 [`DISCLAIMER.md`](DISCLAIMER.md)。
>
> These scripts are kept **in place** as requested, unmodified except for a prominent warning header.
> Keeping them preserves the evidence chain. **Keeping ≠ recommending.** See [`DISCLAIMER.md`](DISCLAIMER.md).

---

## 已知未闭合的问题 / Known open questions

诚实清单——以下**不是结论**，尚未验证：

| # | 问题 |
|---|---|
| 1 | `er3` 与执行层 `0x400408` 是否逐字节同源——两侧公式已实证，但同源性未闭合 |
| 2 | `0x400410` 在某些分支"先拼 16 位再清零"的意图不明 |
| 3 | `0x400408` 的完整业务语义标签未定（已知被多方复用） |
| 4 | 解析层与执行层是否读取同一份数据，影响 `0x91`/`0x92` 的可达性判断 |
| 5 | 扫描几何参数表生成器（`0x03A400–0x03BF00`）未分析 |
| 6 | 图像算法三件：参数位域含义、像素搬运路径、gamma/位深转换本体 |

---

## 方法论：踩过的坑 / Methodology lessons

如果这份仓库有什么普适价值，大概是这几条：

1. **位段类结论必须用模拟执行验证。** 人工推导要同时追踪「寄存器高低半字 / 字节搬移 / 移位 / 立即数」四层语义，任一层出错都会导致位段分配全错——且这种错误**不会报错**，结果看起来依然自洽，只会静静地错。
2. **同一个坑会反复踩。** 两个独立分析路径都犯了同一个 `<<16` 误判——这是系统性陷阱，不是偶发失误。
3. **修产物不如修源头。** 曾经只改 `edges.json` 的键名而不重算内容，中间态比一致地错更危险。
4. **打包是复查的最佳时机。** 一次全量复扫接连查出 5 项问题，其中 3 项是全案级别。
5. **保留错误记录。** R1–R25 的完整修正轨迹，比"干净的结论"更有参考价值。

详见 `01_docs/REPORT_回写总账-20261024.md` 与 `03_indexes/APPLIED_R24_R25_FIXES.md`。

---

## 许可证 / License

| 部分 | 许可证 | 文件 |
|---|---|---|
| **代码**（`tools/` 下的 `.py`、`.ps1`） | **GPL-3.0** | [`LICENSE`](LICENSE) |
| **文档**（`.md` / `.txt` / 数据分析记录） | **CC BY-SA 4.0** | [`LICENSE-DOCS`](LICENSE-DOCS) |
| **底层 Nikon 固件本身** | 著作权归 Nikon Corporation，**不在本仓库、不受上述许可证覆盖** | [`NOTICE`](NOTICE) |

> 许可证覆盖的是**我（在 AI 辅助下）撰写的内容**，
> 不覆盖 Nikon 的固件——本仓库从未包含该固件。见 [`NOTICE`](NOTICE)。

---

## 致谢 / Acknowledgments

- **AI 助手**：如开头所述，本项目的绝大部分分析工作是在 AI 辅助下迭代完成的。
  在此如实标注，避免读者误以为是专业逆向工作。
- **Nikon Corporation**：LS-8000 ED 是一款出色的底片扫描仪。本项目出于学习与保存的目的，
  希望有助于延长这些二十余年前的设备的可用寿命。
- 感谢所有愿意花时间复核、纠正本项目结论的人。请以 ISSUE 形式指出错误，我会更新记录。

---

<sub>
本仓库所有地址中的本机路径均已做占位符脱敏（`<HOME>`），如需在你的环境中复现，请替换为实际路径。
All local paths in this repository have been replaced with placeholders (`<HOME>`).
</sub>
