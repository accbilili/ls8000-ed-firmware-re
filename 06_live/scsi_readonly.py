"""
LS-8000 ED 实机只读工具 —— SCSI 直通层 + Tier 1/2 命令封装

══════════════════════════════════════════════════════════════════════════════
⚠ 安全边界（2026-10-24 21:55 用户指令「不要做对机器有风险的操作」）
   本脚本目前【暂停使用】。任何实机命令都必须先获得用户的再次明确授权。
   本脚本【不含】WRITE BUFFER（0x3B），【不含】任何 E0 机构命令。
   READ BUFFER 只用 mode 2（纯读，不写 flash，不动电机）。
   静态核实结论：真实 ioctl 是 0x190012（结构体为 44 字节 SCSI_PASS_THROUGH），
   不是 IOCTL_SCSISCAN_CMD；且驱动是 32 位，必须在 32 位宿主里跑
   （C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe）。
   本脚本为 64 位 Python，struct 布局与 32 位驱动不兼容 —— 直接使用会失败。
══════════════════════════════════════════════════════════════════════════════

设计原则
--------
1. **自校验**：任何一次 INQUIRY 必须逐字节等于镜像里的已知模板
   `06 80 02 02 1F 00 00 00 "Nikon   LS-8000 ED      1.11"`，否则判为「没打中设备」。
   结构布局、ioctl 码、设备路径全靠这个模板反推，不靠猜。
2. **只读**：仅实现 Tier 1（查询）与 Tier 2（READ BUFFER 读）。
   **不含** WRITE BUFFER（0x3B），也不含任何 E0 机构命令。
3. **可审计**：每次调用都打印 CDB 字节、方向、长度、返回 sense。

用法
----
    python scsi_readonly.py selftest            # 离线自检（不碰设备）
    python scsi_readonly.py enumerate            # 枚举候选设备句柄
    python scsi_readonly.py inq                  # INQUIRY 自校验
    python scsi_readonly.py tier1                # Tier 1 全套只读查询
    python scsi_readonly.py readbuf 0 0x40        # 读 64 B（通路自检）
    python scsi_readonly.py readbuf 0x10000 0x10  # 读 4 KB（与镜像比对）
    python scsi_readonly.py dumpboot 0x10000     # 分块转储引导块
"""

import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import ctypes
import ctypes.wintypes as wt
import os
import struct
import sys
import time

k32 = ctypes.WinDLL('kernel32', use_last_error=True)

# ---- ctypes 声明（必须显式设置，否则句柄判定会出错）----------------------
# 不设 restype 时 CreateFileW 返回值被截断成 32 位整数，
# 与 64 位的 INVALID_HANDLE_VALUE 永不相等 → 失败会被误判为成功。
k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD, ctypes.c_void_p,
                            wt.DWORD, wt.DWORD, wt.HANDLE]
k32.CreateFileW.restype = wt.HANDLE
k32.CloseHandle.argtypes = [wt.HANDLE]
k32.CloseHandle.restype = wt.BOOL
k32.DeviceIoControl.argtypes = [wt.HANDLE, wt.DWORD, ctypes.c_void_p, wt.DWORD,
                                ctypes.c_void_p, wt.DWORD,
                                ctypes.POINTER(wt.DWORD), ctypes.c_void_p]
k32.DeviceIoControl.restype = wt.BOOL

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80
INVALID_HANDLE_VALUE = 0xFFFFFFFFFFFFFFFF

# ---- CTL_CODE -------------------------------------------------------------
def CTL_CODE(devtype, func, method, access):
    return (devtype << 16) | (access << 14) | (func << 2) | method

FILE_ANY_ACCESS = 0
FILE_READ_ACCESS = 1
FILE_WRITE_ACCESS = 2
METHOD_BUFFERED = 0

FILE_DEVICE_SCANNER = 0x19
FILE_DEVICE_SCSI = 0x21

