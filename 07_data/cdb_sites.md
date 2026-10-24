# F5 定稿：LS8000.md3 主机侧 CDB 构造点全表

样本 `D:\DS\TEST\LS8000\driver\LS8000.md3`（PE32，ImageBase `0x10000000`，`.text` `0x10001000`，`.rdata` `0x100BE000`），只读。
本文所有地址均为 VA。证据分级遵循 BRIEF §4：`[实证]` / `[推断]` / `[未证]`。

## 0. 一句话结论

- md3 内共有 **18 个 CDB 构造点**（17 个不同 CDB[0]，0x15 有两个构造点），全部经机器码复核通过。
- 补搜 4 条：`0x00` TUR、`0x16` RESERVE **找到**；`0x03` REQUEST SENSE、`0x17` RELEASE **判定 md3 内未构造**。
- 子功能码由工厂 `0x100AA1D0` 白名单化（写入命令对象 `+0x456`），经 E0/E1 构造函数复制到 CDB 对象 `+0x64`，最终由 E0/E1 的 BuildCDB 落进 **CDB[2]**。
- **主机侧不做与固件相同的数值范围校验**（15354/450/3283/±300 全部未在 md3 中出现为比较常量）。
- **`0xD1` 是真会被发出的子功能码**：构造链 `0x100997C6 → 0x100A1EC0 → 0x100AA1D0` 对 `0xD0..0xD6` 全区间放行，`0xD1` 落在其中。

---

## 1. 命令全表（14 已知 + 4 补搜 + 2 顺带发现）

构造函数签名统一为 `int __fastcall BuildCDB(this* @ecx)`：CDB 缓冲位于 `[this+8]`，`CDB[i] = [this+8+i]`，返回值 `eax` = CDB 长度。
`func` = BuildCDB 入口；`site` = 写 CDB[0] 的指令地址；`长度常量` = `mov eax, 6|10` 的地址；`callers` = 该类构造函数（`mov dword ptr [this], <vtable>` 所在函数）的调用点，最多 5 个。

