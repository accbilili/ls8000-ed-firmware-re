# samples/ 目录说明与来源证明

## 一句话结论

**本目录的固件镜像来自 Nikon 官方公开发布的固件更新软件包**——即尼康自己提供给用户、
用于升级 SUPER COOLSCAN 8000 ED 扫描仪固件的那份安装程序。

这不是推测。本文件给出**三层可独立复现的验证**，任何人都不必信任提交者的陈述，
照着跑一遍即可自行确认。

The firmware images here come from Nikon's own publicly distributed firmware update package —
the very installer Nikon supplied to customers for upgrading the SUPER COOLSCAN 8000 ED scanner.
This is verifiable in three independent ways, documented below.

---

## 一、官方发布包原件（`official_package/`）

本目录原样收录了官方软件包的三件内容，**逐字节未经改动**：

| 文件 | 大小 | 说明 |
|---|---:|---|
| `SUPERCOOLSCAN8000ED_111.exe` | 196,608 B | 固件更新程序本体 |
| `ReadMe.txt` | 2,389 B | 官方说明文件，日期 2002-12-26 |
| `LS8000fw111.pdf` | 47,659 B | 官方更新操作手册 |

### 官方 ReadMe.txt 原文摘录（决定性的自证）

```
Nikon Firmware Update Software
...
1. Contents of This Software Package
   This Software package contains the following files:
   - Readme file (this file)
   - Firmware update software manual
   - Update software (executable file)
     SUPERCOOLSCAN8000ED_111.exe
     (update software for SUPER COOLSCAN 8000 ED film scanners)
...
3. Firmware Version Information
   Running the update software provided on this CD will update scanner
   firmware to the following version:
   - SUPER COOLSCAN 8000 ED: Ver. 1.11

26/12/2002
```

版本号链条完全自洽：
**文件名 `_111`** ↔ **ReadMe 中的 Ver. 1.11** ↔ **ROM 文件名中的 `111`**。

---

## 二、三层可复现验证

### 第 1 层：官方安装程序与仓库内二进制是同一份文件 ✅

```bash
sha256sum samples/official_package/SUPERCOOLSCAN8000ED_111.exe
```

```
16932eda980c865ddf602e571bce72c0ab7ce7faebe8cf1b046d13be10c3c9d4
```

该哈希同时是此前工作区中 `updater.exe` 的哈希——**两者为同一文件**，
仓库中已改为使用官方原始文件名，避免"匿名副本"造成来源不明。

### 第 2 层：固件资源完整嵌在官方程序内 ✅

```bash
python - <<'PY'
up = open('samples/official_package/SUPERCOOLSCAN8000ED_111.exe','rb').read()
fd = open('samples/FIRMDATA.bin','rb').read()
print('FIRMDATA 在 updater 中的偏移:', hex(up.find(fd)))
PY
```

实测输出 `0x17588`。`FIRMDATA.bin` 的全部字节可在官方安装程序中逐字节找到，
说明它是该程序内嵌的**未经改动的 RCDATA 资源**，而非外部或来源不明的镜像。

中部 4 KB 片段与头部 512 B 亦分别命中（`0x23894`、`0x17588`），互为交叉印证。

### 第 3 层：ROM 是该资源的解压产物（强支持）

信息熵可区分"明文固件"与"压缩数据"：

| 文件 | 前 64 KB 信息熵 | 判读 |
|---|---:|---|
| `LS8000_111_ROM.bin` | **5.493** | 典型 H8 机器码分布（明文固件） |
| `FIRMDATA.bin` | **7.648** | 接近满熵 8.0，符合压缩/打包数据 |
| `SUPERCOOLSCAN8000ED_111.exe` | 5.379 | 典型 PE 可执行文件 |

差异与"资源在包内压缩存放、解压后得到 228 KB 明文 ROM"完全一致。

> 诚实标注：本仓库尚未提供一键解压脚本来完整复原该过程（需确定压缩参数），
> 故表述为"强支持"而非"已完整复原"。**欢迎跑通者提交 PR 补足第 3 层。**

---

## 三、目录内容

| 类别 | 文件 | 大小 |
|---|---|---:|
| **LS-8000 ED 固件 ROM** | `LS8000_111_ROM.bin` | 228,345 B |
| 同上（历史命名，同哈希） | `decoded.bin` | 228,345 B |
| 引导块 | `LS8000_bootblock.bin` | 65,536 B |
| 整机 512 KB 全镜像 | `LS8000_full_512K.bin` | 524,288 B |
| updater 内嵌固件资源 | `FIRMDATA.bin` | 99,865 B |
| 官方发布包原件 | `official_package/` | 3 件，246,656 B |
| 主机侧驱动/程序 | `driver/`（6 件） | 约 2.2 MB |
| 其它机型与更新工具 | `other/`（13 件） | 约 2.4 MB |

---

## 四、指纹对照

与仓库根目录 `samples_manifest.txt` 登记的 14 条记录一致，
用于确认你持有的版本与本项目分析所依据的版本相同：

```
fd1f17c594490ad0034ff2b80d4c8eaf1eb93721eaff1a5131e87faca358be85  LS8000_111_ROM.bin   (228345)
2117e671e394bfb5bf407988bb6d28064fd48807580f04bccb4468bdc7790a72  LS8000_bootblock.bin (65536)
015b512723d52c8e8cf89c50fb1de7179c64f8b0edcd57526b12faf002320bc8  LS8000_full_512K.bin (524288)
65e2559e795fc2392a107b5a235b6235d64aac819c3dcfee7ea08b8e201a3563  FIRMDATA.bin         (99865)
16932eda980c865ddf602e571bce72c0ab7ce7faebe8cf1b046d13be10c3c9d4  SUPERCOOLSCAN8000ED_111.exe (196608)
```

**样本间关系（已实测）**

- `LS8000_full_512K.bin[0x00000:0x10000]` == `LS8000_bootblock.bin`（逐字节全等）
- `LS8000_full_512K.bin[0x10000:0x10000+228345]` == `LS8000_111_ROM.bin`（逐字节全等）
- `decoded.bin` 与 `LS8000_111_ROM.bin` 同哈希（历史遗留命名，非独立样本）

---

## 五、为什么要原样收录官方安装包？

在固件逆向领域，**样本来源的可验证性**决定结论的可信度：

1. 证明分析对象是**官方公开发行版本**，而非泄露、内部构建或被篡改的副本
2. 第三方可独立核实持有的是否为同一镜像
3. 完整证据链可供任何人重新审视
4. 便于后续研究者对照 Ver. 1.11 与其它版本做差异分析

---

## 六、许可状态与字节完整性

`samples/` 下的二进制**不属于**本仓库 GPL-3.0 / CC BY-SA 4.0 的授权范围，
著作权归 Nikon Corporation 所有。本仓库仅作为技术研究对象收录，不主张任何权利。

字节完整性保障：

- `.gitattributes` 设置 `* -text`，**全局禁用 Git 的行尾转换**
- `.md3`、`.dll`、`.exe`、`.bin`、`.pdf` 均标记为 `binary`
- 因此 `git clone` 得到的副本与源文件**逐字节一致**
- 可用 `python tools/verify_package.py` 一键验证（MANIFEST.txt 记录每个文件的 SHA256）

*又一次说明：新增或改动任何文件后，必须先重生成 MANIFEST.txt 再提交，否则哈希将不符。*

详见仓库根目录的 [`NOTICE`](../NOTICE) 与 [`DISCLAIMER.md`](../DISCLAIMER.md)。
