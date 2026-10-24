"""精确定位 0x190012 处理块所属函数，并判定 I/O 传输方式。

要点：
1) 用 .pdata（异常目录）得到函数边界 → 找到 0x140008CC2 所在函数
2) 在该函数内查 Irp 字段访问：
   - [rsp+0x08]/[rsi+0x08]  = Irp->MdlAddress      （METHOD_*_DIRECT 会用）
   - [rsi+0x18]             = Irp->AssociatedIrp.SystemBuffer
   - [rsi+0x58]             = Irp->UserBuffer       （METHOD_NEITHER 会用）
   - [rsi+0x40]             = Irp->RequestorMode
3) 判据：
   - 驱动从 SystemBuffer 直接解引用（无 ProbeForRead）→ SystemBuffer 是内核地址
     ⇒ 输入被 I/O Manager 缓冲 ⇒ 不是 METHOD_NEITHER
   - 驱动对结构体内嵌指针自行 MmCreateMdl/MmProbeAndLockPages/MmMapLockedPages
     ⇒ payload 走「驱动自管 MDL 直写用户页」
"""
import struct, os, re, json
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
P = r'C:/Windows/System32/DriverStore/FileRepository/sti.inf_amd64_14dc9a213197a8b8/scsiscan.sys'
d = open(P, 'rb').read()
e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
nsec = struct.unpack_from('<H', d, e_lfanew + 6)[0]
optsz = struct.unpack_from('<H', d, e_lfanew + 20)[0]
magic = struct.unpack_from('<H', d, e_lfanew + 24)[0]
imgbase = struct.unpack_from('<Q', d, e_lfanew + 24 + 24)[0]
secoff = e_lfanew + 24 + optsz
secs = []
for i in range(nsec):
    o = secoff + i * 40
    name = d[o:o+8].rstrip(b'\x00').decode('latin1')
    vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', d, o + 8)
    secs.append((name, vaddr, vsize, raddr, rsize))


def rva2off(rva):
    for n, vaddr, vsize, raddr, rsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    return None


def off2rva(off):
    for n, vaddr, vsize, raddr, rsize in secs:
        if raddr <= off < raddr + rsize:
            return vaddr + (off - raddr)
    return None


# ---- 导入表 ----
imp_rva = None
opt = e_lfanew + 24
dd = opt + (112 if magic == 0x20b else 96)
for i in range(16):
    rva, sz = struct.unpack_from('<II', d, dd + i * 8)
    if rva == 0 and sz == 0:
        continue
    if i == 1:
        imp_rva = rva
iat = {}
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
            api = f'{dll}!ord{v & 0xFFFF}'
        else:
            no = rva2off(v & 0x7FFFFFFF)
            api = d[no + 2:no + 2 + 64].split(b'\x00')[0].decode('latin1')
        iat[imgbase + ft] = api
        t += 8
        ft += 8
    off += 20

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True


def dis(rva, n=400):
    o = rva2off(rva)
    out = []
    for ins in md.disasm(d[o:o + 8000], imgbase + rva):
        out.append((ins.address, ins.mnemonic, ins.op_str, ins.size))
        if len(out) >= n:
            break
    return out


def ann(seq):
    r = []
    for a, m, o, sz in seq:
        extra = ''
        if m == 'call' and 'qword ptr [rip' in o:
            mm = re.search(r'rip ([+-]) (0x[0-9a-f]+)', o)
            if mm:
                disp = int(mm.group(2), 16)
                if mm.group(1) == '-':
                    disp = -disp
                slot = a + sz + disp
                if slot in iat:
                    extra = f'    ; {iat[slot]}'
        r.append(f'0x{a:016X}  {m:<8} {o}{extra}')
    return r


# ---- .pdata 函数边界 ----
pdata = next((s for s in secs if s[0] == '.pdata'), None)
funcs = []
if pdata:
    n, vaddr, vsize, raddr, rsize = pdata
    for i in range(rsize // 12):
        b, e, u = struct.unpack_from('<III', d, raddr + i * 12)
        funcs.append((b, e))
funcs.sort()

TARGET = 0x8CC2
owner = None
for b, e in funcs:
    if b <= TARGET < e:
        owner = (b, e)
        break

print('=' * 78)
print('函数边界（.pdata）')
print('=' * 78)
print(f'  0x190012 处理块 RVA 0x{TARGET:05X} 所属函数: '
      f'RVA 0x{owner[0]:05X} – 0x{owner[1]:05X}  (长度 {owner[1]-owner[0]} B)'
      if owner else '  未找到')

if owner:
    seq = dis(owner[0], 400)
    lines = ann(seq)
    # 截到函数尾
    lines = [l for l in lines if int(l[2:18], 16) < imgbase + owner[1]]
    with open(os.path.join(HERE, 'ioctl_func.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    txt = '\n'.join(lines)

    print()
    print('=' * 78)
    print('Irp 字段访问普查（整个函数）')
    print('=' * 78)
    probes = {
        'Irp->MdlAddress  (+0x08)': r'\[r(si|sp|bx|cx|dx) \+ 0x08\]',
        'Irp->AssociatedIrp.SystemBuffer (+0x18)': r'\[r(si|sp|bx|cx|dx) \+ 0x18\]',
        'Irp->IoStatus.Status (+0x30)': r'\[r(si|sp|bx|cx|dx) \+ 0x30\]',
        'Irp->IoStatus.Information (+0x38)': r'\[r(si|sp|bx|cx|dx) \+ 0x38\]',
        'Irp->RequestorMode (+0x40)': r'\[r(si|sp|bx|cx|dx) \+ 0x40\]',
        'Irp->UserBuffer (+0x58)': r'\[r(si|sp|bx|cx|dx) \+ 0x58\]',
    }
    for label, pat in probes.items():
        hits = [l for l in lines if re.search(pat, l)]
        print(f'  {label:<44} 命中 {len(hits):>3} 次')
        for h in hits[:4]:
            print(f'      {h}')

    print()
    print('=' * 78)
    print('关键 API 使用（整个函数）')
    print('=' * 78)
    for k in ['ProbeForRead', 'ProbeForWrite', 'MmCreateMdl', 'MmProbeAndLockPages',
              'MmMapLockedPages', 'MmUnlockPages', 'IoFreeMdl', 'ExAllocatePool2',
              'IoIs32bitProcess', 'ExFreePool', 'MmBuildMdlForNonPagedPool']:
        hits = [l for l in lines if k in l]
        print(f'  {k:<26} {len(hits):>3} 次')
        for h in hits[:3]:
            print(f'      {h}')

    print()
    print('=' * 78)
    print('关键片段：结构体内嵌指针的 MDL 建立与直写')
    print('=' * 78)
    for i, l in enumerate(lines):
        if 'MmCreateMdl' in l or 'MmProbeAndLockPages' in l or 'MmMapLockedPages' in l:
            for j in range(max(0, i - 5), min(len(lines), i + 4)):
                print('   ', lines[j])
            print('    ---')
