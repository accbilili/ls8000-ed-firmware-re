0x031080  mov.b     @0xffff0c, r3h   ; 23 0c
0x031082  mov.w     @0x400d64, r0   ; 6b 20 00 40 0d 64
0x031088  mov.w     r0, @0x400d6c   ; 6b a0 00 40 0d 6c
0x03108E  mov.w     @0x400d60, r0   ; 6b 20 00 40 0d 60
0x031094  mov.w     r0, @0x400d6a   ; 6b a0 00 40 0d 6a
0x03109A  mov.l     @0x006010, er0   ; 01 00 6b 20 00 00 60 10
0x0310A2  mov.l     er0, @(0x54,sp)   ; 01 00 6f f0 00 54
0x0310A8  mov.l     @0x006014, er0   ; 01 00 6b 20 00 00 60 14
0x0310B0  mov.l     er0, @(0x58,sp)   ; 01 00 6f f0 00 58
0x0310B6  mov.l     @0x006018, er0   ; 01 00 6b 20 00 00 60 18
0x0310BE  mov.l     er0, @(0x5c,sp)   ; 01 00 6f f0 00 5c
0x0310C4  mov.l     @0x00601c, er0   ; 01 00 6b 20 00 00 60 1c
0x0310CC  mov.l     er0, @(0x60,sp)   ; 01 00 6f f0 00 60
0x0310D2  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x0310D8  bne       0x0310fa   ; 46 20
0x0310DA  bt        0x0310f2   ; 40 16
0x0310DC  sub.b     r0l, r0l   ; 18 88
0x0310DE  mov.w     r0, @-sp   ; 6d f0
0x0310E0  mov.l     #0x000186a0, er1   ; 7a 01 00 01 86 a0
0x0310E6  sub.w     r0, r0   ; 19 00
0x0310E8  jsr       0x02adce   ; 5e 02 ad ce
0x0310EC  adds.l    #2, sp   ; 0b 87
0x0310EE  jsr       0x02acba   ; 5e 02 ac ba
0x0310F2  mov.w     @0x4202a2, r0   ; 6b 20 00 42 02 a2
0x0310F8  bne       0x0310dc   ; 46 e2
0x0310FA  mov.b     @0x400d72, r0l   ; 6a 28 00 40 0d 72
0x031100  cmp.b     #0x05, r0l   ; a8 05
0x031102  beq       0x031132   ; 47 2e
0x031104  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x03110A  bne       0x031132   ; 46 26
0x03110C  bt        0x031126   ; 40 18
0x03110E  sub.b     r0l, r0l   ; 18 88
0x031110  mov.w     r0, @-sp   ; 6d f0
0x031112  mov.l     #0x000186a0, er1   ; 7a 01 00 01 86 a0
0x031118  mov.w     #0x00ab, r0   ; 79 00 00 ab
0x03111C  jsr       0x02c9e4   ; 5e 02 c9 e4
0x031120  adds.l    #2, sp   ; 0b 87
0x031122  jsr       0x02c8b4   ; 5e 02 c8 b4
0x031126  mov.w     @0x4202ec, r0   ; 6b 20 00 42 02 ec
0x03112C  cmp.w     #0x00ab, r0   ; 79 20 00 ab
0x031130  bne       0x03110e   ; 46 dc
0x031132  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x031138  cmp.b     #0x03, r0l   ; a8 03
0x03113A  beq       0x031140   ; 47 04
0x03113C  cmp.b     #0x07, r0l   ; a8 07
0x03113E  bne       0x03115a   ; 46 1a
