0x02B8EA  stm.l     er4-er6, @-sp
0x02B8EE  mov.w     r0, r6
0x02B8F0  mov.w     e0, r5
0x02B8F2  mov.b     r1l, r4h
0x02B8F4  mov.w     @0x400402, r0
0x02B8FA  cmp.w     #0x0120, r0
0x02B8FE  beq       0x02b95a
0x02B900  mov.w     @0x400402, r0
0x02B906  cmp.w     #0x0121, r0
0x02B90A  beq       0x02b95a
0x02B90C  mov.l     #0x004202e0, er1
0x02B912  mov.w     @er1, r0
0x02B914  cmp.w     r0, r6
0x02B916  beq       0x02b95a
0x02B918  mov.w     @er1, r0
0x02B91A  cmp.w     r0, r6
0x02B91C  bls       0x02b928
0x02B91E  mov.b     #0x01, r4l
0x02B920  mov.w     @er1, r1
0x02B922  sub.w     r1, r6
0x02B924  mov.w     r6, e4
0x02B926  bt        0x02b930
0x02B928  sub.b     r4l, r4l
0x02B92A  mov.w     @er1, r1
0x02B92C  sub.w     r6, r1
0x02B92E  mov.w     r1, e4
0x02B930  mov.b     @0x4202e9, r0l
0x02B936  cmp.b     #0x01, r0l
0x02B938  bne       0x02b942
0x02B93A  mov.b     #0x08, r6l
0x02B93C  mov.w     #0x0258, e6
0x02B940  bt        0x02b948
0x02B942  mov.b     #0x04, r6l
0x02B944  mov.w     #0x0190, e6
0x02B948  mov.w     r6, @-sp
0x02B94A  mov.b     r4h, r0h
0x02B94C  mov.w     r5, e1
0x02B94E  mov.w     e6, r1
0x02B950  mov.w     e4, e0
0x02B952  mov.b     r4l, r0l
0x02B954  bsr       0x02b276
0x02B958  adds.l    #2, sp
0x02B95A  ldm.l     @sp+, er4-er6
0x02B95E  rts       
0x02B960  stm.l     er4-er5, @-sp
0x02B964  mov.b     r0l, r4h
0x02B966  mov.w     e0, e5
0x02B968  mov.b     #0x04, r4l
0x02B96A  mov.w     #0x0190, r5
0x02B96E  mov.w     #0x0014, e4
0x02B972  mov.w     r4, @-sp
0x02B974  sub.b     r0h, r0h
0x02B976  mov.w     e4, e1
0x02B978  mov.w     r5, r1
0x02B97A  mov.w     e5, e0
0x02B97C  mov.b     r4h, r0l
0x02B97E  bsr       0x02b276
0x02B982  adds.l    #2, sp
0x02B984  ldm.l     @sp+, er4-er5
0x02B988  rts       
