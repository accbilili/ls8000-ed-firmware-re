0x037E68  stm.l     er2-er3, @-sp
0x037E6C  stm.l     er4-er6, @-sp
0x037E70  sub.l     #0x00000042, sp
0x037E76  mov.l     #0x0044902c, er3
0x037E7C  mov.l     #0x00400daa, er4
0x037E82  mov.l     #0x00400e0c, er5
0x037E88  mov.b     #0x01, r6h
0x037E8A  mov.b     @er4, r0l
0x037E8C  mov.b     r0l, @0x44903f
0x037E92  sub.b     r0l, r0l
0x037E94  mov.b     r0l, @er4
0x037E96  mov.b     r0l, @0x400ec4
0x037E9C  mov.b     @0x400d7a, r0l
0x037EA2  cmp.b     #0x40, r0l
0x037EA4  beq       0x037ecc
0x037EA6  cmp.b     #0x04, r0l
0x037EA8  bne       0x037eb4
0x037EAA  mov.b     @0x400db4, r1l
0x037EB0  cmp.b     #0x01, r1l
0x037EB2  beq       0x037ecc
0x037EB4  mov.b     @0x400d7a, r0l
0x037EBA  cmp.b     #0x08, r0l
0x037EBC  bne       0x038260
0x037EC0  mov.b     @0x400db4, r1l
0x037EC6  cmp.b     #0x01, r1l
0x037EC8  bne       0x038260
0x037ECC  mov.w     @0x44903c, r0
0x037ED2  cmp.w     #0x1fff, r0
0x037ED6  bhi       0x038168
0x037EDA  mov.w     @0x44903c, r1
0x037EE0  inc.w     #1, r1
0x037EE2  mov.l     #0x00000020, er0
0x037EE8  add.l     sp, er0
0x037EEA  jsr       0x018ede
0x037EEE  mov.l     #0x0003f850, er1
0x037EF4  mov.l     er0, er2
0x037EF6  mov.l     #0x00000028, er0
0x037EFC  add.l     sp, er0
0x037EFE  jsr       0x01842c
0x037F02  mov.b     @er4, r0l
0x037F04  inc.b     #1, r0l
0x037F06  mov.b     r0l, @er4
0x037F08  dec.b     #1, r0l
0x037F0A  extu.w    r0
0x037F0C  extu.l    er0
0x037F0E  mov.b     @0x44903e, r1l
0x037F14  mov.b     r1l, @(0x400dab,er0)
0x037F1C  sub.b     r6h, r6h
0x037F1E  jmp       0x03808c
0x037F22  mov.b     r6h, r0l
0x037F24  extu.w    r0
0x037F26  extu.l    er0
0x037F28  mov.b     @(0x449040,er0), r6l
0x037F30  cmp.b     #0x03, r6l
0x037F32  beq       0x03808a
0x037F36  mov.b     r6l, r1l
0x037F38  extu.w    r1
0x037F3A  extu.l    er1
0x037F3C  shll.l    #2, er1
0x037F3E  mov.l     er1, @(0x3c,sp)
0x037F44  add.l     er5, er1
0x037F46  mov.l     @er1, er1
0x037F4A  mov.l     #0x00000020, er0
0x037F50  add.l     sp, er0
0x037F52  jsr       0x018e68
0x037F56  mov.l     er0, er1
0x037F58  mov.l     #0x00000028, er2
0x037F5E  add.l     sp, er2
0x037F60  mov.l     #0x00000018, er0
0x037F66  add.l     sp, er0
0x037F68  jsr       0x018aa0
0x037F6C  jsr       0x01876a
0x037F70  mov.l     @(0x3c,sp), er1
0x037F76  mov.l     @(0x3c,sp), er2
0x037F7C  mov.l     @(0x400f32,er2), er2
0x037F86  mov.l     @(0x400f42,er1), er1
0x037F90  add.l     er1, er2
0x037F92  shll.l    #2, er2
0x037F94  shll.l    #2, er2
0x037F96  shll.l    #2, er2
0x037F98  cmp.l     er2, er0
0x037F9A  bls       0x03808a
0x037F9E  mov.b     r6l, r1l
0x037FA0  extu.w    r1
0x037FA2  extu.l    er1
0x037FA4  shll.l    #2, er1
0x037FA6  mov.l     er1, @(0x3c,sp)
0x037FAC  mov.l     @(0x3c,sp), er0
0x037FB2  mov.l     @(0x400f32,er1), er1
0x037FBC  mov.l     @(0x400f42,er0), er0
0x037FC6  add.l     er0, er1
0x037FC8  shll.l    #2, er1
0x037FCA  shll.l    #2, er1
0x037FCC  shll.l    #2, er1
0x037FCE  mov.l     #0x00000020, er0
0x037FD4  add.l     sp, er0
0x037FD6  jsr       0x018958
0x037FDA  mov.l     @(0x3c,sp), er1
0x037FE0  add.l     er5, er1
0x037FE2  mov.l     @er1, er1
0x037FE6  mov.l     er0, @(0x14,sp)
0x037FEC  mov.l     #0x00000018, er0
0x037FF2  add.l     sp, er0
0x037FF4  jsr       0x018e68
0x037FF8  mov.l     @(0x14,sp), er1
0x037FFE  mov.l     er0, er2
0x038000  mov.l     #0x0000000c, er0
0x038006  add.l     sp, er0
0x038008  jsr       0x01842c
0x03800C  mov.l     er0, er1
0x03800E  mov.l     #0x00000028, er0
0x038014  add.l     sp, er0
0x038016  jsr       0x0188d2
0x03801A  mov.w     r0, r0
0x03801C  beq       0x03808a
0x03801E  sub.l     er1, er1
0x038020  mov.b     r6l, r1l
0x038022  shll.l    #2, er1
0x038024  mov.l     er1, @(0x3c,sp)
0x03802A  mov.l     @(0x3c,sp), er0
0x038030  mov.l     @(0x400f32,er1), er1
0x03803A  mov.l     @(0x400f42,er0), er0
0x038044  add.l     er0, er1
0x038046  shll.l    #2, er1
0x038048  shll.l    #2, er1
0x03804A  shll.l    #2, er1
0x03804C  mov.l     #0x00000020, er0
0x038052  add.l     sp, er0
0x038054  jsr       0x018958
0x038058  mov.l     @(0x3c,sp), er1
0x03805E  add.l     er5, er1
0x038060  mov.l     @er1, er1
0x038064  mov.l     er0, @(0x14,sp)
0x03806A  mov.l     #0x00000018, er0
0x038070  add.l     sp, er0
0x038072  jsr       0x018e68
0x038076  mov.l     @(0x14,sp), er1
0x03807C  mov.l     er0, er2
0x03807E  mov.l     #0x00000028, er0
0x038084  add.l     sp, er0
0x038086  jsr       0x01842c
0x03808A  inc.b     #1, r6h
0x03808C  mov.b     @0x44903f, r0l
0x038092  cmp.b     r0l, r6h
0x038094  bcs       0x037f22
0x038098  sub.b     r6l, r6l
0x03809A  jmp       0x038156
0x03809E  extu.w    r6
0x0380A0  extu.l    er6
0x0380A2  mov.b     @(0x449040,er6), r6h
0x0380AA  cmp.b     #0x03, r6h
0x0380AC  beq       0x038154
0x0380B0  sub.l     er0, er0
0x0380B2  mov.b     r6h, r0l
0x0380B4  mov.l     er0, @(0x38,sp)
0x0380BA  shll.l    #2, er0
0x0380BC  add.l     er5, er0
0x0380BE  mov.l     er0, @(0x3c,sp)
0x0380C4  mov.l     @(0x3c,sp), er1
0x0380CA  mov.l     @er1, er1
0x0380CE  mov.l     er0, @(0x1c,sp)
0x0380D4  mov.l     #0x00000020, er0
0x0380DA  add.l     sp, er0
0x0380DC  jsr       0x018e68
0x0380E0  mov.l     er0, er1
0x0380E2  mov.l     #0x00000028, er2
0x0380E8  add.l     sp, er2
0x0380EA  mov.l     #0x00000014, er0
0x0380F0  add.l     sp, er0
0x0380F2  jsr       0x018aa0
0x0380F6  jsr       0x01876a
0x0380FA  mov.l     @(0x1c,sp), er1
0x038100  mov.l     er0, @er1
0x038104  mov.l     @(0x38,sp), er0
0x03810A  shll.l    er0
0x03810C  add.l     #0x00449024, er0
0x038112  mov.l     er0, @(0x3c,sp)
0x038118  mov.l     @(0x3c,sp), er1
0x03811E  mov.w     @er1, r1
0x038120  mov.l     er0, @(0x1c,sp)
0x038126  mov.l     #0x00000020, er0
0x03812C  add.l     sp, er0
0x03812E  jsr       0x018ede
0x038132  mov.l     er0, er1
0x038134  mov.l     #0x00000028, er2
0x03813A  add.l     sp, er2
0x03813C  mov.l     #0x00000014, er0
0x038142  add.l     sp, er0
0x038144  jsr       0x018aa0
0x038148  jsr       0x01876a
0x03814C  mov.l     @(0x1c,sp), er1
0x038152  mov.w     r0, @er1
0x038154  inc.b     #1, r6l
0x038156  mov.b     @0x44903f, r0l
0x03815C  cmp.b     r0l, r6l
0x03815E  bcs       0x03809e
0x038162  sub.b     r6h, r6h
0x038164  jmp       0x038762
0x038168  sub.b     r0l, r0l
0x03816A  bt        0x0381ac
0x03816C  sub.l     er0, er0
0x03816E  mov.b     @(0x41,sp), r0l
0x038172  mov.b     @(0x449040,er0), r6l
0x03817A  cmp.b     #0x03, r6l
0x03817C  beq       0x0381a6
0x03817E  mov.b     r6l, r0l
0x038180  extu.w    r0
0x038182  extu.l    er0
0x038184  shll.l    er0
0x038186  add.l     er3, er0
0x038188  mov.w     @er0, r0
0x03818A  cmp.w     #0x3fff, r0
0x03818E  bne       0x0381a6
0x038190  mov.b     @er4, r0l
0x038192  inc.b     #1, r0l
0x038194  mov.b     r0l, @er4
0x038196  dec.b     #1, r0l
0x038198  extu.w    r0
0x03819A  extu.l    er0
0x03819C  mov.b     r6l, @(0x400dab,er0)
0x0381A4  sub.b     r6h, r6h
0x0381A6  mov.b     @(0x41,sp), r0l
0x0381AA  inc.b     #1, r0l
0x0381AC  mov.b     r0l, @(0x41,sp)
0x0381B0  mov.b     @0x44903f, r1l
0x0381B6  cmp.b     r1l, r0l
0x0381B8  bcs       0x03816c
0x0381BA  mov.b     r6h, r6h
0x0381BC  bne       0x038762
0x0381C0  sub.b     r6l, r6l
0x0381C2  jmp       0x038250
0x0381C6  mov.b     r6l, r0l
0x0381C8  extu.w    r0
0x0381CA  extu.l    er0
0x0381CC  mov.b     @(0x449040,er0), r0l
0x0381D4  cmp.b     #0x03, r0l
0x0381D6  beq       0x03824e
0x0381D8  extu.w    r0
0x0381DA  extu.l    er0
0x0381DC  mov.l     er0, @(0x3c,sp)
0x0381E2  shll.l    #2, er0
0x0381E4  mov.l     er0, @(0x38,sp)
0x0381EA  add.l     er5, er0
0x0381EC  mov.l     @(0x38,sp), er1
0x0381F2  mov.l     @(0x400f32,er1), er1
0x0381FC  mov.l     er1, @er0
0x038200  mov.l     @(0x3c,sp), er0
0x038206  shll.l    er0
0x038208  add.l     #0x00449024, er0
0x03820E  mov.l     er0, @(0x38,sp)
0x038214  mov.l     @(0x38,sp), er1
0x03821A  mov.w     @er1, r1
0x03821C  mov.l     er0, @(0x1c,sp)
0x038222  mov.l     #0x00000020, er0
0x038228  add.l     sp, er0
0x03822A  jsr       0x018ede
0x03822E  mov.l     er0, er1
0x038230  mov.l     #0x0003f858, er2
0x038236  mov.l     #0x00000014, er0
0x03823C  add.l     sp, er0
0x03823E  jsr       0x018aa0
0x038242  jsr       0x01876a
0x038246  mov.l     @(0x1c,sp), er1
0x03824C  mov.w     r0, @er1
0x03824E  inc.b     #1, r6l
0x038250  mov.b     @0x44903f, r0l
0x038256  cmp.b     r0l, r6l
0x038258  bcs       0x0381c6
0x03825C  jmp       0x038762
0x038260  mov.b     @0x400d7a, r0l
0x038266  cmp.b     #0x20, r0l
0x038268  beq       0x03828c
0x03826A  cmp.b     #0x04, r0l
0x03826C  bne       0x038276
0x03826E  mov.b     @0x400db4, r1l
0x038274  beq       0x03828c
0x038276  mov.b     @0x400d7a, r0l
0x03827C  cmp.b     #0x08, r0l
0x03827E  bne       0x038762
0x038282  mov.b     @0x400db4, r1l
0x038288  bne       0x038762
0x03828C  mov.w     #0x31b0, r0
0x038290  mov.w     r0, @(0x30,sp)
0x038294  mov.w     #0x1450, r0
0x038298  mov.w     r0, @(0x32,sp)
0x03829C  mov.w     #0x1210, r0
0x0382A0  mov.w     r0, @(0x34,sp)
0x0382A4  sub.b     r0l, r0l
0x0382A6  mov.b     r0l, @0x400ec4
0x0382AC  sub.b     r0l, r0l
0x0382AE  jmp       0x0383dc
0x0382B2  sub.l     er0, er0
0x0382B4  mov.b     @(0x41,sp), r0l
0x0382B8  mov.b     @(0x449040,er0), r6l
0x0382C0  cmp.b     #0x03, r6l
0x0382C2  beq       0x0383d6
0x0382C6  mov.b     r6l, r1l
0x0382C8  extu.w    r1
0x0382CA  extu.l    er1
0x0382CC  mov.l     er1, @(0x3c,sp)
0x0382D2  shll.l    #2, er1
0x0382D4  mov.l     er1, @(0x38,sp)
0x0382DA  add.l     er5, er1
0x0382DC  mov.l     @er1, er1
0x0382E0  mov.l     #0x00000020, er0
0x0382E6  add.l     sp, er0
0x0382E8  jsr       0x018e68
0x0382EC  mov.l     @(0x38,sp), er1
0x0382F2  mov.l     @(0x400f32,er1), er1
0x0382FC  mov.l     er0, @(0x14,sp)
0x038302  mov.l     #0x00000018, er0
0x038308  add.l     sp, er0
0x03830A  jsr       0x018e68
0x03830E  mov.l     @(0x14,sp), er1
0x038314  mov.l     er0, er2
0x038316  mov.l     #0x0044906c, er0
0x03831C  jsr       0x01842c
0x038320  mov.l     @(0x3c,sp), er1
0x038326  shll.l    er1
0x038328  add.l     er3, er1
0x03832A  mov.w     @er1, r1
0x03832C  mov.l     #0x00000020, er0
0x038332  add.l     sp, er0
0x038334  jsr       0x018ede
0x038338  mov.l     @(0x3c,sp), er1
0x03833E  shll.l    #2, er1
0x038340  shll.l    er1
0x038342  add.l     #0x00400e74, er1
0x038348  mov.l     #0x0044906c, er2
0x03834E  mov.l     er0, @(0x14,sp)
0x038354  mov.l     #0x00000018, er0
0x03835A  add.l     sp, er0
0x03835C  jsr       0x018aa0
0x038360  mov.l     er0, er1
0x038362  mov.l     @(0x14,sp), er0
0x038368  jsr       0x018938
0x03836C  mov.w     r0, r0
0x03836E  beq       0x0383d6
0x038370  sub.l     er1, er1
0x038372  mov.b     r6l, r1l
0x038374  shll.l    er1
0x038376  mov.l     er1, @(0x3c,sp)
0x03837C  add.l     er3, er1
0x03837E  mov.w     @er1, r1
0x038380  mov.l     #0x00000020, er0
0x038386  add.l     sp, er0
0x038388  jsr       0x018ede
0x03838C  mov.l     @(0x3c,sp), er1
0x038392  mov.w     @(0x449034,er1), r1
0x03839A  mov.l     er0, @(0x14,sp)
0x0383A0  mov.l     #0x00000018, er0
0x0383A6  add.l     sp, er0
0x0383A8  jsr       0x018ede
0x0383AC  mov.l     @(0x14,sp), er1
0x0383B2  mov.l     er0, er2
0x0383B4  mov.l     #0x0000000c, er0
0x0383BA  add.l     sp, er0
0x0383BC  jsr       0x01842c
0x0383C0  mov.l     #0x0003f860, er1
0x0383C6  jsr       0x018938
0x0383CA  mov.w     r0, r0
0x0383CC  beq       0x0383d6
0x0383CE  mov.b     #0x01, r0l
0x0383D0  mov.b     r0l, @0x400ec4
0x0383D6  mov.b     @(0x41,sp), r0l
0x0383DA  inc.b     #1, r0l
0x0383DC  mov.b     r0l, @(0x41,sp)
0x0383E0  mov.b     @0x44903f, r1l
0x0383E6  cmp.b     r1l, r0l
0x0383E8  bcs       0x0382b2
0x0383EC  sub.b     r0l, r0l
0x0383EE  jmp       0x038752
0x0383F2  sub.l     er0, er0
0x0383F4  mov.b     @(0x41,sp), r0l
0x0383F8  mov.b     @(0x449040,er0), r6l
0x038400  cmp.b     #0x03, r6l
0x038402  beq       0x038690
0x038406  mov.b     r6l, r0l
0x038408  extu.w    r0
0x03840A  extu.l    er0
0x03840C  shll.l    er0
0x03840E  add.l     er3, er0
0x038410  mov.w     @er0, r0
0x038412  cmp.w     #0x1fff, r0
0x038416  bhi       0x038690
0x03841A  mov.b     r6l, r1l
0x03841C  extu.w    r1
0x03841E  extu.l    er1
0x038420  shll.l    #2, er1
0x038422  mov.l     er1, @(0x3c,sp)
0x038428  add.l     er5, er1
0x03842A  mov.l     @er1, er1
0x03842E  mov.l     #0x00000020, er0
0x038434  add.l     sp, er0
0x038436  jsr       0x018e68
0x03843A  mov.l     @(0x3c,sp), er1
0x038440  mov.l     @(0x400f32,er1), er1
0x03844A  mov.l     er0, @(0x14,sp)
0x038450  mov.l     #0x00000018, er0
0x038456  add.l     sp, er0
0x038458  jsr       0x018e68
0x03845C  mov.l     @(0x14,sp), er1
0x038462  mov.l     er0, er2
0x038464  mov.l     #0x0044906c, er0
0x03846A  jsr       0x01842c
0x03846E  mov.b     @0x400d7a, r0l
0x038474  cmp.b     #0x08, r0l
0x038476  bne       0x0385f8
0x03847A  mov.b     @0x400db4, r0l
0x038480  bne       0x0385f8
0x038484  mov.b     r6l, r1l
0x038486  extu.w    r1
0x038488  extu.l    er1
0x03848A  mov.l     er1, @(0x3c,sp)
0x038490  shll.l    er1
0x038492  add.l     er3, er1
0x038494  mov.w     @er1, r1
0x038496  mov.l     #0x00000020, er0
0x03849C  add.l     sp, er0
0x03849E  jsr       0x018ede
0x0384A2  mov.l     @(0x3c,sp), er1
0x0384A8  shll.l    #2, er1
0x0384AA  shll.l    er1
0x0384AC  add.l     #0x00400e74, er1
0x0384B2  mov.l     #0x0044906c, er2
0x0384B8  mov.l     er0, @(0x14,sp)
0x0384BE  mov.l     #0x00000018, er0
0x0384C4  add.l     sp, er0
0x0384C6  jsr       0x018aa0
0x0384CA  mov.l     er0, er1
0x0384CC  mov.l     @(0x14,sp), er0
0x0384D2  jsr       0x018938
0x0384D6  mov.w     r0, r0
0x0384D8  beq       0x038534
0x0384DA  mov.b     r6l, r0l
0x0384DC  extu.w    r0
0x0384DE  extu.l    er0
0x0384E0  mov.l     er0, @(0x3c,sp)
0x0384E6  shll.l    er0
0x0384E8  add.l     er3, er0
0x0384EA  mov.l     @(0x3c,sp), er1
0x0384F0  shll.l    #2, er1
0x0384F2  shll.l    er1
0x0384F4  mov.l     er0, @(0x24,sp)
0x0384FA  mov.l     #0x00400e74, er0
0x038500  add.l     er1, er0
0x038502  jsr       0x01876a
0x038506  mov.w     r0, r1
0x038508  mov.l     #0x0000001c, er0
0x03850E  add.l     sp, er0
0x038510  jsr       0x018ede
0x038514  mov.l     er0, er1
0x038516  mov.l     #0x0044906c, er2
0x03851C  mov.l     #0x00000014, er0
0x038522  add.l     sp, er0
0x038524  jsr       0x018aa0
0x038528  jsr       0x01876a
0x03852C  mov.l     @(0x24,sp), er1
0x038532  mov.w     r0, @er1
0x038534  mov.b     @0x400ec4, r0l
0x03853A  cmp.b     #0x01, r0l
0x03853C  beq       0x0385f8
0x038540  mov.b     r6l, r1l
0x038542  extu.w    r1
0x038544  extu.l    er1
0x038546  mov.l     er1, @(0x3c,sp)
0x03854C  shll.l    er1
0x03854E  mov.w     @(0x449034,er1), r1
0x038556  mov.l     #0x00000020, er0
0x03855C  add.l     sp, er0
0x03855E  jsr       0x018ede
0x038562  mov.l     @(0x3c,sp), er1
0x038568  shll.l    #2, er1
0x03856A  shll.l    er1
0x03856C  add.l     #0x00400e94, er1
0x038572  mov.l     #0x0044906c, er2
0x038578  mov.l     er0, @(0x14,sp)
0x03857E  mov.l     #0x00000018, er0
0x038584  add.l     sp, er0
0x038586  jsr       0x018aa0
0x03858A  mov.l     er0, er1
0x03858C  mov.l     @(0x14,sp), er0
0x038592  jsr       0x0188d2
0x038596  mov.w     r0, r0
0x038598  beq       0x0385f8
0x03859A  mov.b     r6l, r0l
0x03859C  extu.w    r0
0x03859E  extu.l    er0
0x0385A0  mov.l     er0, @(0x3c,sp)
0x0385A6  shll.l    er0
0x0385A8  mov.l     @(0x3c,sp), er1
0x0385AE  shll.l    #2, er1
0x0385B0  shll.l    er1
0x0385B2  mov.l     er0, @(0x24,sp)
0x0385B8  mov.l     #0x00400e94, er0
0x0385BE  add.l     er1, er0
0x0385C0  jsr       0x01876a
0x0385C4  mov.w     r0, r1
0x0385C6  mov.l     #0x0000001c, er0
0x0385CC  add.l     sp, er0
0x0385CE  jsr       0x018ede
0x0385D2  mov.l     er0, er1
0x0385D4  mov.l     #0x0044906c, er2
0x0385DA  mov.l     #0x00000014, er0
0x0385E0  add.l     sp, er0
0x0385E2  jsr       0x018aa0
0x0385E6  jsr       0x01876a
0x0385EA  mov.l     @(0x24,sp), er1
0x0385F0  mov.w     r0, @(0x449034,er1)
0x0385F8  mov.b     @er4, r0l
0x0385FA  inc.b     #1, r0l
0x0385FC  mov.b     r0l, @er4
0x0385FE  dec.b     #1, r0l
0x038600  extu.w    r0
0x038602  extu.l    er0
0x038604  mov.b     r6l, @(0x400dab,er0)
0x03860C  mov.b     r6l, r0l
0x03860E  extu.w    r0
0x038610  extu.l    er0
0x038612  mov.l     er0, @(0x3c,sp)
0x038618  shll.l    #2, er0
0x03861A  add.l     er5, er0
0x03861C  mov.l     er0, @(0x38,sp)
0x038622  mov.l     @(0x3c,sp), er1
0x038628  shll.l    er1
0x03862A  add.l     er3, er1
0x03862C  mov.w     @er1, r1
0x03862E  inc.w     #1, r1
0x038630  mov.l     er0, @(0x1c,sp)
0x038636  mov.l     #0x00000020, er0
0x03863C  add.l     sp, er0
0x03863E  jsr       0x018ede
0x038642  mov.l     #0x0003f850, er1
0x038648  mov.l     er0, er2
0x03864A  mov.l     #0x00000014, er0
0x038650  add.l     sp, er0
0x038652  jsr       0x01842c
0x038656  mov.l     @(0x38,sp), er1
0x03865C  mov.l     @er1, er1
0x038660  mov.l     er0, @(0x8,sp)
0x038666  mov.l     #0x0000000c, er0
0x03866C  add.l     sp, er0
0x03866E  jsr       0x018e68
0x038672  mov.l     @(0x8,sp), er1
0x038678  mov.l     er0, er2
0x03867A  mov.l     sp, er0
0x03867C  jsr       0x018aa0
0x038680  jsr       0x01876a
0x038684  mov.l     @(0x1c,sp), er1
0x03868A  mov.l     er0, @er1
0x03868E  sub.b     r6h, r6h
0x038690  cmp.b     #0x03, r6l
0x038692  beq       0x03874c
0x038696  mov.b     r6l, r0l
0x038698  extu.w    r0
0x03869A  extu.l    er0
0x03869C  shll.l    er0
0x03869E  add.l     er3, er0
0x0386A0  mov.w     @er0, r0
0x0386A2  cmp.w     #0x3fff, r0
0x0386A6  bne       0x03874c
0x0386AA  mov.b     @er4, r0l
0x0386AC  inc.b     #1, r0l
0x0386AE  mov.b     r0l, @er4
0x0386B0  dec.b     #1, r0l
0x0386B2  extu.w    r0
0x0386B4  extu.l    er0
0x0386B6  mov.b     r6l, @(0x400dab,er0)
0x0386BE  sub.l     er0, er0
0x0386C0  mov.b     r6l, r0l
0x0386C2  mov.l     er0, @(0x38,sp)
0x0386C8  shll.l    #2, er0
0x0386CA  mov.l     er0, @(0x3c,sp)
0x0386D0  add.l     er5, er0
0x0386D2  mov.l     @(0x38,sp), er1
0x0386D8  shll.l    er1
0x0386DA  mov.l     #0x00000030, er2
0x0386E0  add.l     sp, er2
0x0386E2  add.l     er1, er2
0x0386E4  mov.w     @er2, r1
0x0386E6  mov.l     er0, @(0x1c,sp)
0x0386EC  mov.l     #0x00000020, er0
0x0386F2  add.l     sp, er0
0x0386F4  jsr       0x018ede
0x0386F8  mov.l     #0x0003f850, er1
0x0386FE  mov.l     er0, er2
0x038700  mov.l     #0x00000014, er0
0x038706  add.l     sp, er0
0x038708  jsr       0x01842c
0x03870C  mov.l     @(0x3c,sp), er1
0x038712  mov.l     @(0x400f32,er1), er1
0x03871C  mov.l     er0, @(0x8,sp)
0x038722  mov.l     #0x0000000c, er0
0x038728  add.l     sp, er0
0x03872A  jsr       0x018e68
0x03872E  mov.l     @(0x8,sp), er1
0x038734  mov.l     er0, er2
0x038736  mov.l     sp, er0
0x038738  jsr       0x018aa0
0x03873C  jsr       0x01876a
0x038740  mov.l     @(0x1c,sp), er1
0x038746  mov.l     er0, @er1
0x03874A  sub.b     r6h, r6h
0x03874C  mov.b     @(0x41,sp), r0l
0x038750  inc.b     #1, r0l
0x038752  mov.b     r0l, @(0x41,sp)
0x038756  mov.b     @0x44903f, r1l
0x03875C  cmp.b     r1l, r0l
0x03875E  bcs       0x0383f2
0x038762  mov.l     er5, er0
0x038764  jsr       0x0322c6
0x038768  mov.b     r6h, r0l
0x03876A  add.l     #0x00000042, sp
0x038770  ldm.l     @sp+, er4-er6
0x038774  ldm.l     @sp+, er2-er3
0x038778  rts       
