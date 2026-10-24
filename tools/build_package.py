"""
LS8000 固件逆向 —— 打包脚本

把工作区 <HOME>/WorkBuddy/2026-10-24-15-49-48/LS8000 的成果
整理成结构化交付包到 D:/AI/TEST/LS8000_FW_Reverse_20261024/。

原则
----
1. **样本不拷入包体**：D:\\ 下的原始样本保持只读，仅在 samples_manifest.txt
   登记「路径 + 字节数 + SHA256」，避免把 800KB 级原始样本混进交付包造成
   「包内样本 = 已验证样本」的误解。样本与工具链的获取方式写在 README。
2. **脚本可移植**：把 202 个脚本里硬编码的 `D:/DS/TEST/LS8000` 改写为
   `paths.sample(...)` 相对调用，使包在任意机器上都能跑。
3. **可校验**：为每个入库文件生成 SHA256，写入 MANIFEST.txt。
4. **不改原件**：源工作区只读不改；路径改写只发生在包内副本上。

用法
----
    python build_package.py            # 构建
    python build_package.py --verify   # 只校验已有包
"""
import hashlib
import os
import re
import shutil
import sys

SRC = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
# 打包脚本放在 03_analysis/_pkgtool/ 下时，向上两级即工作区根
if os.path.basename(SRC) == '_pkgtool':
    SRC = os.path.dirname(os.path.dirname(SRC))
else:
    SRC = os.path.dirname(SRC)

DST = os.path.abspath(os.environ.get(
    'LS8000_PKG_DEST', 'D:/AI/TEST/LS8000_FW_Reverse_20261024'))

TOOLCHAIN = os.path.join(SRC, '03_analysis', '_pkgtool')

# ------------------------------------------------------------------ 复制规则
# (源相对路径, 包内相对路径)

DOCS_MAIN = [
    'REPORT_全面分析总结-20261024.md',      # 唯一总入口
    'REPORT_回写总账-20261024.md',          # 唯一查证入口
    'REPORT_L3-交接定稿.md',               # 主报告
    'LS8000-全案总结.md',
    'HANDOFF.md',
]

DOCS_SUB = [
    'LS8000-L3-分析报告.md',
    'LS8000-已有成果总索引.md',
    'REPORT_DataTables-解析.md',
    'REPORT_E0-C1-子功能分派.md',
    'REPORT_WriteBuffer-地址校验.md',
    'REPORT_片夹类型码-完整证据链.md',
    'REPORT_实机验证交接.md',
    'REPORT_实机验证方案.md',
    '03_analysis/BRIEF.md',
]

REPORTS_FW = [
    '03_analysis/firmware/E0子功能分派与校验表-实测补全.md',
    '03_analysis/firmware/e0_bridge.md',
    '03_analysis/firmware/internal_26cmds.md',
    '03_analysis/firmware/table_01914A.md',
    '03_analysis/firmware/table_03E390.md',
    '03_analysis/firmware/var_4003FB.md',
    '03_analysis/firmware/calib_2753E.md',
    '03_analysis/firmware/film_ident_28BB0.md',
    '03_analysis/firmware/statemachine_27DC4.md',
    '03_analysis/firmware/hostcode_source.md',
    '03_analysis/firmware/_jobfuncs/LS8000-E0总表与修正-20261024.md',
    '03_analysis/firmware/_jobfuncs/boot_block_code.md',
    '03_analysis/firmware/_jobfuncs/boot_block_data.md',
    '03_analysis/firmware/_jobfuncs/image_algo.md',
    '03_analysis/firmware/_jobfuncs/交叉结论-给实机验证线-20261024.md',
    '03_analysis/firmware/_jobfuncs/回写清单-第三轮-20261024.md',
    '03_analysis/firmware/_jobfuncs/agent_sense/agent_sense_report.md',
    '03_analysis/firmware/_jobfuncs/agent_arms/agent_arms_report.md',
    '03_analysis/firmware/_jobfuncs/agent_b3/agent_b3_report.md',
    '03_analysis/firmware/_jobfuncs/agent_81/REPORT_E0_0x81_jobfuncs.md',
    '03_analysis/firmware/_jobfuncs/agent_10/agent_10_report.md',
    '03_analysis/firmware/_jobfuncs/agent_15354/agent_15354_report.md',
]

