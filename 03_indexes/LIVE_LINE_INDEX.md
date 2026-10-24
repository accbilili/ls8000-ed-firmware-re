# 实机验证线 · 清单与安全红线（打包用独立册）

> **本文为最终版，已完成二次校订。** 校订点见 §0.1「本版校订清单」。

生成：2026-10-25 · 范围：`03_analysis\live\`（13 份）+ 根目录实机线文档（2 份）
方法：**纯静态阅读与代码分析**。本次工作**未执行任何 `ps_*.ps1`、未执行 `scsi_readonly.py`、未向扫描仪发送任何 SCSI 命令**。
定位：把「实机验证线」从主分析线中切出来单独成册，供后续实机操作前逐条对照。
修订：2026-10-25 二次校订 —— 依驱动线裁决 `03_analysis\status\IOCTL_0x190012_METHOD_VERDICT.md` 更正 §4.1/§4.5/§4.8 C1 的 CTL_CODE METHOD 术语（原写 METHOD_NEITHER，实为 **METHOD_OUT_DIRECT**），并补正 §4.3 的 `INQ36` 统计范围（`ps_probe6.ps1` 亦为 0）。**本册只改自己，未动任何已有文档**（源文件修正由 team-lead 另派 `apply-ioctl-fixes` 执行）。

---

## 0. 一页速览

| 项 | 结论 |
|---|---|
| 实机线产物总数 | **15 份**（`live\` 下 13 份：8 个 PowerShell 探针 + 4 个 Python 工具 + 1 份事故报告；根目录 2 份 Markdown） |
| 风险分级 | 零风险 4 份 / 低风险 7 份 / 中风险 1 份 / **高风险 1 份（`ps_probe6.ps1`，即 0xD1 蓝屏的那一次运行）** |
| 已发生事故 | 1 次 `0xD1 DRIVER_IRQL_NOT_LESS_OR_EQUAL`（`sbp2port.sys`，Arg1=`0x2F40CEA`，IRQL=2），2026-10-24 22:48:1x |
| 当前实机白名单 | **仅 1 条命令**：`INQUIRY` 标准页 0，CDB `12 00 00 00 24 00`，alloc 36 B |
| 护栏机制 | `ps_readonly.ps1` 的 `$SAFE_ONLY`（默认 `$true`）+ `$ALLOW` opcode 白名单，双层拦截 |
| ioctl 语义 | `0x190012` = `CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`（驱动线裁决，见 §4.1 脚注） |
| 待用户操作 | **1 项必做**（管理员复制两份 Minidump —— **只差这一步，风险零**）+ 2 项待决策 + 1 项待验证 |

### 0.1 本版校订清单（接手者请先读这张表）

以下 6 条是二次校订后**已定论**的内容。凡与本册其他章节或与源文档表述冲突，**以本表为准**。

| # | 校订点 | 初版写法 | **定论** | 依据 |
|---|---|---|---|---|
| R1 | `0x190012` 的 CTL_CODE 展开 | `CTL_CODE(0x19, 0x012, METHOD_BUFFERED, ANY)`（源文档） | **`CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`** | 穷举 Function∈[0,16)×Method∈[0,4)×Access∈[0,4) 全组合，能产出 `0x190012` 的唯一解；与 disasm 驱动侧反汇编独立复算一致 |
| R2 | Method 位的名称 | 本册初版写 `method=2=METHOD_NEITHER` | **Method=2 是 `METHOD_OUT_DIRECT`**；`METHOD_NEITHER`=3（需 `0x190013`/`0x190023`）。本册初版**名称错**，算术对 | WDK `wdm.h` 常量表 |
| R3 | 三方错法 | 笼统说「文档有误」 | **三种错法不同**：源文档 `INCIDENT:19` = Function 位 + Method 名**都错**（展开 `0x190048`）；`REPORT_实机验证方案.md:42/110-113` 与 `REPORT_实机验证交接.md:164` = **Function 对、Method 名错**（展开 `0x190010`）；本册初版 = Method 名错 | 逐条展开验证 |
| R4 | 「数据在输出缓冲」的机制解释 | 源文档写「METHOD_BUFFERED 的输出缓冲」 | **实测现象完全不变**，仅术语与机制需更正：OUT_DIRECT 下 `lpOutBuffer` **就是用户缓冲本身**，I/O Manager 不拷贝、驱动 `MmMapLockedPages` 直写用户页，用户态立即可见；BUFFERED 则先落内核缓冲、返回时回拷 | 驱动侧：输出侧有 MDL + 直写；`Irp->UserBuffer` 访问 0 次 → 排除 NEITHER；5 个码中**只有 `0x19001C` 是 METHOD_BUFFERED** |
| R5 | `INQ36` 逐字节命中判据的分布 | 本册初版只列 probe5 / ps_readonly 为 0 | **三个脚本均为 0**：`ps_probe5.ps1`（纯三缓冲同印）、**`ps_probe6.ps1`**（崩溃那次，只打印不判定）、`ps_readonly.ps1`（只打印）；其余 5 份各 2 处 | 8 个 ps 脚本全量 `grep -c` 实测 |
| R6 | §1.3 括注的指针编号（C2） | 悬置：§1.2 表格与 §1.3 括注指向不一致 | §1.2 表格「`+0x24`=数据、`+0x28`=sense」**是对的**；**错的是 §1.3 括注**「`+0x28` 的**数据**指针未被写入」—— 按驱动落点应为 **`+0x24`** | `0x140008D3E` 读 `+0x24`→内部 `+0x28`；`0x140008D46` 读 `+0x28`→内部 `+0x30` |

**R1–R6 的源文件修正由 team-lead 另派 `apply-ioctl-fixes` 执行**（含 `REPORT_实机验证交接.md`:269 的 `live\md3dis.py` 失效引用）。**本册未改动任何源文件**，仅在册内加脚注标注。

---

## 1. 探针清单表

文件大小为实测（`stat`/`wc`）。

### 1.1 `03_analysis\live\` 下的 PowerShell 探针（8 份）

| 文件名 | 字节 | 用途 | 对设备发什么命令 | 风险等级 | 备注 |
|---|---|---|---|---|---|
| `ps_probe.ps1` | 9,621 | v1：SetupDi 枚举 + 候选路径探测 + INQUIRY 自校验 | **仅 INQUIRY** `12 00 00 00 24 00`（alloc 36） | 低 | 用的是**错的** 44 字节 `SCSI_PASS_THROUGH` 经典布局；未命中。文件头自述：`No WRITE BUFFER. No E0 mechanism commands.` |
| `ps_probe2.ps1` | 9,526 | v2：路径 × 结构布局 × ioctl 码矩阵 | **仅 INQUIRY** | 低 | 4 种布局(SPT32/SPT64/SSM32/SSM64) × 4 个 ioctl(0x190012/0x190004/0x194004/0x190008)；未命中 |
| `ps_probe3.ps1` | 10,037 | v3：**驱动推导布局** + 5 个 ioctl 码矩阵（首个跑通的版本） | **仅 INQUIRY** | 低 | 布局改为 `+0x14`=CDB / `+0x24`=数据指针 / `+0x28`=sense 指针；5 个 ioctl：`0x190012,0x190016,0x19001A,0x19001C,0x190022` |
| `ps_probe4.ps1` | 6,310 | v4：扫描 flags 字节 `0x00–0xFF` × 长度字段（定位「bit6\|bit7 必须置位」） | **仅 INQUIRY** | 低 | `lenField∈{44,0}` × `headField∈{44,0}` × `flags 0..255`；事故报告称它下发过**约 768 次 INQUIRY 未崩溃** |
| `ps_probe5.ps1` | 5,493 | v5：同时打印**输出缓冲 / 用户数据缓冲 / sense 缓冲**三处 | **仅 INQUIRY**（flags 0x40/0x80/0xC0 三轮） | 低 | **定位到「数据在输出缓冲」的那一次**，是本次实机线的关键转折点 |
| `ps_probe6.ps1` | 6,447 | v6：方向位语义矩阵（**崩溃发生在这次运行**） | INQUIRY std / **TEST UNIT READY ×2** / **REQUEST SENSE** / **MODE SENSE(6) ×3** / **INQUIRY VPD 页 0x80** | **高** | 唯一造成实机蓝屏的脚本。8 条请求里 3 类「非常规响应」见 §3.2 |
| `ps_brute.ps1` | 6,174 | 暴力扫描：ioctl × 结构族 × 结构总长 × 长度字段 × 指针偏移 | **仅 INQUIRY** | 低 | 即前序「2340 组」扫描的主体脚本。`$IOCTLS`（:39）= `0x190012, 0x190004, 0x194004, 0x190014, 0x190024` —— **是唯一含 `0x190024` 的脚本**（该码不在驱动认的 5 个之内，err=50 属预期）。参数：`5 ioctl × 2 fam × size 35..56 × 2 lenval × 6 buf` |
| `ps_readonly.ps1` | 7,650 | **带 opcode 白名单的只读查询工具**（当前唯一在用的实机脚本） | 默认**仅 INQUIRY 标准页 0**；放宽后追加 TUR / REQUEST SENSE / MODE SENSE(6) | 低（默认）/ **中（放宽后）** | **只用 `0x190012` 一个 ioctl 码**（`:116` `DeviceIoControl($h,[uint32]0x190012,$pin,[uint32]44,…)`），是唯一走通通路的脚本。护栏详见 §2 |

### 1.2 `03_analysis\live\` 下的 Python 工具（4 份）

| 文件名 | 字节 | 用途 | 对设备发什么命令 | 风险等级 | 备注 |
|---|---|---|---|---|---|
| `scsi_readonly.py` | 23,408 | SCSI 直通层 + Tier 1/2 命令封装（Python 工具的完整版） | 子命令决定：`selftest` 离线不碰设备；`enumerate` 只开句柄；`inq`=INQUIRY；`tier1`=TUR+REQUEST SENSE+MODE SENSE+**E1 READ STATUS**；`readbuf`/`dumpboot`/`compare`=**READ BUFFER(10) mode 2** | **中**（`readbuf`/`dumpboot`/`compare`/`tier1`） | **文件头自述已暂停使用**：`本脚本目前【暂停使用】。任何实机命令都必须先获得用户的再次明确授权。` 另：64 位 Python，结构体布局与 32 位驱动不兼容 → 直接使用会失败 |
| `drv_ioctl.py` | 2,273 | 反汇编 `NKDSBP2.dll` 的 DeviceIoControl 调用点 | **不碰设备**（只读 DLL 文件） | 零 | 产出 ioctl 码 `0x190012` 与 `nInBufferSize=44` 的反汇编依据 |
| `drv_paths.py` | 4,680 | 挖掘 Nikon 传输层 DLL 的导入表与设备路径字符串 | **不碰设备** | 零 | 解析 `NKDSBP2.dll` / `NKDUSCAN.dll` 的 PE 头、导入表、字符串 |
| `md3_setupdi.py` | 2,413 | 定位 `LS8000.md3` 中 `SetupDiGetDeviceRegistryPropertyA` 的调用点与注册表属性索引 | **不碰设备**（只读 `D:\DS\TEST\LS8000\driver\LS8000.md3`） | 零 | 反汇编 `0x200be164` 等 IAT 槽的 `call [slot]` |

### 1.3 文档（3 份）

| 文件名 | 字节 | 用途 | 风险等级 | 备注 |
|---|---|---|---|---|
| `live\INCIDENT-20241024-实机协议与蓝屏.md` | 10,747 | **事故档案 + ioctl 协议定案 + 安全策略**（本册主要引用源） | 零（文档） | 160 行；§4 是事故记录，§4.4 是安全策略，§4.5 是待用户操作项 |
| `REPORT_实机验证方案.md`（根目录） | 24,013 | 接机器前的完整计划（授权边界、三级命令序列、红线） | 零（文档） | 392 行；§0-A 授权边界、§0-B 传输层静态核实、§0-C 只读探测实录、§4 红线 |
| `REPORT_实机验证交接.md`（根目录） | 18,112 | 跨会话交接件 | 零（文档） | 293 行；§5 实机状态、§5.2 2340 组扫描、§9 文件地图、§10 环境要点（11 条坑） |

### 1.4 风险分级统计

| 等级 | 份数 | 名单 |
|---|---|---|
| **零（不接触设备）** | 4 | `INCIDENT-…md`、`drv_ioctl.py`、`drv_paths.py`、`md3_setupdi.py`（+ 根目录 2 份文档） |
| **低（只发 INQUIRY）** | 7 | `ps_probe.ps1`、`ps_probe2.ps1`、`ps_probe3.ps1`、`ps_probe4.ps1`、`ps_probe5.ps1`、`ps_brute.ps1`、`ps_readonly.ps1`（默认态） |
| **中（含 READ BUFFER / E1，或放宽护栏后）** | 1(+1 变体) | `scsi_readonly.py`；`ps_readonly.ps1` 放宽态 |
| **高（已实证触发蓝屏）** | 1 | `ps_probe6.ps1` |

---

## 2. `$SAFE_ONLY` 护栏详解（重点核对）

来源：`03_analysis\live\ps_readonly.ps1`

### 2.1 双层拦截结构

**第一层 —— opcode 白名单**（`ps_readonly.ps1:49-56`），原文：

```powershell
$ALLOW = @{ 0x00 = 'TEST UNIT READY'; 0x03 = 'REQUEST SENSE'; 0x12 = 'INQUIRY'; 0x1A = 'MODE SENSE(6)' }
```

（原文为 4 行哈希表逐项列出，此处按同一语义合并为一行；逐行原貌见 `ps_readonly.ps1:50-55`。）

**第二层 —— `$SAFE_ONLY` 覆盖**（`ps_readonly.ps1:57-67`），原文：

```powershell
# SAFETY GATE (2026-10-24 22:48 蓝屏之后新增):
#   只放行 INQUIRY 标准页 0。它被实测过数百次、从未崩溃，且任何 SCSI 设备
#   都必须 GOOD 应答。其它命令都可能让设备返回 CHECK CONDITION / 短数据，
#   从而进入 in-box scsiscan+sbp2port 的错误处理路径 —— 该路径已被怀疑是
#   0xD1 蓝屏（sbp2port.sys）的触发点（见 INCIDENT-20241024-实机协议与蓝屏.md）。
#   扩大命令集必须先解析 Minidump 定位到责任代码路径。
$SAFE_ONLY = $true
if ($SAFE_ONLY) {
  $ALLOW = @{ 0x12 = 'INQUIRY (standard page 0 only)' }
}
```

**执行点**（`ps_readonly.ps1:93-95`），原文：`$op = [int]$cdb[0]` + `if (-not $ALLOW.ContainsKey($op)) { throw ("REFUSED: opcode 0x{0:X2} not in allowlist" -f $op) }`

**查询清单**（`ps_readonly.ps1:139-149`），原文：

```powershell
$queries = @(
  @{ n='INQUIRY (standard)'; cdb=[byte[]]@(0x12,0x00,0x00,0x00,0x24,0x00); len=36 }
)
if (-not $SAFE_ONLY) {
  $queries += @(
    @{ n='TEST UNIT READY';    cdb=[byte[]]@(0x00,0x00,0x00,0x00,0x00,0x00); len=0 },
    @{ n='REQUEST SENSE';      cdb=[byte[]]@(0x03,0x00,0x00,0x00,0x12,0x00); len=18 },
    @{ n='MODE SENSE(6) p0';   cdb=[byte[]]@(0x1A,0x00,0x3F,0x00,0xFC,0x00); len=252 }
  )
}
if ($SAFE_ONLY) { Write-Host "SAFE_ONLY mode: only INQUIRY standard page 0 is allowed." }
```

### 2.2 默认行为是否真的只发 INQUIRY 标准页 0 —— **是，双重保证**

| 校验点 | 结论 |
|---|---|
| `$SAFE_ONLY` 默认值 | `$true`（`ps_readonly.ps1:63`），且**脚本无任何命令行参数入口**（无 `param()` 块、无 `args` 解析），因此**不修改文件即永远是 `$true`** |
| 白名单生效 | `$SAFE_ONLY=$true` → `$ALLOW` 被**整体替换**为 `@{ 0x12 = ... }`，4 元素哈希表只剩 1 个键 |
| 运行时拦截 | `Send-Query` 对 `cdb[0]` 做 `ContainsKey` 检查，不在白名单则 `throw "REFUSED: opcode 0x{0:X2} not in allowlist"` |
| 查询清单 | `$queries` 初始只有 1 条 INQUIRY；其余 3 条被 `if (-not $SAFE_ONLY)` 包住，默认不追加 |
| 实际发出的唯一 CDB | `12 00 00 00 24 00`（opcode `0x12`、page 0、alloc `0x24`=36 B）——**确实是标准页 0，不是 VPD** |

**结论：默认态下 `ps_readonly.ps1` 只向设备发送 1 条 INQUIRY 标准页 0 查询。**

### 2.3 唯一的放宽开关及其后果

| 项 | 值 |
|---|---|
| **变量名** | `$SAFE_ONLY`（`ps_readonly.ps1:63`） |
| **放宽方式** | 手动把 `$SAFE_ONLY = $true` 改成 `$SAFE_ONLY = $false`（**唯一途径**，无 CLI 参数、无环境变量、无注册表） |
| **放宽后白名单** | 恢复为 4 条：`0x00` TUR / `0x03` REQUEST SENSE / `0x12` INQUIRY / `0x1A` MODE SENSE(6) |
| **放宽后追加的命令** | ① `TEST UNIT READY` `00 00 00 00 00 00`（alloc 0）② `REQUEST SENSE` `03 00 00 00 12 00`（alloc 18）③ `MODE SENSE(6)` `1A 00 3F 00 FC 00`（alloc 252） |
| **风险后果** | ③ 的 CDB **与 `ps_probe6.ps1` 崩溃运行中的 `MODE SENSE p3F/252` 完全相同**（同一页码、同一 alloc 长度），正是事故报告 §4.2 列为「高：数据长度与请求长度不一致」的那一类请求。① 则撞上事故报告 §4.4 第 3 条明令「暂缓」的项（设备忙时返回 CHECK CONDITION） |

**⇒ 放宽 `$SAFE_ONLY` 会原样复活导致蓝屏的那批「非常规响应」请求。** 这与事故报告 §4.4 第 4 条直接冲突：`若要扩大命令集，必须先拿到转储并定位到 Arg4 所属模块与代码路径。`

### 2.4 护栏的两个缺口（供打包时补注，不改代码）

| # | 缺口 | 证据 | 建议 |
|---|---|---|---|
| G1 | **白名单只校验 opcode，不校验 CDB 内容**。`Send-Query` 只看 `cdb[0]`；因此「standard page 0 only」这个语义**仅由 `$queries` 清单保证**，白名单本身拦不住 `INQUIRY VPD 0x80`（opcode 仍是 `0x12`） | `ps_readonly.ps1:94-95` 只取 `$cdb[0]`；`$ALLOW` 键只有 opcode | 若日后放宽，应改为对完整 CDB 字节串做白名单匹配 |
| G2 | **标签与实际页码不符**：`$queries` 里该项名叫 `MODE SENSE(6) p0`，但 CDB 是 `1A 00 3F 00 FC 00` → **page `0x3F`（all pages），不是 page 0** | `ps_readonly.ps1:146` | 改名，避免误读为「读页 0 模式页」而低估风险 |

---

## 3. 事故档案（原文引用）

来源：`03_analysis\live\INCIDENT-20241024-实机协议与蓝屏.md`

### 3.1 事故事实（§4.1 原文）

> 时间 2026-10-24 约 22:48:1x（重启 22:48:20；WER 事件写于 22:48:35）
> BugCheck `0x000000D1  DRIVER_IRQL_NOT_LESS_OR_EQUAL`
> Arg1 `0x0000000002F40CEA`（被访问地址，远低于内核地址空间 → 野指针/未初始化/被破坏）
> Arg2 `0x2`（IRQL = DISPATCH_LEVEL，该级别禁止访问分页内存）· Arg3 `0x0`（读操作）
> Arg4 `0xFFFFF8017BDCA1E0`（出错指令地址）· WER 1019 可能相关驱动：`sbp2port.sys`
> 转储 `C:\Windows\Minidump\102426-14953-01.dmp`（3,562,358 B）

时间线校正（§4.1 原文）：

> **时间线校正**：6008 事件里的「22:38:13」是**最后一条 System 日志的时间**（本轮探测不写 System 日志），**实际崩溃在 22:48:1x**，紧接 `ps_probe6.ps1` 的运行（本轮最后一次工具调用返回空输出 = 崩溃打断）。
> 本次启动后至 23:05 **无新崩溃**（事件查询确认）。

### 3.2 触发它的具体命令序列

事故报告 §4.2 原文（「嫌疑命令的收敛」）：

> `ps_probe6.ps1` 相对之前成功过的调用，**新增了三类请求**：
>
> | 请求 | 设备侧预期 | 风险 |
> |---|---|---|
> | INQUIRY VPD 页 0x80 | 不支持 → **CHECK CONDITION** | 高：首次进入驱动的「CHECK CONDITION + 交付 sense」路径 |
> | MODE SENSE(6) ×3（alloc 252 / 4 / 4） | 可能返回短数据或 CHECK CONDITION | 高：数据长度与请求长度不一致 |
> | TEST UNIT READY（flags 0x40 / DTL=0） | err=87，未真正下发 | 低 |

收敛后的结论（§4.2 原文继续）：

> 而 `ps_probe4.ps1` 曾经成功下发 **约 768 次 INQUIRY（CDB 位置错、数据缓冲错）**而**没有崩溃** →
> **⇒ 崩溃不在「快乐路径」，而在「设备返回非常规响应 → 驱动错误/短数据处理路径」。**
> `0x2F40CEA` 这种小数值特征与「SRB 字段未初始化 / 陈旧设备扩展指针被当作长度或地址使用」一致。

对照 `ps_probe6.ps1:102-111` 的实际请求表（8 条），可确认上表三类新请求对应：

| # | 脚本内标签 | CDB | alloc | flags | DTL | senseLen |
|---|---|---|---|---|---|---|
| 1 | `INQUIRY std` | `12 00 00 00 24 00` | 36 | 0x40 | 36 | 18 |
| 2 | `TEST UNIT READY` | `00 00 00 00 00 00` | 0 | 0x00 | 0 | 0 |
| 3 | `TEST UNIT READY+s` | `00 00 00 00 00 00` | 0 | 0x00 | 0 | 18 |
| 4 | `REQUEST SENSE` | `03 00 00 00 12 00` | 18 | 0x40 | 18 | 18 |
| 5 | `MODE SENSE p3F/252` | `1A 00 3F 00 FC 00` | 252 | 0x40 | 252 | 18 |
| 6 | `MODE SENSE p00/4` | `1A 00 00 00 04 00` | 4 | 0x40 | 4 | 18 |
| 7 | `MODE SENSE p3F/4` | `1A 00 3F 00 04 00` | 4 | 0x40 | 4 | 18 |
| 8 | `INQUIRY p80 VPD` | `12 80 80 00 24 00` | 36 | 0x40 | 36 | 18 |

> 注：`ps_probe6.ps1` 中第 2 条用的是 flags `0x00`/DTL 0（正确组合）；事故报告 §1.4 记载的「TEST UNIT READY flags=0x40 时 err=87」是更早那次实验（`ps_probe6.ps1` 之前的中间态），本次脚本已修正。

### 3.3 与前一次崩溃的同构性（§4.3 原文）

| 日期 | BugCheck | 特征 |
|---|---|---|
| 10/05 | `0x9F` `DRIVER_POWER_STATE_FAILURE`（Arg1=3，IRP 在电源状态转换中超时） | 6008：最后日志 02:03:28，崩溃约 10:59（同为「长间隔无日志」） |
| 10/24 | `0xD1` 野指针 | 同型 |

> 两起都指向 **1394/SBP-2 设备电源/总线状态变化 → 驱动处理路径失效**这一根因，与另一会话的推断方向一致。

### 3.4 当前允许的命令白名单（§4.4 原文，全文照录）

> ### 4.4 安全策略（下一轮起强制执行）
>
> 1. **默认只允许一条命令**：`INQUIRY` 标准页 0（CDB `12 00 00 00 24 00`）。它被实测过数百次、从未崩溃，且任何 SCSI 设备都必须 GOOD 应答。
> 2. **禁止**：VPD 页、MODE SENSE、READ BUFFER（任何 mode）、任何 E0/E1、任何 WRITE BUFFER。
> 3. **TEST UNIT READY 暂缓**：设备忙时它会返回 CHECK CONDITION（"NOT READY"），同样进入危险路径。
> 4. 若要扩大命令集，**必须先拿到转储并定位到 `Arg4` 所属模块与代码路径**。
> 5. 每次运行后检查 `Get-WinEvent ... Id=41,1001,1019`，确认无新增崩溃。

**白名单内容（一句话）**：唯一允许 = `INQUIRY` 标准页 0，CDB `12 00 00 00 24 00`，alloc 36 B。其余全部禁止。

### 3.5 红线（事故报告 §5 结尾原文）

> **红线不变**：只读、不扫片、不动电机、不发 WRITE BUFFER、不用 READ BUFFER mode 5。
> **新增红线**：在 `sbp2port.sys` 缺陷定位前，**不发任何会产生非常规 SCSI 响应的命令**。

以及 §5 行动清单（原文）：

| 优先 | 动作 | 风险 | 备注 |
|---|---|---|---|
| 1 | **暂缓一切新 SCSI 探测**，直到转储定位到责任代码路径 | — | 本轮已用一台蓝屏换来的教训 |
| 2 | 用管理员复制两份转储并跑 `analyze_dump.py` | 零（只读复制） | 闭合「Arg4 归属」这一环 |
| 3 | 若确认 `sbp2port.sys`，则**只保留 INQUIRY 标准页**作为唯一允许的实机命令 | 零 | 其余价值可由静态分析替代 |
| 4 | 观察性抓包（用户正常运行 NikonScan，我方只旁听 ioctl 流量） | 零 | 但仍会经同一驱动路径，**需在转储定位后再决定** |
| 5 | 固件侧静态工作照常推进（引导块、图像算法） | 零 | 主线不依赖实机 |

> 补充：事故报告开头的安全声明同样为原文——
> **安全状态**：本轮所有命令均为 SCSI 只读查询（INQUIRY / TEST UNIT READY / REQUEST SENSE / MODE SENSE），未发 WRITE BUFFER、未发 READ BUFFER、未发 E0/E1、未触碰走片机构。

---

## 4. 已验证成果（带原文依据）

### 4.1 ioctl 通路：`0x190012`

事故报告 §1.1 原文表行：

> | ioctl | **`0x190012`** = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x012, METHOD_BUFFERED, FILE_ANY_ACCESS)` | `NKDSBP2.dll@0x10002B60` + 驱动分派 `0x140008BA7` |
> | 宿主 | **32 位**（`C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`） | 驱动只加载 64 位 in-box 版 |

