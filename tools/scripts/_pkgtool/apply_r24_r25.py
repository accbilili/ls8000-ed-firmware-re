"""
LS8000 —— R25 回滚 + R24 METHOD 术语修正（打包阶段收尾，一次性执行）

本脚本做两批精准文本替换：

【批次 A：R25 —— 回滚 R22/R23 的公式部分】
  起因：上一轮（打包阶段）人工推导 H8 位段时犯了两处错
        ① `4 × shll.l #2` 是左移 8 位（每次 2 位），误判为 16 位
        ② payload 索引偏移 —— `er6` 指向 CDB 基址，`@(0x2,er6)` 是 payload[2]
  现由指令级模拟器实跑证伪（`sim_verify_formulas.py`）：
        er3      = BE32(payload[1..4])     实测 0x11223344
        0x400408 = BE32(payload[2..5])     实测 0x22334455
        0x40040C = (P7<<16)+(P8<<8)+P9     实测 0x00778899
  ⇒ 「V1 = payload[1..4]（32 位 BE）」本来是对的，R22/R23 的公式部分撤销。
  ⇒ 但 R22/R23 里的两条仍然成立，予以保留：
        · 「六数值」实为按子功能号分派的校验表（12 分支）
        · 0x400408 第 4 写入点 0x028D96 机制不同 ⇒ 该槽位被多处复用

【批次 B：R24 —— METHOD 术语修正】
  `0x190012` = CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)
  三方说法各自的错法不同；驱动侧实证（MDL + MmMapLockedPages 直写、
  Irp->UserBuffer 访问 0 次）排除 NEITHER；5 个码里只有 0x19001C 是 BUFFERED。
  ⚠ 「数据出现在输出缓冲」这个**实测现象不变**，只改机制归因的措辞。

用法
----
    python apply_r24_r25.py
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BAK = os.path.join(ROOT, '03_analysis', '_pkgtool', '_backup_preR25')


def _backup(rel):
    s = os.path.join(ROOT, rel.replace('/', os.sep))
    if not os.path.isfile(s):
        return False
    os.makedirs(BAK, exist_ok=True)
    d = os.path.join(BAK, os.path.basename(rel))
    shutil.copy2(s, d)
    return True


# ======================= 批次 A：R25 回滚 =======================

FIX_A = [
    # ---- 主报告 §3「校验对象」段 ----
    ('REPORT_全面分析总结-20261024.md', [
        ('**校验对象 = `er3`，由 payload[1..8] 经「重排 + 相加」拼成的 32 位模式**'
         '（位段：bit23-16 ← P2+P6，bit15-8 ← P1+P5，bit7-0 ← P3+P4+P7+P8）；'
         '**不是** `payload[1..4]` 的 32 位大端：',
         '**校验对象 = `er3` = 32 位大端参数 V1 = `payload[1..4]`**'
         '（`payload[1]<<24 | payload[2]<<16 | payload[3]<<8 | payload[4]`）'
         '〔R25：模拟器实跑确认〕：'),
        ('> **打包阶段实测更正（R22）**：`er3` 的真实装载链在 `0x026D10`–`0x026D74`，'
         '且 `0x026DAE` 起是**按子功能号（CDB[2]）分派的校验表**'
         '（12 分支、6 个校验值、其中 `0x80`/`0x81`/`0xB0`/`0xD0` 完全不校验）。'
         '证据与复现命令见 `03_analysis/firmware/E0子功能分派与校验表-实测补全.md`。',
         '> **打包阶段实测补全（R22 保留部分）**：`0x026DAE` 起是'
         '**按子功能号（CDB[2]）分派的校验表**'
         '（12 分支、6 个校验值、其中 `0x80`/`0x81`/`0xB0`/`0xD0` **完全不校验**）。'
         '这条**不依赖**公式口径，独立成立。'
         '证据与复现命令见 `03_analysis/firmware/E0子功能分派与校验表-实测补全.md`。'),
    ]),

    # ---- 回写总账：撤销 R22/R23，追加 R25 ----
    ('REPORT_回写总账-20261024.md', [
        ('| **R22** | REPORT §3「六数值」、`交叉结论` §4/§7、`agent_15354` §3 | '
         '校验对象 = **V1 = `payload[1..4]`（32 位 BE）**；'
         '「六数值门限依次校验同一个 V1」 | **两条均被证伪**：'
         '① `er3` 实为 **payload[1..8] 经「重排 + 相加」拼成的 32 位模式**'
         '（bit23-16 ← P2+P6；bit15-8 ← P1+P5；bit7-0 ← P3+P4+P7+P8）；'
         '② `0x026DAE` 起是**按子功能号（CDB[2]）分派的校验表**——**12 个分支**、'
         '6 个校验值（15354/450/3283/450/±300/{0,1}）、'
         '其中 `0x80`/`0x81`/`0xB0`/`0xD0` **完全不校验**；'
         '③ payload 基址是 **`er5`**（`@/0x1,er5` 起），`er4` 读的是 CDB[2] | '
         '`0x026D10`–`0x026D74`（`er3` 装载链）+ `0x026DAE`–`0x026DF4`（分派表）；'
         '证据文档 `03_analysis/firmware/E0子功能分派与校验表-实测补全.md` |',
         '| **R22**（已撤销，见 R25） | REPORT §3「六数值」、`交叉结论` §4/§7、`agent_15354` §3 | '
         '（原 R22 主张 `er3` 是 payload[1..8] 重排相加 —— **该公式部分已由 R25 撤销**） | '
         '**仅保留一条仍然成立**：`0x026DAE` 起是**按子功能号（CDB[2]）分派的校验表**'
         '——**12 个分支**、6 个校验值（15354/450/3283/450/±300/{0,1}）、'
         '其中 `0x80`/`0x81`/`0xB0`/`0xD0` **完全不校验**。'
         '（payload 基址是 `er5`=`sp+1` 暂存区、`er4` 读 CDB[2]，此说亦成立） | '
         '`0x026DAE`–`0x026DF4`（分派表）；证据文档 '
         '`03_analysis/firmware/E0子功能分派与校验表-实测补全.md` |'),

        ('| **R23** | REPORT §3/§4、`agent_b3` §2.8（标为「实证」） | '
         '`0x400408` = `BE32(V1)`（`P1<<24+P2<<16+P3<<8+P4`）／'
         '`P1<<24+(P2+P3)<<16+P4` | **两条均被证伪**：实测 **C1 臂 `0x026A86`、'
         'A0 臂 `0x026AC4`、B3 臂 `0x026B46` 三写入点同构**，公式 = '
         '**`(P2<<8)+(P3<<8)+(P4<<16)+P5`**，**P1 不参与**（B3 臂把 P1 单独写入 `0x400412`）；'
         '另第 4 写入点 `0x028D96`（片夹识别区）机制完全不同'
         '（`[0x4204E8]>>1 + [0x420308]`，与 payload 无关）⇒ `0x400408` 是'
         '**被多处复用的暂存槽位**，非单一字段 | 同上；`agent_b3` 的「实证」标注与指令不符 |',
         '| **R23**（已撤销，见 R25） | REPORT §3/§4、`agent_b3` §2.8 | '
         '（原 R23 主张 `0x400408` = `(P2<<8)+(P3<<8)+(P4<<16)+P5` —— '
         '**该公式部分已由 R25 撤销**） | '
         '**仅保留一条仍然成立**：第 4 写入点 `0x028D96`（片夹识别区）机制完全不同'
         '（`[0x4204E8]>>1 + [0x420308]`，与 payload 无关）⇒ `0x400408` 是'
         '**被多处复用的暂存槽位**，非单一字段。'
         '（`agent_b3` §2.8 的「`<<16` 怪癖」不成立 —— 根因见 R25） | '
         '`0x028D80`–`0x028D96`；模拟器见 R25 |'),

        # 追加 R25
        ('| **R23**（已撤销，见 R25） | REPORT §3/§4、`agent_b3` §2.8 | '
         '（原 R23 主张 `0x400408` = `(P2<<8)+(P3<<8)+(P4<<16)+P5` —— '
         '**该公式部分已由 R25 撤销**） | '
         '**仅保留一条仍然成立**：第 4 写入点 `0x028D96`（片夹识别区）机制完全不同'
         '（`[0x4204E8]>>1 + [0x420308]`，与 payload 无关）⇒ `0x400408` 是'
         '**被多处复用的暂存槽位**，非单一字段。'
         '（`agent_b3` §2.8 的「`<<16` 怪癖」不成立 —— 根因见 R25） | '
         '`0x028D80`–`0x028D96`；模拟器见 R25 |',
         '| **R23**（已撤销，见 R25） | REPORT §3/§4、`agent_b3` §2.8 | '
         '（原 R23 主张 `0x400408` = `(P2<<8)+(P3<<8)+(P4<<16)+P5` —— '
         '**该公式部分已由 R25 撤销**） | '
         '**仅保留一条仍然成立**：第 4 写入点 `0x028D96`（片夹识别区）机制完全不同'
         '（`[0x4204E8]>>1 + [0x420308]`，与 payload 无关）⇒ `0x400408` 是'
         '**被多处复用的暂存槽位**，非单一字段。'
         '（`agent_b3` §2.8 的「`<<16` 怪癖」不成立 —— 根因见 R25） | '
         '`0x028D80`–`0x028D96`；模拟器见 R25 |\n'
         '| **R25** | R22/R23 的公式部分、`REPORT_全面分析总结` §3、'
         '`交叉结论` §4、`LS8000-E0总表` §3.1、`agent_15354` §3 | '
         '**R22/R23 主张的「重排相加」公式** | '
         '**撤销 R22/R23 的公式部分，恢复正确口径**：'
         '`er3` = **`BE32(payload[1..4])`**（`0x11223344`）、'
         '`0x400408` = **`BE32(payload[2..5])`**（`0x22334455`）、'
         '`0x40040C` = **`(P7<<16)+(P8<<8)+P9`**（`0x00778899`）。'
         '**根因**：人工推导 H8 位段时 ① 把 `4 × shll.l #2` 误判为左移 16 位'
         '（实为 **8** 位，每次 2 位）② 误判 payload 索引偏移'
         '（`er6`=CDB 基址，`@(0x2,er6)` 是 payload[2]）。'
         '**方法**：新建 H8 指令子集模拟器 `h8sim.py` + `sim_verify_formulas.py`，'
         '**实跑**固件指令序列反推公式。**教训：位段类结论必须用模拟执行验证，'
         '不能靠人工推导** | `03_analysis/_pkgtool/sim_verify_formulas.py`（实跑）；'
         '`03_analysis/status/VERDICT_0x400408.md`（独立裁决，结论一致） |'),
    ]),

    # ---- 交叉结论 ----
    ('03_analysis/firmware/_jobfuncs/交叉结论-给实机验证线-20261024.md', [
        ('**关键点（纠正一个容易踩的坑）**：被比较的量 `er3` **不是 CDB 字节**，'
         '而是 **payload[1..8] 经「重排 + 相加」拼成的 32 位模式**'
         '（bit23-16 ← P2+P6，bit15-8 ← P1+P5，bit7-0 ← P3+P4+P7+P8）；'
         '**打包阶段实测更正**：不是 payload[1..4] 的 32 位大端 ——',
         '**关键点（纠正一个容易踩的坑）**：被比较的量 `er3` **不是 CDB 字节**，'
         '而是 **32 位大端参数 V1 = `payload[1..4]`**'
         '（`payload[1]<<24 | payload[2]<<16 | payload[3]<<8 | payload[4]`）'
         '〔R25：模拟器实跑确认；R22 的「重排相加」说已撤销〕——'),
        ('| 3 | 若要抓参数，抓 **data-out 缓冲**（不是 CDB） | 零 | '
         '`er3` 由 payload[1..8] 重排相加（R22 实测更正） |',
         '| 3 | 若要抓参数，抓 **data-out 缓冲**（不是 CDB） | 零 | '
         'V1 = `payload[1..4]`（32 位 BE，R25 实测确认） |'),
        ('| 数值门限对象不明 | **`er3` = payload[1..8] 重排相加**（R22 实测更正），在 data-out 里 |',
         '| 数值门限对象不明 | **`er3` = V1 = `payload[1..4]`**（32 位 BE，R25 实测确认），在 data-out 里 |'),
    ]),

    # ---- E0 总表 §3.1 ----
    ('03_analysis/firmware/_jobfuncs/LS8000-E0总表与修正-20261024.md', [
        ('### 3.1 校验对象 `er3`：payload[1..8] 重排相加，不是 CDB 字节 —— '
         '本条为自我修正（并经打包阶段实测再修正）',
         '### 3.1 校验对象 `er3` = 32 位大端参数 V1 = `payload[1..4]`，不是 CDB 字节 —— '
         '本条为自我修正〔R25：模拟器实跑确认〕'),
        ('> **⚠️ 打包阶段实测更正（R22）**：本节初版写的是\n'
         '> `er3 = payload[1]<<24 | payload[2]<<16 | payload[3]<<8 | payload[4]`（32 位大端 V1）。\n'
         '> **该式与指令不符**，已作废。逐条复核 `0x026D10`–`0x026D74` 得到的真实公式是\n'
         '> **8 个字节经「重排 + 相加」拼成的 32 位模式**：\n'
         '>\n'
         '> ```\n'
         '> er3 = (payload[1]<<8) + (payload[2]<<8) + (payload[3]<<16) + payload[4]\n'
         '>     + (payload[5]<<8) + (payload[6]<<8) + (payload[7]<<16) + payload[8]\n'
         '> ```\n'
         '>\n'
         '> 位段展开：\n'
         '>\n'
         '> | 位段 | 累加项 | 来源指令 |\n'
         '> |---|---|---|\n'
         '> | bit 31–24 | `0`（可接收下方进位） | — |\n'
         '> | bit 23–16 | `payload[2] + payload[6]` | `mov.b r0l,r0h` + `mov.w r0,e0`（P2）、'
         '`mov.w r1,e1`（P6） |\n'
         '> | bit 15–8 | `payload[1] + payload[5]` | `mov.b r3l,r3h` + `mov.w r3,e3`（P1）、'
         '`mov.b r0l,r0h` + `mov.w r0,e0`（P5） |\n'
         '> | bit 7–0 | `payload[3] + payload[4] + payload[7] + payload[8]` | '
         '`shll.l #2`×4（P3）、直加（P4）、`shll.l #2`×4（P7）、直加（P8） |\n'
         '>\n'
         '> 关键指令形态：`mov.b rXl,rXh` 把字节放到 rX 的**高字节**，'
         '`mov.w rX,eX` 又把 rX 写进 ERX 的\n'
         '> **高 16 位** —— 两次「抬高」使字节落在 bit8–15，而非直觉上的 bit16–23。\n',
         '> **📌 R25 更正记录**：本节初版写的是\n'
         '> `er3 = payload[1]<<24 | payload[2]<<16 | payload[3]<<8 | payload[4]`（32 位大端 V1）\n'
         '> —— 这**本来就是对的**。打包阶段我曾误把它改作「payload[1..8] 重排相加」，\n'
         '> 该错误更正已撤销。\n'
         '>\n'
         '> **误判根因（两处）**：\n'
         '> ① 把 `4 × shll.l #2` 当成左移 **16** 位 —— 实际每次移 **2** 位，4 次共 **8** 位；\n'
         '> ② 误判 payload 索引偏移 —— `er6` 指向 CDB 基址，`@(0x2,er6)` 对应 **payload[2]**。\n'
         '>\n'
         '> **正确口径由模拟器实跑给出**（`03_analysis/_pkgtool/sim_verify_formulas.py`）：\n'
         '> `er3 = BE32(payload[1..4])` = `0x11223344`（测试 payload `11 22 33 44 …`）。\n'
         '> **教训：位段类结论必须用模拟执行验证，不能靠人工推导。**\n'),

        ('⇒ 修正后的表述：**六个数值是「按子功能分派、对 payload 字节加权和模式做等值/区间/布尔判定」的门槛**，\n'
         '与 CDB 字节无关；`0x91/0x92` 的 `{0,1}` 是**布尔参数校验**，语义自洽。',
         '⇒ 修正后的表述：**六个数值是「按子功能分派、对 32 位大端参数 V1 做等值/区间/布尔判定」的门槛**，\n'
         '与 CDB 字节无关；`0x91/0x92` 的 `{0,1}` 是**布尔参数校验**，语义自洽。'),

        ('| `0xB3` | `0x02BBAE` | **持久设置写 + 机构重定位**：组装 33 B 参数块@`0x400CA0` → '
         '擦写引导块 flash `0x6000-0x7FFF` → 回读校验 → 电机移至 **位置值+333**'
         '（位置值 = `0x400408` 槽位内容，区间 33…633，无效退化 333）'
         '⚠️ **R23 更正**：该槽位由 `(P2<<8)+(P3<<8)+(P4<<16)+P5` 拼成，**P1 不参与**，'
         '故不再称「payload 首 32 位大端」 | — | `[实证]` |',
         '| `0xB3` | `0x02BBAE` | **持久设置写 + 机构重定位**：组装 33 B 参数块@`0x400CA0` → '
         '擦写引导块 flash `0x6000-0x7FFF` → 回读校验 → 电机移至 **V1+333**'
         '（V1 = `payload[1..4]` 的 32 位大端有符号位置偏移，区间 33…633，无效退化 333）'
         '〔R25：模拟器实跑确认 `0x400408` = `BE32(payload[2..5])`，'
         '`agent_b3` §2.8 的「`<<16` 怪癖」不成立〕 | — | `[实证]` |'),
    ]),

    # ---- agent_15354 §3 ----
    ('03_analysis/firmware/_jobfuncs/agent_15354/agent_15354_report.md', [
        ('> **⚠️ 打包阶段实测更正（R22）**：上式**不成立**。根因是把 `er5` 误当成 CDB 基址 ——\n'
         '> 实际序言是 `0x026C0C mov.l #0x00000001, er5` / `0x026C12 add.l sp, er5`\n'
         '> ⇒ **`er5 = sp+1`，是 data-out 相位 payload 的暂存区**；CDB 基址是 `er4`（`0x40043C`）。\n'
         '> 逐条复核 `0x026D10`–`0x026D74` 得到的真实公式是\n'
         '> **8 个 payload 字节经「重排 + 相加」拼成的 32 位模式**：\n'
         '>\n'
         '> ```\n'
         '> er3 = (payload[1]<<8) + (payload[2]<<8) + (payload[3]<<16) + payload[4]\n'
         '>     + (payload[5]<<8) + (payload[6]<<8) + (payload[7]<<16) + payload[8]\n'
         '> ```\n'
         '>\n'
         '> 位段：bit23-16 ← `P2+P6`；bit15-8 ← `P1+P5`；bit7-0 ← `P3+P4+P7+P8`。\n'
         '> 故 §4.5 基于上式得出的「`0x91/0x92` 恒不可满足」结论**随之失效**，\n'
         '> 正确表述为「布尔参数校验」（`er3 ∈ {0,1}`，反解多解）。\n'
         '>\n'
         '> **本报告 §1 判决表与 §3 的「12 路 cmp.b 分派链」经打包阶段独立复核为正确**，\n'
         '> 被推翻的只有 `er3` 的装配公式。完整证据见\n'
         '> `03_analysis/firmware/E0子功能分派与校验表-实测补全.md`。',
         '> **📌 R25 更正记录**：上式（`er3` = CDB[1]·256 + 子功能号）**仍不成立** ——\n'
         '> 根因是把 `er5` 误当成 CDB 基址。实际序言是\n'
         '> `0x026C0C mov.l #0x00000001, er5` / `0x026C12 add.l sp, er5`\n'
         '> ⇒ **`er5 = sp+1`，是 data-out 相位 payload 的暂存区**；CDB 基址是 `er4`（`0x40043C`）。\n'
         '>\n'
         '> **正确的 `er3` 公式 = `BE32(payload[1..4])`**（32 位大端 V1），\n'
         '> 由指令级模拟器实跑确认（`03_analysis/_pkgtool/sim_verify_formulas.py`，\n'
         '> 测试 payload `11 22 33 44 …` → `er3 = 0x11223344`）。\n'
         '>\n'
         '> ⇒ §4.5 基于旧式得出的「`0x91/0x92` 恒不可满足」结论**仍然失效**，\n'
         '> 正确表述为「布尔参数校验」（`er3 ∈ {0,1}`）。\n'
         '>\n'
         '> **本报告 §1 判决表与 §3 的「12 路 cmp.b 分派链」经复核为正确。**\n'
         '> 完整证据见 `03_analysis/firmware/E0子功能分派与校验表-实测补全.md`。'),
    ]),
]

# ======================= 批次 B：R24 METHOD 术语 =======================

FIX_B = [
    ('REPORT_全面分析总结-20261024.md', [
        ('| ioctl | **`0x190012`** = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x012, '
         'METHOD_BUFFERED, FILE_ANY_ACCESS)`（驱动只认 5 个码：'
         '`0x190012/16/1A/1C/22`；`0x190004/8/14` 在驱动里 0 命中 ⇒ err=50 属预期） |',
         '| ioctl | **`0x190012`** = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, '
         'METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`〔R24：驱动侧实测更正〕'
         '（驱动只认 5 个码：`0x190012/16/1A/1C/22`；'
         '`0x190004/8/14` 在驱动里 0 命中 ⇒ err=50 属预期；'
         '其中**只有 `0x19001C` 是 METHOD_BUFFERED**） |'),
        ('**★ 前序 2340 组扫描全军覆没的真因**：**SCSI 数据落在 METHOD_BUFFERED 的'
         '「输出缓冲」（`bytesRet` = 数据长度），不在用户态 DataBuffer**——之前一直在读错的地方。',
         '**★ 前序 2340 组扫描全军覆没的真因**：**SCSI 数据出现在「输出缓冲」**'
         '（`bytesRet` = 数据长度），不在用户态 DataBuffer —— 之前一直在读错的地方。'
         '〔R24〕**机制解释更精确**：该码是 **METHOD_OUT_DIRECT** 语义，'
         '`lpOutBuffer` 就是用户缓冲本身、I/O Manager **不做代拷贝**，'
         '驱动直接写用户页；且**32 位调用者必须在结构体里传入有效指针**'
         '（64 位进程的用户态指针普遍 > 4 GB，不被接受）。'
         '**实测现象本身不变。**'),
    ]),

    ('REPORT_回写总账-20261024.md', [
        ('| D5 | **前序 2340 组暴力扫描失败的真因**：SCSI 数据落在 **METHOD_BUFFERED 的输出缓冲**'
         '（`bytesRet`=长度），不在用户态 DataBuffer | ✅ |',
         '| D5 | **前序 2340 组暴力扫描失败的真因**：SCSI 数据出现在**输出缓冲**'
         '（`bytesRet`=长度），不在用户态 DataBuffer。'
         '〔R24〕机制解释更精确：控制码为 **METHOD_OUT_DIRECT**（`lpOutBuffer` 即用户缓冲、'
         'I/O Manager 不代拷贝），且 32 位调用者须传入有效指针。**实测现象不变。** | ✅ |'),
    ]),

    ('03_analysis/firmware/_jobfuncs/交叉结论-给实机验证线-20261024.md', [
        ('> METHOD_BUFFERED 的输出缓冲，不在用户 DataBuffer**',
         '> 输出缓冲，不在用户 DataBuffer**〔R24：机制为 METHOD_OUT_DIRECT，现象不变〕'),
    ]),

    ('REPORT_实机验证交接.md', [
        ('**`0x190012` = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, '
         'METHOD_BUFFERED, FILE_ANY_ACCESS)`，输入结构 44 字节（`SCSI_PASS_THROUGH` 布局）。**',
         '**`0x190012` = `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, '
         'METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`，输入结构 44 字节（`SCSI_PASS_THROUGH` 布局）。**'
         '〔R24：驱动侧实测更正 —— 原写 `METHOD_BUFFERED` 的宏展开是 `0x190010`，与本码不符；'
         '驱动输出侧走 MDL + `MmMapLockedPages` 直写用户页、`Irp->UserBuffer` 访问 0 次，'
         '排除 NEITHER。**注意**：数据出现在「输出缓冲」这一**实测现象不变**，'
         '只是机制归因更精确。〕'),
    ]),

    ('REPORT_实机验证方案.md', [
        ('| `0x190012` | `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, '
         'METHOD_BUFFERED, FILE_ANY_ACCESS)` | **err=87**（ERROR_INVALID_PARAMETER）'
         '→ 码被识别，参数被拒 |',
         '| `0x190012` | `CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, '
         'METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`〔R24〕 | **err=87**（ERROR_INVALID_PARAMETER）'
         '→ 码被识别，参数被拒 |'),
        ('解 `0x190012`：`CTL_CODE(0x19, 0x004, METHOD_BUFFERED, FILE_ANY_ACCESS)`',
         '解 `0x190012`：`CTL_CODE(0x19, 0x004, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)`〔R24〕'),
    ]),
]


def apply_batch(name, fixes):
    print('=' * 66)
    print(name)
    print('=' * 66)
    total = 0
    for rel, pairs in fixes:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        if not os.path.isfile(p):
            print('  [跳过] 文件不存在: %s' % rel)
            continue
        _backup(rel)
        src = open(p, encoding='utf-8').read()
        orig = src
        n = 0
        for old, new in pairs:
            c = src.count(old)
            if c == 0:
                print('  [未匹配] %s :: %s' % (rel, old[:56].replace('\n', '⏎')))
                continue
            if c > 1:
                print('  [多处 %d，跳过] %s :: %s' % (c, rel, old[:48].replace('\n', '⏎')))
                continue
            src = src.replace(old, new)
            n += 1
        if src != orig:
            open(p, 'w', encoding='utf-8', newline='').write(src)
            total += n
            print('  [OK %d 处] %s' % (n, rel))
        else:
            print('  [无变化] %s' % rel)
    print('  小计 %d 处' % total)
    print()
    return total


def main():
    print('备份目录: %s' % BAK)
    print()
    a = apply_batch('批次 A —— R25：回滚 R22/R23 的公式部分', FIX_A)
    b = apply_batch('批次 B —— R24：METHOD 术语修正', FIX_B)
    print('=' * 66)
    print('合计替换 %d 处（A=%d, B=%d）' % (a + b, a, b))
    return 0


if __name__ == '__main__':
    sys.exit(main())