| # | CDB[0] | 名称 | func | site | 长度常量 | vtable | ctor | 参数校验 / CDB 字段来源 | 上层调用者（≤5） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `0x00` | TEST UNIT READY | `0x1009FEB0` | `0x1009FEB0` | 6 @`0x1009FEB4` | `0x100C28D4`/`0x100C2974` | `0x1009FD20`/`0x1009FE80` | 无参数，CDB 全 0 | `0x10093D9C` `0x100941D0` `0x10094AB0` `0x100A4DE8` `0x100A603C` |
| 2 | `0x03` | REQUEST SENSE | — | — | — | — | — | **md3 内未构造** | — |
| 3 | `0x12` | INQUIRY | `0x100A01A0` | `0x100A01A5` | 6 @`0x100A01BF` | `0x100C299C` | `0x1009FEC0` | `[+0x64]!=0 → CDB[1]|=1`(EVPD)；CDB[2]=`[+0x68]`；CDB[4]=`[+0x50]`；CDB[5]=`0x80` | `0x100A4E8E` `0x100A7443` `0x100A7C15` `0x100A7EBD` `0x100A7F2B` |
| 4 | `0x15` | MODE SELECT(6) [a] | `0x1009FDB0` | `0x1009FDBE` | 6 @`0x1009FDB9` | `0x100C2924` | `0x1009FD60` | CDB[1]=`0x10`、CDB[4]=`0x14`(固定 20)；另置 `[+0x63]=8 [+0x6b]=1 [+0x6c]=3 [+0x6d]=6 [+0x70]=[+0x5d] [+0x71]=[+0x5c]` | `0x1009402A` |
| 5 | `0x15` | MODE SELECT(6) [b] | `0x100A0070` | `0x100A007E` | 6 @`0x100A0079` | `0x100C2A64` | `0x100A0020` | 同 [a]，替换为 `[+0x73]=1 [+0x74]=3 [+0x75]=6 [+0x78]=[+0x65] [+0x79]=[+0x64]` | `0x100A4FB7` |
| 6 | `0x16` | RESERVE(6) | `0x1009FF40` | `0x1009FF40` | 6 @`0x1009FF44` | `0x100C29C4` | `0x1009FF10` | 无参数 | `0x100A4ED0` |
| 7 | `0x17` | RELEASE(6) | — | — | — | — | — | **md3 内未构造** | — |
| 8 | `0x1A` | MODE SENSE(6) | `0x1009FE60` | `0x1009FE69` | 6 @`0x1009FE74` | `0x100C294C` | `0x1009FDE0` | CDB[1]=`0x18`(DBD)；CDB[2]=`[+0x5c]`(page code)；CDB[4]=`[+0x50]` | `0x10094101` |
| 9 | `0x1B` | START STOP UNIT | `0x100A0290` | `0x100A0296` | 6 @`0x100A029A` | `0x100C2ADC` | `0x100A0120` | CDB[4]=`[+0x50]` | `0x100A9F92` |
| 10 | `0x1D` | SEND DIAGNOSTIC | `0x1009FF80` | `0x1009FF80` | 6 @`0x1009FF88` | `0x100C28FC`/`0x100C29EC` | `0x1009FD40`/`0x1009FF50` | CDB[1]=`4`(自测码) | `0x10093E08` `0x1009423A` `0x100A4FF9` `0x100A61D2` `0x100A6B2B` |
| 11 | `0x24` | SET WINDOW | `0x100A0210` | `0x100A021E` | 10 @`0x100A0229` | `0x100C2A3C` | `0x1009FFE0` | CDB[6..8]=`[+0x50]` 24 位；CDB[9]=`0x80` | `0x100A98F9` `0x100A9B34` `0x100A9DA9` `0x100AA00E` `0x100AA789` |
| 12 | `0x25` | GET WINDOW | `0x100A01D0` | `0x100A01E8` | 10 @`0x100A0205` | `0x100C2A14` | `0x1009FF90` | CDB[6..8]=`[+0x50]`；CDB[9]=`([+0x66]\|0xFE)<<6`；`word[+0x64]!=0 → CDB[1]|=1` 且 CDB[5]=`[+0x64]` | `0x100A4F68` `0x100A5B3B` `0x100A9C0A` `0x100AA0A6` |
| 13 | `0x28` | READ(10) | `0x100AAD00` | `0x100AAD20` | 10 @`0x100AAD2B` | `0x100C303C` | `0x100AAB30`/`0x100AAB90` | CDB[2]=`[+0x64]`；CDB[4]=`[+0x66]`；CDB[5]=`[+0x68]`；CDB[6..8]=`[+0x50]`；CDB[9]=`0x80` | `0x100A3B12` `0x100A3B62` `0x100A5088` `0x100A6877` `0x100A7518` |
| 14 | `0x2A` | WRITE(10) | `0x100AAD50` | `0x100AAD70` | 10 @`0x100AAD77` | `0x100C3064` | `0x100AABF0` | 同 READ(10)（**不写 CDB[9]=0x80**） | `0x100A3AAA` `0x100A695C` `0x100AA161` |
| 15 | `0x3B` | WRITE BUFFER | `0x100AADC0` | `0x100AADEC` | 10 @`0x100AADF3` | `0x100C30B4` | `0x100AAC90` | CDB[1]=`[+0x64]`；CDB[2]=`[+0x66]`；CDB[3]=`[+0x6a]`；CDB[4]=`[+0x69]`；CDB[5]=`[+0x68]`；CDB[6..8]=`[+0x50]` | `0x100A3D56` |
| 16 | `0x3C` | READ BUFFER | `0x100AAD80` | `0x100AADAC` | 10 @`0x100AADB3` | `0x100C308C` | `0x100AAC40` | 同 WRITE BUFFER | `0x100A3D07` |
| 17 | `0xC0` | CANCEL | `0x100AAE20` | `0x100AAE20` | 6 @`0x100AAE24` | `0x100C30DC` | `0x100AAE00` | 无参数 | `0x100A43F4` |
| 18 | `0xC1` | EXECUTE | `0x100A0190` | `0x100A0190` | 6 @`0x100A0194` | `0x100C2B04` | `0x100A0160` | 无参数；**CDB 内不携带子功能码**（构造函数 `0x100A0160` 只置 `[+0x5c]`，BuildCDB 只写 CDB[0]） | `0x100A60F8` `0x100A6A81` |
| 19 | `0xE0` | MECHANISM CONTROL | `0x100A0230` | `0x100A0244` | 10 @`0x100A024B` | `0x100C2A8C` | `0x100A00A0` | **CDB[2]=`[+0x64]`=子功能码**（`0x100A0233`）；CDB[6..8]=`[+0x50]` | `0x100A60BD` `0x100A6A3F` |
| 20 | `0xE1` | READ STATUS | `0x100A0260` | `0x100A0274` | 10 @`0x100A027B` | `0x100C2AB4` | `0x100A00E0` | **CDB[2]=`[+0x64]`=子功能码**（`0x100A0263`）；CDB[6..8]=`[+0x50]` | `0x100A6190` `0x100A6AEC` |