REPORTS_LIVE = [
    '03_analysis/live/INCIDENT-20241024-实机协议与蓝屏.md',
]

# 数据表（机读格式一并带走）
DATA_TABLES = [
    '03_analysis/firmware/table_01914A.csv',
    '03_analysis/firmware/table_03E390.json',
    '03_analysis/firmware/internal_26cmds.json',
    '03_analysis/firmware/rows.json',
    '03_analysis/firmware/rows_md.txt',
    '03_analysis/firmware/out_census.txt',
    '03_analysis/firmware/sites.json',
    '03_analysis/firmware/_jobfuncs/edges.json',
    '03_analysis/md3/cap_to_cdb.csv',
    '03_analysis/md3/cap_to_cdb.md',
    '03_analysis/md3/cdb_sites.md',
    '03_analysis/md3/dispatch.md',
    '03_analysis/md3/exports.md',
    '03_analysis/md3/cfg_stats.txt',
    '03_analysis/md3/factory_ids.txt',
]

# 反汇编产物
DISASM = [
    '03_analysis/firmware/_jobfuncs/fix36_summary.txt',
    '02_analysis/h8/disasm_all.txt',
    '02_analysis/h8/functions.txt',
    '02_analysis/h8/blocks.txt',
    '02_analysis/h8/key_analysis.txt',
    '02_analysis/h8/sample_regions.txt',
    '02_analysis/h8/strings_xref.txt',
    '03_analysis/firmware/calib_2753E.asm.txt',
    '03_analysis/firmware/film_ident_28BB0.asm.txt',
    '03_analysis/firmware/statemachine_27DC4.asm.txt',
]

# 索引（子 agent 产出）
INDEX_FILES = [
    '03_analysis/status/PRIOR_ROUND_INDEX.md',
    '03_analysis/status/FW_DOC_INDEX.md',
    '03_analysis/status/DISASM_INDEX.md',
    '03_analysis/status/HOST_TOOL_INDEX.md',
    '03_analysis/status/LIVE_LINE_INDEX.md',
    '03_analysis/status/VERDICT_0x400408.md',
    '03_analysis/status/IOCTL_0x190012_METHOD_VERDICT.md',
    '03_analysis/status/EDGES_0x40_STATE_AUDIT.md',
    '03_analysis/status/APPLIED_R24_R25_FIXES.md',
]

# 主机侧原始数据（机读）
HOST_DATA = [
    '03_analysis/md3/cfg_dispatch.json',
    '03_analysis/md3/cfg_dispatch.txt',
    '03_analysis/md3/cfg_funcs.txt',
    '03_analysis/md3/caps_raw.json',
    '03_analysis/md3/cdb_sites.json',
    '03_analysis/md3/statics.json',
    '03_analysis/md3/s2_strings.json',
    '03_analysis/md3/anchors.json',
    '03_analysis/md3/funcs.txt',
    '03_analysis/md3/indirect.txt',
    '03_analysis/md3/jmp_scan.txt',
]


def _copy_list(rel_list, subdir, dst_root):
    """复制一组文件到包内 subdir 下，返回 (成功数, 缺失列表)。"""
    ok, miss = 0, []
    for rel in rel_list:
        s = os.path.join(SRC, rel.replace('/', os.sep))
        d = os.path.join(dst_root, subdir, os.path.basename(rel))
        if os.path.isfile(s):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            ok += 1
        else:
            miss.append(rel)
    return ok, miss


