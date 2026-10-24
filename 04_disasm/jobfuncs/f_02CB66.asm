0x02CB66  stm.l     er4-er5, @-sp
0x02CB6A  mov.l     #0x004202ec, er5
0x02CB70  mov.l     #0x00400408, er4
0x02CB76  mov.b     #0x01, r0l
0x02CB78  mov.b     r0l, @0x400d75
0x02CB7E  bt        0x02cb98
0x02CB80  sub.b     r0l, r0l
0x02CB82  mov.w     r0, @-sp
0x02CB84  mov.l     #0x000186a0, er1
0x02CB8A  mov.w     @(0x2,er4), r0
0x02CB8E  bsr       0x02c9e4
0x02CB92  adds.l    #2, sp
0x02CB94  bsr       0x02c8b4
0x02CB98  mov.w     @er5, r0
0x02CB9A  mov.w     @(0x2,er4), r1
0x02CB9E  cmp.w     r1, r0
0x02CBA0  bne       0x02cb80
0x02CBA2  mov.w     @er5, r0
0x02CBA4  mov.w     r0, @0x4202fc
0x02CBAA  ldm.l     @sp+, er4-er5
0x02CBAE  rts       
