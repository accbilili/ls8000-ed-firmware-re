# fn 0x03BD4A (callee_x2) : 182 insns
0x03BD4A  stm.l     er2-er3, @-sp
0x03BD4E  stm.l     er4-er6, @-sp
0x03BD52  sub.l     #0x00000022, sp
0x03BD58  mov.l     #0x004491d5, er5
0x03BD5E  mov.w     r0, @(0x4,sp)
0x03BD62  mov.b     r1l, @(0x7,sp)
0x03BD66  mov.b     r1h, @(0x6,sp)
0x03BD6A  mov.w     #0xffff, r2
0x03BD6E  mov.w     r2, @(0x1e,sp)
0x03BD72  mov.b     #0xff, r2l
0x03BD74  mov.b     r2l, @0x4491d4
0x03BD7A  sub.b     r2l, r2l
0x03BD7C  mov.b     r2l, @(0x21,sp)
0x03BD80  jmp       0x03beb0
0x03BD84  sub.b     r0l, r0l
0x03BD86  mov.b     r0l, @(0x20,sp)
0x03BD8A  mov.b     @(0x21,sp), r0l
0x03BD8E  extu.w    r0
0x03BD90  mov.w     r0, r6
0x03BD92  mov.w     #0x0018, e0
0x03BD96  mulxu.w   e0, er0
0x03BD98  mov.l     er0, er3
0x03BD9A  mov.w     r6, r0
0x03BD9C  mov.w     #0x0030, e0
0x03BDA0  mulxu.w   e0, er0
0x03BDA2  add.l     #0x00449092, er0
0x03BDA8  mov.l     er0, @(0xc,sp)
0x03BDAE  jmp       0x03be98
0x03BDB2  sub.l     er0, er0
0x03BDB4  mov.b     @(0x20,sp), r0l
0x03BDB8  mov.b     @(0x400dab,er0), r6h
0x03BDC0  sub.b     r6l, r6l
0x03BDC2  mov.b     r6h, r0l
0x03BDC4  extu.w    r0
0x03BDC6  mov.w     r0, e6
0x03BDC8  mov.w     #0x0006, e0
0x03BDCC  mulxu.w   e0, er0
0x03BDCE  mov.l     er0, er4
0x03BDD0  mov.w     e6, r0
0x03BDD2  mov.w     #0x000c, e0
0x03BDD6  mulxu.w   e0, er0
0x03BDD8  mov.l     @(0xc,sp), er1
0x03BDDE  add.l     er0, er1
0x03BDE0  mov.l     er1, @(0x16,sp)
0x03BDE6  jmp       0x03be84
0x03BDEA  mov.l     #0x00449172, er0
0x03BDF0  add.l     er3, er0
0x03BDF2  add.l     er4, er0
0x03BDF4  mov.b     r6l, r1l
0x03BDF6  extu.w    r1
0x03BDF8  mov.w     r1, e6
0x03BDFA  mov.b     @er5, r2l
0x03BDFC  extu.w    r2
0x03BDFE  add.w     r1, r2
0x03BE00  exts.l    er2
0x03BE02  shll.l    er2
0x03BE04  add.l     er2, er0
0x03BE06  mov.w     @er0, r0
0x03BE08  mov.w     r0, @0x4491d2
0x03BE0E  bsr       0x03bfbe
0x03BE12  mov.l     er0, er2
0x03BE14  mov.l     #0x004491a2, er0
0x03BE1A  add.l     er3, er0
0x03BE1C  add.l     er4, er0
0x03BE1E  mov.b     @er5, r1l
0x03BE20  extu.w    r1
0x03BE22  add.w     r1, e6
0x03BE24  mov.w     e6, r1
0x03BE26  exts.l    er1
0x03BE28  shll.l    er1
0x03BE2A  add.l     er1, er0
0x03BE2C  mov.w     @er0, e6
0x03BE2E  mov.w     @(0x1e,sp), r0
0x03BE32  cmp.w     r0, e6
0x03BE34  bcc       0x03be76
0x03BE36  mov.w     e6, @(0x1e,sp)
0x03BE3A  mov.b     @er5, r0l
0x03BE3C  extu.w    r0
0x03BE3E  mov.b     r6l, r1l
0x03BE40  extu.w    r1
0x03BE42  add.w     r1, r0
0x03BE44  exts.l    er0
0x03BE46  shll.l    #2, er0
0x03BE48  mov.l     @(0x16,sp), er1
0x03BE4E  add.l     er0, er1
0x03BE50  mov.l     @er1, er0
0x03BE54  mov.l     er0, @(0x8,sp)
0x03BE5A  mov.b     @(0x21,sp), r0l
0x03BE5E  mov.b     r0l, @(0x15,sp)
0x03BE62  mov.b     @er5, r0l
0x03BE64  add.b     r6l, r0l
0x03BE66  mov.b     r0l, @(0x14,sp)
0x03BE6A  mov.l     er2, @(0x10,sp)
0x03BE70  mov.b     r6h, @0x4491d4
0x03BE76  btst      #7, @0x400400
0x03BE7E  bne       0x03bfae
0x03BE82  inc.b     #1, r6l
0x03BE84  mov.b     @(0x7,sp), r0l
0x03BE88  cmp.b     r0l, r6l
0x03BE8A  bcs       0x03bdea
0x03BE8E  mov.b     @(0x20,sp), r0l
0x03BE92  inc.b     #1, r0l
0x03BE94  mov.b     r0l, @(0x20,sp)
0x03BE98  mov.b     @(0x20,sp), r0l
0x03BE9C  mov.b     @(0x3b,sp), r1l
0x03BEA0  cmp.b     r1l, r0l
0x03BEA2  bcs       0x03bdb2
0x03BEA6  mov.b     @(0x21,sp), r0l
0x03BEAA  inc.b     #1, r0l
0x03BEAC  mov.b     r0l, @(0x21,sp)
0x03BEB0  mov.b     @(0x21,sp), r0l
0x03BEB4  mov.b     @(0x6,sp), r1l
0x03BEB8  cmp.b     r1l, r0l
0x03BEBA  bcs       0x03bd84
0x03BEBE  mov.b     @0x4491d4, r0l
0x03BEC4  cmp.b     #0xff, r0l
0x03BEC6  beq       0x03bfae
0x03BECA  mov.b     @(0x14,sp), r0l
0x03BECE  mov.b     r0l, @er5
0x03BED0  mov.l     @(0x8,sp), er0
0x03BED6  mov.l     er0, @0x4498f0
0x03BEDE  mov.l     @(0x10,sp), er0
0x03BEE4  mov.l     er0, @0x4491d8
0x03BEEC  mov.l     #0x00420276, er6
0x03BEF2  sub.l     er4, er4
0x03BEF4  mov.b     @0x4491d4, r4l
0x03BEFA  mov.l     er4, er0
0x03BEFC  shll.l    #2, er0
0x03BEFE  add.l     er6, er0
0x03BF00  mov.l     er0, @sp
0x03BF04  mov.l     er4, er0
0x03BF06  mov.l     #0x0000000c, er1
0x03BF0C  jsr       0x018e1e
0x03BF10  mov.b     @(0x15,sp), r1l
0x03BF14  extu.w    r1
0x03BF16  mov.w     #0x0030, e1
0x03BF1A  mulxu.w   e1, er1
0x03BF1C  add.l     #0x00449978, er1
0x03BF22  add.l     er0, er1
0x03BF24  sub.l     er0, er0
0x03BF26  mov.b     @(0x14,sp), r0l
0x03BF2A  shll.l    #2, er0
0x03BF2C  add.l     er0, er1
0x03BF2E  mov.l     @er1, er1
0x03BF32  mov.l     @sp, er0
0x03BF36  mov.l     er1, @er0
0x03BF3A  mov.l     er6, er0
0x03BF3C  bsr       0x03c194
0x03BF40  sub.l     er4, er4
0x03BF42  mov.b     @0x4491d4, r4l
0x03BF48  mov.l     er4, er3
0x03BF4A  shll.l    #2, er3
0x03BF4C  add.l     er3, er6
0x03BF4E  mov.l     @er6, er0
0x03BF52  jsr       0x018e9e
0x03BF56  sub.l     er1, er1
0x03BF58  mov.b     @(0x41ff6e,er4), r1l
0x03BF60  shll.l    #2, er1
0x03BF62  mov.l     @(0x400dda,er1), er1
0x03BF6C  jsr       0x0185ee
0x03BF70  jsr       0x018860
0x03BF74  mov.l     er0, @(0x420286,er3)
0x03BF7E  mov.b     @(0x15,sp), r0l
0x03BF82  mov.b     #0xc8, r0h
0x03BF84  mulxu.b   r0h, r0
0x03BF86  mov.w     @(0x4,sp), r6
0x03BF8A  sub.w     r0, r6
0x03BF8C  bt        0x03bfa4
0x03BF8E  sub.b     r0l, r0l
0x03BF90  mov.w     r0, @-sp
0x03BF92  mov.l     #0x00002710, er1
0x03BF98  mov.w     r6, r0
0x03BF9A  jsr       0x02adce
0x03BF9E  adds.l    #2, sp
0x03BFA0  jsr       0x02acba
0x03BFA4  mov.w     @0x4202a2, r0
0x03BFAA  cmp.w     r0, r6
0x03BFAC  bne       0x03bf8e
0x03BFAE  add.l     #0x00000022, sp
0x03BFB4  ldm.l     @sp+, er4-er6
0x03BFB8  ldm.l     @sp+, er2-er3
0x03BFBC  rts       
