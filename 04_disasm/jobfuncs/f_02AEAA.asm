0x02AEAA  mov.l     er3, @-sp
0x02AEAE  stm.l     er4-er6, @-sp
0x02AEB2  mov.l     #0x004202a2, er5
0x02AEB8  sub.b     r0l, r0l
0x02AEBA  mov.b     r0l, @0x4202a8
0x02AEC0  mov.b     #0x01, r0l
0x02AEC2  mov.b     r0l, @0x400d75
0x02AEC8  mov.l     #0x00400408, er4
0x02AECE  mov.w     @0x400410, r0
0x02AED4  bne       0x02aefa
0x02AED6  sub.b     r0l, r0l
0x02AED8  mov.w     r0, @-sp
0x02AEDA  mov.l     #0x000186a0, er1
0x02AEE0  mov.w     @(0x2,er4), r0
0x02AEE4  bsr       0x02adce
0x02AEE8  adds.l    #2, sp
0x02AEEA  bsr       0x02acba
0x02AEEE  mov.w     @er5, r0
0x02AEF0  mov.w     @(0x2,er4), r4
0x02AEF4  cmp.w     r4, r0
0x02AEF6  bne       0x02aec0
0x02AEF8  bt        0x02af5a
0x02AEFA  mov.w     @(0x2,er4), r0
0x02AEFE  cmp.w     #0x43e1, r0
0x02AF02  bls       0x02af0a
0x02AF04  mov.w     #0x43e1, r6
0x02AF08  bt        0x02af0e
0x02AF0A  mov.w     @(0x2,er4), r6
0x02AF0E  mov.w     @er5, r0
0x02AF10  cmp.w     r0, r6
0x02AF12  beq       0x02af62
0x02AF14  mov.w     @er5, r0
0x02AF16  cmp.w     r0, r6
0x02AF18  bls       0x02af24
0x02AF1A  mov.b     #0x01, r4l
0x02AF1C  mov.w     r6, e6
0x02AF1E  mov.w     @er5, r0
0x02AF20  sub.w     r0, e6
0x02AF22  bt        0x02af2a
0x02AF24  sub.b     r4l, r4l
0x02AF26  mov.w     @er5, e6
0x02AF28  sub.w     r6, e6
0x02AF2A  sub.l     er3, er3
0x02AF2C  mov.l     #0x000186a0, er0
0x02AF32  mov.l     er0, @-sp
0x02AF36  mov.l     er3, @-sp
0x02AF3A  sub.b     r0h, r0h
0x02AF3C  mov.w     @0x400410, r1
0x02AF42  mov.w     e6, e0
0x02AF44  mov.b     r4l, r0l
0x02AF46  bsr       0x02a2f6
0x02AF4A  adds.l    #4, sp
0x02AF4C  adds.l    #4, sp
0x02AF4E  bsr       0x02acba
0x02AF52  mov.w     @er5, r0
0x02AF54  cmp.w     r6, r0
0x02AF56  bne       0x02aec0
0x02AF5A  mov.w     @er5, r0
0x02AF5C  mov.w     r0, @0x4202b2
0x02AF62  ldm.l     @sp+, er4-er6
0x02AF66  mov.l     @sp+, er3
0x02AF6A  rts       