同文 §1.1 续：

> **驱动只认 5 个 ioctl**：`0x190012`（SCSI 透传）、`0x190016`、`0x19001A`、`0x19001C`、`0x190022`（分派 `0x140008BA7`）。
> 前序会话试的 `0x190004`/`0x190008`/`0x190014` **在驱动里根本不存在**（全文件 0 命中）→ err=50 属预期，**枚举 ioctl 码无意义**。

`ps_readonly.ps1:10-12` 的协议头注释独立复述同一结论：`# PROTOCOL (derived from the loaded 64-bit in-box scsiscan.sys, verified live):` / `#   ioctl 0x190012, 44-byte input struct, 32-bit caller:`

> ⚠️ **上表原文的 CTL_CODE 展开式有误，已由驱动线裁决**（详见 `03_analysis\status\IOCTL_0x190012_METHOD_VERDICT.md`，202 行）：`0x190012` 正确展开为 `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`。原文写的 `0x012, METHOD_BUFFERED` 展开后是 `0x190048`，与常量不符；`METHOD_BUFFERED` + func `0x004` 展开是 `0x190010`，也对不上。**Function `0x004` 与「5 个 ioctl」结论不受影响，仅 Method 位与展开式需更正。**

### 4.2 44 字节私有结构布局

事故报告 §1.2 原文表（**六项全部对上**）：

