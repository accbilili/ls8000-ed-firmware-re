# 实机验证工作 · 交接报告

> 用途：粘贴到新一轮对话，让对方零上下文接手。
> 起点：2026-10-24 20:30 提问「如果我把 8000ed 扫描仪连接到电脑上对你有帮助吗」。
> 截止：2026-10-24 22:15。**全程只读，未向扫描仪发送过任何一条成功的 SCSI 命令。**

---

## 0. 一句话现状

项目是 Nikon Super Coolscan 8000 ED 扫描仪的 H8/300H 固件逆向（228,345 B 应用区）+ 主机驱动链拆解，**L3 已完成约 92–94%**。

本轮的全部工作围绕一个问题：**剩下的硬缺口（引导块 `0x0–0xFFFF`，静态分析已穷尽）能否用实机补上。**

结论：**能，而且比预期容易——扫描仪一直在线、链路全通、ioctl 码已钉死。只差结构体布局这一个点没拿下。**

---

## 1. 为什么"连接扫描仪"有价值

分两种，价值和风险都不同：

| 方式 | 能拿到什么 | 设备风险 | 状态 |
|---|---|---|---|
| **纯观察**：你用 NikonScan 4.0.3 正常操作，我用 API 监控抓 `DeviceIoControl` | 一次真实扫描的**完整 CDB 字节流 + 顺序 + 参数** | 零（纯被动） | **推荐下一步** |
| **主动命令**：我发 READ BUFFER | 可能拿到 64 KB 引导块，补上唯一结构性缺口 | 小但非零（见 §4） | 受阻于 §5 |

**"观察"这条路本身就有独立价值**，且不依赖任何 ioctl 逆向成功：
- `0x40/0x41/0x42` 的真实参数值 → 顺带解决 15354/450/3283 那个悬案（原 §11.4 的数值出处至今未证，已升级为待办 B15）
- `0xD1` 到底会不会真被发出去（静态已证"主机有能力发、固件必然拒"，但没实证）
- `0x03EDE8` 作业表那 11 个处理函数里哪些真被走到（当前最大未解项）
- 进片/校准/扫描各阶段的实际时序

---

## 2. 发现一：驱动是原厂 + AI 兼容补丁（已字节级核实）

### 2.1 补丁范围极小，且没碰代码

