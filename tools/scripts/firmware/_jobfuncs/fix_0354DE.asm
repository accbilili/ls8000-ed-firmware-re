0x035006  sub.l     er0, er0
0x035008  mov.b     @(0x3f,sp), r0l
0x03500C  mov.b     @(0x400dab,er0), r0l
0x035014  mov.b     r0l, @er5
0x035016  jsr       0x032d2c
0x03501A  sub.l     er0, er0
0x03501C  mov.b     @er5, r0l
0x03501E  mov.b     @(0x41ff6e,er0), r0h
0x035026  mov.b     @er5, r0l
0x035028  jsr       0x02daa2
0x03502C  sub.l     er0, er0
0x03502E  mov.b     @er5, r0l
0x035030  shll.l    er0
0x035032  mov.w     @(0x400da2,er0), r1
0x03503A  beq       0x03508a
0x03503C  mov.b     @er5, r1l
0x03503E  extu.w    r1
0x035040  mov.w     #0x0006, e1
0x035044  mulxu.w   e1, er1
0x035046  add.l     #0x0041ff3e, er1
0x03504C  mov.b     @er5, r0l
0x03504E  jsr       0x03a2d8
0x035052  mov.b     #0x04, r0l
0x035054  jsr       0x0330fa
0x035058  mov.l     @(0x1a,sp), er0
0x03505E  mov.l     @er0, er1
0x035062  mov.l     er1, @(0x56,sp)
0x035068  mov.b     @er5, r0l
0x03506A  extu.w    r0
0x03506C  mov.w     #0x0006, e0
0x035070  mulxu.w   e0, er0
0x035072  sub.w     r1, r1
0x035074  mov.w     r1, @(0x41ff58,er0)
0x03507C  mov.b     #0x22, r0l
0x03507E  mov.b     r0l, @(0x61,sp)
0x035082  sub.b     r0l, r0l
0x035084  mov.b     r0l, @(0x3e,sp)
0x035088  bt        0x0350ec
0x03508A  mov.l     @(0x1e,sp), er0
0x035090  sub.l     er1, er1
0x035092  mov.b     @er0, r1l
0x035094  shll.l    #2, er1
0x035096  shll.l    #2, er1
0x035098  sub.l     er6, er6
0x03509A  mov.b     @er5, r6l
0x03509C  sub.l     er0, er0
0x03509E  mov.b     @(0x41ff6e,er6), r0l
0x0350A6  shll.l    #2, er0
0x0350A8  shll.l    er0
0x0350AA  add.l     #0x0003f74a, er1
0x0350B0  add.l     er1, er0
0x0350B2  mov.l     er6, er1
0x0350B4  shll.l    er1
0x0350B6  add.l     er1, er0
0x0350B8  mov.w     @er0, r0
0x0350BA  extu.l    er0
0x0350BC  mov.w     @0x400d6a, r1
0x0350C2  extu.l    er1
0x0350C4  mov.w     #0x0003, r2
0x0350C8  divxu.w   r2, er1
0x0350CA  extu.l    er1
0x0350CC  jsr       0x018e1e
0x0350D0  mov.l     #0x00000064, er1
0x0350D6  jsr       0x01872e
0x0350DA  mov.l     er0, @(0x56,sp)
0x0350E0  sub.b     r0l, r0l
0x0350E2  mov.b     r0l, @(0x61,sp)
0x0350E6  mov.b     #0x01, r0l
0x0350E8  mov.b     r0l, @(0x3e,sp)
0x0350EC  sub.b     r0l, r0l
0x0350EE  mov.b     r0l, @(0x45,sp)
0x0350F2  mov.l     @(0x2a,sp), er0
0x0350F8  mov.w     #0x01fe, r1
0x0350FC  mov.w     r1, @er0
0x0350FE  mov.l     @(0x26,sp), er0
0x035104  mov.w     r1, @er0
0x035106  mov.w     r1, @(0x14,sp)
0x03510A  mov.l     @(0x32,sp), er0
0x035110  sub.w     r1, r1
0x035112  mov.w     r1, @er0
0x035114  mov.l     @(0x2e,sp), er0
0x03511A  mov.w     r1, @er0
0x03511C  mov.w     r1, @(0xe,sp)
0x035120  mov.l     @(0x22,sp), er0
0x035126  mov.w     #0x00ff, r1
0x03512A  mov.w     r1, @er0
0x03512C  mov.l     @(0x36,sp), er0
0x035132  mov.w     r1, @er0
0x035134  mov.w     r1, @er3
0x035136  sub.b     r0l, r0l
0x035138  jmp       0x0352e0
0x03513C  mov.w     #0x0080, r2
0x035140  sub.l     er6, er6
0x035142  mov.b     @(0x4d,sp), r6l
0x035146  mov.l     er6, @(0x40,sp)
0x03514C  shll.l    er6
0x03514E  mov.l     er3, er4
0x035150  add.l     er6, er4
0x035152  mov.l     @(0x40,sp), er0
0x035158  shll.l    #2, er0
0x03515A  add.l     #0x0041ff7c, er0
0x035160  mov.l     er0, @(0x52,sp)
0x035166  mov.b     @(0x4d,sp), r0l
0x03516A  extu.w    r0
0x03516C  mov.w     #0x0001, r1
0x035170  dec.b     #1, r0l
0x035172  bmi       0x035178
0x035174  shll.w    r1
0x035176  bt        0x035170
0x035178  mov.w     r1, e2
0x03517A  mov.w     @er4, e0
0x03517C  sub.b     r0h, r0h
0x03517E  mov.b     @er5, r0l
0x035180  jsr       0x03a284
0x035184  mov.w     @er4, e0
0x035186  mov.b     #0x01, r0h
0x035188  mov.b     @er5, r0l
0x03518A  jsr       0x03a284
0x03518E  mov.w     @er4, e0
0x035190  mov.b     #0x02, r0h
0x035192  mov.b     @er5, r0l
0x035194  jsr       0x03a284
0x035198  jsr       0x0330aa
0x03519C  btst      #7, @0x400400
0x0351A4  bne       0x035578
0x0351A8  mov.l     @(0x52,sp), er0
0x0351AE  mov.l     @er0, er0
0x0351B2  mov.l     @(0x56,sp), er1
0x0351B8  cmp.l     er1, er0
0x0351BA  bcc       0x0351f6
0x0351BC  mov.l     #0x0000000e, er0
0x0351C2  add.l     sp, er0
0x0351C4  add.l     er6, er0
0x0351C6  mov.l     er3, er1
0x0351C8  add.l     er6, er1
0x0351CA  mov.l     er1, @(0x40,sp)
0x0351D0  mov.w     @er1, r1
0x0351D2  mov.w     r1, @er0
0x0351D4  mov.l     @(0x40,sp), er0
0x0351DA  mov.w     @er0, r0
0x0351DC  mov.w     r2, r1
0x0351DE  add.w     r1, r0
0x0351E0  cmp.w     #0x01fe, r0
0x0351E4  bhi       0x0351ee
0x0351E6  mov.w     @er4, r0
0x0351E8  mov.w     r2, r1
0x0351EA  add.w     r1, r0
0x0351EC  bt        0x0351f2
0x0351EE  mov.w     #0x01fe, r0
0x0351F2  mov.w     r0, @er4
0x0351F4  bt        0x03523e
0x0351F6  mov.l     @(0x52,sp), er0
0x0351FC  mov.l     @er0, er0
0x035200  mov.l     @(0x56,sp), er1
0x035206  cmp.l     er1, er0
0x035208  bls       0x0352b6
0x03520C  mov.l     #0x00000014, er0
0x035212  add.l     sp, er0
0x035214  add.l     er6, er0
0x035216  mov.l     er3, er1
0x035218  add.l     er6, er1
0x03521A  mov.l     er1, @(0x40,sp)
0x035220  mov.w     @er1, r1
0x035222  mov.w     r1, @er0
0x035224  mov.l     @(0x40,sp), er0
0x03522A  mov.w     @er0, r0
0x03522C  mov.w     r2, r1
0x03522E  cmp.w     r1, r0
0x035230  bcs       0x03523a
0x035232  mov.w     @er4, r0
0x035234  mov.w     r2, r1
0x035236  sub.w     r1, r0
0x035238  bt        0x03523c
0x03523A  sub.w     r0, r0
0x03523C  mov.w     r0, @er4
0x03523E  mov.l     #0x00000014, er0
0x035244  add.l     sp, er0
0x035246  add.l     er6, er0
0x035248  mov.l     #0x0000000e, er1
0x03524E  add.l     sp, er1
0x035250  add.l     er6, er1
0x035252  mov.w     @er0, r0
0x035254  mov.w     @er1, r1
0x035256  cmp.w     r1, r0
0x035258  bcs       0x03528e
0x03525A  mov.l     #0x00000014, er0
0x035260  add.l     sp, er0
0x035262  add.l     er6, er0
0x035264  mov.l     #0x0000000e, er1
0x03526A  add.l     sp, er1
0x03526C  add.l     er6, er1
0x03526E  mov.w     @er0, r0
0x035270  mov.w     @er1, r1
0x035272  sub.w     r1, r0
0x035274  cmp.w     #0x0001, r0
0x035278  bhi       0x0352cc
0x03527A  mov.l     er3, er0
0x03527C  add.l     er6, er0
0x03527E  mov.l     #0x00000014, er1
0x035284  add.l     sp, er1
0x035286  add.l     er6, er1
0x035288  mov.w     @er1, r1
0x03528A  mov.w     r1, @er0
0x03528C  bt        0x0352b6
0x03528E  mov.l     er3, er0
0x035290  add.l     er6, er0
0x035292  mov.l     #0x00000014, er4
0x035298  add.l     sp, er4
0x03529A  add.l     er6, er4
0x03529C  mov.w     @er4, r1
0x03529E  mov.w     r1, @er0
0x0352A0  mov.l     #0x0000000e, er0
0x0352A6  add.l     sp, er0
0x0352A8  add.l     er6, er0
0x0352AA  mov.w     @er0, r0
0x0352AC  mov.w     @er4, r4
0x0352AE  sub.w     r4, r0
0x0352B0  cmp.w     #0x0002, r0
0x0352B4  bhi       0x0352c4
0x0352B6  mov.w     e2, r0
0x0352B8  mov.b     @(0x61,sp), r1l
0x0352BC  or.b      r0l, r1l
0x0352BE  mov.b     r1l, @(0x61,sp)
0x0352C2  bt        0x0352da
0x0352C4  sub.b     r0l, r0l
0x0352C6  mov.b     r0l, @(0x45,sp)
0x0352CA  bt        0x0352da
0x0352CC  mov.w     r2, r0
0x0352CE  beq       0x0352da
0x0352D0  mov.w     r2, r0
0x0352D2  shlr.w    r0
0x0352D4  mov.w     r0, r2
0x0352D6  jmp       0x03517a
0x0352DA  mov.b     @(0x4d,sp), r0l
0x0352DE  inc.b     #1, r0l
0x0352E0  mov.b     r0l, @(0x4d,sp)
0x0352E4  cmp.b     #0x03, r0l
0x0352E6  bcs       0x03513c
0x0352EA  mov.b     @(0x61,sp), r0l
0x0352EE  and.b     #0x07, r0l
0x0352F0  cmp.b     #0x07, r0l
0x0352F2  bne       0x0352fa
0x0352F4  mov.b     #0x01, r0l
0x0352F6  mov.b     r0l, @(0x45,sp)
0x0352FA  mov.b     @(0x45,sp), r0l
0x0352FE  bne       0x03531e
0x035300  mov.b     @er5, r0l
0x035302  extu.w    r0
0x035304  inc.w     #1, r0
0x035306  or.w      #0x0810, r0
0x03530A  mov.w     r0, @0x400402
0x035310  mov.l     #0x004206ed, er0
0x035316  mov.b     @er0, r1l
0x035318  and.b     #0x0b, r1l
0x03531A  jmp       0x03555a
0x03531E  sub.b     r6h, r6h
0x035320  sub.b     r6l, r6l
0x035322  jmp       0x035530
0x035326  sub.w     e6, e6
0x035328  mov.b     r6l, r4l
0x03532A  extu.w    r4
0x03532C  extu.l    er4
0x03532E  mov.l     er4, @(0x40,sp)
0x035334  shll.l    er4
0x035336  mov.l     er4, er2
0x035338  add.l     er3, er4
0x03533A  mov.l     @(0x40,sp), er0
0x035340  shll.l    #2, er0
0x035342  add.l     #0x0041ff88, er0
0x035348  mov.l     er0, @(0x40,sp)
0x03534E  mov.b     r6l, r0l
0x035350  extu.w    r0
0x035352  mov.w     #0x0010, r1
0x035356  dec.b     #1, r0l
0x035358  bmi       0x03535e
0x03535A  shll.w    r1
0x03535C  bt        0x035356
0x03535E  mov.w     r1, @(0x46,sp)
0x035362  jmp       0x0354de
0x035366  btst      #7, @0x400400
0x03536E  bne       0x035578
0x035372  mov.b     r6l, r0l
0x035374  extu.w    r0
0x035376  extu.l    er0
0x035378  mov.l     er0, @(0x48,sp)
0x03537E  shll.l    er0
0x035380  add.l     er3, er0
0x035382  mov.l     er0, @(0x4e,sp)
0x035388  mov.w     @er0, e0
0x03538A  sub.b     r0h, r0h
0x03538C  mov.b     @er5, r0l
0x03538E  jsr       0x03a284
0x035392  mov.l     @(0x4e,sp), er0
0x035398  mov.w     @er0, e0
0x03539A  mov.b     #0x01, r0h
0x03539C  mov.b     @er5, r0l
0x03539E  jsr       0x03a284
0x0353A2  mov.l     @(0x4e,sp), er0
0x0353A8  mov.w     @er0, e0
0x0353AA  mov.b     #0x02, r0h
0x0353AC  mov.b     @er5, r0l
0x0353AE  jsr       0x03a284
0x0353B2  mov.b     #0x02, r0l
0x0353B4  jsr       0x0330fa
0x0353B8  mov.l     @(0x48,sp), er0
0x0353BE  shll.l    #2, er0
0x0353C0  mov.l     @(0x41ff7c,er0), er0
0x0353CA  mov.l     @(0x56,sp), er1
0x0353D0  cmp.l     er1, er0
0x0353D2  bcc       0x0353ee
0x0353D4  mov.w     @er4, r0
0x0353D6  inc.w     #1, r0
0x0353D8  cmp.w     #0x01fe, r0
0x0353DC  bcc       0x0353e4
0x0353DE  mov.w     @er4, r0
0x0353E0  inc.w     #1, r0
0x0353E2  bt        0x0353e8
0x0353E4  mov.w     #0x01fe, r0
0x0353E8  mov.w     r0, @er4
0x0353EA  jmp       0x0354dc
0x0353EE  mov.b     @er5, r0l
0x0353F0  extu.w    r0
0x0353F2  mov.w     #0x0006, e0
0x0353F6  mulxu.w   e0, er0
0x0353F8  mov.l     er2, er1
0x0353FA  add.l     #0x0041ff3e, er0
0x035400  add.l     er1, er0
0x035402  add.l     er3, er1
0x035404  mov.l     er1, er4
0x035406  mov.w     @er1, r1
0x035408  mov.w     r1, @er0
0x03540A  mov.b     @er5, r0l
0x03540C  extu.w    r0
0x03540E  mov.w     #0x0006, e0
0x035412  mulxu.w   e0, er0
0x035414  mov.l     @(0x3a,sp), er1
0x03541A  add.l     er0, er1
0x03541C  mov.l     er2, er0
0x03541E  add.l     er0, er1
0x035420  mov.w     @er4, r4
0x035422  mov.w     r4, @er1
0x035424  mov.b     @(0x3e,sp), r0l
0x035428  bne       0x03547e
0x03542A  mov.l     @(0x40,sp), er0
0x035430  mov.l     @er0, er0
0x035434  shlr.l    er0
0x035436  mov.w     r0, e6
0x035438  bne       0x03543e
0x03543A  mov.w     #0x0001, e6
0x03543E  mov.b     @er5, r0l
0x035440  extu.w    r0
0x035442  mov.w     #0x0006, e0
0x035446  mulxu.w   e0, er0
0x035448  mov.b     r6l, r4l
0x03544A  extu.w    r4
0x03544C  extu.l    er4
0x03544E  mov.l     er4, er1
0x035450  shll.l    er1
0x035452  add.l     #0x0041ff56, er0
0x035458  add.l     er1, er0
0x03545A  mov.l     er4, er1
0x03545C  shll.l    #2, er1
0x03545E  mov.l     @(0x41ff7c,er1), er1
0x035468  mov.l     @(0x56,sp), er2
0x03546E  sub.l     er2, er1
0x035470  mov.w     e6, r2
0x035472  extu.l    er2
0x035474  mov.l     er0, @sp
0x035478  mov.l     er1, er0
0x03547A  mov.l     er2, er1
0x03547C  bt        0x0354c2
0x03547E  mov.b     @er5, r0l
0x035480  extu.w    r0
0x035482  mov.w     #0x0006, e0
0x035486  mulxu.w   e0, er0
0x035488  mov.b     r6l, r1l
0x03548A  extu.w    r1
0x03548C  extu.l    er1
0x03548E  mov.l     er1, @(0x48,sp)
0x035494  shll.l    er1
0x035496  add.l     #0x0041ff56, er0
0x03549C  add.l     er1, er0
0x03549E  mov.l     @(0x48,sp), er4
0x0354A4  shll.l    #2, er4
0x0354A6  mov.l     @(0x41ff7c,er4), er1
0x0354B0  shll.l    er1
0x0354B2  mov.l     er0, @sp
0x0354B6  mov.l     er1, er0
0x0354B8  mov.l     @(0x41ff88,er4), er1
0x0354C2  jsr       0x01872e
0x0354C6  mov.l     @sp, er1
0x0354CA  mov.w     r0, @er1
0x0354CC  mov.w     @(0x46,sp), r0
0x0354D0  mov.b     @(0x61,sp), r1l
0x0354D4  or.b      r0l, r1l
0x0354D6  mov.b     r1l, @(0x61,sp)
0x0354DA  bt        0x0354e6
0x0354DC  inc.w     #1, e6
0x0354DE  cmp.w     #0x0040, e6
0x0354E2  bcs       0x035366
0x0354E6  mov.b     @er5, r0l
0x0354E8  extu.w    r0
0x0354EA  mov.w     #0x0006, e0
0x0354EE  mulxu.w   e0, er0
0x0354F0  mov.b     r6l, r1l
0x0354F2  extu.w    r1
0x0354F4  extu.l    er1
0x0354F6  shll.l    er1
0x0354F8  add.l     #0x0041ff56, er0
0x0354FE  add.l     er1, er0
0x035500  mov.w     @er0, r1
0x035502  beq       0x03552e
0x035504  jsr       0x010b56
0x035508  mov.b     @er5, r0l
0x03550A  extu.w    r0
0x03550C  mov.w     #0x0006, e0
0x035510  mulxu.w   e0, er0
0x035512  mov.b     r6l, r1l
0x035514  extu.w    r1
0x035516  extu.l    er1
0x035518  shll.l    er1
0x03551A  add.l     #0x0041ff56, er0
0x035520  add.l     er1, er0
0x035522  mov.b     r6l, r1l
0x035524  extu.w    r1
0x035526  mov.w     @er0, e0
0x035528  mov.w     r1, r0
0x03552A  jsr       0x03ddb2
0x03552E  inc.b     #1, r6l
0x035530  cmp.b     #0x03, r6l
0x035532  bcs       0x035326
0x035536  mov.b     @(0x61,sp), r0l
0x03553A  and.b     #0x70, r0l
0x03553C  cmp.b     #0x70, r0l
0x03553E  bne       0x035542
0x035540  mov.b     #0x01, r6h
0x035542  mov.b     r6h, r6h
0x035544  bne       0x03555e
0x035546  mov.w     #0x0810, r0
0x03554A  mov.w     r0, @0x400402
0x035550  mov.l     #0x004206ed, er0
0x035556  mov.b     @er0, r1l
0x035558  and.b     #0x0d, r1l
0x03555A  mov.b     r1l, @er0
0x03555C  bt        0x035578
0x03555E  mov.b     @(0x3f,sp), r0l
0x035562  inc.b     #1, r0l
0x035564  mov.b     r0l, @(0x3f,sp)
0x035568  mov.b     @(0x3f,sp), r0l
0x03556C  mov.b     @0x400daa, r1l
0x035572  cmp.b     r1l, r0l
0x035574  bcs       0x035006
0x035578  sub.b     r0l, r0l
0x03557A  mov.b     r0l, @0x2001c1
0x035580  mov.b     #0x80, r0l
0x035582  mov.b     r0l, @0x200001
0x035588  add.l     #0x00000064, sp
0x03558E  ldm.l     @sp+, er4-er6
0x035592  ldm.l     @sp+, er2-er3
0x035596  rts       