统计：**20 行命令，18 行有构造点**；`0x15` 有两个构造点（两套不同字段偏移，对应两个不同 vtable），`0x1D` SEND DIAGNOSTIC 是本次顺带发现的第 17 个 CDB[0]。

---

## 2. 判定依据：为什么某个 `mov byte ptr [x], imm8` 就是 CDB[0]

### 2.1 判据（三条同时成立才记为构造点）`[实证]`

1. **落点固定**：指令形如 `mov byte ptr [ecx + 8], imm8`，基址为**非栈寄存器**（排除 `esp`/`ebp`），位移恰为 `+8`。
   → 该对象 `+0` 是 vptr（构造函数里 `mov dword ptr [esi], <.rdata 地址>`），`+8` 起是 CDB 字节区：`[+8]`=CDB[0]、`[+9]`=CDB[1]、`[+0xA]`=CDB[2]、…、`[+0x11]`=CDB[9]。
2. **紧邻 CDB 长度常量**：同一函数内必有一条 `mov eax, 6` 或 `mov eax, 0xA`（10），且该常量仅出现在 CDB 构造语义中（SCSI-2 的 6 字节 / 10 字节 CDB 长度）。
3. **字段语义自洽**：`[+9]/[+0xA]/[+0xC]/[+0xD]/[+0xE..0x11]` 的写入内容与对应 SCSI 命令的字段定义对得上（见 2.2 三例）。

补充对照（来自 `dispatch.md`，`[实证]`）：`NkCtrlEntry` 的 request 结构中 `request+0x14` = CDB 长度、`request+0x18` = CDB 指针；BuildCDB 的返回值 `eax` 正是写入 `request+0x14` 的那个长度，而 `request+0x18` 指向的正是 `[this+8]`。这条"长度/指针配对"把上面的 1、2 两条钉死。

### 2.2 例证一：INQUIRY `0x12`（`0x100A01A0`）

```
0x100A01A0  mov  eax, dword ptr [ecx + 0x64]
0x100A01A3  test eax, eax
0x100A01A5  mov  byte ptr [ecx + 8], 0x12      <<< CDB[0] = 0x12
0x100A01A9  je   0x100A01AF
0x100A01AB  or   byte ptr [ecx + 9], 1         ; CDB[1] |= 1  → EVPD
0x100A01AF  mov  al, byte ptr [ecx + 0x68]
0x100A01B2  mov  dl, byte ptr [ecx + 0x50]
0x100A01B5  mov  byte ptr [ecx + 0xa], al      ; CDB[2] = page code
0x100A01B8  mov  byte ptr [ecx + 0xc], dl      ; CDB[4] = allocation length
0x100A01BB  mov  byte ptr [ecx + 0xd], 0x80    ; CDB[5] = control = 0x80
0x100A01BF  mov  eax, 6                        ; CDB 长度常量 = 6
0x100A01C4  ret
```
INQUIRY 的 6 字节 CDB 定义正是 `[0]=0x12, [1]=EVPD<<0, [2]=page code, [3..4]=allocation length(2B), [5]=control`。这里 CDB[3] 未写（保持 0），CDB[5] 固定 `0x80`，与 SPC 的 control 字节完全一致。`[+0x64]!=0 → CDB[1]|=1` 就是 EVPD 分支。**判定：`0x100A01A5` 即 CDB[0]。**

### 2.3 例证二：MODE SENSE(6) `0x1A`（`0x1009FE60`）

```
0x1009FE60  mov  al, byte ptr [ecx + 0x5c]
0x1009FE63  mov  dl, byte ptr [ecx + 0x50]
0x1009FE66  mov  byte ptr [ecx + 0xa], al      ; CDB[2] = page code
0x1009FE69  mov  byte ptr [ecx + 8], 0x1a      <<< CDB[0] = 0x1A
0x1009FE6D  mov  byte ptr [ecx + 9], 0x18      ; CDB[1] = 0x18 → DBD=1
0x1009FE71  mov  byte ptr [ecx + 0xc], dl      ; CDB[4] = allocation length
0x1009FE74  mov  eax, 6                        ; 长度常量 = 6
0x1009FE79  ret
```
MODE SENSE(6) 定义：`[0]=0x1A, [1]=DBD<<3|PC, [2]=page code, [3]=subpage, [4]=allocation length, [5]=control`。`0x18 = 0b11000` 即 DBD(bit3)=1、PC=0，完全合法。**判定：`0x1009FE69` 即 CDB[0]。**