已安装副本（`C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\`）与我分析的原版副本（`D:\DS\TEST\LS8000\driver\`）**大小相同（958,464 B）但哈希不同**。逐字节 diff：

| 节 | 大小 | 差异字节 |
|---|---|---|
| `.text` | 774,144 | **0** |
| `.rdata` | 77,824 | **0** |
| `.data` | 32,768 | **0** |
| `.reloc` | 40,960 | **0** |
| `.rsrc` | 28,672 | 13,878 |
| PE 头 | 4,096 | 2 |

合计 1.45%，全在 `.rsrc` 和 PE 头。PE 头那 2 字节在 `0x184`，落在 OptionalHeader（@`0x110`）的 **DataDirectory[2]（Resource）的 Size 字段**——为配合资源区大小变化而改的元数据。

**→ AI 兼容补丁只重写了版本资源 + 对应 PE 元数据。`LS8000.md3` 上得出的全部结论（268 个能力 ID 分类、18 条 CDB 构造点、5 个 opcode 开关、三套 request 结构、三套 selector 编号、主机不做数值校验）对设备实际运行的那份 100% 成立。**

其余 DLL（`NKDUSCAN.dll`、`NKDSBP2.dll`、`ICEDLL.dll`、`ICENKNL1/2.dll`）与原厂**逐字节一致**。

### 2.2 原厂 1394 传输驱动包的内容

`…\Nikon Scan 4.0.3\NikonScan403\INF\1394\`：

| 文件 | 大小 | 说明 |
|---|---|---|
| `Nks1394.INF` / `nks1394.cat` | 2,473 / 7,914 B | 1394 总线层 |
| `NKScnUSD.dll` | 6,545 B | 用户态桩，与 `INF\USB\` 下同名文件**哈希相同**（`5F8EDA9B…`） |
| `Win98SE\scsiscan.sys` | 10,576 B | **微软 SCSI 扫描仪类驱动** |
| `Win98SE\NS1394SE.INF` | 2,401 B | Win98SE 专用 |

**关键推论：`IOCTL_SCSISCAN_CMD` 来自微软 `scsiscan.sys`，不是 Nikon 实现。** 这改变了方案的一个前提——能否走通取决于 `1394 OHCI → SBP-2 → scsiscan.sys` 这条枚举链在现代 Windows 上是否成立（结论：成立，见 §5）。

### 2.3 设备路径是运行时枚举的

`LS8000.md3` 导入表含 `SetupDiGetClassDevsA` / `SetupDiEnumDeviceInfo` / `SetupDiGetDeviceRegistryPropertyA` / `SetupDiClassGuidsFromNameA` / `RegOpenKeyExA`，字符串里有 `'SCSI'` / `'USB'` / `'IEEE1394'` 三个类名。**路径不硬编码**，DLL 里也没有路径字符串。

（这些 API 在 md3 里是 `GetProcAddress` 动态解析的，`.text` 里没有 IAT 直接引用——所以静态追不出属性索引，只能按同样方式在宿主里复现。）

---

## 3. 发现二：READ BUFFER 的白名单有**两张**，READ 侧覆盖引导块

这是 Tier 2 能成立的关键。

| | 基址 | 条目数 | 内容 |
|---|---|---|---|
| **WRITE** 白名单 | `0x03ED60` | 5 | `0x6000–0x607F`(128 B) / `0x400000–0x43FFFF` / `0x800000–0x8FFFFF` / `0xC00000–0xC3FFFF` / `0xC40000–0xC7FFFF` |
| **READ** 白名单 | **`0x03ED88`** | 6 | **`0x00000000–0x0007FFFF`** / `0x400000–0x43FFFF` / `0x800000–0x8FFFFF` / `0xC00000–0xC3FFFF` / `0xC40000–0xC7FFFF` / `0x00FFDC00–0x00FFFFFF` |

判决性代码在 READ BUFFER handler `0x0267AA`：

```asm
0x02683E  er0 = idx*8 + 0x0003ed88     ; ★ READ 白名单基址是 0x03ED88，不是 0x03ED60
0x026850  er0 = @er0                    ; start
0x026854  cmp.l er0, er6 ; bcs 下一条   ; offset < start → 换下一条
0x02685A  er0 = @(er1+4)                ; end
0x026860  cmp.l er0, er6 ; bhi 下一条   ; offset > end → 换下一条
0x0268A0  inc.b #1, r4l
0x0268A2  cmp.b #0x06, r4l ; bcs 循环   ; 6 条，穷尽后拒绝
```

**READ 白名单第 0 条完整覆盖引导块 `0x0–0xFFFF`，也覆盖应用区 `0x10000–0x47BF8`。而 WRITE 侧只开了一个 128 字节小窗。这个不对称正是我们要的：整片 flash 可读，几乎不可写。**

### 3.1 mode 2 是纯读，mode 5 会动 flash 解锁序列

`0x0267BE` 起：`mode = CDB[1] & 0x1F`，只接受 **2** 和 **5**，其余返回状态 `0x50`。

| mode | 路径 | 行为 |
|---|---|---|
| **2** | `0x02682A`→`0x026898` | 查 READ 白名单 → `jsr 0x011900` → `0x013d98` → `0x013872`：`bsr 0x012bc4` 从 offset 拷到 `0x008DC000`（ASIC 图像缓冲），写 ASIC 寄存器 `0x2000C7=0xDC`、`0x2000C2=0x80`，`bsr 0x013580/0x0135b8` 启 DMA。**不写任何 flash 寄存器** |
| 5 | `0x0268A8`→`0x0268F4` | `offset += 0x60000`，分块拷贝，每轮写 `0x5A00` 到 `0xFFFFBC`（**flash 写保护解锁序列**）。**方案不走** |

### 3.2 长度限制

- `0x011906 mov.w r1, r4` —— 长度按 **16 位寄存器**取，**单次上限 65535 B**
- `0x02687A` 用白名单条目 end 的高 16 位做上界裁剪 → **物理上不可能读到白名单外**

---

## 4. 发现三：Tier 2 的风险评估（已排除灾难性后果）

**已排除：**

| 风险 | 排除依据 |
|---|---|
| **写入 flash** | mode 2 分支**无任何 flash 写指令**；解锁序列只在 mode 5（`0x0268F4`） |
| **越界读** | offset 先过 `0x03ED88` 六条白名单，长度再被 end 高 16 位裁剪（`0x02687A`） |
| **缓冲区溢出** | 长度按 16 位取，上限 65535 |

**残余风险（小额但真实，不隐瞒）：这条路径过 ASIC/DMA 暂存引擎，而 DMA 引擎是有状态的。** 若引擎处于异常态（上次操作出错未恢复），命令**可能挂住或返回错误**；最坏现实后果是超时（SCSI 层可恢复）或 ASIC 进入需复位的瞬态，**不涉及 flash 内容改变**。

诚实记录：`0x0146ea` / `0x0152b0` / `0x015300` / `0x015256` / `0x013608` / `0x013580` / `0x0135b8` 这几个 setup/teardown 子例程**未追完**，所以不能说"零风险"。

**关键旁证**：`0x011900`（暂存拷贝）在全镜像有 **14 处 `jsr` 调用者**，其中包括 MODE SELECT(`0x02182C`)、START STOP UNIT(`0x021D54`)、SEND DIAGNOSTIC(`0x022D86`)、WRITE(10)(`0x023A1E`)、参数块校验引擎(`0x025A42`)、片夹处理(`0x02724C`)——**全是 NikonScan 正常使用时天天发的普通命令**。READ BUFFER mode 2 调用的不是特殊危险路径，而是被六类普通命令共用的标准 helper。

**缓解措施**：块长 4096 B；金丝雀两步（① 只读 64 B → ② 读 `0x10000` 起 4 KB 与镜像逐字节比对）都正常才读引导块；任一步非预期 sense 立即停止不重试；备 `E0 0x80` reset 与断电重启。

---

## 5. 发现四：实机状态（**设备一直在线**）

```
SBP2  1394\NIKON___&LS-8000_ED______\0090B54002FFFFFF        Status=OK  svc=sbp2port
Image SBP2\NIKON___&LS-8000_ED______&LUN0\0090B54002FFFFFF   Status=OK  svc=scsiscan
已加载: 1394ohci.sys(1394ohci) / sbp2port.sys(sbp2port) / scsiscan.sys(scsiscan)  全 Running
本机:   Texas Instruments 1394 OHCI Compliant Host Controller，Status=OK
```

**1394 → SBP-2 → scsiscan 链路完全正常，不需要用户再插线。**

### 5.1 ioctl 码已钉死

从 `NKDSBP2.dll`（ImageBase `0x10000000`）反汇编 `0x10002B66`：

```asm
0x10002B55  push   edi                ; &bytesReturned
0x10002B56  push   ebp                ; nOutBufferSize
0x10002B57  push   eax                ; (esi+0x28)
0x10002B5C  push   edx                ; lpOutBuffer  = [ecx+0x20]
0x10002B5D  push   0x2c               ; nInBufferSize = 44
0x10002B5F  push   ebx                ; lpInBuffer   = esi+0x18
0x10002B60  push   0x190012           ; dwIoControlCode  ★
0x10002B65  push   eax                ; hDevice
0x10002B66  call   dword ptr [0x1000e030]   ; DeviceIoControl
```

**`0x190012` = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`，输入结构 44 字节（`SCSI_PASS_THROUGH` 布局）。**〔R24：驱动侧实测更正 —— 原写 `METHOD_BUFFERED` 的宏展开是 `0x190010`，与本码不符；驱动输出侧走 MDL + `MmMapLockedPages` 直写用户页、`Irp->UserBuffer` 访问 0 次，排除 NEITHER。**注意**：数据出现在「输出缓冲」这一**实测现象不变**，只是机制归因更精确。〕

