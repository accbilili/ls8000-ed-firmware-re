# ==========================================================
# !! WARNING — 请勿盲目运行 / DO NOT RUN BLINDLY !!
# ----------------------------------------------------------
# 本脚本会向**真实的** Nikon LS-8000 ED 扫描仪发送原始 DeviceIoControl
# 请求（IEEE-1394 / FireWire 总线）。操作对象是硬件，不是文件。
#
# This script issues raw DeviceIoControl calls to REAL hardware.
#
# 风险等级 Risk level      : 🟠 MEDIUM (中间版本，未完整验证)
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

# LS-8000 ED read-only probe v5 - 32-bit PowerShell
#
# SCOPE: READ ONLY. Only INQUIRY (0x12). No WRITE BUFFER / READ BUFFER / E0.
#
# v5: struct layout is now correct (ioctl returns TRUE). Remaining question:
#      where did the result go? With METHOD_BUFFERED the driver sees
#      SystemBuffer = the OUTPUT buffer, so ScsiStatus / SenseInfo land in
#      the out buffer, not in the user data pointer. This probe dumps all
#      three regions: out buffer, user data buffer, user sense buffer.
#
# ASCII-only source: 32-bit PowerShell reads .ps1 as ANSI/GBK.

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

$h = [W]::CreateFileA('\\.\Scanner0', [uint32]3221225472, [uint32]0, [IntPtr]::Zero, [uint32]3, [uint32]0x80, [IntPtr]::Zero)
if ($h -eq [W]::INVALID) { Write-Host "open FAILED err=$([W]::GetLastError())"; exit 1 }
Write-Host "[OPEN] \\.\Scanner0"

$data  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
$sense = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(64)
try {
  foreach ($fb in @(0x40, 0x80, 0xC0)) {
    foreach ($cdbLen in @(6)) {
      # clear the user buffers so we can tell "written" from "untouched"
      for ($i = 0; $i -lt 512; $i++) { [System.Runtime.InteropServices.Marshal]::WriteByte($data, $i, 0xCC) }
      for ($i = 0; $i -lt 64;  $i++) { [System.Runtime.InteropServices.Marshal]::WriteByte($sense, $i, 0xDD) }

      $inb = New-Object byte[] 44
      Put32 $inb 0     44          # +0x00
      Put32 $inb 4     44          # +0x04 struct total length
      $inb[8] = [byte]$fb         # +0x08 flags (bit6|bit7 required)
      $inb[0x0C] = [byte]$cdbLen  # +0x0C CdbLength
      $inb[0x0D] = 18             # +0x0D SenseInfoLength
      Put32 $inb 0x10 36           # +0x10 DataTransferLength
      $inb[0x14] = 0x12; $inb[0x15] = 0x00; $inb[0x16] = 0x00
      $inb[0x17] = 0x00; $inb[0x18] = 0x24; $inb[0x19] = 0x00
      PutPtr32 $inb 0x24 $data      # +0x24 DataBuffer
      PutPtr32 $inb 0x28 $sense     # +0x28 SenseBuffer

      $outb = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
      for ($i = 0; $i -lt 512; $i++) { [System.Runtime.InteropServices.Marshal]::WriteByte($outb, $i, 0xEE) }
      $pin = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(44)
      try {
        [System.Runtime.InteropServices.Marshal]::Copy($inb, 0, $pin, 44)
        $ret = 0
        $ok = [W]::DeviceIoControl($h, [uint32]0x190012, $pin, [uint32]44,
                                  $outb, [uint32]512, [ref]$ret, [IntPtr]::Zero)
        $err = 0; if (-not $ok) { $err = [W]::GetLastError() }
        Write-Host ""
        Write-Host ("=== flags=0x{0:X2} cdbLen={1} -> ok={2} err={3} bytesRet={4}" -f $fb, $cdbLen, $ok, $err, $ret)
        if ($ok) {
          $ob = New-Object byte[] 96
          [System.Runtime.InteropServices.Marshal]::Copy($outb, $ob, 0, 96)
          $db = New-Object byte[] 48
          [System.Runtime.InteropServices.Marshal]::Copy($data, $db, 0, 48)
          $sb = New-Object byte[] 32
          [System.Runtime.InteropServices.Marshal]::Copy($sense, $sb, 0, 32)
          Write-Host ("  out[00..47]: {0}" -f (Hex $ob 48))
          Write-Host ("  out[48..95]: {0}" -f (Hex $ob[48..95] 48))
          Write-Host ("  data[00..47]: {0}" -f (Hex $db 48))
          Write-Host ("  data ascii : {0}" -f (Ascii $db 48))
          Write-Host ("  sense[00..31]: {0}" -f (Hex $sb 32))
        }
      } finally {
        [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pin)
        [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb)
      }
    }
  }
} finally {
  [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
  [System.Runtime.InteropServices.Marshal]::FreeHGlobal($sense)
  [W]::CloseHandle($h) | Out-Null
}
Write-Host ""
Write-Host "probe finished. Only INQUIRY was attempted."
