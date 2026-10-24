# Windows 11 x64 驱动适配包（LS-8000 ED / LS-9000 ED）

**让你那台画质很棒的老扫描仪，在现代 Windows 上被正确识别。**

> 适用：Nikon SUPER COOLSCAN **8000 ED** 与 **9000 ED**
> 平台：Windows 11 x64（Intel/AMD）
> 连接：IEEE 1394 / FireWire（需要电脑本身有可用的 1394 控制器）
> 版本：本地安装包 1.0 · 制作 2026-10-04

---

## 这是什么 / What it is

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

## 目录内容 / Contents

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

## 安装步骤 / Install

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

## ⚠️ 安装前必须知道的三件事

### 1. 会向本机证书存储添加根证书

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

### 2. 不做这些事（有意不为）

- 不修改 BCD、不启用测试模式（testsigning）
- 不关闭驱动签名强制
- 不下载任何外部组件
- 不改动 1394 控制器本身的驱动

安装程序只调用 Windows 自带的 PowerShell、PnPUtil 与 Image Scan 相关接口。

### 3. 每台机器环境不同，**不保证都能成功**

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

## 🔍 精妙之处：这 1,217 字节为什么管用 / Why 1,217 bytes is enough

### 一句话 / In one sentence

> 原厂驱动想让 Nikon 自己的代码接管这台扫描仪。
> 这个包反其道而行——**它承认 Windows 早就知道怎么跟这台扫描仪说话，然后把路让开。**
>
> The vendor INF tries to put Nikon's own code in charge. This package does the opposite:
> it recognises that Windows already knows how to talk to this scanner, and steps aside.

---

### ① 关键洞察：1394 扫描仪在 Windows 里本来就是"伪装成 SCSI"的

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

### ② 绕开签名强制的正确姿势：不签驱动，只签"一句话"

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

### ③ 硬件 ID 一个字符都不改

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

### ④ 真正的工作量在"删"，不在"加"

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

### ⑤ 安装脚本不是"点下一步"，是闭环验证

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

### ⑥ 但作用域是"设备绑定"，不是整个扫描流程

技术在这一点上很干净，也必须把边界说清楚：
**设备管理器里显示正常，不等于扫描、保存、色彩处理全流程都已通过。**
原厂 32 位的 `NKScnUSD.dll`（STI/USD 应用层集成）本包并未包含。

A device node that starts correctly does **not** mean the full scan/save/colour pipeline
works. The vendor's 32-bit `NKScnUSD.dll` (STI/USD application integration) is not included.

---

## 原理依据 / References

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

## 完整性核验 / Verify

包自带的 `SHA256SUMS.txt` 可用于确认文件未被改动：

```bash
sha256sum -c SHA256SUMS.txt
```

本仓库亦已用该清单核验通过（9/9 一致）。
此外每个文件的 SHA256 也登记在仓库根目录的 `MANIFEST.txt`。

---

## 许可与责任 / License

- 本目录内容遵循仓库整体的 **GPL-3.0**（脚本）与 **CC BY-SA 4.0**（文档）
- 它**不是** Nikon 发布的官方驱动；Nikon 不对本包负责，本包也未对其做任何修改或反向工程
- 作者为爱好者而非专业驱动开发者，**请在理解上述风险的前提下自行决定是否使用**
- 完整免责声明见仓库根目录 [`DISCLAIMER.md`](../DISCLAIMER.md)

> 若你在某台机器上验证成功或失败，欢迎回来提 Issue 记录机型与环境。
> 这类"哪台机器能跑 / 哪台不能"的一手数据，对后来的人非常有价值。
