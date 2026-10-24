0x022BF2  stm.l     er4-er5, @-sp
0x022BF6  mov.l     #0x004007d1, er4
0x022BFC  mov.b     #0x06, r0l
0x022BFE  mov.b     r0l, @er4
0x022C00  mov.w     @0x400436, r5   <<< 0x400436
0x022C06  mov.w     #0x0005, e5
0x022C0A  mulxu.w   e5, er5
0x022C0C  add.l     #0x0001914a, er5
0x022C12  mov.b     @(0x1,er5), r0l
0x022C16  mov.b     r0l, @(0x1,er4)
0x022C1A  mov.b     @(0x2,er5), r0l
0x022C1E  mov.b     r0l, @(0x2,er4)
0x022C22  mov.b     @(0x3,er5), r0l
0x022C26  mov.b     r0l, @(0x3,er4)
0x022C2A  mov.b     @(0x4,er5), r5l
0x022C2E  mov.b     r5l, @(0x4,er4)
0x022C32  sub.b     r0l, r0l
0x022C34  mov.b     r0l, @(0x5,er4)
0x022C38  mov.b     r0l, @(0x6,er4)
0x022C3C  sub.b     r0l, r0l
0x022C3E  mov.b     r0l, @(0x7,er4)
0x022C42  mov.b     #0x01, r0l
0x022C44  mov.b     r0l, @(0x8,er4)
0x022C48  mov.b     #0x09, r5l
0x022C4A  mov.b     r5l, r0l
0x022C4C  extu.w    r0
0x022C4E  extu.l    er0
0x022C50  add.l     er4, er0
0x022C52  sub.b     r1l, r1l
0x022C54  mov.b     r1l, @er0
0x022C56  inc.b     #1, r5l
0x022C58  cmp.b     #0x12, r5l
0x022C5A  bcs       0x022c4a
0x022C5C  ldm.l     @sp+, er4-er5
0x022C60  rts       
