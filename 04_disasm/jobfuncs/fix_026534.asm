0x026534  stm.l     er2-er3, @-sp
0x026538  stm.l     er4-er6, @-sp
0x02653C  sub.l     #0x0000004a, sp
0x026542  mov.l     #0x00400436, er5
0x026548  mov.l     #0x0040043c, er6
0x02654E  mov.b     @(0x1,er6), r0l
0x026552  and.b     #0x18, r0l
0x026554  bne       0x02678c
0x026558  mov.b     @(0x9,er6), r0l
0x02655C  bne       0x02678c
0x026560  mov.b     @(0x1,er6), r0l
0x026564  and.b     #0x07, r0l
0x026566  mov.b     r0l, r1l
0x026568  cmp.b     #0x05, r0l
0x02656A  bne       0x0266ae
0x02656E  mov.b     @(0x2,er6), r1l
0x026572  cmp.b     #0x02, r1l
0x026574  bne       0x0265b6
0x026576  sub.l     er1, er1
0x026578  mov.b     @(0x6,er6), r1l
0x02657C  mov.w     r1, e1
0x02657E  sub.w     r1, r1
0x026580  sub.l     er2, er2
0x026582  mov.b     @(0x7,er6), r2l
0x026586  shll.l    #2, er2
0x026588  shll.l    #2, er2
0x02658A  shll.l    #2, er2
0x02658C  shll.l    #2, er2
0x02658E  add.l     er2, er1
0x026590  sub.l     er2, er2
0x026592  mov.b     @(0x8,er6), r2l
0x026596  add.l     er2, er1
0x026598  mov.l     er1, er6
0x02659A  cmp.l     #0x00020006, er1
0x0265A0  bls       0x0265ac
0x0265A2  mov.w     #0x0050, r2
0x0265A6  mov.w     r2, @er5
0x0265A8  jmp       0x02679a
0x0265AC  mov.l     er6, er0
0x0265AE  jsr       0x0170a0
0x0265B2  jmp       0x02679a
0x0265B6  mov.l     #0x00000001, er4
0x0265BC  add.l     sp, er4
0x0265BE  mov.b     @(0x2,er6), r0l
0x0265C2  cmp.b     #0x03, r0l
0x0265C4  bne       0x02662a
0x0265C6  sub.l     er0, er0
0x0265C8  mov.b     @(0x6,er6), r0l
0x0265CC  mov.w     r0, e0
0x0265CE  sub.w     r0, r0
0x0265D0  sub.l     er1, er1
0x0265D2  mov.b     @(0x7,er6), r1l
0x0265D6  shll.l    #2, er1
0x0265D8  shll.l    #2, er1
0x0265DA  shll.l    #2, er1
0x0265DC  shll.l    #2, er1
0x0265DE  add.l     er1, er0
0x0265E0  sub.l     er1, er1
0x0265E2  mov.b     @(0x8,er6), r1l
0x0265E6  add.l     er1, er0
0x0265E8  mov.l     er0, er6
0x0265EA  cmp.l     #0x00000003, er0
0x0265F0  bne       0x02665e
0x0265F2  mov.w     r6, r1
0x0265F4  mov.l     er4, er0
0x0265F6  jsr       0x0118d0
0x0265FA  sub.l     er0, er0
0x0265FC  mov.b     @(0x1,er4), r0l
0x026600  shll.l    #2, er0
0x026602  shll.l    #2, er0
0x026604  shll.l    #2, er0
0x026606  shll.l    #2, er0
0x026608  sub.l     er1, er1
0x02660A  mov.b     @er4, r1l
0x02660C  mov.w     r1, e1
0x02660E  sub.w     r1, r1
0x026610  add.l     er1, er0
0x026612  sub.l     er1, er1
0x026614  mov.b     @(0x2,er4), r1l
0x026618  add.l     er1, er0
0x02661A  mov.l     er0, @0x40052a
0x026622  bsr       0x0272d6
0x026626  jmp       0x02679a
0x02662A  mov.b     @(0x2,er6), r0l
0x02662E  cmp.b     #0x04, r0l
0x026630  bne       0x026678
0x026632  sub.l     er0, er0
0x026634  mov.b     @(0x6,er6), r0l
0x026638  mov.w     r0, e0
0x02663A  sub.w     r0, r0
0x02663C  sub.l     er1, er1
0x02663E  mov.b     @(0x7,er6), r1l
0x026642  shll.l    #2, er1
0x026644  shll.l    #2, er1
0x026646  shll.l    #2, er1
0x026648  shll.l    #2, er1
0x02664A  add.l     er1, er0
0x02664C  sub.l     er1, er1
0x02664E  mov.b     @(0x8,er6), r1l
0x026652  add.l     er1, er0
0x026654  mov.l     er0, er6
0x026656  cmp.l     #0x00000010, er0
0x02665C  beq       0x026668
0x02665E  mov.w     #0x0050, r1
0x026662  mov.w     r1, @er5
0x026664  jmp       0x02679a
0x026668  mov.w     r6, r1
0x02666A  mov.l     er4, er0
0x02666C  jsr       0x0118d0
0x026670  mov.l     er4, er0
0x026672  bsr       0x027362
0x026676  bt        0x0266aa
0x026678  jsr       0x01280c
0x02667C  mov.w     @er5, r0
0x02667E  bne       0x02679a
0x026682  jsr       0x028676
0x026686  bclr      #4, @0xffff2e
0x02668E  mov.b     #0x01, r0l
0x026690  mov.b     r0l, @0x400d20
0x026696  sub.b     r0l, r0l
0x026698  mov.b     r0l, @0x400d21
0x02669E  sub.b     r0l, r0l
0x0266A0  mov.b     r0l, @0x400d22
0x0266A6  bsr       0x027260
0x0266AA  jmp       0x02679a
0x0266AE  sub.l     er3, er3
0x0266B0  mov.b     @(0x6,er6), r3l
0x0266B4  mov.w     r3, e3
0x0266B6  sub.w     r3, r3
0x0266B8  sub.l     er0, er0
0x0266BA  mov.b     @(0x7,er6), r0l
0x0266BE  shll.l    #2, er0
0x0266C0  shll.l    #2, er0
0x0266C2  shll.l    #2, er0
0x0266C4  shll.l    #2, er0
0x0266C6  add.l     er0, er3
0x0266C8  sub.l     er0, er0
0x0266CA  mov.b     @(0x8,er6), r0l
0x0266CE  add.l     er0, er3
0x0266D0  sub.l     er4, er4
0x0266D2  mov.b     @(0x3,er6), r4l
0x0266D6  mov.w     r4, e4
0x0266D8  sub.w     r4, r4
0x0266DA  sub.l     er0, er0
0x0266DC  mov.b     @(0x4,er6), r0l
0x0266E0  shll.l    #2, er0
0x0266E2  shll.l    #2, er0
0x0266E4  shll.l    #2, er0
0x0266E6  shll.l    #2, er0
0x0266E8  add.l     er0, er4
0x0266EA  sub.l     er0, er0
0x0266EC  mov.b     @(0x5,er6), r0l
0x0266F0  add.l     er0, er4
0x0266F2  mov.b     r1l, r0l
0x0266F4  cmp.b     #0x02, r0l
0x0266F6  bne       0x026794
0x0266FA  mov.b     @(0x2,er6), r0l
0x0266FE  bne       0x02678c
0x026702  mov.l     #0x0003ed60, er6
0x026708  mov.l     @er6, er0
0x02670C  cmp.l     er0, er4
0x02670E  bne       0x026732
0x026710  mov.l     er4, er0
0x026712  add.l     er3, er0
0x026714  dec.l     #1, er0
0x026716  mov.l     @(0x4,er6), er1
0x02671C  cmp.l     er1, er0
0x02671E  bhi       0x026732
0x026720  mov.w     r3, r1
0x026722  mov.l     #0x00400ca0, er0
0x026728  jsr       0x0118d0
0x02672C  bsr       0x02726e
0x026730  bt        0x02679a
0x026732  mov.l     #0x00000001, er6
0x026738  mov.l     er4, er0
0x02673A  add.l     er3, er0
0x02673C  dec.l     #1, er0
0x02673E  mov.l     er0, er2
0x026740  bt        0x026784
0x026742  mov.l     er6, er0
0x026744  shll.l    #2, er0
0x026746  shll.l    er0
0x026748  add.l     #0x0003ed60, er0
0x02674E  mov.l     er0, er1
0x026750  mov.l     @er0, er0
0x026754  cmp.l     er0, er4
0x026756  bcs       0x026782
0x026758  mov.l     er1, er0
0x02675A  adds.l    #4, er0
0x02675C  mov.l     @er0, er0
0x026760  cmp.l     er0, er4
0x026762  bhi       0x026782
0x026764  shll.l    #2, er6
0x026766  shll.l    er6
0x026768  mov.l     er2, er0
0x02676A  mov.l     @(0x3ed64,er6), er6
0x026774  cmp.l     er6, er0
0x026776  bhi       0x02678c
0x026778  mov.w     r3, r1
0x02677A  mov.l     er4, er0
0x02677C  jsr       0x0118d0
0x026780  bt        0x02679a
0x026782  inc.l     #1, er6
0x026784  cmp.l     #0x00000005, er6
0x02678A  bcs       0x026742
0x02678C  mov.w     #0x0050, r0
0x026790  mov.w     r0, @er5
0x026792  bt        0x02679a
0x026794  mov.w     #0x0050, r0
0x026798  mov.w     r0, @er5
0x02679A  add.l     #0x0000004a, sp
0x0267A0  ldm.l     @sp+, er4-er6
0x0267A4  ldm.l     @sp+, er2-er3
0x0267A8  rts       
