0x018708  mov.w     r2, @-sp
0x01870A  mov.w     e0, r2
0x01870C  mov.b     r2h, r2l
0x01870E  bpl       0x018712
0x018710  neg.l     er0
0x018712  mov.w     e1, e1
0x018714  bpl       0x01871a
0x018716  xor.b     #0x80, r2h
0x018718  neg.l     er1
0x01871A  jsr       0x01872e
0x01871E  mov.b     r2h, r2h
0x018720  bpl       0x018724
0x018722  neg.l     er0
0x018724  mov.b     r2l, r2l
0x018726  bpl       0x01872a
0x018728  neg.l     er1
0x01872A  mov.w     @sp+, r2
0x01872C  rts       
0x029D2A  stm.l     er4-er6, @-sp
0x029D2E  mov.l     #0x00420301, er6
0x029D34  mov.b     r0l, r4l
0x029D36  sub.b     r0l, r0l
0x029D38  mov.b     r0l, @er6
0x029D3A  mov.l     #0x00ffff2f, er0
0x029D40  mov.b     @er0, r1l
0x029D42  and.b     #0xbe, r1l
0x029D44  mov.b     r1l, @er0
0x029D46  mov.b     @0x400d72, r0l
0x029D4C  cmp.b     #0x05, r0l
0x029D4E  bne       0x029d68
0x029D50  jsr       0x02cfa0
0x029D54  cmp.b     #0x01, r0l
0x029D56  beq       0x029d68
0x029D58  jsr       0x02cf60
0x029D5C  cmp.b     #0x01, r0l
0x029D5E  beq       0x029d68
0x029D60  jsr       0x02cfe0
0x029D64  cmp.b     #0x01, r0l
0x029D66  bne       0x029d6c
0x029D68  bset      #6, @er6
0x029D6C  mov.l     #0x004202ff, er5
0x029D72  sub.b     r0l, r0l
0x029D74  mov.b     r0l, @er5
0x029D76  mov.b     r4l, r4l
0x029D78  beq       0x029db4
0x029D7A  jsr       0x02cfa0
0x029D7E  cmp.b     #0x01, r0l
0x029D80  bne       0x029dac
0x029D82  mov.w     @0x4202ec, r0
0x029D88  mov.w     #0x000c, e0
0x029D8C  mulxu.w   e0, er0
0x029D8E  mov.w     @0x4202a2, r1
0x029D94  add.w     r0, r1
0x029D96  sub.l     er0, er0
0x029D98  mov.b     @0x4003fb, r0l
0x029D9E  shll.l    er0
0x029DA0  mov.w     @(0x3ee10,er0), r0
0x029DA8  cmp.w     r0, r1
0x029DAA  bcs       0x029db4
0x029DAC  mov.b     #0x01, r0l
0x029DAE  mov.b     r0l, @er5
0x029DB0  bset      #0, @er6
0x029DB4  ldm.l     @sp+, er4-er6
0x029DB8  rts       
0x02A2F6  mov.l     er3, @-sp
0x02A2FA  stm.l     er4-er6, @-sp
0x02A2FE  mov.l     #0x004202a4, er4
0x02A304  mov.l     #0x00440e36, er6
0x02A30A  mov.b     r0l, r5l
0x02A30C  mov.w     e0, e5
0x02A30E  mov.w     r1, r3
0x02A310  mov.b     r0h, r5h
0x02A312  mov.b     r5l, r5l
0x02A314  bne       0x02a31c
0x02A316  mov.b     #0x01, r0l
0x02A318  jsr       0x029d2a
0x02A31C  sub.b     r0l, r0l
0x02A31E  mov.b     r0l, @0x44080f
0x02A324  mov.b     #0x01, r0l
0x02A326  mov.b     r0l, @er4
0x02A328  mov.l     @(0x14,sp), er0
0x02A32E  beq       0x02a33a
0x02A330  mov.l     @(0x14,sp), er0
0x02A336  bsr       0x02a4fe
0x02A33A  cmp.w     #0x0172, e5
0x02A33E  bcs       0x02a346
0x02A340  mov.w     #0x02df, r0
0x02A344  bt        0x02a348
0x02A346  sub.w     r0, r0
0x02A348  mov.w     r0, @er6
0x02A34A  mov.w     r3, @0x4202a0
0x02A350  mov.b     #0x10, r0l
0x02A352  mov.b     r0l, @0x440811
0x02A358  sub.w     r0, r0
0x02A35A  mov.w     r0, @0x440e38
0x02A360  sub.w     r0, r0
0x02A362  mov.w     r0, @0x440e3e
0x02A368  mov.l     #0x00440e3c, er3
0x02A36E  mov.w     e5, @er3
0x02A370  mov.w     @er6, r0
0x02A372  beq       0x02a3a0
0x02A374  mov.b     @0x440811, r0l
0x02A37A  extu.w    r0
0x02A37C  exts.l    er0
0x02A37E  mov.w     #0x0004, r1
0x02A382  divxs.w   r1, er0
0x02A386  mov.w     @er6, r1
0x02A388  extu.l    er1
0x02A38A  divxu.w   r0, er1
0x02A38C  mov.w     r1, @0x440e3a
0x02A392  mov.w     @0x440e3a, r0
0x02A398  shll.w    r0
0x02A39A  mov.w     @er3, r1
0x02A39C  sub.w     r0, r1
0x02A39E  mov.w     r1, @er3
0x02A3A0  mov.b     r5l, @0x440810
0x02A3A6  mov.b     r5h, @0x4202a9
0x02A3AC  mov.l     @(0x18,sp), er0
0x02A3B2  mov.l     er0, @0x4202aa
0x02A3BA  mov.b     r5l, r0l
0x02A3BC  bsr       0x02a55c
0x02A3C0  bsr       0x02a3ee
0x02A3C2  mov.l     @(0x14,sp), er0
0x02A3C8  bne       0x02a3dc
0x02A3CA  mov.w     @er6, r0
0x02A3CC  bne       0x02a3d2
0x02A3CE  mov.b     #0x03, r0l
0x02A3D0  bt        0x02a3d4
0x02A3D2  mov.b     #0x04, r0l
0x02A3D4  mov.b     r0l, @er4
0x02A3D6  bsr       0x02a788
0x02A3DA  bt        0x02a3e4
0x02A3DC  bset      #0, @0xfffe84
0x02A3E4  ldm.l     @sp+, er4-er6
0x02A3E8  mov.l     @sp+, er3
0x02A3EC  rts       
0x02A3EE  mov.l     #0x00ffff48, er0
0x02A3F4  mov.w     @er0, r1
0x02A3F6  or.w      #0x00ff, r1
0x02A3FA  mov.w     r1, @er0
0x02A3FC  mov.b     @0x440846, r0l
0x02A402  bsr       0x02b11a
0x02A406  bclr      #0, @0xffffc0
0x02A40E  mov.b     #0x22, r0l
0x02A410  mov.b     r0l, @0xffffd0
0x02A416  mov.b     @0xffffd5, r0l
0x02A41C  mov.b     r0l, @0x40041b
0x02A422  bclr      #0, @0xffffd5
0x02A42A  mov.l     #0x00ffffd4, er0
0x02A430  mov.b     @er0, r1l
0x02A432  and.b     #0x60, r1l
0x02A434  mov.b     r1l, @er0
0x02A436  bset      #0, @0xffffd4
0x02A43E  mov.w     @0x440e36, r0
0x02A444  beq       0x02a44e
0x02A446  mov.w     @0x440850, r0
0x02A44C  bt        0x02a454
0x02A44E  mov.w     @0x440e1a, r0
0x02A454  mov.w     r0, @0xffffd8
0x02A45A  mov.b     @0xffff07, r0l
0x02A460  mov.b     r0l, @0x40041b
0x02A466  mov.w     @0xffff06, r0
0x02A46C  and.w     #0xaccc, r0
0x02A470  or.w      #0x0332, r0
0x02A474  mov.w     r0, @0xffff06
0x02A47A  mov.b     #0x28, r0l
0x02A47C  mov.b     r0l, @0xffff02
0x02A482  mov.b     @0x440811, r0l
0x02A488  mov.b     r0l, @0xfffee7
0x02A48E  mov.b     r0l, @0xfffee6
0x02A494  mov.l     #0x00440812, er0
0x02A49A  mov.l     er0, @0xfffee0
0x02A4A2  mov.w     #0xff4d, r0
0x02A4A6  mov.w     r0, @0xfffee4
0x02A4AC  mov.b     #0x88, r0l
0x02A4AE  mov.b     r0l, @0xffff03
0x02A4B4  mov.b     @0x440811, r0l
0x02A4BA  extu.w    r0
0x02A4BC  shlr.w    #2, r0
0x02A4BE  mov.w     r0, @0xfffeee
0x02A4C4  mov.w     @0x440e36, r0
0x02A4CA  beq       0x02a4d4
0x02A4CC  mov.l     #0x00440852, er0
0x02A4D2  bt        0x02a4da
0x02A4D4  mov.l     #0x00440e1c, er0
0x02A4DA  mov.l     er0, @0xfffee8
0x02A4E2  mov.w     #0xffd8, r0
0x02A4E6  mov.w     r0, @0xfffeec
0x02A4EC  sub.w     r0, r0
0x02A4EE  mov.w     r0, @0xffffd6
0x02A4F4  mov.b     #0x01, r0l
0x02A4F6  mov.b     r0l, @0x4003ff
0x02A4FC  rts       
0x02A4FE  mov.l     er6, @-sp
0x02A502  mov.l     er0, er6
0x02A504  mov.l     #0x0044084e, er0
0x02A50A  mov.l     er0, @-sp
0x02A50E  mov.l     er6, er0
0x02A510  mov.l     #0x000003e8, er1
0x02A516  jsr       0x018e1e
0x02A51A  mov.l     #0x00000280, er1
0x02A520  jsr       0x01872e
0x02A524  mov.l     #0x0044084c, er1
0x02A52A  bsr       0x02b1e4
0x02A52E  adds.l    #4, sp
0x02A530  mov.b     @0x44084c, r0l
0x02A536  mov.b     r0l, @0x44084d
0x02A53C  mov.w     @0x44084e, e0
0x02A542  bsr       0x02b22e
0x02A546  mov.b     #0x01, r0l
0x02A548  mov.b     r0l, @0x4003fe
0x02A54E  bset      #3, @0xffffc0
0x02A556  mov.l     @sp+, er6
0x02A55A  rts       
0x02A55C  mov.w     r6, @-sp
0x02A55E  mov.b     r0l, r6l
0x02A560  bsr       0x02a56a
0x02A562  bsr       0x02a664
0x02A566  mov.w     @sp+, r6
0x02A568  rts       
0x02A56A  stm.l     er2-er3, @-sp
0x02A56E  stm.l     er4-er6, @-sp
0x02A572  sub.l     #0x0000000a, sp
0x02A578  mov.b     r0l, r2l
0x02A57A  mov.l     #0x0003f0e8, er4
0x02A580  mov.l     er4, er6
0x02A582  mov.b     @0x440811, r1l
0x02A588  extu.w    r1
0x02A58A  dec.w     #1, r1
0x02A58C  mov.w     r1, r5
0x02A58E  sub.w     e1, e1
0x02A590  bt        0x02a5a2
0x02A592  mov.b     @er6, r0l
0x02A594  mov.b     @0x440846, r1l
0x02A59A  cmp.b     r1l, r0l
0x02A59C  beq       0x02a5a6
0x02A59E  inc.l     #1, er6
0x02A5A0  inc.w     #1, e1
0x02A5A2  cmp.w     r5, e1
0x02A5A4  ble       0x02a592
0x02A5A6  mov.l     #0x00000002, er3
0x02A5AC  mov.b     r2l, r0l
0x02A5AE  bne       0x02a5d2
0x02A5B0  mov.l     er6, er0
0x02A5B2  add.l     er3, er0
0x02A5B4  mov.w     r5, r1
0x02A5B6  exts.l    er1
0x02A5B8  add.l     er4, er1
0x02A5BA  cmp.l     er1, er0
0x02A5BC  bls       0x02a5ce
0x02A5BE  add.l     er6, er3
0x02A5C0  sub.l     er0, er0
0x02A5C2  mov.b     @0x440811, r0l
0x02A5C8  sub.l     er0, er3
0x02A5CA  mov.l     er3, er6
0x02A5CC  bt        0x02a5ee
0x02A5CE  add.l     er3, er6
0x02A5D0  bt        0x02a5ee
0x02A5D2  mov.l     er6, er0
0x02A5D4  sub.l     er3, er0
0x02A5D6  cmp.l     er4, er0
0x02A5D8  bcc       0x02a5ec
0x02A5DA  mov.l     er6, er0
0x02A5DC  sub.l     er3, er0
0x02A5DE  sub.l     er1, er1
0x02A5E0  mov.b     @0x440811, r1l
0x02A5E6  add.l     er1, er0
0x02A5E8  mov.l     er0, er6
0x02A5EA  bt        0x02a5ee
0x02A5EC  sub.l     er3, er6
0x02A5EE  mov.l     #0x00440812, er0
0x02A5F4  mov.l     er0, @(0x6,sp)
0x02A5FA  mov.b     r2l, r0l
0x02A5FC  bne       0x02a604
0x02A5FE  mov.w     #0x0001, r3
0x02A602  bt        0x02a608
0x02A604  mov.w     #0xffff, r3
0x02A608  sub.w     e1, e1
0x02A60A  mov.w     r5, r0
0x02A60C  exts.l    er0
0x02A60E  add.l     er4, er0
0x02A610  mov.l     er0, er2
0x02A612  bt        0x02a63e
0x02A614  mov.l     @(0x6,sp), er0
0x02A61A  inc.l     #1, er0
0x02A61C  mov.l     er0, @(0x6,sp)
0x02A622  dec.l     #1, er0
0x02A624  mov.b     @er6, r1l
0x02A626  mov.b     r1l, @er0
0x02A628  mov.w     r3, r0
0x02A62A  exts.l    er0
0x02A62C  add.l     er0, er6
0x02A62E  mov.l     er2, er0
0x02A630  cmp.l     er0, er6
0x02A632  bls       0x02a636
0x02A634  mov.l     er4, er6
0x02A636  cmp.l     er4, er6
0x02A638  bcc       0x02a63c
0x02A63A  mov.l     er2, er6
0x02A63C  inc.w     #1, e1
0x02A63E  cmp.w     r5, e1
0x02A640  ble       0x02a614
0x02A642  mov.w     r5, r0
0x02A644  exts.l    er0
0x02A646  add.l     #0x00440811, er0
0x02A64C  mov.l     er0, @0x440848
0x02A654  add.l     #0x0000000a, sp
0x02A65A  ldm.l     @sp+, er4-er6
0x02A65E  ldm.l     @sp+, er2-er3
0x02A662  rts       
0x02A664  stm.l     er2-er3, @-sp
0x02A668  stm.l     er4-er6, @-sp
0x02A66C  mov.l     #0x004202a0, er3
0x02A672  mov.l     #0x00440850, er5
0x02A678  mov.l     #0x00440e36, er6
0x02A67E  mov.w     @er6, r0
0x02A680  beq       0x02a744
0x02A684  sub.w     r4, r4
0x02A686  bt        0x02a6c8
0x02A688  mov.w     #0x5a00, r0
0x02A68C  mov.w     r0, @0xffffbc
0x02A692  mov.w     @er3, r0
0x02A694  sub.w     #0x09c4, r0
0x02A698  extu.l    er0
0x02A69A  mov.w     @er6, r2
0x02A69C  divxu.w   r2, er0
0x02A69E  mulxu.w   r4, er0
0x02A6A0  add.w     #0x09c4, r0
0x02A6A4  extu.l    er0
0x02A6A6  mov.l     er0, er1
0x02A6A8  mov.l     #0x0017d784, er0
0x02A6AE  jsr       0x018708
0x02A6B2  mov.w     r4, r1
0x02A6B4  exts.l    er1
0x02A6B6  shll.l    er1
0x02A6B8  add.l     er5, er1
0x02A6BA  mov.w     r0, @er1
0x02A6BC  mov.w     #0x5a00, r0
0x02A6C0  mov.w     r0, @0xffffbc
0x02A6C6  inc.w     #1, r4
0x02A6C8  mov.w     @er6, r0
0x02A6CA  cmp.w     r0, r4
0x02A6CC  bls       0x02a688
0x02A6CE  mov.w     @er6, r4
0x02A6D0  extu.l    er4
0x02A6D2  shll.l    er4
0x02A6D4  add.l     er5, er4
0x02A6D6  mov.w     @er4, r0
0x02A6D8  mov.w     r0, @(0x2,er4)
0x02A6DC  mov.w     @er6, r4
0x02A6DE  extu.l    er4
0x02A6E0  shll.l    er4
0x02A6E2  add.l     er5, er4
0x02A6E4  mov.w     @er4, r0
0x02A6E6  mov.w     r0, @(0x4,er4)
0x02A6EA  mov.w     @er6, r4
0x02A6EC  extu.l    er4
0x02A6EE  shll.l    er4
0x02A6F0  add.l     er5, er4
0x02A6F2  mov.w     @er4, r0
0x02A6F4  mov.w     r0, @(0x6,er4)
0x02A6F8  mov.w     @er6, r4
0x02A6FA  extu.l    er4
0x02A6FC  shll.l    er4
0x02A6FE  add.l     er5, er4
0x02A700  mov.w     @er4, r0
0x02A702  mov.w     r0, @(0x8,er4)
0x02A706  mov.w     @er6, r4
0x02A708  extu.l    er4
0x02A70A  shll.l    er4
0x02A70C  add.l     er5, er4
0x02A70E  mov.w     @er4, r0
0x02A710  mov.w     r0, @(0xa,er4)
0x02A714  mov.w     @er6, r4
0x02A716  extu.l    er4
0x02A718  shll.l    er4
0x02A71A  add.l     er5, er4
0x02A71C  mov.w     @er4, r0
0x02A71E  mov.w     r0, @(0xc,er4)
0x02A722  mov.w     @er6, r4
0x02A724  extu.l    er4
0x02A726  shll.l    er4
0x02A728  add.l     er5, er4
0x02A72A  mov.w     @er4, r0
0x02A72C  mov.w     r0, @(0xe,er4)
0x02A730  mov.w     @er6, r0
0x02A732  extu.l    er0
0x02A734  shll.l    er0
0x02A736  add.l     er5, er0
0x02A738  add.l     #0x00000010, er0
0x02A73E  mov.w     #0xffff, r1
0x02A742  mov.w     r1, @er0
0x02A744  sub.w     r4, r4
0x02A746  mov.w     @er3, r1
0x02A748  extu.l    er1
0x02A74A  mov.l     #0x3b9aca00, er0
0x02A750  jsr       0x018708
0x02A754  mov.l     #0x00000280, er1
0x02A75A  jsr       0x018708
0x02A75E  mov.w     r4, r1
0x02A760  exts.l    er1
0x02A762  shll.l    er1
0x02A764  mov.w     r0, @(0x440e1a,er1)
0x02A76C  inc.w     #1, r4
0x02A76E  cmp.w     #0x0009, r4
0x02A772  blt       0x02a746
0x02A774  mov.w     #0xffff, r0
0x02A778  mov.w     r0, @0x440e2c
0x02A77E  ldm.l     @sp+, er4-er6
0x02A782  ldm.l     @sp+, er2-er3
0x02A786  rts       
0x02A788  mov.b     @0xffff46, r0l
0x02A78E  and.b     #0xf0, r0l
0x02A790  mov.b     r0l, @0xffff46
0x02A796  mov.b     @0xffff47, r0l
0x02A79C  and.b     #0xcc, r0l
0x02A79E  or.b      #0x30, r0l
0x02A7A0  mov.b     r0l, @0xffff47
0x02A7A6  mov.l     @0x440848, er0
0x02A7AE  mov.b     @(0x1,er0), r0l
0x02A7B2  mov.b     r0l, @0xffff4d
0x02A7B8  mov.b     @0xffffd5, r0l
0x02A7BE  mov.b     r0l, @0x40041b
0x02A7C4  bclr      #0, @0xffffd5
0x02A7CC  bset      #0, @0xffffc0
0x02A7D4  mov.b     @0x440810, r0l
0x02A7DA  bne       0x02a7f4
0x02A7DC  mov.b     @0xffff2e, r0l
0x02A7E2  and.b     #0xbe, r0l
0x02A7E4  mov.b     @0x420301, r1l
0x02A7EA  and.b     #0x41, r1l
0x02A7EC  or.b      r1l, r0l
0x02A7EE  mov.b     r0l, @0xffff2e
0x02A7F4  rts       
0x02AFA4  mov.l     er6, @-sp
0x02AFA8  mov.l     #0x0044080e, er6
0x02AFAE  mov.b     #0x01, r0l
0x02AFB0  mov.b     r0l, @er6
0x02AFB2  jsr       0x02cf40
0x02AFB6  cmp.b     #0x01, r0l
0x02AFB8  bne       0x02afd0
0x02AFBA  mov.b     @0x44080e, r0l
0x02AFC0  cmp.b     #0x01, r0l
0x02AFC2  bne       0x02afd0
0x02AFC4  mov.b     #0x02, r0l
0x02AFC6  mov.b     r0l, @er6
0x02AFC8  mov.b     #0x01, r0l
0x02AFCA  mov.b     r0l, @0x44080f
0x02AFD0  mov.b     @0x4202a4, r0l
0x02AFD6  beq       0x02afde
0x02AFD8  jsr       0x010b56
0x02AFDC  bt        0x02afb2
0x02AFDE  mov.b     @er6, r0l
0x02AFE0  cmp.b     #0x02, r0l
0x02AFE2  beq       0x02afee
0x02AFE4  mov.w     #0x0110, r0
0x02AFE8  mov.w     r0, @0x400402
0x02AFEE  mov.l     @sp+, er6
0x02AFF2  rts       
0x02AFF4  mov.l     er6, @-sp
0x02AFF8  mov.l     #0x0044080e, er6
0x02AFFE  mov.b     #0x02, r0l
0x02B000  mov.b     r0l, @er6
0x02B002  jsr       0x02cf40
0x02B006  mov.b     r0l, r0l
0x02B008  bne       0x02b014
0x02B00A  mov.b     #0x01, r0l
0x02B00C  mov.b     r0l, @er6
0x02B00E  mov.b     r0l, @0x4202a8
0x02B014  mov.b     @0x4202a4, r0l
0x02B01A  beq       0x02b022
0x02B01C  jsr       0x010b56
0x02B020  bt        0x02b002
0x02B022  mov.b     @er6, r0l
0x02B024  cmp.b     #0x01, r0l
0x02B026  beq       0x02b032
0x02B028  mov.w     #0x0110, r0
0x02B02C  mov.w     r0, @0x400402
0x02B032  mov.l     @sp+, er6
0x02B036  rts       
0x02B038  mov.l     #0x00ffff48, er0
0x02B03E  mov.w     @er0, r1
0x02B040  and.w     #0xff00, r1
0x02B044  mov.w     r1, @er0
0x02B046  mov.l     #0x00ffff4b, er0
0x02B04C  mov.w     @er0, r1
0x02B04E  or.w      #0x00fc, r1
0x02B052  mov.w     r1, @er0
0x02B054  mov.l     #0x00ffff48, er0
0x02B05A  mov.w     @er0, r1
0x02B05C  or.w      #0x00ff, r1
0x02B060  mov.w     r1, @er0
0x02B062  mov.b     @0x03f0e8, r0l
0x02B068  mov.b     r0l, @0x440846
0x02B06E  jsr       0x02cf40
0x02B072  mov.b     r0l, r0l
0x02B074  bne       0x02b0ae
0x02B076  sub.b     r0l, r0l
0x02B078  mov.b     r0l, @0x4202a8
0x02B07E  mov.l     #0x000186a0, er0
0x02B084  mov.l     er0, @-sp
0x02B088  sub.l     er0, er0
0x02B08A  mov.l     er0, @-sp
0x02B08E  sub.b     r0h, r0h
0x02B090  mov.w     #0x2710, r1
0x02B094  mov.w     #0x4517, e0
0x02B098  sub.b     r0l, r0l
0x02B09A  bsr       0x02a2f6
0x02B09E  adds.l    #4, sp
0x02B0A0  adds.l    #4, sp
0x02B0A2  bsr       0x02afa4
0x02B0A6  sub.w     r0, r0
0x02B0A8  mov.w     r0, @0x4202a2
0x02B0AE  mov.l     #0x000186a0, er0
0x02B0B4  mov.l     er0, @-sp
0x02B0B8  sub.l     er0, er0
0x02B0BA  mov.l     er0, @-sp
0x02B0BE  sub.b     r0h, r0h
0x02B0C0  mov.w     #0x09c4, r1
0x02B0C4  mov.w     #0x092b, e0
0x02B0C8  mov.b     #0x01, r0l
0x02B0CA  bsr       0x02a2f6
0x02B0CE  adds.l    #4, sp
0x02B0D0  adds.l    #4, sp
0x02B0D2  bsr       0x02aff4
0x02B0D6  sub.w     r0, r0
0x02B0D8  mov.w     r0, @0x4202a2
0x02B0DE  sub.b     r0l, r0l
0x02B0E0  mov.b     r0l, @0x4202a8
0x02B0E6  rts       
0x02B11A  stm.l     er4-er5, @-sp
0x02B11E  mov.l     #0x00ffffc0, er5
0x02B124  mov.l     #0x00ffffd5, er4
0x02B12A  mov.b     r0l, r1h
0x02B12C  bclr      #0, @er5
0x02B130  sub.w     r0, r0
0x02B132  mov.w     r0, @0xffffd6
0x02B138  mov.b     #0x20, r0l
0x02B13A  mov.b     r0l, @0xffffd0
0x02B140  bclr      #0, @er4
0x02B144  mov.l     #0x00ffffd4, er0
0x02B14A  mov.b     @er0, r1l
0x02B14C  and.b     #0x60, r1l
0x02B14E  mov.b     r1l, @er0
0x02B150  mov.w     #0x0001, r0
0x02B154  mov.w     r0, @0xffffd8
0x02B15A  mov.b     @0xffff46, r0l
0x02B160  and.b     #0xf0, r0l
0x02B162  mov.b     r0l, @0xffff46
0x02B168  mov.b     @0xffff47, r0l
0x02B16E  and.b     #0xf0, r0l
0x02B170  or.b      #0x30, r0l
0x02B172  mov.b     r0l, @0xffff47
0x02B178  mov.b     r1h, @0xffff4d
0x02B17E  bset      #0, @er5
0x02B182  btst      #0, @er4
0x02B186  beq       0x02b182
0x02B188  bclr      #0, @er5
0x02B18C  bclr      #0, @er4
0x02B190  ldm.l     @sp+, er4-er5
0x02B194  rts       
0x02B1E4  stm.l     er4-er5, @-sp
0x02B1E8  mov.l     er0, er4
0x02B1EA  mov.l     @(0xc,sp), er5
0x02B1F0  cmp.l     #0x00010000, er4
0x02B1F6  bcc       0x02b200
0x02B1F8  mov.w     r4, @er5
0x02B1FA  mov.b     #0x01, r0l
0x02B1FC  mov.b     r0l, @er1
0x02B1FE  bt        0x02b228
0x02B200  cmp.l     #0x007fffff, er4
0x02B206  bcc       0x02b21e
0x02B208  mov.w     r4, r0
0x02B20A  bclr      #7, r0h
0x02B20C  add.w     #0x8000, r0
0x02B210  mov.w     r0, @er5
0x02B212  mov.b     #0x0f, r0l
0x02B214  shlr.l    er4
0x02B216  dec.b     #1, r0l
0x02B218  bgt       0x02b214
0x02B21A  mov.b     r4l, @er1
0x02B21C  bt        0x02b228
0x02B21E  mov.w     #0xffff, r0
0x02B222  mov.w     r0, @er5
0x02B224  mov.b     #0xff, r0l
0x02B226  mov.b     r0l, @er1
0x02B228  ldm.l     @sp+, er4-er5
0x02B22C  rts       
0x02B22E  mov.b     r0l, r1h
0x02B230  mov.w     e0, e1
0x02B232  bclr      #3, @0xffffc0
0x02B23A  mov.b     #0x22, r0l
0x02B23C  mov.b     r0l, @0xfffe80
0x02B242  bclr      #0, @0xfffe85
0x02B24A  sub.w     r0, r0
0x02B24C  mov.w     r0, @0xfffe86
0x02B252  mov.l     #0x00fffe84, er0
0x02B258  mov.b     @er0, r1l
0x02B25A  and.b     #0x60, r1l
0x02B25C  mov.b     r1l, @er0
0x02B25E  cmp.b     #0x01, r1h
0x02B260  bne       0x02b26a
0x02B262  mov.w     e1, @0xfffe88
0x02B268  rts       
0x02B26A  mov.w     #0x8000, r0
0x02B26E  mov.w     r0, @0xfffe88
0x02B274  rts       
0x02CF40  sub.b     r1l, r1l
0x02CF42  sub.w     r0, r0
0x02CF44  bt        0x02cf56
0x02CF46  btst      #3, @0xffff55
0x02CF4E  bne       0x02cf54
0x02CF50  mov.b     #0x01, r1l
0x02CF52  bt        0x02cf5c
0x02CF54  inc.w     #1, r0
0x02CF56  cmp.w     #0x0014, r0
0x02CF5A  blt       0x02cf46
0x02CF5C  mov.b     r1l, r0l
0x02CF5E  rts       
0x02CF60  sub.b     r1l, r1l
0x02CF62  sub.w     r0, r0
0x02CF64  bt        0x02cf76
0x02CF66  btst      #2, @0xffff55
0x02CF6E  bne       0x02cf74
0x02CF70  mov.b     #0x01, r1l
0x02CF72  bt        0x02cf7c
0x02CF74  inc.w     #1, r0
0x02CF76  cmp.w     #0x0014, r0
0x02CF7A  blt       0x02cf66
0x02CF7C  mov.b     r1l, r0l
0x02CF7E  rts       
0x02CFA0  sub.b     r1l, r1l
0x02CFA2  sub.w     r0, r0
0x02CFA4  bt        0x02cfb6
0x02CFA6  btst      #5, @0xffff55
0x02CFAE  bne       0x02cfb4
0x02CFB0  mov.b     #0x01, r1l
0x02CFB2  bt        0x02cfbc
0x02CFB4  inc.w     #1, r0
0x02CFB6  cmp.w     #0x0014, r0
0x02CFBA  blt       0x02cfa6
0x02CFBC  mov.b     r1l, r0l
0x02CFBE  rts       
0x02CFE0  sub.b     r1l, r1l
0x02CFE2  sub.w     r0, r0
0x02CFE4  bt        0x02cff6
0x02CFE6  btst      #4, @0xffff55
0x02CFEE  bne       0x02cff4
0x02CFF0  mov.b     #0x01, r1l
0x02CFF2  bt        0x02cffc
0x02CFF4  inc.w     #1, r0
0x02CFF6  cmp.w     #0x0014, r0
0x02CFFA  blt       0x02cfe6
0x02CFFC  mov.b     r1l, r0l
0x02CFFE  rts       
