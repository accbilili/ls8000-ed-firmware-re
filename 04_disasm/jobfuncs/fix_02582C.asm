0x0256BC  cmp.b     #0x2e, r4l
0x0256BE  bne       0x025732
0x0256C0  mov.l     #0x0000012a, er3
0x0256C6  add.l     sp, er3
0x0256C8  mov.b     @er5, r0l
0x0256CA  mov.b     r0l, @er3
0x0256CC  mov.b     @(0x1,er5), r0l
0x0256D0  mov.b     r0l, @(0x1,er3)
0x0256D4  mov.b     @(0x2,er5), r0l
0x0256D8  mov.b     r0l, @(0x2,er3)
0x0256DC  mov.b     @(0x3,er5), r0l
0x0256E0  mov.b     r0l, @(0x3,er3)
0x0256E4  mov.b     @(0xfffb,er5), r0l
0x0256E8  and.b     #0x01, r0l
0x0256EA  extu.w    r0
0x0256EC  extu.l    er0
0x0256EE  shll.l    #2, er0
0x0256F0  shll.l    #2, er0
0x0256F2  add.l     #0x00400e1c, er0
0x0256F8  mov.l     @(0x132,sp), er1
0x0256FE  add.l     er1, er0
0x025700  mov.l     @er0, er1
0x025704  mov.l     er1, @(0x12a,sp)
0x02570A  mov.l     er6, er0
0x02570C  inc.l     #1, er6
0x02570E  mov.b     @er3+, r1l
0x025710  mov.b     r1l, @er0
0x025712  mov.l     er6, er0
0x025714  inc.l     #1, er6
0x025716  mov.b     @er3+, r1l
0x025718  mov.b     r1l, @er0
0x02571A  mov.l     er6, er0
0x02571C  inc.l     #1, er6
0x02571E  mov.b     @er3+, r1l
0x025720  mov.b     r1l, @er0
0x025722  mov.l     er6, er0
0x025724  inc.l     #1, er6
0x025726  mov.b     @er3, r3l
0x025728  mov.b     r3l, @er0
0x02572A  adds.l    #4, er5
0x02572C  add.b     #0x03, r4l
0x02572E  jmp       0x02582a
0x025732  cmp.b     #0x33, r4l
0x025734  bne       0x025764
0x025736  mov.l     er6, er0
0x025738  inc.l     #1, er6
0x02573A  mov.l     @(0x13a,sp), er1
0x025740  mov.w     @er1, r1
0x025742  inc.w     #1, r1
0x025744  mov.b     r1h, r1l
0x025746  sub.b     r1h, r1h
0x025748  mov.b     r1l, @er0
0x02574A  mov.l     er6, er0
0x02574C  inc.l     #1, er6
0x02574E  mov.l     @(0x13a,sp), er1
0x025754  mov.b     @(0x1,er1), r1l
0x025758  add.b     #0x01, r1l
0x02575A  mov.b     r1l, @er0
0x02575C  inc.l     #2, er5
0x02575E  inc.b     #1, r4l
0x025760  jmp       0x02582a
0x025764  cmp.b     #0x35, r4l
0x025766  bne       0x02580a
0x02576A  mov.l     #0x0000012a, er3
0x025770  add.l     sp, er3
0x025772  mov.b     @er5, r0l
0x025774  mov.b     r0l, @er3
0x025776  mov.b     @(0x1,er5), r0l
0x02577A  mov.b     r0l, @(0x1,er3)
0x02577E  mov.b     @(0x2,er5), r0l
0x025782  mov.b     r0l, @(0x2,er3)
0x025786  mov.b     @(0x3,er5), r0l
0x02578A  mov.b     r0l, @(0x3,er3)
0x02578E  mov.b     @(0xfff4,er5), r1l
0x025792  and.b     #0x01, r1l
0x025794  extu.w    r1
0x025796  extu.l    er1
0x025798  shll.l    #2, er1
0x02579A  shll.l    #2, er1
0x02579C  mov.b     r4h, r0l
0x02579E  extu.w    r0
0x0257A0  extu.l    er0
0x0257A2  mov.l     er0, @(0x13e,sp)
0x0257A8  shll.l    #2, er0
0x0257AA  add.l     #0x00400e1c, er1
0x0257B0  add.l     er1, er0
0x0257B2  mov.l     @er0, er0
0x0257B6  jsr       0x018e9e
0x0257BA  mov.l     @(0x13e,sp), er1
0x0257C0  sub.l     er2, er2
0x0257C2  mov.b     @(0x41ff6e,er1), r2l
0x0257CA  shll.l    #2, er2
0x0257CC  mov.l     @(0x400dda,er2), er1
0x0257D6  jsr       0x0185ee
0x0257DA  jsr       0x018860
0x0257DE  mov.l     er0, @(0x12a,sp)
0x0257E4  mov.l     er6, er0
0x0257E6  inc.l     #1, er6
0x0257E8  mov.b     @er3+, r1l
0x0257EA  mov.b     r1l, @er0
0x0257EC  mov.l     er6, er0
0x0257EE  inc.l     #1, er6
0x0257F0  mov.b     @er3+, r1l
0x0257F2  mov.b     r1l, @er0
0x0257F4  mov.l     er6, er0
0x0257F6  inc.l     #1, er6
0x0257F8  mov.b     @er3+, r1l
0x0257FA  mov.b     r1l, @er0
0x0257FC  mov.l     er6, er0
0x0257FE  inc.l     #1, er6
0x025800  mov.b     @er3, r3l
0x025802  mov.b     r3l, @er0
0x025804  adds.l    #4, er5
0x025806  add.b     #0x03, r4l
0x025808  bt        0x02582a
0x02580A  cmp.b     #0x39, r4l
0x02580C  bne       0x025822
0x02580E  mov.l     er6, er0
0x025810  inc.l     #1, er6
0x025812  mov.l     @(0x12e,sp), er1
0x025818  mov.b     @er1, r1l
0x02581A  add.b     #0x01, r1l
0x02581C  mov.b     r1l, @er0
0x02581E  inc.l     #1, er5
0x025820  bt        0x02582a
0x025822  mov.l     er6, er0
0x025824  inc.l     #1, er6
0x025826  mov.b     @er5+, r1l
0x025828  mov.b     r1l, @er0
0x02582A  inc.b     #1, r4l
0x02582C  mov.b     @(0x142,sp), r0l
0x025830  cmp.b     r0l, r4l
0x025832  bcs       0x0256bc
0x025836  jmp       0x025a3c
0x025A3C  mov.l     sp, er0
0x025A3E  mov.w     @(0x138,sp), r1
0x025A42  jsr       0x011900
0x025A46  add.l     #0x00000144, sp
0x025A4C  ldm.l     @sp+, er4-er6
0x025A50  ldm.l     @sp+, er2-er3
0x025A54  rts       
