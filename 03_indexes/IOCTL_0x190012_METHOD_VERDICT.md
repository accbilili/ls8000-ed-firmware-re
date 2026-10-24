# 裁决：0x190012 的 METHOD 语义（驱动侧反汇编实证）

日期：2026-10-25 · 样本：`C:\Windows\System32\DriverStore\FileRepository\sti.inf_amd64_14dc9a213197a8b8\scsiscan.sys`
（57,344 B，sha256 `71f33f6ac3973990fe1488fc73533bc0771b93aa0b278fcff38968adf7f5a236`，64 位 in-box）
工具：capstone 5.0.7 + 自写 IAT/`.pdata` 解析 · 脚本在 `03_analysis\status\_verify\`
**只读，未修改驱动、未修改任何已有文档。**

---

> **✅ 本文件为最终裁决（打包阶段定稿）**
> 配套文档：`LIVE_LINE_INDEX.md`（实机线册 · 已二次校订）、
> `EDGES_0x40_STATE_AUDIT.md`（产物侧审计）、`VERDICT_0x400408.md`（固件参数侧裁决）。
>
> **已回写位置（打包阶段 R24）**：
> `03_analysis/live/INCIDENT-20241024-实机协议与蓝屏.md`（ioctl 表格行 + §1.2/§1.3）、
> `REPORT_实机验证交接.md:164`（Method 名 + §9 失效引用 `md3dis.py`）、
> `REPORT_实机验证方案.md:42/110-113`（Method 声明）、
> `REPORT_全面分析总结-20261024.md` §6（ioctl 行 + 2340 组真因）、
> `REPORT_回写总账-20261024.md` D5 条、`交叉结论-给实机验证线-20261024.md` 头部。

## 0. 结论（一句话）

**三方说法都不对，且是两种不同的错。**
- 三处文档写的 `METHOD_BUFFERED` —— **错**：按 CTL_CODE 算术，`0x190012` 的 Method 位 = 2 = **`METHOD_OUT_DIRECT`**；且驱动行为是「直接写用户缓冲」，不是「I/O Manager 代拷贝」。
- live-line 写的 `method=2=METHOD_NEITHER` —— **错在命名**：Method=2 的标准名是 `METHOD_OUT_DIRECT`；`METHOD_NEITHER` 需要 Method=3（即 `0x190013`/`0x190023`）。算术本身对，名称错。
- 正确表述：**`0x190012` = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`**，且**输出直写用户缓冲**（输出侧不拷贝、输入侧由 I/O Manager 缓冲）。

---

## 1. CTL_CODE 算术（唯一解）

WDK `wdm.h`：
```
#define CTL_CODE(DeviceType, Function, Method, Access) \
    (((DeviceType) << 16) | ((Access) << 14) | ((Function) << 2) | (Method))
METHOD_BUFFERED=0  METHOD_IN_DIRECT=1  METHOD_OUT_DIRECT=2  METHOD_NEITHER=3
FILE_ANY_ACCESS=0  FILE_READ_ACCESS=1  FILE_WRITE_ACCESS=2  FILE_READ_WRITE_ACCESS=3
```

`0x190012` 拆解：

| 字段 | 值 | 名称 |
|---|---|---|
| DeviceType | `0x19` (25) | FILE_DEVICE_SCANNER |
| Access | `0` | FILE_ANY_ACCESS |
| Function | `0x004` | — |
| **Method** | **`2`** | **METHOD_OUT_DIRECT** |

**穷举唯一性**：对 Function∈[0,16) × Method∈[0,4) × Access∈[0,4) 全枚举，能产出 `0x190012` 的组合**只有** `(F=0x004, M=2, A=0)`。不存在第二种解释。

**反证两份写法**：

| 写法 | 展开结果 | 与 `0x190012` 是否相符 |
|---|---|---|
| `CTL_CODE(0x19, 0x012, METHOD_BUFFERED, FILE_ANY_ACCESS)` | `0x190048` | ✗ |
| `CTL_CODE(0x19, 0x004, METHOD_BUFFERED, FILE_ANY_ACCESS)` | `0x190010` | ✗ |
| `CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)` | **`0x190012`** | ✓ |

