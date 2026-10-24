# LS8000.md3 导出接口、`request` 结构与调用方向（F6 定稿）

样本（只读）：`D:\DS\TEST\LS8000\driver\LS8000.md3`（958,464 B，PE32/i386，ImageBase `0x10000000`）
同只读：`D:\DS\TEST\LS8000\driver\NKDUSCAN.dll`（90,112 B）、`NKDSBP2.dll`（86,016 B）
版本：`LS8000.MD3` / Nikon Scan Driver `1.3.0.3003`；对齐 `dispatch.md`、`REPORT_L3-交接定稿.md` §13

证据分级：`[实证]`＝附 VA 的反汇编/字节；`[推断]`＝写清依据链；`[未证]`＝只有线索。

---

## 0. 七条结论（相对上一稿的变化用 ★ 标）

1. 三个导出**都是薄垫片**：`NkCtrlEntry`＝取单例＋跳虚表槽 1；`NkMDCtrlEntry`＝4 路表＋转发；`MAIDEntryPoint`＝16 路表＋换参转发。三者自身都不含 CDB 构造、不含 SCSI 调用、不含 magic/长度校验。
2. ★ **`NkDriverEntry` 的调用点找到了**：md3 内唯一的调用点在 `0x1009A32A`（`call dword ptr [esp+0x1C]`，指针来自加载器对象 `+0x04`）。上一稿 Q1 关闭，§3.3 的链路升级为 `[实证]`。
3. ★ **CDB 归属要分两段说**：**md3 负责构造 CDB 字节**（命令对象 `[this+8]`，长度由构造器返回 6 或 10，共 ~20 个构造器）；**NKDUSCAN/NKDSBP2 的 `NkDriverEntry` 负责把它送上总线**。上一稿“md3 零 SCSI ⇒ CDB 在 DLL 发出”的说法不完整，本稿更正。
4. ★ `REPORT` §13.1 的 `request` 布局（`+0x14` CDB 长度、`+0x18` CDB 指针、`+0x1C` 数据长度、`+0x20` 数据指针）**在 DLL 侧得到实证（升级）**，在 md3 的导出侧仍无消费点（降级为“跨模块”而非“证伪”）。
5. `NkCtrlEntry`＝4 参 `ret 0x10`，`NkMDCtrlEntry`＝2 参 `ret 8`，`MAIDEntryPoint`＝≥7 参 `ret 0x1C`；与 `dispatch.md` 一致。
6. ★ 存在**三套**不同的 `request` 解释：md3 `NkCtrlEntry` 侧（键/子键回填）、md3 `NkMDCtrlEntry` 侧（长度+类型自校验）、传输层 `request`（DLL 消费，§2.3）。混淆这三套是 §13.1 长期对不上的根因。
7. ★ 「第 13 章的 selector 5 属于 `NkDriverEntry`」**成立**，且新增一条硬证据：md3 的封装器对 selector 5 有**独占特判**（调用前把 `loader+0x14` 写进 `request+8`，`0x1009A31E`–`0x1009A321`）。

---

## 1. 三个导出逐个

### 1.1 总表（`[实证]`）

| 导出 | 序号 | 入口 VA | 真实 ABI | 返回 | 性质 |
|---|---|---|---|---|---|
| `?NkCtrlEntry@@YGFFFFPAX@Z` | 1 | `0x10091850` | `u16 __stdcall(sel, a2, a3, void* req)`，`ret 0x10`，`ecx`=单例 this | `u16` | 取单例 + `jmp [vt+4]` |
| `MAIDEntryPoint` | 2 | `0x10027600` | `u32 __stdcall(a1..a7)`，`ret 0x1C` | `u32` | 16 路查表 + 转发 |
| `NkMDCtrlEntry` | 3 | `0x1000B520` | `u16 __stdcall(sel, void* req)`，`ret 8` | `u16` | 4 路查表 + 转发 |

导出目录：`0x100D0780` → 地址表 `0x100D0798`、名字表 `0x100D07A4`、`{0,1,2}+"LS8000.md3"` @`0x100D07B0`。

### 1.2 `NkCtrlEntry` @`0x10091850`

```
10091850  call 0x100918A0        ; 单例 getter（对象 0x34 B，全局 0x100D85A0）
10091855  test eax,eax
10091857  je   10091860
10091859  mov  edx,[eax]         ; vtable
1009185B  mov  ecx,eax           ; this
1009185D  jmp  dword ptr [edx+4] ; vtable[1] = 0x10091D50
10091860  mov  eax,5
10091865  ret  0x10
```

- **参数读取**（在分派体 `0x10091D50`，入口 push `ecx/ebx/ebp/esi/edi` 共 0x14）：
  第 1 参＝`mov eax,[esp+8]`@`0x10091D51` → `movsx ebx,ax`@`0x10091D5C`（**16 位有符号**扩展，负值可进）；
  第 4 参＝`mov ebp,[esp+0x1C]`@`0x10091D57`（`request`）；
  第 2/3 参不预取，臂内按 `word ptr [esp+0x1C]`/`[esp+0x20]` 读**低 16 位**（`0x10091DC4`、`0x10091DD0`、`0x10091EEA`、`0x10091F0F`）。