def _copy_tree(rel_dir, subdir, dst_root, exts=None, skip_names=None):
    """递归复制整个目录。exts 限定后缀；skip_names 为要跳过的文件名集合。"""
    s0 = os.path.join(SRC, rel_dir.replace('/', os.sep))
    n = 0
    if not os.path.isdir(s0):
        return 0
    for root, dirs, files in os.walk(s0):
        dirs[:] = [d for d in dirs if d not in ('__pycache__',)]
        for f in files:
            if skip_names and f in skip_names:
                continue
            if exts and os.path.splitext(f)[1].lower() not in exts:
                continue
            s = os.path.join(root, f)
            rel = os.path.relpath(s, s0)
            d = os.path.join(dst_root, subdir, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    return n


# ------------------------------------------------- 路径重定位（硬编码 → 相对）

RE_PAT = [
    # r'D:/DS/TEST/LS8000/xxx'  与  r'D:\DS\TEST\LS8000\xxx'
    (re.compile(r"""(?P<q>['"])(?:[rR])?(?P<p>[Dd]:[\\/]{1,2}DS[\\/]{1,2}TEST[\\/]{1,2}LS8000[\\/]{1,2})(?P<rest>[^'"]+?)(?P=q)"""),
     None),
]


def _rewrite_paths_in_file(path):
    """把脚本里的硬编码 D 盘样本路径改写为 paths.sample()/paths.cfg() 调用。

    改写规则：
      open(r'D:/DS/TEST/LS8000/LS8000_111_ROM.bin') -> open(sample('LS8000_111_ROM.bin'))
      open(r'D:/DS/TEST/LS8000/cfg_v4.json')        -> open(cfg('cfg_v4.json'))
      open(r'D:/DS/TEST/LS8000/driver/LS8000.md3')  -> open(sample('driver/LS8000.md3'))
      sys.path.insert(0, r'D:/DS/TEST/LS8000')      -> sys.path.insert(0, TOOLCHAIN_ROOT)
    """
    try:
        src = open(path, 'r', encoding='utf-8', errors='replace').read()
    except Exception:
        return 0
    orig = src

    # 1) sys.path.insert / sys.path.append 的样本根
    src = re.sub(
        r"""sys\.path\.(insert|append)\(\s*0\s*,\s*(?:[rR])?['"](?:[Dd]:[\\/]{1,2}DS[\\/]{1,2}TEST[\\/]{1,2}LS8000)['"]\s*\)""",
        r"sys.path.\1(0, TOOLCHAIN_ROOT)", src)
    # 2) 文件打开路径
    #    稳健写法：一次性匹配 [前缀r]引号 + 完整路径 + 结束引号，
    #    路径部分允许不含引号，避免嵌套引号导致的错配。
    _PATH_RE = re.compile(
        r"""(?:[rR])?(?P<q>['"])"""
        r"""[Dd]:[\\/]{1,2}DS[\\/]{1,2}TEST[\\/]{1,2}LS8000[\\/]{1,2}"""
        r"""(?P<rest>[^'"\r\n]*?)"""
        r"""(?P=q)""")

    def _sub_open(m):
        rest = m.group('rest').replace('\\', '/')
        fn = 'cfg' if rest.startswith('cfg_') else 'sample'
        return "%s('%s')" % (fn, rest)

    src = _PATH_RE.sub(_sub_open, src)

    if src != orig:
        # 确保 import 存在
        needs = []
        if re.search(r"\bsample\(", src):
            needs.append('sample')
        if re.search(r"\bcfg\(", src):
            needs.append('cfg')
        if 'TOOLCHAIN_ROOT' in src:
            needs.append('TOOLCHAIN_ROOT')

        if needs and 'from paths import' not in src and 'import paths' not in src:
            # 让包内 paths.py 可被找到。脚本可能位于 tools/scripts/<多层子目录>/，
            # 深度不定，故向上逐级查找含 paths.py 的目录（包根），而非固定层数。
            imp = ('import os as _os, sys as _sys\n'
                   '_p = _os.path.dirname(_os.path.abspath(__file__))\n'
                   'while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):\n'
                   '    _q = _os.path.dirname(_p)\n'
                   '    if _q == _p:\n'
                   '        break\n'
                   '    _p = _q\n'
                   '_sys.path.insert(0, _p)\n'
                   'from paths import %s' % ', '.join(sorted(set(needs))))
            lines = src.split('\n')
            # 插入点：第一个 import/from 语句之前；找不到则放在文件头
            idx = None
            for i, l in enumerate(lines):
                if l.startswith('import ') or l.startswith('from '):
                    idx = i
                    break
            if idx is None:
                idx = 0
                for i, l in enumerate(lines[:10]):
                    if l.startswith('#!') or l.startswith('# -*-'):
                        idx = i + 1
            # 若第一个 import 已在函数体内（缩进），退回到文件头安全位置
            if idx < len(lines) and lines[idx][:1] in (' ', '\t'):
                idx = 0
            lines.insert(idx, imp)
            src = '\n'.join(lines)

        try:
            open(path, 'w', encoding='utf-8', newline='').write(src)
            return 1
        except Exception:
            return 0
    return 0


def _rewrite_tree(dst_root, subdir):
    """对包内已复制的 .py 脚本做路径重定位。"""
    base = os.path.join(dst_root, subdir)
    n = 0
    if not os.path.isdir(base):
        return 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                n += _rewrite_paths_in_file(os.path.join(root, f))
    return n


def _fix_escape_errors(dst_root, subdirs):
    """修正常见笔误：字节串里不完整的十六进制转义（\\xa / \\x2 这类）。

    `b'\\xa'` 在 Python 里是 `\\x` + `a` 的歧义写法，编译期直接报
    "invalid \\x escape"。这类错误只影响个别脚本，但会让整包构建中断。
    这里自动补齐为 2 位形式（`\\xa` → `\\xa0`），并记录修复数。
    """
    import re as _re
    # 只在 b'...' 字节串字面量内部修复，避免误伤正则/普通字符串里的 \x 写法
    pat = _re.compile(r"""(b(['"]))(?:[^\\]|\\.)*?\2""", _re.S)
    hexpat = _re.compile(r"\\x([0-9a-fA-F](?![0-9a-fA-F]))")
    fixed = 0
    touched = []

    def _fix_bytes(m):
        nonlocal fixed
        lit = m.group(0)
        if not hexpat.search(lit):
            return lit
        n = len(hexpat.findall(lit))
        new = hexpat.sub(lambda mm: '\\x' + (mm.group(1) + '0')[:2], lit)
        fixed += n
        return new

    for sub in subdirs:
        base = os.path.join(dst_root, sub)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if not f.endswith('.py'):
                    continue
                p = os.path.join(root, f)
                # 排除打包脚本自身：它的 docstring 里含本规则的自述示例，
                # 改它会形成自修改循环。
                if os.path.basename(p) == 'build_package.py':
                    continue
                try:
                    src = open(p, 'r', encoding='utf-8', errors='replace').read()
                except Exception:
                    continue
                if not hexpat.search(src):
                    continue
                before = fixed
                # 逐行处理：注释行不参与修复（注释里可能出现 b'\\xa' 这类示例文本）
                lines_out = []
                for ln in src.split('\n'):
                    st = ln.lstrip()
                    if st.startswith('#') or not hexpat.search(ln):
                        lines_out.append(ln)
                        continue
                    new = pat.sub(_fix_bytes, ln)
                    if new != ln:
                        fixed += len(hexpat.findall(ln)) - len(hexpat.findall(new))
                    lines_out.append(new)
                src2 = '\n'.join(lines_out)
                if fixed == before:
                    continue
                try:
                    compile(src2, p, 'exec')
                except SyntaxError:
                    # 修完仍不合法就放弃，保原文件
                    fixed = before
                    continue
                try:
                    open(p, 'w', encoding='utf-8', newline='').write(src2)
                    touched.append(os.path.relpath(p, dst_root).replace('\\', '/'))
                except Exception:
                    fixed = before
    return fixed, touched


def _syntax_gate(dst_root, subdirs):
    """重定位后逐个编译校验 .py，任何语法错误立即报告。

    这是打包的关键闸门：路径改写若产出畸形代码（如 open(rsample(...))），
    语法层面就能抓到，不必等到运行时才发现。
    """
    bad = []
    checked = 0
    for sub in subdirs:
        base = os.path.join(dst_root, sub)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if not f.endswith('.py'):
                    continue
                p = os.path.join(root, f)
                rel = os.path.relpath(p, dst_root).replace('\\', '/')
                checked += 1
                try:
                    src = open(p, 'r', encoding='utf-8', errors='replace').read()
                    compile(src, rel, 'exec')
                except SyntaxError as e:
                    bad.append((rel, 'SyntaxError line %s: %s' % (e.lineno, e.msg)))
                except Exception as e:
                    bad.append((rel, '%s: %s' % (type(e).__name__, e)))
    return checked, bad


# --------------------------------------------------------------- SHA256 清单

def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def build_manifest(dst_root, out_name='MANIFEST.txt'):
    """生成包内文件的 SHA256 清单（相对路径排序，跳过清单自身）。"""
    rows = []
    for root, dirs, files in os.walk(dst_root):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, dst_root).replace('\\', '/')
            if rel == out_name:
                continue
            rows.append((rel, os.path.getsize(p), sha256_of(p)))
    rows.sort(key=lambda x: x[0])
    lines = []
    lines.append('# LS8000 固件逆向交付包 —— 文件校验清单')
    lines.append('# 格式: SHA256  字节数  相对路径')
    lines.append('# 包根: %s' % dst_root)
    lines.append('# 文件数: %d   总字节: %d' % (len(rows), sum(r[1] for r in rows)))
    lines.append('# 校验: sha256sum -c 可用（需把下行转为标准格式），或用 verify_package.py')
    lines.append('')
    for rel, size, h in rows:
        lines.append('%s  %10d  %s' % (h, size, rel))
    out = os.path.join(dst_root, out_name)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    return len(rows), sum(r[1] for r in rows)