→ 三处文档写的 `METHOD_BUFFERED` 与它们自己写的宏展开式**自相矛盾**：那个宏展开出来根本不是 `0x190012`。

### 1.1 驱动认可的 5 个 ioctl 的 method 位

| ioctl | Function | Method | 标准名 | 驱动分派 |
|---|---|---|---|---|
| `0x190012` | 0x004 | 2 | METHOD_OUT_DIRECT | `0x140008CC2` |
| `0x190016` | 0x005 | 2 | METHOD_OUT_DIRECT | `0x140008CA6` |
| `0x19001A` | 0x006 | 2 | METHOD_OUT_DIRECT | `0x140008C8D` |
| `0x19001C` | 0x007 | **0** | **METHOD_BUFFERED** | `0x140008C5C` |
| `0x190022` | 0x008 | 2 | METHOD_OUT_DIRECT | `0x140008BFC` |

→ **只有 `0x19001C` 是 METHOD_BUFFERED**（`0x19001C` 走 `0x140008C5C`，该块直接读写 `[rsi+0x18]` = SystemBuffer 且做 `xchg`/`mov` 回写 —— 典型 buffered 语义）。
→ `0x190012` 与另外三个都是 OUT_DIRECT，其处理块形态一致（自建 MDL + 直写）。

---

## 2. 驱动行为实证（决定性证据）

### 2.1 分派与函数边界

`.pdata` 异常目录给出 `0x190012` 处理块所属函数边界：**RVA `0x08B00` – `0x0904C`**（1356 B）。
分派链（`0x140008BA7` 起）：
```
sub ecx, 0x190012 ; je 0x140008CC2   ← 目标
sub ecx, 4        ; je 0x140008CA6   ← 0x190016
sub ecx, 4        ; je 0x140008C8D   ← 0x19001A
sub ecx, 2        ; je 0x140008C5C   ← 0x19001C  ← 唯一 METHOD_BUFFERED
cmp ecx, 6        ; je 0x140008BFC   ← 0x190022
（都不中 → inc byte ptr [rsi+0x43] 记未知 ioctl 并失败）
```

### 2.2 `0x190012` 处理块逐条

```asm
0x140008CC2  mov      rcx, rsi
0x140008CC5  call     qword ptr [rip - 0x1bb4]   ; IoIs32bitProcess   ← ★
0x140008CD1  mov      ecx, dword ptr [rbx + 0x10] ; InputBufferLength
0x140008CD4  test     al, al
0x140008CD6  je       0x140008d5e                 ; 64 位分支
; ===== 32 位调用者分支 =====
0x140008CDC  cmp      ecx, 0x2c                   ; ★ 入参 ≥ 44 (0x2C)，否则 STATUS_INVALID_PARAMETER
0x140008CE1  edx=0x38 ; ecx=edx+8 ; r8d='SITS'(0x53495453)
0x140008CEF  call     qword ptr [rip - 0x1cc6]   ; ExAllocatePool2(0x40, 0x38, 'SITS')
0x140008D12  mov      rcx, qword ptr [rsi + 0x18] ; ← Irp->AssociatedIrp.SystemBuffer（输入，内核地址）
0x140008D16  mov      eax, dword ptr [rcx + 4]    ; 逐字段搬运 +0x04
0x140008D1E  mov      eax, dword ptr [rcx + 8]    ; +0x08
0x140008D26  mov      al, byte ptr [rcx + 0xc]    ; +0x0C  CdbLength
0x140008D2E  mov      al, byte ptr [rcx + 0xd]    ; +0x0D  SenseInfoLength
0x140008D36  mov      eax, dword ptr [rcx + 0x10] ; +0x10  DataTransferLength
0x140008D3E  mov      eax, dword ptr [rcx + 0x24] ; ★ +0x24 4 字节指针 → 展宽成 8 字节
0x140008D41  mov      qword ptr [r12 + 0x28], rax
0x140008D46  mov      eax, dword ptr [rcx + 0x28] ; ★ +0x28 4 字节指针 → 展宽成 8 字节
0x140008D49  mov      qword ptr [r12 + 0x30], rax
0x140008D4E  movups   xmm0, xmmword ptr [rcx + 0x14]  ; +0x14..0x23 16 字节 CDB 区
0x140008D52  movdqu   xmmword ptr [r12 + 0x14], xmm0
; ===== 64 位调用者分支 =====
0x140008D5E  cmp      ecx, 0x38                   ; ★ 入参 ≥ 56 (0x38)
0x140008D67  mov      rbx, qword ptr [rsi + 0x18] ; SystemBuffer 直接当描述符用（不再拷贝）
```

