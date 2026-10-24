# ==========================================================
# !! WARNING — 请勿盲目运行 / DO NOT RUN BLINDLY !!
# ----------------------------------------------------------
# 本脚本会向**真实的** Nikon LS-8000 ED 扫描仪发送原始 DeviceIoControl
# 请求（IEEE-1394 / FireWire 总线）。操作对象是硬件，不是文件。
#
# This script issues raw DeviceIoControl calls to REAL hardware.
#
# 风险等级 Risk level      : 🟢 LOW  (SAFE_ONLY, 仅发 0x190012)
# 已知危害 Known hazards   :
#     - 曾有脚本(ps_probe6 / ps_brute)导致宿主蓝屏
#       0xD1 DRIVER_IRQL_NOT_LESS_OR_EQUAL，疑似 sbp2port.sys 1394 协议栈
#     - 写入类命令 SCSI WRITE BUFFER 可能造成扫描仪固件损坏且不可恢复
#     - 命令集超出白名单时后果未知
#
# 白名单 Whitelist (冻结中) :
#     仅允许 INQUIRY 标准页 0，CDB = 12 00 00 00 24 00，alloc 36 字节
#
# 前置 Before running       :
#     1) 完整阅读仓库根目录 DISCLAIMER.md
#     2) 确认已断开其它 1394 设备、无重要数据、可承受蓝屏
#     3) 本脚本由 AI 辅助迭代生成，作者非专业固件工程师，未经同行评审
#
# 本项目为个人学习性质，作者是新手，代码能力有限，全部分析结论均由 AI
# 多轮推演得出，请自行核验后再决定是否使用。使用后果自负。
# ==========================================================

# LS-8000 ED read-only SCSI tool - 32-bit PowerShell
#
# ============================================================================
# SAFETY: every command below is in the SCSI "pure query" set:
#   INQUIRY(0x12) / TEST UNIT READY(0x00) / REQUEST SENSE(0x03) / MODE SENSE(0x1A)
# No media access, no mechanism motion, no parameter change, no WRITE BUFFER,
# no READ BUFFER, no E0/E1. An allowlist below refuses anything else, so a
# mistake in the caller cannot send an unsafe command.
#
# PROTOCOL (derived from the loaded 64-bit in-box scsiscan.sys, verified live):
#   ioctl 0x190012, 44-byte input struct, 32-bit caller:
#     +0x00 dword    44
#     +0x04 dword    44                 (struct total length; driver requires == 0x2C)
#     +0x08 byte     0x40               (bit6 = data from device; bit7 = to device)
#     +0x0C byte     CdbLength (6)
#     +0x0D byte     SenseInfoLength (18)
#     +0x10 dword    DataTransferLength
#     +0x14 byte[16] CDB
#     +0x24 dword    DataBuffer pointer
#     +0x28 dword    SenseBuffer pointer
#   The SCSI data arrives in the METHOD_BUFFERED OUTPUT buffer (bytesRet bytes),
#   NOT in the user DataBuffer.
#
# ASCII-only source: 32-bit PowerShell reads .ps1 as ANSI/GBK.
# ============================================================================

$ErrorActionPreference = 'Stop'

$src = @'
using System;
using System.Runtime.InteropServices;

public class W {
    public static readonly IntPtr INVALID = new IntPtr(-1);
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
    public static extern IntPtr CreateFileA(string name, uint access, uint share,
        IntPtr sec, uint disp, uint flags, IntPtr tmpl);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool DeviceIoControl(IntPtr h, uint code, IntPtr inBuf, uint inLen,
        IntPtr outBuf, uint outLen, out uint bytesRet, IntPtr overlapped);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr h);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint GetLastError();
}
'@
Add-Type -TypeDefinition $src -Language CSharp

# ---- safety allowlist: only these opcodes may ever be sent -------------------
$ALLOW = @{
  0x00 = 'TEST UNIT READY'
  0x03 = 'REQUEST SENSE'
  0x12 = 'INQUIRY'
  0x1A = 'MODE SENSE(6)'
}
# ---------------------------------------------------------------------------
# SAFETY GATE (2026-10-24 22:48 蓝屏之后新增):
#   只放行 INQUIRY 标准页 0。它被实测过数百次、从未崩溃，且任何 SCSI 设备
#   都必须 GOOD 应答。其它命令都可能让设备返回 CHECK CONDITION / 短数据，
#   从而进入 in-box scsiscan+sbp2port 的错误处理路径 —— 该路径已被怀疑是
#   0xD1 蓝屏（sbp2port.sys）的触发点（见 INCIDENT-20241024-实机协议与蓝屏.md）。
#   扩大命令集必须先解析 Minidump 定位到责任代码路径。
$SAFE_ONLY = $true
if ($SAFE_ONLY) {
  $ALLOW = @{ 0x12 = 'INQUIRY (standard page 0 only)' }
}
# ---------------------------------------------------------------------------

