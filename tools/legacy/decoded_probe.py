import sys, os, math, collections, re, struct
from capstone import *

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\TEST\LS8000-firmware-REA-20261021-reviewed\firmware.decoded.bin"
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
data = open(SRC, "rb").read()
lines = []
def w(s=""):
    lines.append(str(s)); print(s)

def ent(b):
    if not b: return 0.0
    c = collections.Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

w("=" * 78)
w(f"解压镜像 size={len(data)} (0x{len(data):X})  熵={ent(data):.4f}")
w("=" * 78)
w(f"0x00占比 {data.count(0)/len(data)*100:.2f}%   0xFF占比 {data.count(0xFF)/len(data)*100:.2f}%")

w()
w("-- 头部 64 字节 --")
for i in range(0, 64, 16):
    ch = data[i:i+16]
    w(f"{i:06X}  " + " ".join(f"{b:02x}" for b in ch) + "  " +
      "".join(chr(b) if 32 <= b < 127 else "." for b in ch))

w()
w("-- 头部按大端 DWORD / WORD --")
for i in range(0, 16, 4):
    dw = struct.unpack(">I", data[i:i+4])[0]
    w(f"  +{i:02X}  DWORD={dw:#010x} ({dw})")

w()
w("-- 0x600 重复区验证 --")
same = 0
for i in range(len(data) - 0x10000):
    if data[i] == data[i + 0x10000]:
        same += 1
    else:
        break
w(f"  offset 0 与 0x10000 起连续相同字节数: {same} (0x{same:X})")
# 全文件范围内 0x10000 位移的相同率
if len(data) > 0x10000:
    n = len(data) - 0x10000
    eq = sum(1 for i in range(n) if data[i] == data[i+0x10000])
    w(f"  整段位移 0x10000 的字节相同率: {eq/n*100:.2f}%  (n={n})")

w()
w("-- 分块熵 (每 8KB) --")
for i in range(0, len(data), 8192):
    e = ent(data[i:i+8192])
    w(f"  0x{i:06X}  ent={e:5.3f}  " + "#" * int(e * 8))

w()
w("-- ASCII 字符串 (>=8, 前 60 条) --")
found = [(m.start(), m.group().decode("latin1")) for m in re.finditer(rb"[\x20-\x7e]{8,}", data)]
w(f"  总数 {len(found)}")
for off, s in found[:60]:
    w(f"  0x{off:06X}  {s[:80]}")

w()
w("-- 关键字符串定位 --")
for kw in [b"Nikon", b"LS-8000", b"1.11", b"SCSI", b"SBP", b"Flash", b"flash", b"ROM", b"CCD", b"motor", b"ERROR", b"Error"]:
    hits = [m.start() for m in re.finditer(re.escape(kw), data)]
    if hits:
        w(f"  {kw.decode():<10} {len(hits):>3} 处  前5: {[hex(h) for h in hits[:5]]}")

w()
w("-- H8 特征字节统计 --")
for pat, nm in [(b"\x54\x70", "54 70 (RTS?)"), (b"\x5e", "5E (JSR@16?)"),
                (b"\x7a", "7A (MOV.L@32?)"), (b"\x5a", "5A (JMP@16:24?)")]:
    w(f"  {nm:<22} {data.count(pat):>5} 处")

w()
w("-- 多架构反汇编评分（skipdata）--")
BR = {"b","bl","bx","br","jmp","call","jsr","bra","bsr","ret","rts","rtn","rte","beq","bne",
      "beqz","bnez","jr","jal","jz","jnz"}
cands = [
    (CS_ARCH_ARM, CS_MODE_ARM|CS_MODE_BIG_ENDIAN, "ARM BE"),
    (CS_ARCH_ARM, CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN, "Thumb LE"),
    (CS_ARCH_MIPS, CS_MODE_MIPS32|CS_MODE_BIG_ENDIAN, "MIPS32 BE"),
    (CS_ARCH_X86, CS_MODE_32, "x86-32"),
    (CS_ARCH_SH, CS_MODE_SH4|CS_MODE_BIG_ENDIAN, "SH-4 BE"),
    (CS_ARCH_M68K, CS_MODE_BIG_ENDIAN, "m68k BE"),
]
for arch, mode, name in cands:
    md = Cs(arch, mode); md.skipdata = True; md.detail = False
    valid = skip = br = 0
    for st in (0x600, 0x8000, 0x10600, 0x20000):
        buf = data[st:st+4096]
        for ins in md.disasm(buf, st):
            if ins.id == 0 or ins.mnemonic.startswith(".byte"):
                skip += 1
            else:
                valid += 1
                if ins.mnemonic in BR: br += 1
    tot = valid + skip
    w(f"  {name:<12} valid={valid/tot*100 if tot else 0:5.1f}%  branch={br/valid*100 if valid else 0:4.1f}%")

with open(os.path.join(OUT, "decoded_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n[saved] decoded_probe.txt")
