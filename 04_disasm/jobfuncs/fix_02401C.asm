0x02401C  mov.b     r6l, r0l
0x02401E  extu.w    r0
0x024020  mov.w     #0x0006, e0
0x024024  mulxu.w   e0, er0
0x024026  mov.b     @er5, r1l
0x024028  mov.b     @(0x3e5d8,er0), r0l
0x024030  cmp.b     r0l, r1l
0x024032  bne       0x024058
0x024034  mov.l     @sp, er0
0x024038  mov.b     @er5, r1l
0x02403A  mov.b     r1l, @er0
0x02403C  mov.l     er2, er0
0x02403E  sub.b     r1l, r1l
0x024040  mov.b     r1l, @er0
0x024042  mov.b     r6l, r0l
0x024044  extu.w    r0
0x024046  mov.w     #0x0006, e0
0x02404A  mulxu.w   e0, er0
0x02404C  mov.l     @(0x3e5da,er0), er0
0x024056  bt        0x0240d2
0x024058  mov.b     r6l, r0l
0x02405A  extu.w    r0
0x02405C  mov.w     #0x0006, e0
0x024060  mulxu.w   e0, er0
0x024062  mov.b     @(0x3e5d8,er0), r0l
0x02406A  cmp.b     #0xff, r0l
0x02406C  bne       0x024110
0x024070  sub.b     r6l, r6l
0x024072  mov.b     r6l, r0l
0x024074  extu.w    r0
0x024076  mov.w     #0x0006, e0
0x02407A  mulxu.w   e0, er0
0x02407C  mov.b     @er3, r1l
0x02407E  extu.w    r1
0x024080  mov.w     #0x0024, e1
0x024084  mulxu.w   e1, er1
0x024086  add.l     #0x0003e62c, er1
0x02408C  add.l     er0, er1
0x02408E  sub.l     #0x00000240, er1
0x024094  mov.b     @er5, r0l
0x024096  mov.b     @er1, r1l
0x024098  cmp.b     r1l, r0l
0x02409A  bne       0x0240d6
0x02409C  mov.l     @sp, er0
0x0240A0  mov.b     @er5, r1l
0x0240A2  mov.b     r1l, @er0
0x0240A4  mov.l     er2, er0
0x0240A6  sub.b     r1l, r1l
0x0240A8  mov.b     r1l, @er0
0x0240AA  mov.b     r6l, r0l
0x0240AC  extu.w    r0
0x0240AE  mov.w     #0x0006, e0
0x0240B2  mulxu.w   e0, er0
0x0240B4  mov.b     @er3, r1l
0x0240B6  extu.w    r1
0x0240B8  mov.w     #0x0024, e1
0x0240BC  mulxu.w   e1, er1
0x0240BE  add.l     #0x0003e62c, er1
0x0240C4  add.l     er1, er0
0x0240C6  sub.l     #0x00000240, er0
0x0240CC  mov.l     @(0x2,er0), er0
0x0240D2  jsr       er0
0x0240D4  bt        0x024116
0x0240D6  mov.b     r6l, r0l
0x0240D8  extu.w    r0
0x0240DA  mov.w     #0x0006, e0
0x0240DE  mulxu.w   e0, er0
0x0240E0  mov.b     @er3, r1l
0x0240E2  extu.w    r1
0x0240E4  mov.w     #0x0024, e1
0x0240E8  mulxu.w   e1, er1
0x0240EA  add.l     #0x0003e62c, er1
0x0240F0  add.l     er0, er1
0x0240F2  sub.l     #0x00000240, er1
0x0240F8  mov.b     @er1, r1l
0x0240FA  cmp.b     #0xff, r1l
0x0240FC  bne       0x02410a
0x0240FE  mov.w     #0x0050, r0
0x024102  mov.w     r0, @0x400436
0x024108  bt        0x02414e
0x02410A  inc.b     #1, r6l
0x02410C  jmp       0x024072
0x024110  inc.b     #1, r6l
0x024112  jmp       0x02401c
0x024116  mov.b     @0x4004ff, r0l
0x02411C  beq       0x024126
0x02411E  mov.b     @0x400509, r6l
0x024124  bt        0x02412c
0x024126  mov.b     @(0x1,er4), r6l
0x02412A  and.b     #0xe0, r6l
0x02412C  mov.b     r6l, r6l
0x02412E  beq       0x024134
0x024130  mov.b     #0x7f, r0l
0x024132  bt        0x024136
0x024134  mov.b     #0x06, r0l
0x024136  mov.b     r0l, @0x40052e
0x02413C  mov.b     @(0x4,er4), r6l
0x024140  extu.w    r6
0x024142  mov.l     #0x0040052e, er0
0x024148  mov.w     r6, r1
0x02414A  jsr       0x011900
0x02414E  adds.l    #4, sp
0x024150  adds.l    #4, sp
0x024152  ldm.l     @sp+, er4-er6
0x024156  ldm.l     @sp+, er2-er3
0x02415A  rts       
