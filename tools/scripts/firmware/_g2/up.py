"""向上遍历调用链：从 target 走到已知命令入口。"""
import sys
from util import INS, owner, dis

KNOWN = {0x020E86: 'SCSI 分派器', 0x020B84: '主循环', 0x025A56: '参数块引擎',
         0x010648: '段1 入口区', 0x011078: '段1 函数'}


def callers(target):
    """返回 (调用地址, 类型, 所属函数)"""
    res = []
    for a, v in INS.items():
        nm = v[1]
        if nm not in ('jsr', 'bsr', 'jmp', 'bra'):
            continue
        for tok in (v[2], v[3]):
            if tok is None:
                continue
            s = str(tok).lstrip('@')
            try:
                if int(s, 16) == target:
                    res.append((a, nm, owner(a)))
            except ValueError:
                pass
    return sorted(set(res))


def walk(target, depth=0, seen=None, maxd=12):
    if seen is None:
        seen = set()
    if depth > maxd or target in seen:
        return
    seen.add(target)
    ind = '  ' * depth
    tag = KNOWN.get(target)
    name = f'  <<{tag}>>' if tag else ''
    print(f'{ind}0x{target:06X}{name}')
    for a, nm, ow in callers(target):
        print(f'{ind}   <- {nm} @0x{a:06X} (in 0x{ow:06X})')
        if ow and ow != target:
            walk(ow, depth + 2, seen, maxd)


if __name__ == '__main__':
    walk(int(sys.argv[1], 16), maxd=int(sys.argv[2]) if len(sys.argv) > 2 else 12)
