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

# LS-8000 ED read-only probe - 32-bit PowerShell
#
# Scope: READ ONLY. The only SCSI command sent is INQUIRY (0x12).
#        It must match the known 36-byte template byte-for-byte to count as a hit.
#        No WRITE BUFFER. No E0 mechanism commands.
#
# MUST run under 32-bit PowerShell:
#   C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File ps_probe.ps1
#
# Static facts (see REPORT_live-plan.md):
#   ioctl  = 0x190012 = CTL_CODE(FILE_DEVICE_SCANNER=0x19, 0x004, METHOD_BUFFERED, FILE_ANY_ACCESS)
#   struct = 44-byte SCSI_PASS_THROUGH layout (as NKDSBP2.dll sends it)
#   device path is enumerated at runtime via SetupDi (md3 uses class names 'SCSI'/'USB'/'IEEE1394')
#
# NOTE: ASCII-only source on purpose - 32-bit PowerShell reads .ps1 as ANSI/GBK,
#       so UTF-8 Chinese text would corrupt string quoting.

$ErrorActionPreference = 'Stop'

$src = @'
using System;
using System.Runtime.InteropServices;

public class W {
    public const uint GENERIC_READ  = 0x80000000;
    public const uint GENERIC_WRITE = 0x40000000;
    public const uint OPEN_EXISTING = 3;
    public const uint FILE_ATTRIBUTE_NORMAL = 0x80;
    public static readonly IntPtr INVALID = new IntPtr(-1);

    [StructLayout(LayoutKind.Sequential)]
    public struct SP_DEVINFO_DATA {
        public int cbSize;
        public IntPtr ClassGuid;
        public uint DevInst;
        public IntPtr Reserved;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SCSI_PASS_THROUGH {
        public ushort Length;
        public byte  ScsiStatus;
        public byte  PathId;
        public byte  TargetId;
        public byte  LunId;
        public byte  CdbLength;
        public byte  SenseInfoLength;
        public byte  DataIn;
        public uint  DataTransferLength;
        public uint  TimeOutValue;
        public IntPtr DataBuffer;
        public uint  SenseInfoOffset;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 16)]
        public byte[] Cdb;
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

    [DllImport("setupapi.dll", SetLastError = true, CharSet = CharSet.Ansi)]
    public static extern bool SetupDiGetDeviceRegistryPropertyA(IntPtr set, int index,
        int prop, out uint type, byte[] buf, uint buflen, out uint needed);

    [DllImport("setupapi.dll", SetLastError = true)]
    public static extern bool SetupDiDestroyDeviceInfoList(IntPtr set);

    [DllImport("setupapi.dll", SetLastError = true, CharSet = CharSet.Ansi)]
    public static extern bool SetupDiClassGuidsFromNameA(string name, out Guid[] guids, uint count,
        out uint needed);
}
'@

Add-Type -TypeDefinition $src -Language CSharp

$INQ36 = [byte[]]@(
 0x06,0x80,0x02,0x02,0x1F,0x00,0x00,0x00,
 0x4E,0x69,0x6B,0x6F,0x6E,0x20,0x20,0x20,0x4C,0x53,0x2D,0x38,0x30,0x30,0x30,
 0x20,0x45,0x44,0x20,0x20,0x20,0x20,0x20,0x20,0x31,0x2E,0x31,0x31)

function Hex([byte[]]$b, [int]$n) {
  $m = [Math]::Min($n, $b.Length); $s = ''
  for ($i = 0; $i -lt $m; $i++) { $s += ('{0:X2} ' -f $b[$i]) }
  return $s
}

function Try-Inquiry([IntPtr]$h) {
  $spt = New-Object W+SCSI_PASS_THROUGH
  $spt.Length = 44
  $spt.Cdb = New-Object byte[] 16
  $spt.Cdb[0] = 0x12; $spt.Cdb[1] = 0x00; $spt.Cdb[2] = 0x00
  $spt.Cdb[3] = 0x00; $spt.Cdb[4] = 0x24; $spt.Cdb[5] = 0x00
  $spt.CdbLength = 6
  $spt.DataIn = 1
  $spt.DataTransferLength = 36
  $spt.TimeOutValue = 30
  $spt.SenseInfoLength = 32
  $spt.SenseInfoOffset = 44

  $data = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(256)
  $outb = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(256)
  $inb  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(64)
  try {
    $spt.DataBuffer = $data
    $inSize = [System.Runtime.InteropServices.Marshal]::SizeOf([type]'W+SCSI_PASS_THROUGH')
    [System.Runtime.InteropServices.Marshal]::StructureToPtr($spt, $inb, $false)
    $ret = 0
    $ok = [W]::DeviceIoControl($h, [uint32]0x190012, $inb, [uint32]$inSize,
                              $outb, [uint32]256, [ref]$ret, [IntPtr]::Zero)
    if (-not $ok) {
      return @{ ok = $false; err = [W]::GetLastError(); data = $null; ss = $inSize }
    }
    $o = New-Object byte[] 36
    [System.Runtime.InteropServices.Marshal]::Copy($data, $o, 0, 36)
    return @{ ok = $true; err = 0; data = $o; ss = $inSize }
  } finally {
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($inb)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
  }
}

Write-Host "=== LS-8000 ED read-only probe (INQUIRY only) ==="
Write-Host ("  pointer size: {0} bytes" -f [IntPtr]::Size)
if ([IntPtr]::Size -ne 4) { Write-Warning "not a 32-bit process - struct layout may mismatch" }

