0x03C9E2  sub.l     er6, er6
0x03C9E4  mov.b     @er5, r6l
0x03C9E6  mov.l     er6, er0
0x03C9E8  shll.l    #2, er0
0x03C9EA  mov.l     @(0x400f32,er0), er0
0x03C9F4  mov.l     er0, @0x420248
0x03C9FC  mov.l     er6, er0
0x03C9FE  mov.l     #0x00000006, er1
0x03CA04  jsr       0x018e1e
0x03CA08  mov.l     #0x0041ff3e, er1
0x03CA0E  add.l     er0, er1
0x03CA10  mov.b     @er5, r0l
0x03CA12  jsr       0x02da8e
0x03CA16  jsr       0x03338e
0x03CA1A  jsr       0x0330aa
0x03CA1E  mov.w     @0x400d60, r1
0x03CA24  extu.l    er1
0x03CA26  mov.w     #0x0003, r0
0x03CA2A  divxu.w   r0, er1
0x03CA2C  extu.l    er1
0x03CA2E  mov.l     @0x41ff7c, er0
0x03CA36  jsr       0x01872e
0x03CA3A  mov.l     er0, @0x449a9e
0x03CA42  mov.w     @0x400d60, r1
0x03CA48  extu.l    er1
0x03CA4A  mov.w     #0x0003, r0
0x03CA4E  divxu.w   r0, er1
0x03CA50  extu.l    er1
0x03CA52  mov.l     @(0x18,sp), er0
0x03CA58  mov.l     @er0, er0
0x03CA5C  jsr       0x01872e
0x03CA60  mov.l     @(0x8,sp), er1
0x03CA66  mov.l     er0, @er1
0x03CA6A  mov.w     @0x400d60, r1
0x03CA70  extu.l    er1
0x03CA72  mov.w     #0x0003, r0
0x03CA76  divxu.w   r0, er1
0x03CA78  extu.l    er1
0x03CA7A  mov.l     @(0x14,sp), er0
0x03CA80  mov.l     @er0, er0
0x03CA84  jsr       0x01872e
0x03CA88  mov.l     @(0x4,sp), er1
0x03CA8E  mov.l     er0, @er1
0x03CA92  mov.l     #0x00000003, er0
0x03CA98  jmp       0x03cc36
0x03CA9C  mov.l     @er3, er0
0x03CAA0  mov.l     #0x00000014, er1
0x03CAA6  jsr       0x018e1e
0x03CAAA  add.l     #0x00000064, er0
0x03CAB0  sub.l     er1, er1
0x03CAB2  mov.b     @er5, r1l
0x03CAB4  shll.l    #2, er1
0x03CAB6  mov.l     @(0x400f32,er1), er1
0x03CAC0  jsr       0x018e1e
0x03CAC4  mov.l     #0x00000064, er1
0x03CACA  jsr       0x01872e
0x03CACE  mov.l     er0, @0x420248
0x03CAD6  jsr       0x03338e
0x03CADA  jsr       0x0330aa
0x03CADE  mov.w     @0x400d60, r1
0x03CAE4  extu.l    er1
0x03CAE6  mov.w     #0x0003, r0
0x03CAEA  divxu.w   r0, er1
0x03CAEC  extu.l    er1
0x03CAEE  mov.l     @0x41ff7c, er0
0x03CAF6  jsr       0x01872e
0x03CAFA  mov.l     er0, @0x449aaa
0x03CB02  mov.w     @0x400d60, r1
0x03CB08  extu.l    er1
0x03CB0A  mov.w     #0x0003, r0
0x03CB0E  divxu.w   r0, er1
0x03CB10  extu.l    er1
0x03CB12  mov.l     @(0x18,sp), er0
0x03CB18  mov.l     @er0, er0
0x03CB1C  jsr       0x01872e
0x03CB20  mov.l     @(0xc,sp), er1
0x03CB26  mov.l     er0, @er1
0x03CB2A  mov.w     @0x400d60, r1
0x03CB30  extu.l    er1
0x03CB32  mov.w     #0x0003, r0
0x03CB36  divxu.w   r0, er1
0x03CB38  extu.l    er1
0x03CB3A  mov.l     @(0x14,sp), er0
0x03CB40  mov.l     @er0, er0
0x03CB44  jsr       0x01872e
0x03CB48  mov.l     @(0x10,sp), er1
0x03CB4E  mov.l     er0, @er1
0x03CB52  sub.w     r6, r6
0x03CB54  jmp       0x03cc28
0x03CB58  mov.w     r6, r0
0x03CB5A  exts.l    er0
0x03CB5C  shll.l    #2, er0
0x03CB5E  mov.l     er0, @(0x1c,sp)
0x03CB64  mov.l     er0, @sp
0x03CB68  mov.l     @er3, er0
0x03CB6C  mov.l     #0x00000014, er1
0x03CB72  jsr       0x018e1e
0x03CB76  add.l     #0x00000064, er0
0x03CB7C  mov.l     @sp, er2
0x03CB80  mov.l     @(0x449a9e,er2), er1
0x03CB8A  jsr       0x018e1e
0x03CB8E  mov.l     #0x00000064, er1
0x03CB94  jsr       0x01872e
0x03CB98  mov.l     er0, @er4
0x03CB9C  mov.l     #0x0000000a, er1
0x03CBA2  jsr       0x01872e
0x03CBA6  mov.l     er0, @0x449abe
0x03CBAE  mov.l     @(0x1c,sp), er0
0x03CBB4  mov.l     @(0x449aaa,er0), er0
0x03CBBE  mov.l     @er4, er1
0x03CBC2  cmp.l     er1, er0
0x03CBC4  bcs       0x03cbea
0x03CBC6  mov.w     r6, r0
0x03CBC8  exts.l    er0
0x03CBCA  shll.l    #2, er0
0x03CBCC  mov.l     @(0x449aaa,er0), er0
0x03CBD6  mov.l     @er4, er1
0x03CBDA  sub.l     er1, er0
0x03CBDC  mov.l     @0x449abe, er1
0x03CBE4  cmp.l     er1, er0
0x03CBE6  bls       0x03cc26
0x03CBE8  bt        0x03cc0c
0x03CBEA  mov.w     r6, r0
0x03CBEC  exts.l    er0
0x03CBEE  shll.l    #2, er0
0x03CBF0  mov.l     @er4, er1
0x03CBF4  mov.l     @(0x449aaa,er0), er0
0x03CBFE  sub.l     er0, er1
0x03CC00  mov.l     @0x449abe, er0
0x03CC08  cmp.l     er0, er1
0x03CC0A  bls       0x03cc26
0x03CC0C  sub.l     er0, er0
0x03CC0E  mov.b     @er5, r0l
0x03CC10  mov.b     @(0x3fbe2,er0), r0l
0x03CC18  mov.l     #0x004206ed, er1
0x03CC1E  mov.b     @er1, r2l
0x03CC20  and.b     r0l, r2l
0x03CC22  mov.b     r2l, @er1
0x03CC24  bt        0x03cc52
0x03CC26  inc.w     #1, r6
0x03CC28  cmp.w     #0x0003, r6
0x03CC2C  blt       0x03cb58
0x03CC30  mov.l     @er3, er0
0x03CC34  dec.l     #1, er0
0x03CC36  mov.l     er0, @er3
0x03CC3A  cmp.l     #0x00000001, er0
0x03CC40  bcc       0x03ca9c
0x03CC44  mov.b     @er5, r0l
0x03CC46  inc.b     #1, r0l
0x03CC48  mov.b     r0l, @er5
0x03CC4A  mov.b     @er5, r0l
0x03CC4C  cmp.b     #0x04, r0l
0x03CC4E  bcs       0x03c9e2
0x03CC52  add.l     #0x00000020, sp
0x03CC58  ldm.l     @sp+, er4-er6
0x03CC5C  ldm.l     @sp+, er2-er3
0x03CC60  rts       