| 偏移 | 宽度 | 内容 | 驱动校验点 |
|---|---|---|---|
| `+0x00` | dword | 未被 32 位路径拷贝（64 位路径会用） | — |
| **`+0x04`** | dword | **结构总长**，32 位路径必须 **== 0x2C (44)**，64 位 == 0x38 | `0x1400084AF`/`0x1400084B5` |
| **`+0x08`** | byte | **方向位**：bit6(0x40)=数据从设备读，bit7(0x80)=数据写给设备 | DTL>0 → `test al,0xC0` 必须非零（`0x1400084D1`）；**DTL==0 → 必须为零**（`0x140008501`） |
| `+0x0C` | byte | **CdbLength**（1–16）。==10 → CDB 取自 `+0x00`；==6 → CDB 取自 `+0x14` | `0x140008485`/`0x140008D93` |
| `+0x0D` | byte | **SenseInfoLength**；>0 时 `+0x28` 的 sense 指针必须非 NULL | `0x140008505`–`0x140008510` |
| `+0x10` | dword | **DataTransferLength**；须 ≤ 设备上限 | `0x1400084DA` |
| `+0x14` | byte[16] | **CDB** | `0x140008D9A` |
| `+0x24` | dword | **数据缓冲指针**（32 位路径） | `0x1400084BB`（内部 `+0x28`，必须非 NULL） |
| `+0x28` | dword | **sense 缓冲指针**（32 位路径） | `0x14000850B` |

