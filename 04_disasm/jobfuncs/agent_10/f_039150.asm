0x039150  bsr       0x0390f2
0x039152  sub.b     r1l, r1l
0x039154  extu.w    r1
0x039156  extu.l    er1
0x039158  mov.b     #0xff, r0l
0x03915A  mov.b     r0l, @(0x400db8,er1)
0x039162  inc.b     #1, r1l
0x039164  cmp.b     #0x03, r1l
0x039166  bls       0x039154
0x039168  sub.b     r0l, r0l
0x03916A  mov.b     r0l, @0x400eb4
0x039170  rts       
