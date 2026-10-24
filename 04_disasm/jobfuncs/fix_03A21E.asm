0x03A21E  stm.l     er2-er3, @-sp
0x03A222  stm.l     er4-er6, @-sp
0x03A226  mov.b     r0l, r5l
0x03A228  mov.b     r0h, r1l
0x03A22A  sub.b     r6l, r6l
0x03A22C  mov.b     r5l, r0l
0x03A22E  extu.w    r0
0x03A230  mov.w     #0x000c, e0
0x03A234  mulxu.w   e0, er0
0x03A236  add.l     #0x0003f898, er0
0x03A23C  mov.l     er0, er2
0x03A23E  sub.l     er5, er5
0x03A240  mov.b     r1l, r5l
0x03A242  add.l     #0x0003f908, er5
0x03A248  mov.b     r6l, r3l
0x03A24A  extu.w    r3
0x03A24C  extu.l    er3
0x03A24E  mov.l     er3, er4
0x03A250  shll.l    #2, er4
0x03A252  mov.l     @(0x3f888,er4), er0
0x03A25C  mov.b     @(0x3f90b,er3), r1l
0x03A264  mov.b     r1l, @er0
0x03A266  mov.b     @er5, r0l
0x03A268  extu.w    r0
0x03A26A  mov.l     er2, er1
0x03A26C  add.l     er4, er1
0x03A26E  mov.l     @er1, er1
0x03A272  mov.w     r0, @er1
0x03A274  inc.b     #1, r6l
0x03A276  cmp.b     #0x03, r6l
0x03A278  bcs       0x03a248
0x03A27A  ldm.l     @sp+, er4-er6
0x03A27E  ldm.l     @sp+, er2-er3
0x03A282  rts       
