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
0x03C0BE  mov.b     @er4, r0l
0x03C0C0  mov.b     @0x40041a, r1l
0x03C0C6  cmp.b     r1l, r0l
0x03C0C8  bcc       0x03c188
0x03C0CC  bt        0x03c0d2
0x03C0CE  add.b     #0xff, r6l
0x03C0D0  mov.b     r6l, @er4
0x03C0D2  mov.l     #0x004202f8, er6
0x03C0D8  sub.l     er3, er3
0x03C0DA  mov.b     @er4, r3l
0x03C0DC  shll.l    #2, er3
0x03C0DE  mov.l     er3, er2
0x03C0E0  add.l     #0x004203f8, er3
0x03C0E6  mov.l     er2, er5
0x03C0E8  add.l     #0x004205d8, er5
0x03C0EE  mov.l     @er5, er0
0x03C0F2  shlr.l    er0
0x03C0F4  mov.l     @er3, er1
0x03C0F8  add.l     er1, er0
0x03C0FA  mov.l     #0x0000000c, er1
0x03C100  jsr       0x01872e
0x03C104  mov.w     r0, @er6
0x03C106  mov.l     @er5, er5
0x03C10A  shlr.l    er5
0x03C10C  mov.l     er5, @sp
0x03C110  mov.w     @(0x2,er3), r3
0x03C114  add.w     r3, r5
0x03C116  mov.w     @er6, r0
0x03C118  mov.w     #0x000c, e0
0x03C11C  mulxu.w   e0, er0
0x03C11E  sub.w     r0, r5
0x03C120  mov.w     @(0x2,sp), r0
0x03C124  sub.w     r0, r5
0x03C126  add.w     #0x1ec2, r5
0x03C12A  mov.w     r5, @0x4202ae
0x03C130  mov.w     @er6, r0
0x03C132  add.w     #0x00ab, r0
0x03C136  mov.w     r0, @er6
0x03C138  cmp.w     #0x00fb, r0
0x03C13C  bls       0x03c14c
0x03C13E  mov.w     @er6, r6
0x03C140  sub.w     #0x0050, r6
0x03C144  mov.w     r6, @0x4202fa
0x03C14A  bt        0x03c156
0x03C14C  mov.w     #0x00ab, r0
0x03C150  mov.w     r0, @0x4202fa
0x03C156  mov.w     @0x4202ae, r0
0x03C15C  cmp.w     #0x006c, r0
0x03C160  bls       0x03c16e
0x03C162  mov.w     @0x4202ae, r0
0x03C168  sub.w     #0x006c, r0
0x03C16C  bt        0x03c170
0x03C16E  sub.w     r0, r0
0x03C170  mov.w     r0, @0x4202b0
0x03C176  mov.w     r0, @0x4202b2
0x03C17C  mov.w     @0x4202fa, r0
0x03C182  mov.w     r0, @0x4202fc
0x03C188  adds.l    #4, sp
0x03C18A  ldm.l     @sp+, er4-er6
0x03C18E  ldm.l     @sp+, er2-er3
0x03C192  rts       
