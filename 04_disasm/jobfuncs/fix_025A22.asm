0x025840  mov.b     @(0x143,sp), r0l
0x025844  bne       0x02584a
0x025846  mov.b     #0x01, r4h
0x025848  bt        0x025868
0x02584A  mov.b     @(0x143,sp), r0l
0x02584E  cmp.b     #0x04, r0l
0x025850  bne       0x025856
0x025852  mov.b     #0x03, r4h
0x025854  bt        0x025868
0x025856  mov.b     @(0x143,sp), r0l
0x02585A  cmp.b     #0x05, r0l
0x02585C  bne       0x025862
0x02585E  sub.b     r4h, r4h
0x025860  bt        0x025868
0x025862  mov.b     @(0x143,sp), r4h
0x025866  add.b     #0xff, r4h
0x025868  mov.b     @(0x143,sp), r5l
0x02586C  extu.w    r5
0x02586E  mov.w     #0x003a, e5
0x025872  mulxu.w   e5, er5
0x025874  add.l     #0x0040064e, er5
0x02587A  sub.b     r4l, r4l
0x02587C  mov.b     r4h, r3l
0x02587E  extu.w    r3
0x025880  extu.l    er3
0x025882  mov.l     er3, er0
0x025884  shll.l    #2, er0
0x025886  mov.l     er0, @(0x12e,sp)
0x02588C  mov.b     r4h, r0l
0x02588E  extu.w    r0
0x025890  mov.w     #0x0006, e0
0x025894  mulxu.w   e0, er0
0x025896  add.l     #0x0041ff3e, er0
0x02589C  mov.l     er0, @(0x13e,sp)
0x0258A2  add.l     #0x0041ff6e, er3
0x0258A8  mov.l     er3, @(0x132,sp)
0x0258AE  jmp       0x025a22
0x0258B2  cmp.b     #0x2e, r4l
0x0258B4  bne       0x025928
0x0258B6  mov.l     #0x0000012a, er3
0x0258BC  add.l     sp, er3
0x0258BE  mov.b     @er5, r0l
0x0258C0  mov.b     r0l, @er3
0x0258C2  mov.b     @(0x1,er5), r0l
0x0258C6  mov.b     r0l, @(0x1,er3)
0x0258CA  mov.b     @(0x2,er5), r0l
0x0258CE  mov.b     r0l, @(0x2,er3)
0x0258D2  mov.b     @(0x3,er5), r0l
0x0258D6  mov.b     r0l, @(0x3,er3)
0x0258DA  mov.b     @(0xfffb,er5), r0l
0x0258DE  and.b     #0x01, r0l
0x0258E0  extu.w    r0
0x0258E2  extu.l    er0
0x0258E4  shll.l    #2, er0
0x0258E6  shll.l    #2, er0
0x0258E8  add.l     #0x00400e1c, er0
0x0258EE  mov.l     @(0x12e,sp), er1
0x0258F4  add.l     er1, er0
0x0258F6  mov.l     @er0, er1
0x0258FA  mov.l     er1, @(0x12a,sp)
0x025900  mov.l     er6, er0
0x025902  inc.l     #1, er6
0x025904  mov.b     @er3+, r1l
0x025906  mov.b     r1l, @er0
0x025908  mov.l     er6, er0
0x02590A  inc.l     #1, er6
0x02590C  mov.b     @er3+, r1l
0x02590E  mov.b     r1l, @er0
0x025910  mov.l     er6, er0
0x025912  inc.l     #1, er6
0x025914  mov.b     @er3+, r1l
0x025916  mov.b     r1l, @er0
0x025918  mov.l     er6, er0
0x02591A  inc.l     #1, er6
0x02591C  mov.b     @er3, r3l
0x02591E  mov.b     r3l, @er0
0x025920  adds.l    #4, er5
0x025922  add.b     #0x03, r4l
0x025924  jmp       0x025a20
0x025928  cmp.b     #0x33, r4l
0x02592A  bne       0x02595a
0x02592C  mov.l     er6, er0
0x02592E  inc.l     #1, er6
0x025930  mov.l     @(0x13e,sp), er1
0x025936  mov.w     @er1, r1
0x025938  inc.w     #1, r1
0x02593A  mov.b     r1h, r1l
0x02593C  sub.b     r1h, r1h
0x02593E  mov.b     r1l, @er0
0x025940  mov.l     er6, er0
0x025942  inc.l     #1, er6
0x025944  mov.l     @(0x13e,sp), er1
0x02594A  mov.b     @(0x1,er1), r1l
0x02594E  add.b     #0x01, r1l
0x025950  mov.b     r1l, @er0
0x025952  inc.l     #2, er5
0x025954  inc.b     #1, r4l
0x025956  jmp       0x025a20
0x02595A  cmp.b     #0x35, r4l
0x02595C  bne       0x025a00
0x025960  mov.l     #0x0000012a, er3
0x025966  add.l     sp, er3
0x025968  mov.b     @er5, r0l
0x02596A  mov.b     r0l, @er3
0x02596C  mov.b     @(0x1,er5), r0l
0x025970  mov.b     r0l, @(0x1,er3)
0x025974  mov.b     @(0x2,er5), r0l
0x025978  mov.b     r0l, @(0x2,er3)
0x02597C  mov.b     @(0x3,er5), r0l
0x025980  mov.b     r0l, @(0x3,er3)
0x025984  mov.b     @(0xfff1,er5), r1l
0x025988  and.b     #0x01, r1l
0x02598A  extu.w    r1
0x02598C  extu.l    er1
0x02598E  shll.l    #2, er1
0x025990  shll.l    #2, er1
0x025992  mov.b     r4h, r0l
0x025994  extu.w    r0
0x025996  extu.l    er0
0x025998  mov.l     er0, @(0x13a,sp)
0x02599E  shll.l    #2, er0
0x0259A0  add.l     #0x00400e1c, er1
0x0259A6  add.l     er1, er0
0x0259A8  mov.l     @er0, er0
0x0259AC  jsr       0x018e9e
0x0259B0  mov.l     @(0x13a,sp), er1
0x0259B6  sub.l     er2, er2
0x0259B8  mov.b     @(0x41ff6e,er1), r2l
0x0259C0  shll.l    #2, er2
0x0259C2  mov.l     @(0x400dda,er2), er1
0x0259CC  jsr       0x0185ee
0x0259D0  jsr       0x018860
0x0259D4  mov.l     er0, @(0x12a,sp)
0x0259DA  mov.l     er6, er0
0x0259DC  inc.l     #1, er6
0x0259DE  mov.b     @er3+, r1l
0x0259E0  mov.b     r1l, @er0
0x0259E2  mov.l     er6, er0
0x0259E4  inc.l     #1, er6
0x0259E6  mov.b     @er3+, r1l
0x0259E8  mov.b     r1l, @er0
0x0259EA  mov.l     er6, er0
0x0259EC  inc.l     #1, er6
0x0259EE  mov.b     @er3+, r1l
0x0259F0  mov.b     r1l, @er0
0x0259F2  mov.l     er6, er0
0x0259F4  inc.l     #1, er6
0x0259F6  mov.b     @er3, r3l
0x0259F8  mov.b     r3l, @er0
0x0259FA  adds.l    #4, er5
0x0259FC  add.b     #0x03, r4l
0x0259FE  bt        0x025a20
0x025A00  cmp.b     #0x39, r4l
0x025A02  bne       0x025a18
0x025A04  mov.l     er6, er0
0x025A06  inc.l     #1, er6
0x025A08  mov.l     @(0x132,sp), er1
0x025A0E  mov.b     @er1, r1l
0x025A10  add.b     #0x01, r1l
0x025A12  mov.b     r1l, @er0
0x025A14  inc.l     #1, er5
0x025A16  bt        0x025a20
0x025A18  mov.l     er6, er0
0x025A1A  inc.l     #1, er6
0x025A1C  mov.b     @er5+, r1l
0x025A1E  mov.b     r1l, @er0
0x025A20  inc.b     #1, r4l
0x025A22  mov.b     @(0x142,sp), r0l
0x025A26  cmp.b     r0l, r4l
0x025A28  bcs       0x0258b2
0x025A2C  mov.b     @(0x143,sp), r0l
0x025A30  inc.b     #1, r0l
0x025A32  mov.b     r0l, @(0x143,sp)
0x025A36  cmp.b     #0x05, r0l
0x025A38  bcs       0x025840
0x025A3C  mov.l     sp, er0
0x025A3E  mov.w     @(0x138,sp), r1
0x025A42  jsr       0x011900
0x025A46  add.l     #0x00000144, sp
0x025A4C  ldm.l     @sp+, er4-er6
0x025A50  ldm.l     @sp+, er2-er3
0x025A54  rts       
