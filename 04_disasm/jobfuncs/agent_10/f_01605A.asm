0x01605A  stm.l     er4-er5, @-sp
0x01605E  subs.l    #2, sp
0x016060  mov.l     er0, er5
0x016062  mov.w     r1, r4
0x016064  mov.l     sp, er1
0x016066  extu.l    er4
0x016068  add.l     er4, er5
0x01606A  mov.b     @er5, r0l
0x01606C  mov.b     r0l, @er1
0x01606E  inc.l     #1, er1
0x016070  inc.l     #1, er5
0x016072  mov.b     @er5, r5l
0x016074  mov.b     r5l, @er1
0x016076  mov.w     @sp, r0
0x016078  adds.l    #2, sp
0x01607A  ldm.l     @sp+, er4-er5
0x01607E  rts       
