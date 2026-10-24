"""裁决 scsiscan.sys 对 ioctl 0x190012 的处理方式（只读）。

问题：三处文档写 METHOD_BUFFERED，live-line 按 CTL_CODE 算术推出 method=2 却称 METHOD_NEITHER。
本脚本直接从驱动反汇编判定：
  1) CTL_CODE 标准算术（DeviceType/Access/Function/Method 四段）
  2) 驱动分派链里 0x190012 对应的处理块
  3) 该块是「直接用用户缓冲(NEITHER/OUT_DIRECT)」还是「ExAllocatePool 拷贝(BUFFERED)」

只读 C:\\Windows\\System32\\DriverStore\\...\\scsiscan.sys；产物写工作区 _verify。
"""
import re, struct, os, sys, json
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
P = r'C:/Windows/System32/DriverStore/FileRepository/sti.inf_amd64_14dc9a213197a8b8/scsiscan.sys'
d = open(P, 'rb').read()
import hashlib
sha = hashlib.sha256(d).hexdigest()

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


def off2rva(off):
    for name, vaddr, vsize, raddr, rsize in secs:
        if raddr <= off < raddr + rsize:
            return vaddr + (off - raddr)
    return None


def rva2off(rva):
    for name, vaddr, vsize, raddr, rsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    return None


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False


def dis(rva, n=60):
    off = rva2off(rva)
    out = []
    for ins in md.disasm(d[off:off + 800], imgbase + rva):
        out.append((ins.address, ins.mnemonic, ins.op_str, ins.size))
        if len(out) >= n:
            break
    return out


report = []
print('=' * 78)
print('scsiscan.sys  只读分析')
print('=' * 78)
print(f'  size   : {len(d)} B')
print(f'  sha256 : {sha}')
print(f'  ImageBase 0x{imgbase:X}  sections={nsec}')
for s in secs:
    print(f'    {s[0]:<10} RVA 0x{s[1]:06X} vsize 0x{s[2]:06X} file 0x{s[3]:06X} rsize 0x{s[4]:06X}')

# ---------- 1) CTL_CODE 标准算术 ----------
print()
print('=' * 78)
print('1) CTL_CODE(DeviceType, Function, Method, Access) 标准算术')
print('=' * 78)
print('  定义 (WDK wdm.h):')
print('    #define CTL_CODE(DeviceType, Function, Method, Access)')
print('        (((DeviceType) << 16) | ((Access) << 14) | ((Function) << 2) | (Method))')
print('    METHOD_BUFFERED=0  METHOD_IN_DIRECT=1  METHOD_OUT_DIRECT=2  METHOD_NEITHER=3')
print('    FILE_ANY_ACCESS=0 FILE_READ_ACCESS=1 FILE_WRITE_ACCESS=2 FILE_READ_WRITE_ACCESS=3')
print()

M = {0: 'METHOD_BUFFERED', 1: 'METHOD_IN_DIRECT', 2: 'METHOD_OUT_DIRECT', 3: 'METHOD_NEITHER'}
A = {0: 'FILE_ANY_ACCESS', 1: 'FILE_READ_ACCESS', 2: 'FILE_WRITE_ACCESS', 3: 'FILE_READ_WRITE_ACCESS'}
CTL = 0x190012
dt = (CTL >> 16) & 0xFFFF
acc = (CTL >> 14) & 3
fn = (CTL >> 2) & 0xF
mth = CTL & 3
print(f'  0x{CTL:06X} 拆解:')
print(f'    DeviceType = 0x{dt:04X} ({dt})')
print(f'    Access     = {acc} ({A[acc]})')
print(f'    Function   = 0x{fn:03X} ({fn})')
print(f'    Method     = {mth} ({M[mth]})')
print()
print('  ★ 关键：Method=2 的标准名称是 **METHOD_OUT_DIRECT**，不是 METHOD_NEITHER。')
print('    METHOD_NEITHER 需要 Method=3（CTL 低 2 位 = 0b11），如 0x190013 / 0x190023。')
print('  ★ 反推：若真是 METHOD_BUFFERED(Method=0)，同 DeviceType/Access/Function 下 CTL 应为')
print(f'    0x{dt:04X}<<16 | {acc}<<14 | {fn}<<2 | 0 = 0x{(dt<<16)|(acc<<14)|(fn<<2):06X}')
print('    → 与实测的 0x190012 不符。')