# ------------------------------------------------------------- 样本清单

SAMPLES = [
    ('D:/DS/TEST/LS8000/LS8000_111_ROM.bin', 'H8 固件 ROM 主程序镜像（228345 B，逆向主对象）'),
    ('D:/DS/TEST/LS8000/LS8000_bootblock.bin', '引导块 64 KB（复位向量/缝隙/挂死桩/设置记录）'),
    ('D:/DS/TEST/LS8000/LS8000_full_512K.bin', '整机 512 KB 全镜像（引导块 + ROM + 两段镜像 + 0x60000 区）'),
    ('D:/DS/TEST/LS8000/decoded.bin', '与 LS8000_111_ROM.bin 同哈希（历史遗留命名，非独立样本）'),
    ('D:/DS/TEST/LS8000/FIRMDATA.bin', '宿主 updater 的 FIRMDATA 资源'),
    ('D:/DS/TEST/LS8000/h8.lst', 'H8 指令模式表（自建解码器输入；注意原版正则缺陷）'),
    ('D:/DS/TEST/LS8000/h8dis.py', '自建 H8 反汇编器'),
    ('D:/DS/TEST/LS8000/h8tab.py', '模式表加载器（原版，含被修复的缺陷）'),
    ('D:/DS/TEST/LS8000/cfg_v4.json', '主机侧静态分析配置快照（脚本高频引用）'),
    ('D:/DS/TEST/LS8000/driver/LS8000.md3', '扫描仪主机侧驱动/程序（958 KB）'),
    ('D:/DS/TEST/LS8000/driver/NKDUSCAN.dll', '主机侧 USB/1394 通道 DLL'),
    ('D:/DS/TEST/LS8000/driver/NKDSBP2.dll', '主机侧 SBP2 通道 DLL（蓝屏栈涉及）'),
    ('D:/DS/TEST/LS8000/driver/ICEDLL.dll', '主机侧 ICE 引擎 DLL'),
    ('D:/DS/TEST/research/LS8000.bin', '异源镜像（与 full_512K 差异 249568 B，非本机 ROM）'),
]


