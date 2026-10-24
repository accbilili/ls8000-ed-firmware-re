# 免责声明 / Disclaimer

> **本文件的严重性高于仓库中其它任何内容。**
> **This document outweighs everything else in this repository.**

---

## 1. 总体免责 / General

本仓库按 "**AS IS**"、"**WITH ALL FAULTS**" 提供。作者不对任何内容作出准确性、
完整性、适用性或非侵权性的担保。使用本仓库的**全部风险与后果由使用者自行承担**。

Provided "AS IS" and "WITH ALL FAULTS". The author makes no warranty of accuracy,
completeness, fitness for a particular purpose, or non-infringement.
**You assume all risk and all consequences of use.**

作者是逆向工程与编程方面的新手，几乎所有内容均在 AI 助手辅助下迭代生成（详见 README 开头）。
仓库中的**分析结论可能有错**，请勿将未经验证的内容用于生产、维修或商业决策。

The author is a novice; nearly all content was generated iteratively with AI assistance.
**Analysis conclusions may be wrong.** Do not use unverified content for production,
repair, or business decisions.

---

## 2. 🔴 实机操作风险 / Hardware risk — the important part

`06_live/` 与 `tools/scripts/live/` 下的 **19 个 PowerShell 脚本，会向真实的 Nikon LS-8000 ED
扫描仪硬件发送原始 DeviceIoControl 命令**。

它们是取证用的探针，**不是工具软件**，不具备任何安全保护、**没有 --dry-run 模式**。

The 19 PowerShell scripts under `06_live/` and `tools/scripts/live/` issue raw
DeviceIoControl commands to **a real physical scanner**. They are forensic probes,
**not tools**. They have no safeguards and **no --dry-run mode**.

### 2.1 已确认发生的事故 / A real incident that already happened

```
故障代码 Bugcheck   : 0xD1  DRIVER_IRQL_NOT_LESS_OR_EQUAL
触发脚本 Trigger    : ps_probe6.ps1
疑似组件 Suspected  : sbp2port.sys（Windows IEEE-1394 协议栈）
状态 Status         : ⚠️ 根因尚未定位（ROOT CAUSE NOT IDENTIFIED）
后果 Consequence    : 宿主操作系统蓝屏崩溃；未知是否对扫描仪造成持久影响
```

**在根因定位之前，实机命令白名单必须保持冻结。** 这是本仓库的一条硬约束。

While the root cause is unknown, the command whitelist **must remain frozen**.

### 2.2 冻结中的白名单 / Frozen whitelist

| 允许 Allowed | 禁止 Forbidden |
|---|---|
| `INQUIRY` 标准页 0（standard page 0 only） | 任何 VPD 页（all VPD pages） |
| CDB `12 00 00 00 24 00`，alloc 36 字节 | `MODE SENSE` |
| | `READ BUFFER` |
| | `WRITE BUFFER` ⚠️ **可能永久性损坏固件** |
| | `E0` / `E1` 厂商自定义命令 |
| | `TEST UNIT READY`（暂缓） |

> `WRITE BUFFER` 有可能把数据写入扫描仪内部，**造成不可恢复的固件损坏（变砖）**。
> 任何情况下都不要在你还需要使用的设备上运行它。

### 2.3 逐脚本风险分级 / Per-script risk levels

| 级别 | 脚本 | 说明 |
|---|---|---|
| 🟢 LOW | `ps_readonly.ps1` | 唯一相对安全者。`SAFE_ONLY=$true`，仅发 `0x190012`。**修改时请勿关闭此开关** |
| 🟠 MEDIUM | `ps_probe.ps1` `ps_probe2` `ps_probe3` `ps_probe4` `ps_probe5` | 历史中间版本，未经完整验证，保留仅为证据链完整 |
| 🔴 HIGH | `ps_probe6.ps1` | **实测触发 0xD1 蓝屏** |
| 🔴 HIGH | `ps_brute.ps1` | `:39` 处含 `0x190024` 等**更宽的 ioctl 码** |

每个脚本文件头部均已追加同样的警告。这是按作者要求**原位保留**、**未改动功能**，
**保留 ≠ 推荐运行**。

### 2.4 若你仍然决定运行 / If you still decide to run them

作者建议你至少做到：

1. 使用一台**可以承受重装**的 Windows 主机，且已备份全部数据
2. **断开**其它所有 IEEE-1394 设备
3. 确认扫描仪内**无未取出的底片**（机械动作可能损坏胶片）
4. 准备好可一步回滚的系统还原点 / 完整镜像备份
5. 仅使用 `ps_readonly.ps1`，且保持 `SAFE_ONLY=$true`
6. 全程旁观，**不要无人值守运行**

**在任何情况下，不要运行 `WRITE BUFFER` 类命令。**

---

## 3. 关于 samples/ 与固件来源 / Sample provenance & legal compliance

`samples/` 中的固件来自 **Nikon 官方公开发布的固件更新软件包**
（SUPER COOLSCAN 8000 ED Ver. 1.11，随附官方 ReadMe 标注 2002-12-26）。
来源的三层可复现验证方法记录于 [`samples/SOURCES.md`](samples/SOURCES.md)，
任何人都可以自行核实，毋须信任本项目的陈述。

The firmware in `samples/` originates from Nikon's publicly distributed firmware
update package (Ver. 1.11, official ReadMe dated 2002-12-26). `samples/SOURCES.md`
documents three reproducible verification steps anyone can run independently.

**仍需使用者自行遵守所在地法律**：

Users remain responsible for compliance with their local laws:

- 各国对软件逆向、技术措施规避、以及著作权例外的规定不同，
  请在你的司法辖区内自行判断使用的合法性
- 本仓库**不涉及**任何需登录、付费或非公开渠道才能取得的固件
- `samples/other/` 下的其它机型固件仅供格式交叉参考

Regulations on reverse engineering, circumvention of technological measures and
copyright exceptions vary by jurisdiction. Verify legality where you are.
This repository includes no firmware obtainable only via login, payment or
non-public channels.

> 若你是权利持有人并认为本仓库内容不当，请提交 Issue，作者会配合处理。

---

## 4. 第三方权利 / Third-party rights

- 底层固件与驱动的全部权利归 **Nikon Corporation**，见 [`NOTICE`](NOTICE)
- 本仓库**非官方**，无任何关联、授权、赞助或背书
- 若你是权利持有人且认为本仓库侵犯了你的权利，请提交 Issue，
  作者会配合处理（包括但不限于移除相应内容）

---

## 5. 责任限制 / Limitation of liability

在适用法律允许的最大范围内，作者不对因使用或无法使用本仓库内容而导致的
任何损害承担责任，包括但不限于：数据丢失、硬件损坏、固件损坏、
业务中断、利润损失或任何间接、特殊、附带的损害。

To the maximum extent permitted by law, the author shall not be liable for any damages
arising from the use or inability to use this repository, including but not limited to
data loss, hardware damage, firmware corruption, business interruption, lost profits,
or any indirect, special or consequential damages.

---

<sub>最后更新 Last updated: 2026-10-25</sub>