- **入口校验**：只有「单例为 NULL → 返回 5」（`0x10091860`）。对 selector、request、长度、magic **一律不校验**；`request` 为 NULL 会在臂内崩（`0x10091E05` 直接 `mov eax,[ebp+8]`）。
- **只转发**：是。本体 4 条指令；真正分派体在 `0x10091D50`（11 项表 `0x10091F88` + 比较树），vtable `0x100C24C4` 16 项、`[1]=[14]=0x10091D50`。
- **模块级校验不在导出里**：型号签名 `"Nikon MD3.01IILS8000"`（`0x100BE708`，23 B）有 5 处 `memcmp(...,23)`：`0x10008BB3`、`0x10009C02`、`0x1001A42A`、`0x1001AC3B`、`0x1001AED1`。属**装载期单机型绑定**，不是入口校验 `[实证]`。

### 1.3 `NkMDCtrlEntry` @`0x1000B520`

```
1000B520  mov eax,[esp+4] / dec eax / cmp eax,3 / ja 0x1000B571   ; 只认 1..4
1000B52A  jmp dword ptr [eax*4+0x1000B57C]
1000B531  mov eax,[esp+8] / push eax / call 0x1000B220 / ret 8     ; sel=1
1000B541  ... call 0x1000B270 ... / ret 8                          ; sel=2
1000B551  ... call 0x1000B2A0 ... / ret 8                          ; sel=3
1000B561  ... call 0x1000B3A0 ... / ret 8                          ; sel=4
1000B571  mov eax,0x1001 / ret 8                                   ; 非法选择子
```

- **参数读取**：`[esp+4]`→`eax`（selector，32 位比较）；`[esp+8]`→转发给 4 个内部函数的**唯一实参**。
- **入口校验**：只有 selector ∈ [1,4] 的范围校验；`request` 不查空；逐字段校验在 4 个臂内。
- **只转发**：是。函数体 20 条指令；4 臂互不共享代码。
- **错误码族**：`0x1001`（非法选择子）、`0x1005`（类型/长度不符）、`0x1006`（建对象失败）、`0x1008`（名字不符）、`0x1009`（注册失败）——与 `NkCtrlEntry` 的 default `6` 不同源 `[实证]`。

### 1.4 `MAIDEntryPoint` @`0x10027600`

```
10027600  mov eax,[esp+8] / cmp eax,0xF / ja 0x1002780E
1002760E  jmp dword ptr [eax*4+0x10027840]
```

- **参数读取**：`[esp+4]`=a1、`[esp+8]`=a2=功能号、…、`[esp+0x1C]`=a7；每个臂把 a1、a3..a7 原样转交，并**用臂常量原位替换 a2**（例 sel=5 臂 `0x100276FB`：`push a7,a6,a5,a4,a3,5,a1 → call 0x100250A0`，实参仍 7 个）。
  > 对 `dispatch.md` §5「把功能号作为**额外**常量压栈」的修正：不是额外，而是**替换 a2** `[实证]`（`0x10027615`–`0x1002763A`）。
- **入口校验**：`cmp eax,0xF / ja`；无空指针校验。
- **default 臂** `0x1002780E`：`esi=0xFFFFFF81`（−127）；若 a6≠0 则把 a6 当**错误回调**调用（`0x10027819`–`0x10027836`），否则直接返回 −127。**a6 是回调槽** `[实证]` 结构 + `[推断]` 语义（回调签名未定）。
- **只转发**：是，纯 ABI 垫片。

### 1.5 与 `dispatch.md` 的对齐 / 冲突

| 项 | `dispatch.md` | 本稿 | 判定 |
|---|---|---|---|
| `NkCtrlEntry` 4 参 `ret 0x10` | 是 | 复核成立（`0x10091865`、`[esp+0x1C]`→`ebp`） | 一致 |
| vtable `0x100C24C4` 16 项、`[1]=0x10091D50` | 是 | 一致 | 一致 |
| `NkMDCtrlEntry` 只认 1..4，5→`0x1001` | 是 | `0x1000B571` 一致 | 一致 |
| `MAIDEntryPoint` 16 路 | 是 | `0x10027840` 一致 | 一致 |
| `MAIDEntryPoint` 传参方式 | “额外常量压栈” | **原位替换 a2** | **补正（§1.4）** |
| `request +0x14…+0x20` 语义 | 沿用 §13.1 | md3 导出侧无消费点；**DLL 侧实证** | **改判：不是 md3 导出结构（§2.3）** |
| `NkDriverEntry` 调用点 | 未提 | `0x1009A32A` | **新增实证（§3.2）** |

`dispatch.md` 无结论被推翻，只有 1 处补正 + 1 处改判 + 1 处新增。

---

## 2. `request` 结构偏移表

### 2.1 方法

- 对三个导出做递归下降，对「request 所在寄存器」做**钉住式**传播（`_f6/prov2.py`）：只承认可证位点，遇调用/分支不清即停，不做猜测性跨函数传播。
- `NkMDCtrlEntry` 侧证据最硬：`mov esi,[esp+8]`（`0x1000B221` 等）后 `esi` 恒为 request。
- `NkCtrlEntry` 侧：`ebp` 恒为第 4 参（`0x10091D57`）。
- DLL 侧：对 `NKDUSCAN`/`NKDSBP2` 的 `NkDriverEntry` 各臂做同类跟踪（`_f6/dll_arms.py`、`dll_anchor.py`）。

