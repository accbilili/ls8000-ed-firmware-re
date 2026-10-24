0x02B196  mov.w     r3, @-sp
0x02B198  stm.l     er4-er6, @-sp
0x02B19C  mov.b     r0l, r3l
0x02B19E  mov.l     er1, er4
0x02B1A0  mov.l     #0x00440812, er5
0x02B1A6  mov.b     @0x440811, r6h
0x02B1AC  sub.b     r6l, r6l
0x02B1AE  bt        0x02b1c0
0x02B1B0  mov.b     r6l, r0l
0x02B1B2  extu.w    r0
0x02B1B4  extu.l    er0
0x02B1B6  add.l     er5, er0
0x02B1B8  mov.b     @er0, r0l
0x02B1BA  cmp.b     r3l, r0l
0x02B1BC  beq       0x02b1c4
0x02B1BE  inc.b     #1, r6l
0x02B1C0  cmp.b     r6h, r6l
0x02B1C2  bcs       0x02b1b0
0x02B1C4  sub.l     er0, er0
0x02B1C6  mov.b     r6l, r0l
0x02B1C8  add.l     er0, er4
0x02B1CA  sub.l     er1, er1
0x02B1CC  mov.b     r6h, r1l
0x02B1CE  mov.l     er4, er0
0x02B1D0  jsr       0x01872e
0x02B1D4  mov.l     er1, er4
0x02B1D6  add.l     er4, er5
0x02B1D8  mov.b     @er5, r6l
0x02B1DA  mov.b     r6l, r0l
0x02B1DC  ldm.l     @sp+, er4-er6
0x02B1E0  mov.w     @sp+, r3
0x02B1E2  rts       
