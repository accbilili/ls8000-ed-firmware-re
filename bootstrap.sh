#!/usr/bin/env bash
# =============================================================================
# LS-8000 ED 固件逆向 —— 环境引导脚本 (Linux / macOS / Git Bash)
#
# 用途：帮助你设置 LS8000_SAMPLE_ROOT 环境变量，并校验样本是否齐备。
# 注意：本仓库**不提供**样本，需你自行从自己合法拥有的设备中提取。
#       See README.md → Quick start
# =============================================================================
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo "=============================================================="
echo " LS-8000 ED 固件逆向 —— 环境引导"
echo " LS-8000 ED Firmware RE — environment bootstrap"
echo "=============================================================="
echo

# ---------------------------------------------------------------- 1. Python
PY="${PYTHON:-python3}"
if ! command -v "$PY" >/dev/null 2>&1; then
    echo "[失败] 找不到 python3。请先安装 Python 3.9 或更高版本。"
    echo "[FAIL] python3 not found. Please install Python 3.9+."
    exit 1
fi
V="$("$PY" -c 'import sys;print("%d.%d.%d" % sys.version_info[:3])')"
echo "[信息] 使用的 Python: $PY  (版本 $V)"
echo "[INFO] Using Python: $PY  (version $V)"
echo

# ---------------------------------------------------------------- 2. 样本路径
CURRENT="${LS8000_SAMPLE_ROOT:-}"
if [ -z "$CURRENT" ]; then
    if [ -d "$REPO_ROOT/samples" ]; then
        CURRENT="$REPO_ROOT/samples"
        echo "[信息] 检测到 $REPO_ROOT/samples，将使用它。"
        echo "[INFO] Detected $REPO_ROOT/samples, using it."
    else
        echo "⚠️  环境变量 LS8000_SAMPLE_ROOT 尚未设置。"
        echo "⚠️  Environment variable LS8000_SAMPLE_ROOT is not set."
        echo
        echo "请提供你的样本目录路径（固件 ROM 等文件所在的目录）。"
        echo "Enter the path to your samples directory (containing the firmware ROM, etc.)."
        echo "示例 / example:  /home/you/ls8000-samples"
        read -r -p "> " INPUT
        INPUT="${INPUT%\"}"; INPUT="${INPUT#\"}"
        if [ -z "$INPUT" ]; then
            echo "[中止] 未提供路径。"
            echo "[ABORT] No path provided."
            exit 1
        fi
        if [ ! -d "$INPUT" ]; then
            echo "[错误] 目录不存在: $INPUT"
            echo "[ERROR] Directory does not exist: $INPUT"
            exit 1
        fi
        CURRENT="$INPUT"
    fi
fi

export LS8000_SAMPLE_ROOT="$CURRENT"
echo "[信息] LS8000_SAMPLE_ROOT = $LS8000_SAMPLE_ROOT"
echo

# ---------------------------------------------------------------- 3. 持久化建议
RC="~/.bashrc"
case "${SHELL##*/}" in
    zsh) RC="~/.zshrc" ;;
    bash) RC="~/.bashrc" ;;
esac
echo "💡 建议把下面这行加入 $RC，以免每次都要重新设置："
echo "💡 Tip: add this line to $RC to make it permanent:"
echo "      export LS8000_SAMPLE_ROOT=\"$LS8000_SAMPLE_ROOT\""
echo

# ---------------------------------------------------------------- 4. 自检
echo "=============================================================="
echo " 样本自检 / Sample check"
echo "=============================================================="
"$PY" paths.py
STATUS=$?
echo
if [ $STATUS -eq 0 ]; then
    echo "✅ 引导完成。接下来可以运行："
    echo "✅ Bootstrap done. You can now run:"
    echo "      python tools/verify_package.py"
    echo "      python tools/sim_verify_formulas.py"
else
    echo "⚠️  样本检查未全部通过。请对照 samples_manifest.txt 的 SHA256 核对样本版本。"
    echo "⚠️  Some samples failed the check. Compare against samples_manifest.txt SHA256."
fi
echo
echo "⚠️  安全提醒：在触碰 06_live/ 下的任何脚本之前，请先完整阅读 DISCLAIMER.md。"
echo "⚠️  SAFETY: read DISCLAIMER.md before touching anything in 06_live/."
