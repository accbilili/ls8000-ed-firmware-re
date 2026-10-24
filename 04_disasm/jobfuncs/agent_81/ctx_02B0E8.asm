0x02B0E8  mov.l     er6, @-sp
0x02B0EC  mov.l     #0x004202b2, er6
0x02B0F2  sub.b     r0l, r0l
0x02B0F4  mov.w     r0, @-sp
0x02B0F6  mov.l     #0x000186a0, er1
0x02B0FC  mov.w     @er6, r0
0x02B0FE  bsr       0x02adce
0x02B102  adds.l    #2, sp
0x02B104  bsr       0x02acba
0x02B108  mov.w     @er6, r0
0x02B10A  mov.w     @0x4202a2, r1
0x02B110  cmp.w     r1, r0
0x02B112  bne       0x02b0f2
0x02B114  mov.l     @sp+, er6
0x02B118  rts       
