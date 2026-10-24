# fn 0x018EDE (helper_dbl?) : 14 insns
0x018EDE  mov.l     er1, @-sp
0x018EE2  mov.w     r1, e1
0x018EE4  beq       0x018ef4
0x018EE6  mov.w     #0x040f, e1
0x018EEA  dec.w     #1, e1
0x018EEC  shll.w    r1
0x018EEE  bcc       0x018eea
0x018EF0  shll.l    #2, er1
0x018EF2  shll.l    #2, er1
0x018EF4  mov.l     er1, @er0
0x018EF8  sub.l     er1, er1
0x018EFA  mov.l     er1, @(0x4,er0)
0x018F00  mov.l     @sp+, er1
0x018F04  rts       
