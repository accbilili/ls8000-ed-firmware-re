0x0376EE  stm.l     er2-er3, @-sp
0x0376F2  stm.l     er4-er6, @-sp
0x0376F6  sub.l     #0x00000042, sp
0x0376FC  mov.l     #0x0044902c, er3
0x037702  mov.b     r0l, r4h
0x037704  mov.b     #0x02, r0l
0x037706  mov.b     r0l, @0x200001
0x03770C  sub.b     r4l, r4l
0x03770E  jmp       0x037892
0x037712  mov.b     r4l, r0l
0x037714  extu.w    r0
0x037716  extu.l    er0
0x037718  mov.b     @(0x400dab,er0), r5l
0x037720  mov.b     r5l, r6l
0x037722  extu.w    r6
0x037724  extu.l    er6
0x037726  mov.l     er6, @(0x3e,sp)
0x03772C  shll.l    #2, er6
0x03772E  mov.l     #0x00000010, er0
0x037734  add.l     sp, er0
0x037736  add.l     er6, er0
0x037738  mov.b     r5l, r1l
0x03773A  extu.w    r1
0x03773C  rotr.w    #2, r1
0x03773E  and.w     #0xc000, r1
0x037742  extu.l    er1
0x037744  shll.l    #2, er1
0x037746  add.l     #0x00c40000, er1
0x03774C  mov.l     er1, @er0
0x037750  mov.l     @(0x3e,sp), er0
0x037756  shll.l    er0
0x037758  mov.l     er0, @(0x34,sp)
0x03775E  add.l     er3, er0
0x037760  sub.w     r1, r1
0x037762  mov.w     r1, @er0
0x037764  mov.l     @(0x34,sp), er0
0x03776A  mov.w     r1, @(0x449034,er0)
0x037772  mov.l     @(0x400e0c,er6), er0
0x03777C  mov.l     @(0x400f42,er6), er1
0x037786  add.l     er1, er0
0x037788  jsr       0x01899e
0x03778C  mov.l     @(0x3e,sp), er1
0x037792  sub.l     er2, er2
0x037794  mov.b     @(0x41ff6e,er1), r2l
0x03779C  shll.l    #2, er2
0x03779E  mov.l     @(0x400dda,er2), er1
0x0377A8  jsr       0x0185ee
0x0377AC  jsr       0x018860
0x0377B0  mov.l     #0x00000020, er1
0x0377B6  add.l     sp, er1
0x0377B8  add.l     er6, er1
0x0377BA  mov.l     er0, @er1
0x0377BE  mov.b     @0x4007ca, r0l
0x0377C4  beq       0x03780e
0x0377C6  mov.b     r5l, r6l
0x0377C8  extu.w    r6
0x0377CA  extu.l    er6
0x0377CC  mov.l     er6, @(0x34,sp)
0x0377D2  shll.l    #2, er6
0x0377D4  mov.l     #0x00000020, er0
0x0377DA  add.l     sp, er0
0x0377DC  add.l     er0, er6
0x0377DE  mov.l     @er6, er1
0x0377E2  mov.l     #0x00000008, er0
0x0377E8  add.l     sp, er0
0x0377EA  jsr       0x018e68
0x0377EE  mov.l     @(0x34,sp), er1
0x0377F4  shll.l    #2, er1
0x0377F6  shll.l    er1
0x0377F8  add.l     #0x00420108, er1
0x0377FE  mov.l     er0, er2
0x037800  mov.l     sp, er0
0x037802  jsr       0x018aa0
0x037806  jsr       0x01876a
0x03780A  mov.l     er0, @er6
0x03780E  sub.l     er6, er6
0x037810  mov.b     r5l, r6l
0x037812  shll.l    #2, er6
0x037814  mov.l     #0x00000010, er0
0x03781A  add.l     sp, er0
0x03781C  add.l     er0, er6
0x03781E  mov.l     @er6, er6
0x037822  sub.w     r5, r5
0x037824  bt        0x037832
0x037826  mov.l     er6, er0
0x037828  adds.l    #4, er6
0x03782A  sub.l     er1, er1
0x03782C  mov.l     er1, @er0
0x037830  inc.w     #1, r5
0x037832  cmp.w     #0x1000, r5
0x037836  bcs       0x037826
0x037838  jsr       0x010b56
0x03783C  mov.w     #0x1000, r5
0x037840  bt        0x03784e
0x037842  mov.l     er6, er0
0x037844  adds.l    #4, er6
0x037846  sub.l     er1, er1
0x037848  mov.l     er1, @er0
0x03784C  inc.w     #1, r5
0x03784E  cmp.w     #0x2000, r5
0x037852  bcs       0x037842
0x037854  jsr       0x010b56
0x037858  mov.w     #0x2000, r5
0x03785C  bt        0x03786a
0x03785E  mov.l     er6, er0
0x037860  adds.l    #4, er6
0x037862  sub.l     er1, er1
0x037864  mov.l     er1, @er0
0x037868  inc.w     #1, r5
0x03786A  cmp.w     #0x3000, r5
0x03786E  bcs       0x03785e
0x037870  jsr       0x010b56
0x037874  mov.w     #0x3000, r5
0x037878  bt        0x037886
0x03787A  mov.l     er6, er0
0x03787C  adds.l    #4, er6
0x03787E  sub.l     er1, er1
0x037880  mov.l     er1, @er0
0x037884  inc.w     #1, r5
0x037886  cmp.w     #0x4000, r5
0x03788A  bcs       0x03787a
0x03788C  jsr       0x010b56
0x037890  inc.b     #1, r4l
0x037892  mov.b     @0x400daa, r0l
0x037898  cmp.b     r0l, r4l
0x03789A  bcs       0x037712
0x03789E  mov.b     @0x400daa, r0l
0x0378A4  cmp.b     #0x01, r0l
0x0378A6  bne       0x0378b2
0x0378A8  mov.b     @0x400dab, r0l
0x0378AE  cmp.b     #0x03, r0l
0x0378B0  beq       0x0378ba
0x0378B2  sub.w     r0, r0
0x0378B4  mov.w     r0, @0x44903c
0x0378BA  sub.w     e4, e4
0x0378BC  jmp       0x037998
0x0378C0  jsr       0x010b56
0x0378C4  jsr       0x02ace6
0x0378C8  btst      #7, @0x400400
0x0378D0  bne       0x037c5a
0x0378D4  mov.l     #0x00000020, er1
0x0378DA  add.l     sp, er1
0x0378DC  mov.b     @0x400daa, r0l
0x0378E2  jsr       0x02d700
0x0378E6  mov.w     @0x400e00, r0
0x0378EC  dec.w     #1, r0
0x0378EE  cmp.w     r0, e4
0x0378F0  beq       0x037928
0x0378F2  sub.l     er6, er6
0x0378F4  mov.w     e4, e4
0x0378F6  bne       0x037914
0x0378F8  mov.b     @0x449077, r0l
0x0378FE  extu.w    r0
0x037900  mov.w     r0, @(0xe,sp)
0x037904  mov.b     #0x01, r0h
0x037906  mov.l     er6, er1
0x037908  mov.w     @(0xe,sp), e0
0x03790C  mov.b     r4h, r0l
0x03790E  jsr       0x02ae52
0x037912  bt        0x037928
0x037914  mov.l     er6, @-sp
0x037918  mov.b     @0x449077, r0l
0x03791E  extu.w    r0
0x037920  sub.l     er1, er1
0x037922  jsr       0x02ad0a
0x037926  adds.l    #4, sp
0x037928  sub.b     r4l, r4l
0x03792A  bt        0x03798c
0x03792C  mov.b     r4l, r5l
0x03792E  extu.w    r5
0x037930  extu.l    er5
0x037932  sub.l     er0, er0
0x037934  mov.b     @(0x400dab,er5), r0l
0x03793C  shll.l    #2, er0
0x03793E  mov.l     @(0x420250,er0), er5
0x037948  mov.w     @0x400dfc, r1
0x03794E  extu.l    er1
0x037950  shll.l    er1
0x037952  add.l     er5, er1
0x037954  mov.l     er1, @(0x3e,sp)
0x03795A  mov.l     #0x00000010, er6
0x037960  add.l     sp, er6
0x037962  add.l     er0, er6
0x037964  mov.l     @er6, er6
0x037968  mov.l     @(0x3e,sp), er0
0x03796E  cmp.l     er0, er5
0x037970  bcc       0x037986
0x037972  mov.w     @er5+, r0
0x037974  extu.l    er0
0x037976  shll.l    #2, er0
0x037978  add.l     er6, er0
0x03797A  mov.l     @er0, er1
0x03797E  inc.l     #1, er1
0x037980  mov.l     er1, @er0
0x037984  bt        0x037968
0x037986  jsr       0x010b56
0x03798A  inc.b     #1, r4l
0x03798C  mov.b     @0x400daa, r0l
0x037992  cmp.b     r0l, r4l
0x037994  bcs       0x03792c
0x037996  inc.w     #1, e4
0x037998  mov.w     @0x400e00, r0
0x03799E  cmp.w     r0, e4
0x0379A0  bcs       0x0378c0
0x0379A4  btst      #7, @0x400400
0x0379AC  bne       0x037c5a
0x0379B0  sub.b     r0l, r0l
0x0379B2  jmp       0x037c4c
0x0379B6  sub.l     er0, er0
0x0379B8  mov.b     r2l, r0l
0x0379BA  mov.b     @(0x400dab,er0), r4h
0x0379C2  mov.b     r4h, r6l
0x0379C4  extu.w    r6
0x0379C6  extu.l    er6
0x0379C8  shll.l    #2, er6
0x0379CA  mov.l     #0x00000010, er0
0x0379D0  add.l     sp, er0
0x0379D2  add.l     er0, er6
0x0379D4  mov.l     @er6, er6
0x0379D8  mov.w     @0x400dfc, r0
0x0379DE  extu.l    er0
0x0379E0  mov.w     @0x400e00, r1
0x0379E6  extu.l    er1
0x0379E8  jsr       0x018e1e
0x0379EC  mov.l     #0x0000002a, er1
0x0379F2  jsr       0x018e1e
0x0379F6  mov.l     #0x00002710, er1
0x0379FC  jsr       0x01872e
0x037A00  mov.l     er0, er5
0x037A02  mov.b     #0x01, r4l
0x037A04  sub.w     e4, e4
0x037A06  mov.b     r4h, r0l
0x037A08  extu.w    r0
0x037A0A  extu.l    er0
0x037A0C  shll.l    er0
0x037A0E  mov.l     er0, er1
0x037A10  add.l     er3, er0
0x037A12  mov.l     er0, @(0x3a,sp)
0x037A18  mov.l     er1, er0
0x037A1A  add.l     #0x00449034, er0
0x037A20  mov.l     er0, @(0x34,sp)
0x037A26  bt        0x037a78
0x037A28  mov.w     e4, r0
0x037A2A  extu.l    er0
0x037A2C  shll.l    #2, er0
0x037A2E  add.l     er6, er0
0x037A30  mov.l     @er0, er1
0x037A34  beq       0x037a3e
0x037A36  mov.l     @(0x3a,sp), er0
0x037A3C  mov.w     e4, @er0
0x037A3E  cmp.b     #0x01, r4l
0x037A40  bne       0x037a6a
0x037A42  mov.w     e4, r0
0x037A44  extu.l    er0
0x037A46  shll.l    #2, er0
0x037A48  add.l     er6, er0
0x037A4A  mov.l     @er0, er0
0x037A4E  cmp.l     er5, er0
0x037A50  bhi       0x037a6a
0x037A52  mov.w     e4, r0
0x037A54  extu.l    er0
0x037A56  shll.l    #2, er0
0x037A58  add.l     er6, er0
0x037A5A  mov.l     @er0, er0
0x037A5E  sub.l     er0, er5
0x037A60  mov.l     @(0x34,sp), er0
0x037A66  mov.w     e4, @er0
0x037A68  bt        0x037a6c
0x037A6A  sub.b     r4l, r4l
0x037A6C  mov.w     #0x5a00, r0
0x037A70  mov.w     r0, @0xffffbc
0x037A76  inc.w     #1, e4
0x037A78  cmp.w     #0x1000, e4
0x037A7C  bcs       0x037a28
0x037A7E  jsr       0x010b56
0x037A82  mov.w     #0x1000, e4
0x037A86  mov.b     r4h, r0l
0x037A88  extu.w    r0
0x037A8A  extu.l    er0
0x037A8C  shll.l    er0
0x037A8E  mov.l     er0, er1
0x037A90  add.l     er3, er0
0x037A92  mov.l     er0, @(0x3a,sp)
0x037A98  mov.l     er1, er0
0x037A9A  add.l     #0x00449034, er0
0x037AA0  mov.l     er0, @(0x34,sp)
0x037AA6  bt        0x037af8
0x037AA8  mov.w     e4, r0
0x037AAA  extu.l    er0
0x037AAC  shll.l    #2, er0
0x037AAE  add.l     er6, er0
0x037AB0  mov.l     @er0, er1
0x037AB4  beq       0x037abe
0x037AB6  mov.l     @(0x3a,sp), er0
0x037ABC  mov.w     e4, @er0
0x037ABE  cmp.b     #0x01, r4l
0x037AC0  bne       0x037aea
0x037AC2  mov.w     e4, r0
0x037AC4  extu.l    er0
0x037AC6  shll.l    #2, er0
0x037AC8  add.l     er6, er0
0x037ACA  mov.l     @er0, er0
0x037ACE  cmp.l     er5, er0
0x037AD0  bhi       0x037aea
0x037AD2  mov.w     e4, r0
0x037AD4  extu.l    er0
0x037AD6  shll.l    #2, er0
0x037AD8  add.l     er6, er0
0x037ADA  mov.l     @er0, er0
0x037ADE  sub.l     er0, er5
0x037AE0  mov.l     @(0x34,sp), er0
0x037AE6  mov.w     e4, @er0
0x037AE8  bt        0x037aec
0x037AEA  sub.b     r4l, r4l
0x037AEC  mov.w     #0x5a00, r0
0x037AF0  mov.w     r0, @0xffffbc
0x037AF6  inc.w     #1, e4
0x037AF8  cmp.w     #0x2000, e4
0x037AFC  bcs       0x037aa8
0x037AFE  jsr       0x010b56
0x037B02  mov.w     #0x2000, e4
0x037B06  mov.b     r4h, r0l
0x037B08  extu.w    r0
0x037B0A  extu.l    er0
0x037B0C  shll.l    er0
0x037B0E  mov.l     er0, er1
0x037B10  add.l     er3, er0
0x037B12  mov.l     er0, @(0x3a,sp)
0x037B18  mov.l     er1, er0
0x037B1A  add.l     #0x00449034, er0
0x037B20  mov.l     er0, @(0x34,sp)
0x037B26  bt        0x037b78
0x037B28  mov.w     e4, r0
0x037B2A  extu.l    er0
0x037B2C  shll.l    #2, er0
0x037B2E  add.l     er6, er0
0x037B30  mov.l     @er0, er1
0x037B34  beq       0x037b3e
0x037B36  mov.l     @(0x3a,sp), er0
0x037B3C  mov.w     e4, @er0
0x037B3E  cmp.b     #0x01, r4l
0x037B40  bne       0x037b6a
0x037B42  mov.w     e4, r0
0x037B44  extu.l    er0
0x037B46  shll.l    #2, er0
0x037B48  add.l     er6, er0
0x037B4A  mov.l     @er0, er0
0x037B4E  cmp.l     er5, er0
0x037B50  bhi       0x037b6a
0x037B52  mov.w     e4, r0
0x037B54  extu.l    er0
0x037B56  shll.l    #2, er0
0x037B58  add.l     er6, er0
0x037B5A  mov.l     @er0, er0
0x037B5E  sub.l     er0, er5
0x037B60  mov.l     @(0x34,sp), er0
0x037B66  mov.w     e4, @er0
0x037B68  bt        0x037b6c
0x037B6A  sub.b     r4l, r4l
0x037B6C  mov.w     #0x5a00, r0
0x037B70  mov.w     r0, @0xffffbc
0x037B76  inc.w     #1, e4
0x037B78  cmp.w     #0x3000, e4
0x037B7C  bcs       0x037b28
0x037B7E  jsr       0x010b56
0x037B82  mov.w     #0x3000, e4
0x037B86  mov.b     r4h, r0l
0x037B88  extu.w    r0
0x037B8A  extu.l    er0
0x037B8C  shll.l    er0
0x037B8E  mov.l     er0, er1
0x037B90  add.l     er3, er0
0x037B92  mov.l     er0, @(0x3a,sp)
0x037B98  mov.l     er1, er0
0x037B9A  add.l     #0x00449034, er0
0x037BA0  mov.l     er0, @(0x34,sp)
0x037BA6  bt        0x037bf8
0x037BA8  mov.w     e4, r0
0x037BAA  extu.l    er0
0x037BAC  shll.l    #2, er0
0x037BAE  add.l     er6, er0
0x037BB0  mov.l     @er0, er1
0x037BB4  beq       0x037bbe
0x037BB6  mov.l     @(0x3a,sp), er0
0x037BBC  mov.w     e4, @er0
0x037BBE  cmp.b     #0x01, r4l
0x037BC0  bne       0x037bea
0x037BC2  mov.w     e4, r0
0x037BC4  extu.l    er0
0x037BC6  shll.l    #2, er0
0x037BC8  add.l     er6, er0
0x037BCA  mov.l     @er0, er0
0x037BCE  cmp.l     er5, er0
0x037BD0  bhi       0x037bea
0x037BD2  mov.w     e4, r0
0x037BD4  extu.l    er0
0x037BD6  shll.l    #2, er0
0x037BD8  add.l     er6, er0
0x037BDA  mov.l     @er0, er0
0x037BDE  sub.l     er0, er5
0x037BE0  mov.l     @(0x34,sp), er0
0x037BE6  mov.w     e4, @er0
0x037BE8  bt        0x037bec
0x037BEA  sub.b     r4l, r4l
0x037BEC  mov.w     #0x5a00, r0
0x037BF0  mov.w     r0, @0xffffbc
0x037BF6  inc.w     #1, e4
0x037BF8  cmp.w     #0x4000, e4
0x037BFC  bcs       0x037ba8
0x037BFE  cmp.b     #0x03, r4h
0x037C00  beq       0x037c30
0x037C02  mov.b     r4h, r0l
0x037C04  extu.w    r0
0x037C06  extu.l    er0
0x037C08  shll.l    er0
0x037C0A  add.l     er3, er0
0x037C0C  mov.w     @0x44903c, r1
0x037C12  mov.w     @er0, r0
0x037C14  cmp.w     r0, r1
0x037C16  bcc       0x037c30
0x037C18  mov.b     r4h, r0l
0x037C1A  extu.w    r0
0x037C1C  extu.l    er0
0x037C1E  shll.l    er0
0x037C20  add.l     er3, er0
0x037C22  mov.w     @er0, r0
0x037C24  mov.w     r0, @0x44903c
0x037C2A  mov.b     r4h, @0x44903e
0x037C30  sub.l     er6, er6
0x037C32  mov.b     r4h, r6l
0x037C34  shll.l    er6
0x037C36  mov.l     er3, er0
0x037C38  add.l     er6, er0
0x037C3A  mov.w     @er0, r0
0x037C3C  mov.w     r0, @(0x449024,er6)
0x037C44  jsr       0x010b56
0x037C48  mov.b     r2l, r0l
0x037C4A  inc.b     #1, r0l
0x037C4C  mov.b     r0l, r2l
0x037C4E  mov.b     @0x400daa, r1l
0x037C54  cmp.b     r1l, r0l
0x037C56  bcs       0x0379b6
0x037C5A  add.l     #0x00000042, sp
0x037C60  ldm.l     @sp+, er4-er6
0x037C64  ldm.l     @sp+, er2-er3
0x037C68  rts       