注意：**不是 `IOCTL_SCSISCAN_CMD`（function 1）**。实测印证：
- `0x190012` → **err=87**（ERROR_INVALID_PARAMETER）→ 码被识别，进了参数校验分支
- `0x190004` / `0x194004` / `0x190008` → **err=50**（连分发都没进）

错误处理与重试（同处反汇编）：997(ERROR_IO_INCOMPLETE) 视为成功；1453(ABORTED) 时最多重试 **200 次 × Sleep 50 ms**（总 10 s）；最终失败状态码 **`0x21008`**。

`NKDSBP2.dll` **只有一个导出**：`NkDriverEntry`@`0x100041D0`。

### 5.2 2340 组暴力扫描，未命中

在 32 位宿主里以 **INQUIRY (0x12) 为唯一命令**（必须逐字节等于已知 36 字节模板才算命中），扫了：

- ioctl 码 × 5（`0x190012` / `0x190004` / `0x194004` / `0x190008` / `0x190014`）
- 结构族 × 2（`SEND_SCSI_CMD` / `SCSI_PASS_THROUGH`）
- 结构总长 35–56 字节
- 长度字段值（= 总长 / = 0）
- 数据缓冲区指针偏移与宽度（26/4、32/8、24/8、20/4、28/8、36/8）

