0x0387AA  stm.l     er2-er3, @-sp
0x0387AE  stm.l     er4-er6, @-sp
0x0387B2  sub.l     #0x00000040, sp
0x0387B8  mov.l     #0x00400e1c, er3
0x0387BE  mov.l     #0x00400e0c, er4
0x0387C4  mov.l     #0x0044904c, er5
0x0387CA  mov.l     #0x00400d7a, er6
0x0387D0  mov.b     @er6, r0l
0x0387D2  cmp.b     #0x40, r0l
0x0387D4  beq       0x0387fa
0x0387D6  mov.b     @er6, r0l
0x0387D8  cmp.b     #0x04, r0l
0x0387DA  bne       0x0387e6
0x0387DC  mov.b     @0x400db4, r0l
0x0387E2  cmp.b     #0x01, r0l
0x0387E4  beq       0x0387fa
0x0387E6  mov.b     @er6, r0l
0x0387E8  cmp.b     #0x08, r0l
0x0387EA  bne       0x038c1c
0x0387EE  mov.b     @0x400db4, r0l
0x0387F4  cmp.b     #0x01, r0l
0x0387F6  bne       0x038c1c
0x0387FA  mov.l     #0x0003f868, er0
0x038800  mov.l     #0x00000030, er1
0x038806  add.l     sp, er1
0x038808  jsr       0x018e36
0x03880C  sub.b     r6h, r6h
0x03880E  mov.l     er5, er0
0x038810  add.l     #0x00000018, er0
0x038816  mov.l     er0, @(0x38,sp)
0x03881C  jmp       0x038998
0x038820  mov.b     r6h, r0l
0x038822  extu.w    r0
0x038824  extu.l    er0
0x038826  mov.b     @(0x449040,er0), r6l
0x03882E  cmp.b     #0x03, r6l
0x038830  beq       0x038920
0x038834  mov.b     r6l, r1l
0x038836  extu.w    r1
0x038838  extu.l    er1
0x03883A  shll.l    #2, er1
0x03883C  mov.l     er1, @(0x3c,sp)
0x038842  mov.l     @(0x3c,sp), er0
0x038848  mov.l     @(0x400f32,er1), er1
0x038852  mov.l     @(0x400f42,er0), er0
0x03885C  add.l     er0, er1
0x03885E  shll.l    #2, er1
0x038860  shll.l    #2, er1
0x038862  shll.l    #2, er1
0x038864  mov.l     #0x00000028, er0
0x03886A  add.l     sp, er0
0x03886C  jsr       0x018958
0x038870  mov.l     @(0x3c,sp), er1
0x038876  add.l     er4, er1
0x038878  mov.l     @er1, er1
0x03887C  mov.l     er0, @(0x1c,sp)
0x038882  mov.l     #0x00000020, er0
0x038888  add.l     sp, er0
0x03888A  jsr       0x018e68
0x03888E  mov.l     @(0x1c,sp), er1
0x038894  mov.l     er0, er2
0x038896  mov.l     #0x00000014, er0
0x03889C  add.l     sp, er0
0x03889E  jsr       0x01842c
0x0388A2  mov.l     er0, er1
0x0388A4  mov.l     #0x00000030, er0
0x0388AA  add.l     sp, er0
0x0388AC  jsr       0x0188d2
0x0388B0  mov.w     r0, r0
0x0388B2  beq       0x038996
0x0388B6  sub.l     er1, er1
0x0388B8  mov.b     r6l, r1l
0x0388BA  shll.l    #2, er1
0x0388BC  mov.l     er1, @(0x3c,sp)
0x0388C2  mov.l     @(0x3c,sp), er0
0x0388C8  mov.l     @(0x400f32,er1), er1
0x0388D2  mov.l     @(0x400f42,er0), er0
0x0388DC  add.l     er0, er1
0x0388DE  shll.l    #2, er1
0x0388E0  shll.l    #2, er1
0x0388E2  shll.l    #2, er1
0x0388E4  mov.l     #0x00000028, er0
0x0388EA  add.l     sp, er0
0x0388EC  jsr       0x018958
0x0388F0  mov.l     @(0x3c,sp), er1
0x0388F6  add.l     er4, er1
0x0388F8  mov.l     @er1, er1
0x0388FC  mov.l     er0, @(0x1c,sp)
0x038902  mov.l     #0x00000020, er0
0x038908  add.l     sp, er0
0x03890A  jsr       0x018e68
0x03890E  mov.l     @(0x1c,sp), er1
0x038914  mov.l     er0, er2
0x038916  mov.l     #0x00000030, er0
0x03891C  add.l     sp, er0
0x03891E  bt        0x038992
0x038920  mov.l     @(0x38,sp), er0
0x038926  sub.l     er1, er1
0x038928  mov.b     r6l, r1l
0x03892A  shll.l    #2, er1
0x03892C  mov.l     er1, @(0x3c,sp)
0x038932  mov.l     @(0x3c,sp), er2
0x038938  mov.l     @(0x400f32,er1), er1
0x038942  mov.l     @(0x400f42,er2), er2
0x03894C  add.l     er2, er1
0x03894E  shll.l    #2, er1
0x038950  shll.l    #2, er1
0x038952  shll.l    #2, er1
0x038954  mov.l     er0, @(0x24,sp)
0x03895A  mov.l     #0x00000028, er0
0x038960  add.l     sp, er0
0x038962  jsr       0x018958
0x038966  mov.l     @(0x3c,sp), er1
0x03896C  add.l     er4, er1
0x03896E  mov.l     @er1, er1
0x038972  mov.l     er0, @(0x18,sp)
0x038978  mov.l     #0x0000001c, er0
0x03897E  add.l     sp, er0
0x038980  jsr       0x018e68
0x038984  mov.l     @(0x18,sp), er1
0x03898A  mov.l     er0, er2
0x03898C  mov.l     @(0x24,sp), er0
0x038992  jsr       0x01842c
0x038996  inc.b     #1, r6h
0x038998  mov.b     @0x44903f, r0l
0x03899E  cmp.b     r0l, r6h
0x0389A0  bcs       0x038820
0x0389A4  mov.l     #0x00000030, er0
0x0389AA  add.l     sp, er0
0x0389AC  mov.l     er5, er1
0x0389AE  jsr       0x018e36
0x0389B2  mov.l     #0x00000030, er0
0x0389B8  add.l     sp, er0
0x0389BA  mov.l     #0x00000008, er1
0x0389C0  add.l     er5, er1
0x0389C2  jsr       0x018e36
0x0389C6  mov.l     #0x00000030, er0
0x0389CC  add.l     sp, er0
0x0389CE  mov.l     #0x00000010, er1
0x0389D4  add.l     er5, er1
0x0389D6  jsr       0x018e36
0x0389DA  sub.b     r6h, r6h
0x0389DC  jmp       0x038c0c
0x0389E0  mov.b     r6h, r0l
0x0389E2  extu.w    r0
0x0389E4  extu.l    er0
0x0389E6  mov.b     @(0x449040,er0), r6l
0x0389EE  cmp.b     #0x03, r6l
0x0389F0  beq       0x038a4a
0x0389F2  mov.b     r6l, r1l
0x0389F4  extu.w    r1
0x0389F6  extu.l    er1
0x0389F8  mov.l     er1, @(0x2c,sp)
0x0389FE  mov.l     @(0x2c,sp), er0
0x038A04  mov.b     @(0x400db8,er0), r1l
0x038A0C  extu.w    r1
0x038A0E  mov.l     #0x00000024, er0
0x038A14  add.l     sp, er0
0x038A16  jsr       0x018ede
0x038A1A  mov.l     er0, er1
0x038A1C  mov.l     #0x0003f870, er2
0x038A22  mov.l     #0x0000001c, er0
0x038A28  add.l     sp, er0
0x038A2A  jsr       0x018aa0
0x038A2E  mov.l     er0, er1
0x038A30  mov.l     #0x0003f878, er2
0x038A36  mov.l     #0x00000014, er0
0x038A3C  add.l     sp, er0
0x038A3E  jsr       0x01842c
0x038A42  mov.w     @0x44903c, r1
0x038A48  bt        0x038ab0
0x038A4A  mov.b     r6l, r1l
0x038A4C  extu.w    r1
0x038A4E  extu.l    er1
0x038A50  mov.l     er1, @(0x3c,sp)
0x038A56  mov.l     er1, @(0x2c,sp)
0x038A5C  mov.l     @(0x2c,sp), er0
0x038A62  mov.b     @(0x400db8,er0), r1l
0x038A6A  extu.w    r1
0x038A6C  mov.l     #0x00000024, er0
0x038A72  add.l     sp, er0
0x038A74  jsr       0x018ede
0x038A78  mov.l     er0, er1
0x038A7A  mov.l     #0x0003f870, er2
0x038A80  mov.l     #0x0000001c, er0
0x038A86  add.l     sp, er0
0x038A88  jsr       0x018aa0
0x038A8C  mov.l     er0, er1
0x038A8E  mov.l     #0x0003f878, er2
0x038A94  mov.l     #0x00000014, er0
0x038A9A  add.l     sp, er0
0x038A9C  jsr       0x01842c
0x038AA0  mov.l     @(0x3c,sp), er1
0x038AA6  shll.l    er1
0x038AA8  mov.w     @(0x44902c,er1), r1
0x038AB0  mov.l     er0, @(0x8,sp)
0x038AB6  mov.l     #0x0000000c, er0
0x038ABC  add.l     sp, er0
0x038ABE  jsr       0x018ede
0x038AC2  mov.l     @(0x8,sp), er1
0x038AC8  mov.l     er0, er2
0x038ACA  mov.l     sp, er0
0x038ACC  jsr       0x01842c
0x038AD0  mov.l     #0x00449044, er1
0x038AD6  jsr       0x018e36
0x038ADA  mov.b     r6l, r1l
0x038ADC  extu.w    r1
0x038ADE  extu.l    er1
0x038AE0  shll.l    #2, er1
0x038AE2  shll.l    er1
0x038AE4  add.l     er5, er1
0x038AE6  mov.l     #0x00449044, er0
0x038AEC  jsr       0x0188d2
0x038AF0  mov.w     r0, r0
0x038AF2  beq       0x038b0a
0x038AF4  mov.b     r6l, r0l
0x038AF6  extu.w    r0
0x038AF8  extu.l    er0
0x038AFA  shll.l    #2, er0
0x038AFC  shll.l    er0
0x038AFE  add.l     er5, er0
0x038B00  mov.l     #0x00449044, er1
0x038B06  jsr       0x018e36
0x038B0A  mov.b     r6l, r0l
0x038B0C  extu.w    r0
0x038B0E  extu.l    er0
0x038B10  shll.l    #2, er0
0x038B12  mov.l     er0, @(0x3c,sp)
0x038B18  sub.l     er1, er1
0x038B1A  mov.b     @0x400db4, r1l
0x038B20  shll.l    #2, er1
0x038B22  shll.l    #2, er1
0x038B24  add.l     er3, er1
0x038B26  add.l     er0, er1
0x038B28  add.l     er4, er0
0x038B2A  mov.l     er1, @(0x2c,sp)
0x038B30  mov.l     @er0, er1
0x038B34  mov.l     #0x00000024, er0
0x038B3A  add.l     sp, er0
0x038B3C  jsr       0x018e68
0x038B40  mov.l     er0, er1
0x038B42  mov.l     #0x00449044, er2
0x038B48  mov.l     #0x0000001c, er0
0x038B4E  add.l     sp, er0
0x038B50  jsr       0x018aa0
0x038B54  jsr       0x01876a
0x038B58  mov.l     @(0x3c,sp), er1
0x038B5E  mov.l     @(0x400f42,er1), er1
0x038B68  add.l     er1, er0
0x038B6A  mov.l     @(0x2c,sp), er1
0x038B70  mov.l     er0, @er1
0x038B74  sub.l     er0, er0
0x038B76  mov.b     @0x400db4, r0l
0x038B7C  shll.l    #2, er0
0x038B7E  shll.l    #2, er0
0x038B80  add.l     er3, er0
0x038B82  mov.l     @(0x3c,sp), er1
0x038B88  add.l     er1, er0
0x038B8A  mov.l     @er0, er0
0x038B8E  cmp.l     #0x03ffffff, er0
0x038B94  bls       0x038bb8
0x038B96  sub.l     er0, er0
0x038B98  mov.b     @0x400db4, r0l
0x038B9E  shll.l    #2, er0
0x038BA0  shll.l    #2, er0
0x038BA2  add.l     er3, er0
0x038BA4  mov.b     r6l, r1l
0x038BA6  extu.w    r1
0x038BA8  extu.l    er1
0x038BAA  shll.l    #2, er1
0x038BAC  add.l     er1, er0
0x038BAE  mov.l     #0x03ffffff, er1
0x038BB4  mov.l     er1, @er0
0x038BB8  sub.l     er0, er0
0x038BBA  mov.b     r6l, r0l
0x038BBC  shll.l    er0
0x038BBE  mov.l     er0, @(0x3c,sp)
0x038BC4  mov.l     @(0x3c,sp), er1
0x038BCA  mov.w     @(0x449024,er1), r1
0x038BD2  mov.l     er0, @(0x24,sp)
0x038BD8  mov.l     #0x00000028, er0
0x038BDE  add.l     sp, er0
0x038BE0  jsr       0x018ede
0x038BE4  mov.l     er0, er1
0x038BE6  mov.l     #0x00449044, er2
0x038BEC  mov.l     #0x0000001c, er0
0x038BF2  add.l     sp, er0
0x038BF4  jsr       0x018aa0
0x038BF8  jsr       0x01876a
0x038BFC  mov.l     @(0x24,sp), er1
0x038C02  mov.w     r0, @(0x400e5c,er1)
0x038C0A  inc.b     #1, r6h
0x038C0C  mov.b     @0x44903f, r0l
0x038C12  cmp.b     r0l, r6h
0x038C14  bcs       0x0389e0
0x038C18  jmp       0x0390b0
0x038C1C  mov.b     @er6, r0l
0x038C1E  cmp.b     #0x20, r0l
0x038C20  beq       0x038c42
0x038C22  mov.b     @er6, r0l
0x038C24  cmp.b     #0x04, r0l
0x038C26  bne       0x038c30
0x038C28  mov.b     @0x400db4, r0l
0x038C2E  beq       0x038c42
0x038C30  mov.b     @er6, r0l
0x038C32  cmp.b     #0x08, r0l
0x038C34  bne       0x0390b0
0x038C38  mov.b     @0x400db4, r0l
0x038C3E  bne       0x0390b0
0x038C42  mov.l     #0x0003f880, er0
0x038C48  mov.l     er5, er1
0x038C4A  jsr       0x018e36
0x038C4E  mov.l     #0x0003f880, er0
0x038C54  mov.l     #0x00000008, er1
0x038C5A  add.l     er5, er1
0x038C5C  jsr       0x018e36
0x038C60  mov.l     #0x0003f880, er0
0x038C66  mov.l     #0x00000010, er1
0x038C6C  add.l     er5, er1
0x038C6E  jsr       0x018e36
0x038C72  mov.l     #0x0003f880, er0
0x038C78  mov.l     #0x00000018, er1
0x038C7E  add.l     er5, er1
0x038C80  jsr       0x018e36
0x038C84  sub.b     r6h, r6h
0x038C86  jmp       0x0390a4
0x038C8A  mov.b     r6h, r0l
0x038C8C  extu.w    r0
0x038C8E  extu.l    er0
0x038C90  mov.b     @(0x449040,er0), r6l
0x038C98  mov.b     r6l, r1l
0x038C9A  extu.w    r1
0x038C9C  extu.l    er1
0x038C9E  shll.l    #2, er1
0x038CA0  mov.l     er1, @(0x3c,sp)
0x038CA6  add.l     er4, er1
0x038CA8  mov.l     @er1, er1
0x038CAC  mov.l     #0x00000028, er0
0x038CB2  add.l     sp, er0
0x038CB4  jsr       0x018e68
0x038CB8  mov.l     @(0x3c,sp), er1
0x038CBE  mov.l     @(0x400f32,er1), er1
0x038CC8  mov.l     er0, @(0x1c,sp)
0x038CCE  mov.l     #0x00000020, er0
0x038CD4  add.l     sp, er0
0x038CD6  jsr       0x018e68
0x038CDA  mov.l     @(0x1c,sp), er1
0x038CE0  mov.l     er0, er2
0x038CE2  mov.l     #0x0044906c, er0
0x038CE8  jsr       0x01842c
0x038CEC  cmp.b     #0x03, r6l
0x038CEE  beq       0x038e84
0x038CF2  mov.b     @0x400d7a, r0l
0x038CF8  cmp.b     #0x08, r0l
0x038CFA  bne       0x038e84
0x038CFE  mov.b     @0x400db4, r0l
0x038D04  bne       0x038e84
0x038D08  mov.b     r6l, r1l
0x038D0A  extu.w    r1
0x038D0C  extu.l    er1
0x038D0E  mov.l     er1, @(0x3c,sp)
0x038D14  shll.l    er1
0x038D16  mov.w     @(0x44902c,er1), r1
0x038D1E  mov.l     #0x00000028, er0
0x038D24  add.l     sp, er0
0x038D26  jsr       0x018ede
0x038D2A  mov.l     @(0x3c,sp), er1
0x038D30  shll.l    #2, er1
0x038D32  shll.l    er1
0x038D34  add.l     #0x00400e74, er1
0x038D3A  mov.l     #0x0044906c, er2
0x038D40  mov.l     er0, @(0x1c,sp)
0x038D46  mov.l     #0x00000020, er0
0x038D4C  add.l     sp, er0
0x038D4E  jsr       0x018aa0
0x038D52  mov.l     er0, er1
0x038D54  mov.l     @(0x1c,sp), er0
0x038D5A  jsr       0x018938
0x038D5E  mov.w     r0, r0
0x038D60  beq       0x038dc0
0x038D62  mov.b     r6l, r0l
0x038D64  extu.w    r0
0x038D66  extu.l    er0
0x038D68  mov.l     er0, @(0x3c,sp)
0x038D6E  shll.l    er0
0x038D70  mov.l     @(0x3c,sp), er1
0x038D76  shll.l    #2, er1
0x038D78  shll.l    er1
0x038D7A  mov.l     er0, @(0x2c,sp)
0x038D80  mov.l     #0x00400e74, er0
0x038D86  add.l     er1, er0
0x038D88  jsr       0x01876a
0x038D8C  mov.w     r0, r1
0x038D8E  mov.l     #0x00000024, er0
0x038D94  add.l     sp, er0
0x038D96  jsr       0x018ede
0x038D9A  mov.l     er0, er1
0x038D9C  mov.l     #0x0044906c, er2
0x038DA2  mov.l     #0x0000001c, er0
0x038DA8  add.l     sp, er0
0x038DAA  jsr       0x018aa0
0x038DAE  jsr       0x01876a
0x038DB2  mov.l     @(0x2c,sp), er1
0x038DB8  mov.w     r0, @(0x44902c,er1)
0x038DC0  mov.b     @0x400ec4, r0l
0x038DC6  cmp.b     #0x01, r0l
0x038DC8  beq       0x038e84
0x038DCC  mov.b     r6l, r1l
0x038DCE  extu.w    r1
0x038DD0  extu.l    er1
0x038DD2  mov.l     er1, @(0x3c,sp)
0x038DD8  shll.l    er1
0x038DDA  mov.w     @(0x449034,er1), r1
0x038DE2  mov.l     #0x00000028, er0
0x038DE8  add.l     sp, er0
0x038DEA  jsr       0x018ede
0x038DEE  mov.l     @(0x3c,sp), er1
0x038DF4  shll.l    #2, er1
0x038DF6  shll.l    er1
0x038DF8  add.l     #0x00400e94, er1
0x038DFE  mov.l     #0x0044906c, er2
0x038E04  mov.l     er0, @(0x1c,sp)
0x038E0A  mov.l     #0x00000020, er0
0x038E10  add.l     sp, er0
0x038E12  jsr       0x018aa0
0x038E16  mov.l     er0, er1
0x038E18  mov.l     @(0x1c,sp), er0
0x038E1E  jsr       0x0188d2
0x038E22  mov.w     r0, r0
0x038E24  beq       0x038e84
0x038E26  mov.b     r6l, r0l
0x038E28  extu.w    r0
0x038E2A  extu.l    er0
0x038E2C  mov.l     er0, @(0x3c,sp)
0x038E32  shll.l    er0
0x038E34  mov.l     @(0x3c,sp), er1
0x038E3A  shll.l    #2, er1
0x038E3C  shll.l    er1
0x038E3E  mov.l     er0, @(0x2c,sp)
0x038E44  mov.l     #0x00400e94, er0
0x038E4A  add.l     er1, er0
0x038E4C  jsr       0x01876a
0x038E50  mov.w     r0, r1
0x038E52  mov.l     #0x00000024, er0
0x038E58  add.l     sp, er0
0x038E5A  jsr       0x018ede
0x038E5E  mov.l     er0, er1
0x038E60  mov.l     #0x0044906c, er2
0x038E66  mov.l     #0x0000001c, er0
0x038E6C  add.l     sp, er0
0x038E6E  jsr       0x018aa0
0x038E72  jsr       0x01876a
0x038E76  mov.l     @(0x2c,sp), er1
0x038E7C  mov.w     r0, @(0x449034,er1)
0x038E84  mov.b     r6l, r1l
0x038E86  extu.w    r1
0x038E88  extu.l    er1
0x038E8A  mov.l     er1, @(0x3c,sp)
0x038E90  mov.l     er1, @(0x2c,sp)
0x038E96  mov.l     @(0x2c,sp), er0
0x038E9C  mov.b     @(0x400db8,er0), r1l
0x038EA4  extu.w    r1
0x038EA6  mov.l     #0x00000024, er0
0x038EAC  add.l     sp, er0
0x038EAE  jsr       0x018ede
0x038EB2  mov.l     er0, er1
0x038EB4  mov.l     #0x0003f870, er2
0x038EBA  mov.l     #0x0000001c, er0
0x038EC0  add.l     sp, er0
0x038EC2  jsr       0x018aa0
0x038EC6  mov.l     er0, er1
0x038EC8  mov.l     #0x0003f878, er2
0x038ECE  mov.l     #0x00000014, er0
0x038ED4  add.l     sp, er0
0x038ED6  jsr       0x01842c
0x038EDA  mov.l     @(0x3c,sp), er1
0x038EE0  shll.l    er1
0x038EE2  mov.w     @(0x44902c,er1), r1
0x038EEA  mov.l     er0, @(0x8,sp)
0x038EF0  mov.l     #0x0000000c, er0
0x038EF6  add.l     sp, er0
0x038EF8  jsr       0x018ede
0x038EFC  mov.l     @(0x8,sp), er1
0x038F02  mov.l     er0, er2
0x038F04  mov.l     sp, er0
0x038F06  jsr       0x01842c
0x038F0A  mov.l     #0x00449044, er1
0x038F10  jsr       0x018e36
0x038F14  mov.l     @(0x3c,sp), er1
0x038F1A  shll.l    #2, er1
0x038F1C  shll.l    er1
0x038F1E  add.l     er5, er1
0x038F20  mov.l     #0x00449044, er0
0x038F26  jsr       0x0188d2
0x038F2A  mov.w     r0, r0
0x038F2C  beq       0x038f44
0x038F2E  mov.b     r6l, r0l
0x038F30  extu.w    r0
0x038F32  extu.l    er0
0x038F34  shll.l    #2, er0
0x038F36  shll.l    er0
0x038F38  add.l     er5, er0
0x038F3A  mov.l     #0x00449044, er1
0x038F40  jsr       0x018e36
0x038F44  mov.b     r6l, r0l
0x038F46  extu.w    r0
0x038F48  extu.l    er0
0x038F4A  shll.l    #2, er0
0x038F4C  mov.l     er0, @(0x3c,sp)
0x038F52  sub.l     er1, er1
0x038F54  mov.b     @0x400db4, r1l
0x038F5A  shll.l    #2, er1
0x038F5C  shll.l    #2, er1
0x038F5E  add.l     er3, er1
0x038F60  add.l     er0, er1
0x038F62  add.l     er4, er0
0x038F64  mov.l     er1, @(0x2c,sp)
0x038F6A  mov.l     @er0, er1
0x038F6E  mov.l     #0x00000024, er0
0x038F74  add.l     sp, er0
0x038F76  jsr       0x018e68
0x038F7A  mov.l     er0, er1
0x038F7C  mov.l     #0x00449044, er2
0x038F82  mov.l     #0x0000001c, er0
0x038F88  add.l     sp, er0
0x038F8A  jsr       0x018aa0
0x038F8E  jsr       0x01876a
0x038F92  mov.l     @(0x3c,sp), er1
0x038F98  mov.l     @(0x400f42,er1), er1
0x038FA2  add.l     er1, er0
0x038FA4  mov.l     @(0x2c,sp), er1
0x038FAA  mov.l     er0, @er1
0x038FAE  sub.l     er0, er0
0x038FB0  mov.b     @0x400db4, r0l
0x038FB6  shll.l    #2, er0
0x038FB8  shll.l    #2, er0
0x038FBA  add.l     er3, er0
0x038FBC  mov.l     @(0x3c,sp), er1
0x038FC2  add.l     er1, er0
0x038FC4  mov.l     @er0, er0
0x038FC8  cmp.l     #0x03ffffff, er0
0x038FCE  bls       0x038ff2
0x038FD0  sub.l     er0, er0
0x038FD2  mov.b     @0x400db4, r0l
0x038FD8  shll.l    #2, er0
0x038FDA  shll.l    #2, er0
0x038FDC  add.l     er3, er0
0x038FDE  mov.b     r6l, r1l
0x038FE0  extu.w    r1
0x038FE2  extu.l    er1
0x038FE4  shll.l    #2, er1
0x038FE6  add.l     er1, er0
0x038FE8  mov.l     #0x03ffffff, er1
0x038FEE  mov.l     er1, @er0
0x038FF2  mov.b     r6l, r0l
0x038FF4  extu.w    r0
0x038FF6  extu.l    er0
0x038FF8  shll.l    er0
0x038FFA  mov.l     er0, @(0x3c,sp)
0x039000  mov.l     @(0x3c,sp), er1
0x039006  mov.w     @(0x449024,er1), r1
0x03900E  mov.l     er0, @(0x24,sp)
0x039014  mov.l     #0x00000028, er0
0x03901A  add.l     sp, er0
0x03901C  jsr       0x018ede
0x039020  mov.l     er0, er1
0x039022  mov.l     #0x00449044, er2
0x039028  mov.l     #0x0000001c, er0
0x03902E  add.l     sp, er0
0x039030  jsr       0x018aa0
0x039034  jsr       0x01876a
0x039038  mov.l     @(0x24,sp), er1
0x03903E  mov.w     r0, @(0x400e5c,er1)
0x039046  mov.b     @0x400eb4, r0l
0x03904C  cmp.b     #0x01, r0l
0x03904E  bne       0x0390a2
0x039050  sub.l     er0, er0
0x039052  mov.b     r6l, r0l
0x039054  shll.l    er0
0x039056  mov.l     er0, @(0x3c,sp)
0x03905C  mov.l     @(0x3c,sp), er1
0x039062  mov.w     @(0x449034,er1), r1
0x03906A  mov.l     er0, @(0x24,sp)
0x039070  mov.l     #0x00000028, er0
0x039076  add.l     sp, er0
0x039078  jsr       0x018ede
0x03907C  mov.l     er0, er1
0x03907E  mov.l     #0x00449044, er2
0x039084  mov.l     #0x0000001c, er0
0x03908A  add.l     sp, er0
0x03908C  jsr       0x018aa0
0x039090  jsr       0x01876a
0x039094  mov.l     @(0x24,sp), er1
0x03909A  mov.w     r0, @(0x400e64,er1)
0x0390A2  inc.b     #1, r6h
0x0390A4  mov.b     @0x44903f, r0l
0x0390AA  cmp.b     r0l, r6h
0x0390AC  bcs       0x038c8a
0x0390B0  sub.b     r6l, r6l
0x0390B2  mov.b     r6l, r0l
0x0390B4  extu.w    r0
0x0390B6  extu.l    er0
0x0390B8  shll.l    er0
0x0390BA  mov.w     @(0x400e5c,er0), r0
0x0390C2  cmp.w     #0x3fff, r0
0x0390C6  bls       0x0390dc
0x0390C8  mov.b     r6l, r0l
0x0390CA  extu.w    r0
0x0390CC  extu.l    er0
0x0390CE  shll.l    er0
0x0390D0  mov.w     #0x3fff, r1
0x0390D4  mov.w     r1, @(0x400e5c,er0)
0x0390DC  inc.b     #1, r6l
0x0390DE  cmp.b     #0x04, r6l
0x0390E0  bcs       0x0390b2
0x0390E2  add.l     #0x00000040, sp
0x0390E8  ldm.l     @sp+, er4-er6
0x0390EC  ldm.l     @sp+, er2-er3
0x0390F0  rts       
