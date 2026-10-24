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

# LS-8000 ED read-only probe v4 - 32-bit PowerShell
#
# SCOPE: READ ONLY. Only INQUIRY (0x12) is ever attempted. A hit requires
#        byte-exact match with the known 36-byte INQUIRY template.
#        No WRITE BUFFER / READ BUFFER / E0 / mode-5 anything.
#
# v4: struct layout derived from the loaded driver's own send routine
#     (scsiscan.sys 0x140008468):
#       +0x00  dword   (unused by the 32-bit path)
#       +0x04  dword   total struct length  -> must be 0x2C (44) for 32-bit caller
#       +0x08  byte    direction/mode flags -> bit6|bit7 must be set
#       +0x0C  byte    CdbLength            -> 6 (INQUIRY) or 10
#       +0x0D  byte    SenseInfoLength
#       +0x10  dword   DataTransferLength
#       +0x14  byte[16] CDB
#       +0x24  dword   DataBuffer pointer   (32-bit path)
#       +0x28  dword   SenseBuffer pointer  (32-bit path)
#     Flags byte is swept 0x00..0xFF because the driver only tests bit6|bit7.
#
# ASCII-only source on purpose: 32-bit PowerShell reads .ps1 as ANSI/GBK.

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

$INQ36 = [byte[]]@(
 0x06,0x80,0x02,0x02,0x1F,0x00,0x00,0x00,
 0x4E,0x69,0x6B,0x6F,0x6E,0x20,0x20,0x20,0x4C,0x53,0x2D,0x38,0x30,0x30,0x30,
 0x20,0x45,0x44,0x20,0x20,0x20,0x20,0x20,0x20,0x31,0x2E,0x31,0x31)

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

# one INQUIRY attempt. returns @{ok;err;data}
function Try-Inq([IntPtr]$h, [int]$flagByte, [int]$lenField, [int]$headField,
                 [IntPtr]$data, [IntPtr]$sense) {
  $inb = New-Object byte[] 44
  $outb = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(256)
  try {
    Put32 $inb 0     ([uint32]$headField)   # +0x00
    Put32 $inb 4     ([uint32]$lenField)    # +0x04  struct total length
    $inb[8] = [byte]$flagByte               # +0x08  flags
    $inb[0x0C] = 6                          # +0x0C  CdbLength
    $inb[0x0D] = 0                          # +0x0D  SenseInfoLength
    Put32 $inb 0x10 36                      # +0x10  DataTransferLength
    # CDB at +0x14 : INQUIRY page 0 alloc 0x24
    $inb[0x14] = 0x12; $inb[0x15] = 0x00; $inb[0x16] = 0x00
    $inb[0x17] = 0x00; $inb[0x18] = 0x24; $inb[0x19] = 0x00
    PutPtr32 $inb 0x24 $data                 # +0x24 DataBuffer
    PutPtr32 $inb 0x28 $sense                # +0x28 SenseBuffer
    $pin = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(44)
    try {
      [System.Runtime.InteropServices.Marshal]::Copy($inb, 0, $pin, 44)
      $ret = 0
      $ok = [W]::DeviceIoControl($h, [uint32]0x190012, $pin, [uint32]44,
                                $outb, [uint32]256, [ref]$ret, [IntPtr]::Zero)
      if (-not $ok) { return @{ ok=$false; err=[W]::GetLastError(); data=$null } }
      $o = New-Object byte[] 36
      [System.Runtime.InteropServices.Marshal]::Copy($data, $o, 0, 36)
      return @{ ok=$true; err=0; data=$o }
    } finally { [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pin) }
  } finally { [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb) }
}

Write-Host "=== LS-8000 ED read-only probe v4 (INQUIRY only) ==="
Write-Host ("  pointer size {0} bytes" -f [IntPtr]::Size)

$h = [W]::CreateFileA('\\.\Scanner0', [uint32]3221225472, [uint32]0, [IntPtr]::Zero, [uint32]3, [uint32]0x80, [IntPtr]::Zero)
if ($h -eq [W]::INVALID) { Write-Host "open \\.\Scanner0 FAILED err=$([W]::GetLastError())"; exit 1 }
Write-Host "  [OPEN] \\.\Scanner0"

$data = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(256)
$sense = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(64)
$hit = $false
try {
  Write-Host ""
  Write-Host "--- sweep flags byte (user+0x08), len field (user+0x04) ---"
  foreach ($lenField in @(44, 0)) {
    foreach ($headField in @(44, 0)) {
      foreach ($fb in 0..255) {
        $r = Try-Inq $h $fb $lenField $headField $data $sense
        if ($r.ok) {
          $same = $true
          for ($k = 0; $k -lt 36; $k++) { if ($r.data[$k] -ne $INQ36[$k]) { $same = $false; break } }
          if ($same) {
            Write-Host ("  *** HIT *** lenField={0} headField={1} flags=0x{2:X2}" -f $lenField, $headField, $fb)
            Write-Host ("      data: {0}" -f (Hex $r.data 36))
            $hit = $true
            break
          } else {
            Write-Host ("  [OK-but-mismatch] lenField={0} headField={1} flags=0x{2:X2} -> {3}" -f $lenField, $headField, $fb, (Hex $r.data 12))
          }
        } elseif ($r.err -ne 87) {
          Write-Host ("  [err={0}] lenField={1} headField={2} flags=0x{3:X2}" -f $r.err, $lenField, $headField, $fb)
        }
      }
      if ($hit) { break }
    }
    if ($hit) { break }
  }
  if (-not $hit) { Write-Host "  no byte-exact INQUIRY hit in this sweep" }
} finally {
  [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
  [System.Runtime.InteropServices.Marshal]::FreeHGlobal($sense)
  [W]::CloseHandle($h) | Out-Null
}
Write-Host "probe finished. Only INQUIRY was attempted."
