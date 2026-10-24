0x0269A6  mov.l     er3, @-sp
0x0269AA  stm.l     er4-er6, @-sp
0x0269AE  mov.l     #0x0040043c, er3
0x0269B4  mov.l     #0x00400436, er4
0x0269BA  mov.l     #0x00400c55, er6
0x0269C0  mov.b     @(0x1,er3), r0l
0x0269C4  and.b     #0x1f, r0l
0x0269C6  bne       0x0269d8
0x0269C8  mov.b     #0x02, r5l
0x0269CA  bt        0x0269e2
0x0269CC  mov.b     r5l, r0l
0x0269CE  extu.w    r0
0x0269D0  extu.l    er0
0x0269D2  add.l     er3, er0
0x0269D4  mov.b     @er0, r1l
0x0269D6  beq       0x0269e0
0x0269D8  mov.w     #0x0050, r0
0x0269DC  jmp       0x026bce
0x0269E0  inc.b     #1, r5l
0x0269E2  cmp.b     #0x06, r5l
0x0269E4  bcs       0x0269cc
0x0269E6  mov.l     #0x00400410, er5
0x0269EC  mov.b     @er6, r0l
0x0269EE  cmp.b     #0x40, r0l
0x0269F0  beq       0x026a3e
0x0269F2  cmp.b     #0x41, r0l
0x0269F4  beq       0x026a3e
0x0269F6  cmp.b     #0x42, r0l
0x0269F8  beq       0x026a3e
0x0269FA  cmp.b     #0x80, r0l
0x0269FC  beq       0x026a2e
0x0269FE  cmp.b     #0x81, r0l
0x026A00  beq       0x026bd2
0x026A04  cmp.b     #0x91, r0l
0x026A06  beq       0x026bb2
0x026A0A  cmp.b     #0x92, r0l
0x026A0C  beq       0x026bbe
0x026A10  cmp.b     #0xa0, r0l
0x026A12  beq       0x026a92
0x026A14  cmp.b     #0xb0, r0l
0x026A16  beq       0x026bd2
0x026A1A  cmp.b     #0xb3, r0l
0x026A1C  beq       0x026b0a
0x026A20  cmp.b     #0xc1, r0l
0x026A22  beq       0x026a54
0x026A24  cmp.b     #0xd0, r0l
0x026A26  beq       0x026bd2
0x026A2A  jmp       0x026bca
0x026A2E  mov.b     #0x01, r0l
0x026A30  mov.b     r0l, @0x400d3b
0x026A36  jmp       0x026bee
0x026A3A  jmp       0x026bd2
0x026A3E  mov.b     @(0xa,er6), r0l
0x026A42  extu.w    r0
0x026A44  mov.b     r0l, r0h
0x026A46  sub.b     r0l, r0l
0x026A48  mov.b     @(0xb,er6), r1l
0x026A4C  extu.w    r1
0x026A4E  add.w     r1, r0
0x026A50  sub.w     r0, r0
0x026A52  mov.w     r0, @er5
0x026A54  sub.l     er0, er0
0x026A56  mov.b     @(0x2,er6), r0l
0x026A5A  mov.b     r0l, r0h
0x026A5C  sub.b     r0l, r0l
0x026A5E  mov.w     r0, e0
0x026A60  sub.w     r0, r0
0x026A62  sub.l     er1, er1
0x026A64  mov.b     @(0x3,er6), r1l
0x026A68  mov.w     r1, e1
0x026A6A  sub.w     r1, r1
0x026A6C  add.l     er1, er0
0x026A6E  sub.l     er1, er1
0x026A70  mov.b     @(0x4,er6), r1l
0x026A74  shll.l    #2, er1
0x026A76  shll.l    #2, er1
0x026A78  shll.l    #2, er1
0x026A7A  shll.l    #2, er1
0x026A7C  add.l     er1, er0
0x026A7E  sub.l     er1, er1
0x026A80  mov.b     @(0x5,er6), r1l
0x026A84  add.l     er1, er0
0x026A86  mov.l     er0, @0x400408
0x026A8E  jmp       0x026bd2
0x026A92  sub.l     er0, er0
0x026A94  mov.b     @(0x2,er6), r0l
0x026A98  mov.b     r0l, r0h
0x026A9A  sub.b     r0l, r0l
0x026A9C  mov.w     r0, e0
0x026A9E  sub.w     r0, r0
0x026AA0  sub.l     er1, er1
0x026AA2  mov.b     @(0x3,er6), r1l
0x026AA6  mov.w     r1, e1
0x026AA8  sub.w     r1, r1
0x026AAA  add.l     er1, er0
0x026AAC  sub.l     er1, er1
0x026AAE  mov.b     @(0x4,er6), r1l
0x026AB2  shll.l    #2, er1
0x026AB4  shll.l    #2, er1
0x026AB6  shll.l    #2, er1
0x026AB8  shll.l    #2, er1
0x026ABA  add.l     er1, er0
0x026ABC  sub.l     er1, er1
0x026ABE  mov.b     @(0x5,er6), r1l
0x026AC2  add.l     er1, er0
0x026AC4  mov.l     er0, @0x400408
0x026ACC  sub.l     er0, er0
0x026ACE  mov.b     @(0x6,er6), r0l
0x026AD2  mov.b     r0l, r0h
0x026AD4  sub.b     r0l, r0l
0x026AD6  mov.w     r0, e0
0x026AD8  sub.w     r0, r0
0x026ADA  sub.l     er1, er1
0x026ADC  mov.b     @(0x7,er6), r1l
0x026AE0  mov.w     r1, e1
0x026AE2  sub.w     r1, r1
0x026AE4  add.l     er1, er0
0x026AE6  sub.l     er1, er1
0x026AE8  mov.b     @(0x8,er6), r1l
0x026AEC  shll.l    #2, er1
0x026AEE  shll.l    #2, er1
0x026AF0  shll.l    #2, er1
0x026AF2  shll.l    #2, er1
0x026AF4  add.l     er1, er0
0x026AF6  sub.l     er1, er1
0x026AF8  mov.b     @(0x9,er6), r1l
0x026AFC  add.l     er1, er0
0x026AFE  mov.l     er0, @0x40040c
0x026B06  jmp       0x026bd2
0x026B0A  mov.b     @(0x1,er6), r0l
0x026B0E  mov.b     r0l, @0x400412
0x026B14  sub.l     er0, er0
0x026B16  mov.b     @(0x2,er6), r0l
0x026B1A  mov.b     r0l, r0h
0x026B1C  sub.b     r0l, r0l
0x026B1E  mov.w     r0, e0
0x026B20  sub.w     r0, r0
0x026B22  sub.l     er1, er1
0x026B24  mov.b     @(0x3,er6), r1l
0x026B28  mov.w     r1, e1
0x026B2A  sub.w     r1, r1
0x026B2C  add.l     er1, er0
0x026B2E  sub.l     er1, er1
0x026B30  mov.b     @(0x4,er6), r1l
0x026B34  shll.l    #2, er1
0x026B36  shll.l    #2, er1
0x026B38  shll.l    #2, er1
0x026B3A  shll.l    #2, er1
0x026B3C  add.l     er1, er0
0x026B3E  sub.l     er1, er1
0x026B40  mov.b     @(0x5,er6), r1l
0x026B44  add.l     er1, er0
0x026B46  mov.l     er0, @0x400408
0x026B4E  sub.l     er0, er0
0x026B50  mov.b     @(0x6,er6), r0l
0x026B54  mov.b     r0l, r0h
0x026B56  sub.b     r0l, r0l
0x026B58  mov.w     r0, e0
0x026B5A  sub.w     r0, r0
0x026B5C  sub.l     er1, er1
0x026B5E  mov.b     @(0x7,er6), r1l
0x026B62  mov.w     r1, e1
0x026B64  sub.w     r1, r1
0x026B66  add.l     er1, er0
0x026B68  sub.l     er1, er1
0x026B6A  mov.b     @(0x8,er6), r1l
0x026B6E  shll.l    #2, er1
0x026B70  shll.l    #2, er1
0x026B72  shll.l    #2, er1
0x026B74  shll.l    #2, er1
0x026B76  add.l     er1, er0
0x026B78  sub.l     er1, er1
0x026B7A  mov.b     @(0x9,er6), r1l
0x026B7E  add.l     er1, er0
0x026B80  mov.l     er0, @0x40040c
0x026B88  mov.b     @(0xa,er6), r0l
0x026B8C  extu.w    r0
0x026B8E  mov.b     r0l, r0h
0x026B90  sub.b     r0l, r0l
0x026B92  mov.b     @(0xb,er6), r1l
0x026B96  extu.w    r1
0x026B98  add.w     r1, r0
0x026B9A  mov.w     r0, @er5
0x026B9C  mov.b     @(0xc,er6), r0l
0x026BA0  mov.b     r0l, @0x400413
0x026BA6  mov.b     @(0xd,er6), r0l
0x026BAA  mov.b     r0l, @0x400414
0x026BB0  bt        0x026bd2
0x026BB2  mov.b     @(0x5,er6), r0l
0x026BB6  mov.b     r0l, @0x42029e
0x026BBC  bt        0x026bd2
0x026BBE  mov.b     @(0x5,er6), r0l
0x026BC2  mov.b     r0l, @0x42029f
0x026BC8  bt        0x026bd2
0x026BCA  mov.w     #0x0056, r0
0x026BCE  mov.w     r0, @er4
0x026BD0  bt        0x026bee
0x026BD2  mov.b     @er6, r0l
0x026BD4  extu.w    r0
0x026BD6  bset      #6, r0h
0x026BD8  mov.w     r0, @0x400400
0x026BDE  mov.b     #0x01, r0l
0x026BE0  mov.b     r0l, @0x4007c8
0x026BE6  sub.w     r0, r0
0x026BE8  mov.w     r0, @0x400438
0x026BEE  ldm.l     @sp+, er4-er6
0x026BF2  mov.l     @sp+, er3
0x026BF6  rts       
