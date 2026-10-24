0x015FFC  stm.l     er4-er6, @-sp
0x016000  mov.l     #0x004003f6, er5
0x016006  mov.l     er0, er4
0x016008  mov.l     @er5, er6
0x01600C  bt        0x016012
0x01600E  jsr       0x010b56
0x016012  mov.l     @er5, er0
0x016016  sub.l     er6, er0
0x016018  cmp.l     er4, er0
0x01601A  bcs       0x01600e
0x01601C  ldm.l     @sp+, er4-er6
0x016020  rts       
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
0x02B276  mov.l     er6, @-sp
0x02B27A  mov.b     r0l, r6l
0x02B27C  mov.w     r1, e6
0x02B27E  mov.b     #0x01, r0l
0x02B280  mov.b     r0l, @0x4202e6
0x02B286  mov.w     e6, @0x4202de
0x02B28C  mov.b     @(0x9,sp), r0l
0x02B290  mov.b     r0l, @0x440e42
0x02B296  mov.w     e0, @0x4202e2
0x02B29C  mov.b     r0h, @0x4202e8
0x02B2A2  mov.w     e1, @0x4202e4
0x02B2A8  mov.b     r6l, @0x4202e7
0x02B2AE  mov.b     r6l, r0l
0x02B2B0  bsr       0x02b442
0x02B2B4  bsr       0x02b2d4
0x02B2B6  mov.b     #0x03, r0l
0x02B2B8  mov.b     r0l, @0x4202e6
0x02B2BE  sub.w     r0, r0
0x02B2C0  mov.w     r0, @0xffffe6
0x02B2C6  bset      #1, @0xffffc0
0x02B2CE  mov.l     @sp+, er6
0x02B2D2  rts       
0x02B2D4  mov.l     #0x00ffff48, er0
0x02B2DA  mov.w     @er0, r1
0x02B2DC  or.w      #0xf000, r1
0x02B2E0  mov.w     r1, @er0
0x02B2E2  mov.b     @0x440e50, r0l
0x02B2E8  bsr       0x02bd66
0x02B2EC  bclr      #1, @0xffffc0
0x02B2F4  mov.b     #0x42, r0l
0x02B2F6  mov.b     r0l, @0xffffe0
0x02B2FC  mov.b     @0xffffe5, r0l
0x02B302  mov.b     r0l, @0x40041b
0x02B308  bclr      #0, @0xffffe5
0x02B310  mov.b     @0x4202e9, r0l
0x02B316  cmp.b     #0x01, r0l
0x02B318  bne       0x02b320
0x02B31A  mov.w     #0x0001, r0
0x02B31E  bt        0x02b346
0x02B320  mov.w     @0x4202de, r1
0x02B326  extu.l    er1
0x02B328  mov.l     #0x3b9aca00, er0
0x02B32E  jsr       0x018708
0x02B332  mov.l     #0x00000280, er1
0x02B338  jsr       0x018708
0x02B33C  mov.l     #0x00000064, er1
0x02B342  jsr       0x018708
0x02B346  mov.w     r0, @0xffffe8
0x02B34C  mov.w     @0x440e58, r0
0x02B352  mov.w     r0, @0xffffea
0x02B358  mov.l     #0x00ffffe4, er0
0x02B35E  mov.b     @er0, r1l
0x02B360  and.b     #0x4c, r1l
0x02B362  mov.b     r1l, @er0
0x02B364  bset      #0, @0xffffe4
0x02B36C  sub.w     r0, r0
0x02B36E  mov.w     r0, @0x440e5e
0x02B374  mov.b     @0xffff46, r0l
0x02B37A  and.b     #0x3f, r0l
0x02B37C  or.b      #0x40, r0l
0x02B37E  mov.b     r0l, @0xffff46
0x02B384  mov.l     #0x00ffff47, er1
0x02B38A  mov.b     @0x4202e9, r0l
0x02B390  cmp.b     #0x01, r0l
0x02B392  bne       0x02b39c
0x02B394  mov.b     @er1, r0l
0x02B396  and.b     #0x77, r0l
0x02B398  or.b      #0x80, r0l
0x02B39A  bt        0x02b3a2
0x02B39C  mov.b     @er1, r0l
0x02B39E  and.b     #0x77, r0l
0x02B3A0  or.b      #0x88, r0l
0x02B3A2  mov.b     r0l, @er1
0x02B3A4  mov.l     @0x440e52, er0
0x02B3AC  mov.b     @(0x1,er0), r0l
0x02B3B0  mov.b     r0l, @0xffff4c
0x02B3B6  mov.b     @0xffff07, r0l
0x02B3BC  mov.b     r0l, @0x40041b
0x02B3C2  mov.w     @0xffff06, r0
0x02B3C8  and.w     #0xaccc, r0
0x02B3CC  or.w      #0x0332, r0
0x02B3D0  mov.w     r0, @0xffff06
0x02B3D6  mov.b     #0x29, r0l
0x02B3D8  mov.b     r0l, @0xffff02
0x02B3DE  mov.b     @0x440e42, r0l
0x02B3E4  mov.b     r0l, @0xfffee7
0x02B3EA  mov.b     r0l, @0xfffee6
0x02B3F0  mov.l     #0x00440e43, er0
0x02B3F6  mov.l     er0, @0xfffee0
0x02B3FE  mov.w     #0xff4c, r0
0x02B402  mov.w     r0, @0xfffee4
0x02B408  mov.b     #0xa9, r0l
0x02B40A  mov.b     r0l, @0xffff03
0x02B410  mov.l     #0x00440e58, er0
0x02B416  mov.l     er0, @0xfffee8
0x02B41E  mov.w     #0xffea, r0
0x02B422  mov.w     r0, @0xfffeec
0x02B428  mov.b     @0x440e42, r0l
0x02B42E  extu.w    r0
0x02B430  shlr.w    #2, r0
0x02B432  mov.w     r0, @0xfffeee
0x02B438  mov.b     #0x02, r0l
0x02B43A  mov.b     r0l, @0x4003ff
0x02B440  rts       
0x02B442  mov.w     r6, @-sp
0x02B444  mov.b     r0l, r6l
0x02B446  bsr       0x02b450
0x02B448  bsr       0x02b618
0x02B44C  mov.w     @sp+, r6
0x02B44E  rts       
0x02B450  stm.l     er2-er3, @-sp
0x02B454  stm.l     er4-er6, @-sp
0x02B458  sub.l     #0x00000012, sp
0x02B45E  mov.l     #0x00440e43, er3
0x02B464  mov.l     #0x00000002, er4
0x02B46A  mov.b     r0l, r2l
0x02B46C  mov.l     #0x0003f0f8, er5
0x02B472  mov.l     er5, er6
0x02B474  sub.w     r1, r1
0x02B476  mov.w     r1, @(0x8,sp)
0x02B47A  bt        0x02b494
0x02B47C  mov.b     @er6, r0l
0x02B47E  mov.b     @0x440e50, r1l
0x02B484  cmp.b     r1l, r0l
0x02B486  beq       0x02b49e
0x02B488  inc.l     #1, er6
0x02B48A  mov.w     @(0x8,sp), r0
0x02B48E  inc.w     #1, r0
0x02B490  mov.w     r0, @(0x8,sp)
0x02B494  mov.w     @(0x8,sp), r0
0x02B498  cmp.w     #0x0007, r0
0x02B49C  ble       0x02b47c
0x02B49E  mov.b     @0x4202e9, r0l
0x02B4A4  cmp.b     #0x01, r0l
0x02B4A6  bne       0x02b550
0x02B4AA  mov.b     r2l, r0l
0x02B4AC  bne       0x02b4ce
0x02B4AE  mov.l     er6, er0
0x02B4B0  add.l     er4, er0
0x02B4B2  mov.l     er5, er1
0x02B4B4  add.l     #0x00000007, er1
0x02B4BA  cmp.l     er1, er0
0x02B4BC  bls       0x02b4ca
0x02B4BE  mov.l     er6, er0
0x02B4C0  add.l     er4, er0
0x02B4C2  subs.l    #4, er0
0x02B4C4  subs.l    #4, er0
0x02B4C6  mov.l     er0, er6
0x02B4C8  bt        0x02b4e4
0x02B4CA  add.l     er4, er6
0x02B4CC  bt        0x02b4e4
0x02B4CE  mov.l     er6, er0
0x02B4D0  sub.l     er4, er0
0x02B4D2  cmp.l     er5, er0
0x02B4D4  bcc       0x02b4e2
0x02B4D6  mov.l     er6, er0
0x02B4D8  sub.l     er4, er0
0x02B4DA  adds.l    #4, er0
0x02B4DC  adds.l    #4, er0
0x02B4DE  mov.l     er0, er6
0x02B4E0  bt        0x02b4e4
0x02B4E2  sub.l     er4, er6
0x02B4E4  mov.l     er3, @sp
0x02B4E8  mov.b     r2l, r0l
0x02B4EA  bne       0x02b4f2
0x02B4EC  mov.w     #0x0001, r0
0x02B4F0  bt        0x02b4f6
0x02B4F2  mov.w     #0xffff, r0
0x02B4F6  mov.w     r0, @(0x8,sp)
0x02B4FA  sub.w     r0, r0
0x02B4FC  mov.w     r0, e2
0x02B4FE  mov.l     er5, er0
0x02B500  add.l     #0x00000007, er0
0x02B506  mov.l     er0, @(0x4,sp)
0x02B50C  mov.l     @sp, er0
0x02B510  inc.l     #1, er0
0x02B512  mov.l     er0, @sp
0x02B516  dec.l     #1, er0
0x02B518  mov.b     @er6, r1l
0x02B51A  mov.b     r1l, @er0
0x02B51C  mov.w     @(0x8,sp), r0
0x02B520  exts.l    er0
0x02B522  add.l     er0, er6
0x02B524  mov.l     @(0x4,sp), er0
0x02B52A  cmp.l     er0, er6
0x02B52C  bls       0x02b530
0x02B52E  mov.l     er5, er6
0x02B530  cmp.l     er5, er6
0x02B532  bcc       0x02b53a
0x02B534  mov.l     @(0x4,sp), er6
0x02B53A  mov.w     e2, r0
0x02B53C  inc.w     #1, r0
0x02B53E  mov.w     r0, e2
0x02B540  cmp.w     #0x0007, r0
0x02B544  ble       0x02b50c
0x02B546  mov.l     er3, er0
0x02B548  adds.l    #4, er0
0x02B54A  inc.l     #2, er0
0x02B54C  jmp       0x02b600
0x02B550  mov.b     r2l, r0l
0x02B552  bne       0x02b574
0x02B554  mov.l     er6, er0
0x02B556  adds.l    #4, er0
0x02B558  mov.l     er5, er1
0x02B55A  add.l     #0x00000007, er1
0x02B560  cmp.l     er1, er0
0x02B562  bls       0x02b570
0x02B564  mov.l     er6, er0
0x02B566  adds.l    #4, er0
0x02B568  subs.l    #4, er0
0x02B56A  subs.l    #4, er0
0x02B56C  mov.l     er0, er6
0x02B56E  bt        0x02b58a
0x02B570  adds.l    #4, er6
0x02B572  bt        0x02b58a
0x02B574  mov.l     er6, er0
0x02B576  subs.l    #4, er0
0x02B578  cmp.l     er5, er0
0x02B57A  bcc       0x02b588
0x02B57C  mov.l     er6, er0
0x02B57E  subs.l    #4, er0
0x02B580  adds.l    #4, er0
0x02B582  adds.l    #4, er0
0x02B584  mov.l     er0, er6
0x02B586  bt        0x02b58a
0x02B588  subs.l    #4, er6
0x02B58A  mov.l     er3, @(0x4,sp)
0x02B590  mov.b     r2l, r0l
0x02B592  bne       0x02b59a
0x02B594  mov.w     #0x0002, r0
0x02B598  bt        0x02b59e
0x02B59A  mov.w     #0xfffe, r0
0x02B59E  mov.w     r0, @(0x8,sp)
0x02B5A2  sub.w     r0, r0
0x02B5A4  mov.w     r0, e2
0x02B5A6  mov.l     er5, er0
0x02B5A8  add.l     #0x00000007, er0
0x02B5AE  mov.l     er0, @(0xa,sp)
0x02B5B4  mov.l     er5, er1
0x02B5B6  inc.l     #1, er1
0x02B5B8  mov.l     er1, @sp
0x02B5BC  mov.l     @(0x4,sp), er0
0x02B5C2  inc.l     #1, er0
0x02B5C4  mov.l     er0, @(0x4,sp)
0x02B5CA  dec.l     #1, er0
0x02B5CC  mov.b     @er6, r1l
0x02B5CE  mov.b     r1l, @er0
0x02B5D0  mov.w     @(0x8,sp), r0
0x02B5D4  exts.l    er0
0x02B5D6  add.l     er0, er6
0x02B5D8  mov.l     @(0xa,sp), er0
0x02B5DE  cmp.l     er0, er6
0x02B5E0  bls       0x02b5e6
0x02B5E2  mov.l     @sp, er6
0x02B5E6  cmp.l     er5, er6
0x02B5E8  bcc       0x02b5f0
0x02B5EA  mov.l     @(0xa,sp), er6
0x02B5F0  mov.w     e2, r0
0x02B5F2  inc.w     #1, r0
0x02B5F4  mov.w     r0, e2
0x02B5F6  cmp.w     #0x0003, r0
0x02B5FA  ble       0x02b5bc
0x02B5FC  mov.l     er3, er0
0x02B5FE  add.l     er4, er0
0x02B600  mov.l     er0, @0x440e52
0x02B608  add.l     #0x00000012, sp
0x02B60E  ldm.l     @sp+, er4-er6
0x02B612  ldm.l     @sp+, er2-er3
0x02B616  rts       
0x02B618  mov.w     @0x4202de, r1
0x02B61E  extu.l    er1
0x02B620  mov.l     #0x3b9aca00, er0
0x02B626  jsr       0x018708
0x02B62A  mov.l     #0x00000280, er1
0x02B630  jsr       0x018708
0x02B634  mov.w     r0, @0x440e58
0x02B63A  mov.w     @0x4202de, r1
0x02B640  extu.l    er1
0x02B642  mov.l     #0x3b9aca00, er0
0x02B648  jsr       0x018708
0x02B64C  mov.l     #0x00000280, er1
0x02B652  jsr       0x018708
0x02B656  mov.w     r0, @0x440e5a
0x02B65C  rts       
0x02B7F6  sub.b     r0l, r0l
0x02B7F8  mov.b     r0l, @0x4202e8
0x02B7FE  bsr       0x02bd66
0x02B802  mov.l     #0x00ffff60, er0
0x02B808  mov.b     @er0, r1l
0x02B80A  and.b     #0x0f, r1l
0x02B80C  mov.b     r1l, @er0
0x02B80E  sub.b     r0l, r0l
0x02B810  mov.b     r0l, @0x4202e6
0x02B816  rts       
0x02B858  mov.w     r6, @-sp
0x02B85A  mov.b     @0x4202e8, r0l
0x02B860  bne       0x02b866
0x02B862  sub.b     r6l, r6l
0x02B864  bt        0x02b86e
0x02B866  mov.b     #0x07, r6l
0x02B868  bt        0x02b86e
0x02B86A  jsr       0x010b56
0x02B86E  mov.b     @0x4202e6, r0l
0x02B874  cmp.b     r6l, r0l
0x02B876  bne       0x02b86a
0x02B878  mov.w     @sp+, r6
0x02B87A  rts       
0x02BAA6  mov.l     er3, @-sp
0x02BAAA  stm.l     er4-er6, @-sp
0x02BAAE  mov.b     #0x04, r6h
0x02BAB0  mov.w     #0x0190, e6
0x02BAB4  mov.l     #0x00440e61, er3
0x02BABA  mov.l     #0x004202e6, er4
0x02BAC0  mov.l     #0x00440e60, er5
0x02BAC6  mov.b     #0x01, r6l
0x02BAC8  sub.b     r0l, r0l
0x02BACA  mov.b     r0l, @0x4202e9
0x02BAD0  mov.b     #0x01, r0l
0x02BAD2  mov.b     r0l, @er5
0x02BAD4  jsr       0x02cf80
0x02BAD8  cmp.b     #0x01, r0l
0x02BADA  bne       0x02bb40
0x02BADC  mov.b     @er4, r0l
0x02BADE  beq       0x02bae6
0x02BAE0  mov.b     @er4, r0l
0x02BAE2  cmp.b     #0x07, r0l
0x02BAE4  bne       0x02bb36
0x02BAE6  mov.b     r6h, r0l
0x02BAE8  mov.w     r0, @-sp
0x02BAEA  mov.b     r6l, r0h
0x02BAEC  mov.w     #0x0003, e1
0x02BAF0  mov.w     e6, r1
0x02BAF2  mov.w     #0x041a, e0
0x02BAF6  sub.b     r0l, r0l
0x02BAF8  bsr       0x02b276
0x02BAFC  adds.l    #2, sp
0x02BAFE  bsr       0x02b858
0x02BB02  mov.b     @er3, r0l
0x02BB04  cmp.b     r6l, r0l
0x02BB06  beq       0x02bb0e
0x02BB08  mov.w     #0x0121, r0
0x02BB0C  bt        0x02bb78
0x02BB0E  sub.b     r0l, r0l
0x02BB10  mov.b     r0l, @er5
0x02BB12  mov.b     r6h, r0l
0x02BB14  mov.w     r0, @-sp
0x02BB16  mov.b     r6l, r0h
0x02BB18  mov.w     #0x000a, e1
0x02BB1C  mov.w     e6, r1
0x02BB1E  mov.w     #0x0032, e0
0x02BB22  sub.b     r0l, r0l
0x02BB24  bsr       0x02b276
0x02BB28  adds.l    #2, sp
0x02BB2A  bsr       0x02b858
0x02BB2E  bsr       0x02b7f6
0x02BB32  jsr       0x010b56
0x02BB36  mov.l     #0x0000000a, er0
0x02BB3C  jsr       0x015ffc
0x02BB40  mov.b     #0x01, r0l
0x02BB42  mov.b     r0l, @er5
0x02BB44  sub.b     r0l, r0l
0x02BB46  mov.b     r0l, @er3
0x02BB48  mov.b     @er4, r0l
0x02BB4A  beq       0x02bb52
0x02BB4C  mov.b     @er4, r0l
0x02BB4E  cmp.b     #0x07, r0l
0x02BB50  bne       0x02bb94
0x02BB52  mov.b     r6h, r0l
0x02BB54  mov.w     r0, @-sp
0x02BB56  mov.b     r6l, r0h
0x02BB58  mov.w     #0x0003, e1
0x02BB5C  mov.w     e6, r1
0x02BB5E  mov.w     #0x00c8, e0
0x02BB62  mov.b     r6l, r0l
0x02BB64  bsr       0x02b276
0x02BB68  adds.l    #2, sp
0x02BB6A  bsr       0x02b858
0x02BB6E  mov.b     @er3, r0l
0x02BB70  cmp.b     r6l, r0l
0x02BB72  beq       0x02bb8c
0x02BB74  mov.w     #0x0120, r0
0x02BB78  mov.w     r0, @0x400402
0x02BB7E  sub.w     r0, r0
0x02BB80  mov.w     r0, @0x4202e0
0x02BB86  bsr       0x02b7f6
0x02BB8A  bt        0x02bba4
0x02BB8C  sub.b     r0l, r0l
0x02BB8E  mov.b     r0l, @er5
0x02BB90  jsr       0x010b56
0x02BB94  sub.b     r0l, r0l
0x02BB96  mov.b     r0l, @er3
0x02BB98  bsr       0x02b7f6
0x02BB9C  sub.w     r0, r0
0x02BB9E  mov.w     r0, @0x4202e0
0x02BBA4  ldm.l     @sp+, er4-er6
0x02BBA8  mov.l     @sp+, er3
0x02BBAC  rts       
0x02BD66  stm.l     er4-er5, @-sp
0x02BD6A  mov.l     #0x00ffffc0, er5
0x02BD70  mov.l     #0x00ffffe5, er4
0x02BD76  mov.b     r0l, r1h
0x02BD78  bclr      #1, @er5
0x02BD7C  sub.w     r0, r0
0x02BD7E  mov.w     r0, @0xffffe6
0x02BD84  mov.b     #0x20, r0l
0x02BD86  mov.b     r0l, @0xffffe0
0x02BD8C  bclr      #0, @er4
0x02BD90  mov.l     #0x00ffffe4, er0
0x02BD96  mov.b     @er0, r1l
0x02BD98  and.b     #0x4c, r1l
0x02BD9A  mov.b     r1l, @er0
0x02BD9C  mov.w     #0x0001, r0
0x02BDA0  mov.w     r0, @0xffffe8
0x02BDA6  mov.b     @0xffff46, r0l
0x02BDAC  and.b     #0x3f, r0l
0x02BDAE  or.b      #0x40, r0l
0x02BDB0  mov.b     r0l, @0xffff46
0x02BDB6  mov.b     @0xffff47, r0l
0x02BDBC  and.b     #0x77, r0l
0x02BDBE  or.b      #0x80, r0l
0x02BDC0  mov.b     r0l, @0xffff47
0x02BDC6  mov.b     r1h, @0xffff4c
0x02BDCC  bset      #1, @er5
0x02BDD0  btst      #0, @er4
0x02BDD4  beq       0x02bdd0
0x02BDD6  bclr      #1, @er5
0x02BDDA  bclr      #0, @er4
0x02BDDE  ldm.l     @sp+, er4-er5
0x02BDE2  rts       
0x02CF80  sub.b     r1l, r1l
0x02CF82  sub.w     r0, r0
0x02CF84  bt        0x02cf96
0x02CF86  btst      #6, @0xffff55
0x02CF8E  bne       0x02cf94
0x02CF90  mov.b     #0x01, r1l
0x02CF92  bt        0x02cf9c
0x02CF94  inc.w     #1, r0
0x02CF96  cmp.w     #0x0014, r0
0x02CF9A  blt       0x02cf86
0x02CF9C  mov.b     r1l, r0l
0x02CF9E  rts       