### 2.4 例证三：READ(10) `0x28`（`0x100AAD00`）

```
0x100AAD00  mov  al, byte ptr [ecx + 0x64]
0x100AAD03  mov  dl, byte ptr [ecx + 0x66]
0x100AAD06  mov  byte ptr [ecx + 0xa], al      ; CDB[2]
0x100AAD09  mov  al, byte ptr [ecx + 0x68]
0x100AAD0C  mov  byte ptr [ecx + 0xd], al      ; CDB[5]
0x100AAD0F  mov  eax, dword ptr [ecx + 0x50]
0x100AAD12  mov  byte ptr [ecx + 0xc], dl      ; CDB[4]
0x100AAD15  mov  edx, eax
0x100AAD17  shr  edx, 0x10
0x100AAD1A  mov  byte ptr [ecx + 0xf], ah      ; CDB[7] = len>>8
0x100AAD1D  mov  byte ptr [ecx + 0x10], al     ; CDB[8] = len&0xFF
0x100AAD20  mov  byte ptr [ecx + 8], 0x28      <<< CDB[0] = 0x28
0x100AAD24  mov  byte ptr [ecx + 0xe], dl      ; CDB[6] = len>>16
0x100AAD27  mov  byte ptr [ecx + 0x11], 0x80   ; CDB[9] = control
0x100AAD2B  mov  eax, 0xa                      ; 长度常量 = 10
0x100AAD30  ret
```
READ(10) 定义：`[0]=0x28, [2..5]=LBA(大端 4B), [7..8]=transfer length(大端 2B), [9]=control`；`[+0x50]` 的 dword 被拆成 `>>16 / >>8 / &0xFF` 三字节写进 CDB[6..8] —— **这是"24 位大端长度"的教科书写法**，不可能是别的结构。WRITE(10) `0x100AAD50` 与之逐指令同构。

### 2.5 反例：为什么那些"看起来像"的不是

- `mov byte ptr [esp/ebp + d], imm8`：栈槽初始化，全部排除（扫描时按基址寄存器过滤）。
- `0x03`/`0x17` 在 `.text` 全量扫描（基址非栈、位移 `0..0x40`）中分别有 100 处 / 0 处候选，**其中带 6/10 长度常量的为 0 处**（`md3\cdb\four_ops.json`）。
- `mov dword ptr [eax], 0x12`（如 `0x100A262C`）是"命令表条目"的字段写入，不是 CDB 字节写入 —— 它写的是 dword，且基址对象无 vptr/CDB 布局。

---

## 3. 补搜结论（TUR / REQ SENSE / RESERVE / RELEASE）

| CDB[0] | 名称 | 结论 | 构造点 | 依据 |
|---|---|---|---|---|
| `0x00` | TEST UNIT READY | **找到** | BuildCDB `0x1009FEB0`，site `0x1009FEB0`，长度 6 @`0x1009FEB4` | 形如 `mov byte ptr [ecx+8],0; mov eax,6; ret`，vtable `0x100C28D4`（另有 `0x100C2974`），ctor `0x1009FD20`/`0x1009FE80`，12 个调用点 |
| `0x03` | REQUEST SENSE | **md3 内未构造** | — | 见下 3.1 |
| `0x16` | RESERVE(6) | **找到** | BuildCDB `0x1009FF40`，site `0x1009FF40`，长度 6 @`0x1009FF44` | `mov byte ptr [ecx+8],0x16; mov eax,6; ret`，vtable `0x100C29C4`，ctor `0x1009FF10`，唯一调用点 `0x100A4ED0` |
| `0x17` | RELEASE(6) | **md3 内未构造** | — | 见下 3.1 |

### 3.1 搜过的形态（`0x03` / `0x17`，全部 0 命中）

在 md3 `.text`（277,966 条指令）中按以下形态穷举，均**未找到**可用构造点：