function Put32([byte[]]$b, [int]$off, [uint32]$v) {
  $b[$off] = [byte]($v -band 0xFF); $b[$off+1] = [byte](($v -shr 8) -band 0xFF)
  $b[$off+2] = [byte](($v -shr 16) -band 0xFF); $b[$off+3] = [byte](($v -shr 24) -band 0xFF)
}
function PutPtr32([byte[]]$b, [int]$off, [IntPtr]$p) {
  $v = [uint32]$p.ToInt64()
  $b[$off] = [byte]($v -band 0xFF); $b[$off+1] = [byte](($v -shr 8) -band 0xFF)
  $b[$off+2] = [byte](($v -shr 16) -band 0xFF); $b[$off+3] = [byte](($v -shr 24) -band 0xFF)
}
function Hex([byte[]]$b, [int]$n) {
  $m = [Math]::Min($n, $b.Length); $s = ''
  for ($i = 0; $i -lt $m; $i++) { $s += ('{0:X2} ' -f $b[$i]) }
  return $s
}
function Ascii([byte[]]$b, [int]$n) {
  $m = [Math]::Min($n, $b.Length); $s = ''
  for ($i = 0; $i -lt $m; $i++) {
    $c = $b[$i]
    if ($c -ge 32 -and $c -lt 127) { $s += [char]$c } else { $s += '.' }
  }
  return $s
}

# Send one allowlisted query. returns @{ok;err;bytesRet;data;sense}
function Send-Query([IntPtr]$h, [byte[]]$cdb, [int]$allocLen) {
  $op = [int]$cdb[0]
  if (-not $ALLOW.ContainsKey($op)) { throw ("REFUSED: opcode 0x{0:X2} not in allowlist" -f $op) }
  $inb = New-Object byte[] 44
  Put32 $inb 0     44
  Put32 $inb 4     44
  # direction bits: data-from-device requires bit6; no-data commands must have both clear
  if ($allocLen -gt 0) { $inb[8] = 0x40 } else { $inb[8] = 0x00 }
  $inb[0x0C] = [byte]$cdb.Length       # CdbLength
  $inb[0x0D] = 18                      # SenseInfoLength
  Put32 $inb 0x10 ([uint32]$allocLen)   # DataTransferLength
  for ($i = 0; $i -lt $cdb.Length -and $i -lt 16; $i++) { $inb[0x14 + $i] = $cdb[$i] }
  $data  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
  $sense = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(64)
  $outb  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
  try {
    for ($i = 0; $i -lt 512; $i++) { [System.Runtime.InteropServices.Marshal]::WriteByte($outb, $i, 0xEE) }
    PutPtr32 $inb 0x24 $data
    PutPtr32 $inb 0x28 $sense
    $pin = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(44)
    try {
      [System.Runtime.InteropServices.Marshal]::Copy($inb, 0, $pin, 44)
      $ret = 0
      $ok = [W]::DeviceIoControl($h, [uint32]0x190012, $pin, [uint32]44,
                                $outb, [uint32]512, [ref]$ret, [IntPtr]::Zero)
      $err = 0; if (-not $ok) { $err = [W]::GetLastError() }
      $n = [Math]::Min([int]$ret, 512)
      $ob = New-Object byte[] 512
      [System.Runtime.InteropServices.Marshal]::Copy($outb, $ob, 0, 512)
      $sb = New-Object byte[] 64
      [System.Runtime.InteropServices.Marshal]::Copy($sense, $sb, 0, 64)
      return @{ ok=$ok; err=$err; bytesRet=[int]$ret; out=$ob; outLen=$n; sense=$sb }
    } finally { [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pin) }
  } finally {
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($sense)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb)
  }
}

$h = [W]::CreateFileA('\\.\Scanner0', [uint32]3221225472, [uint32]0, [IntPtr]::Zero, [uint32]3, [uint32]0x80, [IntPtr]::Zero)
if ($h -eq [W]::INVALID) { Write-Host "open \\.\Scanner0 FAILED err=$([W]::GetLastError())"; exit 1 }
Write-Host "=== LS-8000 ED read-only query tool (INQUIRY / TEST UNIT READY / REQUEST SENSE / MODE SENSE only) ==="
Write-Host "[OPEN] \\.\Scanner0"
Write-Host ""

$queries = @(
  @{ n='INQUIRY (standard)'; cdb=[byte[]]@(0x12,0x00,0x00,0x00,0x24,0x00); len=36 }
)
if (-not $SAFE_ONLY) {
  $queries += @(
    @{ n='TEST UNIT READY';    cdb=[byte[]]@(0x00,0x00,0x00,0x00,0x00,0x00); len=0 },
    @{ n='REQUEST SENSE';      cdb=[byte[]]@(0x03,0x00,0x00,0x00,0x12,0x00); len=18 },
    @{ n='MODE SENSE(6) p0';   cdb=[byte[]]@(0x1A,0x00,0x3F,0x00,0xFC,0x00); len=252 }
  )
}
if ($SAFE_ONLY) { Write-Host "SAFE_ONLY mode: only INQUIRY standard page 0 is allowed." }

try {
  foreach ($q in $queries) {
    $r = Send-Query $h $q.cdb $q.len
    Write-Host ("--- {0}  cdb={1}" -f $q.n, (Hex $q.cdb $q.cdb.Length))
    if (-not $r.ok) {
      Write-Host ("    FAILED err={0}" -f $r.err)
    } else {
      Write-Host ("    ok bytesRet={0}" -f $r.bytesRet)
      if ($r.bytesRet -gt 0) {
        Write-Host ("    out : {0}" -f (Hex $r.out ([Math]::Min(48, $r.bytesRet))))
        Write-Host ("    ascii: {0}" -f (Ascii $r.out ([Math]::Min(48, $r.bytesRet))))
      }
    }
  }
} finally {
  [W]::CloseHandle($h) | Out-Null
}
Write-Host ""
Write-Host "done. No state-changing command was issued."