# 反向：哪些组合能产出 0x190012
print()
print('  穷举：能产出 0x190012 的 (Function, Method, Access) 组合 —— Function/Method/Access 全部唯一解')
sols = []
for f in range(16):
    for mm in range(4):
        for aa in range(4):
            if ((dt << 16) | (aa << 14) | (f << 2) | mm) == CTL:
                sols.append((f, mm, aa))
for f, mm, aa in sols:
    print(f'    Function=0x{f:03X}  Method={mm} ({M[mm]})  Access={aa} ({A[aa]})')
report.append(dict(sha256=sha, size=len(d), ctl=CTL, device_type=dt, access=acc,
                    function=fn, method=mth, method_name=M[mth], sols=sols))

# ---------- 2) 驱动里的 0x190012 位置 ----------
print()
print('=' * 78)
print('2) 驱动内 0x190012 的全部出现位置')
print('=' * 78)
pat = (0x190012).to_bytes(4, 'little')
hits = [m.start() for m in re.finditer(re.escape(pat), d)]
for h in hits:
    r = off2rva(h)
    print(f'  file 0x{h:05X}  RVA 0x{r:05X}  VA 0x{imgbase+r:X}')

# ---------- 3) 分派链 ----------
print()
print('=' * 78)
print('3) 分派链（找 sub ecx, 0x190012 附近的比较链）')
print('=' * 78)
for h in hits:
    r = off2rva(h)
    # 向前找 64 字节内的比较指令起点
    start = r - 48
    seq = dis(start, 40)
    for a, m, o, sz in seq:
        if '0x190012' in o or '0x190012' in hex(0):
            pass
    # 直接打印含 0x190012 的那条及其后
    print(f'--- 上下文 @ RVA 0x{r:05X} ---')
    for a, m, o, sz in dis(r - 40, 30):
        mark = '   <<<< 0x190012' if m == 'sub' and '0x190012' in o else ''
        print(f'  0x{a:016X}  {m:<8} {o}{mark}')
    print()

# ---------- 4) 0x190012 处理块：判定 BUFFERED vs NEITHER ----------
print('=' * 78)
print('4) 0x190012 处理块：判定是「拷入内核池(BUFFERED)」还是「直用用户指针(NEITHER/OUT_DIRECT)」')
print('=' * 78)
# 从 sub ecx,0x190012 的 je 目标开始
for h in hits:
    r = off2rva(h)
    seq = dis(r - 40, 30)
    target = None
    for a, m, o, sz in seq:
        if m == 'sub' and '0x190012' in o:
            # 下一条 je 的目标
            idx = seq.index((a, m, o, sz))
            if idx + 1 < len(seq):
                a2, m2, o2, sz2 = seq[idx + 1]
                if m2 == 'je' or m2 == 'jz':
                    t = int(o2, 16)
                    target = t - imgbase
                    print(f'  0x190012 的 je 目标 = RVA 0x{target:05X}  (VA 0x{t:X})')
    if target is None:
        continue
    blk = dis(target, 90)
    txt = '\n'.join(f'  0x{a:016X}  {m:<8} {o}' for a, m, o, sz in blk)
    print(txt)
    # 判定
    has_alloc = any(m.startswith('call') and 'ExAllocatePool' in o or 'ExAllocatePool' in o for a, m, o, sz in blk)
    has_probe = any('ProbeForRead' in o or 'ProbeForWrite' in o for a, m, o, sz in blk)
    print()
    print(f'  >> 该块 ExAllocatePool 出现: {has_alloc}；ProbeForRead/Write 出现: {has_probe}')
    report.append(dict(target_rva=target, disasm=[(hex(a), m, o) for a, m, o, sz in blk],
                        has_alloc=has_alloc, has_probe=has_probe))

with open(os.path.join(HERE, 'ioctl_verdict.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=1, ensure_ascii=False)
print()
print('产物: ioctl_verdict.json')
