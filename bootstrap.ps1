# =============================================================================
# LS-8000 ED 固件逆向 —— 环境引导脚本 (Windows PowerShell)
#
# 用途：帮助你设置 LS8000_SAMPLE_ROOT 环境变量，并校验样本是否齐备。
# 注意：本仓库**不提供**样本，需你自行从自己合法拥有的设备中提取。
#       See README.md → Quick start
#
# 本文件使用 UTF-8 with BOM 编码保存，以保证 PowerShell 5.1 正确显示中文。
# =============================================================================

$ErrorActionPreference = 'Continue'
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host " LS-8000 ED 固件逆向 —— 环境引导"
Write-Host " LS-8000 ED Firmware RE - environment bootstrap"
Write-Host "=============================================================="
Write-Host ""

# ---------------------------------------------------------------- 1. Python
$py = $null
foreach ($cand in @('python', 'py', 'python3')) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) { $py = $cand; break }
}
if (-not $py) {
    Write-Host "[失败] 找不到 Python。请先安装 Python 3.9 或更高版本。" -ForegroundColor Red
    exit 1
}
$v = & $py -c 'import sys;print("%d.%d.%d" % sys.version_info[:3])'
Write-Host "[信息] 使用的 Python: $py  (版本 $v)"
Write-Host ""

# ---------------------------------------------------------------- 2. 样本路径
$sampleRoot = $env:LS8000_SAMPLE_ROOT
if ([string]::IsNullOrWhiteSpace($sampleRoot)) {
    if (Test-Path (Join-Path $RepoRoot 'samples')) {
        $sampleRoot = Join-Path $RepoRoot 'samples'
        Write-Host "[信息] 检测到 .\samples，将使用它。"
    } else {
        Write-Host "⚠️  环境变量 LS8000_SAMPLE_ROOT 尚未设置。" -ForegroundColor Yellow
        Write-Host "请提供你的样本目录路径（固件 ROM 等文件所在的目录）："
        $input_path = Read-Host "> "
        $input_path = $input_path.Trim('"')
        if ([string]::IsNullOrWhiteSpace($input_path) -or -not (Test-Path $input_path)) {
            Write-Host "[中止] 路径无效或不存在。" -ForegroundColor Red
            exit 1
        }
        $sampleRoot = $input_path
    }
}
$env:LS8000_SAMPLE_ROOT = $sampleRoot
Write-Host "[信息] LS8000_SAMPLE_ROOT = $sampleRoot"
Write-Host ""

Write-Host "💡 建议持久化（当前用户）："
Write-Host "   [Environment]::SetEnvironmentVariable('LS8000_SAMPLE_ROOT', '$sampleRoot', 'User')"
Write-Host ""

# ---------------------------------------------------------------- 3. 自检
Write-Host "=============================================================="
Write-Host " 样本自检 / Sample check"
Write-Host "=============================================================="
& $py paths.py
Write-Host ""

Write-Host "=============================================================="
Write-Host " 后续命令 / Next steps"
Write-Host "=============================================================="
Write-Host "   python tools/verify_package.py"
Write-Host "   python tools/sim_verify_formulas.py"
Write-Host ""
Write-Host "⚠️  安全提醒：在触碰 06_live\ 下的任何脚本之前，" -ForegroundColor Red -NoNewline
Write-Host "请先完整阅读 DISCLAIMER.md。" -ForegroundColor Red
Write-Host "   其中 ps_probe6.ps1 / ps_brute.ps1 已知会导致蓝屏。" -ForegroundColor Red