结果：**err=50 × 1872，err=87 × 468，零成功。**

自查出的自身 bug（记下来以免重犯）：`SCSI_PASS_THROUGH` 族里 CDB 放在偏移 6，与 `SenseInfoLength` 字段**同址**，后写者把 CDB[0] 覆写成 0。`SEND_SCSI_CMD` 族无此问题，其 468 次 err=87 属真实拒绝。

### 5.3 一个还没解释的矛盾

已加载的 `scsiscan.sys` 来自 `DriverStore\FileRepository\sti.inf_amd64_14dc9a213197a8b8\scsiscan.sys`，是**微软 64 位 in-box 版**；而 `NKDSBP2.dll` 是 32 位、发的结构体是 44 字节。**32 位进程怎么和 64 位驱动在 `0x190012` 上达成一致，目前无解释。** 三种可能：

- (a) in-box 驱动为扫描仪类保留了历史 32 位打包布局
- (b) `\\.\Scanner0` 其实是 WIA 节点，真正的 scsiscan 节点另有名
- (c) AI 兼容补丁另有未被我发现的改动（`.text` 全等已排除，但驱动栈里可能还有别的文件被换过）

**这条不查清，继续盲扫就是浪费。**

---

## 6. 发现五：各命令的 CDB 字节格式（从主机侧构造器反推，已验证）

| 命令 | 构造器 | CDB | 长度 |
|---|---|---|---|
| INQUIRY | `0x100A01A0` | `12 00 <page> 00 <len> 80` | 6 |
| TEST UNIT READY | — | `00 00 00 00 00 00` | 6 |
| REQUEST SENSE | — | `03 00 00 00 FC 00` | 6 |
| MODE SENSE(6) | — | `1A 00 <page> 00 FC 00` | 6 |
| C1 EXECUTE | `0x100A0190` | `C1 00 00 00 00 00` | 6 |
| **E0 机构控制** | `0x100A0230` | `E0 00 <sub> 00 00 <p2> <p1> <p0> 00 00` | 10 |
| **E1 读状态** | `0x100A0260` | `E1 00 <sub> 00 00 <p2> <p1> <p0> 00 00` | 10 |
| **READ BUFFER** | — | `3C 02 00 <off[3] BE> <len[3] BE> 00` | 10 |

