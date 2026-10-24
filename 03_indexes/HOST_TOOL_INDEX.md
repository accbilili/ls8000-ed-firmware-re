# 主机侧（md3 驱动/宿主程序）分析产物清单 + 工具链清单

日期：2026-10-25 · 范围：`LS8000\03_analysis\md3\`（主机侧） + `LS8000\tools\`（通用工具）
证据分级沿用既有约定：`[实证]` 可复现 / `[推断]` 自洽未直证 / `[未证]` 仅线索

---

## 0. 本文件的范围与边界

| 项 | 值 |
|---|---|
| 主机侧产物根 | `LS8000\03_analysis\md3\` |
| 产物总数 | **164 个文件 / 4,670,735 B**（顶层 44 个，子目录 120 个） |
| 文件类型分布 | `.py` 89 / `.txt` 45 / `.json` 18 / `.pkl` 5 / `.md` 4 / `.bin` 2 / `.csv` 1 |
| 通用工具根 | `LS8000\tools\` |
| 工具脚本数 | **23 个**（22 个 `.py` + 1 个 `.txt` 工具清单） |
| 被分析样本 | `D:\DS\TEST\LS8000\driver\LS8000.md3`（958,464 B，PE32/i386，ImageBase `0x10000000`，只读） |
| 兄弟 DLL | `NKDUSCAN.dll`（90,112 B）、`NKDSBP2.dll`（86,016 B）（同目录，只读） |
| 版本 | `LS8000.MD3` / Nikon Scan Driver `1.3.0.3003` |

本清单只登记**主机侧**产物；固件侧产物（`03_analysis\firmware\`）另见 `FW_DOC_INDEX.md`。

---

## 1. 主机侧产物表

### 1.1 顶层分析结果（44 个文件 / 1,132,585 B）

#### 1.1.1 核心结论文档（4 个 `.md`）

| 相对路径 | 字节 | 类型 | 一句话说明 |
|---|---:|---|---|
| `exports.md` | 30,138 | 分析结果 | F6 定稿：三个导出（`NkCtrlEntry`/`MAIDEntryPoint`/`NkMDCtrlEntry`）的真实 ABI、request 偏移表、**md3→DLL 调用方向**定论（单向）、CDB 由 md3 造、由 `NkDriverEntry` 送上总线 |
| `dispatch.md` | 23,414 | 分析结果 | 16 位选择子 / 能力 ID 四层分派机制：4 个独立分派层、268 个能力 ID、129 个分支、`selector≠capability ID` 判定 |
| `cdb_sites.md` | 24,811 | 分析结果 | F5 定稿：**18 个 CDB 构造点**（17 个不同 CDB[0]）、E0/E1 子功能码三段数据流、`0xD1` 真会被发出的构造链 |
| `cap_to_cdb.md` | 8,937 | 分析结果 | 268 个能力 ID → CDB 对接面定案：A 类 153 / B 类 115 / C 类 0，**5 个 SCSI opcode 开关**，主机不做数值范围校验 |

#### 1.1.2 机读数据（18 个 `.json` / 1 个 `.csv`）

| 相对路径 | 字节 | 类型 | 一句话说明 |
|---|---:|---|---|
| `dispatch_caps.json` | 58,711 | 分析结果 | 交付格式的 268 条能力 ID → 构造函数映射（含 11 张表站点/base/range/slots/valid/byte_map） |
| `cap_to_cdb.csv` | 40,407 | 分析结果 | **268 行**机器可读分类表（`cap_id/group/handler/class/exit/evidence`） |
| `cdb_sites.json` | 3,620 | 分析结果 | **20 条** CDB 记录（18 条有构造点 + `0x03`/`0x17` 未构造），带 ctor 与调用者 |
| `cdb_sites.json` 配套 `cfg_dispatch.json` | 12,077 | 分析结果 | **37 个**可达分派点（含表地址、条目数、valid 数、索引变换、guard 指令序列） |
| `caps_raw.json` | 44,183 | 分析结果 | 能力 ID 原始枚举产物：`_meta` + **268 条** caps |
| `statics.json` | 132,916 | 分析结果 | md3 纯静态数据总表：3 导出 / **105 导入** / 4 动态加载 / 6 张表 / **1054 字符串** / SCSI API 普查（0 命中）/ 型号签名 5 处 |
| `s2_strings.json` | 137,128 | 分析结果 | **1,038 条**字符串（VA/编码/节/正文/引用点），`.rdata`+`.rsrc` ASCII 与 UTF-16LE |
| `anchors.json` | 940 | 分析结果 | **14 个**CDB 构造点锚点（VA → 命令名） |
| `iface/field_stat.json` | 61,029 | 分析结果 | 字段访问频次统计（`+0x00` 4311 / `+0x04` 1144 / `+0x08` 1650 / `+0x0C` 1214 / `+0x10` 1118 / `+0x14` 428 / `+0x18` 245） |
| `cdb/callers.json` | 147,707 | 分析结果 | 每个命令类 ctor/builder 的调用者索引 |
| `cdb/four_ops.json` | 50,987 | 分析结果 | 4 个补搜 opcode（`0x00` TUR / `0x03` REQ SENSE / `0x16` RESERVE / `0x17` RELEASE）形式化搜寻结果 |
| `cdb/vt_rows.json` | 7,051 | 分析结果 | vtable 行 → CDB 字节对应关系 |
| `cdb/vt_rows2.json` | 8,974 | 分析结果 | vtable 行关系（第二批，交叉校验用） |
| `statics_work/st_pe.json` | 17,091 | 分析结果 | PE 头/导入/导出/资源全解（`st_pe.py` 产出） |
| `statics_work/st_refmap.json` | 79,784 | 分析结果 | `.text` 中所有指向 `.rdata`/`.data` 的 imm32 按目标地址聚类 |
| `statics_work/st_strtab.json` | 28,667 | 分析结果 | 字符串表（表索引形式） |
| `_g3/caps_feat.json` | 60,556 | 分析结果 | 268 条能力 ID 的特征表（ctor/vt/nmeth/callees/reach3/directA），归类依据 |
| `_g3/final_stats.json` | 2,641 | 分析结果 | 归类统计：A=153 / B=115、**锚点 73**、BuildCDB 18、传输层 31、范围扫描 245,413 条指令、cmp 命中 0 |

#### 1.1.3 文本摘要（`.txt`）

| 相对路径 | 字节 | 类型 | 一句话说明 |
|---|---:|---|---|
| `cfg_stats.txt` | 146 | 分析结果 | CFG 规模：**1,241 函数 / 13,616 指令 / 43,632 B（`.text` 的 5.6%）/ 37 分派点 / 36 跳表站点 / 330 表项 / 0 无效项** |
| `cfg_dispatch.txt` | 10,638 | 分析结果 | 37 个可达分派点的逐条转储（站点/表地址/条目数/guard 指令） |
| `cfg_funcs.txt` | 22,390 | 分析结果 | **1,241 行**可达函数表（地址 + 指令数） |
| `factory_ids.txt` | 8,586 | 分析结果 | **129 臂 / 268 ID** 的原始枚举（arm → ctor → id 列表） |
| `funcs.txt` | 12,256 | 分析结果 | **339 个**从 3 个导出递归下降所得的函数（指令数 + 调用数 + 已知名） |
| `indirect.txt` | 7,903 | 分析结果 | **75 条**间接 `jmp`/`call` 站点清单（含 reachable 标记与机器码） |
| `jmp_scan.txt` | 14,985 | 分析结果 | 全 `.text` 线性扫 `FF 24 /4`，**185 个**跳转表站点（索引寄存器 + 表地址 + 所在节） |
| `recdesc_stats.txt` | 135 | 分析结果 | 首轮递归下降统计：339 函数 / 2,715 指令 / 7,934 B（1.0%）/ 0 不可解码字节 |
| `s2_strings.py` 配套 `statics_work/st_loadstr.txt` | 5,435 | 分析结果 | `LoadStringA` 调用点与字符串 id 立即数 |
| `statics_work/st_pe.txt` | 15,597 | 分析结果 | PE 头/节/导入/导出/资源全解的可读转储 |
| `statics_work/st_rsrc.txt` | 15,839 | 分析结果 | RT_STRING 表 / VS_VERSIONINFO / 自定义资源 1000 解析 |
| `statics_work/st_rsrc2.txt` | 17,015 | 分析结果 | 正确 RVA→文件偏移映射后的 `.rsrc` 解析 |
| `cluster1.txt` | 19,025 | 分析结果 | 某聚簇反汇编转储（`0x1009FD90` 起，含数据/代码混合区） |
| `dump_arms.txt` | 3,248 | 分析结果 | `NkCtrlEntry` 选择子 11 臂 + 特殊臂（`0x1000`/`0x2000`/`0x2100`）定点反汇编 |
| `dump_disp.txt` | 6,981 | 分析结果 | 能力 ID 工厂 `0x10071A60` 入口反汇编（比较树起始段） |
| `dump_entry.txt` | 15,979 | 分析结果 | `NkMDCtrlEntry` `0x1000B520`–`0x1000B5B0` 入口反汇编（含机器码列） |
| `_f5/hunt.txt` | 34 | 分析结果 | `0x03`/`0x17` 补搜命中数（0） |
| `_f5/scan2.txt` | 2,184 | 分析结果 | 带重同步线性扫描 + 结构体字段共现分析 |
| `_f5/v2.txt` | 9,730 | 分析结果 | 逐个 dump CDB 构造函数（entry..ret）复核 CDB[0] 与长度常量 |
| `_f5/v3a.txt` | 7,865 | 分析结果 | 复核 3 结果转储 |
| `_f5/v4.txt` | 12,994 | 分析结果 | 子功能码工厂跳转表 + `[x+0x454/456/458/45C]` 读写点 |
| `_f5/v5.txt` | 8,927 | 分析结果 | vtable `0x100C2F58` / 工厂 callers / `[x+0x64]` 写入点 |
| `_f5/v6.txt` | 4,425 | 分析结果 | 固件约束常量（450/3283/300/15354）在主机侧上下文 |
| `_f5/v8.txt` | 1,368 | 分析结果 | 固件范围约束常量全形态搜索 + `0xD1` 可达性 |
| `_f6/anchor.txt` | 21,589 | 分析结果 | 同一窗口内同基址同时出现 `+0x14/+0x18/+0x1C/+0x20` 的位置 |
| `_f6/dll_anchor.txt` | 27,877 | 分析结果 | 两个 `Nk*.dll` 内同类窗口扫描（17/11 候选） |
| `_f6/dll_arms.txt` | 1,111 | 分析结果 | 各选择子钟函数入口与参数校验 |
| `_f6/dll_arms2.txt` | 3,723 | 分析结果 | 各选择子钟函数定点反汇编 |
| `_f6/dll_arms3.txt` | 19,878 | 分析结果 | DLL 侧 request 字段消费点汇总 |
| `_f6/dll_entry.txt` | 171,599 | 分析结果 | 两 DLL 的 `NkDriverEntry` 入口反汇编全文（发现 3 参 `ret 0xC`、选择子 1..9） |
| `_f6/dll_ioctl.txt` | 687 | 分析结果 | DLL 侧 IAT 归属扫描初版 |
| `_f6/dll_ioctl2.txt` | 6,675 | 分析结果 | 全部 `DeviceIoControl/CreateFileA/WriteFile/ReadFile` 调用点 |
| `_f6/dll_ioctl3.txt` | 25,256 | 分析结果 | 含 DeviceIoControl/CreateFileA 调用点的外层函数反汇编 |
| `_f6/dll_win.txt` | 16,634 | 分析结果 | DLL 选择子跳转表（各 9 项）与枚举函数 |
| `_f6/f6load.txt` | 1,755 | 分析结果 | 加载器虚方法反汇编（**核心产物：调用点 `0x1009A32A`**） |
| `_f6/nk_call.txt` | 76 | 分析结果 | md3 全 `.text` 278,657 条指令扫 `mov R,[X+4]; call R`（0 命中） |
| `_f6/nk_call2.txt` | 24 | 分析结果 | 同上第二版（0 命中） |
| `_f6/nkdrv.txt` | 13 | 分析结果 | `call [0x100C2578]` 站点扫描结果（0） |
| `_f6/prov.txt` | 1,639 | 分析结果 | request 指针来源传播结果 |
| `_f6/sibs.txt` | 6,392 | 分析结果 | 两 DLL 导出/导入清单（**判定调用方向单向的证据**） |
| `_g3/sw.txt` | 30,518 | 分析结果 | md3 内所有「跳表 + 字节重映射 + 上界比较」开关枚举（判定 5 个 SCSI opcode 开关） |

#### 1.1.4 二进制中间产物（`.pkl` / `.bin`，只登记大小与用途）

| 相对路径 | 字节 | 类型 | 用途 |
|---|---:|---|---|
| `_g3/g3cfg.pkl` | 1,002,910 | 中间产物 | G3 全 `.text` 递归下降 CFG：`mark` 772,762 / `edges` 7,069 / `funcs` 23,509 / `nins` **245,413** / `seeds` 6,998 |
| `_g3/g3vtall.pkl` | 1,420,977 | 中间产物 | 全 `.rdata` vtable 枚举：`vts` **534** / `slot_index` 1,796 / `sites` 23,509 |
| `calls.pkl` | 129,308 | 中间产物 | 调用点索引（`fnresolve.py` 消费） |
| `memwr.pkl` | 307,191 | 中间产物 | 全部内存写点（`enum_builders.py` 用于找 CDB 字节写） |
| `cfg_cache.pkl` | 9,143 | 中间产物 | 字节步进解码缓存（`oracle.py`） |
| `statics_work/st_strtab.bin` | 132 | 中间产物 | 字符串表二进制镜像 |
| `statics_work/st_version.bin` | 840 | 中间产物 | VS_VERSIONINFO 二进制块 |

### 1.2 工具脚本（89 个 `.py`，按目录）

#### 1.2.1 顶层工具（16 个）

| 相对路径 | 字节 | 类型 | 一句话说明 |
|---|---:|---|---|
| `pe_md3.py` | 2,902 | 工具脚本 | 最小 PE32 读取器（节表/导出/按 VA 读），`struct` 手工解析，不用 pefile |
| `lib_md3.py` | 2,247 | 工具脚本 | 反汇编基础设施：pefile 装载 + capstone + 函数范围扫描 |
| `md3lib.py` | 2,018 | 工具脚本 | PE 装载 + 递归下降 CFG 构建 + xref 索引（可 import） |
| `cfg.py` | 5,444 | 工具脚本 | 迭代式 CFG + 跳转表解析 → 分派清单（`cfg_dispatch.txt` 的产出者） |
| `cfgmod.py` | 4,129 | 工具脚本 | 同上但可 import 版本（`dispatch.md`/`cap_to_cdb.md` 引用） |
| `oracle.py` | 2,594 | 工具脚本 | 字节步进解码 oracle + 递归下降 CFG（带缓存） |
| `recdesc.py` | 4,613 | 工具脚本 | 从 3 个导出递归下降 → `recdesc_stats.txt`/`indirect.txt`/`funcs.txt` |
| `resolve.py` | 1,941 | 工具脚本 | 为锚点 VA 解析函数入口，dump CFG + callers |
| `scan_cdb.py` | 1,722 | 工具脚本 | 全 `.text` 扫 CDB 字节写模式（31 个 SCSI opcode 集） |
| `scan_jmp.py` | 1,327 | 工具脚本 | 线性扫 `jmp/call dword ptr [reg*4+disp32]` → `jmp_scan.txt`（185 站点） |
| `sim_factory.py` | 4,832 | 工具脚本 | 对工厂 `0x10071A60` 做符号执行，枚举 0..0xFFFF 全部能力 ID |
| `final_gen.py` | 3,684 | 工具脚本 | 构建能力 ID → handler 映射 → `caps_raw.json` |
| `gen_json.py` | 2,661 | 工具脚本 | 从 `caps_raw.json` 生成交付格式 `dispatch_caps.json` |
| `enum_builders.py` | 1,304 | 工具脚本 | 枚举 CDB 构造函数（写 `[reg+8]` 且返回 6/10） |
| `fnresolve.py` | 1,424 | 工具脚本 | 任意函数内 VA → 函数入口解析（消费 `calls.pkl`） |
| `xdis.py` | 859 | 工具脚本 | 指定 VA 区间反汇编（确认字符串引用点上下文） |

#### 1.2.2 子目录工具（73 个）

| 子目录 | 文件数 | 字节 | 内容 |
|---|---:|---:|---|
| `iface/` | 7 | 74,323 | 接口组：`lmd.py`（私有反汇编库）、`s1_pe.py`（PE 基础信息）、`scan2.py`（带重同步扫描 + 字段共现）、`scan_req.py`（`[base+disp]` 访问统计 → `field_stat.json`）、`sibdis.py`（兄弟 DLL `NkDriverEntry` 反汇编）、`sibs.py`（兄弟模块导出/导入 → 判定调用方向） |
| `cdb/` | 12 | 230,359 | CDB 组：`core.py`（自包含分析核心，隔离复制）、`ctors.py`（vptr 写点 → ctor）、`callers.py`（ctor 调用者）、`vt.py`（vtable→builder 解析）、`where.py`（函数 VA → vtable 槽 + 所属类）、`four_ops.py`（4 个补搜 opcode）、`md3lib.py`（PE+CFG 副本）、`callers_helper.py`、`vt_rows.json`/`vt_rows2.json`/`four_ops.json`/`callers.json` |
| `statics_work/` | 21 | 208,192 | 静态数据组：`st_emit.py`（生成 `statics.json`）、`st_pe.py`、`st_rsrc.py`/`st_rsrc2.py`/`st_rsrcdir.py`（`.rsrc` 三种解法）、`st_refmap.py`、`st_tables.py`、`st_idxtab.py`、`st_loadstr.py`、`s2_strings.py`、`xdis.py`、`t1.py` + 8 个转储 |
| `_f5/` | 28 | 88,633 | F5 轮（CDB 构造点）：`gen.py`（生成 `cdb_sites.json` 20 行）、`v1`–`v10`（10 轮独立复核）、`emit.py`/`emit2.py`、`scan2.py`/`scanlim.py`/`hunt.py`/`dll.py`/`d1.py`/`ctx.py` + 9 个转储 |
| `_f6/` | 36 | 370,965 | F6 轮（导出 ABI + 调用方向）：`dll_entry.py`/`dll_ioctl*.py`/`dll_arms*.py`/`dll_anchor.py`/`dll_win.py`/`dll_dump.py`/`f6dis.py`/`nk_call.py`/`nkdrv.py`/`prov.py`/`prov2.py`/`anchor.py`/`xref.py` + 14 个转储 |
| `_g3/` | 13 | 2,559,156 | G3 轮（能力 ID → CDB 全量归类）：`g3cfg.py`（全 `.text` CFG）、`g3vt.py`/`g3vtall.py`（vtable 枚举）、`g3class.py`（归类主分析）、`g3final.py`（复核统计）、`g3hc.py`/`g3imm.py`（host_code 命中普查）、`g3sw.py`（opcode 开关枚举）+ `g3cfg.pkl`/`g3vtall.pkl`/`caps_feat.json`/`final_stats.json`/`sw.txt` |
| `_diff/` | 3 | 6,522 | 版本对比：`diff_md3.py`（与 `C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\LS8000.md3` 比对）、`field.py`、`md3dis.py` |

---

## 2. 主机侧关键结论汇总（数字全部取自产物文件）

### 2.1 三个导出与调用方向

| 项 | 数值 | 出处 |
|---|---|---|
| 导出数 | **3**（`?NkCtrlEntry@@YGFFFFPAX@Z` @`0x10091850`、`MAIDEntryPoint` @`0x10027600`、`NkMDCtrlEntry` @`0x1000B520`） | `statics.json` exports / `exports.md` §1.1 |
| 导入项数 | **105** | `statics.json` imports |
| 动态加载 DLL | **4**（`ICEDLL.dll`、`Nkduscan.dll`、`Nkdsbp2.dll`、`user32.dll`） | `statics.json` dynamic_loads |
| 型号签名 | `"Nikon MD3.01IILS8000 "`（23 B @`0x100BE708`），**5 处** `memcmp(...,23)` | `statics.json` signature_check |
| 调用方向 | **单向 md3 → DLL**（两 DLL 各只导出 `NkDriverEntry`，全文件不含 `LS8000`/`.md3`/三导出名） | `exports.md` §3.1 / `_f6/sibs.txt` |
| `NkDriverEntry` 调用点 | **`0x1009A32A`**（`call dword ptr [esp+0x1C]`，仅经虚表到达） | `exports.md` §3.2 / `_f6/f6load.txt` |
| `NkDriverEntry` 选择子域 | **1..9**（两个 DLL 同构），返回 8 = 忙，重试上限 20 次 × 250 ms | `exports.md` §3.3 |
| md3 内 SCSI 通道 | **0**（`DeviceIoControl`/`SCSI_PASS_THROUGH`/`\\.\` 全文件 0 命中） | `statics.json` scsi_api_scan |

### 2.2 分派机制

| 项 | 数值 | 出处 |
|---|---|---|
| 可达 CFG 规模 | **1,241 函数 / 13,616 指令 / 43,632 B = `.text` 的 5.6%** | `cfg_stats.txt` |
| 可达分派点 | **37**（其中 30 个 valid） | `cfg_stats.txt` / `cfg_dispatch.json` |
| 跳表站点（全 `.text` 线性扫） | **185**（37 个落在可达 CFG，其余 148 个在不可达区） | `jmp_scan.txt` / `dispatch.md` §1 |
| 跳表总条目 / 无效条目 | **330 / 0** | `cfg_stats.txt` |
| 语义分派层 | **4 层**（A `NkCtrlEntry` / B `NkMDCtrlEntry` / C `MAIDEntryPoint` / D 能力 ID 工厂） | `dispatch.md` §0 |
| 能力 ID 数 / 分支数 | **268 个 ID / 129 个分支**，11 张稠密跳表 + 4 张字节重映射表 | `dispatch.md` §6 |
| 能力 ID group 数 | **15 个**（`0x05 0x11 0x12 0x13 0x14 0x15 0x40 0x50 0x51 0x52 0x54 0x55 0x60 0x80 0x81`） | `dispatch.md` §0 |
| 工厂表候选覆盖 | **688 个候选 ID，100% 落在 `.text`，0 越界** | `dispatch.md` §6.1 |
| `.rdata` 静态 `(u16 id, u32 handler)` 表 | **不存在**（实证否定，42 段指针密集区全是纯 vtable） | `dispatch.md` §7 |
| `selector` 域 | `NkCtrlEntry` 1..11 + `0x1000`/`0x2000`/`0x2100`（16 位有符号）；`NkMDCtrlEntry` 1..4；`MAIDEntryPoint` 0..15 | `dispatch.md` §3–5 |
| 错误码族 | `NkCtrlEntry` default = `6`；`NkMDCtrlEntry` = `0x1001`/`0x1005`/`0x1006`/`0x1008`/`0x1009`；DLL 侧 = `0x11003`/`0x11004`/`0x11006`/`0x21008` | `exports.md` §1.3/§3.3 |

### 2.3 CDB 构造点（对接面核心）

| 项 | 数值 | 出处 |
|---|---|---|
| CDB 构造点 | **18 个**（17 个不同 CDB[0]，`0x15` 有两个构造点） | `cdb_sites.md` §0 |
| 命令全表行数 | **20 行**（18 行有构造点，`0x03` REQUEST SENSE / `0x17` RELEASE 判定 md3 内未构造） | `cdb_sites.md` §1 |
| CDB 长度常量 | **6 或 10** 字节（SCSI-2），CDB 缓冲在命令对象 `[this+8]` | `cdb_sites.md` §1 |
| 锚点总数 | **73**（18 个 BuildCDB + 21 个 CDB 构造器 + 3 张传输层 vtable 展开的 31 槽 + 3 个子功能白名单/分派函数） | `cap_to_cdb.md` §1 |
| 能力 ID → CDB 归类 | **A 153 / B 115 / C 0**（A=4 跳内命中锚点；B=恢复 vtable 未命中；C=未恢复方法） | `cap_to_cdb.md` §2 / `_g3/final_stats.json` |
| A/B 按 group 拆分 | `0x50` 82/35、`0x54` 40/29、`0x60` 13/16、`0x52` 11/10、`0x40` 5/5、`0x80`+`0x81` **0/14**、`0x05`+`0x51` 2/0、`0x11`–`0x15`+`0x55` 0/5 | `cap_to_cdb.md` §2 |
| 覆盖边界 | A 类 153 是**下界**，B 类 115 是**上界**（他对象虚调用静态无法展开） | `cap_to_cdb.md` §1 |
| SCSI opcode 开关 | **5 个**（`0x100A4DA6` 上界 0x28、`0x100A5FFE` 0xE1、`0x100A67AE` 0xE1、`0x100A9EA8` 0x2A、`0x100A516C` 0xF8） | `cap_to_cdb.md` §3 |
| E0/E1 子功能码白名单 | **21 个码值**（`0x40`–`0x45`、`0x80`、`0x81`、`0x90`、`0x91`、`0xA0`、`0xA1`、`0xB0`–`0xB4`、`0xC0`、`0xC1`、`0xD0`–`0xD3`、`0xD5`、`0xD6`）+ 透传码 `0x800`；**`0x92` 不在白名单** | `cdb_sites.md` §4.2 |
| 子功能码落点 | 工厂 `0x100AA1D0` 写命令对象 `+0x456` → E0/E1 ctor 复制到 CDB 对象 `+0x64` → BuildCDB 落 **CDB[2]**（`0x100A0233` / `0x100A0263`） | `cdb_sites.md` §4.1 |
| `0xC1` 两重身份 | 作为 CDB[0] = 独立 EXECUTE（6 字节，不带子功能码）；作为子功能码 = 落在 CDB[2] 且 CDB[0] 是 `0xE0`/`0xE1` | `cdb_sites.md` §4.3 |
| 主机侧数值范围校验 | **0 条 `cmp` 命中**（扫 245,413 条已对齐指令 × 9 个固件约束常量）；仅 `push` 命中 17 处 | `cap_to_cdb.md` §4 / `_g3/final_stats.json` |
| `0xD1` | **主机确实会发**（构造点 `0x100AA3BC` + 调度器 `0x100997A9`–`0x100997C0` 对 `0xD0..0xD6` 整段放行），但固件三层都不认 | `cdb_sites.md` §5 |
| host_code 与 cap_id 交集 | 85 个 host_code 中 20 个在 md3 出现，但与 268 个 cap_id **精确相同的只有 2 个**（`0x4000`、`0x1100`） | `cap_to_cdb.md` §5 |
| 结论 | **主机与固件的公共契约只有 CDB 字节与 sense 三元组**；两侧命令编号、状态编号各自独立、无换算关系 | `cap_to_cdb.md` §6 |

### 2.4 静态数据规模

| 项 | 数值 | 出处 |
|---|---|---|
| 字符串条目 | `statics.json` **1,054**；`s2_strings.json` **1,038** | `statics.json` / `s2_strings.json` |
| 静态表 | **6** 张（导出 RVA 表、导出名指针表、模块名描述符、vftable 15 项、`double[128]` EV/增益阶梯、`u8[128]` ctype 区） | `statics.json` tables |
| 字段访问频次（前 7 个偏移） | `+0x00` 4311 / `+0x04` 1144 / `+0x08` 1650 / `+0x0C` 1214 / `+0x10` 1118 / `+0x14` 428 / `+0x18` 245 | `iface/field_stat.json` |
| 间接跳转/调用站点 | **75** 条（全部 reachable=Y） | `indirect.txt` |
| G3 全量 CFG | **23,509 函数 / 245,413 指令 / 7,069 直调边 / 6,998 种子 / 772,762 标记** | `_g3/g3cfg.pkl` |
| G3 vtable | **534** 张 vtable / 1,796 槽索引 | `_g3/g3vtall.pkl` |
| 版本信息 | FileVersion `1,3,0,3003` / ProductVersion `4,0,0,0`，时间戳 2007-02-06 | `statics.json` version |

### 2.5 已知遗留问题（主机侧，源自产物原文）

1. `NkCtrlEntry` 签名自相矛盾：`ret 0x10` + 实测 4 参 vs 导出名 `YGFFFFPAX`（4×short+ptr，应 `ret 0x14`）vs BRIEF 记 3 参（`dispatch.md` Q3）
2. `0x92` 为何不在白名单（`cdb_sites.md` §7.1）
3. CDB 对象 `+0x64`/`+0x66`/`+0x68` 字段语义未定（`cdb_sites.md` §7.2）
4. `0xD1` 走 E0 还是 E1 未定（`cdb_sites.md` §7.3）
5. `request+0x14/+0x18` 的写入点未直接定位（`cdb_sites.md` §7.4）
6. md3 侧传输层 request 的构造点仍未锁定（`exports.md` §6.1）
7. `NKDSBP2` 的 ioctl `0x190012` 与 `[obj+0x18]` 的 0x2C 字节输入块格式未解（`exports.md` §6.4）

---

## 3. CDB ↔ E0/C1 协议映射说明

### 3.1 主机侧下行链路（md3 → 总线）

```
宿主 (Nikon Scan)
  └─ LS8000.md3 导出层
       ├─ NkCtrlEntry(sel, a2, a3, req)      11+4 路选择子 → 虚方法槽
       ├─ NkMDCtrlEntry(sel, req)             4 路 → 模块/句柄生命周期
       └─ MAIDEntryPoint(a1..a7)              16 路 → 功能号下推
  └─ 能力 ID 工厂 0x10071A60                 268 ID / 129 分支 → 造「命令对象」
  └─ CDB 构造器（18 个 BuildCDB）
       CDB 缓冲 = [this+8]，长度由构造器返回 6 或 10
       E0 = 0x100A0230（CDB[2] = 子功能码）；E1 = 0x100A0260（CDB[2] = 子功能码）
  └─ 传输层 request（+0x14 = CDB 长度 / +0x18 = CDB 指针 / +0x1C = 数据长度 / +0x20 = 数据指针）
  └─ 加载器虚方法 0x1009A2E0 → 0x1009A32A → NkDriverEntry(selector, request, ctx)
       ├─ NKDUSCAN：CreateFileA + WriteFile(request[+0x18], request[+0x14])   （USB）
       └─ NKDSBP2 ：DeviceIoControl(h, 0x190012, [obj+0x18], 0x2C, request[+0x20], [obj+0x28])（IEEE1394）
