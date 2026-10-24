0x039172  stm.l     er4-er5, @-sp
0x039176  mov.l     #0x00400db8, er5
0x03917C  bsr       0x0390f2
0x039180  sub.b     r4l, r4l
0x039182  extu.w    r4
0x039184  extu.l    er4
0x039186  mov.l     er5, er0
0x039188  add.l     er4, er0
0x03918A  mov.b     #0xff, r1l
0x03918C  mov.b     r1l, @er0
0x03918E  inc.b     #1, r4l
0x039190  cmp.b     #0x02, r4l
0x039192  bls       0x039182
0x039194  mov.b     #0xff, r0l
0x039196  mov.b     r0l, @(0x3,er5)
0x03919A  mov.b     #0x01, r0l
0x03919C  mov.b     r0l, @0x400eb4
0x0391A2  ldm.l     @sp+, er4-er5
0x0391A6  rts       