**输入侧结论**：驱动从 `Irp->AssociatedIrp.SystemBuffer`（`[rsi+0x18]`）取输入，**无 `ProbeForRead`/`ProbeForWrite`**（全文件 0 命中，导入表里根本没有这两个 API）。
→ 输入由 **I/O Manager 缓冲**（这是 OUT_DIRECT 下输入侧的正常行为），**排除 METHOD_NEITHER**（NEITHER 时驱动必须自己 probe 用户指针）。

### 2.3 输出侧：自建 MDL + 直写用户页

```asm
; ---- 数据缓冲（描述符 +0x28，即原始结构 +0x24 的展宽指针）----
0x140008E95  mov      rdx, qword ptr [rbx + 0x28]  ; ★ 用户态数据缓冲地址
0x140008E99  xor      ecx, ecx
0x140008E9B  call     qword ptr [rip - 0x1e0a]    ; MmCreateMdl(NULL, va, len)
0x140008EBA  mov      dl, byte ptr [rsi + 0x40]   ; Irp->RequestorMode
0x140008EC0  call     qword ptr [rip - 0x1e37]    ; MmProbeAndLockPages(...)
0x140008EF1  call     qword ptr [rip - 0x1db0]    ; MmMapLockedPages(...)
0x140008F05  mov      qword ptr [rbx + 0x28], rax  ; 换回映射后的内核地址
; ---- sense 缓冲（描述符 +0x30，即原始结构 +0x28 的展宽指针）----
0x140008DC9  mov      rdx, qword ptr [rbx + 0x30]  ; ★ 用户态 sense 缓冲地址
0x140008DCF  call     qword ptr [rip - 0x1d3e]    ; MmCreateMdl
0x140008DFA  mov      dl, byte ptr [rsi + 0x40]
0x140008E00  call     qword ptr [rip - 0x1d77]    ; MmProbeAndLockPages
0x140008E39  call     qword ptr [rip - 0x1cf8]    ; MmMapLockedPages
; ---- 收尾：解锁 + 释放 MDL ----
0x140008F91  call     qword ptr [rip - 0x1f90]    ; MmUnlockPages
0x140008FA0  call     qword ptr [rip - 0x1f5f]    ; IoFreeMdl
0x140008FD0  call     qword ptr [rip - 0x1fcf]    ; MmUnlockPages
0x140008FE3  call     qword ptr [rip - 0x1fa2]    ; IoFreeMdl
```

**关键判据（区分 BUFFERED / OUT_DIRECT / NEITHER）**：

| 判据 | 本驱动实测 | 含义 |
|---|---|---|
| `Irp->UserBuffer`（`[rsi+0x58]`）访问次数 | **0** | 不是 NEITHER（NEITHER 时输出缓冲在 UserBuffer） |
| `ProbeForRead` / `ProbeForWrite` 导入 | **0 次**（全文件 0 命中） | 不是 NEITHER 风格 |
| `Irp->MdlAddress`（`[rsi+8]`）访问 | 有（`0x140008C10`/`0x140008C22`/`0x140008D6B`），且 `cmp dword ptr [rax+0x28], ecx` 比对 **MDL.ByteCount** | **有 MDL ⇒ I/O Manager 为 OUT_DIRECT 建的 MDL** |
| `MmCreateMdl` / `MmProbeAndLockPages` / `MmMapLockedPages` | 2 / 2 / 3 次 | 驱动对**结构内嵌的**用户指针自建 MDL 并直写 |
| `Irp->IoStatus.Information`（`[rsi+0x38]`） | 写 5 次 | 返回字节数语义正常 |

