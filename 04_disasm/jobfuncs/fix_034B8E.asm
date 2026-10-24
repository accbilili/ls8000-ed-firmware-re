0x034A2C  sub.l     er0, er0
0x034A2E  mov.b     @(0x9,sp), r0l
0x034A32  mov.b     @(0x400dab,er0), r0l
0x034A3A  mov.b     r0l, @er5
0x034A3C  extu.w    r0
0x034A3E  mov.w     #0x003a, e0
0x034A42  mulxu.w   e0, er0
0x034A44  mov.b     @(0x400680,er0), r0l
0x034A4C  btst      #5, r0l
0x034A4E  bne       0x034a88
0x034A50  mov.w     @0x41ffb2, r0
0x034A56  extu.l    er0
0x034A58  sub.l     er1, er1
0x034A5A  mov.b     @er5, r1l
0x034A5C  jsr       0x018e1e
0x034A60  mov.w     @0x400d6c, r6
0x034A66  extu.l    er6
0x034A68  add.l     er0, er6
0x034A6A  shll.l    er6
0x034A6C  mov.l     @0x41ffae, er0
0x034A74  add.l     er0, er6
0x034A76  mov.w     @er3, e1
0x034A78  sub.w     r1, r1
0x034A7A  mov.l     er6, er0
0x034A7C  jsr       0x0337a2
0x034A80  jsr       0x0337fe
0x034A84  jmp       0x034b88
0x034A88  sub.l     er0, er0
0x034A8A  mov.b     @er5, r0l
0x034A8C  mov.b     @(0x41ff6e,er0), r0h
0x034A94  mov.b     @er5, r0l
0x034A96  jsr       0x02daa2
0x034A9A  jsr       0x032d2c
0x034A9E  mov.b     #0x02, r0h
0x034AA0  mov.b     #0x08, r0l
0x034AA2  jsr       0x0331f8
0x034AA6  mov.b     #0x01, r6h
0x034AA8  sub.b     r0l, r0l
0x034AAA  mov.b     r0l, @er4
0x034AAC  sub.b     r6l, r6l
0x034AAE  bt        0x034b2a
0x034AB0  mov.b     r6l, r0l
0x034AB2  extu.w    r0
0x034AB4  extu.l    er0
0x034AB6  shll.l    #2, er0
0x034AB8  mov.l     @(0x420224,er0), er1
0x034AC2  bne       0x034ac6
0x034AC4  sub.b     r6h, r6h
0x034AC6  mov.b     r6l, r0l
0x034AC8  extu.w    r0
0x034ACA  extu.l    er0
0x034ACC  shll.l    #2, er0
0x034ACE  mov.l     er0, @(0x4,sp)
0x034AD4  mov.l     @(0x4,sp), er1
0x034ADA  mov.w     @er3, r2
0x034ADC  extu.l    er2
0x034ADE  mov.l     er0, @sp
0x034AE2  mov.w     #0x0003, r0
0x034AE6  divxu.w   r0, er2
0x034AE8  extu.l    er2
0x034AEA  mov.l     @(0x420218,er1), er0
0x034AF4  mov.l     er2, er1
0x034AF6  jsr       0x01872e
0x034AFA  mov.l     @sp, er1
0x034AFE  mov.l     @(0x420230,er1), er1
0x034B08  sub.l     er0, er1
0x034B0A  cmp.l     #0x00000200, er1
0x034B10  bcs       0x034b28
0x034B12  mov.b     r6l, r0l
0x034B14  extu.w    r0
0x034B16  mov.w     #0x0080, r1
0x034B1A  dec.b     #1, r0l
0x034B1C  bmi       0x034b22
0x034B1E  shar.w    r1
0x034B20  bt        0x034b1a
0x034B22  mov.b     @er4, r0l
0x034B24  or.b      r1l, r0l
0x034B26  mov.b     r0l, @er4
0x034B28  inc.b     #1, r6l
0x034B2A  cmp.b     #0x03, r6l
0x034B2C  bcs       0x034ab0
0x034B2E  mov.b     @er4, r0l
0x034B30  and.b     #0xe0, r0l
0x034B32  bne       0x034b6a
0x034B34  mov.w     @0x41ffb2, r0
0x034B3A  extu.l    er0
0x034B3C  sub.l     er1, er1
0x034B3E  mov.b     @er5, r1l
0x034B40  jsr       0x018e1e
0x034B44  mov.w     @0x400d6c, r6
0x034B4A  extu.l    er6
0x034B4C  add.l     er0, er6
0x034B4E  shll.l    er6
0x034B50  mov.l     @0x41ffae, er0
0x034B58  add.l     er0, er6
0x034B5A  mov.w     @er3, e1
0x034B5C  sub.w     r1, r1
0x034B5E  mov.l     er6, er0
0x034B60  jsr       0x0337a2
0x034B64  jsr       0x0337fe
0x034B68  bt        0x034b88
0x034B6A  mov.b     #0x01, r0h
0x034B6C  mov.b     #0x18, r0l
0x034B6E  jsr       0x0331f8
0x034B72  btst      #7, @0x400400
0x034B7A  bne       0x034b9e
0x034B7C  jsr       0x010b56
0x034B80  jsr       0x03db20
0x034B84  jsr       0x010b56
0x034B88  mov.b     @(0x9,sp), r0l
0x034B8C  inc.b     #1, r0l
0x034B8E  mov.b     r0l, @(0x9,sp)
0x034B92  mov.b     @0x400daa, r1l
0x034B98  cmp.b     r1l, r0l
0x034B9A  bcs       0x034a2c
0x034B9E  sub.b     r0l, r0l
0x034BA0  mov.b     r0l, @0x2001c1
0x034BA6  mov.b     #0x80, r0l
0x034BA8  mov.b     r0l, @0x200001
0x034BAE  add.l     #0x0000000a, sp
0x034BB4  ldm.l     @sp+, er4-er6
0x034BB8  ldm.l     @sp+, er2-er3
0x034BBC  rts       