IOCTL_SCSISCAN_CMD = [
    CTL_CODE(FILE_DEVICE_SCANNER, 0x001, METHOD_BUFFERED, FILE_READ_ACCESS),   # 0x194004
    CTL_CODE(FILE_DEVICE_SCANNER, 0x001, METHOD_BUFFERED, FILE_ANY_ACCESS),   # 0x190004
]
IOCTL_SCSI_PASS_THROUGH = CTL_CODE(FILE_DEVICE_SCSI, 0x040, METHOD_BUFFERED,
                                   FILE_READ_ACCESS | FILE_WRITE_ACCESS)
IOCTL_SCSI_MINIPORT = CTL_CODE(FILE_DEVICE_SCSI, 0x004, METHOD_BUFFERED,
                               FILE_READ_ACCESS | FILE_WRITE_ACCESS)

# 已知正确的 INQUIRY 响应（镜像 0x19424 / 0x3E99C 模板，实机 36/36 一致）
# 06 80 02 02 1F 00 00 00 | "Nikon   LS-8000 ED      1.11"（28 字节 ASCII）
INQ_36 = bytes.fromhex('068002021F000000') + b'Nikon   LS-8000 ED      1.11'
assert len(INQ_36) == 36, 'INQ_36 长度应为 36，实际 %d' % len(INQ_36)

DIR_IN = 0x00     # 从设备读
DIR_OUT = 0x01    # 向设备写

# SEND_SCSI_CMD 的 pDataBuffer 偏移在不同 SDK 版本不同，全部试
PDB_OFFSETS = (0x1A, 0x1C, 0x18)


class SendScsiCmd(ctypes.Structure):
    """SEND_SCSI_CMD，**32 位布局**（驱动是 x86，结构体必须按 32 位对齐）。

    注意：pDataBuffer 必须声明为 c_ulong（固定 4 字节）而不是 c_void_p ——
    64 位 Python 下 c_void_p 是 8 字节，会把后续字段整体错位 4 字节。
    目标驱动是 32 位，所以这里强制 4 字节指针。
    """
    _pack_ = 1
    _fields_ = [
        ('cbSize', wt.USHORT),            # 0x00
        ('TimeoutValue', ctypes.c_ubyte),  # 0x02
        ('bDirection', ctypes.c_ubyte),    # 0x03
        ('bCommand', ctypes.c_ubyte),      # 0x04
        ('bCdbLength', ctypes.c_ubyte),    # 0x05
        ('bCdb', ctypes.c_char * 16),      # 0x06
        ('dwDataTransferLength', ctypes.c_ulong),  # 0x16
        ('pDataBuffer', ctypes.c_ulong),   # 0x1A  ← 必须是 4 字节
        ('bSenseInfoLength', ctypes.c_ubyte),      # 0x1E
        ('bHostAdapterNumber', ctypes.c_ubyte),    # 0x1F
        ('wHostAdapterUniqueId', ctypes.c_ushort), # 0x20
        ('bReserved', ctypes.c_ubyte),     # 0x22
    ]


# 0x23 = 35 字节。布局错位会让 ioctl 直接失败，所以这里硬断言。
assert ctypes.sizeof(SendScsiCmd) == 0x23, \
    'SEND_SCSI_CMD 尺寸应为 35，实际 %d（检查 pDataBuffer 是否为 4 字节）' % ctypes.sizeof(SendScsiCmd)