**结论**：输出缓冲由 **I/O Manager 提供 MDL（`Irp->MdlAddress`）**，驱动再对它 `MmMapLockedPages` 后**直接写用户页** —— 这是 **METHOD_OUT_DIRECT** 的教科书形态。
（METHOD_BUFFERED 时驱动不会看到 MDL、不会 probe/map，而是写 SystemBuffer 由 I/O Manager 回拷。）

### 2.4 「数据出现在输出缓冲」这一实测现象的解释

live-line 的疑问是：「METHOD_NEITHER 下 lpOutBuffer 即用户缓冲」是否影响该现象？
**不影响现象，但解释要换**：

在 OUT_DIRECT 下，`DeviceIoControl` 的 **输出缓冲（lpOutBuffer）就是用户缓冲本身**，I/O Manager 不拷贝、直接给驱动 MDL，驱动写完用户态立刻可见。
⇒ 实测「数据出现在输出缓冲（`bytesRet` = 数据长度），不在用户态 DataBuffer 指针」与 OUT_DIRECT **完全自洽**，而且比 METHOD_BUFFERED 更精确：
- BUFFERED 时数据应先落 I/O Manager 的内核缓冲、返回时回拷到 lpOutBuffer；
- OUT_DIRECT 时数据**直接**落 lpOutBuffer（用户缓冲），`bytesRet` 即 `IoStatus.Information`。

⇒ **现象不变，结论从 METHOD_BUFFERED 改为 METHOD_OUT_DIRECT。**

---

## 3. 对三处文档的修正建议（我不改，列出待改点）

| 文件 | 行 | 现状 | 建议改为 |
|---|---|---|---|
| `03_analysis\live\INCIDENT-20241024-实机协议与蓝屏.md` | 19 | `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x012, METHOD_BUFFERED, FILE_ANY_ACCESS)` | `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`（Function 位应为 0x004，Method 应为 2） |
| 同上 | 45 | 「SCSI 数据落在 METHOD_BUFFERED 的『输出缓冲』里」 | 「SCSI 数据**直写** OUT_DIRECT 的输出缓冲（用户缓冲本身，无回拷）里」 |
| `REPORT_实机验证方案.md` | 42 | `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_BUFFERED, FILE_ANY_ACCESS)` | 同上，Method → `METHOD_OUT_DIRECT` |
| 同上 | 110–113 | 「解 0x190012：CTL_CODE(0x19, 0x004, METHOD_BUFFERED, FILE_ANY_ACCESS)」+「Method `METHOD_BUFFERED`」 | Method → `METHOD_OUT_DIRECT`（并可补：Access `FILE_ANY_ACCESS`、Function `0x004` 正确） |
| `REPORT_实机验证交接.md` | 164 | `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_BUFFERED, FILE_ANY_ACCESS)` | 同上 |

**注**：`REPORT_实机验证方案.md` / `REPORT_实机验证交接.md` 写的 Function `0x004` 是**对的**，错的只是 Method 名。

---

## 4. 对 live-line 三条同步信息的回应

1. **`ps_probe5.ps1` 不含 `$INQ36` 逐字节比对** —— **核实无误**。实测各文件 `INQ36` 出现次数：`ps_brute`/`ps_probe`/`ps_probe2`/`ps_probe3`/`ps_probe4` 各 **2**；`ps_probe5`/`ps_probe6`/`ps_readonly` 各 **0**。
   （补充：`ps_probe6.ps1` 也是 0，`ps_readonly.ps1` 也是 0 —— 比 live-line 列的范围还多两个文件。probe5 是纯三缓冲同印、无命中判定。）

