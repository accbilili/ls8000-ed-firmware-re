0x031B2A  stm.l     er2-er3, @-sp
0x031B2E  stm.l     er4-er6, @-sp
0x031B32  sub.l     #0x00000022, sp
0x031B38  mov.l     #0x00420248, er3
0x031B3E  mov.l     #0x00420265, er4
0x031B44  mov.l     #0x00000004, er5
0x031B4A  add.l     sp, er5
0x031B4C  mov.b     #0x01, r0l
0x031B4E  mov.b     r0l, @0x420246
0x031B54  mov.b     @0x4206ec, r0l
0x031B5A  bne       0x031bac
0x031B5C  bt        0x031b74
0x031B5E  sub.b     r0l, r0l
0x031B60  mov.w     r0, @-sp
0x031B62  mov.l     #0x000186a0, er1
0x031B68  sub.w     r0, r0
0x031B6A  jsr       0x02adce
0x031B6E  adds.l    #2, sp
0x031B70  jsr       0x02acba
0x031B74  mov.w     @0x4202a2, r0
0x031B7A  bne       0x031b5e
0x031B7C  mov.b     @0x400d72, r0l
0x031B82  cmp.b     #0x05, r0l
0x031B84  beq       0x031bac
0x031B86  bt        0x031ba0
0x031B88  sub.b     r0l, r0l
0x031B8A  mov.w     r0, @-sp
0x031B8C  mov.l     #0x000186a0, er1
0x031B92  mov.w     #0x00ab, r0
0x031B96  jsr       0x02c9e4
0x031B9A  adds.l    #2, sp
0x031B9C  jsr       0x02c8b4
0x031BA0  mov.w     @0x4202ec, r0
0x031BA6  cmp.w     #0x00ab, r0
0x031BAA  bne       0x031b88
0x031BAC  mov.b     @0x4007c9, r0h
0x031BB2  mov.b     @0x4007ca, r0l
0x031BB8  jsr       0x02ed5a
0x031BBC  bsr       0x033422
0x031BC0  jsr       0x02d0de
0x031BC4  mov.b     #0x01, r0l
0x031BC6  mov.b     r0l, @0x420266
0x031BCC  sub.b     r0l, r0l
0x031BCE  mov.b     r0l, @er4
0x031BD0  mov.w     @0x400d64, r0
0x031BD6  mov.w     r0, @0x400d6c
0x031BDC  mov.w     @0x400d60, r0
0x031BE2  mov.w     r0, @0x400d6a
0x031BE8  mov.l     #0x0041ff3e, er1
0x031BEE  mov.b     @er4, r0l
0x031BF0  jsr       0x02da8e
0x031BF4  sub.l     er6, er6
0x031BF6  mov.b     @er4, r6l
0x031BF8  add.l     #0x0041ff6e, er6
0x031BFE  mov.b     @er6, r0l
0x031C00  mov.b     r0l, @(0x15,sp)
0x031C04  sub.b     r0l, r0l
0x031C06  mov.b     r0l, @er6
0x031C08  sub.l     er0, er0
0x031C0A  mov.b     @er4, r0l
0x031C0C  shll.l    #2, er0
0x031C0E  mov.l     @(0x400f32,er0), er0
0x031C18  mov.l     #0x00000009, er1
0x031C1E  jsr       0x018e1e
0x031C22  mov.l     #0x0000000a, er1
0x031C28  jsr       0x01872e
0x031C2C  mov.l     er0, @(0x1a,sp)
0x031C32  sub.b     r6l, r6l
0x031C34  mov.b     r6l, r1l
0x031C36  extu.w    r1
0x031C38  inc.w     #1, r1
0x031C3A  exts.l    er1
0x031C3C  mov.l     @(0x1a,sp), er0
0x031C42  jsr       0x01872e
0x031C46  mov.l     er0, @er3
0x031C4A  bne       0x031c56
0x031C4C  mov.l     #0x00000001, er0
0x031C52  mov.l     er0, @er3
0x031C56  mov.b     r6l, r0h
0x031C58  mov.b     @er4, r0l
0x031C5A  jsr       0x02daa2
0x031C5E  mov.b     r6l, r0l
0x031C60  extu.w    r0
0x031C62  extu.l    er0
0x031C64  shll.l    #2, er0
0x031C66  add.l     er5, er0
0x031C68  sub.l     er1, er1
0x031C6A  mov.l     er1, @er0
0x031C6E  sub.b     r6h, r6h
0x031C70  mov.b     r6l, r0l
0x031C72  extu.w    r0
0x031C74  extu.l    er0
0x031C76  shll.l    #2, er0
0x031C78  add.l     er5, er0
0x031C7A  mov.l     er0, @(0x1e,sp)
0x031C80  bsr       0x0332be
0x031C84  mov.l     @(0x1e,sp), er0
0x031C8A  mov.w     @0x41ff76, r1
0x031C90  extu.l    er1
0x031C92  mov.l     @er0, er2
0x031C96  add.l     er1, er2
0x031C98  mov.l     er2, @er0
0x031C9C  inc.b     #1, r6h
0x031C9E  cmp.b     #0x10, r6h
0x031CA0  bcs       0x031c80
0x031CA2  mov.b     r6l, r0l
0x031CA4  beq       0x031cb0
0x031CA6  cmp.b     #0x01, r0l
0x031CA8  beq       0x031ccc
0x031CAA  cmp.b     #0x02, r0l
0x031CAC  beq       0x031cf0
0x031CAE  bt        0x031d22
0x031CB0  mov.b     r6l, r0l
0x031CB2  extu.w    r0
0x031CB4  extu.l    er0
0x031CB6  shll.l    #2, er0
0x031CB8  add.l     er5, er0
0x031CBA  mov.l     er0, @(0x1e,sp)
0x031CC0  mov.l     @(0x1e,sp), er1
0x031CC6  mov.l     @er1, er1
0x031CCA  bt        0x031ce8
0x031CCC  mov.b     r6l, r0l
0x031CCE  extu.w    r0
0x031CD0  extu.l    er0
0x031CD2  shll.l    #2, er0
0x031CD4  add.l     er5, er0
0x031CD6  mov.l     er0, @(0x1e,sp)
0x031CDC  mov.l     @(0x1e,sp), er1
0x031CE2  mov.l     @er1, er1
0x031CE6  shll.l    er1
0x031CE8  shlr.l    #2, er1
0x031CEA  mov.l     er1, @er0
0x031CEE  bt        0x031d22
0x031CF0  mov.b     r6l, r0l
0x031CF2  extu.w    r0
0x031CF4  extu.l    er0
0x031CF6  shll.l    #2, er0
0x031CF8  add.l     er5, er0
0x031CFA  mov.l     er0, @(0x1e,sp)
0x031D00  mov.l     @(0x1e,sp), er1
0x031D06  mov.l     @er1, er1
0x031D0A  mov.l     er0, @sp
0x031D0E  mov.l     #0x00000003, er0
0x031D14  jsr       0x018e1e
0x031D18  shlr.l    #2, er0
0x031D1A  mov.l     @sp, er1
0x031D1E  mov.l     er0, @er1
0x031D22  mov.b     r6l, r0l
0x031D24  extu.w    r0
0x031D26  extu.l    er0
0x031D28  shll.l    #2, er0
0x031D2A  add.l     er5, er0
0x031D2C  mov.l     @er0, er1
0x031D30  bne       0x031d46
0x031D32  mov.b     r6l, r0l
0x031D34  extu.w    r0
0x031D36  extu.l    er0
0x031D38  shll.l    #2, er0
0x031D3A  add.l     er5, er0
0x031D3C  mov.l     #0x00000001, er1
0x031D42  mov.l     er1, @er0
0x031D46  mov.b     r6l, r6l
0x031D48  bne       0x031d5a
0x031D4A  mov.l     #0x3f800000, er0
0x031D50  mov.l     er0, @0x400dda
0x031D58  bt        0x031dce
0x031D5A  mov.b     r6l, r2l
0x031D5C  extu.w    r2
0x031D5E  extu.l    er2
0x031D60  shll.l    #2, er2
0x031D62  mov.l     er2, @(0x16,sp)
0x031D68  add.l     #0x00400dda, er2
0x031D6E  mov.l     er2, @(0x1e,sp)
0x031D74  mov.l     @(0x16,sp), er0
0x031D7A  add.l     er5, er0
0x031D7C  mov.l     @er0, er0
0x031D80  jsr       0x018e9e
0x031D84  mov.l     er0, @sp
0x031D88  mov.l     @er5, er0
0x031D8C  jsr       0x018e9e
0x031D90  mov.l     er0, er1
0x031D92  mov.l     @sp, er0
0x031D96  jsr       0x0185ee
0x031D9A  mov.l     #0x461c4000, er1
0x031DA0  jsr       0x018cac
0x031DA4  mov.l     er0, @er2
0x031DA8  mov.l     @(0x1e,sp), er0
0x031DAE  mov.l     @er0, er0
0x031DB2  jsr       0x018860
0x031DB6  jsr       0x018e9e
0x031DBA  mov.l     #0x461c4000, er1
0x031DC0  jsr       0x0185ee
0x031DC4  mov.l     @(0x1e,sp), er1
0x031DCA  mov.l     er0, @er1
0x031DCE  inc.b     #1, r6l
0x031DD0  cmp.b     #0x02, r6l
0x031DD2  bcs       0x031c34
0x031DD6  sub.l     er0, er0
0x031DD8  mov.b     @er4, r0l
0x031DDA  mov.b     @(0x15,sp), r1l
0x031DDE  mov.b     r1l, @(0x41ff6e,er0)
0x031DE6  jsr       0x02d694
0x031DEA  sub.b     r0l, r0l
0x031DEC  mov.b     r0l, @0x420246
0x031DF2  add.l     #0x00000022, sp
0x031DF8  ldm.l     @sp+, er4-er6
0x031DFC  ldm.l     @sp+, er2-er3
0x031E00  rts       
