0x03A2D8  stm.l     er2-er3, @-sp
0x03A2DC  stm.l     er4-er6, @-sp
0x03A2E0  mov.l     er1, er2
0x03A2E2  sub.b     r6l, r6l
0x03A2E4  mov.b     r0l, r3l
0x03A2E6  extu.w    r3
0x03A2E8  mov.w     #0x000c, e3
0x03A2EC  mulxu.w   e3, er3
0x03A2EE  add.l     #0x0003f920, er3
0x03A2F4  mov.b     r6l, r5l
0x03A2F6  extu.w    r5
0x03A2F8  extu.l    er5
0x03A2FA  mov.l     er5, er4
0x03A2FC  shll.l    #2, er4
0x03A2FE  mov.l     @(0x3f914,er4), er0
0x03A308  mov.b     @(0x3f90e,er5), r1l
0x03A310  mov.b     r1l, @er0
0x03A312  shll.l    er5
0x03A314  mov.l     er2, er0
0x03A316  add.l     er5, er0
0x03A318  mov.w     @er0, r0
0x03A31A  bsr       0x03a334
0x03A31C  add.l     er3, er4
0x03A31E  mov.l     @er4, er4
0x03A322  mov.w     r0, @er4
0x03A324  inc.b     #1, r6l
0x03A326  cmp.b     #0x03, r6l
0x03A328  bcs       0x03a2f4
0x03A32A  ldm.l     @sp+, er4-er6
0x03A32E  ldm.l     @sp+, er2-er3
0x03A332  rts       
