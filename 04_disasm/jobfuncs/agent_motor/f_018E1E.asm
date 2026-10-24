0x018E1E  stm.l     er2-er3, @-sp
0x018E22  mov.w     e0, r2
0x018E24  mulxu.w   r1, er2
0x018E26  mov.w     e1, r3
0x018E28  mulxu.w   r0, er3
0x018E2A  mulxu.w   r1, er0
0x018E2C  add.w     r2, e0
0x018E2E  add.w     r3, e0
0x018E30  ldm.l     @sp+, er2-er3
0x018E34  rts       