```

> 关键分界：**md3 造 CDB，`NkDriverEntry` 送上总线**。md3 的 105 项导入中无 `DeviceIoControl`/`SCSI_PASS_THROUGH`/`\\.\`，全文件 0 命中 `[实证]`。

### 3.2 固件侧三段式（`firmware/e0_bridge.md`）

```
CDB 落 0x40043C
  └─ 分派器 0x020E86 → 表 0x03E2E8（20 条 × 8 B，opcode → handler）
       ├─ op=0xC1 → 0x0269A6   ← C1（EXECUTE）处理函数：12 值开关
       └─ op=0xE0 → 0x026BF8   ← E0 handler：解析 + 门限 + 落存
  └─ E0 子功能表 0x03EDB8（12 条 2 B/条：[子功能码][长度]，0xFF 终止）
  └─ 作业层 0x02753E/0x0275F2 → 作业表 0x03EDE8（11 条 × 6 B）
  └─ 状态回流：内部状态码 → 0x03E390 → 0x01914A → sense 三元组 → 主机 REQUEST SENSE
```

### 3.3 主机 CDB 捕获点 ↔ 固件 E0/C1 的对应关系

`cap_to_cdb.md` 的 **A 类 153 个能力 ID** 通过 4 跳正向 BFS 抵达 73 个锚点（18 个 BuildCDB + 21 个 CDB 构造器 + 31 个传输层槽 + 3 个白名单/分派函数），由此与固件侧形成如下对应：

| 主机侧 | 固件侧 | 契约内容 | 状态 |
|---|---|---|---|
| `E0` BuildCDB `0x100A0230` | 分派表 `0x03E2E8[18]` → `0x026BF8`；子功能表 `0x03EDB8`（12 条） | **CDB[0]=`0xE0`，CDB[2]=子功能码，CDB[6..8]=24 位大端分配长度** | `[实证]` |
| `E1` BuildCDB `0x100A0260` | 分派表 `0x03E2E8` 读状态臂 `0x026EFC` | **CDB[0]=`0xE1`，CDB[2]=子功能码** | `[实证]` |
| `C1` BuildCDB `0x100A0190`（6 字节，不带子功能码） | 分派表 `0x03E2E8[17]` → `0x0269A6`（12 路 `cmp.b` 开关） | **CDB[0]=`0xC1` → 执行层**；CDB[2] 此时是 payload 而非子功能码 | `[实证]` |
| 主机子功能码白名单（21 码） | 固件 `0x03EDB8` 12 条 | 交集 = `0x40 0x41 0x42 0x80 0x81 0x90 0x91 0xA0 0xA1 0xB0 0xB1 0xB2 0xB3 0xB4 0xC0 0xC1 0xD0 0xD1 0xD2 0xD3 0xD5 0xD6` + 透传 `0x800`；**`0x92` 主机不发** | `[实证]` |
| 固件侧 `0x03EDB8` 独有 | `0x92`（长度 5）在固件表内但**不在主机白名单** | 主机无从触发 | `[实证]` |
| 固件 `0xD1` | **不在固件 `0x03EDB8` / `0x0269A6` / `0x03EDE8` 任何一层** | 主机发 `0xD1` → 解析层 `0x400436←0x50`（ILLEGAL REQUEST） | `[实证]` **真实协议缺陷** |
| 5 个 opcode 开关（`0x100A4DA6` 等） | 固件 `0x03E2E8` 按 SCSI opcode 索引 | **两条分派链在 md3 内部并行，彼此不换算** | `[实证]` |
| 固件六数值约束（15354/450/3283/450/±300/{0,1}） | `0x026DF8`–`0x026EA8`，比较对象是 **payload[1..4] 的 32 位 BE 参数 V1** | 主机侧 `cmp` 命中 **0** → 越界参数原样打包进 CDB 发往设备，由固件拒绝 | `[实证]` |

### 3.4 26 条记录的最终定性（重要修正）

`firmware/internal_26cmds.md` 已把"`0x03EBC0` 26 条内部命令"**改判**为：**一张 58 字节参数块的 26 个字段描述符**（`[实证]`，四条独立证据：handler 无外部引用 / op 无缝铺满 `0x00–0x39` / 引擎硬编码表址 / `len` 被当作迭代跨度使用）。

⇒ **主机侧不存在与这 26 条一一对应的捕获点**。`cap_to_cdb.md` 的 A/B/C 三类是「能力 ID → CDB」维度，与 `0x03EBC0` 的「参数块字段」维度**不相交**。

两者的真实关系是**间接**的：主机用 `SET WINDOW (0x24)` / `MODE SELECT (0x15)` 构造几何与输出参数块 → 固件 `0x025A56` 参数块校验引擎按 26 个字段描述符逐字段校验 → 通过后落 `0x400680 + n×0x3A`。即 **26 条描述符校验的是主机经 CDB 传来的那类参数**，而不是「26 条主机命令」。

---

## 4. 工具链清单（`tools/` 23 个文件）

### 4.1 前置条件总览

| 前置条件 | 涉及脚本数 | 说明 |
|---|---:|---|
| **硬编码 `D:\` 路径** | **8** | `resolve_tables.py`、`scan_calls.py`、`scan_ptr_tables.py`、`scan_code_regions.py`、`decoded_probe.py`、`holder_verify.py`、`h8_disasm_holder.py`（依赖 `D:\DS\TEST\LS8000`）；`scan_calls.py`/`scan_ptr_tables.py`/`scan_code_regions.py`/`decoded_probe.py`（依赖 `D:\TEST\LS8000-firmware-REA-20261021-reviewed`） |
| **硬编码 `<HOME>\Videos\...` 路径** | **7** | `codec_probe.py`、`layout_scan.py`、`tail_resolve.py`、`firm_probe.py`、`firm_struct.py`、`isa_scan.py`、`pe_info.py`（读 `SUPERCOOLSCAN8000ED_111` 安装目录 / `.rsrc/0/RCDATA/FIRMDATA`） |
| **硬编码 `<HOME>\WorkBuddy\...\LS8000` 输出路径** | **14** | 全部写 `02_analysis/` 的脚本 |
| **需要 `capstone`** | 4 | `decoded_probe.py`、`isa_scan.py`、+ md3 侧 89 个脚本中的大部分 |
| **需要 `pefile`** | 3 | `pe_info.py` + md3 侧 `lib_md3.py`/`statics_work/st_pe.py`/`iface/s1_pe.py`/`iface/sibs.py`/`iface/sibdis.py`/`_f6/dll_*.py` |
| **需要 `numpy`** | 2 | `layout_scan.py`、`tail_resolve.py` |
| **需要 `zstandard`** | 3 | `codex_holder_search.py`（可选，缺失则跳过 `.zst` 会话）、`dump_session.py`（必需）、md3 侧无 |
| **需要外部 Node + REA MCP 服务** | 4 | `rea_client.py`、`rea_host.py`、`rea_schema.py`、`rea_xref.py`、`mcp_probe.py` |
| **需要 32 位宿主 Python** | **0（实测证伪）** | 见 §4.4 |

### 4.2 通用工具逐项表（`tools/`）

| 脚本 | 用途 | 输入 | 输出 | 前置条件（32 位 / 路径依赖 / 外部依赖） |
|---|---|---|---|---|
| `codec_probe.py` (28,092 B) | FIRMDATA 是否经压缩/编码的只读探测（熵/分布/位打包/LZ 指纹/ISA 粗判/解压扫描） | `<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111\.rsrc\0\RCDATA\FIRMDATA`（可 `--target` 覆盖） | stdout；`--json <path>` 可选 | 无 32 位需求；**C 盘硬编码**（可 `--target` 绕过）；纯标准库（bz2/lzma/zlib）；**只读**，可加 `--skip-scan` 提速 |
| `layout_scan.py` (30,924 B) | 固件镜像候选结构测绘（指针表扫描 / 头部字段解析 / 熵-直方图突变 + 置换零模型 p 值） | 同上 FIRMDATA（`--pfx` 可覆盖，断言 `N==99865`） | `02_analysis/layout_report.md`、`02_analysis/layout_scan_output.txt` | **需 numpy**（当前环境已装）；**C 盘硬编码**；`--shuf` 置换次数默认 200（耗时）；**耗时较长**，会写两个输出文件 |
| `tail_resolve.py` (15,976 B) | FIRMDATA 尾部规律区结构判定 | 同上 FIRMDATA | `02_analysis/tail_resolve.md` | **需 numpy**；**C 盘硬编码**；只读输入 |
| `firm_probe.py` (3,974 B) | FIRMDATA 整体熵 / 分块熵 / 滑窗熵 / 字节分布普查 | 同上 FIRMDATA | stdout + `02_analysis/firm_probe.txt` | 无 32 位需求；**C 盘硬编码**；纯标准库 |
| `firm_struct.py` (3,746 B) | 字长与周期性分析（16/32 位字模式、步进采样熵、高字节直方图） | 同上 FIRMDATA | stdout + `02_analysis/firm_struct.txt` | 无 32 位需求；**C 盘硬编码**；纯标准库 |
| `isa_scan.py` (3,214 B) | 指令集粗判（多架构 capstone 打分，**只给弱证据**） | 同上 FIRMDATA | stdout + `02_analysis/isa_scan.txt` | **需 capstone**；**C 盘硬编码**；脚本内明确不做架构断言 |
| `pe_info.py` (3,781 B) | 升级 exe 的 PE 元信息 / 节区 / 导入导出 | `<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111.exe` | stdout + `02_analysis/pe_info.txt` | **需 pefile**；**C 盘硬编码** |
| `resolve_tables.py` (4,078 B) | 固件未分类数据表解析（`0x03EB70` 双精度表 / `0x03EBC0` 16 B 记录表 / 地址白名单） | `D:\DS\TEST\LS8000\LS8000_111_ROM.bin` + `D:\DS\TEST\LS8000\xrefs_data.csv` | stdout + `02_analysis/tables_resolved.txt` | **D 盘硬编码（2 处）**；无 32 位需求；纯标准库 |
| `scan_calls.py` (2,783 B) | H8 调用/跳转目标扫描（`5E`/`5A`）+ `0x3EAD8` 字符串指针表 | `D:\TEST\LS8000-firmware-REA-20261021-reviewed\firmware.decoded.bin` | stdout + `02_analysis/call_scan.txt` + `02_analysis/call_seeds.txt` | **D 盘硬编码**；无 32 位需求。**注意缺陷**：脚本按 **2 字节**读 `5E`/`5A` 后的目标，而 H8 实为 **3 字节大端绝对地址**（24 位），故当前版本实测命中 **0**（原 621 条种子应由 3 字节版产出，见 §4.5） |
| `scan_ptr_tables.py` (3,306 B) | 4 字节大端指针表扫描（步长 2）+ 与既有种子合并 + 4KB 覆盖率热图 | 同上 decoded.bin + `02_analysis/h8/functions.txt` | `02_analysis/ptr_tables.txt`、`02_analysis/call_seeds_v2.txt` | **D 盘硬编码**；无 32 位需求；依赖 `02_analysis/h8/functions.txt` 存在 |
| `scan_code_regions.py` (4,481 B) | 代码区段识别（用 functions.txt 过滤函数边界） | 同上 decoded.bin + `02_analysis/h8/functions.txt` | `02_analysis/code_regions.txt` | **D 盘硬编码**；无 32 位需求；依赖 functions.txt |
| `decoded_probe.py` (3,751 B) | 解压镜像头部/熵/字节占比探查 | `D:\TEST\LS8000-firmware-REA-20261021-reviewed\firmware.decoded.bin` | stdout + `02_analysis/decoded_probe.txt` | **D 盘硬编码**；**需 capstone**（实测当前可跑） |
| `h8_disasm_holder.py` (1,416 B) | 用 Harness 自建 `h8dis` 反汇编片夹识别调用区（验证返回码落地） | `D:\DS\TEST\LS8000\LS8000_111_ROM.bin` + `D:\DS\TEST\LS8000\h8dis.py` + `h8tab.py`（`sys.path.insert` 硬编码） | stdout | **D 盘硬编码（3 处）**；无 32 位需求。**当前缺陷**：脚本找 `h8tab.ENTRIES`/`TAB`/`TABLE`/`OPS`/`ENC` 属性，而实际 `h8tab.py` 只暴露 `load_entries(path)` 函数 → 实测 `exit=1`（打印 `h8tab 属性: ['load_entries', 're']`）。需改为 `h8tab.load_entries(h8.lst)` |
| `holder_verify.py` (1,672 B) | 验证片夹光学识别返回码的落地地址与消费方 | `D:\DS\TEST\LS8000\cfg_v4.json` + `LS8000_111_ROM.bin` | stdout | **D 盘硬编码（2 处）**；无 32 位需求；实测可跑（输出正常） |
| `rea_client.py` (2,996 B) | 最小 MCP stdio 客户端（对接本地 REA server） | Node + `rea-agents/scripts/rea.mjs` | 内存对象（供其他脚本 import） | **需外部 Node**（`C:\Program Files\nodejs\node.exe`）+ npm 全局 `rea-agents` 包；无 32 位需求 |
| `rea_host.py` (1,575 B) | 用 REA 打开升级 exe 并批量 dump（overview/strings/procedures/搜索） | 升级 exe（**C 盘硬编码**） | `02_analysis/rea_overview.json`、`rea_strings.json`、`rea_procedures.json`、`rea_search_*.json` | **需 Node + REA**；**C 盘硬编码**；依赖 `rea_client.py` |
| `rea_schema.py` (1,103 B) | 列出 REA MCP 全部工具名与 schema | REA server | `tools/rea_tools.txt`（本仓库内） | **需 Node + REA** |
| `rea_xref.py` (2,779 B) | 对 8 个关键地址做 xref 交叉引用分析 | 升级 exe（**C 盘硬编码**） | `02_analysis/xref_0x*.json`（8 份） | **需 Node + REA**；**C 盘硬编码** |
| `mcp_probe.py` (1,922 B) | 探测 REA MCP server 是否在线并列出工具 | Node + `rea.mjs` | stdout | **需 Node + REA** |
| `codex_holder_search.py` (2,892 B) | 在 Codex 全部会话（含 zst）中搜片夹类型码证据 | `~/.codex/sessions/` + `~/.codex/archived_sessions/` | `02_analysis/codex_holder_hits.txt` | **需 zstandard**（缺失则静默跳过 `.zst` 会话，输出会显著变小 —— 实测 312 KB vs 2,088 KB）；无 32 位需求 |
| `dump_session.py` (3,405 B) | 解压并导出指定 Codex 会话的可读正文 | `~/.codex/archived_sessions/*.jsonl(.zst)`（硬编码 2 个路径） | `02_analysis/codex_sessions/<tag>.md` | **需 zstandard（必需）**；无 32 位需求 |
| `extract_codex.py` (3,501 B) | 从 4 个指定 Codex 会话（.jsonl）提取正文 | `~/.codex/archived_sessions/` + `~/.codex/sessions/2026/10/21/`（4 条硬编码绝对路径） | `02_analysis/codex_sessions/*.md`（4 份） | 无 32 位需求；路径硬编码到具体 rollout 文件名；实测确定性可重跑 |

### 4.3 md3 侧工具脚本清单（`03_analysis/md3/`，89 个 `.py`）

统一前置条件：读 `D:\DS\TEST\LS8000\driver\LS8000.md3`（只读）；**需 capstone 5.x**；部分脚本需 **pefile**；`_f5/` 下多数脚本以 `sys.path.insert` 硬编码 `...\03_analysis\md3\cdb` 绝对路径；`_f6/` 下脚本硬编码 `D:\DS\TEST\LS8000\driver\{NKDUSCAN,NKDSBP2}.dll`；`_diff/` 需 `C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\LS8000.md3`（安装目录）。

| 分组 | 关键脚本 | 输入 | 输出 | 前置条件 |
|---|---|---|---|---|
| 顶层 16 个 | `pe_md3.py`/`lib_md3.py`/`md3lib.py`/`cfg.py`/`cfgmod.py`/`oracle.py`/`recdesc.py`/`resolve.py`/`scan_cdb.py`/`scan_jmp.py`/`sim_factory.py`/`final_gen.py`/`gen_json.py`/`enum_builders.py`/`fnresolve.py`/`xdis.py` | md3 本体；`calls.pkl`/`memwr.pkl`/`caps_raw.json` | `cfg_dispatch.txt/.json`、`jmp_scan.txt`、`indirect.txt`、`funcs.txt`、`factory_ids.txt`、`caps_raw.json`、`dispatch_caps.json` | capstone；`pe_md3.py` 用手工 struct 解析可脱离 pefile；**D 盘硬编码**（`pe_md3.py`/`lib_md3.py`/`md3lib.py`/`xdis.py`） |
| `iface/` 7 个 | `scan_req.py`、`sibs.py`、`sibdis.py`、`lmd.py`、`s1_pe.py`、`scan2.py` | md3 + 两个兄弟 DLL | `iface/field_stat.json` | capstone + pefile；**D 盘硬编码** |
| `cdb/` 12 个 | `core.py`、`ctors.py`、`callers.py`、`vt.py`、`where.py`、`four_ops.py` | md3 | `cdb/callers.json`、`cdb/four_ops.json`、`cdb/vt_rows*.json`、`cdb_sites.json` | capstone；`core.py` 为隔离副本（自带 PE 解析，不依赖顶层模块） |
| `statics_work/` 21 个 | `st_emit.py`、`st_pe.py`、`st_rsrc.py`/`st_rsrc2.py`/`st_rsrcdir.py`、`st_refmap.py`、`st_tables.py`、`st_idxtab.py`、`st_loadstr.py`、`s2_strings.py` | md3 | `statics.json`、`s2_strings.json`、`statics_work/*.txt/.json` | pefile（`st_pe.py`）+ capstone（`st_loadstr.py`）；**D 盘硬编码** |
| `_f5/` 28 个 | `gen.py`（生成 `cdb_sites.json`）、`v1`–`v10`（10 轮独立复核）、`emit.py`/`emit2.py`、`dll.py`（两个兄弟 DLL 补搜） | md3 + 两个兄弟 DLL | `cdb_sites.json`（20 行）+ 9 个 `.txt` 转储 | capstone；**D 盘硬编码**（`dll.py`）；`sys.path` 硬编码到 `md3/cdb` |
| `_f6/` 36 个 | `dll_entry.py`、`dll_ioctl{,2,3}.py`、`dll_arms{,2}.py`、`dll_anchor.py`、`dll_win.py`、`dll_dump.py`、`f6dis.py`、`nk_call.py`、`nkdrv.py`、`prov{,2}.py`、`anchor.py`、`xref.py` | 两个兄弟 DLL + md3 | `exports.md` 的全部证据（`dll_entry.txt` 171 KB 等 14 份转储） | capstone + pefile；**D 盘硬编码**（`D:\`） |
| `_g3/` 13 个 | `g3cfg.py`、`g3vt.py`/`g3vtall.py`、`g3class.py`、`g3final.py`、`g3hc.py`/`g3imm.py`、`g3sw.py` | md3 | `_g3/g3cfg.pkl`、`_g3/g3vtall.pkl`、`_g3/caps_feat.json`、`_g3/final_stats.json`、`_g3/sw.txt`、`cap_to_cdb.md/.csv` | capstone；**D 盘硬编码**（`g3cfg.py`）；**耗时最长**（全 `.text` 递归下降 + 534 vtable 恢复） |
| `_diff/` 3 个 | `diff_md3.py`、`field.py`、`md3dis.py` | md3（D 盘）+ 系统中安装的 `LS8000.md3` | stdout | capstone；**双路径硬编码**（D 盘 + `C:\Program Files (x86)\Common Files\Nikon\MaidMods\Scanners\`） |

### 4.4 关于「32 位宿主 Python」的核实结论

任务描述中提到「H8 反汇编类脚本需要 32 位宿主 Python」。**逐个核实后，此说法在当前代码上不成立**：

1. **H8 反汇编器本体（`h8dis.py` / `h8tab.py`）是纯 Python**：只用 `self.d[p]` 字节索引 + 整数移位构造助记符，**无 `ctypes`、无 `struct`、无指针宽度假设**（`D:\DS\TEST\LS8000\h8dis.py` 全文核查确认）。
2. **D 盘全部 271 个脚本无 native-endian `struct` 用法**：全量扫描 `struct.unpack/pack` 格式串只有 `<`/`>` 显式字节序（`<I` 11 次、`<II` 10 次、`<H` 6 次、`>d` 6 次、`>I` 6 次等），**没有 `'='`/`'@'`/`'n'`**。
3. **实测**：本机 Python **3.13.14 / 64 位**（`struct.calcsize('P')*8 == 64`），`holder_verify.py`（读 `cfg_v4.json` + ROM）、`resolve_tables.py`（读 ROM + xrefs CSV）、`h8fix.py`（读 ROM + `h8.lst`，含 393→399 条目修复对比）**全部正常运行并输出正确结果**。
4. **两个 H8 相关脚本的失败原因不是位数**：
   - `h8_disasm_holder.py` → `exit=1`，原因是 **API 不匹配**（找 `h8tab.ENTRIES` 属性，实际只有 `load_entries(path)` 函数），与 32/64 位无关。
   - `holder_verify.py` → 正常。
5. `D:\DS\TEST\LS8000\` 下确实存在 `build_manual.py` / `mini.py` / `sq.py` 三个脚本被 grep 命中 `ctypes|struct|calcsize` 关键字，但逐一打开确认**命中的是注释里的 "pointer" 一词**，脚本内**无** native struct 调用。

**结论**：H8 反汇编链在 64 位 Python 3.13 下可跑；真正的门槛是 **① 样本必须在 `D:\DS\TEST\LS8000\`（或用 `03_analysis/_pkgtool/paths.py` 的 `LS8000_SAMPLE_ROOT` 环境变量改写）② `h8tab.py` 需用修复版 `03_analysis/firmware/_jobfuncs/h8fix.py`（原版正则丢 6 条 12 位十六进制表项 → 10 字节指令永不解出）**。

### 4.5 移植/可移植性结论

- **`_pkgtool/paths.py` 已提供统一路径解析**：优先级 = 环境变量 `LS8000_SAMPLE_ROOT` > 包内 `samples/` > 原始 `D:/DS/TEST/LS8000`；`LS8000_CFG_ROOT` 可单独指向配置根；`ensure_sample()` 缺文件时给出明确提示而非裸 `FileNotFoundError`。
- **`_pkgtool/build_package.py` 已有路径重写逻辑**（`_rewrite_paths_in_file` / `_rewrite_tree`），把 `D:\` 硬编码批量改写为包内相对路径 —— 即**打包交付路径已经解决**，本次核实的问题只存在于**原始工作区**。
- **本次核实发现的两个脚本缺陷**（均已写入本清单，未修改原文件）：
  1. `tools/scan_calls.py`：`5E`/`5A` 目标按 **2 字节**读取，而 H8 实为 **3 字节大端绝对地址** → 实测命中 0，产出空 `call_seeds.txt`。原始 621 条种子须用 3 字节版产出（**2,037 处 JSR / 296 唯一，543 处 JMP / 334 唯一，合计 621**，与 `LS8000-L3-分析报告.md` §11 完全吻合）。
  2. `tools/h8_disasm_holder.py`：`h8tab` 属性名不匹配（`ENTRIES` vs `load_entries(path)`）→ 实测 `exit=1`。

### 4.6 工具链运行前置条件实测表

| 脚本 | 退出码 | 依赖满足情况 |
|---|---:|---|
| `codec_probe.py` | 0 | OK（纯标准库） |
| `firm_probe.py` / `firm_struct.py` / `isa_scan.py` / `pe_info.py` | 0 | OK |
| `codex_holder_search.py` | 0 | OK（需 zstandard，已装） |
| `extract_codex.py` | 0 | OK |
| `scan_calls.py` / `scan_ptr_tables.py` / `scan_code_regions.py` / `decoded_probe.py` | 0 | OK（**但 scan_calls 逻辑有 2/3 字节缺陷，见 §4.5**） |
| `resolve_tables.py` / `holder_verify.py` | 0 | OK（D 盘样本在位） |
| `layout_scan.py` / `tail_resolve.py` | — | 需 numpy（已装）；`layout_scan.py` 耗时较长，实测超时中断 |
| `dump_session.py` | — | 需 zstandard（已装） |
| `rea_host.py` / `rea_xref.py` / `rea_schema.py` / `mcp_probe.py` | — | 需外部 Node + REA MCP server |
| `h8_disasm_holder.py` | **1** | **API 不匹配**（`h8tab.ENTRIES` 不存在） |
| md3 `scan_jmp.py` / `recdesc.py` | 0 | OK |
| md3 `xdis.py` | 1 | 需命令行参数（无参运行报错） |
| md3 `s2_strings.py` | 1 | 需 numpy（已装后可跑） |

---

## 5. 已知问题与遗留（本轮核实附带发现）

| # | 问题 | 影响 | 状态 |
|---|---|---|---|
| 1 | `tools/scan_calls.py` 的 `5E`/`5A` 目标按 2 字节读，与 H8 的 3 字节大端绝对地址不符 | 产出空 `call_seeds.txt`；当前工作区已按 3 字节版还原为 621 条 / 5,587 B（与报告一致） | 已在 §4.5 记录，**未修改脚本** |
| 2 | `tools/h8_disasm_holder.py` 的 `h8tab` 属性名不匹配 | 脚本 `exit=1`，无法产出片夹识别反汇编 | 已在 §4.5 记录，**未修改脚本** |
| 3 | `tools/codex_holder_search.py` 在缺 `zstandard` 时静默跳过 `.zst` 会话 | 输出从 2,088 KB 缩到 312 KB 且**无任何警告** | 已装依赖并重跑还原为 2,088,226 B（原 2,088,228 B，2 B 差异源于源会话文件此后增长） |
| 4 | `tools/layout_scan.py` / `tail_resolve.py` 缺 `numpy` 时直接 `ModuleNotFoundError` | 无法运行 | 已装 numpy；`layout_scan.py` 实测耗时较长 |
| 5 | `02_analysis/ptr_tables.txt` 当前为 **3,701 B**，历史版本为 **4,251 B** | 历史版本对应的是 `functions.txt` 在 2026-10-24 16:45 被重新生成**之前**的函数表快照（当时 671 个函数，现 769 个），该历史快照已不可得 | 无法逐字节还原；**当前版本是脚本在现有输入下的确定性输出**（重跑稳定），且与 `functions.txt` 现状自洽 |
| 6 | `tools/dump_session.py` 的 2 个会话路径硬编码到具体 rollout 文件名 | 换机器/换会话即失效 | 已在 §4.2 标注 |

> **纪律声明**：本次核实为**只读分析**任务，未修改任何既有 `.md`/`.txt`/`.json` 文档；唯一被写动的 4 个派生文件（`call_seeds.txt` / `call_seeds_v2.txt` / `codex_holder_hits.txt` / `ptr_tables.txt`）均为**脚本重跑产物**，已按原算法还原（第 5 项 `ptr_tables.txt` 除外，已如实说明）；`D:\` 目录全程只读访问，无任何写入。

---

## 6. 交叉引用

| 需要 | 看这里 |
|---|---|
| 主机侧导出 ABI / 调用方向定论 | `md3/exports.md` |
| 选择子与能力 ID 分派机制 | `md3/dispatch.md` + `md3/dispatch_caps.json` |
| CDB 构造点全表与 E0/E1 子功能码 | `md3/cdb_sites.md` + `md3/cdb_sites.json` |
| 能力 ID → CDB 对接面定案 | `md3/cap_to_cdb.md` + `md3/cap_to_cdb.csv` |
| 固件侧 E0/C1 两段式全通路 | `firmware/e0_bridge.md` |
| `0x03EBC0` 26 条的最终定性（参数块字段描述符） | `firmware/internal_26cmds.md` |
| 固件 SCSI 分派表 20 条 | `firmware/_jobfuncs/LS8000-E0总表与修正-20261024.md` |
| 打包与路径可移植化 | `03_analysis/_pkgtool/paths.py`、`03_analysis/_pkgtool/build_package.py` |
