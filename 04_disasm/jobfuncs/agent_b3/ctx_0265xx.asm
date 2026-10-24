0x026500  mov.l     @sp+, er6   ; 01 00 6d 76
0x026504  rts          ; 54 70
0x026506  mov.l     er6, @-sp   ; 01 00 6d f6
0x02650A  mov.l     er0, er6   ; 0f 86
0x02650C  mov.w     r1, e1   ; 0d 19
0x02650E  mov.w     @er6, r6   ; 69 66
0x026510  mov.l     @(0x8,sp), er0   ; 01 00 6f 70 00 08
0x026516  sub.w     r1, r1   ; 19 11
0x026518  mov.w     r1, @er0   ; 69 81
0x02651A  inc.w     #1, r6   ; 0b 56
0x02651C  cmp.w     e1, r6   ; 1d 96
0x02651E  bhi       0x02652c   ; 42 0c
0x026520  mov.l     @(0x8,sp), er0   ; 01 00 6f 70 00 08
0x026526  mov.w     #0x0002, r1   ; 79 01 00 02
0x02652A  mov.w     r1, @er0   ; 69 81
0x02652C  mov.b     #0x01, r0l   ; f8 01
0x02652E  mov.l     @sp+, er6   ; 01 00 6d 76
0x026532  rts          ; 54 70
0x026534  stm.l     er2-er3, @-sp   ; 01 10 6d f2
0x026538  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x02653C  sub.l     #0x0000004a, sp   ; 7a 37 00 00 00 4a
0x026542  mov.l     #0x00400436, er5   ; 7a 05 00 40 04 36
0x026548  mov.l     #0x0040043c, er6   ; 7a 06 00 40 04 3c
0x02654E  mov.b     @(0x1,er6), r0l   ; 6e 68 00 01
0x026552  and.b     #0x18, r0l   ; e8 18
0x026554  bne       0x02678c   ; 58 60 02 34
0x026558  mov.b     @(0x9,er6), r0l   ; 6e 68 00 09
0x02655C  bne       0x02678c   ; 58 60 02 2c
0x026560  mov.b     @(0x1,er6), r0l   ; 6e 68 00 01
0x026564  and.b     #0x07, r0l   ; e8 07
0x026566  mov.b     r0l, r1l   ; 0c 89
0x026568  cmp.b     #0x05, r0l   ; a8 05
0x02656A  bne       0x0266ae   ; 58 60 01 40
0x02656E  mov.b     @(0x2,er6), r1l   ; 6e 69 00 02
0x026572  cmp.b     #0x02, r1l   ; a9 02
0x026574  bne       0x0265b6   ; 46 40
0x026576  sub.l     er1, er1   ; 1a 91
0x026578  mov.b     @(0x6,er6), r1l   ; 6e 69 00 06
0x02657C  mov.w     r1, e1   ; 0d 19
0x02657E  sub.w     r1, r1   ; 19 11
0x026580  sub.l     er2, er2   ; 1a a2
0x026582  mov.b     @(0x7,er6), r2l   ; 6e 6a 00 07
0x026586  shll.l    #2, er2   ; 10 72
0x026588  shll.l    #2, er2   ; 10 72
0x02658A  shll.l    #2, er2   ; 10 72
0x02658C  shll.l    #2, er2   ; 10 72
0x02658E  add.l     er2, er1   ; 0a a1
0x026590  sub.l     er2, er2   ; 1a a2
0x026592  mov.b     @(0x8,er6), r2l   ; 6e 6a 00 08
0x026596  add.l     er2, er1   ; 0a a1
0x026598  mov.l     er1, er6   ; 0f 96
0x02659A  cmp.l     #0x00020006, er1   ; 7a 21 00 02 00 06
0x0265A0  bls       0x0265ac   ; 43 0a
0x0265A2  mov.w     #0x0050, r2   ; 79 02 00 50
0x0265A6  mov.w     r2, @er5   ; 69 d2
0x0265A8  jmp       0x02679a   ; 5a 02 67 9a
0x0265AC  mov.l     er6, er0   ; 0f e0
0x0265AE  jsr       0x0170a0   ; 5e 01 70 a0
0x0265B2  jmp       0x02679a   ; 5a 02 67 9a
0x0265B6  mov.l     #0x00000001, er4   ; 7a 04 00 00 00 01
0x0265BC  add.l     sp, er4   ; 0a f4
0x0265BE  mov.b     @(0x2,er6), r0l   ; 6e 68 00 02
0x0265C2  cmp.b     #0x03, r0l   ; a8 03
0x0265C4  bne       0x02662a   ; 46 64
0x0265C6  sub.l     er0, er0   ; 1a 80
0x0265C8  mov.b     @(0x6,er6), r0l   ; 6e 68 00 06
0x0265CC  mov.w     r0, e0   ; 0d 08
0x0265CE  sub.w     r0, r0   ; 19 00
0x0265D0  sub.l     er1, er1   ; 1a 91
0x0265D2  mov.b     @(0x7,er6), r1l   ; 6e 69 00 07
0x0265D6  shll.l    #2, er1   ; 10 71
0x0265D8  shll.l    #2, er1   ; 10 71
0x0265DA  shll.l    #2, er1   ; 10 71
0x0265DC  shll.l    #2, er1   ; 10 71
0x0265DE  add.l     er1, er0   ; 0a 90
0x0265E0  sub.l     er1, er1   ; 1a 91
0x0265E2  mov.b     @(0x8,er6), r1l   ; 6e 69 00 08
0x0265E6  add.l     er1, er0   ; 0a 90
0x0265E8  mov.l     er0, er6   ; 0f 86
0x0265EA  cmp.l     #0x00000003, er0   ; 7a 20 00 00 00 03
0x0265F0  bne       0x02665e   ; 46 6c
0x0265F2  mov.w     r6, r1   ; 0d 61
0x0265F4  mov.l     er4, er0   ; 0f c0
0x0265F6  jsr       0x0118d0   ; 5e 01 18 d0
0x0265FA  sub.l     er0, er0   ; 1a 80
0x0265FC  mov.b     @(0x1,er4), r0l   ; 6e 48 00 01
0x026600  shll.l    #2, er0   ; 10 70
0x026602  shll.l    #2, er0   ; 10 70
0x026604  shll.l    #2, er0   ; 10 70
0x026606  shll.l    #2, er0   ; 10 70
0x026608  sub.l     er1, er1   ; 1a 91
0x02660A  mov.b     @er4, r1l   ; 68 49
0x02660C  mov.w     r1, e1   ; 0d 19
0x02660E  sub.w     r1, r1   ; 19 11
0x026610  add.l     er1, er0   ; 0a 90
0x026612  sub.l     er1, er1   ; 1a 91
0x026614  mov.b     @(0x2,er4), r1l   ; 6e 49 00 02
0x026618  add.l     er1, er0   ; 0a 90
0x02661A  mov.l     er0, @0x40052a   ; 01 00 6b a0 00 40 05 2a
0x026622  bsr       0x0272d6   ; 5c 00 0c b0
0x026626  jmp       0x02679a   ; 5a 02 67 9a
0x02662A  mov.b     @(0x2,er6), r0l   ; 6e 68 00 02
0x02662E  cmp.b     #0x04, r0l   ; a8 04
0x026630  bne       0x026678   ; 46 46
0x026632  sub.l     er0, er0   ; 1a 80
0x026634  mov.b     @(0x6,er6), r0l   ; 6e 68 00 06
0x026638  mov.w     r0, e0   ; 0d 08
0x02663A  sub.w     r0, r0   ; 19 00
0x02663C  sub.l     er1, er1   ; 1a 91
0x02663E  mov.b     @(0x7,er6), r1l   ; 6e 69 00 07
0x026642  shll.l    #2, er1   ; 10 71
0x026644  shll.l    #2, er1   ; 10 71
0x026646  shll.l    #2, er1   ; 10 71
0x026648  shll.l    #2, er1   ; 10 71
0x02664A  add.l     er1, er0   ; 0a 90
0x02664C  sub.l     er1, er1   ; 1a 91
0x02664E  mov.b     @(0x8,er6), r1l   ; 6e 69 00 08
0x026652  add.l     er1, er0   ; 0a 90
0x026654  mov.l     er0, er6   ; 0f 86
0x026656  cmp.l     #0x00000010, er0   ; 7a 20 00 00 00 10
0x02665C  beq       0x026668   ; 47 0a
0x02665E  mov.w     #0x0050, r1   ; 79 01 00 50
0x026662  mov.w     r1, @er5   ; 69 d1
0x026664  jmp       0x02679a   ; 5a 02 67 9a
0x026668  mov.w     r6, r1   ; 0d 61
0x02666A  mov.l     er4, er0   ; 0f c0
0x02666C  jsr       0x0118d0   ; 5e 01 18 d0
0x026670  mov.l     er4, er0   ; 0f c0
0x026672  bsr       0x027362   ; 5c 00 0c ec
0x026676  bt        0x0266aa   ; 40 32
0x026678  jsr       0x01280c   ; 5e 01 28 0c
0x02667C  mov.w     @er5, r0   ; 69 50
0x02667E  bne       0x02679a   ; 58 60 01 18
0x026682  jsr       0x028676   ; 5e 02 86 76
0x026686  bclr      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 72 40
0x02668E  mov.b     #0x01, r0l   ; f8 01
0x026690  mov.b     r0l, @0x400d20   ; 6a a8 00 40 0d 20
0x026696  sub.b     r0l, r0l   ; 18 88
0x026698  mov.b     r0l, @0x400d21   ; 6a a8 00 40 0d 21
0x02669E  sub.b     r0l, r0l   ; 18 88
0x0266A0  mov.b     r0l, @0x400d22   ; 6a a8 00 40 0d 22
0x0266A6  bsr       0x027260   ; 5c 00 0b b6
0x0266AA  jmp       0x02679a   ; 5a 02 67 9a
0x0266AE  sub.l     er3, er3   ; 1a b3
0x0266B0  mov.b     @(0x6,er6), r3l   ; 6e 6b 00 06
0x0266B4  mov.w     r3, e3   ; 0d 3b
0x0266B6  sub.w     r3, r3   ; 19 33
0x0266B8  sub.l     er0, er0   ; 1a 80
0x0266BA  mov.b     @(0x7,er6), r0l   ; 6e 68 00 07
0x0266BE  shll.l    #2, er0   ; 10 70
0x0266C0  shll.l    #2, er0   ; 10 70
0x0266C2  shll.l    #2, er0   ; 10 70
0x0266C4  shll.l    #2, er0   ; 10 70
0x0266C6  add.l     er0, er3   ; 0a 83
0x0266C8  sub.l     er0, er0   ; 1a 80
0x0266CA  mov.b     @(0x8,er6), r0l   ; 6e 68 00 08
0x0266CE  add.l     er0, er3   ; 0a 83
0x0266D0  sub.l     er4, er4   ; 1a c4
0x0266D2  mov.b     @(0x3,er6), r4l   ; 6e 6c 00 03
0x0266D6  mov.w     r4, e4   ; 0d 4c
0x0266D8  sub.w     r4, r4   ; 19 44
0x0266DA  sub.l     er0, er0   ; 1a 80
0x0266DC  mov.b     @(0x4,er6), r0l   ; 6e 68 00 04
0x0266E0  shll.l    #2, er0   ; 10 70
0x0266E2  shll.l    #2, er0   ; 10 70
0x0266E4  shll.l    #2, er0   ; 10 70
0x0266E6  shll.l    #2, er0   ; 10 70
0x0266E8  add.l     er0, er4   ; 0a 84
0x0266EA  sub.l     er0, er0   ; 1a 80
0x0266EC  mov.b     @(0x5,er6), r0l   ; 6e 68 00 05
0x0266F0  add.l     er0, er4   ; 0a 84
0x0266F2  mov.b     r1l, r0l   ; 0c 98
0x0266F4  cmp.b     #0x02, r0l   ; a8 02
0x0266F6  bne       0x026794   ; 58 60 00 9a
0x0266FA  mov.b     @(0x2,er6), r0l   ; 6e 68 00 02
0x0266FE  bne       0x02678c   ; 58 60 00 8a
0x026702  mov.l     #0x0003ed60, er6   ; 7a 06 00 03 ed 60
0x026708  mov.l     @er6, er0   ; 01 00 69 60
0x02670C  cmp.l     er0, er4   ; 1f 84
0x02670E  bne       0x026732   ; 46 22
0x026710  mov.l     er4, er0   ; 0f c0
0x026712  add.l     er3, er0   ; 0a b0
0x026714  dec.l     #1, er0   ; 1b 70
0x026716  mov.l     @(0x4,er6), er1   ; 01 00 6f 61 00 04
0x02671C  cmp.l     er1, er0   ; 1f 90
0x02671E  bhi       0x026732   ; 42 12
0x026720  mov.w     r3, r1   ; 0d 31
0x026722  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x026728  jsr       0x0118d0   ; 5e 01 18 d0
0x02672C  bsr       0x02726e   ; 5c 00 0b 3e
0x026730  bt        0x02679a   ; 40 68
0x026732  mov.l     #0x00000001, er6   ; 7a 06 00 00 00 01
0x026738  mov.l     er4, er0   ; 0f c0
0x02673A  add.l     er3, er0   ; 0a b0
0x02673C  dec.l     #1, er0   ; 1b 70
0x02673E  mov.l     er0, er2   ; 0f 82
0x026740  bt        0x026784   ; 40 42
0x026742  mov.l     er6, er0   ; 0f e0
0x026744  shll.l    #2, er0   ; 10 70
0x026746  shll.l    er0   ; 10 30
0x026748  add.l     #0x0003ed60, er0   ; 7a 10 00 03 ed 60
0x02674E  mov.l     er0, er1   ; 0f 81
0x026750  mov.l     @er0, er0   ; 01 00 69 00
0x026754  cmp.l     er0, er4   ; 1f 84
0x026756  bcs       0x026782   ; 45 2a
0x026758  mov.l     er1, er0   ; 0f 90
0x02675A  adds.l    #4, er0   ; 0b 90
0x02675C  mov.l     @er0, er0   ; 01 00 69 00
