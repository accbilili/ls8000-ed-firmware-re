# fn 0x0185EE (helper_x) : 156 insns
0x018590  mov.l     er0, er0
0x018592  bne       0x0185e4
0x018594  cmp.w     #0x00ff, r3
0x018598  bne       0x0185da
0x01859A  bt        0x0185e4
0x01859C  mov.l     er1, er1
0x01859E  beq       0x0185d0
0x0185A0  bt        0x0185e4
0x0185A2  mov.l     er0, er0
0x0185A4  bne       0x0185b0
0x0185A6  mov.w     r3, r3
0x0185A8  bne       0x0185d0
0x0185AA  mov.l     er1, er1
0x0185AC  bne       0x0185d0
0x0185AE  bt        0x0185e4
0x0185B0  shll.l    er0
0x0185B2  bcs       0x0185ba
0x0185B4  dec.w     #1, r2
0x0185B6  shll.l    er0
0x0185B8  bcc       0x0185b4
0x0185BA  bt        0x018634
0x0185BE  mov.l     er1, er1
0x0185C0  beq       0x0185da
0x0185C2  shll.l    er1
0x0185C4  bcs       0x0185cc
0x0185C6  dec.w     #1, r3
0x0185C8  shll.l    er1
0x0185CA  bcc       0x0185c6
0x0185CC  bt        0x01863a
0x0185D0  sub.l     er0, er0
0x0185D2  shll.w    e5
0x0185D4  rotxr.w   e0
0x0185D6  bt        0x0186fa
0x0185DA  mov.w     #0x00ff, r2
0x0185DE  sub.l     er1, er1
0x0185E0  bt        0x0186e8
0x0185E4  mov.l     #0x7f800001, er0
0x0185EA  bt        0x0186fa
0x0185EE  stm.l     er4-er5, @-sp
0x0185F2  stm.l     er2-er3, @-sp
0x0185F6  mov.l     er1, @-sp
0x0185FA  mov.w     e0, e5
0x0185FC  xor.w     e1, e5
0x0185FE  shll.l    er0
0x018600  mov.w     e0, r4
0x018602  mov.b     r4h, r2l
0x018604  sub.b     r2h, r2h
0x018606  shll.l    #2, er0
0x018608  shll.l    #2, er0
0x01860A  shll.l    #2, er0
0x01860C  shll.l    #2, er0
0x01860E  shll.l    er1
0x018610  mov.w     e1, r4
0x018612  mov.b     r4h, r3l
0x018614  sub.b     r3h, r3h
0x018616  shll.l    #2, er1
0x018618  shll.l    #2, er1
0x01861A  shll.l    #2, er1
0x01861C  shll.l    #2, er1
0x01861E  cmp.w     #0x00ff, r2
0x018622  beq       0x018590
0x018626  cmp.w     #0x00ff, r3
0x01862A  beq       0x01859c
0x01862E  mov.w     r2, r2
0x018630  beq       0x0185a2
0x018634  mov.w     r3, r3
0x018636  beq       0x0185be
0x01863A  sub.w     r3, r2
0x01863C  add.w     #0x007f, r2
0x018640  or.b      #0x01, r0l
0x018642  rotr.l    er0
0x018644  rotxr.l   er1
0x018646  shlr.l    er0
0x018648  sub.b     r5l, r5l
0x01864A  sub.l     er4, er4
0x01864C  mov.b     #0x1a, r5h
0x01864E  bt        0x018658
0x018650  shll.l    er4
0x018652  btst      #0, r5l
0x018654  bne       0x018658
0x018656  bset      #0, r4l
0x018658  shll.l    er0
0x01865A  rotxl.b   r5l
0x01865C  btst      #1, r5l
0x01865E  bne       0x018668
0x018660  sub.l     er1, er0
0x018662  bcc       0x01866e
0x018664  xor.b     #0x01, r5l
0x018666  bt        0x01866e
0x018668  add.l     er1, er0
0x01866A  bcc       0x01866e
0x01866C  xor.b     #0x01, r5l
0x01866E  dec.b     #1, r5h
0x018670  bne       0x018650
0x018672  and.b     #0x01, r5l
0x018674  beq       0x018678
0x018676  add.l     er1, er0
0x018678  mov.l     er4, er1
0x01867A  shll.l    er1
0x01867C  xor.b     #0x01, r5l
0x01867E  or.b      r5l, r1l
0x018680  shll.l    #2, er1
0x018682  shll.l    #2, er1
0x018684  shll.l    #2, er1
0x018686  mov.l     er0, er0
0x018688  beq       0x01868c
0x01868A  or.b      #0x20, r1l
0x01868C  mov.w     e1, r5
0x01868E  btst      #7, r5h
0x018690  bne       0x018696
0x018692  shll.l    er1
0x018694  dec.w     #1, r2
0x018696  cmp.w     #0x00ff, r2
0x01869A  bge       0x0185da
0x01869E  cmp.w     #0xffe9, r2
0x0186A2  bmi       0x0185d0
0x0186A6  mov.w     r2, r2
0x0186A8  bgt       0x0186d0
0x0186AA  shlr.l    er1
0x0186AC  bcc       0x0186b0
0x0186AE  bset      #0, r1l
0x0186B0  mov.w     r2, r2
0x0186B2  bpl       0x0186b8
0x0186B4  inc.w     #1, r2
0x0186B6  bt        0x0186aa
0x0186B8  btst      #7, r1l
0x0186BA  beq       0x0186ce
0x0186BC  mov.w     r1, r5
0x0186BE  and.w     #0x017f, r5
0x0186C2  beq       0x0186ce
0x0186C4  add.l     #0x00000100, er1
0x0186CA  bpl       0x0186ce
0x0186CC  inc.w     #1, r2
0x0186CE  bt        0x0186e8
0x0186D0  btst      #7, r1l
0x0186D2  beq       0x0186e8
0x0186D4  mov.w     r1, r5
0x0186D6  and.w     #0x017f, r5
0x0186DA  beq       0x0186e8
0x0186DC  add.l     #0x00000100, er1
0x0186E2  bcc       0x0186e8
0x0186E4  rotxr.l   er1
0x0186E6  inc.w     #1, r2
0x0186E8  shll.l    er1
0x0186EA  mov.w     e1, r5
0x0186EC  mov.b     r5l, r0h
0x0186EE  mov.b     r1h, r0l
0x0186F0  mov.b     r5h, r5l
0x0186F2  mov.b     r2l, r5h
0x0186F4  mov.w     r5, e0
0x0186F6  shll.w    e5
0x0186F8  rotxr.l   er0
0x0186FA  mov.l     @sp+, er1
0x0186FE  ldm.l     @sp+, er2-er3
0x018702  ldm.l     @sp+, er4-er5
0x018706  rts       
