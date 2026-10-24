0x03BFBE  stm.l     er2-er3, @-sp
0x03BFC2  sub.l     #0x00000018, sp
0x03BFC8  mov.w     r0, r1
0x03BFCA  mov.l     #0x0003f950, er3
0x03BFD0  bt        0x03bfde
0x03BFD2  mov.w     @er3, r0
0x03BFD4  cmp.w     r1, r0
0x03BFD6  bls       0x03bfe6
0x03BFD8  add.l     #0x0000000a, er3
0x03BFDE  mov.w     @er3, r0
0x03BFE0  cmp.w     #0xffff, r0
0x03BFE4  bne       0x03bfd2
0x03BFE6  mov.l     @0x42029a, er1
0x03BFEE  mov.l     #0x00000010, er0
0x03BFF4  add.l     sp, er0
0x03BFF6  jsr       0x018e68
0x03BFFA  mov.l     er0, er1
0x03BFFC  mov.l     #0x00000002, er2
0x03C002  add.l     er3, er2
0x03C004  mov.l     #0x00000008, er0
0x03C00A  add.l     sp, er0
0x03C00C  jsr       0x018aa0
0x03C010  mov.l     er0, er1
0x03C012  mov.l     #0x0003f9d4, er2
0x03C018  mov.l     sp, er0
0x03C01A  jsr       0x017fd2
0x03C01E  jsr       0x01876a
0x03C022  mov.l     er0, er3
0x03C024  add.l     #0x00000018, sp
0x03C02A  ldm.l     @sp+, er2-er3
0x03C02E  rts       
0x03C030  stm.l     er2-er3, @-sp
0x03C034  stm.l     er4-er6, @-sp
0x03C038  subs.l    #4, sp
0x03C03A  mov.l     #0x00449a30, er4
0x03C040  mov.w     r0, e5
0x03C042  mov.w     e0, r3
0x03C044  mov.b     r1l, r6l
0x03C046  mov.b     @0x400db7, r0l
0x03C04C  cmp.b     #0x01, r0l
0x03C04E  beq       0x03c188
0x03C052  mov.b     r6l, r6l
0x03C054  bne       0x03c0ce
0x03C056  mov.b     #0xff, r0l
0x03C058  mov.b     r0l, @er4
0x03C05A  mov.b     @0x40041a, r0l
0x03C060  extu.w    r0
0x03C062  dec.w     #1, r0
0x03C064  mov.w     r0, r5
0x03C066  bt        0x03c0ba
0x03C068  mov.w     r5, r6
0x03C06A  exts.l    er6
0x03C06C  shll.l    #2, er6
0x03C06E  mov.l     @(0x420308,er6), er0
0x03C078  mov.l     er0, @sp
0x03C07C  cmp.w     r0, e5
0x03C07E  bcs       0x03c0b8
0x03C080  mov.w     @(0x2,sp), r0
0x03C084  mov.w     @(0x4204ea,er6), r1
0x03C08C  add.w     r1, r0
0x03C08E  cmp.w     r0, e5
0x03C090  bhi       0x03c0b8
0x03C092  mov.w     @(0x4203fa,er6), r0
0x03C09A  cmp.w     r0, r3
0x03C09C  bcs       0x03c0b8
0x03C09E  mov.w     @(0x4203fa,er6), r0
0x03C0A6  mov.w     @(0x4205da,er6), r1
0x03C0AE  add.w     r1, r0
0x03C0B0  cmp.w     r0, r3
0x03C0B2  bhi       0x03c0b8
0x03C0B4  mov.b     r5l, @er4
0x03C0B6  bt        0x03c0be
0x03C0B8  dec.w     #1, r5
0x03C0BA  mov.w     r5, r5
0x03C0BC  bge       0x03c068
