0x02CE44  mov.l     #0x004202fc, er6
0x02CE4A  bt        0x02ce62
0x02CE4C  sub.b     r0l, r0l
0x02CE4E  mov.w     r0, @-sp
0x02CE50  mov.l     #0x000186a0, er1
0x02CE56  mov.w     @er6, r0
0x02CE58  bsr       0x02c9e4
0x02CE5C  adds.l    #2, sp
0x02CE5E  bsr       0x02c8b4
0x02CE62  mov.w     @0x4202ec, r0
0x02CE68  mov.w     @er6, r1
0x02CE6A  cmp.w     r1, r0
0x02CE6C  bne       0x02ce4c
0x02CE6E  mov.l     @sp+, er6
0x02CE72  rts       
