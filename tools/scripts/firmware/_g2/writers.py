"""列出所有写 0x400402 / 0x400404 的指令及其前文上下文（判别常数还是派生值）。"""
from util import dis, owner, INS

WRITES = []
for a, v in INS.items():
    nm, ops = v[1], ' '.join(str(x) for x in v[2:4] if x is not None)
    if nm not in ('mov', 'mov.w', 'mov.b', 'mov.l'):
        continue
    if '@0x400402' in ops or '@0x400404' in ops:
        if ops.startswith('@'):      # 读：@0x400402, r0
            continue
        WRITES.append((a, nm, ops))

WRITES.sort()
for a, nm, ops in WRITES:
    fn = owner(a)
    print(f'\n--- 写点 0x{a:06X}  {nm} {ops}   (函数 0x{fn:06X}) ---')
    rows = [r for r in dis(fn, 500) if r[0] <= a]
    for aa, nnm, oops in rows[-8:]:
        print(f'      0x{aa:06X}  {nnm:<9} {oops}')