2. **`0x190012` 的 METHOD** —— 见上，结论是 **METHOD_OUT_DIRECT**（既不是 METHOD_BUFFERED，也不是 METHOD_NEITHER）。
   - live-line 的算术（func=0x004、method=2）**正确**，仅名称错：Method=2 = `METHOD_OUT_DIRECT`。
   - 三处文档的 `METHOD_BUFFERED` 也不对，且其自带的宏展开式（= `0x190010` / `0x190048`）与常量 `0x190012` 自相矛盾。
   - **「数据出现在输出缓冲」的现象不变**，不需要改动实测现象的描述。

3. **`REPORT_实机验证交接.md` §9 列出 `live\md3dis.py` 但该目录无此文件** —— **核实无误**。
   `03_analysis\live\` 实测 **13 个文件**：`INCIDENT-20241024-实机协议与蓝屏.md`、`drv_ioctl.py`、`drv_paths.py`、`md3_setupdi.py`、`ps_brute.ps1`、`ps_probe.ps1`、`ps_probe2.ps1`、`ps_probe3.ps1`、`ps_probe4.ps1`、`ps_probe5.ps1`、`ps_probe6.ps1`、`ps_readonly.ps1`、`scsi_readonly.py`。**确无 `md3dis.py`**（`md3_setupdi.py` 是另一个东西，不是它）。
   → 我的反汇编工作不依赖该脚本；驱动侧分析已用自写 capstone 脚本完成（见 §5）。

---

## 5. 复现方式（只读）

```bash
cd LS8000/03_analysis/status/_verify
python ioctl_verdict.py   # CTL_CODE 算术 + 驱动分派链 + 导入表
python ioctl_iat.py      # IAT 解析 + 处理块全量反汇编（call 已解析为 API 名）
python ioctl_func.py     # .pdata 函数边界 + Irp 字段普查 + 关键 API 计数
python ioctl_block.py    # .idata 字符串扫描 + 处理块
```
产物：`ioctl_verdict.json`、`ioctl_block_annotated.txt`、`ioctl_func.txt`

---

## 6. 实机线侧的连带修正（C2，已解）

### C2 —— `INCIDENT-…md` §1.3 括注里的字段号错了

§1.2 表格的「`+0x24`=数据、`+0x28`=sense」是**对的**；
错的是 §1.3 那句括注把「数据指针」写成了 `+0x28`。按驱动落点：

```
0x140008D3E  mov   eax, [rcx+0x24]  → 内部对象 +0x28   ; 数据指针
0x140008D46  mov   eax, [rcx+0x28]  → 内部对象 +0x30   ; sense 指针
0x140008D4E  movups xmm0, [rcx+0x14]                   ; CDB 16 字节整体拷
```

⇒ 该括注应改为 **`+0x24`**。〔R24 已回写〕

### 44 / 56 字节两条路径

```
0x140008CDC  cmp   ecx, 0x2C      ; 44 字节路径（32 位调用者）
0x140008D5E  cmp   ecx, 0x38      ; 56 字节路径（另一套布局）
```

### `ps_readonly.ps1` vs `ps_brute.ps1`

| 脚本 | 用的码 | 说明 |
|---|---|---|
| `ps_readonly.ps1:116` | **仅 `0x190012`** | 唯一走通通路的脚本 |
| `ps_brute.ps1:39` | `0x190012, 0x190004, 0x194004, 0x190014, 0x190024` | 历史暴力脚本；`0x190024` 不在驱动认的 5 个之内 ⇒ err=50 属预期 |

---

## 7. 措辞纪律（重要）

**「数据出现在输出缓冲」这个实测现象完全不变，只是机制解释更精确。**

- 原实测（属实，保留）：SCSI 数据出现在「输出缓冲」里，用户态立即可见
- 修正后的机制：OUT_DIRECT 下 `lpOutBuffer` 就是用户缓冲本身，
  I/O Manager **不做代拷贝**，驱动经 MDL + `MmMapLockedPages` 直写用户页
- ⇒ 措辞用「机制解释更精确」，**不要**写成「以前的实测结论错了」
- 「2340 组暴力扫描失败」这个**现象记录要保留**；
  真实原因改述为「**32 位调用者必须在结构体里传入有效指针，
  64 位进程的用户态指针普遍 > 4 GB、不被接受**」
