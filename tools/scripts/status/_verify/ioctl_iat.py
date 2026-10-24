"""解析 scsiscan.sys 的导入表，把处理块里的 call [rip+X] 解析成真实 API 名，
并追踪 0x190012 的输出回拷路径，判定 I/O 传输方式。

只读 scsiscan.sys。
"""
import struct, os, re, json, hashlib
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


# ---------- 解析导入目录 ----------
imp_rva = None
opt = e_lfanew + 24
dd = opt + (112 if magic == 0x20b else 96)
for i in range(16):
    rva, sz = struct.unpack_from('<II', d, dd + i * 8)
    if rva == 0 and sz == 0:
        continue
    if i == 1:
        imp_rva = rva
if imp_rva is None:
    raise SystemExit('no import dir')

iat = {}   # IAT slot VA -> api name
off = rva2off(imp_rva)
while True:
    olt, ts, fwd, nm, ft = struct.unpack_from('<IIIII', d, off)
    if olt == 0 and nm == 0:
        break
    dll = d[rva2off(nm):rva2off(nm) + 64].split(b'\x00')[0].decode('latin1')
    t = rva2off(olt)
    while True:
        v = struct.unpack_from('<Q', d, t)[0]
        if v == 0:
            break
        if v & (1 << 63):
            ordinal = v & 0xFFFF
            api = f'{dll}!ord{ordinal}'
        else:
            no = rva2off(v & 0x7FFFFFFF)
            api = d[no + 2:no + 2 + 64].split(b'\x00')[0].decode('latin1')
        iat[imgbase + ft] = api
        t += 8
        ft += 8
    off += 20

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True


def dis(rva, n=300):
    o = rva2off(rva)
    out = []
    for ins in md.disasm(d[o:o + 6000], imgbase + rva):
        out.append((ins.address, ins.mnemonic, ins.op_str, ins.size, ins.bytes))
        if len(out) >= n:
            break
    return out


def annotate(seq):
    res = []
    for a, m, o, sz, by in seq:
        extra = ''
        if m == 'call' and 'qword ptr [rip' in o:
            # 目标 = 下一条指令地址 + disp
            tgt = a + sz
            mm = re.search(r'rip ([+-]) (0x[0-9a-f]+)', o)
            if mm:
                disp = int(mm.group(2), 16)
                if mm.group(1) == '-':
                    disp = -disp
                slot = tgt + disp
                if slot in iat:
                    extra = f'    ; {iat[slot]}'
        res.append(f'0x{a:016X}  {m:<8} {o}{extra}')
    return res


print('=' * 78)
print('scsiscan.sys 导入表（IAT 槽位 → API）')
print('=' * 78)
for slot in sorted(iat):
    print(f'  0x{slot:016X}  {iat[slot]}')

print()
print('=' * 78)
print('0x190012 处理块 0x140008CC2（call 已解析为 API 名）')
print('=' * 78)
blk = dis(0x08CC2, 300)
lines = annotate(blk)
with open(os.path.join(HERE, 'ioctl_block_annotated.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
for l in lines:
    print(' ', l)

print()
print('=' * 78)
print('判定')
print('=' * 78)
txt = '\n'.join(lines)
for k in ['ProbeForRead', 'ProbeForWrite', 'IoAllocateMdl', 'MmProbeAndLockPages',
          'MmMapLockedPages', 'MmGetSystemAddressForMdlSafe', 'ExAllocatePool2',
          'memcpy', 'RtlCopyMemory']:
    print(f'  处理块内 {k:<30}: {k in txt}')

# 找 IoStatus.Information 写入（IRP+0x38）与 输出长度
print()
print('  IRP 相对偏移提示：+0x10=StackLocation, +0x18=AssociatedIrp.SystemBuffer/UserBuffer,')
print('                     +0x38=IoStatus.Information, +0x30=IoStatus.Status')
for l in lines:
    if re.search(r'\[rsi \+ 0x(10|18|30|38|58)\]', l) or re.search(r'\[rbx \+ 0x(24|28|30)\]', l):
        print('   ', l)