| 形态 | 说明 | 0x03 | 0x17 |
|---|---|---|---|
| A | `mov byte ptr [reg+d], imm8`，`d∈[0,0x40]`，基址非栈 | 100 处候选 | 0 处候选 |
| A′ | 形态 A 且同函数内出现 `mov eax, 6/10`（CDB 长度） | **0 处** | **0 处** |
| B | 打包 dword：`mov dword ptr [x], imm32`，其中某字节 = 目标码 | 155 处（均为无关常量/浮点位型） | 13 处（同上） |
| C | `mov byte ptr [reg+8], reg8`（子功能码由寄存器传入的间接形态） | 无 0x03/0x17 常量来源 | 同 |
| D | 工厂白名单跳转表 `0x100AA1D0`（`0x40..0x45 / 0x81..0xB3 / 0xC0..0xD1 / 0xD3,D5,D6,0x800`） | 不含 `0x03` | 不含 `0x17` |

跨模块补搜（`md3\_f5\dll.py`，同样形态 A）：

- `NKDUSCAN.dll`（`.text` `0x10001000..0x1000D41B`，10,874 条指令）：候选 11 处，**全部是 `mov byte ptr [x], 0` 的清零操作**，`0x03`/`0x16`/`0x17` 零命中。
- `NKDSBP2.dll`（`.text` `0x10001000..0x1000D68B`，11,430 条指令）：候选 14 处，同样全是清零操作，`0x03`/`0x16`/`0x17` 零命中。

**结论**：`0x03`/`0x17` 在 md3、NKDUSCAN.dll、NKDSBP2.dll 三份样本里都没有构造点。`[实证]`（就这三份样本而言）。

**下一步该查哪个模块**：优先 `NKDUSCAN.dll`。理由：它是 USB/通用扫描层，REQUEST SENSE 与 RELEASE 属于 SPC 通用族的**错误恢复/预留管理**，通常由类驱动/总线层在 autosense 流程中自动构造，而不是由设备专用插件（md3）构造。具体做法建议：
1. 在 `NKDUSCAN.dll` 里找 autosense 回调（`NkCtrlEntry` 之外的导出/虚表槽），顺着"命令失败 → 补发 REQUEST SENSE"的路径定位；
2. 若 `NKDUSCAN.dll` 也确实没有，则这两条命令由 Windows 的 `USBSTOR`/`SBP2` 系统类驱动或上层 TWAIN/WIA 数据源产生，需转去查系统驱动（`usbstor.sys`、`sbp2port.sys`）而不是厂商模块。此步超出本轮样本范围，`[未证]`。

---

## 4. E0 / C1 / E1 子功能码

### 4.1 数据流（三段）`[实证]`

```
[1] 工厂 0x100AA1D0（__stdcall，ret 0x10）
      movsx eax, word ptr [esp + 0x18]      ; 入参 = 主机命令 ID
      ...switch 白名单...
      mov  word ptr [esi + 0x456], <sub>    ; 子功能码写入命令对象 +0x456
      mov  dword ptr [esi], 0x100C2F58      ; 命令对象 vtable
      mov  dword ptr [esi + 0x45C], edi     ; 关联参数
[2] 构造函数（E0 = 0x100A00A0 / E1 = 0x100A00E0）
      mov  dx, word ptr [esp + 0x10]        ; 取子功能码实参
      mov  word ptr [esi + 0x64], dx        ; → CDB 对象 +0x64
[3] BuildCDB（E0 = 0x100A0230 / E1 = 0x100A0260）
      mov  al, byte ptr [ecx + 0x64]
      mov  byte ptr [ecx + 0xa], al         ; → CDB[2]   ★子功能码落点★
```

调用现场（E0）：`0x100A60AB` `xor ecx,ecx` / `0x100A60AD` `mov cx,[esi+0x456]` / `0x100A60B6` `push ecx` / `0x100A60BD` `call 0x100A00A0`。
调用现场（E1）：`0x100A617F` `mov dx,[esi+0x456]` / `0x100A618D` `push edx` / `0x100A6190` `call 0x100A00E0`。

### 4.2 逐个落点

