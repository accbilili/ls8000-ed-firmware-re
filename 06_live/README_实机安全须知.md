# 🔴 实机操作安全须知 —— 开机前必读

> **本目录的脚本会真实向扫描仪发送 SCSI 命令。**
> 本项目曾导致一次 Windows 蓝屏（`0xD1`）。请在执行任何脚本前读完本文。

---

## 1. 事故档案

| 项 | 内容 |
|---|---|
| 故障码 | **`0xD1`** DRIVER_IRQL_NOT_LESS_OR_EQUAL |
| 责任模块 | **`sbp2port.sys`**（微软 in-box SCSI 端口驱动） |
| 参数 | Arg1 = `0x2F40CEA`（野指针）、Arg2 = `0x2`、Arg3 = `0x0` |
| 触发动作 | `ps_probe6.ps1` 依次发送 **INQUIRY VPD 0x80** 与 **MODE SENSE×3** |
| 现象 | 设备返回非常规 SCSI 响应 → 驱动进入错误处理路径 → 内核崩溃 |
| 原始记录 | `02_reports/live/INCIDENT-20241024-实机协议与蓝屏.md` |

**结论**：`0xD1` 不是扫描仪固件的 bug，而是**主机侧 in-box 驱动栈**（`scsiscan.sys` + `sbp2port.sys`）在遇到"设备返回非常规响应"时的缺陷。固件侧的响应本身是合法的。

---

## 2. 当前冻结的命令白名单

`ps_readonly.ps1` 内置 `$SAFE_ONLY = $true` 护栏，**只放行一条命令**：

```
INQUIRY (standard page 0)   CDB = 12 00 00 00 24 00   长度 36
```

理由：
- 它被实测过数百次，**从未崩溃**
- 任何 SCSI 设备都必须 GOOD 应答，**无失败分支**
- 其余命令（TEST UNIT READY / REQUEST SENSE / MODE SENSE / VPD 页）都**可能**让设备返回 CHECK CONDITION 或短数据，从而进入那条有缺陷的错误处理路径

### 放宽方式（谨慎）

```powershell
# 把 ps_readonly.ps1 第 63 行的 $SAFE_ONLY = $true 改为 $false
```

放宽后脚本会额外发送：

| 命令 | CDB | 长度 | 风险 |
|---|---|---|---|
| TEST UNIT READY | `00 00 00 00 00 00` | 0 | 中 —— 可能返回 NOT READY |
| REQUEST SENSE | `03 00 00 00 12 00` | 18 | 中 —— 已在实测中成功过 |
| MODE SENSE(6) | `1A 00 3F 00 FC 00` | 252 | **高 —— 触发过蓝屏** |

> ⚠️ **MODE SENSE 这一项实际请求的是 page `0x3F`（all pages，全部模式页），不是 page 0。**
> 脚本里给它的标签写作 `MODE SENSE(6) p0` 属于**命名误导** —— 会让人误以为"只读页 0，风险有限"而低估后果。
> 实际返回的是 252 字节的**全部模式页**，信息量与触发面都远大于页 0。
> 这是 `ps_readonly.ps1` 的一处已知缺陷（标签未改），**放宽前请以 CDB 字节为准，不要信标签**。

### 白名单护栏的两个已知缺口

| # | 缺口 | 后果 |
|---|---|---|
| G1 | 白名单只校验 **opcode**（`Send-Query` 只看 `cdb[0]`），不校验 CDB 完整内容 | 「只允许 INQUIRY 标准页 0」这个语义**仅由 `$queries` 清单保证**，白名单本身拦不住 `INQUIRY VPD 0x80`（opcode 同样是 `0x12`） |
| G2 | 上表的 MODE SENSE 标签与实际页码不符 | 误导风险评估，见上 |

> ⚠️ **在解析 Minidump 定位到 `sbp2port.sys` 责任代码路径之前，不要放开 MODE SENSE 与任何 VPD 页。**

---

## 3. 放开前的必办事项

定位蓝屏责任代码需要两份 Minidump（需管理员权限复制）：

```
C:\Windows\Minidump\*.dmp        →  <HOME>\WorkBuddy\2026-10-24-20-10-48\dumps\
```

拿到后才能：
1. 用 WinDbg 确认 `sbp2port.sys` 的具体崩溃指令
2. 判定是「固件返回了不该返回的字节」还是「驱动错误路径本身有缺陷」
3. 据此决定**扩大命令白名单的边界**

---

## 4. 脚本清单与风险分级

完整清单见 `03_indexes/LIVE_LINE_INDEX.md`。速览：

| 脚本 | 作用 | 风险 |
|---|---|---|
| `ps_readonly.ps1` | **唯一推荐**。默认只发 INQUIRY 标准页 0 | 🟢 只读 |
| `scsi_readonly.py` | Python 版只读通道 | 🟢 只读 |
| `ps_probe.ps1` … `ps_probe6.ps1` | 历史探针，**逐步放宽** | 🟡→🔴 |
| `ps_probe6.ps1` | **曾触发蓝屏的那个** | 🔴 |
| `ps_brute.ps1` | 暴力扫描（2340 组已证明无效） | 🔴 |
| `drv_ioctl.py` / `drv_paths.py` / `md3_setupdi.py` | 设备路径与句柄探测 | 🟡 |

> **前序 2340 组暴力扫描失败的真因**：SCSI 数据出现在**输出缓冲**里，不在用户态 DataBuffer —— 早期把结果读回了错误的缓冲区，所以看起来"全部失败"。
> 〔R24〕**机制解释更精确**：该控制码 `0x190012` 是 **METHOD_OUT_DIRECT** 语义（`lpOutBuffer` 就是用户缓冲本身、I/O Manager **不做代拷贝**，驱动经 MDL + `MmMapLockedPages` 直写用户页；`Irp->UserBuffer` 访问 0 次）。
> 且**32 位调用者必须在结构体里传入有效指针** —— 64 位进程的用户态指针普遍 > 4 GB，不被接受。**实测现象本身不变。**

---

## 5. 运行前提

- **管理员权限**（打开 SCSI 设备句柄需要）
- 扫描仪已连接、驱动已装（`scsiscan.sys` in-box）
- Python 32 位宿主（部分 ioctl 脚本需要）

```powershell
# 推荐做法：先跑只读探针
powershell -ExecutionPolicy Bypass -File .\ps_readonly.ps1
```

---

## 6. 一句话总结

> **当前唯一被证明安全的实机操作是 INQUIRY 标准页 0。**
> 在 Minidump 分析完成前，冻结其余所有命令。
