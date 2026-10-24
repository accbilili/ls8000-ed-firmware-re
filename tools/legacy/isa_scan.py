import sys, os, collections
from capstone import *

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111\.rsrc\0\RCDATA\FIRMDATA"
data = open(SRC, "rb").read()
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"

BRANCH = {"b", "bl", "bx", "br", "jmp", "call", "jsr", "bra", "bsr", "ret", "rts", "rtn", "rte",
          "beq", "bne", "beqz", "bnez", "jr", "jal", "jz", "jnz", "dbra", "dbcc", "bf", "bt",
          "bf.s", "bt.s", "bclr", "bset", "braf", "bsrf", "rts", "rtb", "rte", "rtd"}


def score(arch, mode, name, start, nbytes=4096):
    try:
        md = Cs(arch, mode)
    except Exception as e:
        return None
    md.detail = False
    md.skipdata = True
    buf = data[start:start + nbytes]
    valid = 0
    skipped = 0
    skip_bytes = 0
    consumed = 0
    br = 0
    mnems = collections.Counter()
    for ins in md.disasm(buf, start):
        if ins.id == 0 or ins.mnemonic.startswith(".byte"):
            skipped += 1
            skip_bytes += ins.size
            consumed += ins.size
        else:
            valid += 1
            consumed += ins.size
            mnems[ins.mnemonic] += 1
            if ins.mnemonic in BRANCH:
                br += 1
        if consumed >= nbytes or valid + skipped > 20000:
            break
    tot = valid + skipped
    return {
        "name": name, "valid": valid, "skipped": skipped,
        "valid_ratio": round(valid / tot, 4) if tot else 0,
        "coverage": round(consumed / len(buf), 3) if buf else 0,
        "branch_ratio": round(br / valid, 3) if valid else 0,
        "top": mnems.most_common(6),
    }


cands = [
    (CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN, "ARM LE"),
    (CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_BIG_ENDIAN, "ARM BE"),
    (CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN, "Thumb LE"),
    (CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_BIG_ENDIAN, "MIPS32 BE"),
    (CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN, "MIPS32 LE"),
    (CS_ARCH_X86, CS_MODE_32, "x86-32"),
    (CS_ARCH_SH, CS_MODE_SH4 | CS_MODE_BIG_ENDIAN, "SH-4 BE"),
    (CS_ARCH_SH, CS_MODE_SH4 | CS_MODE_LITTLE_ENDIAN, "SH-4 LE"),
    (CS_ARCH_M68K, CS_MODE_BIG_ENDIAN, "m68k BE"),
    (CS_ARCH_M68K, CS_MODE_M68K_040, "m68k 040"),
]

starts = [0x0, 0x100, 0x1000, 0x4000, 0x8000, 0xC000, 0x10000]
print("=" * 96)
print("多架构评分（skipdata 模式，抽样多个起点，统计有效指令占比）")
print("=" * 96)
best = {}
for arch, mode, name in cands:
    row = []
    fr = []
    for st in starts:
        s = score(arch, mode, name, st)
        if s is None:
            row.append("n/a")
            continue
        row.append(f"{s['valid_ratio']:.2f}/{s['branch_ratio']:.2f}")
        fr.append(s["valid_ratio"])
    avg = sum(fr) / len(fr) if fr else 0
    best[name] = avg
    print(f"{name:<12} " + "  ".join(f"{r:>11}" for r in row) + f"   | 均值 {avg:.3f}")

print()
print("列格式 = 有效指令占比 / 分支指令占比")
print("起点顺序: " + ", ".join(f"0x{s:X}" for s in starts))
print()
print("排序（有效指令占比均值）:")
for k, v in sorted(best.items(), key=lambda x: -x[1]):
    print(f"  {k:<12} {v:.3f}")
