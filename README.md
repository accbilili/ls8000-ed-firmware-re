# Nikon LS-8000 ED 固件逆向 · 工具链与分析记录

**Nikon LS-8000 ED Firmware Reverse Engineering — Toolkit & Analysis Notes**

![CI](https://github.com/accbilili/ls8000-ed-firmware-re/actions/workflows/ci.yml/badge.svg)
![Files](https://img.shields.io/badge/files-725-blue)
![Size](https://img.shields.io/badge/size-12.9MB-blue)
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

### 关于作者：我是新手，这是 AI 辅助的产物 / About the author: a beginner, AI-assisted

> **中文**  
>
> 这个仓库里**几乎没有一行代码是我"从零写出来"的**。全部内容是在 **AI 助手辅助**下完成的——  
> 方式是**一轮一轮提问 → AI 给出假设 → 我用脚本/模拟器去跑 → 推翻 → 再提问**，这样迭代累积出来的。  
> 中间经历了 **25 轮较大的修正（R1–R25）**，其中还包括几次**自我推翻**已写进文档的结论。
>
> 所以我请你：**把这里的所有结论当作"待验证的线索"，而不是"权威结论"**。真正能站住脚的，  
> 是那些能被脚本重复跑出来、且脚本就在本仓库里的部分。
>
> **English**  
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

| 结论 / Conclusion | 人工/AI 推导的版本 / Hand- or AI-derived | 模拟器实跑的正确答案 / Simulator-executed |
| --- | --- | --- |
| `er3`（校验对象 / checksum target） | payload[1..8] 重排相加 ❌<br>payload[1..8] rearranged and summed ❌ | **`BE32(payload[1..4])`** ✅ |
| 四条 `shll.l #2` 的位移量 / shift amount of the four `shll.l #2` | 以为是左移 16 位 ❌<br>thought to be a left shift of 16 ❌ | **实为左移 8 位（2 位 ×4）** ✅<br>**actually a left shift of 8 (2 bits × 4)** ✅ |
| `@(0x2,er6)` 的含义 / meaning of `@(0x2,er6)` | 以为是 payload[1] ❌<br>thought to be payload[1] ❌ | **实为 payload[2]**（下标基准不同）✅<br>**actually payload[2]** (different index base) ✅ |

复现方法只需一行 / Reproduction takes one line:

```bash
python tools/sim_verify_formulas.py
```

> 这也是本项目最想留下的经验：**凡是涉及位段、移位、字节序的结论，永远不要用推导，用模拟执行。**
> 因为推理链条上任何一层出错，结果看起来仍然自洽——它不会报错，只会静静地错。
>
> The lesson this project most wants to leave behind: **for any conclusion involving bit fields, shifts or byte
> order, never derive it — execute it in a simulator.** Because if any link in the reasoning chain is wrong,
> the result still looks self-consistent: it raises no error, it is simply and quietly wrong.

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
> `samples/` includes the firmware update package that Nikon publicly released, together with the ROM image
> inside it — that is, the very installer Nikon shipped for users to update their scanner firmware
> (Ver. 1.11, released 2002-12-26). This is not a leak and does not come from any internal channel;
> its provenance is verified by a **three-layer reproducible method** that anyone can re-check —
> see [`samples/SOURCES.md`](samples/SOURCES.md).
>
> 分析本体仍以纯文本为主：`.md` / `.py` / `.asm` / `.txt` / `.json` / `.csv` / `.ps1`。
> 本仓库**不涉及**任何需登录、付费或非公开渠道才能取得的固件。
>
> The analysis itself remains mostly plain text: `.md` / `.py` / `.asm` / `.txt` / `.json` / `.csv` / `.ps1`.
> This repository **does not involve** any firmware that requires a login, a payment, or a non-public
> channel to obtain.
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

| # | 产出 / Deliverable | 说明 / Notes |
| - | --- | --- |
| 1 | **H8 反汇编工具链** / **H8 disassembly toolchain**<br>`h8dis` / `h8tab` / `h8sim` | 纯 Python，无第三方依赖，零 `ctypes`/`struct`<br>Pure Python, no third-party dependencies, no `ctypes`/`struct` |
| 2 | **解码器缺陷的量化修复** / **Quantified fix of a decoder defect** | 原版指令表 393 项 → 修复版 399 项；全 ROM 多检出 **211 处** 此前不可解的 `mov.l`（均为 size=10）<br>Original instruction table 393 entries → fixed 399; **211** previously undecodable `mov.l` (all size=10) newly decoded across the whole ROM |
| 3 | **指令级模拟器** / **Instruction-level simulator** | 可执行真实指令读出寄存器值——本项目最重要的纠错手段<br>Executes real instructions and reads out register values — the most important error-correction tool in this project |
| 4 | **200 个带洞函数的递归复走** / **Recursive re-walk of 200 holed functions** | 36 个带洞函数额外解出 **1,299 条**指令<br>36 holed functions yielded an extra **1,299** decoded instructions |
| 5 | **ioctl `0x190012` 的完整判定** / **Complete determination of ioctl `0x190012`** | 穷举 Function×Method×Access 后的**唯一解**：`CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`<br>After exhausting Function×Method×Access: the **unique** solution `CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)` |
| 6 | **25 轮修正的完整记录** / **Full record of 25 correction rounds** | 含 4 次自我推翻——难得的"错误档案"，见 `docs/REPORT_回写总账-20261024.md`<br>Includes 4 self-retractions — a rare "error archive", see `docs/REPORT_回写总账-20261024.md` |
| 7 | **12 组 / 146 条调用边** / **12 groups / 146 call edges** | 由实测而非猜测得出<br>Derived from measurement, not guesswork |
| 8 | ⭐ **Windows 11 驱动适配包** / **Windows 11 driver package**<br>[`win11-driver/`](win11-driver) | LS-8000 ED / 9000 ED 在 Win11 x64 上被正确识别；不含任何驱动二进制，INF 仅 1,217 B<br>LS-8000 ED / 9000 ED correctly detected on Win11 x64; contains no driver binaries, the INF is only 1,217 B |

> ⭐ **如果你只想要一件能直接用的东西**：看 [`win11-driver/`](win11-driver)。
> 其余部分是逆向分析记录，主要用于研究与参考。
>
> 🔍 好奇它为什么只用了 **1,217 字节**就能管用？
> 见下方「**Windows 11 驱动适配包**」一节中的「**精妙之处**」：
> 没有写一行内核代码，也没有关签名强制——它只是把路让开了。
>
> If you only want one immediately usable thing: see [`win11-driver/`](win11-driver).
> Everything else is reverse-engineering notes, mainly for study and reference.
>
> 🔍 Curious why **1,217 bytes** is enough? See "**Why 1,217 bytes is enough**" inside the
> **Windows 11 driver package** section below: no kernel code was written and signature
> enforcement was never disabled — it just stepped out of the way.

**这不是 / What this is NOT**

- ❌ 不是官方产物：与 Nikon 无关联，未获授权（见 [`NOTICE`](NOTICE)）<br>Not an official product: no affiliation with Nikon, no authorization (see [`NOTICE`](NOTICE))
- ❌ 不是可用替代品：没有开源驱动、不能替代官方软件、不提供可刷写镜像<br>Not a working replacement: no open-source driver, does not substitute for the vendor software, ships no flashable image
- ❌ 不是完整逆向：结论覆盖 ROM 的一小部分，大量区域仍未分析<br>Not a complete reverse-engineering: the conclusions cover only a small part of the ROM, large regions remain unanalyzed
- ❌ 不是权威资料：见开头关于作者能力与 AI 辅助的说明<br>Not an authoritative source: see the note at the top about the author's ability and AI assistance
- ⚠️ `samples/other/` 下的 LS-2000 等**其它机型**固件仅供格式交叉参考，与本项目主题无关<br>Firmware of **other models** (LS-2000 etc.) under `samples/other/` is kept only for format cross-reference and is unrelated to this project

> 关于样本完整性 On sample integrity：`samples/` 收录的是**完整未改动的官方发布原件**，  
> 而非改造过的或来源不明的镜像。所有文件的 SHA256 均登记在 `MANIFEST.txt`，  
> 可用 `python tools/verify_package.py` 一键核对是否被改动。  
> The samples are complete, unmodified official originals — not altered or  
> unattributable dumps. Every SHA256 is recorded in MANIFEST.txt.

---

## 🔧 Windows 11 驱动适配包（LS-8000 ED / LS-9000 ED） / Windows 11 x64 driver package

> 本节内容与独立文件 [`win11-driver/README.md`](win11-driver/README.md) 一致；文中出现的相对路径均相对于 `win11-driver/` 目录。
> This section mirrors [`win11-driver/README.md`](win11-driver/README.md); relative paths below are relative to `win11-driver/`.

**让你那台画质很棒的老扫描仪，在现代 Windows 上被正确识别。**

> 适用：Nikon SUPER COOLSCAN **8000 ED** 与 **9000 ED**
> 平台：Windows 11 x64（Intel/AMD）
> 连接：IEEE 1394 / FireWire（需要电脑本身有可用的 1394 控制器）
> 版本：本地安装包 1.0 · 制作 2026-10-04

---

### 驱动包是什么 / What the package is

一个**本地设备绑定包**。它做的事情很单纯：

> 把 Nikon 原厂 INF 里的**硬件 ID**，绑定到 **Windows 自带的 `sti.inf`**（微软已签名的 SBP2/静态图像堆栈）上。

```
SBP2\NIKON___&LS-8000_ED______&CMDSETID104D8   ──┐
                                                  ├─→  Windows 自带 sti.inf
SBP2\NIKON___&LS-9000_ED______&CMDSETID104D8   ──┘     (STI.SBP2Section)
```

**关键点：本包不包含任何驱动二进制。**

内核驱动由 Windows 自带的 `scsiscan.sys` 提供，使用的是**微软自己的签名**。
本包只是告诉 Windows："遇到这个硬件 ID，请用你自带的那个驱动。"

这就是为什么整个 INF 只有 **1,217 字节** —— 没有改动任何一行驱动代码。

It contains **no driver binaries**. The kernel driver is supplied by Windows itself
(`scsiscan.sys`), already signed by Microsoft. The package merely binds Nikon's
hardware IDs to it. That is why the INF is only **1,217 bytes**.

---

### 目录内容 / Contents

| 文件 | 大小 | 说明 |
|---|---:|---|
| `使用说明.txt` | 4,654 B | 完整中文说明（建议先读它） |
| `安装.cmd` | 262 B | 安装入口，自动请求管理员权限 |
| `卸载.cmd` | 266 B | 卸载入口 |
| `Setup.ps1` | 10,406 B | 安装/卸载主脚本 |
| `Driver/Nikon8000-9000-x64.inf` | 1,217 B | 驱动 INF（含硬件 ID 绑定） |
| `Driver/Nikon8000-9000-x64.cat` | 1,838 B | 目录文件（CAT 签名） |
| `Nikon8000-9000-LocalSigner.cer` | 824 B | **本地自签**代码签名证书（仅公钥） |
| `SHA256SUMS.txt` | 782 B | 包内文件校验值 |
| `签名信息.json` | 292 B | 证书指纹与有效期 |
| `核对结果.json` | 950 B | 制作时的自校验记录 |

---

### 安装步骤 / Install

1. **把整个 ZIP 解压**到一个可写目录（如桌面）。**不要在压缩包内直接运行**
2. 接好扫描仪、打开电源（也可以先装驱动再接设备）
3. 双击 **`安装.cmd`**，UAC 提示时点"是"
4. 等待结果。**问题代码 0** 表示设备已正常启动
5. 打开 Nikon Scan 核对预览与扫描

安装后会在设备管理器中显示为：

```
Nikon SUPER COOLSCAN 8000 ED
Nikon SUPER COOLSCAN 9000 ED
```

**卸载**：双击 `卸载.cmd`，它会按 INF 名称查询实际的 `oem*.inf` 发布名再移除，
并一并清理本包添加的两份公共信任证书。

---

### ⚠️ 安装前必须知道的三件事

#### 1. 会向本机证书存储添加根证书

因为 INF 被修改过，Windows 需要一个能验证它的签名。本包带一枚**本地自签证书**，
安装时会加入本机的「受信任的根证书颁发机构」和「受信任的发布者」存储区：

```
证书名称 Subject   : CN=Local Nikon 8000 ED 9000 ED INF Package
指纹 Thumbprint    : 17124401603110A5F91704BB536493C0BE336944
有效期 Validity    : 2026-10-04 → 2031-10-04
私钥是否随包提供    : 否（制作完成后即删除）
```

这是 Windows 驱动本地自签名的标准做法，但你要知道这是一次**本机安全区域的变更**。
卸载脚本会把证书一并移除。

#### 2. 不做这些事（有意不为）

- 不修改 BCD、不启用测试模式（testsigning）
- 不关闭驱动签名强制
- 不下载任何外部组件
- 不改动 1394 控制器本身的驱动

安装程序只调用 Windows 自带的 PowerShell、PnPUtil 与 Image Scan 相关接口。

#### 3. 每台机器环境不同，**不保证都能成功**

作者原话：「因为每台电脑的环境不同，不能保证每台电脑都能完美兼容。」

已知限制（摘录自 `使用说明.txt` 第六节，原文更详细）：

| 项目 | 状态 |
|---|---|
| LS-8000 ED 设备可正常启动、问题代码 0 | ✅ 已验证 |
| LS-9000 ED | ⚠️ 硬件 ID 已与原厂核对，**尚未真机验证** |
| STI / USD 应用集成（原厂 32 位 `NKScnUSD.dll`、COM 注册） | ❌ 本包未包含，需另行验证 |
| WIA、其它扫描软件、Nikon Scan 的全部功能 | ❌ 不能声称已全部可用 |
| Nikon Scan.exe / LS9000.md3 的访问冲突 | ❌ 本包未解决应用层崩溃 |

> **设备管理器显示正常 ≠ 扫描、保存、色彩处理全流程都已通过。**
> A working device node does not mean the whole scanning pipeline works.

---

### 🔍 精妙之处：这 1,217 字节为什么管用 / Why 1,217 bytes is enough

#### 一句话 / In one sentence

> 原厂驱动想让 Nikon 自己的代码接管这台扫描仪。
> 这个包反其道而行——**它承认 Windows 早就知道怎么跟这台扫描仪说话，然后把路让开。**
>
> The vendor INF tries to put Nikon's own code in charge. This package does the opposite:
> it recognises that Windows already knows how to talk to this scanner, and steps aside.

---

#### ① 关键洞察：1394 扫描仪在 Windows 里本来就是"伪装成 SCSI"的

这是整个方案能成立的**根本原因**，也是最反直觉的一点。

```
扫描仪硬件
   │
   ↓  IEEE 1394 线缆
1394 控制器驱动
   │
   ↓
sbp2port.sys     ← 微软提供。SBP-2 协议，把 1394 设备"伪装"成 SCSI 设备
   │                （SBP2 = Serial Bus Protocol 2，即 SCSI-over-1394）
   ↓
scsiscan.sys     ← 微软提供、微软签名。静态图像扫描仪驱动，发标准 SCSI 命令
   │
   ↓
STI / WIA        ← Windows 的扫描仪 API
```

**实证**：在 Windows 11 自带的 `sti.inf` 里，`STI.SBP2Section` 与 `STI.SCSISection`
的内容**逐字相同**——两者都只有一行
`AddService = scsiscan, 0x00000002, STI.ScsiScan.AddService`。

这意味着：**微软自己就没有为 1394 扫描仪写过专门的驱动。**
因为 SBP-2 已经在下一层把 1394 翻译成 SCSI 了，上层用同一个 `scsiscan.sys` 就够了。

所以 Nikon 那份 2003 年的 INF 真正缺的，
不是一个"能在 Windows 11 上运行的驱动"，而是**一句把这条路指出来的话**。

Evidence: in Windows 11's own `sti.inf`, `STI.SBP2Section` and `STI.SCSISection` are
**identical** — both contain only
`AddService = scsiscan, 0x00000002, STI.ScsiScan.AddService`. Microsoft never wrote a
1394-specific scanner driver, because SBP-2 already translates 1394 into SCSI one layer
down. What Nikon's 2003 INF lacked was not a working driver — it was the one line
pointing Windows at the road that was already there.

---

#### ② 绕开签名强制的正确姿势：不签驱动，只签"一句话"

Windows 11 x64 的驱动签名强制（Driver Signature Enforcement）是老硬件复活的最大障碍。
常见的"解决办法"本质是**降低系统安全性**：开测试模式、改 BCD、利用过期签名漏洞。

这个包一样都没做。原因很巧妙——

| 需要签名的东西 / What needs signing | 门槛 / The bar | 本包的做法 / What this package does |
|---|---|---|
| 内核驱动代码（`.sys`） | 必须是有效的微软/WHQL 签名 | **一个字节都没有**——直接用 Windows 自带的 |
| 安装指令（`.inf`） | 可由本机信任的发布者签名 | 本地自签证书 + CAT 目录文件 |

**没有内核代码，签名强制就无从谈起。**

需要签名的只是一个 1,217 字节的文本文件，而 INF 级签名的门槛完全不同：
一枚本地自签证书、一个 CAT 目录文件、把公钥导入本机
「受信任的根证书颁发机构」+「受信任的发布者」两个存储区即可。

而且**私钥不随包分发**（`PrivateKeyIncluded: false`，签完即删）——
拿到这个包的人，无法用这枚证书去签别的东西。

With no kernel code, signature enforcement has nothing to bite on. All that needs signing
is a 1,217-byte text file, and INF-level signing has an entirely different bar: one local
self-signed certificate, one catalog file, and the public key imported into the machine's
Root + Trusted Publisher stores. The private key is never shipped
(`PrivateKeyIncluded: false`, deleted after signing), so nobody can reuse it.

---

#### ③ 硬件 ID 一个字符都不改

```
SBP2\NIKON___&LS-8000_ED______&CMDSETID104D8
```

这串 ID 逐字符抄自 Nikon Scan 4.0.3 的 `Nks1394.INF`。
注意那些下划线——它们是 SBP-2 ID 里的**空格填充**（`NIKON___` = "NIKON" + 3 个空格）。

关键在于：**这个 ID 是 Windows 自己的 1394 栈枚举出来的，不是 Nikon 上报的。**
只要 1394 控制器还在工作，Windows 每次开机都会生成这个 ID 去找驱动。
我们只是在那个位置上换了一个答案——**扫描仪自己完全不知道发生了什么。**

The ID is copied character-for-character from Nikon Scan 4.0.3's `Nks1394.INF`. Note the
underscores: they are SBP-2 **space padding** (`NIKON___` = "NIKON" + 3 spaces). Crucially,
this ID is enumerated by Windows' own 1394 stack, not declared by Nikon. As long as the
controller works, Windows regenerates this ID at every boot and goes looking for a driver.
We only changed the answer it finds — the scanner itself is entirely unaware.

---

#### ④ 真正的工作量在"删"，不在"加"

原厂 `Nks1394.INF` 写于 2003 年，它依赖的好几套机制在 Windows 11 上**已经不存在了**。
所以问题从来不是"改一个开关"，而是整条路径都断了。

| 原厂 INF（2003）/ Vendor INF (2003) | 在 Windows 11 上的下场 / Fate on Windows 11 | 本包的处理 / How this package handles it |
|---|---|---|
| `Signature="$CHICAGO$"` | Windows 9x/ME 遗留写法，NT 系不接受 | 改为 `$Windows NT$` |
| `DriverVer=02/03/2003` + `nks1394.cat` | 2003 年的签名，证书早已过期 | 新 CAT，本地自签，有效期至 2031 |
| `HKR,,DevLoader,,*NTKERN` | Windows 2000/XP 遗留机制，已移除 | **删除** |
| `HKR,,NTMPDriver,,"scsiscan.sys"` | 同上 | **删除**（改由 `sti.inf` 的 AddService 提供） |
| `CopyFiles` 从 "Nikon Scan 4 CD-ROM" 拷 `NKSCNUSD.dll` | 要求原安装盘位于正确路径 | **删除** |
| `USDClass` + HKCR 的 COM 注册（32 位 STI USD） | 32 位 COM 组件在 x64 下的兼容问题 | **删除** |
| `[Manufacturer]` 无平台限定 | 任何架构/系统版本都会尝试匹配 | 限定 `NTamd64.10.0...22000` |

最后**只保留了两条**注册表项：

```ini
[NK1394SCN.AddReg]
HKR,,HardwareConfig,1,2          ; 告诉 STI：这是台扫描仪
HKR,DeviceData,ICMProfile,1,0,0  ; 不做色彩配置文件注入
```

> **加上去的只有"绑定"这一件事；删掉的，才是让它活过来的原因。**
>
> What was added is one thing — the binding. What was **removed** is why it works.

---

#### ⑤ 安装脚本不是"点下一步"，是闭环验证

`Setup.ps1` 有几处很讲究的处理：

- **装之前**：硬编码校验证书指纹（`1712…6944`）防掉包；`Test-FileCatalog` 校验
  INF 与 CAT 的哈希一致，确认 INF 没被改过
- **装**：导入证书到 Root + TrustedPublisher 两个存储；`pnputil /add-driver /install`
- **装之后**：回读设备的**真实状态**——用 `Get-PnpDevice` 过滤
  `SBP2\NIKON___&LS-(8000|9000)_ED_`，读取 `DEVPKEY_Device_ProblemCode`
  与 `DEVPKEY_Device_DriverInfPath`，再比对 `UsingThisPackage`，
  确认设备**确实在用本包**，而没有被系统里别的驱动抢走
- **判定标准**是"设备起来了"，不是"命令返回 0"
- 识别退出码 `3010`（需重启）但**绝不自动重启**，只提示
- **卸载**：按实际的 `oem*.inf` 发布名精确卸载，并把两份证书一起删掉——
  不留永久的信任垃圾
- 脚本自身带 Authenticode 签名块；非管理员时自动请求 UAC 提权并回传真实退出码

It validates the certificate thumbprint and `Test-FileCatalog` **before** installing, and
reads back `DEVPKEY_Device_ProblemCode` / `DriverInfPath` **after** installing, confirming
`UsingThisPackage` so a competing driver can't silently win. Success means "the device
came up", not "the command returned 0".

---

#### ⑥ 但作用域是"设备绑定"，不是整个扫描流程

技术在这一点上很干净，也必须把边界说清楚：
**设备管理器里显示正常，不等于扫描、保存、色彩处理全流程都已通过。**
原厂 32 位的 `NKScnUSD.dll`（STI/USD 应用层集成）本包并未包含。

A device node that starts correctly does **not** mean the full scan/save/colour pipeline
works. The vendor's 32-bit `NKScnUSD.dll` (STI/USD application integration) is not included.

---

### 原理依据 / References

本方案所依据的技术点均为 Microsoft 官方文档：

- 硬件 ID 来源：Nikon Scan 4.0.3 原厂 `Nks1394.INF` 中的 LS-8000/LS-9000 条目
- Windows 安装段：本机 `sti.inf` 的 `STI.SBP2Section` 及其 Services 段
- INF 平台声明：<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/inf-manufacturer-section>
- PnPUtil 命令语法：<https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax>
- 受信任发布者存储：<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/trusted-publishers-certificate-store>

INF 文件头部注释原文：

```
; Local Windows 11 x64 binding for Nikon SUPER COOLSCAN 8000 ED / 9000 ED.
; Hardware IDs are taken from Nikon Scan 4.0.3 Nks1394.INF.
; The kernel driver is supplied and signed by Microsoft through sti.inf.
```

---

### 完整性核验 / Verify

包自带的 `SHA256SUMS.txt` 可用于确认文件未被改动：

```bash
cd win11-driver && sha256sum -c SHA256SUMS.txt
```

本仓库亦已用该清单核验通过（9/9 一致）。
此外每个文件的 SHA256 也登记在仓库根目录的 `MANIFEST.txt`。

---

### 许可与责任 / License

- 本目录内容遵循仓库整体的 **GPL-3.0**（脚本）与 **CC BY-SA 4.0**（文档）
- 它**不是** Nikon 发布的官方驱动；Nikon 不对本包负责，本包也未对其做任何修改或反向工程
- 作者为爱好者而非专业驱动开发者，**请在理解上述风险的前提下自行决定是否使用**
- 完整免责声明见仓库根目录 [`DISCLAIMER.md`](DISCLAIMER.md)

> 若你在某台机器上验证成功或失败，欢迎回来提 Issue 记录机型与环境。
> 这类"哪台机器能跑 / 哪台不能"的一手数据，对后来的人非常有价值。

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
| **`samples/`**         | **28** | **固件样本 + 官方安装包原件** | **Firmware samples + official updater** |

`samples/` 结构 / layout：

```
samples/
├── LS8000_111_ROM.bin            228,345 B  ← 逆向主对象（Ver. 1.11）/ main RE target (Ver. 1.11)
├── LS8000_bootblock.bin           65,536 B  引导块 / boot block
├── LS8000_full_512K.bin          524,288 B  整机全镜像 / whole-device image
├── FIRMDATA.bin                   99,865 B  updater 内嵌资源 / resource embedded in the updater
├── decoded.bin                   228,345 B  与 ROM 同哈希（历史命名）/ same hash as the ROM (legacy name)
├── SOURCES.md                               来源证明与三层验证方法 / provenance proof & 3-layer verification
├── official_package/                        官方发布包原件（逐字节未改动）/ official release package (byte-for-byte unmodified)
│   ├── SUPERCOOLSCAN8000ED_111.exe 196,608 B
│   ├── ReadMe.txt                    2,389 B
│   └── LS8000fw111.pdf             47,659 B
├── driver/                              6 件 Windows 驱动组件 / 6 Windows driver components
└── other/                              13 件 其它机型与更新工具 / 13 other-model firmwares & update tools
```

**核心工具 / Core tools**（`tools/`）

`h8dis.py` 反汇编器 · `h8tab.py` 指令表 · `h8sim.py` 指令级模拟器 · `paths.py` 路径/样本解析 ·
`verify_package.py` 完整性校验 · `verify_decoder_fix.py` 解码器缺陷复现 · `sim_verify_formulas.py` 三公式验证

`h8dis.py` disassembler · `h8tab.py` instruction table · `h8sim.py` instruction-level simulator ·
`paths.py` path/sample resolution · `verify_package.py` integrity check ·
`verify_decoder_fix.py` decoder-defect reproduction · `sim_verify_formulas.py` three-formula verification

### 旧路径对照表 / Legacy path mapping

老文档里提到的 `03_analysis/` 与 `02_analysis/` 是**重组前的目录名**，现已不存在。  
对照如下（首次整理时未同步更新这些引用，属已知遗留问题）：

Old references to `03_analysis/` and `02_analysis/` point to pre-reorganization paths that no longer exist:

| 文档中的旧路径 / Old path in the docs | 现在的位置 / Current location |
| --------------------------- | ------------------------------------------- |
| `03_analysis/status/*.md`   | `03_indexes/*.md`                           |
| `03_analysis/firmware/*.md` | `02_reports/firmware/*.md`                  |
| `02_analysis/*.md`          | `01_docs/*.md` 或 / or `02_reports/firmware/*.md` |

---

## 快速上手 / Quick start

### 前置条件 / Prerequisites

- Python **3.9+**（纯标准库，无需 pip install；已在 64 位 Python 3.13 实测通过）<br>Python **3.9+** (standard library only, no `pip install`; tested on 64-bit Python 3.13)
- **样本已随仓库提供，clone 即可运行** 🎉 —— `samples/` 目录含全部分析用 ROM 镜像与官方安装包原件，来源与校验方法见 [`samples/SOURCES.md`](samples/SOURCES.md)<br>**Samples ship with the repo — just clone and run** 🎉 — `samples/` contains every ROM image used by the analysis plus the official installer originals; see [`samples/SOURCES.md`](samples/SOURCES.md) for provenance and verification

如果你希望改用自己持有的样本（例如别的固件版本），可指向自己的目录：

If you would rather use samples you already have (for example a different firmware version), point to your own directory:

```bash
export LS8000_SAMPLE_ROOT=/path/to/your/samples      # Linux / macOS / Git Bash
$env:LS8000_SAMPLE_ROOT = "D:\path\to\your\samples"  # Windows PowerShell
```

- 用 `samples_manifest.txt` 中的 **SHA256** 核对样本版本是否与分析所用一致（防止张冠李戴）<br>Use the **SHA256** values in `samples_manifest.txt` to confirm your sample version matches the one the analysis used (so versions don't get mixed up)
- 引导脚本见 [`bootstrap.sh`](bootstrap.sh) / [`bootstrap.ps1`](bootstrap.ps1)<br>Bootstrap scripts: [`bootstrap.sh`](bootstrap.sh) / [`bootstrap.ps1`](bootstrap.ps1)

### 复现命令 / Reproduce

```bash
python tools/verify_package.py            # 完整性校验，应输出 全部通过（0 缺失/0 不符/0 未收录）/ integrity check; should print 全部通过 (0 missing / 0 mismatch / 0 unlisted)
python tools/verify_decoder_fix.py        # 解码器缺陷：原版 393 / 修复版 399 / 命中 211 / decoder defect: original 393 / fixed 399 / 211 hits
python tools/sim_verify_formulas.py       # 三公式（模拟器实跑，非人工推导）/ three formulas (simulator-executed, not hand-derived)
python paths.py                           # 自检：SAMPLE_ROOT + 14 个样本是否齐备 / self-test: SAMPLE_ROOT + all 14 samples present
```

> **Windows 用户请注意**：`显示与编码问题只影响实机线的 PowerShell 脚本`。固件分析脚本是纯 Python，
> 64 位下可正常运行。**"必须使用 32 位宿主"的要求仅针对实机线**（x86 驱动指针指针对齐），
> 这一点在早期文档中误写成了全局要求，现已更正。
>
> **Windows users**: display and encoding issues affect **only the PowerShell scripts on the live-hardware
> track**. The firmware analysis scripts are pure Python and run fine under 64-bit. **The "32-bit host
> required" rule applies only to the live track** (x86 driver pointer alignment); early documents wrongly
> stated it as a global requirement — now corrected.

### 三公式速查 / Three formulas (simulator-verified)

测试 payload / Test payload = `11 22 33 44 55 66 77 88 99 AA BB CC DD`

| 目标 / Target | 公式 / Formula | 实测值 / Measured |
| --- | --- | --- |
| `er3` | `BE32(payload[1..4])` | `0x11223344` |
| `0x400408` | `BE32(payload[2..5])` | `0x22334455` |
| `0x40040C` | `(payload[7]<<16) + (payload[8]<<8) + payload[9]` | `0x00778899` |

**请勿重新推导这三条**——早期版本曾把它写成"重排相加"，已被模拟器证伪并撤销（见 R22/R23 → R25）。

**Do not re-derive these three** — an earlier version described it as "rearrange and add", which the simulator disproved; it was withdrawn (see R22/R23 → R25).

---

## 🔴 实机安全须知 / Hardware safety (read before touching `06_live/`)

这一节的严重性**高于**仓库里其它任何内容。

This section is more important than anything else in this repo.

`06_live/` 与 `tools/scripts/live/` 下的 **19 个 PowerShell 脚本会向真实的扫描仪硬件发送原始命令**。
它们是抓取证据用的探针，**不是工具软件**。

The **19 PowerShell scripts** under `06_live/` and `tools/scripts/live/` **send raw commands to real scanner
hardware**. They are probes for collecting evidence, **not utility software**.

```
┌──────────────────────────────────────────────────────────────┐
│  已发生的真实事故 / REAL INCIDENT THAT ALREADY HAPPENED     │
│                                                             │
│  ps_probe6.ps1 曾导致宿主蓝屏：                             │
│  ps_probe6.ps1 caused a BSOD on the host machine:           │
│      0xD1  DRIVER_IRQL_NOT_LESS_OR_EQUAL                    │
│      疑似发生于 sbp2port.sys（IEEE-1394 协议栈）            │
│      probably inside sbp2port.sys (IEEE-1394 stack)         │
│                                                             │
│  根因尚未定位。在此之前，实机命令白名单保持冻结。           │
│  Root cause NOT yet identified → the command whitelist      │
│  remains FROZEN.                                            │
└──────────────────────────────────────────────────────────────┘
```

**冻结中的白名单 / Frozen whitelist**

| 允许 / Allowed | 禁止 / Forbidden |
| --- | --- |
| `INQUIRY` 标准页 0 / `INQUIRY` standard page 0 | 一切 VPD 页 / all VPD pages |
| CDB `12 00 00 00 24 00`（alloc 36 字节 / 36 bytes allocated） | `MODE SENSE` / `READ BUFFER` / `WRITE BUFFER` |
| | `E0` / `E1` 自定义命令 / vendor commands / `TUR` |

**风险分级 / Script risk levels**（每个脚本头部均已标注 / marked in each script's header）

| 级别 / Level | 脚本 / Scripts | 说明 / Notes |
| --- | --- | --- |
| 🟢 LOW | `ps_readonly.ps1` | 唯一相对安全的脚本，`SAFE_ONLY=$true`，仅发 `0x190012`<br>The only relatively safe script; `SAFE_ONLY=$true`, sends only `0x190012` |
| 🟠 MEDIUM | `ps_probe{,2,3,4,5}.ps1` | 中间演进版本，未完整验证<br>Intermediate iterations, not fully validated |
| 🔴 HIGH | `ps_probe6.ps1`、`ps_brute.ps1` | **已知致蓝屏** / 含 `0x190024` 等宽 ioctl 码<br>**Known to cause a BSOD** / contains wide ioctl codes such as `0x190024` |

> 这些脚本按用户要求**原位保留**，未做功能修改，仅追加了醒目的危险说明头。
> 保留它们是为了让证据链完整；**保留 ≠ 推荐运行**。完整说明见 [`DISCLAIMER.md`](DISCLAIMER.md)。
>
> These scripts are kept **in place** as requested, unmodified except for a prominent warning header.
> Keeping them preserves the evidence chain. **Keeping ≠ recommending.** See [`DISCLAIMER.md`](DISCLAIMER.md).

---

## 已知未闭合的问题 / Known open questions

诚实清单——以下**不是结论**，尚未验证：

An honest list — the following are **not conclusions**; they remain unverified:

| # | 问题 / Open question |
|---|---|
| 1 | `er3` 与执行层 `0x400408` 是否逐字节同源——两侧公式已实证，但同源性未闭合<br>Whether `er3` and the execution-layer `0x400408` come from the very same bytes — both formulas are empirically verified, but the shared-source property is not closed |
| 2 | `0x400410` 在某些分支"先拼 16 位再清零"的意图不明<br>The intent of "assemble 16 bits first, then clear" at `0x400410` in some branches is unclear |
| 3 | `0x400408` 的完整业务语义标签未定（已知被多方复用）<br>The full semantic label of `0x400408` is undecided (known to be reused by several callers) |
| 4 | 解析层与执行层是否读取同一份数据，影响 `0x91`/`0x92` 的可达性判断<br>Whether the parsing layer and the execution layer read the same data — this affects the reachability judgement for `0x91`/`0x92` |
| 5 | 扫描几何参数表生成器（`0x03A400–0x03BF00`）未分析<br>The scan geometry parameter-table generator (`0x03A400–0x03BF00`) is unanalyzed |
| 6 | 图像算法三件：参数位域含义、像素搬运路径、gamma/位深转换本体<br>Three image-algorithm items: the meaning of the parameter bit fields, the pixel transfer path, and the gamma/bit-depth conversion itself |

---

## 方法论：踩过的坑 / Methodology lessons

如果这份仓库有什么普适价值，大概是这几条：

If this repository has any generalizable value, it is probably these five:

1. **位段类结论必须用模拟执行验证。** 人工推导要同时追踪「寄存器高低半字 / 字节搬移 / 移位 / 立即数」四层语义，任一层出错都会导致位段分配全错——且这种错误**不会报错**，结果看起来依然自洽，只会静静地错。<br>**Bit-field conclusions must be verified by simulated execution.** Manual derivation has to track four semantic layers at once — register high/low halves, byte moves, shifts, and immediates. An error in any one layer mis-assigns the whole bit field — and it **raises nothing**; the result still looks self-consistent, it is simply and quietly wrong.
2. **同一个坑会反复踩。** 两个独立分析路径都犯了同一个 `<<16` 误判——这是系统性陷阱，不是偶发失误。<br>**The same trap gets stepped in again and again.** Two independent analysis paths both made the same `<<16` misjudgement — a systemic trap, not an occasional slip.
3. **修产物不如修源头。** 曾经只改 `edges.json` 的键名而不重算内容，中间态比一致地错更危险。<br>**Fix the source, not the artifact.** At one point I renamed keys in `edges.json` without recomputing their contents; a half-updated intermediate state is more dangerous than being consistently wrong.
4. **打包是复查的最佳时机。** 一次全量复扫接连查出 5 项问题，其中 3 项是全案级别。<br>**Packaging is the best moment to re-audit.** A single full re-scan turned up 5 issues in a row, 3 of them case-level.
5. **保留错误记录。** R1–R25 的完整修正轨迹，比"干净的结论"更有参考价值。<br>**Keep the record of the mistakes.** The complete R1–R25 correction trail is more useful as a reference than a "clean" conclusion.

详见 `01_docs/REPORT_回写总账-20261024.md` 与 `03_indexes/APPLIED_R24_R25_FIXES.md`。

See `01_docs/REPORT_回写总账-20261024.md` and `03_indexes/APPLIED_R24_R25_FIXES.md`.

---

## 许可证 / License

| 部分 / Part | 许可证 / License | 文件 / File |
|---|---|---|
| **代码**（`tools/` 下的 `.py`、`.ps1`）<br>**Code** (`.py` / `.ps1` under `tools/`) | **GPL-3.0** | [`LICENSE`](LICENSE) |
| **文档**（`.md` / `.txt` / 数据分析记录）<br>**Docs** (`.md` / `.txt` / data-analysis notes) | **CC BY-SA 4.0** | [`LICENSE-DOCS`](LICENSE-DOCS) |
| **Nikon 固件样本**（`samples/` 官方发布包原件）<br>**Nikon firmware samples** (official release package under `samples/`) | 著作权归 Nikon Corporation，**按原始形态收录、不受上述许可证覆盖**<br>Copyright stays with Nikon Corporation; **included verbatim and not covered by the licenses above** | [`NOTICE`](NOTICE) |

> 许可证覆盖的是**我（在 AI 辅助下）撰写的内容**，不覆盖 Nikon 的固件本身——
> `samples/` 中收录的是尼康官方公开发布的固件更新包，逐字节未改动，著作权仍归 Nikon Corporation。见 [`NOTICE`](NOTICE)。
>
> The licenses cover **what I wrote (with AI assistance)**; they do **not** cover Nikon's firmware itself —
> `samples/` contains the firmware update package Nikon publicly released, byte-for-byte unmodified, with
> copyright remaining at Nikon Corporation. See [`NOTICE`](NOTICE).

---

## 致谢 / Acknowledgments

- **AI 助手 / AI assistants**：如开头所述，本项目的绝大部分分析工作是在 AI 辅助下迭代完成的。在此如实标注，避免读者误以为是专业逆向工作。<br>As stated at the top, the vast majority of the analysis here was iterated with AI assistance. Stated plainly so that readers do not mistake it for professional reverse-engineering work.
- **Nikon Corporation**：LS-8000 ED 是一款出色的底片扫描仪。本项目出于学习与保存的目的，希望有助于延长这些二十余年前设备的可用寿命。<br>The LS-8000 ED is an outstanding film scanner. This project exists for study and preservation, in the hope of extending the usable life of these twenty-plus-year-old machines.
- 感谢所有愿意花时间复核、纠正本项目结论的人。请以 ISSUE 形式指出错误，我会更新记录。<br>Thanks to everyone willing to spend time reviewing and correcting the conclusions here. Please report errors via ISSUE and I will update the record.

---

<sub>
本仓库所有地址中的本机路径均已做占位符脱敏（`<HOME>`），如需在你的环境中复现，请替换为实际路径。
All local paths in this repository have been replaced with placeholders (`<HOME>`).
</sub>
