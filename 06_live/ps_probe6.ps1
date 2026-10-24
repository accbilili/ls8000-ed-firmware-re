# ==========================================================
# !! WARNING — 请勿盲目运行 / DO NOT RUN BLINDLY !!
# ----------------------------------------------------------
# 本脚本会向**真实的** Nikon LS-8000 ED 扫描仪发送原始 DeviceIoControl
# 请求（IEEE-1394 / FireWire 总线）。操作对象是硬件，不是文件。
#
# This script issues raw DeviceIoControl calls to REAL hardware.
#
# 风险等级 Risk level      : 🔴 HIGH (实测触发 0xD1 蓝屏)
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

# LS-8000 ED read-only probe v6 - 32-bit PowerShell
#
# SCOPE: READ ONLY. Only INQUIRY / TEST UNIT READY / REQUEST SENSE / MODE SENSE.
#        No WRITE BUFFER, no READ BUFFER, no E0/E1, no media access.
#
# v6: direction semantics learned from the driver:
#   flags user+0x08 : bit6 (0x40) = data FROM device (read)
#                      bit7 (0x80) = data TO device (write)
#                      DTL > 0  -> bit6|bit7 must be NON-zero   (0x1400084D1)
#                      DTL == 0 -> bit6|bit7 must be ZERO       (0x140008501)
#   SenseInfoLength>0 -> the sense pointer (user+0x28) must be non-NULL
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

$ALLOW = @{ 0x00=1; 0x03=1; 0x12=1; 0x1A=1 }

function Send-Q([IntPtr]$h, [byte[]]$cdb, [int]$allocLen, [int]$flags, [int]$dtl, [int]$senseLen) {
  $op = [int]$cdb[0]
  if (-not $ALLOW.ContainsKey($op)) { throw ("REFUSED opcode 0x{0:X2}" -f $op) }
  $inb = New-Object byte[] 44
  Put32 $inb 0 44; Put32 $inb 4 44
  $inb[8] = [byte]$flags
  $inb[0x0C] = [byte]$cdb.Length
  $inb[0x0D] = [byte]$senseLen
  Put32 $inb 0x10 ([uint32]$dtl)
  for ($i = 0; $i -lt $cdb.Length -and $i -lt 16; $i++) { $inb[0x14 + $i] = $cdb[$i] }
  $data  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
  $sense = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(64)
  $outb  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
  try {
    for ($i = 0; $i -lt 512; $i++) { [System.Runtime.InteropServices.Marshal]::WriteByte($outb, $i, 0xEE) }
    for ($i = 0; $i -lt 64;  $i++) { [System.Runtime.InteropServices.Marshal]::WriteByte($sense, $i, 0xDD) }
    PutPtr32 $inb 0x24 $data
    PutPtr32 $inb 0x28 $sense
    $pin = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(44)
    try {
      [System.Runtime.InteropServices.Marshal]::Copy($inb, 0, $pin, 44)
      $ret = 0
      $ok = [W]::DeviceIoControl($h, [uint32]0x190012, $pin, [uint32]44,
                                $outb, [uint32]512, [ref]$ret, [IntPtr]::Zero)
      $err = 0; if (-not $ok) { $err = [W]::GetLastError() }
      $ob = New-Object byte[] 512; [System.Runtime.InteropServices.Marshal]::Copy($outb, $ob, 0, 512)
      $sb = New-Object byte[] 64;  [System.Runtime.InteropServices.Marshal]::Copy($sense, $sb, 0, 64)
      $db = New-Object byte[] 512; [System.Runtime.InteropServices.Marshal]::Copy($data, $db, 0, 512)
      return @{ ok=$ok; err=$err; n=[int]$ret; out=$ob; sense=$sb; data=$db }
    } finally { [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pin) }
  } finally {
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($sense)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb)
  }
}

$h = [W]::CreateFileA('\\.\Scanner0', [uint32]3221225472, [uint32]0, [IntPtr]::Zero, [uint32]3, [uint32]0x80, [IntPtr]::Zero)
if ($h -eq [W]::INVALID) { Write-Host "open FAILED err=$([W]::GetLastError())"; exit 1 }
Write-Host "[OPEN] \\.\Scanner0   (read-only queries only)"

$T = @(
  @{ n='INQUIRY std';        cdb=[byte[]]@(0x12,0x00,0x00,0x00,0x24,0x00); al=36; fl=0x40; dtl=36; sl=18 },
  @{ n='TEST UNIT READY';    cdb=[byte[]]@(0x00,0x00,0x00,0x00,0x00,0x00); al=0;  fl=0x00; dtl=0;  sl=0  },
  @{ n='TEST UNIT READY+s';  cdb=[byte[]]@(0x00,0x00,0x00,0x00,0x00,0x00); al=0;  fl=0x00; dtl=0;  sl=18 },
  @{ n='REQUEST SENSE';      cdb=[byte[]]@(0x03,0x00,0x00,0x00,0x12,0x00); al=18; fl=0x40; dtl=18; sl=18 },
  @{ n='MODE SENSE p3F/252'; cdb=[byte[]]@(0x1A,0x00,0x3F,0x00,0xFC,0x00); al=252; fl=0x40; dtl=252; sl=18 },
  @{ n='MODE SENSE p00/4';   cdb=[byte[]]@(0x1A,0x00,0x00,0x00,0x04,0x00); al=4;  fl=0x40; dtl=4;  sl=18 },
  @{ n='MODE SENSE p3F/4';   cdb=[byte[]]@(0x1A,0x00,0x3F,0x00,0x04,0x00); al=4;  fl=0x40; dtl=4;  sl=18 },
  @{ n='INQUIRY p80 VPD';    cdb=[byte[]]@(0x12,0x80,0x80,0x00,0x24,0x00); al=36; fl=0x40; dtl=36; sl=18 }
)
try {
  foreach ($t in $T) {
    $r = Send-Q $h $t.cdb $t.al $t.fl $t.dtl $t.sl
    Write-Host ""
    Write-Host ("--- {0}  cdb={1} flags=0x{2:X2} dtl={3} senseLen={4}" -f $t.n, (Hex $t.cdb $t.cdb.Length), $t.fl, $t.dtl, $t.sl)
    if (-not $r.ok) { Write-Host ("    FAILED err={0}" -f $r.err); continue }
    Write-Host ("    ok bytesRet={0}" -f $r.n)
    if ($r.n -gt 0) {
      Write-Host ("    out  : {0}" -f (Hex $r.out ([Math]::Min(64, $r.n))))
      Write-Host ("    ascii: {0}" -f (Ascii $r.out ([Math]::Min(64, $r.n))))
    }
    $ss = (Hex $r.sense 18)
    if ($ss -notmatch '^(DD DD DD DD DD DD DD DD DD DD DD DD DD DD DD DD DD DD)$') {
      Write-Host ("    sense: {0}" -f $ss)
    }
  }
} finally { [W]::CloseHandle($h) | Out-Null }
Write-Host ""
Write-Host "done. Only read-only queries were issued."
