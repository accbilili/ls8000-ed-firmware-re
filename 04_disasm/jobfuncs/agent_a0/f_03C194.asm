# fn 0x03C194 (callee_pos) : 11 insns
0x03C194  stm.l     er4-er5, @-sp
0x03C198  mov.l     er0, er5
0x03C19A  sub.b     r4l, r4l
0x03C19C  mov.l     er5, er1
0x03C19E  mov.b     r4l, r0l
0x03C1A0  bsr       0x03c1ae
0x03C1A2  inc.b     #1, r4l
0x03C1A4  cmp.b     #0x03, r4l
0x03C1A6  bls       0x03c19c
0x03C1A8  ldm.l     @sp+, er4-er5
0x03C1AC  rts       
