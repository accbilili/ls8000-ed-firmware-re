0x03A284  mov.l     er2, @-sp
0x03A288  stm.l     er4-er6, @-sp
0x03A28C  mov.b     r0l, r6h
0x03A28E  mov.b     r0h, r6l
0x03A290  mov.w     e0, e6
0x03A292  cmp.b     #0x02, r6l
0x03A294  bhi       0x03a2ce
0x03A296  sub.l     er5, er5
0x03A298  mov.b     r6l, r5l
0x03A29A  mov.l     er5, er4
0x03A29C  shll.l    #2, er4
0x03A29E  mov.l     @(0x3f914,er4), er0
0x03A2A8  mov.b     @(0x3f90e,er5), r1l
0x03A2B0  mov.b     r1l, @er0
0x03A2B2  mov.w     e6, r0
0x03A2B4  bsr       0x03a334
0x03A2B6  mov.b     r6h, r2l
0x03A2B8  extu.w    r2
0x03A2BA  mov.w     #0x000c, e2
0x03A2BE  mulxu.w   e2, er2
0x03A2C0  add.l     #0x0003f920, er2
0x03A2C6  add.l     er4, er2
0x03A2C8  mov.l     @er2, er2
0x03A2CC  mov.w     r0, @er2
0x03A2CE  ldm.l     @sp+, er4-er6
0x03A2D2  mov.l     @sp+, er2
0x03A2D6  rts       