### 2.2 md3 导出侧偏移表（`+0x00`–`+0x40`）

| 偏移 | 读写宽度 | 建议名 | 证据地址 | 置信度 |
|---|---|---|---|---|
| `+0x00` | u32 R/W | 查表键（Ctrl 侧）/ 结构长度（MD 侧，0x10/0x14/0x58） | `0x10091CF7`（→`0x10091B50` 当键）；`0x1000B22B cmp [esi],0x10`、`0x1000B2C0 cmp [esi],0x14`、`0x1000B3C1 cmp [esi],0x58` | 高（两导出语义不同） |
| `+0x04` | u32 R/W | Ctrl 侧由 map 回填（`0x10091D28`）；MD 侧＝**请求类型** 1/2/3 | `0x1000B225`、`0x1000B274`、`0x1000B2BA`、`0x1000B3BB`；`0x10091C1A`、`0x10092F26` | 高 |
| `+0x08` | u32 R/W | Ctrl 侧＝回填 / sel=5 时作**设备 ID**（`0x10091E05`→`0x10091A50`）；MD 侧＝**句柄出参**（`0x1000B25A` 写入，源 `0x100D165C` 自增） | 同左 | 高 |
| `+0x0C` | u32 R/W | 子命令键（Ctrl 侧 `0x10091F34`、`0x10092EE6`）；MD 侧＝**模块码**，`memcmp(req+0xC,"1000",4)` @`0x1000B237`（字面串 `0x100BE778`） | 同左 | 高 |
| `+0x10` | u32 R/W | 从属 ID / 名称索引 | 读 `0x1000B336`、`0x10095FA9`；写 0 `0x10092F0B` | 中 |
| `+0x14` | u32 R（回填槽 1） | `0x1000B432 lea edx,[esi+0x14]`（第 3 实参传 `call [eax+0x24]` @`0x1000B43E`） | 中（**非** CDB 长度，见 §2.3） |
| `+0x18` | u32 R（回填槽 2） | `0x1000B42E lea edx,[esi+0x18]` | 中（**非** CDB 指针） |
| `+0x1C` | — | 未见访问（MD 四臂最大用到 `+0x18`） | 无 | 未证 |
| `+0x20` | — | 未见访问 | 无 | 未证 |
| `+0x24`–`+0x40` | — | 未见访问；MD 侧结构长度上限 0x58（`0x1000B3C1`）说明存在更长变体，其尾部由能力对象 `0x8105` 的虚方法解读 | 无 | 未证 |

补充 `[实证]`：MD 侧三种长度 `0x10/0x14/0x58` ↔ 三种类型 `1/2/3` 是「长度-类型成对自校验」（`0x1000B225`+`0x1000B22B`；`0x1000B2BA`+`0x1000B2C0`；`0x1000B3BB`+`0x1000B3C1`）。这比 `dispatch.md` §4 只写“类型1↔0x10”更完整。

### 2.3 ★ 传输层 `request`（`NkDriverEntry` 的第二参数）—— §13.1 锚点在此证实

md3 导出侧找不到 `+0x14…+0x20` 的消费点，是因为**该布局属于跨界结构，消费方在 DLL 内**。逐字段证据：

| 偏移 | 语义 | 证据 | 分级 |
|---|---|---|---|
| `+0x00` | 设备标识（用于查设备对象） | NKDUSCAN sel5 臂 `0x1000401F` `mov edx,[esi+0]` → 交给 `[vtable+0x10]` 查设备（`0x10004026`） | `[实证]` |
| `+0x04` | 标志/方向：非 0 时要求数据缓冲非空 | NKDUSCAN sel5 `0x1000400A` `cmp [esi+4],0` → 若非 0 再查 `[esi+0x20]`（`0x10004010`） | `[实证]` |
| `+0x0C` | **完成/错误回调** `(req, errcode)` | NKDUSCAN `0x10003FE9`、`0x1000402E`、`0x100040A0`；NKDSBP2 `0x10002ADD`、`0x10002B9D` 均 `mov eax,[X+0xC]; push X; push <错误码>; call eax` | `[实证]` |
| `+0x14` | **CDB 长度** | NKDUSCAN `0x10002B81` `mov edx,[eax+0x14]` → 作为 **`nNumberOfBytesToWrite`** 传给 WriteFile（见下） | `[实证]` |
| `+0x18` | **CDB 指针** | NKDUSCAN `0x10002B88` `mov ebx,[eax+0x18]` → 作为 **`lpBuffer`** 传给 WriteFile | `[实证]` |
| `+0x1C` | **数据长度** | NKDSBP2 `0x10002B37` `mov ecx,[eax+0x1C]` 与 `0x10002B3D` `mov edx,[eax+0x20]` → `call 0x10006260(arg1=[req+0x20], 0, [req+0x1C])`，形如 `(ptr, 0, len)` 缓冲区准备 | `[实证]` |
| `+0x20` | **数据指针** | 同上；另 NKDSBP2 `0x10002B4F`–`0x10002B5C`：`arg5(lpOutBuffer)=[req+0x20]`、`arg6(nOutBufferSize)=[esi+0x28]` | `[实证]` |
| `+0x24` | 长度上界/容量（sel5 要求 ≥0x20） | NKDUSCAN `0x10004000` `cmp [esi+0x24],0x20 / jb <错误>` | `[实证]` |
| `+0x28` | 未定（被读进局部，未追踪到消费） | NKDUSCAN `0x10002B96` | `[未证]` |

