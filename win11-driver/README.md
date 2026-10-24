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
