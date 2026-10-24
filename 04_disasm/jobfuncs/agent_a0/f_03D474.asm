# fn 0x03D474 (callee_success3) : 14 insns
0x03D474  mov.l     er0, @-sp
0x03D478  mov.l     er1, @-sp
0x03D47C  mov.l     er2, @-sp
0x03D480  mov.l     #0x0003d4a8, er0
0x03D486  mov.l     #0x00ffdd00, er1
0x03D48C  mov.w     @er0+, r2
0x03D48E  mov.w     r2, @er1
0x03D490  inc.l     #2, er1
0x03D492  cmp.l     #0x0003d582, er0
0x03D498  bcs       0x03d48c
0x03D49A  mov.l     @sp+, er2
0x03D49E  mov.l     @sp+, er1
0x03D4A2  mov.l     @sp+, er0
0x03D4A6  rts       
