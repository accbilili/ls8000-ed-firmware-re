"""
LS8000 固件逆向 —— 路径配置（打包版可移植入口）

背景
----
原始工作区里 202 个脚本把样本根目录硬编码为 `D:/DS/TEST/LS8000`。
打包到 `D:\\AI\\TEST` 后样本不再位于 D 盘，硬编码会导致脚本全部不可运行。

本模块提供统一的可移植路径解析：

    from paths import SAMPLE_ROOT, sample, ensure_sample

优先级
------
1. 环境变量 `LS8000_SAMPLE_ROOT`（显式指定，最高优先）
2. 包内 `samples/` 目录（若样本已随包分发）
3. 原始 D 盘位置 `D:/DS/TEST/LS8000`（保持对旧工作区的兼容）

用法
----
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from paths import sample, SAMPLE_ROOT
    rom = open(sample('LS8000_111_ROM.bin'), 'rb').read()

命令行
------
    python paths.py            # 打印当前解析到的样本根与各样本是否存在
"""
import os
import sys

# ---------------------------------------------------------------- 候选根目录

# 1) 显式环境变量
_env = os.environ.get('LS8000_SAMPLE_ROOT', '').strip()

# 2) 包内随包分发的样本目录（scripts/ 的上两级即包根）
_pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_pkg_samples = os.path.join(_pkg_root, 'samples')

# 3) 原始 D 盘位置（兼容旧工作区）
_orig = 'D:/DS/TEST/LS8000'

_CANDIDATES = [p for p in (_env, _pkg_samples, _orig) if p]


def _pick_root():
    """按优先级选出实际存在的样本根目录；都不存在则返回首选候选。"""
    for p in _CANDIDATES:
        if os.path.isdir(p):
            return os.path.abspath(p).replace('\\', '/')
    return os.path.abspath(_CANDIDATES[0]).replace('\\', '/')


SAMPLE_ROOT = _pick_root()

# 工具链（h8.lst / h8dis.py / h8tab.py）在样本根下；打包时它们与样本同级
TOOLCHAIN_ROOT = SAMPLE_ROOT

# 配置表（cfg_v4.json 等）体量较大，独立放置时可指向别处
CFG_ROOT = os.environ.get('LS8000_CFG_ROOT', '').strip() or SAMPLE_ROOT


def sample(name, root=None):
    """返回样本根下某文件的绝对路径（不要求文件一定存在）。"""
    base = (root or SAMPLE_ROOT).replace('\\', '/')
    return base.rstrip('/') + '/' + name.replace('\\', '/')


def cfg(name):
    """返回配置文件绝对路径（cfg 独立根优先）。"""
    return sample(name, root=CFG_ROOT)


def ensure_sample(name, root=None):
    """取样本绝对路径；文件不存在则抛清晰异常，避免脚本里出现裸 FileNotFoundError。"""
    p = sample(name, root)
    if not os.path.isfile(p):
        raise FileNotFoundError(
            '缺少样本 %s\n  期望位置: %s\n'
            '  解决办法（二选一）:\n'
            '    1) 设置环境变量 LS8000_SAMPLE_ROOT 指向样本所在目录\n'
            '    2) 把样本放到包内 samples/ 目录\n'
            '  可用样本清单见 samples_manifest.txt' % (name, p))
    return p


def _self_test():
    print('LS8000 样本路径解析')
    print('=' * 60)
    print('  SAMPLE_ROOT = %s' % SAMPLE_ROOT)
    print('  来源        = %s' % (
        '环境变量 LS8000_SAMPLE_ROOT' if _env and os.path.isdir(_env) else
        '包内 samples/' if os.path.isdir(_pkg_samples) else
        '原始 D 盘位置（兼容模式）'))
    print()
    print('%-34s %12s %s' % ('文件', '大小', '状态'))
    print('-' * 60)
    for n in ('LS8000_111_ROM.bin', 'LS8000_bootblock.bin',
              'LS8000_full_512K.bin', 'h8.lst', 'h8dis.py', 'h8tab.py',
              'cfg_v4.json'):
        p = sample(n)
        if os.path.isfile(p):
            print('%-34s %12d OK' % (n, os.path.getsize(p)))
        else:
            print('%-34s %12s 缺失' % (n, '-'))
    for n in ('driver/LS8000.md3', 'driver/NKDUSCAN.dll',
              'driver/NKDSBP2.dll', 'driver/ICEDLL.dll'):
        p = sample(n)
        if os.path.isfile(p):
            print('%-34s %12d OK' % (n, os.path.getsize(p)))
        else:
            print('%-34s %12s 缺失' % (n, '-'))
    print()
    print('提示: 可用 set LS8000_SAMPLE_ROOT=<样本目录> 覆盖解析结果')
    return 0


if __name__ == '__main__':
    sys.exit(_self_test())
