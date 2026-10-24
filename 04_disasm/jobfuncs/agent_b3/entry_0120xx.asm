0x012080  .byte 0x00
0x012081  bt        0x012090   ; 40 0d
0x012083  mov.b     @0xffff19, r0h   ; 20 19
0x012085  .byte 0x00
0x012086  mov.w     r0, @(0xdff0,er6)   ; 6f e0 df f0
0x01208A  bt        0x0120b6   ; 40 2a
0x01208C  mov.w     @(0xdff0,er6), r0   ; 6f 60 df f0
0x012090  extu.l    er0   ; 17 70
0x012092  mov.w     @(0xdff0,er6), r1   ; 6f 61 df f0
0x012096  extu.l    er1   ; 17 71
0x012098  mov.l     #0xffffdffc, er2   ; 7a 02 ff ff df fc
0x01209E  add.l     er6, er2   ; 0a e2
0x0120A0  add.l     er1, er2   ; 0a 92
0x0120A2  mov.b     @(0x400d3d,er0), r0l   ; 78 00 6a 28 00 40 0d 3d
0x0120AA  mov.b     r0l, @er2   ; 68 a8
0x0120AC  mov.w     @(0xdff0,er6), r0   ; 6f 60 df f0
0x0120B0  inc.w     #1, r0   ; 0b 50
0x0120B2  mov.w     r0, @(0xdff0,er6)   ; 6f e0 df f0
0x0120B6  mov.w     @(0xdff0,er6), r0   ; 6f 60 df f0
0x0120BA  cmp.w     #0x0018, r0   ; 79 20 00 18
0x0120BE  bcs       0x01208c   ; 45 cc
0x0120C0  sub.l     er0, er0   ; 1a 80
0x0120C2  mov.b     @0x400442, r0l   ; 6a 28 00 40 04 42
0x0120C8  mov.w     r0, e0   ; 0d 08
0x0120CA  sub.w     r0, r0   ; 19 00
0x0120CC  sub.l     er1, er1   ; 1a 91
0x0120CE  mov.b     @0x400443, r1l   ; 6a 29 00 40 04 43
0x0120D4  shll.l    #2, er1   ; 10 71
0x0120D6  shll.l    #2, er1   ; 10 71
0x0120D8  shll.l    #2, er1   ; 10 71
0x0120DA  shll.l    #2, er1   ; 10 71
0x0120DC  add.l     er1, er0   ; 0a 90
0x0120DE  sub.l     er1, er1   ; 1a 91
0x0120E0  mov.b     @0x400444, r1l   ; 6a 29 00 40 04 44
0x0120E6  add.l     er1, er0   ; 0a 90
0x0120E8  mov.l     er0, @(0xdff6,er6)   ; 01 00 6f e0 df f6
0x0120EE  mov.l     @(0xdff6,er6), er0   ; 01 00 6f 60 df f6
0x0120F4  cmp.l     #0x00002000, er0   ; 7a 20 00 00 20 00
0x0120FA  bcc       0x012106   ; 44 0a
0x0120FC  mov.w     @(0xdff8,er6), r0   ; 6f 60 df f8