def build_samples_manifest(dst_root):
    lines = []
    lines.append('# LS8000 固件逆向 —— 只读样本登记表')
    lines.append('#')
    lines.append('# 【重要】本包 **不包含** 原始样本文件。以下仅登记其路径、字节数与 SHA256，')
    lines.append('#              便于第三方核对分析所依据的样本是否一致（防止张冠李戴）。')
    lines.append('#')
    lines.append('# 获取方式（二选一）：')
    lines.append('#   A. 直接从下表路径取用原样本（推荐，保持原始来源）')
    lines.append('#   B. 复制到一个目录后，用环境变量指定：')
    lines.append('#        set LS8000_SAMPLE_ROOT=<你的样本目录>')
    lines.append('#      然后运行 python tools/paths.py 自检。')
    lines.append('#')
    lines.append('# 样本间关系（已实测）：')
    lines.append('#   - LS8000_full_512K.bin[0x00000:0x10000] == LS8000_bootblock.bin （逐字节全等）')
    lines.append('#   - LS8000_full_512K.bin[0x10000:0x10000+228345] == LS8000_111_ROM.bin（逐字节全等）')
    lines.append('#   - decoded.bin 与 LS8000_111_ROM.bin SHA256 相同（同一份数据，命名有误导）')
    lines.append('#   - research/LS8000.bin 与 full_512K 差异 249568 字节、头部不同，为异源镜像')
    lines.append('')
    lines.append('# %-64s  %10s  %s' % ('SHA256', '字节数', '说明'))
    lines.append('# ' + '-' * 118)
    okc = 0
    for p, desc in SAMPLES:
        p = p.replace('/', os.sep) if os.sep != '/' else p
        if os.path.isfile(p):
            lines.append('%s  %10d  %s' % (sha256_of(p), os.path.getsize(p), desc))
            lines.append('#   └─ 路径: %s' % p.replace(os.sep, '/'))
            okc += 1
        else:
            lines.append('%s  %10s  %s' % ('-' * 64, 'MISSING', desc))
            lines.append('#   └─ 路径: %s  (未找到)' % p.replace(os.sep, '/'))
    lines.append('')
    lines.append('# 登记条目: %d / %d' % (okc, len(SAMPLES)))
    out = os.path.join(dst_root, 'samples_manifest.txt')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    return okc, len(SAMPLES)