**决定性的一段**（`[实证]`）：NKDUSCAN 发送函数 `0x10002B50` 起的对象方法把 `esi` 内部对象的 `+0x18` 取出当 request，然后

```
10002B81  mov edx,[eax+0x14]      ; CDB 长度
10002B88  mov ebx,[eax+0x18]      ; CDB 指针
10002BA3  mov eax,[esp+0x18]      ; = [req+0x18]
10002BA9  push edi(=0)            ; arg3 = lpOverlapped
10002BAA  push edx                ; arg2 = 长度
10002BAB  push eax                ; arg1 = 指针
10002BAC  mov ecx,esi
10002BAE  call 0x10002B20         ; → WriteFile
```

包装器 `0x10002B20`：实参 `(ptr=[req+0x18], len=[req+0x14], overlapped)`，`this=ecx` 提供句柄 `[ecx+0x10]`：

```
10002B33  push eax        ; lpBuffer
10002B34  mov eax,[ecx+0x10]   ; hDevice
10002B37  push edx        ; ...
10002B38  push eax        ; hDevice
10002B41  call [0x1000E02C]    ; WriteFile
```

即 **`WriteFile(hDevice, request[+0x18], request[+0x14], &written, overlapped)`** —— 与 §13.1 的「`+0x14` CDB 长度 / `+0x18` CDB 指针」逐字对应，且 roles 由 API 形参顺序反推，不是猜的。

→ **判定**：`REPORT` §13.1 的布局**成立且属 NKDUSCAN/NKDSBP2 的传输层 request**；它**不是** md3 三个导出的入参结构。上一稿“三个疑似窗口全否”的结论针对 md3 导出侧，仍然有效，但不构成对 §13.1 的否证，此处一并更正。

### 2.4 旁证（`iface/field_stat.json`，不可归属具体结构，仅频次）

`+0x00` 4311 / `+0x04` 1144 / `+0x08` 1650 / `+0x0C` 1214 / `+0x10` 1118 / `+0x14` 428 / `+0x18` 245（以 eax 基址计）。`+0x14` 之后骤降，**支持**“热字段在前 5 个双字”，但**不能**用来指认任一具体结构。

### 2.5 三套 request 的关系

| | `NkCtrlEntry` 入参 | `NkMDCtrlEntry` 入参 | 传输层 request（§2.3） |
|---|---|---|---|
| `+0x00` | 查表键 | 结构长度 | 设备标识 |
| `+0x04` | 回填（出参） | 类型 1/2/3 | 标志 |
| `+0x08` | 回填 / sel=5 时读设备 ID | 句柄出参 | — |
| `+0x0C` | 回填 / sel=3,4 时读子键 | 模块码 `"1000"` | **完成回调** |
| `+0x14`…`+0x20` | 无 | 两个回填槽（`+0x14`/`+0x18`） | **CDB 长度/指针、数据长度/指针** |

同一偏移在不同层含义不同；这是本次对 §13.1 歧义的根因解释 `[实证]`（三者各有独立证据列）。

---

## 3. 调用方向定论

### 3.1 md3 → NKDUSCAN / NKDSBP2（单向，运行时动态解析）`[实证]`

| 环节 | VA | 内容 |
|---|---|---|
| DLL 名字符串 | `0x100C25F0` `"Nkduscan.dll"`；`0x100C2600` `"Nkdsbp2.dll"` | 两版并存 |
| 过程名字符串 | `0x100C2578` `"NkDriverEntry"` | 唯一被解析的符号 |
| 加载器 vtable | `0x100C25D0`（8 项）：`[0]0x10099EB0 [1]0x10099EC0 [2]0x10099EE0(LoadLibrary) [3]0x10099F90(FreeLibrary) [4]0x1009A2E0 [5]0x1009A470 [6]0x1009A370 [7]0x1009A480(构造)` | vtable 后紧跟两个 DLL 名串（`[8]…` 即 `"Nkduscan.dll"` 首字节），故只有 8 项 |
| DLL 加载 | `0x10099EE0`：`call [0x100BE028]` → `mov [esi+8],eax`（`loader+8`=HMODULE） | |
| 符号解析 | GetProcAddress → `mov [esi+4],eax`（**`loader+4` = `NkDriverEntry` 指针**） | |
| 装载使能与上下文 | `0x1009A370`：`loader+0x10 = [x+0x10]`（ctx）、`loader+0x14 = [x+8] & 0x20`（能力位）、`loader+0x18 = 1`（已装载） | |
| 驱动对象 vtable | `0x100C2620`（Nkduscan 版）、`0x100C2660`（Nkdsbp2 版），槽 0 = `0x1009A5F0`/`0x1009A610` | 多态决定加载哪个 DLL |
| 构造点 | `0x1009C3CB`/`0x1009C4B1`（`=0x100C2620`）、`0x1009C587`/`0x1009C661`（`=0x100C2660`） | 两个类各 2 处 |

