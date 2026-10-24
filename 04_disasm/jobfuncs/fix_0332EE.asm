0x0332EE  stm.l     er4-er6, @-sp
0x0332F2  mov.l     #0x00420265, er5
0x0332F8  mov.l     #0x00400df4, er6
0x0332FE  mov.b     @er5, r0l
0x033300  shll.b    #2, r0l
0x033302  shll.b    #2, r0l
0x033304  mov.b     r0l, @er6
0x033306  mov.b     @0x420266, r0l
0x03330C  cmp.b     #0x01, r0l
0x03330E  bne       0x033316
0x033310  mov.b     @er6, r0l
0x033312  or.b      #0x80, r0l
0x033314  mov.b     r0l, @er6
0x033316  mov.b     @er6, r0l
0x033318  mov.b     r0l, @0x2001ca
0x03331E  mov.l     @0x420248, er0
0x033326  jsr       0x018e9e
0x03332A  sub.l     er4, er4
0x03332C  mov.b     @er5, r4l
0x03332E  sub.l     er1, er1
0x033330  mov.b     @(0x41ff6e,er4), r1l
0x033338  shll.l    #2, er1
0x03333A  mov.l     @(0x400dda,er1), er1
0x033344  jsr       0x0185ee
0x033348  jsr       0x018860
0x03334C  mov.l     er0, @0x42024c
0x033354  shll.l    #2, er4
0x033356  mov.l     @(0x3f146,er4), er4
0x033360  mov.l     @0x42024c, er0
0x033368  mov.l     er0, @er4
0x03336C  sub.l     er4, er4
0x03336E  mov.b     @er5, r4l
0x033370  mov.l     er4, er0
0x033372  shll.l    #2, er0
0x033374  mov.l     @(0x3f156,er0), er0
0x03337E  mov.b     @(0x440fdc,er4), r1l
0x033386  mov.b     r1l, @er0
0x033388  ldm.l     @sp+, er4-er6
0x03338C  rts       
