"""F5 复核 7：穷举所有 `mov byte ptr [reg+8], imm8` 且同函数返回 eax=6/10 的 CDB 构造函数。"""
import sys, collections
sys.path.insert(0, r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\cdb')
from core import *
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

ins = sweep(TEXT_LO, TEXT_HI)
byaddr = {i.address: i for i in ins}
order = sorted(byaddr)

def body_of(site, back_lim=0x80, fwd_lim=0x120):
    """回退到最近的 ret/nop 边界作为函数入口，向前走到 ret"""
    idx = order.index(site)
    j = idx; start = None
    while j > 0 and site - order[j] < back_lim:
        p = order[j - 1]
        m = byaddr[p].mnemonic
        if m.startswith('ret') or m in ('nop', 'int3'):
            start = order[j]; break
        j -= 1
    if start is None: start = site
    out = []; a = start
    while a < start + fwd_lim:
        i = byaddr.get(a)
        if i is None: break
        out.append(i)
        if i.mnemonic.startswith('ret'): break
        a += i.size
    return start, out

def ret_imm(body):
    got = []
    for i in body:
        if i.mnemonic == 'mov' and len(i.operands) == 2:
            d, s = i.operands
            if d.type == X86_OP_REG and i.reg_name(d.reg) in ('eax', 'ax') and s.type == X86_OP_IMM:
                got.append((i.address, s.imm))
    return got

hits = []
for i in ins:
    if i.mnemonic != 'mov' or len(i.operands) != 2: continue
    d, s = i.operands
    if d.type != X86_OP_MEM or d.size != 1 or s.type != X86_OP_IMM: continue
    if d.mem.disp != 8: continue
    if d.mem.base == 0 or i.reg_name(d.mem.base) == 'esp': continue
    start, body = body_of(i.address)
    lens = [v for a, v in ret_imm(body) if a > i.address]
    if lens and any(v in (6, 10, 12, 16) for v in lens):
        hits.append((s.imm, i.address, start, sorted(set(lens))))

hits.sort()
print('命中 CDB[0] 构造点 %d 处' % len(hits))
seen = {}
for cdb0, site, start, lens in hits:
    print('  CDB0=0x%02X  site=0x%08X  entry=0x%08X  len=%s' % (cdb0, site, start, lens))
    seen.setdefault(cdb0, []).append((site, start))
print('\n唯一 CDB[0] 值:', sorted('0x%02X' % k for k in seen))
print('\n缺失检查:')
for op in (0x00, 0x03, 0x16, 0x17):
    print('  0x%02X -> %s' % (op, seen.get(op, '未找到')))