**布局定性的原文**（§1.4 末尾）：

> **⇒ 0x190012 通路已完全打通。** 前序会话的「结构体布局」问题至此闭合：不是 SCSI 结构，而是 **in-box scsiscan.sys 私有的 SEND_SCSI_CMD 风格结构**（与经典 `SCSI_PASS_THROUGH` 字段位置不同）。

`ps_probe4.ps1:7-18` 与 `ps_readonly.ps1:10-22` 两处脚本头注释各自独立复述了同一张布局表，可交叉印证。

### 4.3 INQUIRY 36 字节与模板逐字节一致

事故报告 §1.4 原文表行：

> | **INQUIRY 标准页** | `12 00 00 00 24 00` | ✅ **36 字节，与已知模板逐字节一致**：`06 80 02 02 1F 00 00 00` + `Nikon   LS-8000 ED      1.11` |

§2 交叉验证第 1 行原文：

> | 1 | INQUIRY 返回 `06 80 02 02 1F 00 00 00` + `Nikon   LS-8000 ED      1.11` | 主报告 §2.2「实机固件版本已确认：SCSI INQUIRY 得 1.11，与镜像模板 36/36 逐字节一致」 | ✅ **实机 36/36 复现**，固件镜像 = 本机设备 |

命中判据在脚本侧是硬逐字节比较：内嵌 `$INQ36` 模板常量（`06 80 02 02 1F 00 00 00` + `Nikon   LS-8000 ED      1.11`）+ `for($k=0;$k -lt 36;$k++)` 逐字节比对。实测各脚本 `INQ36` 出现次数：`ps_probe.ps1`/`ps_probe2.ps1`/`ps_probe3.ps1`/`ps_probe4.ps1`/`ps_brute.ps1` 各 **2**；**`ps_probe5.ps1`/`ps_probe6.ps1`/`ps_readonly.ps1` 各 0** —— 即 probe5（纯三缓冲同印）、probe6（崩溃那次，只打印不做判定）、ps_readonly（只打印）三者**均不含**该命中判据。比对循环实例见 `ps_probe4.ps1:115`：

