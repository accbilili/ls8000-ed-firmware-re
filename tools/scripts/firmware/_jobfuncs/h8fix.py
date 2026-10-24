"""修复 h8tab.py 的潜在 bug 并导出修正版条目。

bug：load_entries 的 else 分支（len(M)==6，即 6 字节 val/mask 的 slot=4 表项）漏赋 vv，
vv 沿用上一条表项的旧值，导致 h8.lst 第 379/388 行两条 10 字节指令
  mov.l @(d:32,ERn),ERm   (010078006b20 ffffff0ffff8)
  mov.l ERm,@(d:32,ERn)   (010078006ba0 ffffff0ffff8)
永远匹配失败 → 反汇编出现 .byte 断点、大段代码漏跟。

修法：重解析 h8.lst，对 len(M)==6 的表项补 vv=(V[2]<<24)|(V[3]<<16)|(V[4]<<8)|V[5]。
只读 D:\，本文件在workspace。
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import TOOLCHAIN_ROOT, sample
import re

def load_entries_fixed(path):
    ent = []
    dropped = []
    for l in open(path, encoding="utf-8", errors="replace"):
        # BUGFIX: 原正则 [0-9a-f]{2,8} 装不下 12 位十六进制（6 字节模式行），整行被跳过
        m = re.match(r"^([0-9a-f]{2,16})\s+([0-9a-f]{2,16})\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)(?:\s+(\S+))?", l)
        if not m:
            continue
        val, mask, skip, name, am1, am2, ot = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5), m.group(6), (m.group(7) or "undefined")
        def hb(s): return [int(s[i:i+2], 16) for i in range(0, len(s), 2)]
        V, M = hb(val), hb(mask)
        if len(M) == 2:
            slot = 0; vm = (M[0] << 8) | M[1]; vv = (V[0] << 8) | V[1]; vm2 = vv2 = 0
        elif len(M) == 4:
            slot = skip + 1; vm = (M[0] << 24) | (M[1] << 16) | (M[2] << 8) | M[3]
            vv = (V[0] << 24) | (V[1] << 16) | (V[2] << 8) | V[3]; vm2 = vv2 = 0
        else:
            # BUGFIX: 原版此处漏赋 vv
            slot = 4; vm = (M[2] << 24) | (M[3] << 16) | (M[4] << 8) | M[5]
            vv = (V[2] << 24) | (V[3] << 16) | (V[4] << 8) | V[5]
            vm2 = (M[0] << 8) | M[1]; vv2 = (V[0] << 8) | V[1]
        extra = 0
        if (am1 in ("abs16", "abs16e", "abs22e", "abs24e") or am2 in ("abs16", "abs16e", "abs22e", "abs24e")) and skip == 0: extra += 1
        if (am1 == "abs32" or am2 == "abs32") and skip == 0: extra += 2
        if am1 in ("imm16", "rel16", "r16d16h", "r32d16h") or am2 in ("imm16", "rel16", "r16d16h", "r32d16h"): extra += 1
        if am1 in ("imm32", "r32d32hh") or am2 in ("imm32", "r32d32hh"): extra += 2
        ent.append(dict(slot=slot, vm=vm, vv=vv, vm2=vm2, vv2=vv2,
                        size=len(V) + 2 * skip + 2 * extra, name=name, am1=am1, am2=am2, ot=ot))
    A = [e for e in ent if e["ot"] != "o"]; B = [e for e in ent if e["ot"] == "o"]
    return A + B

if __name__ == '__main__':
    import sys
    sys.path.insert(0, TOOLCHAIN_ROOT)
    from h8dis import H8
    from h8tab import load_entries
    d = open(sample('LS8000_111_ROM.bin'), 'rb').read()
    BASE = 0x10000
    old = load_entries(sample('h8.lst'))
    new = load_entries_fixed(sample('h8.lst'))
    print(f'条目数: old={len(old)} new={len(new)} (新增 {len(new)-len(old)} 条)')
    h_old = H8(d, old, base=BASE)
    h_new = H8(d, new, base=BASE)
    for a in (0x03A6CE, 0x03A6E6):
        sz, nm, a1, a2, nxt = h_new.decode(a - BASE)
        print(f'0x{a:06X} new: size={sz} {nm} {a1}, {a2} next=0x{nxt+BASE:06X}')
    n_fix = 0
    sites = []
    for off in range(0, len(d) - 10, 2):
        if h_old.decode(off)[1] is None and h_new.decode(off)[1] is not None:
            n_fix += 1
            if len(sites) < 40:
                sites.append(off + BASE)
    print('全镜像 2 字节对齐点上，修复后可解码的位置数:', n_fix)
    print('前 40 个:', [hex(x) for x in sites])