E0/E1 的 24 位参数取自对象 `+0x50`，**大端**填 CDB[6..8]；子功能码取自对象 `+0x64` → CDB[2]。

E0 的 12 个子功能（表 `0x03EDB8`，2 字节/条 `[sub][最小长度]`，`0xFF` 终止）：

```
80 00 | 81 00 | A0 09 | B0 00 | C1 05 | D0 00
40 0B | 41 0B | 42 0B | 91 05 | 92 05 | B3 0D | FF
```

固件侧执行层 `0x0269A6` 的 12 路开关落点：`0x40/41/42`→`0x026A3E`、`0x80`→`0x026A2E`、`0x81/B0/D0`→`0x026BD2`、`0x91`→`0x026BB2`、`0x92`→`0x026BBE`、`0xA0`→`0x026A92`、`0xB3`→`0x026B0A`、`0xC1`→`0x026A54`、default→`0x026BCA`（状态 `0x56`）。

---

## 7. 授权边界（**请严格遵守**）

用户在过程中两次明确表态：

1. **「不要做对机器有风险的操作」** → 所有实机命令暂停
2. **「可以只读设备」** → Tier 1 纯查询 + Tier 2 READ BUFFER 获授权；**Tier 3（E0 机构命令）取消**（用户另明确「先不扫描胶片和动机器的」）

**当前有效边界：只读。不扫片、不动电机、不发 WRITE BUFFER（`0x3B`）任何 mode、不用 READ BUFFER mode 5。**

**至今未向扫描仪发送过任何一条成功的 SCSI 命令**——所有 INQUIRY 尝试都在驱动参数校验阶段被拒（err=87），从未产生实际 SCSI 交互。

---

## 8. 下一步三选一

| 方案 | 做法 | 代价 | 风险 | 备注 |
|---|---|---|---|---|
| **① 观察真实会话（推荐）** | 跑 NikonScan 4.0.3，用 API 监控抓 `DeviceIoControl` 的 **ioctl 码 + 44 字节入参原始内容** | 需装一个监控工具（管理员权限） | 零 | 一次真实扫描即可钉死布局；**并顺带产出完整 CDB 流**，独立价值极高（见 §1） |
| ② 继续暴力 | 再扫 `bDirection` / `TimeoutValue` / `CdbLength` / `TargetId` / `LunId` / `SenseInfoLength` 各维度 | 不确定 | 零（只发 INQUIRY） | 维度还多，收益递减 |
| ③ 走驱动自己的 API | 直接调 `NKDSBP2.dll!NkDriverEntry(sel, request, ctx)`（该 DLL 唯一导出），请求布局已从 md3 侧确认 | 需再逆 md3 侧调用点确认 selector | 零（只发 INQUIRY） | 绕开 ioctl 结构体问题 |

**先做 §5.3 那条矛盾的查证**（确认 `\\.\Scanner0` 是不是 scsiscan 节点、驱动栈里还有没有别的文件被换过），再选 ①/②/③。

---

## 9. 文件地图

