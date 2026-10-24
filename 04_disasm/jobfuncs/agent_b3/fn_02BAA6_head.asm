0x02BAA6  mov.l     er3, @-sp   ; 01 00 6d f3
0x02BAAA  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x02BAAE  mov.b     #0x04, r6h   ; f6 04
0x02BAB0  mov.w     #0x0190, e6   ; 79 0e 01 90
0x02BAB4  mov.l     #0x00440e61, er3   ; 7a 03 00 44 0e 61
0x02BABA  mov.l     #0x004202e6, er4   ; 7a 04 00 42 02 e6
0x02BAC0  mov.l     #0x00440e60, er5   ; 7a 05 00 44 0e 60
0x02BAC6  mov.b     #0x01, r6l   ; fe 01
0x02BAC8  sub.b     r0l, r0l   ; 18 88
0x02BACA  mov.b     r0l, @0x4202e9   ; 6a a8 00 42 02 e9
0x02BAD0  mov.b     #0x01, r0l   ; f8 01
0x02BAD2  mov.b     r0l, @er5   ; 68 d8
0x02BAD4  jsr       0x02cf80   ; 5e 02 cf 80
0x02BAD8  cmp.b     #0x01, r0l   ; a8 01
0x02BADA  bne       0x02bb40   ; 46 64
0x02BADC  mov.b     @er4, r0l   ; 68 48
0x02BADE  beq       0x02bae6   ; 47 06
0x02BAE0  mov.b     @er4, r0l   ; 68 48
0x02BAE2  cmp.b     #0x07, r0l   ; a8 07
0x02BAE4  bne       0x02bb36   ; 46 50
0x02BAE6  mov.b     r6h, r0l   ; 0c 68
0x02BAE8  mov.w     r0, @-sp   ; 6d f0
0x02BAEA  mov.b     r6l, r0h   ; 0c e0
0x02BAEC  mov.w     #0x0003, e1   ; 79 09 00 03
0x02BAF0  mov.w     e6, r1   ; 0d e1
0x02BAF2  mov.w     #0x041a, e0   ; 79 08 04 1a
0x02BAF6  sub.b     r0l, r0l   ; 18 88
0x02BAF8  bsr       0x02b276   ; 5c 00 f7 7a
0x02BAFC  adds.l    #2, sp   ; 0b 87
0x02BAFE  bsr       0x02b858   ; 5c 00 fd 56
