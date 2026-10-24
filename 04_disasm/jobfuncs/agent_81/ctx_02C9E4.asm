0x02C9E4  stm.l     er2-er3, @-sp
0x02C9E8  stm.l     er4-er6, @-sp
0x02C9EC  mov.l     #0x00440fda, er6
0x02C9F2  mov.w     r0, r5
0x02C9F4  mov.l     er1, er2
0x02C9F6  cmp.w     #0x0f60, r5
0x02C9FA  bls       0x02ca04
0x02C9FC  mov.w     #0x0f60, r0
0x02CA00  mov.w     r0, @er6
0x02CA02  bt        0x02ca06
0x02CA04  mov.w     r5, @er6
0x02CA06  mov.l     #0x004202ec, er5
0x02CA0C  mov.w     @er6, r0
0x02CA0E  mov.w     @er5, r1
0x02CA10  cmp.w     r1, r0
0x02CA12  beq       0x02ca6e
0x02CA14  mov.w     @er6, r0
0x02CA16  mov.w     @er5, r1
0x02CA18  cmp.w     r1, r0
0x02CA1A  bls       0x02ca38
0x02CA1C  sub.b     r4l, r4l
0x02CA1E  mov.w     @er6, r0
0x02CA20  mov.w     @er5, r5
0x02CA22  sub.w     r5, r0
0x02CA24  mov.w     r0, r5
0x02CA26  cmp.w     #0x012f, r0
0x02CA2A  bcs       0x02ca32
0x02CA2C  mov.w     #0x02bc, e5
0x02CA30  bt        0x02ca50
0x02CA32  mov.w     #0x0190, e5
0x02CA36  bt        0x02ca50
0x02CA38  mov.b     #0x01, r4l
0x02CA3A  mov.w     @er5, r5
0x02CA3C  mov.w     @er6, r0
0x02CA3E  sub.w     r0, r5
0x02CA40  cmp.w     #0x012f, r5
0x02CA44  bcs       0x02ca4c
0x02CA46  mov.w     #0x02bc, e5
0x02CA4A  bt        0x02ca50
0x02CA4C  mov.w     #0x0190, e5
0x02CA50  sub.l     er3, er3
0x02CA52  mov.l     er2, er0
0x02CA54  mov.l     er0, @-sp
0x02CA58  mov.l     er3, @-sp
0x02CA5C  mov.b     @(0x21,sp), r0h
0x02CA60  mov.w     e5, r1
0x02CA62  mov.w     r5, e0
0x02CA64  mov.b     r4l, r0l
0x02CA66  bsr       0x02be32
0x02CA6A  adds.l    #4, sp
0x02CA6C  adds.l    #4, sp
0x02CA6E  ldm.l     @sp+, er4-er6
0x02CA72  ldm.l     @sp+, er2-er3
0x02CA76  rts       
0x02CA78  mov.w     r3, @-sp
0x02CA7A  stm.l     er4-er6, @-sp
0x02CA7E  mov.b     r0l, r3h
0x02CA80  mov.w     e0, e6
0x02CA82  mov.l     er1, er4
0x02CA84  mov.b     r0h, r3l
0x02CA86  cmp.w     #0x012f, e6
0x02CA8A  bcs       0x02ca92
0x02CA8C  mov.w     #0x02bc, r6
0x02CA90  bt        0x02ca96
0x02CA92  mov.w     #0x0190, r6
0x02CA96  sub.l     er5, er5
0x02CA98  mov.l     er4, @-sp
0x02CA9C  mov.l     er5, @-sp
0x02CAA0  mov.b     r3l, r0h
0x02CAA2  mov.w     r6, r1
0x02CAA4  mov.w     e6, e0
0x02CAA6  mov.b     r3h, r0l
0x02CAA8  bsr       0x02be32
0x02CAAC  adds.l    #4, sp
0x02CAAE  adds.l    #4, sp
0x02CAB0  ldm.l     @sp+, er4-er6
0x02CAB4  mov.w     @sp+, r3
0x02CAB6  rts       
0x02CAB8  mov.w     r3, @-sp
0x02CABA  stm.l     er4-er6, @-sp
0x02CABE  sub.b     r0l, r0l
0x02CAC0  mov.b     r0l, @0x440e62
0x02CAC6  sub.b     r0l, r0l
0x02CAC8  mov.b     r0l, @0x4202f2
0x02CACE  mov.l     #0x00400408, er5
0x02CAD4  mov.w     @0x400410, r0
0x02CADA  bne       0x02cafa
0x02CADC  sub.b     r0l, r0l
0x02CADE  mov.w     r0, @-sp
0x02CAE0  mov.l     #0x000186a0, er1
0x02CAE6  mov.w     @(0x2,er5), r0
0x02CAEA  bsr       0x02c9e4
0x02CAEE  adds.l    #2, sp
0x02CAF0  bsr       0x02c8b4
0x02CAF4  mov.b     r0l, r0l
0x02CAF6  beq       0x02cace
0x02CAF8  bt        0x02cb5e
0x02CAFA  mov.w     @(0x2,er5), r0
0x02CAFE  cmp.w     #0x0f60, r0
0x02CB02  bls       0x02cb0a
0x02CB04  mov.w     #0x0f60, r6
0x02CB08  bt        0x02cb0e
0x02CB0A  mov.w     @(0x2,er5), r6
0x02CB0E  mov.l     #0x004202ec, er5
0x02CB14  mov.w     @er5, r0
0x02CB16  cmp.w     r0, r6
0x02CB18  beq       0x02cb5e
0x02CB1A  mov.w     @er5, r0
0x02CB1C  cmp.w     r0, r6
0x02CB1E  bls       0x02cb2a
0x02CB20  sub.b     r3l, r3l
0x02CB22  mov.w     @er5, r5
0x02CB24  sub.w     r5, r6
0x02CB26  mov.w     r6, r4
0x02CB28  bt        0x02cb30
0x02CB2A  mov.b     #0x01, r3l
0x02CB2C  mov.w     @er5, r4
0x02CB2E  sub.w     r6, r4
0x02CB30  sub.l     er6, er6
0x02CB32  mov.l     #0x000186a0, er0
0x02CB38  mov.l     er0, @-sp
0x02CB3C  mov.l     er6, @-sp
0x02CB40  sub.b     r0h, r0h
0x02CB42  mov.w     @0x400410, r1
0x02CB48  mov.w     r4, e0
0x02CB4A  mov.b     r3l, r0l
0x02CB4C  bsr       0x02be32
0x02CB50  adds.l    #4, sp
0x02CB52  adds.l    #4, sp
0x02CB54  bsr       0x02c8b4
0x02CB58  mov.b     r0l, r0l
0x02CB5A  beq       0x02cace
0x02CB5E  ldm.l     @sp+, er4-er6
0x02CB62  mov.w     @sp+, r3
0x02CB64  rts       
0x02CB66  stm.l     er4-er5, @-sp
0x02CB6A  mov.l     #0x004202ec, er5
0x02CB70  mov.l     #0x00400408, er4
0x02CB76  mov.b     #0x01, r0l
0x02CB78  mov.b     r0l, @0x400d75
0x02CB7E  bt        0x02cb98
0x02CB80  sub.b     r0l, r0l
0x02CB82  mov.w     r0, @-sp
0x02CB84  mov.l     #0x000186a0, er1
0x02CB8A  mov.w     @(0x2,er4), r0
0x02CB8E  bsr       0x02c9e4
0x02CB92  adds.l    #2, sp
0x02CB94  bsr       0x02c8b4
0x02CB98  mov.w     @er5, r0
0x02CB9A  mov.w     @(0x2,er4), r1
0x02CB9E  cmp.w     r1, r0
0x02CBA0  bne       0x02cb80
0x02CBA2  mov.w     @er5, r0
