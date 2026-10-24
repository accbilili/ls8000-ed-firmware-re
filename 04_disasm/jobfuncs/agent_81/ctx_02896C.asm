0x02896C  mov.w     r6, @-sp
0x02896E  sub.b     r6l, r6l
0x028970  extu.w    r6
0x028972  mov.w     #0x0022, r0
0x028976  mulxu.w   r6, er0
0x028978  sub.b     r1l, r1l
0x02897A  mov.b     r1l, @(0x41ffd4,er0)
0x028982  inc.b     #1, r6l
0x028984  cmp.b     #0x0a, r6l
0x028986  bcs       0x028970
0x028988  mov.w     @sp+, r6
0x02898A  rts       
0x02898C  bclr      #6, @0xffff2f
0x028994  sub.b     r0l, r0l
0x028996  mov.b     r0l, @0x4202ff
0x02899C  bclr      #6, @0xffff2e
0x0289A4  jsr       0x02d000
0x0289A8  mov.b     r0l, r0l
0x0289AA  bne       0x0289b0
0x0289AC  sub.b     r0l, r0l
0x0289AE  rts       
0x0289B0  mov.b     #0x01, r0l
0x0289B2  rts       