| 子功能码 | 工厂写 `+0x456` 处 | 落 CDB[2] 处 | 备注 |
|---|---|---|---|
| `0x40` | `0x100AA22A` | E0 `0x100A0233` / E1 `0x100A0263` | 表 A 直接跳转臂 |
| `0x41` | `0x100AA23A` | 同上 | |
| `0x42` | `0x100AA24A` | 同上 | |
| `0x43`–`0x45` | `0x100AA25A`/`0x100AA26A`/`0x100AA27A` | 同上 | 顺带发现，不在待核清单内 |
| `0x80` | `0x100AA28A` | 同上 | |
| `0x81` | `0x100AA2C7` | 同上 | |
| `0x90`/`0x91` | `0x100AA2D7`/`0x100AA337` | 同上 | `0x91` 在 `0x100A6474` 处参与状态机分支 |
| **`0x92`** | **无（落到默认臂 `0x100AA432`）** | **不写入 CDB[2]** | 索引表 `0x100AA47C` 第 0x11 项（=0x92-0x81）值为 9 → 默认臂，只 `mov eax,esi` 返回，不设 `+0x456`。**`0x92` 不是合法子功能码** |
| `0xA0`/`0xA1` | `0x100AA2E7`/`0x100AA2F7` | 同上 | |
| `0xB0`–`0xB4` | `0x100AA307`/`0x100AA317`/`0x100AA327`/`0x100AA347`/`0x100AA357` | 同上 | 含 `0xB3` |
| `0xC0`/`0xC1` | `0x100AA38C`/`0x100AA39C` | 同上（作为**子功能码**时） | 注意：`0xC1` 同时是独立 opcode（见 4.3） |
| `0xD0`/`0xD1`/`0xD2` | `0x100AA3AC`/`0x100AA3BC`/`0x100AA3CC` | 同上 | |
| `0xD3`/`0xD5`/`0xD6` | `0x100AA401`/`0x100AA3F1`/`0x100AA411` | 同上 | |
| `0x800` | `0x100AA42B`（`mov word ptr [esi+0x456], cx`，值来自 `[edi+0x30]`） | 同上 | 透传分支 |

工厂白名单（`cmp`/跳转表边界实测）：`0x40–0x45`、`0x80`、`0x81`、`0x90`、`0x91`、`0xA0`、`0xA1`、`0xB0`、`0xB1`、`0xB2`、`0xB3`、`0xB4`、`0xC0`、`0xC1`、`0xD0`、`0xD1`、`0xD2`、`0xD3`、`0xD5`、`0xD6`、以及透传码 `0x800`。**`0x92` 不在白名单内。**

### 4.3 关于 C1：`0xC1` 有两重身份，别混

1. **作为 CDB[0]**：`0x100A0190` `mov byte ptr [ecx+8],0xC1; mov eax,6; ret` —— 这是独立的 EXECUTE 命令，CDB 只有 6 字节，**CDB 里不带子功能码**（构造函数 `0x100A0160` 只置 `[+0x5c]`，BuildCDB 只写 CDB[0]）。
2. **作为子功能码**：工厂 `0x100AA39C` 把 `0xC1` 写进命令对象 `+0x456`，随后 E0/E1 的 `0x100A0233`/`0x100A0263` 把它写进 **CDB[2]**。

也就是说：**`0xC1` 出现在 CDB[2] 时，CDB[0] 是 `0xE0` 或 `0xE1`，不是 `0xC1`。** 状态机里 `0x100A6480` `cmp ax,0xC1` 判的是 `+0x456` 的子功能码，不是 CDB[0]。

### 4.4 主机侧是否做与固件相同的范围校验 —— **不做** `[实证]`

固件约束（来自 `REPORT_L3-交接定稿.md` 7.2/7.3/7.4）：`0x40` 参数 ≤15354、`0x41` ≤450、`0x42` ≤3283、`0xC1` ≤450、`0xB3` ∈[−300,300]。

在 md3 `.text` 全部 277,966 条指令中，对这些数值做全形态扫描（任意指令、任意操作数位置，含 `cmp` / `push` / `mov` / 立即数取负）：

| 常量 | 十进制 | 出现次数 | 形态 | 是否范围校验 |
|---|---|---|---|---|
| `0x3BFA` | 15354 | **0** | — | 否 |
| `0x3BF9` | 15353（上限−1） | **0** | — | 否 |
| `0x1C2` | 450 | 1 | `push 0x1C2`（`0x100104E1`，能力 ID 三元组 `0x8003/0x93/0x1C2`） | **否** |
| `0x1C1` | 449 | 2 | `push 0x1C1`（`0x1005794E`、`0x10063744`） | **否** |
| `0xCD3` | 3283 | 1 | `push 0xCD3`（`0x1002A97C`，能力 ID 三元组 `0x8001/0x10/0xCD3`） | **否** |
| `0xCD2` | 3282 | 0 | — | 否 |
| `0x12C` | 300 | 7 | 全是 `push`，且与 `0x12B/0x12D/0x12E/0x12F` 连续出现（能力 ID 序列） | **否** |
| `0x12B` | 299 | 5 | 同上 | **否** |
| `0xFED4` | −300 | **0** | — | 否 |

**`cmp` 类指令中，上述常量命中数为 0。** 即 md3 里**不存在任何一处**把这些数值当作边界来比较。

