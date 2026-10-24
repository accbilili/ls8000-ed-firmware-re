# -*- coding: utf-8 -*-
"""Build statemachine_27DC4.asm.txt"""
import sys, io
from dis27dc4 import ADDR, OWN, INS, d, BASE, h

OUT = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\firmware\statemachine_27DC4.asm.txt'

# function table: (name, lo, hi, owner_key or None for manual decode)
FUNCS = [
    ('MAIN   0x027DC4  load-step (mode 0/1/2)', 0x27DC4, 0x27F24, '0x27dc4'),
    ('SUB    0x029CD8  travel-limit guard', 0x29CD8, 0x29D2A, '0x29cd8'),
    ('SUB    0x02898C  sensor-B debounce (0xFFFF2F bit6)', 0x2898C, 0x289B4, '0x2898c'),
    ('SUB    0x027A54  status/IRQ report', 0x27A54, 0x27AFA, '0x27a54'),
    ('SUB    0x027F24  post-load hook', 0x27F24, 0x27F44, '0x27f24'),
    ('SUB    0x02ADCE  axis-A move-and-wait', 0x2ADCE, 0x2AE52, '0x2adce'),
    ('SUB    0x02ACE6  axis-A status wait', 0x2ACE6, 0x2AD0A, '0x2ace6'),
    ('SUB    0x02C9E4  axis-B move-and-wait', 0x2C9E4, 0x2CA78, '0x2c9e4'),
    ('SUB    0x02C8E0  axis-B status wait', 0x2C8E0, 0x2C904, '0x2c8e0'),
    ('DEP    0x02CFE0  debounce 0xFFFF55 bit4', 0x2CFE0, 0x2D000, '0x2cfe0'),
    ('DEP    0x02D000  debounce 0xFFFF54 bit2', 0x2D000, 0x2D022, '0x2d000'),
    ('DEP    0x010B56  device-ready sync', 0x10B56, 0x10B80, '0x10b56'),
    ('DEP    0x010BD2  irq-mask disable', 0x10BD2, 0x10BD8, '0x10bd2'),
    ('DEP    0x010BDE  irq-mask save', 0x10BDE, 0x10BE2, '0x10bde'),
    ('DEP    0x010BE2  irq-mask restore', 0x10BE2, 0x10BE4, '0x10be2'),
    ('DEP    0x02A2F6  axis-A primitive', 0x2A2F6, 0x2A320, '0x2a2f6'),
    ('DEP    0x02BE32  axis-B primitive', 0x2BE32, 0x2BE50, '0x2be32'),
    ('DEP    0x02B87C  drive-profile loader', 0x2B87C, 0x2B89C, '0x2b87c'),
    ('DEP    0x02896C  clear 10x34B slot array', 0x2896C, 0x2898C, '0x2896c'),
    ('DEP    0x027F44  CCD/analog init hook', 0x27F44, 0x27F9C, '0x27f44'),
    ('DEP    0x02CF60  debounce 0xFFFF55 bit2', 0x2CF60, 0x2CF92, '0x2cf60'),
    ('DEP    0x02CFA0  debounce 0xFFFF55 bit5', 0x2CFA0, 0x2CFD2, '0x2cfa0'),
    ('DEP    0x02CFC0  debounce 0xFFFF55 bit7', 0x2CFC0, 0x2CFDE, '0x2cfc0'),
    ('DEP    0x02ACBA  axis-A settle', 0x2ACBA, 0x2ACE6, '0x2acba'),
    ('CTX    0x027676  load driver (E0 worker step)', 0x27676, 0x277CE, '0x27676'),
    ('CTX    0x0277CE  state sequencer, state @0x420300', 0x277CE, 0x27930, '0x277ce'),
    ('CTX    0x02753E  E0 worker loop (incl. 0x5000 gate)', 0x2753E, 0x27676, '0x2753e'),
    ('CTX    0x0274BC  E0 worker body (cont. of 0x2740A)', 0x274BC, 0x2753E, '0x274bc'),
]

# hand-decoded region (missing from every CFG): 0x2740A-0x274BC
MANUAL = (0x2740A, 0x274BC)


def raw(pc, sz):
    return ' '.join('%02X' % b for b in d[pc - BASE:pc - BASE + sz])


def emit_manual(f, lo, hi):
    pc = lo
    while pc < hi:
        sz, nm, a1, a2, nxt = h.decode(pc - BASE)
        nxt += BASE            # h.decode returns a *file offset*, not an address
        if nm is None or nxt <= pc or sz > 8:
            f.write('%06X  %-16s .byte 0x%02X\n' % (pc, raw(pc, 2), d[pc - BASE]))
            pc += 2
            continue
        ops = ', '.join(x for x in (a1, a2) if x)
        f.write('%06X  %-16s %-9s %s\n' % (pc, raw(pc, sz), 'bra*' if nm == 'bt' else nm, ops))
        pc = nxt


with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('; ======================================================================\n')
    f.write('; Nikon LS-8000 ED  LS8000_111_ROM.bin  H8/300H\n')
    f.write('; Listing for 0x027DC4 and its reachable call tree\n')
    f.write('; ROM: D:\\DS\\TEST\\LS8000\\LS8000_111_ROM.bin  (addr = file offset + 0x10000)\n')
    f.write('; Decoder: h8dis.py + h8.lst (mtime 2026-10)\n')
    f.write('; NOTE: h8.lst names opcode 0x40xx "bt"; it is BRA. Marked "bra*".\n')
    f.write('; NOTE: "mov.b r0l,r0l / bne" tests Z left over by the callee (MOV never\n')
    f.write(';       touches CCR on H8). Flagged where it matters.\n')
    f.write('; ======================================================================\n')

    for name, lo, hi, ow in FUNCS:
        f.write('\n; ' + '=' * 88 + '\n')
        f.write('; ' + name + '\n; range 0x%06X - 0x%06X' % (lo, hi))
        f.write('  insns=%d\n' % sum(1 for p in ADDR if lo <= p < hi and OWN.get('0x%05x' % p) == ow))
        f.write('; ' + '=' * 88 + '\n')
        if name.startswith('CTX    0x0274BC'):
            f.write('\n; --- 0x2740A-0x274BC: NOT decoded by any CFG (cfg_v4/v5/v6), hand-decoded ---\n')
            emit_manual(f, *MANUAL)
            f.write('\n; --- 0x274BC onwards: from cfg_v4 ---\n')
        for pc in ADDR:
            if pc < lo or pc >= hi:
                continue
            if OWN.get('0x%05x' % pc) != ow:
                continue
            v = INS['0x%05x' % pc]
            sz, nm, a1, a2 = v[0], v[1], v[2], v[3]
            ops = ', '.join(x for x in (a1, a2) if x)
            f.write('%06X  %-16s %-9s %s\n' % (pc, raw(pc, sz), 'bra*' if nm == 'bt' else nm, ops))

print('wrote', OUT)
