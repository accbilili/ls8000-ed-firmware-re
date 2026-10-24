0x0116A0  mov.w     r6, @-sp
0x0116A2  mov.w     @0x400436, r6   <<< 0x400436
0x0116A8  sub.w     r0, r0
0x0116AA  mov.w     r0, @0x400436   <<< 0x400436
0x0116B0  mov.b     @0x400509, r0l
0x0116B6  bne       0x0116d0
0x0116B8  mov.b     @0x400503, r0l
0x0116BE  extu.w    r0
0x0116C0  mov.w     #0x0013, e0
0x0116C4  mulxu.w   e0, er0
0x0116C6  mov.w     r6, r1
0x0116C8  add.l     #0x00400464, er0
0x0116CE  bsr       0x011708
0x0116D0  mov.w     #0x0005, r0
0x0116D4  mulxu.w   r6, er0
0x0116D6  mov.b     @(0x1914a,er0), r0l
0x0116DE  btst      #6, r0l
0x0116E0  bne       0x0116fc
0x0116E2  mov.b     @0x400503, r0l
0x0116E8  extu.w    r0
0x0116EA  mov.w     #0x0013, e0
0x0116EE  mulxu.w   e0, er0
0x0116F0  mov.w     r6, r1
0x0116F2  add.l     #0x00400464, er0
0x0116F8  bsr       0x011882
0x0116FC  sub.b     r0l, r0l
0x0116FE  mov.b     r0l, @0x400505
0x011704  mov.w     @sp+, r6
0x011706  rts       