项目根：`<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\`

| 路径 | 内容 |
|---|---|
| `REPORT_实机验证方案.md` | **主文档**。含 §0-A 授权边界、§0-B 传输层静态核实、§0-C 只读探测实录、§2 补丁比对、§2.4 Tier 2 风险评估、§3 命令序列与红线 |
| `LS8000-全案总结.md` | 13 节全案总结，可独立阅读，不依赖主报告 |
| `REPORT_L3-交接定稿.md` | L3 主报告（1787 行，已回写本轮 10 条修正） |
| `HANDOFF.md` | 全项目新对话交接单 |
| `film-holder-spec.html` | 片夹孔位图案交互解码器（自校验通过 7/7） |
| `03_analysis\live\scsi_readonly.py` | 只读工具（**当前暂停使用**，文件头有安全边界声明；64 位 Python，结构体布局与 32 位驱动不兼容） |
| `03_analysis\live\ps_probe.ps1` | 32 位 PowerShell 探测（INQUIRY only，ASCII-only 源码） |
| `03_analysis\live\ps_probe2.ps1` | ioctl × 结构布局矩阵版 |
| `03_analysis\live\ps_brute.ps1` | 2340 组暴力扫描版 |
| `03_analysis\live\drv_ioctl.py` | NKDSBP2.dll 的 ioctl 调用点反汇编（ioctl 码与结构体来源） |
| `03_analysis\live\drv_paths.py` | 驱动导入表与设备路径字符串挖掘 |
| `03_analysis\live\md3_setupdi.py` | md3 的 SetupDi 调用点定位 |
| `03_analysis\live\md3dis.py` | ⚠️ **该文件不存在**（`live\` 目录实测 13 个文件，无 `md3dis.py`）—— 原「md3 任意 VA 区间反汇编器」条目**指向失效**，不可依赖；同目录的 `md3_setupdi.py` 是另一个东西（定位 md3 的 SetupDi 调用点），并非其替代品 |
| `03_analysis\firmware\e0_bridge.md` | E0/CDB 全通路（174 行） |
| `03_analysis\firmware\hostcode_source.md` | host_code 来源定案（387 行） |
| `03_analysis\firmware\table_01914A.md` | sense 三元组表（281 行） |
| `03_analysis\md3\cap_to_cdb.md` | 268 能力 ID 分类（126 行） |
| 样本（**只读**） | `D:\DS\TEST\LS8000\LS8000_111_ROM.bin`（固件，地址 = 文件偏移 + `0x10000`，**大端**）／`D:\DS\TEST\LS8000\driver\LS8000.md3` |

---

## 10. 环境要点（会重复踩的坑）

1. **必须 32 位宿主**。驱动是 32 位 x86，从 64 位进程发 ioctl 时结构体里的指针字段必须是 32 位值，而 64 位进程的用户态指针普遍 > 4 GB。可行宿主：`C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`（`[IntPtr]::Size` = 4，已确认存在）。
2. **32 位 PowerShell 按 ANSI/GBK 读 .ps1**。`.ps1` 源码必须纯 ASCII，否则中文把字符串引号搞乱（已踩过一次，报"字符串缺少终止符"）。
3. **ctypes 必须显式设 `restype`**。否则 `CreateFileW` 的失败返回值被截断成 32 位，与 64 位 `INVALID_HANDLE_VALUE` 永不相等 → **失败被误判为成功**（已踩过一次，导致 32 个设备路径全部"打开成功"）。
4. **ctypes 结构体里的指针字段用 `c_ulong`（固定 4 字节）而不是 `c_void_p`**。64 位 Python 下 `c_void_p` 是 8 字节，会让 32 位驱动的结构体布局整体错位（已踩过一次）。
5. **Bash 调 PowerShell 会被安全策略挡**（"Invoking PowerShell from Bash bypasses PowerShell security checks"）。要用 PowerShell 工具。
6. **COM 对象实例化被挡**（WIA.DeviceManager 起不来）。WIA 路线不可用。
7. **H8/300H 是大端**；`h8.lst` 把 `0x4000`/`0x5800` 命名成 `bt` 实为 `BRA`，按"T 置位才跳"读会把条件判反。
8. **子 agent 必须前台并行**，后台模式约 2 分钟后被系统回收且静默变 `killed`（本轮因此白跑过一轮 10 路任务）。

---

## 11. 给下一轮的一句话

> 固件和主机侧都已拆到对接面，`host_code` 是状态码不是命令码这个坑已踩过并回写主报告。实机这条路：设备在线、ioctl 码 `0x190012` 已钉死、只差 44 字节结构体布局没拿下——**先查清 32 位进程 vs 64 位 in-box 驱动那个矛盾，再决定是抓真实会话的 trace 还是继续暴力。**