$paths = New-Object System.Collections.ArrayList

Write-Host ""
Write-Host "--- 1. SetupDi enumeration ---"

# 已知类 GUID（不依赖 SetupDiClassGuidsFromNameA 的两段式调用）
#   SCSIAdapter = {4d36e96a-e325-11ce-bfc1-08002be10318}
#   Scanner/Image = {4d36e96b-e325-11ce-bfc1-08002be10318}
$classGuids = @(
  '4d36e96a-e325-11ce-bfc1-08002be10318',
  '4d36e96b-e325-11ce-bfc1-08002be10318'
)

$script:devcount = 0
function Scan-Class([Guid]$g) {
  $set = [W]::SetupDiGetClassDevsA([IntPtr]::Zero, $null, [IntPtr]::Zero, 0, [ref]$g)
  if ($set -eq [W]::INVALID) { return }
  $i = 0
  while ($true) {
    $di = New-Object W+SP_DEVINFO_DATA
    $di.cbSize = [System.Runtime.InteropServices.Marshal]::SizeOf([type]'W+SP_DEVINFO_DATA')
    if (-not [W]::SetupDiEnumDeviceInfo($set, $i, [ref]$di)) { break }
    $i++
    $script:devcount++
    Write-Host ("  [dev {0}] instance {1}" -f $i, $di.DevInst)
    foreach ($prop in 0x13, 0x12) {
      $type = 0; $need2 = 0
      $tmp = New-Object byte[] 4
      [W]::SetupDiGetDeviceRegistryPropertyA($set, $di.DevInst, $prop, [ref]$type, $tmp, 4, [ref]$need2) | Out-Null
      if ($need2 -gt 4) {
        $b = New-Object byte[] $need2
        if ([W]::SetupDiGetDeviceRegistryPropertyA($set, $di.DevInst, $prop, [ref]$type, $b, $need2, [ref]$need2)) {
          $s = [System.Text.Encoding]::ASCII.GetString($b, 0, $b.Length - 1)
          if ($s.Length -gt 0) {
            Write-Host ("  [{0}] prop 0x{1:X2}: {2}" -f $g.ToString().Substring(0,8), $prop, $s)
            foreach ($pfx in '\\?\', '\\.\') { $paths.Add($pfx + $s) | Out-Null }
          }
        }
      }
    }
  }
  [W]::SetupDiDestroyDeviceInfoList($set) | Out-Null
}

foreach ($gs in $classGuids) {
  $g = [Guid]$gs
  Write-Host ("  scanning class {0}" -f $gs)
  Scan-Class $g
  Write-Host ("    -> enumerated {0} device(s)" -f $script:devcount)
}

foreach ($s in @('SBP2\NIKON___&LS-8000_ED______&LUN0\0090B54002FFFFFF',
                 '1394\NIKON___&LS-8000_ED______\0090B54002FFFFFF')) {
  foreach ($pfx in '\\?\', '\\.\') { $paths.Add($pfx + $s) | Out-Null }
}
foreach ($i in 0..11) {
  $paths.Add("\\.\Scanner$i") | Out-Null
  $paths.Add("\\.\Scsi$i") | Out-Null
}

$uniq = @{}
foreach ($p in $paths) { $uniq[$p] = 1 }
Write-Host ""
Write-Host ("--- 2. try {0} candidate paths, INQUIRY self-check ---" -f $uniq.Count)

$hit = $null
foreach ($p in $uniq.Keys) {
  $h = [W]::CreateFileA($p, [uint32]3221225472, [uint32]0, [IntPtr]::Zero, 3, 0x80, [IntPtr]::Zero)
  if ($h -eq [W]::INVALID) {
    $e = [W]::GetLastError()
    if ($e -ne 2 -and $e -ne 3 -and $e -ne 5) { Write-Host ("  [??] {0}  err={1}" -f $p, $e) }
    continue
  }
  Write-Host ("  [OPEN] {0}" -f $p)
  $r = Try-Inquiry $h
  if ($r.ok) {
    $same = $true
    if ($r.data.Length -ne 36) { $same = $false }
    else { for ($k = 0; $k -lt 36; $k++) { if ($r.data[$k] -ne $INQ36[$k]) { $same = $false; break } } }
    Write-Host ("    INQUIRY -> {0} B : {1}" -f $r.data.Length, (Hex $r.data 36))
    if ($same) {
      Write-Host "    *** BYTE-EXACT MATCH - HIT ***"
      $hit = $p
      [W]::CloseHandle($h) | Out-Null
      break
    }
    Write-Host "    not a match"
  } else {
    Write-Host ("    ioctl failed err={0}  structsize={1}" -f $r.err, $r.ss)
  }
  [W]::CloseHandle($h) | Out-Null
}

Write-Host ""
if ($hit) {
  Write-Host ("HIT PATH: {0}" -f $hit)
  Write-Host "Next step would be READ BUFFER (still needs explicit authorisation)."
} else {
  Write-Host "NO HIT. Diagnostics:"
  Write-Host "  - 44-byte SCSI_PASS_THROUGH is what the 32-bit NKDSBP2.dll sends"
  Write-Host "  - loaded scsiscan.sys is 64-bit; if all ioctl fail with err=87/50 try 64-bit struct"
}