def open_dev(path):
    h = k32.CreateFileW(path, GENERIC_READ | GENERIC_WRITE, 0, None,
                        OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
    if h == INVALID_HANDLE_VALUE:
        return None
    return h


def close_dev(h):
    if h is not None and h != INVALID_HANDLE_VALUE:
        k32.CloseHandle(h)


def ioctl(h, code, inbuf, inlen, outbuf, outlen):
    ret = wt.DWORD(0)
    ok = k32.DeviceIoControl(h, ctypes.c_ulong(code),
                             ctypes.cast(ctypes.pointer(inbuf), ctypes.c_void_p) if inbuf is not None else None,
                             ctypes.c_ulong(inlen),
                             ctypes.cast(ctypes.pointer(outbuf), ctypes.c_void_p) if outbuf is not None else None,
                             ctypes.c_ulong(outlen),
                             ctypes.byref(ret), None)
    return ok, ret.value, ctypes.get_last_error()


def build_cmd(cdb, direction, data_len, data_buf, pdb_off, timeout=30):
    b = bytearray(0x24)
    struct.pack_into('<H', b, 0, 0x23)                 # cbSize
    b[2] = timeout                                     # TimeoutValue
    b[3] = direction
    b[4] = 0                                           # bCommand
    b[5] = len(cdb)
    b[6:6 + len(cdb)] = cdb
    struct.pack_into('<I', b, 0x16, data_len)          # dwDataTransferLength
    struct.pack_into('<I', b, pdb_off, ctypes.addressof(data_buf) if data_buf else 0)
    b[0x1E] = 32                                       # bSenseInfoLength
    return b


def try_scsiscan(h, cdb, data_len, direction):
    """走 IOCTL_SCSISCAN_CMD。返回 (ok, data, 错误码)"""
    for pdb_off in PDB_OFFSETS:
        for code in IOCTL_SCSISCAN_CMD:
            buf = ctypes.create_string_buffer(max(data_len, 1))
            cmdbuf = build_cmd(cdb, direction, data_len, buf, pdb_off)
            raw = (ctypes.c_ubyte * len(cmdbuf)).from_buffer_copy(cmdbuf)
            ok, ret, err = ioctl(h, code, raw, len(cmdbuf), buf, max(data_len, 1))
            if ok:
                return True, buf.raw[:data_len], err
    return False, b'', ctypes.get_last_error()


def try_spti(h, cdb, data_len, direction):
    """走 IOCTL_SCSI_PASS_THROUGH（SCSI_PASS_THROUGH 结构，44 字节）。

    结构偏移（x86，未打包的 SDK 布局）：
      0x00 Length(2) 0x02 ScsiStatus 0x03 PathId 0x04 TargetId 0x05 LunId
      0x06 CdbLength 0x07 SenseInfoLength 0x08 DataIn 0x09 pad(3)
      0x0C DataTransferLength 0x10 TimeOutValue 0x14 DataBuffer
      0x18 SenseInfoOffset 0x1C Cdb[16]
    """
    HDR = 0x2C
    b = bytearray(HDR + 16)
    struct.pack_into('<H', b, 0, HDR + 16)      # Length
    b[2] = 0                                      # ScsiStatus
    b[6] = len(cdb)                               # CdbLength
    b[7] = 32                                     # SenseInfoLength
    b[8] = 1 if direction == DIR_IN else 0        # DataIn
    struct.pack_into('<I', b, 0x0C, data_len)     # DataTransferLength
    struct.pack_into('<I', b, 0x10, 30)          # TimeOutValue
    buf = ctypes.create_string_buffer(max(data_len, 1))
    struct.pack_into('<I', b, 0x14, ctypes.addressof(buf))   # DataBuffer
    struct.pack_into('<I', b, 0x18, 0)           # SenseInfoOffset
    b[0x1C:0x1C + len(cdb)] = cdb
    ok, ret, err = ioctl(h, IOCTL_SCSI_PASS_THROUGH, b, len(b), buf, max(data_len, 1))
    if ok:
        return True, buf.raw[:data_len], err
    return False, b'', err


def scsi_cmd(h, cdb, data_len=0, direction=DIR_IN, prefer='auto'):
    """优先走 scanner 类驱动，失败再试 SPTI。"""
    order = [try_scsiscan, try_spti] if prefer == 'auto' else [prefer]
    last = (False, b'', 0)
    for fn in order:
        ok, data, err = fn(h, cdb, data_len, direction)
        if ok:
            return True, data, err
        last = (ok, data, err)
    return last


# ---- 设备发现 -------------------------------------------------------------
def candidate_paths():
    paths = []
    for i in range(0, 12):
        paths.append(r'\\.\Scsi%d' % i)
    for i in range(0, 12):
        paths.append(r'\\.\Scanner%d' % i)
    for i in range(0, 8):
        paths.append(r'\\.\PhysicalDrive%d' % i)
    return paths


def pnp_scanner_paths():
    r"""向系统问出扫描仪类设备的实例路径（比盲猜 \\.\ScsiN 可靠）。"""
    import subprocess
    ps = (
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; "
        "Get-CimInstance Win32_PnPEntity | "
        "Where-Object { $_.Service -match 'scsiscan|scsi|wia|nikon|usd' -or "
        "$_.Class -match 'Scanner' -or $_.Name -match 'Scanner|Nikon|Coolscan|SBP|1394' } | "
        "ForEach-Object { $_.Name + '|' + $_.Service + '|' + $_.PNPDeviceID }"
    )
    try:
        out = subprocess.run(['powershell', '-NoProfile', '-Command', ps],
                             capture_output=True, text=True,
                             encoding='utf-8', errors='replace', timeout=30).stdout
    except Exception as e:
        print('  PnP 查询失败: %s' % e)
        return []
    rows = []
    for line in out.splitlines():
        if '|' not in line:
            continue
        parts = line.split('|')
        name = parts[0].strip()
        svc = parts[1].strip() if len(parts) > 1 else ''
        pnp = parts[2].strip() if len(parts) > 2 else ''
        rows.append((name, svc, pnp))
    return rows


def pnp_instance_paths():
    """把 PnP 设备 ID 变成可 CreateFile 的 \\??\\ 路径。

    设备 ID 形如 `SBP2\\NIKON___&LS-8000_ED______&LUN0\\0090B54002FFFFFF`，
    对应的文件路径是 `\\\\?\\SBP2\\NIKON...`（把 `&` 保持原样，不要转义）。
    `1394\\`、`USB\\`、`PCI\\` 同理。
    """
    out = []
    for name, svc, pnp in pnp_scanner_paths():
        if not pnp:
            continue
        for pref in ('SBP2\\', '1394\\', 'USB\\', 'PCI\\'):
            if pnp.upper().startswith(pref.upper()):
                out.append('\\\\?\\' + pnp)
                break
    return out


def enumerate_devices():
    print('=== 1. PnP 扫描仪类设备 ===')
    rows = pnp_scanner_paths()
    if not rows:
        print('  （没查到。可能是没插扫描仪，或该机型没归到扫描仪类）')
    for name, svc, pnp in rows:
        print('  %-46s svc=%-14s %s' % (name[:46], svc[:14], pnp[:60]))

    print()
    print('=== 2. 候选设备句柄 ===')
    found = []
    for p in candidate_paths():
        h = open_dev(p)
        if h is not None:
            found.append(p)
            print('  [开] %s' % p)
            close_dev(h)
    if not found:
        print('  没有一个候选路径能打开。')
    return found


def find_device():
    """逐个试 INQUIRY 自校验，返回第一个真正打中扫描仪的 (路径, 句柄)。"""
    paths = candidate_paths() + pnp_instance_paths()
    opened = []
    for p in paths:
        h = open_dev(p)
        if h is not None:
            opened.append((p, h))
        else:
            err = ctypes.get_last_error()
            if err not in (2, 5):
                print('  [??] %s  err=%d' % (p, err))
    if not opened:
        return None, None
    print('  可打开的句柄 %d 个，逐个做 INQUIRY 自校验…' % len(opened))
    for p, h in opened:
        ok, data, msg = self_check(h)
        if ok:
            print('  ★ 命中: %s  (%s)' % (p, msg))
            return p, h
        print('    %-24s 不匹配（%s）' % (p, msg[:40]))
        close_dev(h)
    return None, None


def self_check(h):
    """INQUIRY 必须逐字节等于已知模板，否则不算打中设备。"""
    try:
        ok, data, err = scsi_cmd(h, bytes.fromhex('120000002400'), 36, DIR_IN)
    except Exception as e:
        return False, None, '异常: %s' % e
    if not ok:
        return False, None, 'ioctl 失败 err=%d' % err
    if data[:36] == INQ_36:
        return True, data, '逐字节一致 ★'
    return False, data, '不匹配：%s' % data[:36].hex()


# ---- 命令封装 -------------------------------------------------------------
def cdb_inquiry():
    return bytes.fromhex('120000002400'), 36, DIR_IN


def cdb_tur():
    return bytes.fromhex('000000000000'), 0, DIR_IN


def cdb_request_sense():
    return bytes.fromhex('03000000fc00'), 252, DIR_IN


def cdb_mode_sense(page=0x3F):
    return bytes.fromhex('1a00%02x00fc00' % page), 252, DIR_IN


def cdb_e1_read_status(sub=0, param=0):
    """E1 READ STATUS：CDB[0]=E1 CDB[2]=子功能 CDB[6..8]=24位参数 大端
    （由主机侧构造器 0x100A0260 反推）"""
    return bytes([0xE1, 0x00, sub, 0x00, 0x00,
                  (param >> 16) & 0xFF, (param >> 8) & 0xFF, param & 0xFF, 0x00, 0x00]), 0, DIR_IN


def cdb_read_buffer(offset, length):
    """READ BUFFER(10) mode 2：CDB[1]=0x02 CDB[2]=0
    CDB[3..5]=24位 offset 大端，CDB[6..8]=24位 length 大端，CDB[9]=0"""
    assert length <= 0xFFFF, '单次长度上限 65535（固件按 16 位取长度）'
    return bytes([0x3C, 0x02, 0x00,
                  (offset >> 16) & 0xFF, (offset >> 8) & 0xFF, offset & 0xFF,
                  (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF,
                  0x00]), length, DIR_IN


def sense_key(data):
    """从 REQUEST SENSE 响应里取 sense key / ASC / ASCQ"""
    if not data or len(data) < 14:
        return None
    return {'response_code': data[0] & 0x0F,
            'sense_key': data[2] & 0x0F,
            'asc': data[12], 'ascq': data[13]}


# ---- 命令行 ---------------------------------------------------------------
def cmd_tier1():
    path, h = find_device()
    if h is None:
        print('打不开任何候选设备。先跑 enumerate。')
        return 2
    print('设备: %s' % path)
    ok, data, msg = self_check(h)
    print('INQUIRY 自校验: %s  %s' % ('通过' if ok else '失败', msg))
    if not ok:
        close_dev(h)
        return 3
    for name, (cdb, dlen, d) in [
        ('TEST UNIT READY', cdb_tur()),
        ('REQUEST SENSE', cdb_request_sense()),
        ('MODE SENSE(6) all pages', cdb_mode_sense()),
        ('E1 READ STATUS sub=0', cdb_e1_read_status()),
    ]:
        ok2, d2, err = scsi_cmd(h, cdb, dlen, d)
        print('\n--- %s ---' % name)
        print('  CDB: %s' % ' '.join('%02X' % b for b in cdb))
        if not ok2:
            print('  ioctl 失败 err=%d' % err)
            continue
        if dlen:
            print('  返回 %d B: %s' % (len(d2), d2[:64].hex()))
        sk = sense_key(d2)
        if sk:
            print('  sense: %s' % sk)
    close_dev(h)
    return 0


def cmd_readbuf(offset, length):
    path, h = find_device()
    if h is None:
        print('打不开任何候选设备。')
        return 2
    ok, data, msg = self_check(h)
    print('INQUIRY 自校验: %s  %s' % ('通过' if ok else '失败', msg))
    if not ok:
        close_dev(h)
        return 3
    cdb, dlen, d = cdb_read_buffer(offset, length)
    print('CDB: %s' % ' '.join('%02X' % b for b in cdb))
    t0 = time.time()
    ok2, d2, err = scsi_cmd(h, cdb, dlen, d)
    print('结果: ok=%s  %d B  %.2fs  err=%d' % (ok2, len(d2), time.time() - t0, err))
    if ok2 and d2:
        open('rb_out.bin', 'wb').write(d2)
        print('已写 rb_out.bin  前 64 B: %s' % d2[:64].hex())
    close_dev(h)
    return 0 if ok2 else 4


def cmd_dumpboot(total=0x10000, chunk=0x1000):
    path, h = find_device()
    if h is None:
        print('打不开任何候选设备。')
        return 2
    ok, data, msg = self_check(h)
    print('INQUIRY 自校验: %s  %s' % ('通过' if ok else '失败', msg))
    if not ok:
        close_dev(h)
        return 3
    out = bytearray()
    off = 0
    while off < total:
        n = min(chunk, total - off)
        cdb, dlen, d = cdb_read_buffer(off, n)
        t0 = time.time()
        ok2, d2, err = scsi_cmd(h, cdb, dlen, d)
        if not ok2 or len(d2) < n:
            print('读 0x%06X 失败 ok=%s len=%d err=%d —— 停止，已读 %d B 保留'
                  % (off, ok2, len(d2), err, len(out)))
            break
        out += d2[:n]
        print('  0x%06X–0x%06X  %d B  %.2fs  累计 %d/%d'
              % (off, off + n - 1, n, time.time() - t0, len(out), total))
        off += n
        time.sleep(0.05)
    fn = 'bootblock_dump.bin'
    open(fn, 'wb').write(bytes(out))
    print('已写 %s（%d B）' % (fn, len(out)))
    close_dev(h)
    return 0


def cmd_compare():
    """读 0x10000 起 4 KB，与本地镜像逐字节比对。"""
    path, h = find_device()
    if h is None:
        print('打不开任何候选设备。')
        return 2
    ok, data, msg = self_check(h)
    if not ok:
        print('INQUIRY 自校验失败: %s' % msg)
        close_dev(h)
        return 3
    cdb, dlen, d = cdb_read_buffer(0x10000, 0x1000)
    ok2, d2, err = scsi_cmd(h, cdb, dlen, d)
    if not ok2:
        print('读失败 err=%d' % err)
        close_dev(h)
        return 4
    rom = open(sample('LS8000_111_ROM.bin'), 'rb').read()
    # 固件地址 = 文件偏移 + 0x10000；ROM 本身从 0x10000 开始
    ref = rom[0:0x1000]
    same = (d2[:0x1000] == ref)
    print('读回 4096 B，与镜像前 4096 B 逐字节比较: %s' % ('★完全一致' if same else '不一致'))
    if not same:
        for i in range(min(len(ref), len(d2))):
            if ref[i] != d2[i]:
                print('  首个差异在 +0x%04X: 镜像 %02X vs 读回 %02X' % (i, ref[i], d2[i]))
                break
    close_dev(h)
    return 0 if same else 5


def cmd_selftest():
    """离线自检：验证 CDB 构造函数、INQUIRY 模板与工具自身逻辑。不碰设备。"""
    ok = True
    print('=== 1. INQUIRY 模板与镜像一致性 ===')
    rom = open(sample('LS8000_111_ROM.bin'), 'rb').read()
    for name, off in [('0x19424', 0x19424 - 0x10000), ('0x3E99C', 0x3E99C - 0x10000)]:
        t = rom[off:off + 36]
        same = (t == INQ_36)
        ok &= same
        print('  镜像 %s: %s  %s' % (name, '一致' if same else '不一致', t.hex()))
    print('  期望值: %s' % INQ_36.hex())
    print('  可读文本: %r' % INQ_36[8:].decode('latin1').rstrip())

    print()
    print('=== 2. CDB 构造函数 ===')
    cases = [
        ('INQUIRY', cdb_inquiry(), '12 00 00 00 24 00'),
        ('TEST UNIT READY', cdb_tur(), '00 00 00 00 00 00'),
        ('REQUEST SENSE', cdb_request_sense(), '03 00 00 00 fc 00'),
        ('MODE SENSE(6) page 0x3F', cdb_mode_sense(), '1a 00 3f 00 fc 00'),
        ('E1 READ STATUS sub=0x41 param=0x020304', cdb_e1_read_status(0x41, 0x020304),
         'e1 00 41 00 00 02 03 04 00 00'),
        ('READ BUFFER off=0 len=0x40', cdb_read_buffer(0, 0x40), '3c 02 00 00 00 00 00 00 40 00'),
        ('READ BUFFER off=0x10000 len=0x1000', cdb_read_buffer(0x10000, 0x1000),
         '3c 02 00 01 00 00 00 10 00 00'),
    ]
    for name, (cdb, dlen, d), exp in cases:
        got = ' '.join('%02x' % b for b in cdb)
        good = (got == exp)
        ok &= good
        print('  %-34s %s  %s' % (name, got, 'OK' if good else '★期望 ' + exp))

    print()
    print('=== 3. 长度上限保护 ===')
    try:
        cdb_read_buffer(0, 0x10000)
        print('  ★ 0x10000 未被拦截')
        ok = False
    except AssertionError:
        print('  0x10000 被正确拦截（固件按 16 位取长度）')

    print()
    print('=== 4. SEND_SCSI_CMD 结构布局（必须 35 字节 / 32 位）===')
    print('  sizeof = %d (0x%X)  %s' % (ctypes.sizeof(SendScsiCmd), ctypes.sizeof(SendScsiCmd),
                                        'OK' if ctypes.sizeof(SendScsiCmd) == 0x23 else '★布局错误'))
    for name, _tp in SendScsiCmd._fields_:
        print('    %-22s @0x%02X' % (name, getattr(SendScsiCmd, name).offset))
    print('  候选 pDataBuffer 偏移: %s（经典 SDK 为 0x1A）' % (PDB_OFFSETS,))

    print()
    print('=== 5. ioctl 码 ===')
    for n, c in [('IOCTL_SCSISCAN_CMD(READ_ACCESS)', IOCTL_SCSISCAN_CMD[0]),
                 ('IOCTL_SCSISCAN_CMD(ANY_ACCESS)', IOCTL_SCSISCAN_CMD[1]),
                 ('IOCTL_SCSI_PASS_THROUGH', IOCTL_SCSI_PASS_THROUGH)]:
        print('  %-32s 0x%08X' % (n, c))

    print()
    print('自检结果: %s' % ('全部通过' if ok else '★有失败项'))
    return 0 if ok else 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == 'selftest':
        sys.exit(cmd_selftest())
    elif cmd == 'enumerate':
        enumerate_devices()
    elif cmd == 'inq':
        p, h = find_device()
        if h is None:
            print('打不开任何候选设备。')
            sys.exit(2)
        ok, data, msg = self_check(h)
        print('%s  %s' % ('通过' if ok else '失败', msg))
        if data:
            print('原始: %s' % data.hex())
            print('文本: %s' % data[8:].decode('latin1').rstrip())
        close_dev(h)
    elif cmd == 'tier1':
        sys.exit(cmd_tier1())
    elif cmd == 'readbuf':
        off = int(sys.argv[2], 0)
        ln = int(sys.argv[3], 0)
        sys.exit(cmd_readbuf(off, ln))
    elif cmd == 'compare':
        sys.exit(cmd_compare())
    elif cmd == 'dumpboot':
        tot = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x10000
        ch = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x1000
        sys.exit(cmd_dumpboot(tot, ch))
    else:
        print(__doc__)
        sys.exit(1)
