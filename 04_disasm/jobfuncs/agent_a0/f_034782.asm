# fn 0x034782 (callee_success2) : 31 insns
0x034782  mov.w     r2, @-sp
0x034784  mov.b     @0x4007c9, r0l
0x03478A  extu.w    r0
0x03478C  mov.b     r0l, r0h
0x03478E  sub.b     r0l, r0l
0x034790  mov.b     @0x4007ca, r1l
0x034796  extu.w    r1
0x034798  or.w      r1, r0
0x03479A  mov.w     r0, e0
0x03479C  mov.b     @0x400daa, r1l
0x0347A2  extu.w    r1
0x0347A4  mov.b     r1l, r1h
0x0347A6  sub.b     r1l, r1l
0x0347A8  mov.b     @0x400dab, r2l
0x0347AE  extu.w    r2
0x0347B0  or.w      r2, r1
0x0347B2  mov.w     r1, e1
0x0347B4  mov.b     @0x4007cb, r2l
0x0347BA  bne       0x0347d0
0x0347BC  mov.w     @0x4007cc, r2
0x0347C2  cmp.w     r0, r2
0x0347C4  bne       0x0347d0
0x0347C6  mov.w     @0x4007ce, r2
0x0347CC  cmp.w     r1, r2
0x0347CE  beq       0x0347e2
0x0347D0  mov.w     e0, @0x4007cc
0x0347D6  mov.w     e1, @0x4007ce
0x0347DC  bsr       0x0347e6
0x0347DE  bsr       0x034bbe
0x0347E2  mov.w     @sp+, r2
0x0347E4  rts       
