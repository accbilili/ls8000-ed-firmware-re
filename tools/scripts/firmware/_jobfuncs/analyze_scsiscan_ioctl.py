"""分析本地 64 位 in-box scsiscan.sys 对 ioctl 0x190012 的处理（只读）。
目的：给实机验证会话提供「0x190012 的期望输入结构布局」线索，解其 §5.3 矛盾。
"""
import re, struct, sys
import capstone

P = r'C:/Windows/System32/DriverStore/FileRepository/sti.inf_amd64_14dc9a213197a8b8/scsiscan.sys'
d = open(P, 'rb').read()

# --- PE 段表 ---
e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
nsec = struct.unpack_from('<H', d, e_lfanew + 6)[0]
optsz = struct.unpack_from('<H', d, e_lfanew + 20)[0]
magic = struct.unpack_from('<H', d, e_lfanew + 24)[0]
imgbase = struct.unpack_from('<Q', d, e_lfanew + 24 + 24)[0] if magic == 0x20b else struct.unpack_from('<I', d, e_lfanew + 24 + 28)[0]
print(f'PE magic=0x{magic:X} ImageBase=0x{imgbase:X} sections={nsec}')
secoff = e_lfanew + 24 + optsz
secs = []
for i in range(nsec):
    o = secoff + i * 40
    name = d[o:o+8].rstrip(b'\x00').decode('latin1')
    vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', d, o + 8)
    secs.append((name, vaddr, vsize, raddr, rsize))
    print(f'  {name:<10} RVA 0x{vaddr:06X} vsize 0x{vsize:06X}  file 0x{raddr:06X} rsize 0x{rsize:06X}')

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

pat = (0x190012).to_bytes(4, 'little')
hits = [m.start() for m in re.finditer(re.escape(pat), d)]
print('\n0x190012 出现位置:')
for h in hits:
    r = off2rva(h)
    print(f'  file 0x{h:05X}  RVA 0x{r:05X}  所在段: ' +
          next((n for n, v, vs, ra, rs in secs if ra <= h < ra + rs), '?'))

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False

def disasm_at(off, n=40, back=0):
    rva = off2rva(off)
    start = off
    if back:
        start = max(0, off - back)
    code = d[start:start + 400]
    out = []
    for ins in md.disasm(code, imgbase + off2rva(start)):
        out.append((ins.address, ins.mnemonic, ins.op_str, ins.size))
        if len(out) >= n:
            break
    return out

for h in hits:
    r = off2rva(h)
    print(f'\n===== 上下文 @ RVA 0x{r:05X} (file 0x{h:05X}) =====')
    for a, m, o, sz in disasm_at(h, n=30, back=24):
        mark = '  <<<< 0x190012' if a <= imgbase + r < a + sz else ''
        print(f'  0x{a:016X}  {m:<8} {o}{mark}')
