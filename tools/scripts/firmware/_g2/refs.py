"""扫描全镜像反汇编中对指定 RAM 地址的引用（读/写）。"""
import re
from util import INS, owner

TARGETS = [0x400402, 0x400404]

NUM = re.compile(r'#?0x([0-9a-fA-F]+)|@0x([0-9a-fA-F]+)')


def scan(addr):
    hits = []
    for a, v in INS.items():
        nm = v[1]
        ops = ' '.join(str(x) for x in v[2:4] if x is not None)
        if not ops:
            continue
        for m in NUM.finditer(ops):
            val = int(m.group(1) or m.group(2), 16)
            if val == addr:
                hits.append((a, nm, ops))
    return sorted(hits)


if __name__ == '__main__':
    import sys
    for t in TARGETS:
        print(f'\n===== 引用 0x{t:06X} 的指令 =====')
        for a, nm, ops in scan(t):
            print(f'  0x{a:06X}  {nm:<9} {ops:<28} (owner 0x{owner(a) or 0:06X})')
