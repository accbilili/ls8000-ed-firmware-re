0x016022  stm.l     er4-er5, @-sp
0x016026  subs.l    #4, sp
0x016028  mov.l     er0, er5
0x01602A  mov.w     r1, r4
0x01602C  mov.l     sp, er1
0x01602E  extu.l    er4
0x016030  add.l     er4, er5
0x016032  mov.b     @er5, r0l
0x016034  mov.b     r0l, @er1
0x016036  inc.l     #1, er1
0x016038  inc.l     #1, er5
0x01603A  mov.b     @er5, r0l
0x01603C  mov.b     r0l, @er1
0x01603E  inc.l     #1, er1
0x016040  inc.l     #1, er5
0x016042  mov.b     @er5, r0l
0x016044  mov.b     r0l, @er1
0x016046  inc.l     #1, er1
0x016048  inc.l     #1, er5
0x01604A  mov.b     @er5, r5l
0x01604C  mov.b     r5l, @er1
0x01604E  mov.l     @sp, er0
0x016052  adds.l    #4, sp
0x016054  ldm.l     @sp+, er4-er5
0x016058  rts       
