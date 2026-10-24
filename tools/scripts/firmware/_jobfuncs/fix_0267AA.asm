0x0267AA  stm.l     er2-er3, @-sp
0x0267AE  stm.l     er4-er6, @-sp
0x0267B2  mov.l     #0x00400436, er3
0x0267B8  mov.l     #0x0040043c, er4
0x0267BE  mov.b     @(0x1,er4), r0l
0x0267C2  and.b     #0x1f, r0l
0x0267C4  mov.b     r0l, r2l
0x0267C6  cmp.b     #0x02, r0l
0x0267C8  beq       0x0267d8
0x0267CA  cmp.b     #0x05, r0l
0x0267CC  beq       0x0267d8
0x0267CE  mov.w     #0x0050, r1
0x0267D2  mov.w     r1, @er3
0x0267D4  jmp       0x026940
0x0267D8  mov.b     @(0x9,er4), r0l
0x0267DC  bne       0x0268bc
0x0267E0  sub.l     er6, er6
0x0267E2  mov.b     @(0x3,er4), r6l
0x0267E6  mov.w     r6, e6
0x0267E8  sub.w     r6, r6
0x0267EA  sub.l     er0, er0
0x0267EC  mov.b     @(0x4,er4), r0l
0x0267F0  shll.l    #2, er0
0x0267F2  shll.l    #2, er0
0x0267F4  shll.l    #2, er0
0x0267F6  shll.l    #2, er0
0x0267F8  add.l     er0, er6
0x0267FA  sub.l     er0, er0
0x0267FC  mov.b     @(0x5,er4), r0l
0x026800  add.l     er0, er6
0x026802  sub.l     er5, er5
0x026804  mov.b     @(0x6,er4), r5l
0x026808  mov.w     r5, e5
0x02680A  sub.w     r5, r5
0x02680C  sub.l     er0, er0
0x02680E  mov.b     @(0x7,er4), r0l
0x026812  shll.l    #2, er0
0x026814  shll.l    #2, er0
0x026816  shll.l    #2, er0
0x026818  shll.l    #2, er0
0x02681A  add.l     er0, er5
0x02681C  sub.l     er0, er0
0x02681E  mov.b     @(0x8,er4), r0l
0x026822  add.l     er0, er5
0x026824  mov.b     r2l, r0l
0x026826  cmp.b     #0x02, r0l
0x026828  bne       0x0268a8
0x02682A  mov.b     @(0x2,er4), r0l
0x02682E  bne       0x0268bc
0x026832  sub.b     r4l, r4l
0x026834  mov.l     er6, er0
0x026836  add.l     er5, er0
0x026838  dec.l     #1, er0
0x02683A  mov.l     er0, er2
0x02683C  bt        0x0268a2
0x02683E  mov.b     r4l, r0l
0x026840  extu.w    r0
0x026842  extu.l    er0
0x026844  shll.l    #2, er0
0x026846  shll.l    er0
0x026848  add.l     #0x0003ed88, er0
0x02684E  mov.l     er0, er1
0x026850  mov.l     @er0, er0
0x026854  cmp.l     er0, er6
0x026856  bcs       0x0268a0
0x026858  mov.l     er1, er0
0x02685A  adds.l    #4, er0
0x02685C  mov.l     @er0, er0
0x026860  cmp.l     er0, er6
0x026862  bhi       0x0268a0
0x026864  mov.b     r4l, r0l
0x026866  extu.w    r0
0x026868  extu.l    er0
0x02686A  shll.l    #2, er0
0x02686C  shll.l    er0
0x02686E  mov.l     er2, er1
0x026870  mov.l     @(0x3ed8c,er0), er0
0x02687A  cmp.l     er0, er1
0x02687C  bls       0x026894
0x02687E  sub.l     er5, er5
0x026880  mov.b     r4l, r5l
0x026882  shll.l    #2, er5
0x026884  shll.l    er5
0x026886  mov.l     @(0x3ed8c,er5), er5
0x026890  sub.l     er6, er5
0x026892  inc.l     #1, er5
0x026894  mov.w     r5, r1
0x026896  mov.l     er6, er0
0x026898  jsr       0x011900
0x02689C  jmp       0x026940
0x0268A0  inc.b     #1, r4l
0x0268A2  cmp.b     #0x06, r4l
0x0268A4  bcs       0x02683e
0x0268A6  bt        0x0268bc
0x0268A8  mov.b     @(0x2,er4), r0l
0x0268AC  cmp.b     #0x02, r0l
0x0268AE  bne       0x026900
0x0268B0  mov.l     er6, er0
0x0268B2  add.l     er5, er0
0x0268B4  cmp.l     #0x00020006, er0
0x0268BA  bls       0x0268c4
0x0268BC  mov.w     #0x0050, r0
0x0268C0  mov.w     r0, @er3
0x0268C2  bt        0x026940
0x0268C4  add.l     #0x00060000, er6
0x0268CA  cmp.l     #0x00008000, er5
0x0268D0  bls       0x0268ea
0x0268D2  mov.w     #0x8000, r1
0x0268D6  mov.l     er6, er0
0x0268D8  jsr       0x011900
0x0268DC  sub.l     #0x00008000, er5
0x0268E2  add.l     #0x00008000, er6
0x0268E8  bt        0x0268f4
0x0268EA  mov.w     r5, r1
0x0268EC  mov.l     er6, er0
0x0268EE  jsr       0x011900
0x0268F2  bt        0x026940
0x0268F4  mov.w     #0x5a00, r0
0x0268F8  mov.w     r0, @0xffffbc
0x0268FE  bt        0x0268ca
0x026900  mov.b     @(0x2,er4), r0l
0x026904  cmp.b     #0x03, r0l
0x026906  bne       0x02691a
0x026908  mov.l     #0x00008000, er6
0x02690E  inc.l     #1, er6
0x026910  mov.w     r5, r1
0x026912  mov.l     er6, er0
0x026914  jsr       0x011900
0x026918  bt        0x026940
0x02691A  mov.b     @(0x2,er4), r4l
0x02691E  cmp.b     #0x04, r4l
0x026920  bne       0x02693a
0x026922  cmp.l     #0x00000010, er5
0x026928  bhi       0x02693a
0x02692A  mov.l     #0x00006010, er6
0x026930  mov.w     r5, r1
0x026932  mov.l     er6, er0
0x026934  jsr       0x011900
0x026938  bt        0x026940
0x02693A  mov.w     #0x0050, r0
0x02693E  mov.w     r0, @er3
0x026940  ldm.l     @sp+, er4-er6
0x026944  ldm.l     @sp+, er2-er3
0x026948  rts       