```powershell
for ($k = 0; $k -lt 36; $k++) { if ($r.data[$k] -ne $INQ36[$k]) { $same = $false; break } }
```

### 4.4 REQUEST SENSE 18 字节三元组

事故报告 §1.4 原文表行：

> | **REQUEST SENSE** | `03 00 00 00 12 00` | ✅ **18 字节定长格式**：`70 00 00 00 00 00 00 0B 00 00 00 00 00 00 00 00 00 00` → **SenseKey=0 / ASC=0 / ASCQ=0（NO SENSE）**——与固件 `0x01914A` 的 `[SenseKey][ASC][ASCQ]` 三元组结构完全对应 |

§2 交叉验证第 2 行原文：

> | 2 | REQUEST SENSE 的 `70 00 00 00 … 00 00 00` 定长格式 | `0x01914A` 记录 `[flags][SenseKey][ASC][ASCQ][vendor]`，固件按三元组构造 | ✅ **sense 三元组在实机上就是这 3 个字节**；SCSI 定长 sense 的 byte2/byte12/byte13 ↔ 固件三元组 |

### 4.5 「SCSI 数据落在输出缓冲里」= 前序 2340 组暴力扫描失败的真因

事故报告 §1.3 原文（标题为 ★ 重点）：

> ### 1.3 ★ 前序 2340 组扫描全军覆没的真正原因：读错了缓冲区
>
> **SCSI 数据落在 METHOD_BUFFERED 的「输出缓冲」里（`bytesRet` = 数据长度），不在用户态的 DataBuffer 指针。**
> 前序会话一直去读 `+0x24` 指向的用户缓冲，因此即使 ioctl 成功也永远看不到 INQUIRY 模板。
> （驱动 `0x140008D4E` 把用户 `+0x14..+0x23` 搬进内部 `+0x14`，而 `+0x28` 的数据指针在本次实测中未被写入。）

