0x032BDC  stm.l     er2-er3, @-sp
0x032BE0  stm.l     er4-er6, @-sp
0x032BE4  sub.l     #0x0000001c, sp
0x032BEA  mov.b     @0x4007c9, r0h
0x032BF0  mov.b     @0x4007ca, r0l
0x032BF6  jsr       0x02ed5a
0x032BFA  bsr       0x033422
0x032BFE  mov.w     @0x400d64, r0
0x032C04  mov.w     r0, @0x400d6c
0x032C0A  mov.w     @0x400d60, r0
0x032C10  mov.w     r0, @0x400d6a
0x032C16  mov.b     #0x01, r0l
0x032C18  mov.b     r0l, @0x400dab
0x032C1E  mov.b     r0l, @0x400d8a
0x032C24  mov.l     #0x00000004, er6
0x032C2A  mov.l     #0x00420276, er5
0x032C30  add.l     er6, er5
0x032C32  mov.l     @(0x400f32,er6), er1
0x032C3C  mov.l     #0x00000010, er0
0x032C42  add.l     sp, er0
0x032C44  jsr       0x018e68
0x032C48  mov.l     er0, er1
0x032C4A  mov.l     #0x0003f7e6, er2
0x032C50  mov.l     #0x00000008, er0
0x032C56  add.l     sp, er0
0x032C58  jsr       0x018aa0
0x032C5C  mov.l     er0, er1
0x032C5E  mov.l     #0x0003f7ee, er2
0x032C64  mov.l     sp, er0
0x032C66  jsr       0x01842c
0x032C6A  jsr       0x01876a
0x032C6E  mov.l     @(0x400f42,er6), er1
0x032C78  add.l     er1, er0
0x032C7A  mov.l     er0, @er5
0x032C7E  jsr       0x018e9e
0x032C82  sub.l     er1, er1
0x032C84  mov.b     @0x41ff6f, r1l
0x032C8A  shll.l    #2, er1
0x032C8C  mov.l     @(0x400dda,er1), er1
0x032C96  jsr       0x0185ee
0x032C9A  jsr       0x018860
0x032C9E  mov.l     er0, @(0x420286,er6)
0x032CA8  jsr       0x02d1dc
0x032CAC  sub.l     er5, er5
0x032CAE  sub.b     r4l, r4l
0x032CB0  add.l     #0x00420250, er6
0x032CB6  mov.l     er6, er2
0x032CB8  mov.l     #0x00420286, er1
0x032CBE  mov.b     #0x01, r0l
0x032CC0  jsr       0x02d700
0x032CC4  mov.w     @0x400d6c, r6
0x032CCA  extu.l    er6
0x032CCC  shll.l    er6
0x032CCE  mov.l     er2, er0
0x032CD0  mov.l     @er0, er0
0x032CD4  add.l     er0, er6
0x032CD6  mov.l     er6, er3
0x032CD8  add.l     #0x00000bb8, er3
0x032CDE  mov.w     #0x5a00, r0
0x032CE2  mov.w     r0, @0xffffbc
0x032CE8  cmp.l     er3, er6
0x032CEA  bcc       0x032cfc
0x032CEC  mov.w     @er6+, r0
0x032CEE  mov.w     @er6, r1
0x032CF0  sub.w     r1, r0
0x032CF2  jsr       0x017f04
0x032CF6  exts.l    er0
0x032CF8  add.l     er0, er5
0x032CFA  bt        0x032ce8
0x032CFC  inc.b     #1, r4l
0x032CFE  cmp.b     #0x04, r4l
0x032D00  bcs       0x032cb8
0x032D02  shlr.l    #2, er5
0x032D04  mov.l     er5, er0
0x032D06  mov.l     #0x00000003, er1
0x032D0C  jsr       0x01872e
0x032D10  mov.l     er0, @0x42029a
0x032D18  jsr       0x02d694
0x032D1C  add.l     #0x0000001c, sp
0x032D22  ldm.l     @sp+, er4-er6
0x032D26  ldm.l     @sp+, er2-er3
0x032D2A  rts       
