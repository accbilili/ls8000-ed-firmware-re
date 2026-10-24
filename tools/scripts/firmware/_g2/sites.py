"""对 0x0211B6 的每个调用点，回溯 r0 的来源（在函数内向后扫最近写 r0/e0 的指令）。"""
from util import dis, owner

SITES = [0x01750E, 0x0175B8, 0x0215FE, 0x0216D6, 0x021728, 0x022FC0, 0x02381E]


def backtrace(site, fn, depth=40):
    """在 fn..site 区间内找最后一条写 r0/r0l/e0 的指令"""
    rows = dis(fn, 400)
    seq = [r for r in rows if r[0] <= site]
    out = []
    for a, nm, ops in reversed(seq):
        dst = ops.split(',')[0].strip()
        if dst in ('r0', 'r0l', 'e0') and nm not in ('cmp', 'btst', 'tst'):
            out.append((a, nm, ops))
            if len(out) >= depth:
                break
    return list(reversed(out))


for s in SITES:
    fn = owner(s)
    print(f'\n=== 调用点 0x{s:06X}  (函数 0x{fn:06X}) ===')
    for a, nm, ops in dis(fn, 400):
        if a == s:
            break
    # 打印 site 前 12 条
    rows = [r for r in dis(fn, 400) if r[0] <= s][-12:]
    for a, nm, ops in rows:
        mark = ' >>>' if a == s else '    '
        print(f'{mark} 0x{a:06X}  {nm:<9} {ops}')
