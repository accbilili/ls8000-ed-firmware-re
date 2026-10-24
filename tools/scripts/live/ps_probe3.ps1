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

# LS-8000 ED read-only probe v3 - 32-bit PowerShell
#
# SCOPE: READ ONLY. The only SCSI command ever attempted is INQUIRY (0x12).
#        No WRITE BUFFER. No READ BUFFER. No E0 mechanism commands.
#        No mode other than INQUIRY. If a hit occurs, nothing on the device
#        is modified: INQUIRY is a pure query.
#
# v3 difference vs v2: the input struct layout is taken directly from the
# loaded 64-bit in-box scsiscan.sys (C:\Windows\System32\DriverStore\
# FileRepository\sti.inf_amd64_14dc9a213197a8b8\scsiscan.sys), whose
# 32-bit-caller path at 0x140008CDC requires:
#   - input length >= 0x2C (44)
#   - user+0x0C = CdbLength   (driver checks == 0x0A or == 0x06)
#   - user+0x0D = SenseInfoLength
#   - user+0x10 = DataTransferLength
#   - user+0x14 = CDB[16]
#   - user+0x24 = 4-byte data buffer pointer   -> internal qword at +0x28
#   - user+0x28 = 4-byte sense buffer pointer  -> internal qword at +0x30
# The same driver also accepts ioctl codes 0x190016 / 0x19001A / 0x19001C /
# 0x190022 (dispatch at 0x140008BA7) - v2 never tried those.
#
# ASCII-only source on purpose: 32-bit PowerShell reads .ps1 as ANSI/GBK.

$ErrorActionPreference = 'Stop'

$src = @'
using System;
using System.Runtime.InteropServices;

public class W {
    public static readonly IntPtr INVALID = new IntPtr(-1);

    [StructLayout(LayoutKind.Sequential)]
    public struct SP_DEVINFO_DATA {
        public int cbSize;
        public IntPtr ClassGuid;
        public uint DevInst;
        public IntPtr Reserved;
    }

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
    [DllImport("setupapi.dll", SetLastError = true, CharSet = CharSet.Ansi)]
    public static extern IntPtr SetupDiGetClassDevsA(IntPtr cls, string enumFilter, IntPtr hwnd,
        int flags, out Guid guid);
    [DllImport("setupapi.dll", SetLastError = true)]
    public static extern bool SetupDiEnumDeviceInfo(IntPtr set, int index, ref SP_DEVINFO_DATA data);
    [DllImport("setupapi.dll", SetLastError = true)]
    public static extern bool SetupDiGetDeviceRegistryPropertyA(IntPtr set, int index,
        int prop, out uint type, byte[] buf, uint buflen, out uint needed);
    [DllImport("setupapi.dll", SetLastError = true)]
    public static extern bool SetupDiDestroyDeviceInfoList(IntPtr set);
}
'@
Add-Type -TypeDefinition $src -Language CSharp

$INQ36 = [byte[]]@(
 0x06,0x80,0x02,0x02,0x1F,0x00,0x00,0x00,
 0x4E,0x69,0x6B,0x6F,0x6E,0x20,0x20,0x20,0x4C,0x53,0x2D,0x38,0x30,0x30,0x30,
 0x20,0x45,0x44,0x20,0x20,0x20,0x20,0x20,0x20,0x31,0x2E,0x31,0x31)

# Driver-derived layouts. All are 32-bit-caller layouts (pointer width 4).
#   sz    : total input length
#   cdb   : CDB offset inside the struct
#   cdbLen: value written at +0x0C (driver compares with 0x0A / 0x06)
#   cdl   : CdbLength flag used when the CDB is copied from struct+0 (value 10)
#   senseLen : value at +0x0D
#   buf   : offset of the 4-byte data buffer pointer
#   sense : offset of the 4-byte sense buffer pointer
$LAYOUTS = @(
  @{ n='DD44_14'; sz=44; cdb=20; cdbLen=6;  senseLen=0;  buf=36; sense=40; slOff=36 },
  @{ n='DD44_14s'; sz=44; cdb=20; cdbLen=6;  senseLen=18; buf=36; sense=40; slOff=36 },
  @{ n='DD44_00'; sz=44; cdb=0;  cdbLen=10; senseLen=0;  buf=36; sense=40; slOff=36 },
  @{ n='DD44_1C'; sz=44; cdb=28; cdbLen=6;  senseLen=0;  buf=36; sense=40; slOff=36 },
  @{ n='DD48_14'; sz=48; cdb=20; cdbLen=6;  senseLen=0;  buf=36; sense=40; slOff=36 }
)
$IOCTLS = @(0x190012, 0x190016, 0x19001A, 0x19001C, 0x190022)