主机侧实际做的校验只有两层，且性质完全不同：

1. **子功能码白名单**：工厂 `0x100AA1D0` 用 `cmp`/跳转表只接受上表那 21 个码值，其余落到默认臂 `0x100AA432`（对象建好但 `+0x456` 未设值）。这是**枚举合法值**，不是数值范围。
2. **前置条件检查**：`0x100A6463` / `0x100A649D` / `0x100A64B1` 等处 `push <能力 ID>; call 0x100A48B0/0x100A4910; cmp eax,1` —— 用能力查询（如 `0x23A0001`、`0x2040100`、`0x6000000`、`0x63F0300`）判断设备当前是否允许该动作，属于**状态/能力门禁**，与参数量纲无关。

**交叉验证结论：主机侧不设上界，固件侧设上界。** 由此可得 `[推断]`：越界参数不会被 md3 拦下，会原样打包进 CDB[6..8]（24 位大端，见 2.4）发往设备，由固件自行拒绝或截断；表现出的现象应是"主机下发成功、设备报错/行为异常"，而不是"主机拒绝下发"。反证条件：若能在 md3 中找到对 `[CDB 对象 +0x50]` 的 `cmp`/`and`/`movzx` 截断指令，则本条需改写——本轮扫描未发现。

---

## 5. `0xD1` 待核项：主机侧**确实会**发出 `0xD1` —— 给构造点

构造链（自上而下）`[实证]`：

```
0x100997A9  cmp  eax, 0xd0
0x100997AE  jl   <跳出>            ; < 0xD0 不建命令
0x100997B4  cmp  eax, 0xd6
0x100997B9  jle  0x100997C6        ; 0xD0 ≤ eax ≤ 0xD6 → 建命令
0x100997BB  cmp  eax, 0x800
0x100997C0  jne  <跳出>
0x100997C6  push 0x60
0x100997C8  call 0x100AB280        ; 分配命令对象（0x60 字节）
0x100997E4  mov  ecx, [esp+0x30]
0x100997EB  push ecx               ; ← 子功能码实参（= eax 所在的命令 ID）
0x100997EE  call 0x100A1EC0        ; 命令包装（vtable 0x100C2C20）
    └─ 0x100A1F29  mov ecx,[esp+0x30]
       0x100A1F2D  push ecx
       0x100A1F33  call 0x100AA1D0   ; 子功能码工厂
            └─ 0x100AA3BC  mov word ptr [esi + 0x456], 0xd1   ★0xD1 构造点★
    └─ 0x100A60AD  mov cx,[esi+0x456]
       0x100A60BD  call 0x100A00A0     ; E0 构造函数 → [CDB 对象 +0x64] = 0xD1
            └─ 0x100A0233  mov byte ptr [ecx + 0xa], al   ★0xD1 落 CDB[2]★
```

**三条独立证据**：

1. **白名单放行**：工厂 `0x100AA1D0` 的第三张跳转表覆盖 `0xC0..0xD1`（`0x100AA36F` `sub eax,0xC0` / `cmp eax,0x11`），索引表 `0x100AA4C4` 第 17 项（`0xD1-0xC0=0x11`）值为 3，跳转表 `0x100AA4B0` 第 3 项 = `0x100AA3BB`，其下一条即 `0x100AA3BC mov word ptr [esi+0x456], 0xD1`。
2. **调度器放行**：`0x100997A9..0x100997C0` 对 `0xD0..0xD6` **整段**放行（不是只放行 `0xD0`/`0xD2`），`0xD1` 落在区间内。
3. **命令表登记**：`0x100A2654` 与 `0x100A2669` 两处 `mov dword ptr [eax+4], 0xD1`（条目头 `mov dword ptr [eax], 0x12`），说明 `0xD1` 被写进一张"命令→处理器"登记表中，与 `0xC1`（`0x100A267E`）、`0xE1`（`0x100A26A8`）、`0xF0`/`0xF1`/`0xF2`/`0xF8` 并列。

**否定项（避免误判）**：另有 5 处 `push 0xD1`（`0x1001CFBF`、`0x10037EEF`、`0x100577A5`、`0x10064F6F`、`0x1007C21A`），现场分别是 `push 0x8003; push 0x46; push 0xD1; call [eax+0xC]` 之类的**错误/状态码上报**，与 CDB 无关，不计为构造点。

