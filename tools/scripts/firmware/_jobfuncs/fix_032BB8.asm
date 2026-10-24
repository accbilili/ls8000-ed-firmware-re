0x0329D4  sub.l     er5, er5
0x0329D6  mov.b     @er6, r5l
0x0329D8  mov.l     er5, er4
0x0329DA  shll.l    #2, er4
0x0329DC  mov.l     @(0x400f32,er4), er1
0x0329E6  mov.l     #0x00000028, er0
0x0329EC  add.l     sp, er0
0x0329EE  jsr       0x018e68
0x0329F2  mov.l     er5, er2
0x0329F4  shll.l    #2, er2
0x0329F6  shll.l    er2
0x0329F8  add.l     #0x00420108, er2
0x0329FE  mov.l     er0, er1
0x032A00  mov.l     #0x00000020, er0
0x032A06  add.l     sp, er0
0x032A08  jsr       0x018aa0
0x032A0C  mov.l     er0, er1
0x032A0E  mov.l     #0x0003f7e6, er2
0x032A14  mov.l     #0x00000018, er0
0x032A1A  add.l     sp, er0
0x032A1C  jsr       0x018aa0
0x032A20  mov.l     er0, er1
0x032A22  mov.l     #0x0003f7ee, er2
0x032A28  mov.l     #0x00000010, er0
0x032A2E  add.l     sp, er0
0x032A30  jsr       0x01842c
0x032A34  jsr       0x01876a
0x032A38  mov.l     @(0x400f42,er4), er1
0x032A42  add.l     er1, er0
0x032A44  mov.l     er0, @0x420248
0x032A4C  bne       0x032a5c
0x032A4E  mov.l     #0x00000001, er0
0x032A54  mov.l     er0, @0x420248
0x032A5C  mov.b     @er6, r1l
0x032A5E  extu.w    r1
0x032A60  mov.w     #0x0006, e1
0x032A64  mulxu.w   e1, er1
0x032A66  add.l     #0x0041ff3e, er1
0x032A6C  mov.b     @er6, r0l
0x032A6E  jsr       0x02da8e
0x032A72  sub.l     er0, er0
0x032A74  mov.b     @er6, r0l
0x032A76  mov.b     @(0x41ff6e,er0), r0h
0x032A7E  mov.b     @er6, r0l
0x032A80  jsr       0x02daa2
0x032A84  mov.b     #0x03, r0h
0x032A86  mov.b     #0x01, r0l
0x032A88  bsr       0x03316c
0x032A8C  mov.w     @0x41ff74, r1
0x032A92  mov.w     @0x41ff72, r0
0x032A98  sub.w     r0, r1
0x032A9A  mov.l     #0x00000028, er0
0x032AA0  add.l     sp, er0
0x032AA2  jsr       0x018ede
0x032AA6  mov.w     @0x41ff74, r1
0x032AAC  mov.l     er0, @(0x1c,sp)
0x032AB2  mov.l     #0x00000020, er0
0x032AB8  add.l     sp, er0
0x032ABA  jsr       0x018ede
0x032ABE  mov.l     @(0x1c,sp), er1
0x032AC4  mov.l     er0, er2
0x032AC6  mov.l     #0x00000014, er0
0x032ACC  add.l     sp, er0
0x032ACE  jsr       0x01842c
0x032AD2  mov.l     er0, er1
0x032AD4  mov.l     #0x0003f7ee, er2
0x032ADA  mov.l     #0x0000000c, er0
0x032AE0  add.l     sp, er0
0x032AE2  jsr       0x018aa0
0x032AE6  mov.b     @0x03f7a4, r1l
0x032AEC  extu.w    r1
0x032AEE  mov.l     er0, @sp
0x032AF2  mov.l     #0x00000004, er0
0x032AF8  add.l     sp, er0
0x032AFA  jsr       0x018ede
0x032AFE  mov.l     er0, er1
0x032B00  mov.l     @sp, er0
0x032B04  jsr       0x0188d2
0x032B08  mov.w     r0, r0
0x032B0A  beq       0x032b1c
0x032B0C  mov.b     @er6, r0l
0x032B0E  extu.w    r0
0x032B10  inc.w     #1, r0
0x032B12  or.w      #0x0880, r0
0x032B16  mov.w     r0, @er3
0x032B18  jmp       0x032bc0
0x032B1C  sub.b     r0h, r0h
0x032B1E  mov.b     #0x10, r0l
0x032B20  bsr       0x03316c
0x032B24  mov.l     #0x00400f5a, er4
0x032B2A  mov.w     @0x400d6a, r0
0x032B30  extu.l    er0
0x032B32  shll.l    er0
0x032B34  add.l     er4, er0
0x032B36  mov.l     er0, @(0x50,sp)
0x032B3C  mov.w     #0x5a00, r0
0x032B40  mov.w     r0, @0xffffbc
0x032B46  mov.w     @er4+, e5
0x032B48  mov.l     @(0x50,sp), er0
0x032B4E  cmp.l     er0, er4
0x032B50  bcc       0x032bb4
0x032B52  mov.w     @er4+, r5
0x032B54  cmp.w     e5, r5
0x032B56  bcs       0x032b7e
0x032B58  mov.w     r5, r0
0x032B5A  sub.w     e5, r0
0x032B5C  mov.b     @0x03f7a5, r1l
0x032B62  extu.w    r1
0x032B64  mov.w     #0x0064, r2
0x032B68  extu.l    er2
0x032B6A  divxu.w   r1, er2
0x032B6C  mov.w     r2, e0
0x032B6E  add.w     r5, r2
0x032B70  dec.w     #1, r2
0x032B72  extu.l    er2
0x032B74  mov.w     e0, r1
0x032B76  divxu.w   r1, er2
0x032B78  cmp.w     r2, r0
0x032B7A  bls       0x032bb0
0x032B7C  bt        0x032ba2
0x032B7E  mov.w     e5, r0
0x032B80  sub.w     r5, r0
0x032B82  mov.b     @0x03f7a5, r1l
0x032B88  extu.w    r1
0x032B8A  mov.w     #0x0064, r2
0x032B8E  extu.l    er2
0x032B90  divxu.w   r1, er2
0x032B92  mov.w     r2, e0
0x032B94  add.w     e5, r2
0x032B96  dec.w     #1, r2
0x032B98  extu.l    er2
0x032B9A  mov.w     e0, r1
0x032B9C  divxu.w   r1, er2
0x032B9E  cmp.w     r2, r0
0x032BA0  bls       0x032bb0
0x032BA2  mov.b     @er6, r0l
0x032BA4  extu.w    r0
0x032BA6  inc.w     #1, r0
0x032BA8  or.w      #0x0880, r0
0x032BAC  mov.w     r0, @er3
0x032BAE  bt        0x032bcc
0x032BB0  mov.w     r5, e5
0x032BB2  bt        0x032b48
0x032BB4  mov.b     @er6, r0l
0x032BB6  inc.b     #1, r0l
0x032BB8  mov.b     r0l, @er6
0x032BBA  cmp.b     #0x04, r0l
0x032BBC  bcs       0x0329d4
0x032BC0  jsr       0x02d694
0x032BC4  sub.b     r0l, r0l
0x032BC6  mov.b     r0l, @0x420246
0x032BCC  add.l     #0x00000056, sp
0x032BD2  ldm.l     @sp+, er4-er6
0x032BD6  ldm.l     @sp+, er2-er3
0x032BDA  rts       