function Hex([byte[]]$b, [int]$n) {
  $m = [Math]::Min($n, $b.Length); $s = ''
  for ($i = 0; $i -lt $m; $i++) { $s += ('{0:X2} ' -f $b[$i]) }
  return $s
}

function Put32([byte[]]$b, [int]$off, [uint32]$v) {
  $b[$off] = [byte]($v -band 0xFF); $b[$off+1] = [byte](($v -shr 8) -band 0xFF)
  $b[$off+2] = [byte](($v -shr 16) -band 0xFF); $b[$off+3] = [byte](($v -shr 24) -band 0xFF)
}
function Put16([byte[]]$b, [int]$off, [uint16]$v) {
  $b[$off] = [byte]($v -band 0xFF); $b[$off+1] = [byte](($v -shr 8) -band 0xFF)
}
function PutPtr32([byte[]]$b, [int]$off, [IntPtr]$p) {
  $v = [uint32]$p.ToInt64()
  $b[$off] = [byte]($v -band 0xFF); $b[$off+1] = [byte](($v -shr 8) -band 0xFF)
  $b[$off+2] = [byte](($v -shr 16) -band 0xFF); $b[$off+3] = [byte](($v -shr 24) -band 0xFF)
}

function Try-Inquiry([IntPtr]$h, $L, [uint32]$code, [IntPtr]$data, [IntPtr]$sense) {
  $inb = New-Object byte[] $L.sz
  $outb = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(256)
  try {
    # CDB: INQUIRY, page 0, alloc 0x24
    $inb[$L.cdb+0] = 0x12; $inb[$L.cdb+1] = 0x00; $inb[$L.cdb+2] = 0x00
    $inb[$L.cdb+3] = 0x00; $inb[$L.cdb+4] = 0x24; $inb[$L.cdb+5] = 0x00
    # length / flags
    Put32 $inb 0 ([uint32]$L.sz)
    $inb[0x0C] = [byte]$L.cdbLen      # CdbLength
    $inb[0x0D] = [byte]$L.senseLen    # SenseInfoLength
    Put32 $inb 0x10 36                # DataTransferLength
    PutPtr32 $inb $L.buf  $data        # data buffer pointer (4 bytes)
    PutPtr32 $inb $L.sense $sense      # sense buffer pointer (4 bytes)
    $pin = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($L.sz)
    try {
      [System.Runtime.InteropServices.Marshal]::Copy($inb, 0, $pin, $L.sz)
      $ret = 0
      $ok = [W]::DeviceIoControl($h, $code, $pin, [uint32]$L.sz,
                                $outb, [uint32]256, [ref]$ret, [IntPtr]::Zero)
      if (-not $ok) { return @{ ok=$false; err=[W]::GetLastError(); data=$null } }
      $o = New-Object byte[] 36
      [System.Runtime.InteropServices.Marshal]::Copy($data, $o, 0, 36)
      return @{ ok=$true; err=0; data=$o; bytes=$ret }
    } finally { [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pin) }
  } finally { [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb) }
}

Write-Host "=== LS-8000 ED read-only probe v3 (INQUIRY only, driver-derived layout) ==="
Write-Host ("  pointer size: {0} bytes   host: {1}" -f [IntPtr]::Size, [System.Environment]::Is64BitProcess)