**结论**：`0xD1` 是主机侧真实可达、真实可发出的子功能码，构造点 `0x100AA3BC`（写 `+0x456`）+ `0x100A0233`/`0x100A0263`（落 CDB[2]）。它载于 **E0 (0xE0)** 或 **E1 (0xE1)** 的 CDB[2]，由 `0x100A6A3F`（E0 ctor）/ `0x100A6AEC`（E1 ctor）两条路径之一承载；本轮未能确定 `0xD1` 具体走 E0 还是 E1（见 §7 疑问 3）。

---

## 6. 与中间产物的冲突与修正

复核以机器码为准，与 `md3/cdb/*.json`、`md3/_f5/*` 的中间结果冲突处如下：

| # | 中间产物说法 | 复核结果 | 判定 |
|---|---|---|---|
| 1 | `vt.py` 用 `d.mem.disp ∈ [8,0x12]` 且 `off = disp-8` 判定 CDB 字节 | 正确，但**漏掉** MODE SELECT 的两个构造点（`0x15a`/`0x15b` 的 `mov eax,6` 出现在 site **之前**，`ret_len` 只找 site 之后的常量） | 采用复核：补回 2 点，落点数 16 → 18 |
| 2 | `emit.py`（18:01 版）把 `0x00` TUR 拆成两行（`0x100C28D4`/`0x100C2974` 两个 vtable），`0x1D` 也拆两行 | 两个 vtable 的 **BuildCDB 槽（+0x24）指向同一函数**，是同一命令的两个类包装，不是两条命令 | 采用复核：合并为一行，调用者取并集 |
| 3 | `emit2.py` 的 `callers` 只取第一个 ctor 的调用者 | 复核按"vtable→所有写 vptr 的 ctor→并集调用者"重算，TUR 12 个、SEND DIAG 11 个、READ(10) 7 个调用点 | 采用复核：表中取并集后截 5 个 |
| 4 | `cdb_sites.json`（18:01 版）`0x28` READ(10) 调用者首项 `0x100A3B62` | 复核得首项 `0x100A3B12`（来自第二个 ctor `0x100AAB90`） | 采用复核 |
| 5 | `scan2.py` 结论"`[esi+0x456]` 是子功能码槽" | 复核确认，但**补充**：`+0x456` 只是中间载体，CDB[2] 的真正落点是 `0x100A0233`/`0x100A0263` | 采用复核补充 |
| 6 | `hunt.txt` 对 `0x03`/`0x17` 输出为空 | 复核确认（四种形态全扫，0 命中），并补扫两个 DLL 亦 0 命中 | 维持，升级为 `[实证]` |

---

## 7. 本轮未解决的疑问

1. **`0x92` 为何不在白名单**：索引表 `0x100AA47C` 明确把 `0x92` 映射到默认臂。是固件从未实现 `0x92`，还是 `0x91` 的变体被改名？需与固件 `0x03E390`/`0x03EBC0` 侧的子码清单对表才能定性。`[未证]`
2. **CDB 对象 `+0x64`/`+0x66`/`+0x68` 的字段语义**：READ(10)/WRITE(10) 分别把 `+0x64/+0x66/+0x68` 写进 CDB[2]/[4]/[5]，`+0x65`/`+0x67` 未被使用，说明这三个字节不是连续的 LBA。尚未找到给它们赋值的上游（疑似 `0x100A44B0` 一类参数打包函数），故未给 LBA 字段下定论。`[未证]`
3. **`0xD1` 走 E0 还是 E1**：`0x100A6A3F`(E0 ctor) 与 `0x100A6AEC`(E1 ctor) 的选择由 `0x100A6A00` 起的一段能力查询状态机决定（`0x100A6A05 cmp eax,ebp`、`0x100A6AB4 cmp edi,ebp`），本轮未把该状态机的判据反推完。
4. **`request+0x14/+0x18` 的写入点未直接定位**：`dispatch.md` 给出的是字段语义，本轮未找到"调用 BuildCDB → 把 eax 写进 `request+0x14`、把 `[this+8]` 写进 `request+0x18`"的那条包装函数。若后续要做端到端论证，应从 `0x100A8730`（工厂内首次调用）往上游追。
5. **`0x1D` SEND DIAGNOSTIC 的上层语义**：它不在 14 条已知锚点里，却有 11 个调用点（`0x10093E08`、`0x1009423A`、`0x100A4FF9`、`0x100A61D2`、`0x100A6B2B` …），CDB[1] 固定为 `4`。它到底对应自检流程的哪一步、与固件内部命令表的哪一条对齐，本轮未追。
