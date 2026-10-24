0x032D2C  stm.l     er2-er3, @-sp
0x032D30  stm.l     er4-er6, @-sp
0x032D34  sub.l     #0x00000014, sp
0x032D3A  mov.l     #0x00420265, er5
0x032D40  mov.l     #0x00420248, er6
0x032D46  mov.l     #0x00400f32, er3
0x032D4C  mov.l     #0x00420108, er4
0x032D52  mov.w     @0x400406, r0
0x032D58  and.w     #0x00ff, r0
0x032D5C  mov.b     r0h, r0h
0x032D5E  bne       0x032eb2
0x032D62  cmp.b     #0x10, r0l
0x032D64  beq       0x032e68
0x032D68  cmp.b     #0x11, r0l
0x032D6A  beq       0x032e68
0x032D6E  cmp.b     #0x12, r0l
0x032D70  beq       0x032dde
0x032D72  cmp.b     #0x13, r0l
0x032D74  beq       0x032dde
0x032D76  cmp.b     #0x14, r0l
0x032D78  beq       0x032dde
0x032D7A  cmp.b     #0x15, r0l
0x032D7C  beq       0x032dde
0x032D7E  cmp.b     #0x80, r0l
0x032D80  beq       0x032d8c
0x032D82  cmp.b     #0xb0, r0l
0x032D84  beq       0x032e7a
0x032D88  jmp       0x032eb2
0x032D8C  sub.l     er0, er0
0x032D8E  mov.b     @er5, r0l
0x032D90  shll.l    #2, er0
0x032D92  add.l     er3, er0
0x032D94  mov.l     @er0, er1
0x032D98  bne       0x032da4
0x032D9A  mov.l     #0x00000800, er0
0x032DA0  jmp       0x032ed2
0x032DA4  sub.l     er1, er1
0x032DA6  mov.b     @er5, r1l
0x032DA8  mov.l     er1, @(0x10,sp)
0x032DAE  shll.l    #2, er1
0x032DB0  add.l     er3, er1
0x032DB2  mov.l     @er1, er1
0x032DB6  mov.l     #0x00000008, er0
0x032DBC  add.l     sp, er0
0x032DBE  jsr       0x018e68
0x032DC2  mov.l     @(0x10,sp), er2
0x032DC8  shll.l    #2, er2
0x032DCA  shll.l    er2
0x032DCC  add.l     er4, er2
0x032DCE  mov.l     er0, er1
0x032DD0  mov.l     sp, er0
0x032DD2  jsr       0x018aa0
0x032DD6  jsr       0x01876a
0x032DDA  jmp       0x032ed2
0x032DDE  sub.l     er0, er0
0x032DE0  mov.b     @er5, r0l
0x032DE2  shll.l    #2, er0
0x032DE4  mov.l     @(0x400e0c,er0), er1
0x032DEE  beq       0x032e12
0x032DF0  sub.l     er3, er3
0x032DF2  mov.b     @er5, r3l
0x032DF4  mov.l     er3, er1
0x032DF6  shll.l    #2, er1
0x032DF8  mov.l     @(0x400e0c,er1), er1
0x032E02  mov.l     #0x00000008, er0
0x032E08  add.l     sp, er0
0x032E0A  jsr       0x018e68
0x032E0E  mov.l     er3, er2
0x032E10  bt        0x032e36
0x032E12  sub.l     er1, er1
0x032E14  mov.b     @er5, r1l
0x032E16  mov.l     er1, @(0x10,sp)
0x032E1C  shll.l    #2, er1
0x032E1E  add.l     er3, er1
0x032E20  mov.l     @er1, er1
0x032E24  mov.l     #0x00000008, er0
0x032E2A  add.l     sp, er0
0x032E2C  jsr       0x018e68
0x032E30  mov.l     @(0x10,sp), er2
0x032E36  shll.l    #2, er2
0x032E38  shll.l    er2
0x032E3A  add.l     er4, er2
0x032E3C  mov.l     er0, er1
0x032E3E  mov.l     sp, er0
0x032E40  jsr       0x018aa0
0x032E44  jsr       0x01876a
0x032E48  mov.l     er0, @er6
0x032E4C  sub.l     er0, er0
0x032E4E  mov.b     @er5, r0l
0x032E50  shll.l    #2, er0
0x032E52  mov.l     @er6, er1
0x032E56  mov.l     @(0x400f42,er0), er0
0x032E60  add.l     er0, er1
0x032E62  mov.l     er1, @er6
0x032E66  bt        0x032ed6
0x032E68  sub.l     er0, er0
0x032E6A  mov.b     @er5, r0l
0x032E6C  shll.l    #2, er0
0x032E6E  mov.l     @(0x400d8e,er0), er0
0x032E78  bt        0x032ed2
0x032E7A  sub.l     er1, er1
0x032E7C  mov.b     @er5, r1l
0x032E7E  mov.l     er1, @(0x10,sp)
0x032E84  shll.l    #2, er1
0x032E86  add.l     er3, er1
0x032E88  mov.l     @er1, er1
0x032E8C  mov.l     #0x00000008, er0
0x032E92  add.l     sp, er0
0x032E94  jsr       0x018e68
0x032E98  mov.l     @(0x10,sp), er2
0x032E9E  shll.l    #2, er2
0x032EA0  shll.l    er2
0x032EA2  add.l     er4, er2
0x032EA4  mov.l     er0, er1
0x032EA6  mov.l     sp, er0
0x032EA8  jsr       0x018aa0
0x032EAC  jsr       0x01876a
0x032EB0  bt        0x032ed2
0x032EB2  sub.l     er1, er1
0x032EB4  mov.b     @er5, r1l
0x032EB6  shll.l    #2, er1
0x032EB8  shll.l    er1
0x032EBA  add.l     er4, er1
0x032EBC  mov.l     #0x0003f7f6, er2
0x032EC2  mov.l     #0x00000008, er0
0x032EC8  add.l     sp, er0
0x032ECA  jsr       0x018aa0
0x032ECE  jsr       0x01876a
0x032ED2  mov.l     er0, @er6
0x032ED6  mov.l     @er6, er0
0x032EDA  bne       0x032ee6
0x032EDC  mov.l     #0x00000001, er0
0x032EE2  mov.l     er0, @er6
0x032EE6  add.l     #0x00000014, sp
0x032EEC  ldm.l     @sp+, er4-er6
0x032EF0  ldm.l     @sp+, er2-er3
0x032EF4  rts       
