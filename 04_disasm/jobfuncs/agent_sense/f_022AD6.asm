0x022AD6  mov.l     er3, @-sp
0x022ADA  stm.l     er4-er6, @-sp
0x022ADE  subs.l    #4, sp
0x022AE0  subs.l    #4, sp
0x022AE2  mov.l     #0x004007d1, er6
0x022AE8  mov.l     er0, @sp
0x022AEC  mov.l     er1, @(0x4,sp)
0x022AF2  mov.b     @0x4007c1, r3l
0x022AF8  cmp.b     #0x09, r3l
0x022AFA  bne       0x022afe
0x022AFC  mov.b     #0x04, r3l
0x022AFE  mov.w     @0x400436, r5   <<< 0x400436
0x022B04  mov.w     #0x0005, e5
0x022B08  mulxu.w   e5, er5
0x022B0A  add.l     #0x0001914a, er5
0x022B10  mov.b     @(0x1,er5), r0l
0x022B14  mov.b     r0l, @(0x1,er6)
0x022B18  mov.b     @(0x2,er5), r0l
0x022B1C  mov.b     r0l, @(0x2,er6)
0x022B20  mov.b     @(0x3,er5), r0l
0x022B24  mov.b     r0l, @(0x3,er6)
0x022B28  mov.b     @(0x4,er5), r0l
0x022B2C  mov.b     r0l, @(0x4,er6)
0x022B30  mov.b     #0x05, r4l
0x022B32  mov.b     r4l, r0l
0x022B34  extu.w    r0
0x022B36  extu.l    er0
0x022B38  add.l     er6, er0
0x022B3A  sub.b     r1l, r1l
0x022B3C  mov.b     r1l, @er0
0x022B3E  inc.b     #1, r4l
0x022B40  cmp.b     #0x12, r4l
0x022B42  bcs       0x022b32
0x022B44  mov.b     @(0x3,er5), r0l
0x022B48  cmp.b     #0x02, r0l
0x022B4A  bne       0x022bbe
0x022B4C  mov.b     #0x02, r0l
0x022B4E  mov.b     r0l, @er6
0x022B50  mov.b     @(0x2,sp), r0l
0x022B54  sub.b     r0h, r0h
0x022B56  mov.b     r0l, @(0x5,er6)
0x022B5A  mov.b     @(0x3,sp), r0l
0x022B5E  mov.b     r0l, @(0x6,er6)
0x022B62  mov.l     er6, er4
0x022B64  add.l     #0x0000000c, er4
0x022B6A  sub.l     er0, er0
0x022B6C  mov.b     @er4, r0l
0x022B6E  mov.l     @(0x4,sp), er1
0x022B74  jsr       0x018e1e
0x022B78  mov.l     er0, er5
0x022B7A  mov.b     r0h, r0l
0x022B7C  sub.b     r0h, r0h
0x022B7E  mov.b     r0l, @(0x7,er6)
0x022B82  mov.b     r5l, @(0x8,er6)
0x022B86  extu.w    r3
0x022B88  mov.w     #0x003a, e3
0x022B8C  mulxu.w   e3, er3
0x022B8E  mov.l     #0x0040064e, er5
0x022B94  add.l     er3, er5
0x022B96  mov.b     @(0x1a,er5), r0l
0x022B9A  mov.b     r0l, @(0x9,er6)
0x022B9E  mov.b     @(0x6,sp), r0l
0x022BA2  mov.b     r0l, @(0xa,er6)
0x022BA6  mov.b     @(0x7,sp), r0l
0x022BAA  mov.b     r0l, @(0xb,er6)
0x022BAE  mov.b     @(0x28,er5), r5l
0x022BB2  and.b     #0xf0, r5l
0x022BB4  shlr.b    #2, r5l
0x022BB6  shlr.b    #2, r5l
0x022BB8  add.b     #0x01, r5l
0x022BBA  mov.b     r5l, @er4
0x022BBC  bt        0x022be4
0x022BBE  mov.b     @(0x3,er5), r5l
0x022BC2  cmp.b     #0x03, r5l
0x022BC4  bne       0x022be4
0x022BC6  mov.b     #0x03, r0l
0x022BC8  mov.b     r0l, @er6
0x022BCA  mov.w     #0x000c, r0
0x022BCE  extu.l    er0
0x022BD0  mov.w     @(0x1c,sp), r1
0x022BD4  divxu.w   r1, er0
0x022BD6  shll.w    #2, r0
0x022BD8  shll.w    #2, r0
0x022BDA  mov.b     r0l, @(0xd,er6)
0x022BDE  sub.b     r0l, r0l
0x022BE0  mov.b     r0l, @(0xe,er6)
0x022BE4  adds.l    #4, sp
0x022BE6  adds.l    #4, sp
0x022BE8  ldm.l     @sp+, er4-er6
0x022BEC  mov.l     @sp+, er3
0x022BF0  rts       