反向证据（`_f6/sibs.txt`）：两个 DLL **各只导出 1 个符号** `NkDriverEntry`；其全文件字节**不含** `"LS8000"`、`".md3"`、`"NkCtrlEntry"`、`"MAIDEntryPoint"`、`"NkMDCtrlEntry"` → 它们不加载、也不直接调用 md3 的导出。**故方向为单向 md3 → DLL。**

### 3.2 ★ `NkDriverEntry` 的真实调用点：`0x1009A32A`（关闭上一稿 Q1）

加载器虚方法 `slot[4]` = `0x1009A2E0`，签名 `thiscall(loader, selector, request)`：

```
1009A2E2  mov ebx,[esp+0xC]          ; arg1 = 选择子
1009A2EA  mov edi,ecx                ; this = loader
1009A2EC  mov eax,[edi+4]            ; = NkDriverEntry 函数指针（存入局部）
1009A2EF  mov [esp+8],eax
1009A2F3  mov al,[edi+0x18]          ; 已装载标志
1009A2F6  jne 1009A307
1009A2F8  test al,al / je 1009A30B   ; sel==1 且未装载 → 放行（装载请求）
1009A307  cmp al,1 / jne 0x1009A2FC  ; 其余选择子必须已装载，否则返回 7
1009A30B  cmp ebx,5 / jne 1009A324
1009A31E  mov ecx,[edi+0x14]
1009A321  mov [ebp+8],ecx            ; ★ sel==5 独占：把 loader+0x14 写进 request+8
1009A324  mov eax,[edi+0x10]         ; ctx
1009A327  push eax                   ; arg3
1009A328  push ebp                   ; arg2 = request
1009A329  push ebx                   ; arg1 = selector
1009A32A  call dword ptr [esp+0x1C]  ; ★★ NkDriverEntry(selector, request, ctx)
1009A32E  push eax / call 0x10099DE0 ; 返回码翻译
1009A339  cmp esi,8 / jne 1009A35D   ; 返回 8 = 设备忙
1009A343  push 0xFA / call 0x100A40B0; Sleep(250 ms)
1009A358  cmp eax,0x14 / jb 1009A324 ; 重试上限 20 次
```

要点：
1. **`NkDriverEntry` 是 3 参数**（`ret 0xC`，见 §3.3），md3 传的 ctx 恒为 `loader+0x10`。
2. **选择子 1 是“装载/初始化”**：只有未装载时才允许；其余 2..9 必须先装载成功。
3. **选择子 5 有独占预处理**：`request+8` 被填入 `loader+0x14`＝设备描述符的能力位（`[x+8] & 0x20`，由 `0x1009A370` 设定）。这是对第 13 章「更新器用 selector 5」的直接支撑。
4. **返回码 8 = 忙重试**：最多 20 次 × 250 ms（`0x1009A339`–`0x1009A35B`）。
5. 该函数**只经虚表到达**（全 `.text` 无对 `0x1009A2E0` 的直接 `call` 立即数引用，已验证），故上一稿用「找立即数调用点」的思路必然落空。

### 3.3 DLL 侧 `NkDriverEntry`（`[实证]`）

```
10003C40  push esi
10003C41  push 0x10012F68
10003C46  call [0x1000E014]     ; EnterCriticalSection
10003C4C  mov eax,[esp+8]       ; arg1 = 选择子
10003C50  add eax,-1 / cmp eax,8 / ja 0x10003DB0   ; 只认 1..9
10003C5C  jmp dword ptr [eax*4+0x10003DC8]
10003C63  mov eax,[esp+0x10]    ; arg3
10003C67  mov ecx,[esp+0xC]     ; arg2
10003C6B  push eax / push ecx / call 0x10003E30    ; 内部函数(request, ctx)  ← 注意实参已交换
10003C7C  call [0x1000E010]     ; LeaveCriticalSection
10003C85  ret 0xC
```

- 两个 DLL 形态完全同构：`NKDUSCAN` 入口 `0x10003C40`（表 `0x10003DC8`，9 项）、`NKDSBP2` 入口 `0x100041D0`（表 `0x10004358`，9 项）。
- 选择子 → 内部函数（`[实证]`）：

| sel | NKDUSCAN | NKDSBP2 |
|---|---|---|
| 1 | `0x10003E30` | `0x100043C0` |
| 2 | `0x10004240` | `0x10004500` |
| 3 | `0x10004290` | `0x10004570` |
| 4 | `0x100042E0` | `0x100045D0` |
| 5 | `0x10003FD0` | `0x10004670` |
| 6 | `0x10003F90` | `0x10004640` |
| 7 | `0x10003F10` | `0x10004490` |
| 8 | `0x100040C0` | （`0x100042F6` 臂） |
| 9 | （`0x10003D8B` 臂） | （`0x1000431B` 臂） |

- 每个内部函数的前两、三条指令都是 `request==NULL → 0x11004`、`ctx==NULL → 0x11003`，错误经 `[request+0xC]` 回调上抛。错误码族 `0x11003/0x11004/0x11006/0x21008` 与 md3 导出的 `0x1001/0x1005…` 完全不同 `[实证]`。

