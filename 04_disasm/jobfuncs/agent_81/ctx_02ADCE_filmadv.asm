0x02ADCE  mov.l     er3, @-sp
0x02ADD2  stm.l     er4-er6, @-sp
0x02ADD6  mov.w     r0, r5
0x02ADD8  mov.l     er1, er3
0x02ADDA  mov.l     #0x00440e40, er6
0x02ADE0  mov.w     r5, @er6
0x02ADE2  mov.l     #0x004202a2, er5
0x02ADE8  mov.w     @er6, r0
0x02ADEA  mov.w     @er5, r1
0x02ADEC  cmp.w     r1, r0
0x02ADEE  beq       0x02ae48
0x02ADF0  mov.w     @er6, r0
0x02ADF2  mov.w     @er5, r1
0x02ADF4  cmp.w     r1, r0
0x02ADF6  bls       0x02ae12
0x02ADF8  mov.b     #0x01, r4l
0x02ADFA  mov.w     @er6, r6
0x02ADFC  mov.w     @er5, r5
0x02ADFE  sub.w     r5, r6
0x02AE00  cmp.w     #0x0172, r6
0x02AE04  bcs       0x02ae0c
0x02AE06  mov.w     #0x2710, e6
0x02AE0A  bt        0x02ae2c
0x02AE0C  mov.w     #0x09c4, e6
0x02AE10  bt        0x02ae2c
0x02AE12  sub.b     r4l, r4l
0x02AE14  mov.w     @er5, r5
0x02AE16  mov.w     @er6, r6
0x02AE18  sub.w     r6, r5
0x02AE1A  mov.w     r5, r6
0x02AE1C  cmp.w     #0x0172, r6
0x02AE20  bcs       0x02ae28
0x02AE22  mov.w     #0x2710, e6
0x02AE26  bt        0x02ae2c
0x02AE28  mov.w     #0x09c4, e6
0x02AE2C  sub.l     er5, er5
0x02AE2E  mov.l     er3, @-sp
0x02AE32  mov.l     er5, @-sp
0x02AE36  mov.b     @(0x1d,sp), r0h
0x02AE3A  mov.w     e6, r1
0x02AE3C  mov.w     r6, e0
0x02AE3E  mov.b     r4l, r0l
0x02AE40  bsr       0x02a2f6
0x02AE44  adds.l    #4, sp
0x02AE46  adds.l    #4, sp
0x02AE48  ldm.l     @sp+, er4-er6
0x02AE4C  mov.l     @sp+, er3
0x02AE50  rts       
0x02AE52  mov.l     er3, @-sp
0x02AE56  stm.l     er4-er6, @-sp
0x02AE5A  mov.b     r0l, r5l
0x02AE5C  mov.w     e0, r6
0x02AE5E  mov.l     er1, er3
0x02AE60  mov.b     r0h, r5h
0x02AE62  cmp.w     #0x0172, r6
0x02AE66  mov.w     #0x09c4, e6
0x02AE6A  cmp.b     #0x01, r5l
0x02AE6C  bne       0x02ae78
0x02AE6E  mov.w     @0x4202a2, r0
0x02AE74  add.w     r6, r0
0x02AE76  bt        0x02ae80
0x02AE78  mov.w     @0x4202a2, r0
0x02AE7E  sub.w     r6, r0
0x02AE80  mov.w     r0, @0x440e40
0x02AE86  sub.l     er4, er4
0x02AE88  mov.l     er3, @-sp
0x02AE8C  mov.l     er4, @-sp
0x02AE90  mov.b     r5h, r0h
0x02AE92  mov.w     e6, r1
0x02AE94  mov.w     r6, e0
0x02AE96  mov.b     r5l, r0l
0x02AE98  bsr       0x02a2f6
0x02AE9C  adds.l    #4, sp
0x02AE9E  adds.l    #4, sp
0x02AEA0  ldm.l     @sp+, er4-er6
0x02AEA4  mov.l     @sp+, er3
0x02AEA8  rts       
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
0x02AF6C  sub.b     r0l, r0l
0x02AF6E  mov.w     r0, @-sp
0x02AF70  mov.l     #0x000186a0, er1
0x02AF76  mov.w     @0x40040a, r0
0x02AF7C  bsr       0x02adce