`ps_readonly.ps1:21-22` 头注释独立复述：`#   The SCSI data arrives in the METHOD_BUFFERED OUTPUT buffer (bytesRet bytes),` / `#   NOT in the user DataBuffer.`

> ⚠️ **措辞更正（驱动线裁决，现象不变）**：原文与脚本注释里的 `METHOD_BUFFERED` 应为 **`METHOD_OUT_DIRECT`**。实测现象「数据出现在输出缓冲（`bytesRet` = 数据长度）、不在用户态 DataBuffer 指针」**完全不变且解释更精确** —— OUT_DIRECT 下 `DeviceIoControl` 的输出缓冲**就是用户缓冲本身**，I/O Manager 不拷贝、直接给驱动 MDL，驱动 `MmMapLockedPages` 后直写用户页，用户态立即可见；而 BUFFERED 应当先落内核缓冲、返回时回拷。详见 `03_analysis\status\IOCTL_0x190012_METHOD_VERDICT.md` §2.2–2.4。

**定位该结论的那次实验**：`ps_probe5.ps1`（三缓冲同印），事故报告 §3 表原文：

> | `live\ps_probe5.ps1` | 打印输出缓冲 / 数据缓冲 / sense 缓冲三处（**定位到数据在输出缓冲**） |

`ps_probe5.ps1:96-105` 原文印证其做法（同一 ioctl 后分别 `Copy` 出 out / data / sense 三块再打印）：

```powershell
          $ob = New-Object byte[] 96
          [System.Runtime.InteropServices.Marshal]::Copy($outb, $ob, 0, 96)
          $db = New-Object byte[] 48
          [System.Runtime.InteropServices.Marshal]::Copy($data, $db, 0, 48)
          $sb = New-Object byte[] 32
          [System.Runtime.InteropServices.Marshal]::Copy($sense, $sb, 0, 32)
          Write-Host ("  out[00..47]: {0}" -f (Hex $ob 48))
          Write-Host ("  data[00..47]: {0}" -f (Hex $db 48))
```

> **补注（分两阶段的读法）**：2340 组扫描（`ps_brute.ps1`）本身在**参数校验阶段**就全灭，根因是**结构布局错**（`REPORT_实机验证方案.md` §0-C.3：「结果：**err=50 × 1872，err=87 × 468，零成功。**」；`REPORT_实机验证交接.md` §5.2 同）。「读错缓冲区」是**第二阶段**的问题——`ps_probe3/4` 拿到 `ok=TRUE` 之后仍看不到模板，因为读的是 `+0x24` 用户缓冲而非输出缓冲。两阶段合起来才是完整因果链。

