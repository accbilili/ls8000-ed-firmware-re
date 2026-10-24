"""续 ioctl_verdict：追踪 0x190012 处理块的输出回拷路径，判定 METHOD。

判据（Windows I/O Manager 语义）：
- METHOD_BUFFERED  → I/O Manager 分配内核缓冲；驱动写 SystemBuffer，
                      返回时 I/O Manager 拷回用户输出缓冲。驱动侧看不到用户指针。
- METHOD_OUT_DIRECT → I/O Manager 探测并锁定用户页；驱动直接写用户缓冲。
- METHOD_NEITHER    → I/O Manager 不探测；驱动必须自己 ProbeForRead/Write。

因此要找的关键证据：
(a) 驱动是否出现 ProbeForRead / ProbeForWrite / MmGetSystemAddressForMdlSafe
(b) 输出数据回写路径：是 memcpy 到用户指针，还是写 IRP 关联缓冲 + 设置 IoStatus.Information
只读 scsiscan.sys。
"""
import re, struct, os, json, hashlib
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
P = r'C:/Windows/System32/DriverStore/FileRepository/sti.inf_amd64_14dc9a213197a8b8/scsiscan.sys'
d = open(P, 'rb').read()

e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
nsec = struct.unpack_from('<H', d, e_lfanew + 6)[0]
optsz = struct.unpack_from('<H', d, e_lfanew + 20)[0]
magic = struct.unpack_from('<H', d, e_lfanew + 24)[0]
imgbase = struct.unpack_from('<Q', d, e_lfanew + 24 + 24)[0] if magic == 0x20b else struct.unpack_from('<I', d, e_lfanew + 24 + 28)[0]
secoff = e_lfanew + 24 + optsz
secs = []
for i in range(nsec):
    o = secoff + i * 40
    name = d[o:o+8].rstrip(b'\x00').decode('latin1')
    vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', d, o + 8)
    secs.append((name, vaddr, vsize, raddr, rsize))

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True


def rva2off(rva):
    for name, vaddr, vsize, raddr, rsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    return None


def off2rva(off):
    for name, vaddr, vsize, raddr, rsize in secs:
        if raddr <= off < raddr + rsize:
            return vaddr + (off - raddr)
    return None


def dis(rva, n=200):
    off = rva2off(rva)
    out = []
    for ins in md.disasm(d[off:off + 4000], imgbase + rva):
        out.append((ins.address, ins.mnemonic, ins.op_str, ins.size))
        if len(out) >= n:
            break
    return out


# 导入表：确认哪些 API 被调用（ProbeForRead/Write、ExAllocatePool、memcpy 等）
print('=' * 78)
print('A) 导入表（按名字找 API）')
print('=' * 78)
# 解析 .idata
idata = next((s for s in secs if s[0] == '.idata'), None)
names = {}
if idata:
    name, vaddr, vsize, raddr, rsize = idata
    # 直接扫 .idata 里的 ASCII 串
    blob = d[raddr:raddr + rsize]
    for m in re.finditer(rb'[A-Za-z_][A-Za-z0-9_@?$]{3,60}\x00', blob):
        s = m.group(0)[:-1].decode('latin1')
        names.setdefault(s, m.start() + raddr)
KEY = ['ProbeForRead', 'ProbeForWrite', 'ExAllocatePool', 'ExAllocatePoolWithTag',
       'MmGetSystemAddressForMdlSafe', 'MmMapLockedPages', 'IoAllocateMdl',
       'RtlCopyMemory', 'memcpy', 'MmProbeAndLockPages', 'IoGetCurrentIrpStackLocation']
for k in KEY:
    found = [n for n in names if k.lower() in n.lower()]
    print(f'  {k:<28} -> {found if found else "未在 .idata 找到"}')

print()
print('=' * 78)
print('B) 0x190012 处理块 0x140008CC2 起，到输出回拷/退出')
print('=' * 78)
blk = dis(0x08CC2, 260)
for a, m, o, sz in blk:
    print(f'  0x{a:016X}  {m:<8} {o}')

print()
print('=' * 78)
print('C) 关键判定')
print('=' * 78)
txt = '\n'.join(f'{m} {o}' for a, m, o, sz in blk)
for k in ['ProbeForRead', 'ProbeForWrite', 'MmGetSystemAddressForMdlSafe', 'MmMapLockedPages']:
    print(f'  处理块内 {k:<32}: {k in txt}')
# 全 .text+.PAGE 段找
allcode = dis(0x1000, 4000)
alltxt = '\n'.join(f'{m} {o}' for a, m, o, sz in allcode)
allcode2 = dis(0x8000, 4000)
alltxt += '\n' + '\n'.join(f'{m} {o}' for a, m, o, sz in allcode2)
print()
for k in ['ProbeForRead', 'ProbeForWrite', 'MmGetSystemAddressForMdlSafe', 'MmMapLockedPages']:
    print(f'  全驱动 {k:<32}: {k in alltxt}')

with open(os.path.join(HERE, 'ioctl_block.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(f'0x{a:016X}  {m:<8} {o}' for a, m, o, sz in blk))
print()
print('产物: ioctl_block.txt')