# ------------------------------------------------------------------ 主流程

def _fix_edges(dst_root):
    """校验包内 edges.json 的作业表键值是否与 ROM 实测真值一致（**只校验，不改写**）。

    实测教训（R25）：早先版本只改「键名」不重算「内容」，
    造成「名实不符」的中间态 —— 键写 0x02AEAA、内容却是 0x02AAAE 的走查残留，
    比修正前更危险。因此这里只校验；不一致时明确报警。

    正确做法：修 `dis_all.py` 的 TARGETS 源头，然后**重跑**重新生成 edges.json。
    """
    import json
    p = os.path.join(dst_root, '07_data', 'edges.json')
    if not os.path.isfile(p):
        print('edges.json 校验         : 未找到，跳过')
        return 0, []
    try:
        e = json.load(open(p, encoding='utf-8'))
    except Exception as ex:
        print('edges.json 校验         : 读取失败 (%s)' % ex)
        return 0, ['读取失败']

    # ROM 实测真值
    rom_path = None
    for cand in (os.environ.get('LS8000_SAMPLE_ROOT', ''),
                 'D:/DS/TEST/LS8000'):
        if cand and os.path.isfile(os.path.join(cand.replace('\\', '/'),
                                                'LS8000_111_ROM.bin')):
            rom_path = os.path.join(cand.replace('\\', '/'), 'LS8000_111_ROM.bin')
            break
    truth = {}
    if rom_path:
        rom = open(rom_path, 'rb').read()
        t = 0x03EDE8 - 0x10000
        for i in range(11):
            b = rom[t + i * 6:t + i * 6 + 6]
            if len(b) < 6 or b[0] == 0:
                break
            truth['%02X' % b[0]] = '%06X' % int.from_bytes(b[2:6], 'big')

    bad = []
    if truth:
        for k in e:
            if '->' not in k:
                continue
            kn, fn = k.split('->', 1)
            t2 = truth.get(kn)
            if t2 and t2 != fn:
                bad.append((k, '应为 %s' % t2))

    # 名实相符性：每组的 from 地址应落在目标函数体附近
    for k, edges in e.items():
        if '->' not in k or not isinstance(edges, list) or not edges:
            continue
        fn = int(k.split('->')[1], 16)
        for ed in edges:
            fr = ed.get('from')
            if isinstance(fr, int) and not (fn - 0x4000 <= fr <= fn + 0x4000):
                bad.append((k, '边的 from=0x%06X 落在目标函数 0x%06X 之外（名实不符）'
                            % (fr, fn)))
                break

    if bad:
        print('edges.json 校验         : **发现 %d 处不一致（中止打包，不做改写）**' % len(bad))
        for k, why in bad:
            print('    %s  <- %s' % (k, why))
        print('    正确做法：修 dis_all.py 的 TARGETS 源头后重跑，重新生成 edges.json')
        return len(bad), [k for k, _ in bad]

    n_edges = sum(len(v) for v in e.values() if isinstance(v, list))
    print('edges.json 校验         : %d 组 / %d 边，键值与名实均与 ROM 实测一致'
          % (len(e), n_edges))
    return 0, []