### 3.4 ★ 明确回答：CDB 最终由谁发出

**分两段，且两段都在实测范围内：**

1. **构造（主机侧 md3）** —— md3 自带 ~20 个 CDB 构造器（`md3/cdb_sites.json`），形如命令对象方法：
   `TEST UNIT READY` `0x1009FEB0`（`mov byte [this+8],0; mov eax,6; ret`）、`INQUIRY` `0x100A01A0`、`START STOP UNIT` `0x100A0290`（`mov byte [this+8],0x1B`、`[this+0xC]=[this+0x50]`）、`READ(10)` `0x100AAD00`、`WRITE BUFFER` `0x100AADC0`、厂商 `0xE0` `0x100A0230` 等。**CDB 缓冲在 `[this+8]`，长度由构造器返回 6 或 10** —— 与 `REPORT` §13.2 的「命令对象字段」完全吻合 `[实证]`。
2. **发出（NKDUSCAN / NKDSBP2 的 `NkDriverEntry`）** —— md3 把 CDB 长度/指针装进传输层 request（§2.3）后经 `0x1009A32A` 下发；DLL 落到具体总线 API：
   - **NKDUSCAN（USB 批量传输）**：`CreateFileA` `0x1000320D`/`0x10003B8C`/`0x100053A5`； **`WriteFile` `0x10002B41`**（包 `0x10002B20`）、`ReadFile` `0x10002B08`、`CloseHandle` `0x1000324E`/`0x10003BC7`/`0x1000543B`；另有 5 处 `DeviceIoControl`（`0x10002DA0`、`0x10003023`、`0x1000323E`、`0x10003BBE`、`0x100054D6`，多为设备枚举/属性）。
   - **NKDSBP2（IEEE1394 SBP-2）**：`CreateFileA` `0x10005642`、**`DeviceIoControl` 仅 1 处 `0x10002B66`**，ioctl 码 **`0x190012`**（`0x10002B60 push 0x190012` 紧邻 `call`），输入缓冲 `[obj+0x18]` / 0x2C 字节，输出缓冲 `[request+0x20]` / 长度 `[obj+0x28]`。
3. **md3 自身没有任何 SCSI/内核通道**：md3 的 105 项导入里没有 `DeviceIoControl`、`SCSI_PASS_THROUGH`、`\\.\`（全文件 0 命中）`[实证]`。

**一句话**：`md3 造 CDB → NkDriverEntry 传 CDB → NKDUSCAN 用 WriteFile（USB）或 NKDSBP2 用 DeviceIoControl(0x190012)（1394）出主机。`

完整链路：

```
宿主 → LS8000.md3（机型逻辑层：构造 CDB 命令对象 [this+8]，长度 6/10）
   └─ 传输层对象（vtable 0x100C2620 / 0x100C2660）
        └─ 加载器（vtable 0x100C25D0）slot[2] LoadLibraryA + GetProcAddress("NkDriverEntry") → loader+4
             └─ slot[4] 0x1009A2E0 → 0x1009A32A call [loader+4]
                  └─ NkDriverEntry(selector 1..9, request, ctx)
                       NKDUSCAN：CreateFileA + WriteFile(request[+0x18], request[+0x14])
                       NKDSBP2 ：DeviceIoControl(h, 0x190012, [obj+0x18], 0x2C, request[+0x20], [obj+0x28])
