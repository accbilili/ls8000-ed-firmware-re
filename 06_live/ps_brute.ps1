# ==========================================================
# !! WARNING — 请勿盲目运行 / DO NOT RUN BLINDLY !!
# ----------------------------------------------------------
# 本脚本会向**真实的** Nikon LS-8000 ED 扫描仪发送原始 DeviceIoControl
# 请求（IEEE-1394 / FireWire 总线）。操作对象是硬件，不是文件。
#
# This script issues raw DeviceIoControl calls to REAL hardware.
#
# 风险等级 Risk level      : 🔴 HIGH (含 0x190024 等宽 ioctl 码，曾致蓝屏)
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

# LS-8000 ED read-only brute-force probe - 32-bit PowerShell
#
# Sends ONLY INQUIRY (0x12). A combination counts as a hit only if the
# response matches the known 36-byte template byte-for-byte.
# No WRITE BUFFER. No E0 mechanism commands.
#
# Sweep: ioctl code x struct family x struct size x length-field value x pointer offset
# ASCII-only source (32-bit PowerShell reads .ps1 as ANSI/GBK).

$ErrorActionPreference = 'Stop'

$src = @'
using System;
using System.Runtime.InteropServices;
public class W {
    public static readonly IntPtr INVALID = new IntPtr(-1);
    [DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Ansi)]
    public static extern IntPtr CreateFileA(string n, uint a, uint s, IntPtr sec, uint d, uint f, IntPtr t);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool DeviceIoControl(IntPtr h, uint code, IntPtr i, uint il,
        IntPtr o, uint ol, out uint r, IntPtr ov);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr h);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern uint GetLastError();
}
'@
Add-Type -TypeDefinition $src -Language CSharp

$INQ36 = [byte[]]@(
 0x06,0x80,0x02,0x02,0x1F,0x00,0x00,0x00,
 0x4E,0x69,0x6B,0x6F,0x6E,0x20,0x20,0x20,0x4C,0x53,0x2D,0x38,0x30,0x30,0x30,
 0x20,0x45,0x44,0x20,0x20,0x20,0x20,0x20,0x20,0x31,0x2E,0x31,0x31)

function Put32([byte[]]$b,[int]$o,[uint32]$v){$b[$o]=[byte]($v -band 0xFF);$b[$o+1]=[byte](($v -shr 8) -band 0xFF);$b[$o+2]=[byte](($v -shr 16) -band 0xFF);$b[$o+3]=[byte](($v -shr 24) -band 0xFF)}
function Put16([byte[]]$b,[int]$o,[uint16]$v){$b[$o]=[byte]($v -band 0xFF);$b[$o+1]=[byte](($v -shr 8) -band 0xFF)}
function PutPtr([byte[]]$b,[int]$o,[IntPtr]$p,[int]$w){$v=[uint64]$p.ToInt64();for($i=0;$i -lt $w;$i++){$b[$o+$i]=[byte](($v -shr (8*$i)) -band 0xFF)}}

$IOCTLS = @([uint32]0x190012,[uint32]0x190004,[uint32]0x194004,[uint32]0x190014,[uint32]0x190024)
# family: 'ssm' = SEND_SCSI_CMD, 'spt' = SCSI_PASS_THROUGH
$FAMS = @('ssm','spt')
$SIZES = 35..56
$LENVALS = @($true,$false)      # length field = struct size, or 0
# (bufOffset, ptrWidth) candidates
$BUFS = @(@(26,4),@(32,8),@(24,8),@(20,4),@(28,8),@(36,8))

Write-Host "=== LS-8000 ED read-only brute force (INQUIRY only) ==="
Write-Host ("  pointer size {0} bytes" -f [IntPtr]::Size)

$paths = @('\\.\Scanner0','\\.\Scanner1','\\.\Scanner2','\\.\Scanner3',
           '\\?\SBP2\NIKON___&LS-8000_ED______&LUN0\0090B54002FFFFFF',
           '\\.\SBP2\NIKON___&LS-8000_ED______&LUN0\0090B54002FFFFFF',
           '\\.\Scsi0','\\.\Scsi1')
