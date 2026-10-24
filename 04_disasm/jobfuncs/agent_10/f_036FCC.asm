0x036FCC  stm.l     er4-er6, @-sp
0x036FD0  mov.l     #0x00400daa, er4
0x036FD6  mov.l     #0x00400dab, er5
0x036FDC  sub.b     r6l, r6l
0x036FDE  bt        0x037024
0x036FE0  mov.b     r6l, r0l
0x036FE2  extu.w    r0
0x036FE4  extu.l    er0
0x036FE6  add.l     er5, er0
0x036FE8  mov.b     @er0, r1l
0x036FEA  bne       0x036ffa
0x036FEC  mov.b     r6l, r0l
0x036FEE  extu.w    r0
0x036FF0  extu.l    er0
0x036FF2  add.l     er5, er0
0x036FF4  mov.b     #0x01, r1l
0x036FF6  mov.b     r1l, @er0
0x036FF8  bt        0x037022
0x036FFA  mov.b     r6l, r0l
0x036FFC  extu.w    r0
0x036FFE  extu.l    er0
0x037000  add.l     er5, er0
0x037002  mov.b     @er0, r0l
0x037004  cmp.b     #0x05, r0l
0x037006  bne       0x037014
0x037008  mov.b     r6l, r0l
0x03700A  extu.w    r0
0x03700C  extu.l    er0
0x03700E  add.l     er5, er0
0x037010  sub.b     r1l, r1l
0x037012  bt        0x037020
0x037014  mov.b     r6l, r0l
0x037016  extu.w    r0
0x037018  extu.l    er0
0x03701A  add.l     er5, er0
0x03701C  mov.b     @er0, r1l
0x03701E  add.b     #0xff, r1l
0x037020  mov.b     r1l, @er0
0x037022  inc.b     #1, r6l
0x037024  mov.b     @er4, r0l
0x037026  cmp.b     r0l, r6l
0x037028  bcs       0x036fe0
0x03702A  mov.b     @0x400d56, r0l
0x037030  cmp.b     #0x01, r0l
0x037032  bne       0x03707e
0x037034  mov.b     @0x400d7a, r0l
0x03703A  cmp.b     #0x01, r0l
0x03703C  bne       0x03707e
0x03703E  mov.b     @er4, r0l
0x037040  add.b     #0x02, r0l
0x037042  mov.b     r0l, @0x44903f
0x037048  mov.l     #0x00449040, er6
0x03704E  mov.b     @er5, r0l
0x037050  cmp.b     #0x03, r0l
0x037052  beq       0x037068
0x037054  sub.b     r0l, r0l
0x037056  mov.b     r0l, @er6
0x037058  mov.b     #0x01, r0l
0x03705A  mov.b     r0l, @(0x1,er6)
0x03705E  mov.b     #0x02, r0l
0x037060  mov.b     r0l, @(0x2,er6)
0x037064  mov.b     #0x03, r0l
0x037066  bt        0x03707a
0x037068  mov.b     #0x03, r0l
0x03706A  mov.b     r0l, @er6
0x03706C  sub.b     r0l, r0l
0x03706E  mov.b     r0l, @(0x1,er6)
0x037072  mov.b     #0x01, r0l
0x037074  mov.b     r0l, @(0x2,er6)
0x037078  mov.b     #0x02, r0l
0x03707A  mov.b     r0l, @(0x3,er6)
0x03707E  ldm.l     @sp+, er4-er6
0x037082  rts       
