# fn 0x03A994 (selfcheck?) : 297 insns
0x03A994  stm.l     er2-er3, @-sp
0x03A998  stm.l     er4-er6, @-sp
0x03A99C  sub.l     #0x0000000e, sp
0x03A9A2  mov.l     #0x00449082, er3
0x03A9A8  mov.l     #0x0044907c, er4
0x03A9AE  mov.l     #0x0044907e, er5
0x03A9B4  mov.l     #0x00449a30, er6
0x03A9BA  mov.w     @0x40040a, r0
0x03A9C0  mov.w     r0, @(0xa,sp)
0x03A9C4  mov.w     @0x40040e, r1
0x03A9CA  mov.w     r1, e2
0x03A9CC  sub.b     r2l, r2l
0x03A9CE  mov.b     r2l, @0x400db7
0x03A9D4  mov.w     r1, @sp
0x03A9D6  sub.b     r1l, r1l
0x03A9D8  mov.w     @sp, e0
0x03A9DA  bsr       0x03c030
0x03A9DE  mov.b     @er6, r0l
0x03A9E0  mov.b     @0x40041a, r1l
0x03A9E6  cmp.b     r1l, r0l
0x03A9E8  bcs       0x03a9f8
0x03A9EA  mov.w     #0x0950, r0
0x03A9EE  mov.w     r0, @0x400402
0x03A9F4  jmp       0x03ade6
0x03A9F8  mov.w     #0x02bc, r0
0x03A9FC  mov.w     r0, @0x420274
0x03AA02  mov.l     @0x42029a, er0
0x03AA0A  mov.l     er0, @0x4491d8
0x03AA12  sub.l     er0, er0
0x03AA14  mov.b     @er6, r0l
0x03AA16  shll.l    #2, er0
0x03AA18  mov.l     @(0x420308,er0), er0
0x03AA22  add.l     #0x000001a4, er0
0x03AA28  mov.w     @(0xa,sp), r1
0x03AA2C  extu.l    er1
0x03AA2E  cmp.l     er0, er1
0x03AA30  bcc       0x03aa6a
0x03AA32  sub.l     er0, er0
0x03AA34  mov.b     @er6, r0l
0x03AA36  shll.l    #2, er0
0x03AA38  mov.w     @0x420274, r1
0x03AA3E  shlr.w    r1
0x03AA40  extu.l    er1
0x03AA42  mov.l     @(0x420308,er0), er0
0x03AA4C  add.l     er1, er0
0x03AA4E  add.w     #0x0046, r0
0x03AA52  mov.w     r0, @0x420272
0x03AA58  mov.w     #0x02bc, r0
0x03AA5C  mov.w     r0, @er3
0x03AA5E  mov.w     #0x0578, r0
0x03AA62  mov.w     r0, @(0x2,er3)
0x03AA66  jmp       0x03abb2
0x03AA6A  sub.l     er0, er0
0x03AA6C  mov.b     @er6, r0l
0x03AA6E  shll.l    #2, er0
0x03AA70  mov.w     @0x420274, r1
0x03AA76  shlr.w    r1
0x03AA78  extu.l    er1
0x03AA7A  mov.l     @(0x420308,er0), er0
0x03AA84  add.l     er1, er0
0x03AA86  add.l     #0x00000302, er0
0x03AA8C  mov.w     @(0xa,sp), r1
0x03AA90  extu.l    er1
0x03AA92  cmp.l     er0, er1
0x03AA94  bcc       0x03aab2
0x03AA96  mov.w     @(0xa,sp), r0
0x03AA9A  mov.w     r0, @0x420272
0x03AAA0  mov.w     #0x02bc, r0
0x03AAA4  mov.w     r0, @er3
0x03AAA6  mov.w     #0x0578, r0
0x03AAAA  mov.w     r0, @(0x2,er3)
0x03AAAE  jmp       0x03abb2
0x03AAB2  sub.l     er0, er0
0x03AAB4  mov.b     @er6, r0l
0x03AAB6  shll.l    #2, er0
0x03AAB8  mov.l     er0, @(0x6,sp)
0x03AABE  mov.l     @(0x6,sp), er1
0x03AAC4  mov.l     @(0x420308,er0), er0
0x03AACE  mov.l     @(0x4204e8,er1), er1
0x03AAD8  add.l     er1, er0
0x03AADA  mov.w     @0x420274, r1
0x03AAE0  shlr.w    r1
0x03AAE2  add.w     #0x0046, r1
0x03AAE6  extu.l    er1
0x03AAE8  sub.l     er1, er0
0x03AAEA  mov.w     @(0xa,sp), r1
0x03AAEE  extu.l    er1
0x03AAF0  cmp.l     er0, er1
0x03AAF2  bls       0x03ab42
0x03AAF4  sub.l     er0, er0
0x03AAF6  mov.b     @er6, r0l
0x03AAF8  shll.l    #2, er0
0x03AAFA  mov.l     er0, @(0x6,sp)
0x03AB00  mov.l     @(0x6,sp), er1
0x03AB06  mov.l     @(0x420308,er0), er0
0x03AB10  mov.l     @(0x4204e8,er1), er1
0x03AB1A  add.l     er1, er0
0x03AB1C  mov.w     @0x420274, r1
0x03AB22  shlr.w    r1
0x03AB24  add.w     #0x0046, r1
0x03AB28  extu.l    er1
0x03AB2A  sub.l     er1, er0
0x03AB2C  mov.w     r0, @0x420272
0x03AB32  mov.w     #0xfd44, r0
0x03AB36  mov.w     r0, @er3
0x03AB38  mov.w     #0xfa88, r0
0x03AB3C  mov.w     r0, @(0x2,er3)
0x03AB40  bt        0x03abb2
0x03AB42  sub.l     er0, er0
0x03AB44  mov.b     @er6, r0l
0x03AB46  shll.l    #2, er0
0x03AB48  mov.l     er0, @(0x6,sp)
0x03AB4E  mov.l     @(0x6,sp), er1
0x03AB54  mov.l     @(0x420308,er0), er0
0x03AB5E  mov.l     @(0x4204e8,er1), er1
0x03AB68  add.l     er1, er0
0x03AB6A  mov.w     @0x420274, r1
0x03AB70  shlr.w    r1
0x03AB72  add.w     #0x0302, r1
0x03AB76  extu.l    er1
0x03AB78  sub.l     er1, er0
0x03AB7A  mov.w     @(0xa,sp), r1
0x03AB7E  extu.l    er1
0x03AB80  cmp.l     er0, er1
0x03AB82  bls       0x03ab9a
0x03AB84  mov.w     @(0xa,sp), r0
0x03AB88  mov.w     r0, @0x420272
0x03AB8E  mov.w     #0xfd44, r0
0x03AB92  mov.w     r0, @er3
0x03AB94  mov.w     #0xfa88, r0
0x03AB98  bt        0x03abae
0x03AB9A  mov.w     @(0xa,sp), r0
0x03AB9E  mov.w     r0, @0x420272
0x03ABA4  mov.w     #0x02bc, r0
0x03ABA8  mov.w     r0, @er3
0x03ABAA  mov.w     #0xfd44, r0
0x03ABAE  mov.w     r0, @(0x2,er3)
0x03ABB2  sub.l     er0, er0
0x03ABB4  mov.b     @er6, r0l
0x03ABB6  shll.l    #2, er0
0x03ABB8  mov.l     @(0x4203f8,er0), er0
0x03ABC2  add.l     #0x00000046, er0
0x03ABC8  mov.w     e2, r1
0x03ABCA  extu.l    er1
0x03ABCC  cmp.l     er0, er1
0x03ABCE  bcc       0x03abf6
0x03ABD0  sub.l     er0, er0
0x03ABD2  mov.b     @er6, r0l
0x03ABD4  shll.l    #2, er0
0x03ABD6  mov.w     @(0x4203fa,er0), r0
0x03ABDE  add.w     #0x0046, r0
0x03ABE2  mov.w     r0, @er4
0x03ABE4  mov.w     #0x02bc, r0
0x03ABE8  mov.w     r0, @er5
0x03ABEA  mov.w     #0x0578, r0
0x03ABEE  mov.w     r0, @(0x2,er5)
0x03ABF2  jmp       0x03ace4
0x03ABF6  sub.l     er0, er0
0x03ABF8  mov.b     @er6, r0l
0x03ABFA  shll.l    #2, er0
0x03ABFC  mov.l     @(0x4203f8,er0), er0
0x03AC06  add.l     #0x00000302, er0
0x03AC0C  mov.w     e2, r1
0x03AC0E  extu.l    er1
0x03AC10  cmp.l     er0, er1
0x03AC12  bcc       0x03ac28
0x03AC14  mov.w     e2, @er4
0x03AC16  mov.w     #0x02bc, r0
0x03AC1A  mov.w     r0, @er5
0x03AC1C  mov.w     #0x0578, r0
0x03AC20  mov.w     r0, @(0x2,er5)
0x03AC24  jmp       0x03ace4
0x03AC28  sub.l     er0, er0
0x03AC2A  mov.b     @er6, r0l
0x03AC2C  shll.l    #2, er0
0x03AC2E  mov.l     er0, @(0x6,sp)
0x03AC34  mov.l     @(0x6,sp), er1
0x03AC3A  mov.l     @(0x4203f8,er0), er0
0x03AC44  mov.l     @(0x4205d8,er1), er1
0x03AC4E  add.l     er1, er0
0x03AC50  add.l     #0xffffffba, er0
0x03AC56  mov.w     e2, r1
0x03AC58  extu.l    er1
0x03AC5A  cmp.l     er0, er1
0x03AC5C  bls       0x03ac90
0x03AC5E  sub.l     er0, er0
0x03AC60  mov.b     @er6, r0l
0x03AC62  shll.l    #2, er0
0x03AC64  mov.l     er0, er2
0x03AC66  mov.l     er2, er1
0x03AC68  mov.w     @(0x4203fa,er0), r0
0x03AC70  mov.w     @(0x4205da,er1), r1
0x03AC78  add.w     r1, r0
0x03AC7A  add.w     #0xffba, r0
0x03AC7E  mov.w     r0, @er4
0x03AC80  mov.w     #0xfd44, r0
0x03AC84  mov.w     r0, @er5
0x03AC86  mov.w     #0xfa88, r0
0x03AC8A  mov.w     r0, @(0x2,er5)
0x03AC8E  bt        0x03ace4
0x03AC90  sub.l     er0, er0
0x03AC92  mov.b     @er6, r0l
0x03AC94  shll.l    #2, er0
0x03AC96  mov.l     er0, @(0x6,sp)
0x03AC9C  mov.l     @(0x6,sp), er1
0x03ACA2  mov.l     @(0x4203f8,er0), er0
0x03ACAC  mov.l     @(0x4205d8,er1), er1
0x03ACB6  add.l     er1, er0
0x03ACB8  add.l     #0xfffffcfe, er0
0x03ACBE  mov.w     e2, r1
0x03ACC0  extu.l    er1
0x03ACC2  cmp.l     er0, er1
0x03ACC4  bls       0x03acd4
0x03ACC6  mov.w     e2, @er4
0x03ACC8  mov.w     #0xfd44, r0
0x03ACCC  mov.w     r0, @er5
0x03ACCE  mov.w     #0xfa88, r0
0x03ACD2  bt        0x03ace0
0x03ACD4  mov.w     e2, @er4
0x03ACD6  mov.w     #0x02bc, r0
0x03ACDA  mov.w     r0, @er5
0x03ACDC  mov.w     #0xfd44, r0
0x03ACE0  mov.w     r0, @(0x2,er5)
0x03ACE4  mov.w     @0x420274, r0
0x03ACEA  exts.l    er0
0x03ACEC  mov.w     #0x0002, r1
0x03ACF0  divxs.w   r1, er0
0x03ACF4  mov.w     @0x400d60, r1
0x03ACFA  sub.w     r0, r1
0x03ACFC  mov.w     @0x420272, r0
0x03AD02  sub.w     r0, r1
0x03AD04  mov.w     r1, @0x449086
0x03AD0A  mov.w     @0x449086, r0
0x03AD10  mov.w     @er3, r1
0x03AD12  sub.w     r1, r0
0x03AD14  mov.w     r0, @0x449088
0x03AD1A  mov.w     @0x449086, r0
0x03AD20  mov.w     @(0x2,er3), r1
0x03AD24  sub.w     r1, r0
0x03AD26  mov.w     r0, @0x44908a
0x03AD2C  mov.w     @0x4202f8, r0
0x03AD32  sub.w     #0x00ab, r0
0x03AD36  mov.w     #0x000c, e0
0x03AD3A  mulxu.w   e0, er0
0x03AD3C  mov.w     #0x1ec2, r1
0x03AD40  sub.w     r0, r1
0x03AD42  mov.w     @er4, r0
0x03AD44  add.w     r1, r0
0x03AD46  mov.w     r0, @er4
0x03AD48  mov.w     r0, @0x44908c
0x03AD4E  mov.w     @er5, r1
0x03AD50  add.w     r1, r0
0x03AD52  mov.w     r0, @0x44908e
0x03AD58  mov.w     @0x44908c, r0
0x03AD5E  mov.w     @(0x2,er5), r1
0x03AD62  add.w     r1, r0
0x03AD64  mov.w     r0, @0x449090
0x03AD6A  bt        0x03ad86
0x03AD6C  sub.b     r0l, r0l
0x03AD6E  mov.w     r0, @-sp
0x03AD70  mov.l     #0x00002710, er1
0x03AD76  mov.w     @0x4202fa, r0
0x03AD7C  jsr       0x02c9e4
0x03AD80  adds.l    #2, sp
0x03AD82  jsr       0x02c8b4
0x03AD86  mov.w     @0x4202ec, r0
0x03AD8C  mov.w     @0x4202fa, r1
0x03AD92  cmp.w     r1, r0
0x03AD94  bne       0x03ad6c
0x03AD96  bt        0x03adb2
0x03AD98  sub.b     r0l, r0l
0x03AD9A  mov.w     r0, @-sp
0x03AD9C  mov.l     #0x00002710, er1
0x03ADA2  mov.w     @0x4202f8, r0
0x03ADA8  jsr       0x02c9e4
0x03ADAC  adds.l    #2, sp
0x03ADAE  jsr       0x02c8b4
0x03ADB2  mov.w     @0x4202ec, r0
0x03ADB8  mov.w     @0x4202f8, r1
0x03ADBE  cmp.w     r1, r0
0x03ADC0  bne       0x03ad98
0x03ADC2  bt        0x03adda
0x03ADC4  sub.b     r0l, r0l
0x03ADC6  mov.w     r0, @-sp
0x03ADC8  mov.l     #0x00002710, er1
0x03ADCE  mov.w     @er4, r0
0x03ADD0  jsr       0x02adce
0x03ADD4  adds.l    #2, sp
0x03ADD6  jsr       0x02acba
0x03ADDA  mov.w     @0x4202a2, r0
0x03ADE0  mov.w     @er4, r1
0x03ADE2  cmp.w     r1, r0
0x03ADE4  bne       0x03adc4
0x03ADE6  add.l     #0x0000000e, sp
0x03ADEC  ldm.l     @sp+, er4-er6
0x03ADF0  ldm.l     @sp+, er2-er3
0x03ADF4  rts       