```

---

## 4. selector 空间

### 4.1 md3 `NkCtrlEntry`（取值全集 `[实证]`）

| selector | 臂 | 前置查表 | 闸门（a2/a3 低 16 位） | 行为 |
|---|---|---|---|---|
| 0 与负值 | `0x10091EDA` | 有 | — | 返回 `6` |
| 1 | `0x10091DC4` | 无 | `a2==1 && a3==2` | `call [vt+8]`=`0x10092770` |
| 2 | `0x10091DF1` | 无 | 无 | `call [vt+0x14]`=`0x10092E80` |
| 3、4 | `0x10091F34` | 有 | 无 | 按 `[req+0x0C]` 在 `this+0x14` 的 map 找命令对象；未命中返回 `6`；命中则 `call [obj->vtbl+4](a2,a3,req)`（`0x10091F77`） |
| 5 | `0x10091E05` | 有 | 无 | `0x10091A50(this,[req+8])`：按设备 ID 找设备对象并 `call [dev->vtbl+8]` |
| 6 | `0x10091E1D` | 有 | `a3==1` | `call [vt+0x1C]`=`0x10091AE0` |
| 7 | `0x10091EB6` | 有 | 无 | `call [vt+0x20]`=`0x100A37A0`（**桩**：直接返回 0） |
| 8 | `0x10091E3E` | 有 | `a3==1` | `call [vt+0x24]`=`0x10092EE0` |
| 9 | `0x10091E5F` | 有 | `a3==1` | `call [vt+0x28]`=`0x10092870` |
| 10 | `0x10091E7C` | 有 | `a3==1` | `call [vt+0x2C]`=`0x10091C70` |
| 11 | `0x10091E99` | 有 | `a3==1` | `call [vt+0x30]`=`0x10091CB0` |
| `0x1000` | `0x10091F7C` | 无 | — | 直接返回 0 |
| `0x2000` | `0x10091F0F` | 无 | `a2==1 && a3==2` | `call [vt+0xC]`=`0x10092D30` |
| `0x2100` | `0x10091EEA` | 有 | `a2==0xA && a3==1` | `call [vt+0x10]`=`0x10091C10` |
| 其他 | `0x10091EDA` | — | — | 返回 `6` |

语义补充 `[实证]` + `[推断]`：`selector=3` 是 REQUEST SENSE。唯一自证的内调用点 `0x1007958C`：`NkCtrlEntry(3, 3, 0xE, &buf)`，随后 `0x10079591`–`0x100795B6` 把 4 字节拼成 sense 码 → `[推断]` a3=0xE 为 sense 长度、CDB `0x03`。**反证条件**：若 `[req+0x0C]` 命中对象后调的是非 sense 虚方法，则该语义只覆盖 a3=0xE 这一路。

### 4.2 md3 `NkMDCtrlEntry`（`[实证]`）

| selector | 内部函数 | 校验 | 语义（`[推断]`） |
|---|---|---|---|
| 1 | `0x1000B220` | `[req+4]==1`、`[req+0]==0x10`、`memcmp([req+0xC],"1000",4)==0` | 打开模块：分配句柄写 `[req+8]`（`0x100D165C` 自增） |
| 2 | `0x1000B270` | `[req+4]==1`、`[req+0]==0x10` | 探测/校验：符合返回 0，否则 `0x1005` |
| 3 | `0x1000B2A0` | `[req+4]==2`、`[req+0]==0x14` | 取能力对象 `0x8105`/`0x1025`（`0x1004CEA0`，`0x1000B2F9`），按 `[req+0x10]` 分支调用虚槽 `+0x1C`/`+0x20`；失败 `0x1005/0x1006/0x1009` |
| 4 | `0x1000B3A0` | `[req+4]==3`、`[req+0]==0x58` | 调用虚槽 `+0x24([req+0xC],[req+0x10],&[req+0x14],&[req+0x18])`，再 `call [obj->vtbl+0](…,1)` 校验，`0x8002` 特判 |
| ≥5 | `0x1000B571` | — | **非法，返回 `0x1001`** |

### 4.3 `selector=5` 在两处的行为（明确回答）

- **`NkCtrlEntry(5, …)` 合法**：`0x10091E05` 取 `[req+8]` 当设备 ID → `0x10091A50` 遍历 `this+0x18` 链，比较 `[dev+0x80]==id`（`0x10091A67`），命中后 `call [dev->vtbl+8]`；未命中返回 0。**＝按设备 ID 定位设备对象并调用其虚方法 #2。**
- **`NkMDCtrlEntry(5, …)` 非法**：`dec/cmp 3/ja` 截到 `0x1000B571`，返回 `0x1001`。

### 4.4 「第 13 章的 selector 5 属于 `NkDriverEntry`（NKDSBP2.dll）」是否成立？

**成立，本轮新增两条硬证据。**

1. **空间不同**：`NkDriverEntry` 的选择子域是 **1..9**（`add eax,-1; cmp eax,8; ja`，两个 DLL 同构），与 `NkCtrlEntry` 的 16 位有符号域（含 `0x1000/0x2000/0x2100`）**无交集**；`NkMDCtrlEntry` 的 5 直接非法。三者数值巧合，非同一编号系统。
2. **5 在传输层确有特判**：md3 的封装器 `0x1009A31E`–`0x1009A321` 只在 selector==5 时把 `loader+0x14`（设备能力位 `[x+8]&0x20`）写进 `request+8`；NKDUSCAN 的 sel5 处理函数 `0x10003FD0` 也是唯一检查 `[req+0x24] >= 0x20` 且「有 `[req+4]` 就必须有 `[req+0x20]`」的一路 → 5 是**带特殊 flags/缓冲要求的事务**（与固件更新场景吻合）。
3. `NkDriverEntry` 的两个宿主在 md3 中并存可切换（`0x100C2620` vs `0x100C2660`），进一步说明这是 **DLL 自己的**选择子空间。

→ 判定：**第 13 章判断成立**；`NkCtrlEntry` 的 `5`（按设备 ID 下发）与 `NkDriverEntry` 的 `5`（特殊事务/更新）是两套编号，**不可互推** `[实证]` + `[推断]`。

---

## 5. `NkMDCtrlEntry` vs `NkCtrlEntry`（给依据）

| 维度 | `NkMDCtrlEntry` | `NkCtrlEntry` | 依据 |
|---|---|---|---|
| 签名 | 2 参 `ret 8` | 4 参 `ret 0x10` | `0x1000B53E` vs `0x10091865` |
| `this` | 无（纯函数） | `ecx` = 进程级单例（`0x100D85A0`，0x34 B，`0x100918A0` 懒构造） | `0x10091859`–`0x1009185D` |
| 选择子域 | 1..4（32 位无符号 + `dec`） | 1..11、`0x1000`、`0x2000`、`0x2100`（**16 位有符号**） | `0x1000B520`–`0x1000B528` vs `0x10091D5C`–`0x10091DB7` |
| 分派形态 | 1 张 4 项表 `0x1000B57C` | 11 项表 `0x10091F88` + 4 处比较树 + 1 个前置查表 | 同上 |
| 非法值 | `0x1001` | `6` | `0x1000B571` / `0x10091EDA` |
| request 语义 | 长度+类型自校验、句柄出参、模块码 memcmp | 键/子键查表、`+4/+8/+0xC` 回填、`+0x08` 设备 ID | §2.5 |
| 能力 ID 使用 | 用 `0x8105`+`0x1025` 造对象（`0x1000B2F9`/`0x1000B3F5`） | **不用**能力 ID，全走虚方法槽 | `0x1004CEA0` 调用点 |
| 是否触达传输层 | 未见直接调用（无 CDB 构造） | sel 3/5 等臂经设备对象可下探到传输层 | `[推断]`，依据：只有后者持有设备 ID 语义 |
| 共享代码 | 与 `NkCtrlEntry` **零共享** | — | CFG 无交叉调用（除 `0x1000B2A0`→`0x1004CEA0`→`0x10071A60` 工厂链） |

一句话：**`NkMDCtrlEntry` 管“模块/句柄生命周期”（open/probe/enum/set），`NkCtrlEntry` 管“设备命令下发”（1..11 动作编号，`0x1000`/`0x2000`/`0x2100` 保留控制码）。两者唯一共同点是都用 `request` 指针，但结构不同。**

---

## 6. 未解决疑问（5 条）

1. **md3 侧传输层 request 的构造点仍未锁定**。已知 md3 在 `0x1009A000`–`0x1009D3FF` 有大量对 `[reg+0x14]` 的**按字节写**（`0x1009B12A`、`0x1009B26B`、`0x1009B293`…40 处），形态像就地拼 SBP-2 命令块，但尚未追到「把 CDB 指针/长度写入某 request 的 `+0x18`/`+0x14` 并交给 `0x1009A2E0`」的那一段。下一步：从 vtable `0x100C2620/0x100C2660` 的 `slot[1]`（`0x1009C090`/`0x1009C0A0`）做 CFG 展开，反向找谁把 request 交给 `slot[4]`。
2. **`NkMDCtrlEntry` sel=4 的 0x58 字节变体尾部（`+0x1C`–`+0x57`）**全部由能力对象 `0x8105`（`0x1000B190` 构造，vtable `0x100BE750`）的虚槽 `+0x24` 解读，该 vtable 未展开。
3. **`MAIDEntryPoint` 的 a6 回调**签名（7 实参压栈次序）与语义未定；16 个臂的“用臂常量替换 a2”是否等价于功能号下推，仍只有间接证据。
4. **NKDSBP2 的 ioctl `0x190012` 与 `[obj+0x18]` 的 0x2C 字节输入块**格式未解（疑为 SBP-2 ORB/命令描述符）；NKDUSCAN 5 处 `DeviceIoControl`（尤 `0x10003023`、`0x1000323E`）用途未分类。下一步：解 `0x10002B20` 之前对 `[obj+0x18]` 的填充过程。
5. **导出名 `YGFFFFPAX`（4×short + `void*`）与实测 `ret 0x10`（4×dword）矛盾**仍未解释（`dispatch.md` Q3 遗留）。新线索：内部调用点 `0x1007958C`、`0x10073C00` 全部按 **dword** 压 selector（`push 3`/`push 0x2000`），若按 `short` 声明应是 `push word` → `.def`/实现不同步的可能性更大。

---

## 附：本轮脚本与中间产物（均在 `md3/_f6/`）

| 文件 | 作用 |
|---|---|
| `dll_entry.py` → `dll_entry.txt` | 两个 DLL 的 `NkDriverEntry` 入口反汇编（发现 3 参 `ret 0xC`、选择子 1..9） |
| `dll_ioctl2.py` → `dll_ioctl2.txt` | IAT 归属扫描，列出全部 `DeviceIoControl/CreateFileA/WriteFile/ReadFile` 调用点 |
| `dll_ioctl3.py`、`dll_win.py` → `dll_win.txt` | NKDUSCAN `CreateFileA+DeviceIoControl` 枚举函数、两 DLL 跳转表（9 项） |
| `dll_arms2.py` → `dll_arms2.txt`/`dll_arms3.txt` | 各选择子内部函数入口与参数校验 |
| `dll_anchor.py` → `dll_anchor.txt` | 窗口扫描定位同一基址读 `+0x14/+0x18/+0x1C/+0x20` 的位置（17/11 候选） |
| `dll_dump.py` | 命令行区间反汇编（用于逐个核验） |
| `nk_call.py` / `nk_call2.txt` | md3 全 `.text` 278,657 条指令扫描 `mov R,[X+4]; call R`（0 命中 → 改为查虚表名） |
| `f6vt.txt` | 三个 vtable 内容（发现 `0x100C25D0` 只有 8 项，后面紧跟 DLL 名字符串） |
| `f6load.txt` | 加载器虚方法反汇编；**核心产物：调用点 `0x1009A32A`** |
| `prov2.py`、`anchor.py`、`xref.py`、`sibs.txt` | 上一轮产物，本稿复核时用 |
