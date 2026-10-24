0x03C1AE  stm.l     er2-er3, @-sp
0x03C1B2  stm.l     er4-er6, @-sp
0x03C1B6  sub.l     #0x00000030, sp
0x03C1BC  mov.b     r0l, r5l
0x03C1BE  mov.l     er1, er3
0x03C1C0  extu.w    r5
0x03C1C2  extu.l    er5
0x03C1C4  mov.l     er5, er4
0x03C1C6  mov.l     er4, er6
0x03C1C8  shll.l    #2, er6
0x03C1CA  add.l     er6, er3
0x03C1CC  mov.l     @er3, er1
0x03C1D0  mov.l     #0x00000020, er0
0x03C1D6  add.l     sp, er0
0x03C1D8  jsr       0x018e68
0x03C1DC  mov.l     @(0x400f32,er6), er1
0x03C1E6  mov.l     er0, @(0x14,sp)
0x03C1EC  mov.l     #0x00000018, er0
0x03C1F2  add.l     sp, er0