$handles = @()
foreach ($p in $paths) {
  $h = [W]::CreateFileA($p, [uint32]3221225472, [uint32]0, [IntPtr]::Zero, [uint32]3, [uint32]0x80, [IntPtr]::Zero)
  if ($h -ne [W]::INVALID) { $handles += ,@($p,$h); Write-Host ("  [OPEN] {0}" -f $p) }
}
if ($handles.Count -eq 0) { Write-Host "no device handle"; exit 1 }

$errHist = @{}
$hit = $null
$tries = 0
foreach ($hv in $handles) {
  $h = $hv[1]
  foreach ($code in $IOCTLS) {
    foreach ($fam in $FAMS) {
      foreach ($sz in $SIZES) {
        foreach ($useLen in $LENVALS) {
          foreach ($bf in $BUFS) {
            $bo = $bf[0]; $pw = $bf[1]
            if (($bo + $pw) -gt $sz) { continue }
            $inb = New-Object byte[] $sz
            # CDB INQUIRY
            $co = if ($fam -eq 'spt' -and $sz -ge 45) { 36 } else { 6 }
            if (($co + 6) -gt $sz) { continue }
            $inb[$co+0]=0x12; $inb[$co+1]=0x00; $inb[$co+2]=0x00
            $inb[$co+3]=0x00; $inb[$co+4]=0x24; $inb[$co+5]=0x00
            if ($fam -eq 'ssm') {
              Put16 $inb 0 $(if ($useLen) { [uint16]$sz } else { [uint16]0 })
              $inb[2]=30; $inb[3]=0; $inb[4]=0; $inb[5]=6
              Put32 $inb 22 36
              PutPtr $inb $bo ([IntPtr]0) $pw     # patched below
            } else {
              Put16 $inb 0 $(if ($useLen) { [uint16]$sz } else { [uint16]0 })
              $inb[5]=6; $inb[6]=0; $inb[7]=1
              Put32 $inb 12 36
              Put32 $inb 16 30
            }
            $outb = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
            $data = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(512)
            $pin  = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($sz)
            try {
              PutPtr $inb $bo ([IntPtr]$data) $pw
              [System.Runtime.InteropServices.Marshal]::Copy($inb,0,$pin,$sz)
              $ret=0
              $ok = [W]::DeviceIoControl($h,$code,$pin,[uint32]$sz,$outb,[uint32]512,[ref]$ret,[IntPtr]::Zero)
              $tries++
              if ($ok) {
                $o = New-Object byte[] 36
                [System.Runtime.InteropServices.Marshal]::Copy($data,$o,0,36)
                $same=$true
                for($k=0;$k -lt 36;$k++){ if($o[$k] -ne $INQ36[$k]){$same=$false;break} }
                if ($same) {
                  Write-Host ("  *** HIT *** path={0} ioctl=0x{1:X8} fam={2} sz={3} len={4} buf={5}/{6}" -f $hv[0],$code,$fam,$sz,$useLen,$bo,$pw)
                  $hit = "$($hv[0]) ioctl=0x$('{0:X8}' -f $code) fam=$fam sz=$sz len=$useLen buf=$bo/$pw"
                  break
                }
                $key = "OK-but-mismatch"
              } else {
                $key = "err=" + [W]::GetLastError()
              }
              if (-not $errHist.ContainsKey($key)) { $errHist[$key] = 0 }
              $errHist[$key]++
            } finally {
              [System.Runtime.InteropServices.Marshal]::FreeHGlobal($pin)
              [System.Runtime.InteropServices.Marshal]::FreeHGlobal($outb)
              [System.Runtime.InteropServices.Marshal]::FreeHGlobal($data)
            }
          }
          if ($hit) { break }
        }
        if ($hit) { break }
      }
      if ($hit) { break }
    }
    if ($hit) { break }
  }
  if ($hit) { break }
}

Write-Host ""
Write-Host ("tries: {0}" -f $tries)
Write-Host "error histogram:"
foreach ($k in $errHist.Keys) { Write-Host ("   {0,-22} {1}" -f $k, $errHist[$k]) }
Write-Host ""
if ($hit) { Write-Host ("HIT: " + $hit) } else { Write-Host "NO HIT" }
foreach ($hv in $handles) { [W]::CloseHandle($hv[1]) | Out-Null }