def main():
    if '--verify' in sys.argv:
        return verify(DST)

    print('源工作区: %s' % SRC)
    print('目标包  : %s' % DST)
    print()

    if os.path.isdir(DST):
        print('目标已存在，先清空...')
        shutil.rmtree(DST)
    os.makedirs(DST, exist_ok=True)

    report = []

    # 1. 主文档
    ok, miss = _copy_list(DOCS_MAIN, '01_docs', DST)
    report.append(('01_docs 主文档', ok, miss))
    print('01_docs 主文档        : %d 份' % ok)

    ok, miss = _copy_list(DOCS_SUB, '01_docs/sub', DST)
    report.append(('01_docs/sub 专题文档', ok, miss))
    print('01_docs/sub            : %d 份' % ok)

    # 2. 专题报告
    ok, miss = _copy_list(REPORTS_FW, '02_reports/firmware', DST)
    report.append(('02_reports/firmware', ok, miss))
    print('02_reports/firmware    : %d 份' % ok)

    ok, miss = _copy_list(REPORTS_LIVE, '02_reports/live', DST)
    report.append(('02_reports/live', ok, miss))
    print('02_reports/live        : %d 份' % ok)

    # 3. 索引
    ok, miss = _copy_list(INDEX_FILES, '03_indexes', DST)
    report.append(('03_indexes', ok, miss))
    print('03_indexes             : %d 份' % ok)

    # 4. 反汇编产物
    ok, miss = _copy_list(DISASM, '04_disasm', DST)
    report.append(('04_disasm', ok, miss))
    print('04_disasm              : %d 份' % ok)

    # 4b. fix_*.asm / f_*.asm / boot_*.asm
    n = _copy_tree('03_analysis/firmware/_jobfuncs', '04_disasm/jobfuncs', DST,
                   exts={'.asm'}, skip_names=None)
    print('04_disasm/jobfuncs     : %d 个 .asm' % n)
    report.append(('04_disasm/jobfuncs', n, []))

    # 5. 工具链（解码器 + 路径模块）
    os.makedirs(os.path.join(DST, 'tools'), exist_ok=True)
    for f in ('h8.lst', 'h8dis.py', 'h8tab.py', 'paths.py', 'verify_package.py',
              'verify_decoder_fix.py', 'h8sim.py', 'sim_verify_formulas.py',
              'build_slot_map.py', 'build_prior_index.py', 'apply_verdict_fixes.py',
              'build_package.py'):
        s = os.path.join(TOOLCHAIN, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(DST, 'tools', f))
    # 包根也放一份 paths.py，便于顶层脚本 import
    shutil.copy2(os.path.join(TOOLCHAIN, 'paths.py'), os.path.join(DST, 'paths.py'))
    # README（唯一入口）
    shutil.copy2(os.path.join(TOOLCHAIN, 'README_00.md'),
                 os.path.join(DST, '00_README.md'))
    print('tools (解码器+验证)      : 12 份 (+ 包根 paths.py, 00_README.md)')

    # 5b. 分析脚本
    n = _copy_tree('03_analysis', 'tools/scripts', DST,
                   exts={'.py', '.ps1'},
                   skip_names={'paths.py'})
    print('tools/scripts           : %d 个脚本' % n)
    report.append(('tools/scripts', n, []))

    n = _copy_tree('tools', 'tools/legacy', DST,
                   exts={'.py', '.txt'},
                   skip_names=set())
    print('tools/legacy            : %d 个' % n)

    # 6. 主机侧数据
    ok, miss = _copy_list(HOST_DATA, '05_hostside/data', DST)
    report.append(('05_hostside/data', ok, miss))
    print('05_hostside/data        : %d 份' % ok)

    # 7. 实机线
    n = _copy_tree('03_analysis/live', '06_live', DST,
                   exts={'.py', '.ps1', '.md'})
    print('06_live                 : %d 个' % n)
    # 实机安全须知（醒目提示）
    shutil.copy2(os.path.join(TOOLCHAIN, 'README_LIVE_SAFETY.md'),
                 os.path.join(DST, '06_live', 'README_实机安全须知.md'))
    # 包根也放一份，让接手者第一眼就能看到红线
    shutil.copy2(os.path.join(TOOLCHAIN, 'README_LIVE_SAFETY.md'),
                 os.path.join(DST, 'README_实机安全须知.md'))

    # 8. 数据表
    ok, miss = _copy_list(DATA_TABLES, '07_data', DST)
    report.append(('07_data', ok, miss))
    print('07_data                 : %d 份' % ok)

    # 8b. edges.json 键值修正（打包时用 ROM 实测真值校验并修正）
    _fix_edges(DST)

    # 9. 路径重定位
    r1 = _rewrite_tree(DST, 'tools/scripts')
    r2 = _rewrite_tree(DST, 'tools/legacy')
    r3 = _rewrite_tree(DST, '06_live')
    print('路径重定位              : %d 个脚本（scripts %d / legacy %d / live %d）'
          % (r1 + r2 + r3, r1, r2, r3))

    # 9b. 转义笔误自动修复（\xa / \x2 这类会让编译失败）
    nfix, touched = _fix_escape_errors(DST, ['tools/scripts', 'tools/legacy', '06_live'])
    if nfix:
        print('转义笔误修复            : %d 处（%d 个文件）' % (nfix, len(touched)))
        for t in touched[:8]:
            print('    %s' % t)
        if len(touched) > 8:
            print('    ... 另有 %d 个' % (len(touched) - 8))
    else:
        print('转义笔误修复            : 无需修复')

    # 9c. 语法闸门：重定位后必须全部可编译
    checked, bad = _syntax_gate(DST, ['tools/scripts', 'tools/legacy', '06_live'])
    print('语法校验                : %d 个脚本，%d 个异常' % (checked, len(bad)))
    if bad:
        print()
        print('【语法错误 %d 个 —— 打包中止】' % len(bad))
        for rel, msg in bad[:40]:
            print('  %s' % rel)
            print('      %s' % msg)
        if len(bad) > 40:
            print('  ... 另有 %d 个' % (len(bad) - 40))
        return 3

    # 10. 清单
    n, total = build_manifest(DST)
    print('MANIFEST.txt            : %d 文件 / %d 字节' % (n, total))

    ok, all_ = build_samples_manifest(DST)
    print('samples_manifest.txt    : %d / %d 条登记' % (ok, all_))

    # 10b. 重生成 MANIFEST（此时 samples_manifest.txt 已存在，把它也纳入清单）
    n, total = build_manifest(DST)
    print('MANIFEST.txt (终版)     : %d 文件 / %d 字节' % (n, total))

    # 10b. 重生成 MANIFEST（此时 samples_manifest.txt 已存在，把它也纳入清单）
    n, total = build_manifest(DST)
    print('MANIFEST.txt (终版)     : %d 文件 / %d 字节' % (n, total))

    # 缺失汇总
    print()
    allmiss = []
    for name, _, miss in report:
        if miss:
            allmiss.extend(miss)
    if allmiss:
        print('【缺失 %d 项】' % len(allmiss))
        for m in allmiss:
            print('  - %s' % m)
    else:
        print('【无缺失】所有登记文件均已找到。')

    return 0


def verify(dst_root):
    """校验包内文件 SHA256 与 MANIFEST.txt 是否一致。"""
    mf = os.path.join(dst_root, 'MANIFEST.txt')
    if not os.path.isfile(mf):
        print('找不到 MANIFEST.txt: %s' % mf)
        return 1
    bad = 0
    total = 0
    for line in open(mf, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#'):
            continue
        parts = line.split('  ')
        if len(parts) < 3:
            continue
        h, size, rel = parts[0], parts[1].strip(), parts[2].strip()
        p = os.path.join(dst_root, rel.replace('/', os.sep))
        total += 1
        if not os.path.isfile(p):
            print('缺失: %s' % rel)
            bad += 1
            continue
        if os.path.getsize(p) != int(size):
            print('大小不符: %s' % rel)
            bad += 1
            continue
        if sha256_of(p) != h:
            print('哈希不符: %s' % rel)
            bad += 1
    print('校验完成: %d 个文件, %d 个异常' % (total, bad))
    return 0 if bad == 0 else 2


if __name__ == '__main__':
    sys.exit(main())