### 4.6 其余实机实测结果（§1.4 同表原文）

> | INQUIRY VPD 页 0x80 | `12 80 80 00 24 00` | ok=TRUE，bytesRet=0（设备不支持 VPD → 走 CHECK CONDITION 路径） |
> | TEST UNIT READY | `00 00 00 00 00 00` | flags=0x40 时 err=87（DTL=0 须 flags 的 bit6\|bit7 全清）；未再试正确组合 |
> | MODE SENSE(6) 页 0x3F | `1A 00 3F 00 FC 00` | ok=TRUE，bytesRet=0 |

### 4.7 与固件侧的第三处交叉验证（§2 原文表第 3 行）

> | 3 | 设备不响应 VPD 页 0x80（CHECK CONDITION） | 固件 SCSI 分派表 `0x03E2E8` 只有 20 个 opcode，无 VPD 特殊处理 | ✅ 一致：2000 年代固件不实现 VPD |

（第 1、2 处交叉验证已分别随 4.3、4.4 引用原文，见上。）

### 4.8 校核备注（3 条，C1/C2 已定案，C3 待修订）

以下 3 条是本次打包时做算术/参数核对发现的**文档内部不一致**。均**不影响上述实机结论**，但影响文档可复现性。**本册未修改任何已有文档**，待改点已移交 `apply-ioctl-fixes` 执行（team-lead 拍板）。

| # | 事项 | 核对结果 | 状态 / 依据 |
|---|---|---|---|
| C1 | `0x190012` 的 CTL_CODE 解码 | 事故报告 §1.1 写 `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x012, METHOD_BUFFERED, FILE_ANY_ACCESS)`；按标准 `CTL_CODE(dev,fn,mth,acc)=(dev<<16)\|(acc<<14)\|(fn<<2)\|mth` 计算，`0x190012` → dev=`0x19`、func=`0x004`、**method=`2`**、acc=FILE_ANY_ACCESS。根目录两份文档（`REPORT_实机验证方案.md` §0-B.2、`REPORT_实机验证交接.md` §5.1）func 写 `0x004` 是对的，错的只是 Method 名 | ✅ **已定案**（见 §0.1 R1–R4）：Method=2 的标准名是 **`METHOD_OUT_DIRECT`**（`METHOD_NEITHER`=3，需 `0x190013`/`0x190023`）。三处文档写的 `METHOD_BUFFERED` 自带宏展开式与常量自相矛盾（`0x012`+BUFFERED → `0x190048`；`0x004`+BUFFERED → `0x190010`）。驱动侧反汇编实证：输出侧有 MDL + `MmMapLockedPages` 直写、`Irp->UserBuffer` 访问 0 次 → 排除 NEITHER；5 个码中**只有 `0x19001C` 是 METHOD_BUFFERED**。详见 `03_analysis\status\IOCTL_0x190012_METHOD_VERDICT.md`（202 行）。**「数据出现在输出缓冲」现象不变** |
| C2 | §1.2 表格 vs §1.3 括注的指针编号 | §1.2 表格：`+0x24`=数据缓冲指针、`+0x28`=**sense** 缓冲指针；§1.3 括注却写「`+0x28` 的**数据**指针在本次实测中未被写入」 | ✅ **已定案**（见 §0.1 R6）：§1.2 表格**是对的**；错的是 §1.3 括注——按驱动落点 `0x140008D3E` 读 `+0x24` 展宽写入内部 `+0x28`、`0x140008D46` 读 `+0x28` 展宽写入内部 `+0x30`，那个括注的 `+0x28` 应改为 **`+0x24`** |
| C3 | 2340 组扫描的 ioctl 清单 | `ps_brute.ps1:39` 实际是 `0x190012, 0x190004, 0x194004, 0x190014, 0x190024`；`REPORT_实机验证交接.md` §5.2 写作 `0x190012 / 0x190004 / 0x194004 / 0x190008 / 0x190014`（`0x190008` vs `0x190024` 不一致） | ⏳ **待修订**：直接读脚本常量 vs 读文档；复现 1872/468 计数时需以脚本为准。注：`0x190024` 不在驱动认的 5 个码内（`0x190012/16/1A/1C/22`），err=50 属预期 |

**待改点清单（由 `apply-ioctl-fixes` 执行；本册按约束未动已有文档）**：
`live\INCIDENT-20241024-实机协议与蓝屏.md`:19（Function `0x012`→`0x004`，Method→`METHOD_OUT_DIRECT`）、同文件 :45（「落在 METHOD_BUFFERED 的『输出缓冲』里」→「**直写** OUT_DIRECT 的输出缓冲（用户缓冲本身，无回拷）」）、同文件 §1.3 括注（`+0x28`→`+0x24`，见 C2）、`REPORT_实机验证方案.md`:42、`:110-113`、`REPORT_实机验证交接.md`:164、`REPORT_实机验证交接.md`:269（`live\md3dis.py` 失效引用，见 §5.4 V4）。

---

## 5. 待用户操作事项

### 5.1 必做（阻塞项）：管理员复制两份 Minidump

事故报告 §4.5 原文：

> 当前进程未提权，无法读 `C:\Windows\Minidump\*.dmp`。请以**管理员**身份执行：
>
> ```powershell
> New-Item -ItemType Directory -Force -Path <HOME>\WorkBuddy\2026-10-24-20-10-48\dumps
> Copy-Item C:\Windows\Minidump\102426-14953-01.dmp <HOME>\WorkBuddy\2026-10-24-20-10-48\dumps\crash_1024.dmp
> Copy-Item C:\Windows\Minidump\100526-13500-01.dmp <HOME>\WorkBuddy\2026-10-24-20-10-48\dumps\crash_1005.dmp
> ```
>
> 拿到后我可直接判定 `Arg4 = 0xFFFFF8017BDCA1E0` 属于哪个模块、偏移多少、是否即 `sbp2port.sys`（脚本已备好：`<HOME>\WorkBuddy\2026-10-24-22-49-48\analyze_dump.py`）。

