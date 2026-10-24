0x02ED8A  mov.l     er6, @-sp
0x02ED8E  mov.l     sp, er6
0x02ED90  mov.w     r5, @-sp
0x02ED92  sub.l     #0x00000014, sp
0x02ED98  mov.b     r0l, r5l
0x02ED9A  mov.b     r0h, r5h
0x02ED9C  mov.l     #0xffffffea, er1
0x02EDA2  add.l     er6, er1
0x02EDA4  mov.b     r5h, r0h
0x02EDA6  mov.b     r5l, r0l
0x02EDA8  bsr       0x02ff32
0x02EDAC  mov.l     @(0xffea,er6), er0
0x02EDB2  mov.l     @(0x2,er0), er0
0x02EDB8  mov.l     er0, @(0xfff8,er6)
0x02EDBE  bt        0x02edd0
0x02EDC0  mov.b     @0x200002, r0l
0x02EDC6  extu.w    r0
0x02EDC8  and.w     #0x0028, r0
0x02EDCC  bne       0x02edd0
0x02EDCE  bt        0x02edd2
0x02EDD0  bt        0x02edc0
0x02EDD2  jsr       0x02d694
0x02EDD6  mov.l     @(0xffea,er6), er0
0x02EDDC  mov.b     @(0x14,er0), r0l
0x02EDE0  mov.b     r0l, @0x200150
0x02EDE6  bt        0x02ee32
0x02EDE8  mov.l     @(0xfff8,er6), er0
0x02EDEE  mov.w     @er0, r0
0x02EDF0  cmp.w     #0xffff, r0
0x02EDF4  bne       0x02edf8
0x02EDF6  bt        0x02ee34
0x02EDF8  mov.l     @(0xfff8,er6), er0
0x02EDFE  inc.l     #2, er0
0x02EE00  mov.l     er0, @(0xfff8,er6)
0x02EE06  dec.l     #2, er0
0x02EE08  mov.w     @er0, r0
0x02EE0A  extu.l    er0
0x02EE0C  add.l     #0x00200000, er0
0x02EE12  mov.l     er0, @(0xfff4,er6)
0x02EE18  mov.l     @(0xfff8,er6), er0
0x02EE1E  inc.l     #2, er0
0x02EE20  mov.l     er0, @(0xfff8,er6)
0x02EE26  dec.l     #2, er0
0x02EE28  mov.l     @(0xfff4,er6), er1
0x02EE2E  mov.w     @er0, r0
0x02EE30  mov.w     r0, @er1
0x02EE32  bt        0x02ede8
0x02EE34  jsr       0x02d694
0x02EE38  mov.l     @0x4003f6, er0
0x02EE40  mov.l     er0, @(0xffee,er6)
0x02EE46  bt        0x02ee48
0x02EE48  mov.l     @0x4003f6, er0
0x02EE50  mov.l     @(0xffee,er6), er1
0x02EE56  sub.l     er1, er0
0x02EE58  cmp.l     #0x0000000b, er0
0x02EE5E  bcs       0x02ee48
0x02EE60  add.l     #0x00000014, sp
0x02EE66  mov.w     @sp+, r5
0x02EE68  mov.l     @sp+, er6
0x02EE6C  rts       
