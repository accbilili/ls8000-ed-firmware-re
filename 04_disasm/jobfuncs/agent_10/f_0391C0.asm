0x0391C0  mov.l     er5, @-sp
0x0391C4  jsr       0x036fcc
0x0391C8  mov.b     @0x400daa, r0l
0x0391CE  mov.b     r0l, @0x44903f
0x0391D4  mov.l     #0x00400dab, er5
0x0391DA  mov.l     #0x00449040, er1
0x0391E0  mov.b     @er5, r0l
0x0391E2  mov.b     r0l, @er1
0x0391E4  mov.b     @(0x1,er5), r0l
0x0391E8  mov.b     r0l, @(0x1,er1)
0x0391EC  mov.b     @(0x2,er5), r0l
0x0391F0  mov.b     r0l, @(0x2,er1)
0x0391F4  mov.b     @(0x3,er5), r5l
0x0391F8  mov.b     r5l, @(0x3,er1)
0x0391FC  mov.l     @sp+, er5
0x039200  rts       