**本次打包时的现状核对**：

| 检查项 | 现状 |
|---|---|
| `<HOME>\WorkBuddy\2026-10-24-20-10-48\dumps\` | **目录已存在，但为空**（0 个文件）→ **转储尚未复制** |
| `C:\Windows\Minidump\102426-14953-01.dmp` | 存在，3,562,358 B（与事故报告记载的字节数一致） |
| `C:\Windows\Minidump\100526-13500-01.dmp` | 存在，4,936,796 B |
| `<HOME>\WorkBuddy\2026-10-24-22-49-48\analyze_dump.py` | 存在，2,636 B；用法 `python analyze_dump.py <dmp路径> [十六进制地址…]`，可直接把 `0xFFFFF8017BDCA1E0` 作为参数传入做归属判定 |

**⇒ 只差管理员复制这一步，风险零（只读复制）。** 现状：源 `.dmp` 已在 `C:\Windows\Minidump\`，目标目录已建但为空，工具已就位 —— **三个前置条件全部具备，唯一缺的就是那两条 `Copy-Item`**。复制完成后我方立刻可跑 §5.2 的归属判定。

### 5.2 转储到位后由我方执行（无需用户操作）

`python <HOME>\WorkBuddy\2026-10-24-22-49-48\analyze_dump.py <HOME>\WorkBuddy\2026-10-24-20-10-48\dumps\crash_1024.dmp 0xFFFFF8017BDCA1E0`
→ 产出 `Arg4` 归属模块 + 模块内偏移 + 是否即 `sbp2port.sys`，以及 `BugCheckCode/Arg1/Arg2/Arg3/Arg4` 复核。

### 5.3 待用户决策（2 项）

| # | 决策项 | 背景 | 现状 |
|---|---|---|---|
| D1 | **是否扩大实机命令集** | 事故报告 §4.4 第 4 条：`若要扩大命令集，必须先拿到转储并定位到 Arg4 所属模块与代码路径`；§5 行动清单第 3 条：`若确认 sbp2port.sys，则只保留 INQUIRY 标准页作为唯一允许的实机命令` | **默认不扩大。** 维持 `ps_readonly.ps1` 的 `$SAFE_ONLY = $true` |
| D2 | **是否进行观察性抓包**（用户正常运行 NikonScan，我方只旁听 ioctl 流量） | §5 行动清单第 4 条：风险为零，但 `仍会经同一驱动路径，需在转储定位后再决定` | **等转储结论出来再定** |

### 5.4 待验证 / 需持续遵守（无需额外动作，但每次实机操作都要执行）

| # | 事项 | 依据 |
|---|---|---|
| V1 | 每次实机运行后检查 `Get-WinEvent ... Id=41,1001,1019`，确认无新增崩溃 | 事故报告 §4.4 第 5 条 |
| V2 | 实机脚本必须在 **32 位** PowerShell 下运行：`C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`；脚本源码必须纯 ASCII（32 位 PS 按 ANSI/GBK 读 `.ps1`，中文会破坏引号） | `REPORT_实机验证交接.md` §10 第 1、2 条；各 `ps_*.ps1` 头注释 `ASCII-only source` |
| V3 | 红线常驻：只读、不扫片、不动电机、不发 WRITE BUFFER、不用 READ BUFFER mode 5、不发任何会产生非常规 SCSI 响应的命令 | 事故报告 §5 结尾；`REPORT_实机验证方案.md` §4 |
| V4 | **`REPORT_实机验证交接.md`:269 的 `03_analysis\live\md3dis.py` 引用指向不存在的文件**（标注为「md3 任意 VA 区间反汇编器」）。`live\` 目录实测 13 个文件，无 `md3dis.py`；同目录的 `md3_setupdi.py` 是**另一个东西**（定位 md3 的 SetupDi 调用点），不是它的替代品。**该引用不可依赖** —— 需要 md3 任意 VA 反汇编器时须另找或重写 | 交接文档 `:269` vs 目录实测 |
| V5 | 固件侧静态工作（引导块、图像算法）照常推进，不依赖实机 | 事故报告 §5 行动清单第 5 条 |

---

## 6. 打包附：本册引用源清单

事故原文、ioctl 协议定案、安全策略 → `03_analysis\live\INCIDENT-20241024-实机协议与蓝屏.md`
护栏实现细节 → `03_analysis\live\ps_readonly.ps1`（`$ALLOW` / `$SAFE_ONLY` / `Send-Query` / `$queries`）
崩溃请求序列 → `03_analysis\live\ps_probe6.ps1`（`$T` 请求表 8 条）
2340 组扫描参数 → `03_analysis\live\ps_brute.ps1`（`$IOCTLS`/`$FAMS`/`$SIZES`/`$LENVALS`/`$BUFS`）
三缓冲同印（数据在输出缓冲） → `03_analysis\live\ps_probe5.ps1`
授权边界、三级命令序列、红线 → `REPORT_实机验证方案.md`
跨会话交接、环境坑位 → `REPORT_实机验证交接.md`
驱动侧反汇编依据 → `03_analysis\firmware\_jobfuncs\analyze_scsiscan_ioctl.py`（事故报告 §3 列出）

**本册编写过程**：只读静态阅读 + 文件大小实测 + CTL_CODE 位运算核对（并经 disasm 驱动侧反汇编独立复算）+ 目录存在性核对 + 8 个 ps 脚本 `INQ36` 出现次数全量统计。

**合规声明**：**未执行任何 `ps_*.ps1`、未执行 `scsi_readonly.py`、未向扫描仪发送任何命令、未写入 `D:\`、未修改任何已有文档**（源文件修正由 team-lead 另派 `apply-ioctl-fixes` 执行）。本册仅新建/更新 `03_analysis\status\LIVE_LINE_INDEX.md` 一个文件。

**本册与配套文档的关系**：`IOCTL_0x190012_METHOD_VERDICT.md`（disasm，驱动侧反汇编证据）· `VERDICT_IOCTL_0x190012.md`（verdict-ioctl，位域与行为总裁决）· 本册（实机线清单与安全红线）—— 三者口径已对齐，冲突时以 §0.1 校订清单为准。