$paths = New-Object System.Collections.ArrayList
function Scan-Class([string]$gs) {
  $g = [Guid]$gs
  $set = [W]::SetupDiGetClassDevsA([IntPtr]::Zero, $null, [IntPtr]::Zero, 0, [ref]$g)
  if ($set -eq [W]::INVALID) { return }
  $i = 0
  while ($true) {
    $di = New-Object W+SP_DEVINFO_DATA
    $di.cbSize = [System.Runtime.InteropServices.Marshal]::SizeOf([type]'W+SP_DEVINFO_DATA')
    if (-not [W]::SetupDiEnumDeviceInfo($set, $i, [ref]$di)) { break }
    $i++
    foreach ($prop in 0x13, 0x12) {
      $type = 0; $need2 = 0
      $tmp = New-Object byte[] 4
      [W]::SetupDiGetDeviceRegistryPropertyA($set, $di.DevInst, $prop, [ref]$type, $tmp, 4, [ref]$need2) | Out-Null
      if ($need2 -gt 4) {
        $b = New-Object byte[] $need2
        if ([W]::SetupDiGetDeviceRegistryPropertyA($set, $di.DevInst, $prop, [ref]$type, $b, $need2, [ref]$need2)) {
          $s = [System.Text.Encoding]::ASCII.GetString($b, 0, $b.Length - 1)
          if ($s.Length -gt 3) {
            Write-Host ("  prop 0x{0:X2}: {1}" -f $prop, $s)
            foreach ($pfx in '\\?\', '\\.\') { $paths.Add($pfx + $s) | Out-Null }
          }
        }
      }
    }
  }
  [W]::SetupDiDestroyDeviceInfoList($set) | Out-Null
}
Write-Host ""
Write-Host "--- 1. SetupDi class enumeration ---"
Scan-Class '4d36e96a-e325-11ce-bfc1-08002be10318'
Scan-Class '4d36e96b-e325-11ce-bfc1-08002be10318'

foreach ($s in @('SBP2\NIKON___&LS-8000_ED______&LUN0\0090B54002FFFFFF',
                 '1394\NIKON___&LS-8000_ED______\0090B54002FFFFFF')) {
  foreach ($pfx in '\\?\', '\\.\') { $paths.Add($pfx + $s) | Out-Null }
}
for ($i = 0; $i -lt 8; $i++) {
  $paths.Add("\\.\Scanner$i") | Out-Null
  $paths.Add("\\.\Scsi$i") | Out-Null
  $paths.Add("\\.\SBP2$i") | Out-Null
}
$uniq = @{}; foreach ($p in $paths) { $uniq[$p] = 1 }

$stats = @{}
$openPaths = New-Object System.Collections.ArrayList
Write-Host ""
Write-Host ("--- 2. {0} paths x {1} layouts x {2} ioctls ---" -f $uniq.Count, $LAYOUTS.Count, $IOCTLS.Count)
foreach ($p in $uniq.Keys) {
  $h = [W]::CreateFileA($p, [uint32]3221225472, [uint32]0, [IntPtr]::Zero, [uint32]3, [uint32]0x80, [IntPtr]::Zero)
  if ($h -eq [W]::INVALID) { continue }
  $openPaths.Add($p) | Out-Null
  Write-Host ("  [OPEN] {0}" -f $p)
  $data = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(256)
  $sense = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(64)
  try {
    foreach ($L in $LAYOUTS) {
      foreach ($code in $IOCTLS) {
        $r = Try-Inquiry $h $L $code $data $sense
        $key = '{0}/0x{1:X8}' -f $L.n, $code
        if (-not $r.ok) {
          $stats[$key] = 'err=' + $r.err
          continue
        }
        $same = $true
        for ($k = 0; $k -lt 36; $k++) { if ($r.data[$k] -ne $INQ36[$k]) { $same = $false; break } }
        $stats[$key] = 'OK'
        Write-Host ("    {0} / 0x{1:X8} -> {2}" -f $L.n, $code, (Hex $r.data 36))
        if ($same) {
          Write-Host "    *** BYTE-EXACT MATCH - HIT ***"
          Write-Host ("    path={0} layout={1} ioctl=0x{2:X8}" -f $p, $L.n, $code)
        }
      }
    }
  } finally {
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($sense)
    [W]::CloseHandle($h) | Out-Null
  }
}

Write-Host ""
Write-Host "--- 3. result matrix ---"
foreach ($k in ($stats.Keys | Sort-Object)) { Write-Host ("  {0,-22} {1}" -f $k, $stats[$k]) }
Write-Host ""
Write-Host ("openable paths: {0}" -f ($openPaths -join ' | '))
Write-Host "probe finished. Only INQUIRY was attempted."
