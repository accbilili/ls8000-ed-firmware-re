0x026B0A  mov.b     @(0x1,er6), r0l   ; 6e 68 00 01
0x026B0E  mov.b     r0l, @0x400412   ; 6a a8 00 40 04 12
0x026B14  sub.l     er0, er0   ; 1a 80
0x026B16  mov.b     @(0x2,er6), r0l   ; 6e 68 00 02
0x026B1A  mov.b     r0l, r0h   ; 0c 80
0x026B1C  sub.b     r0l, r0l   ; 18 88
0x026B1E  mov.w     r0, e0   ; 0d 08
0x026B20  sub.w     r0, r0   ; 19 00
0x026B22  sub.l     er1, er1   ; 1a 91
0x026B24  mov.b     @(0x3,er6), r1l   ; 6e 69 00 03
0x026B28  mov.w     r1, e1   ; 0d 19
0x026B2A  sub.w     r1, r1   ; 19 11
0x026B2C  add.l     er1, er0   ; 0a 90
0x026B2E  sub.l     er1, er1   ; 1a 91
0x026B30  mov.b     @(0x4,er6), r1l   ; 6e 69 00 04
0x026B34  shll.l    #2, er1   ; 10 71
0x026B36  shll.l    #2, er1   ; 10 71
0x026B38  shll.l    #2, er1   ; 10 71
0x026B3A  shll.l    #2, er1   ; 10 71
0x026B3C  add.l     er1, er0   ; 0a 90
0x026B3E  sub.l     er1, er1   ; 1a 91
0x026B40  mov.b     @(0x5,er6), r1l   ; 6e 69 00 05
0x026B44  add.l     er1, er0   ; 0a 90
0x026B46  mov.l     er0, @0x400408   ; 01 00 6b a0 00 40 04 08
0x026B4E  sub.l     er0, er0   ; 1a 80
0x026B50  mov.b     @(0x6,er6), r0l   ; 6e 68 00 06
0x026B54  mov.b     r0l, r0h   ; 0c 80
0x026B56  sub.b     r0l, r0l   ; 18 88
0x026B58  mov.w     r0, e0   ; 0d 08
0x026B5A  sub.w     r0, r0   ; 19 00
0x026B5C  sub.l     er1, er1   ; 1a 91
0x026B5E  mov.b     @(0x7,er6), r1l   ; 6e 69 00 07
0x026B62  mov.w     r1, e1   ; 0d 19
0x026B64  sub.w     r1, r1   ; 19 11
0x026B66  add.l     er1, er0   ; 0a 90
0x026B68  sub.l     er1, er1   ; 1a 91
0x026B6A  mov.b     @(0x8,er6), r1l   ; 6e 69 00 08
0x026B6E  shll.l    #2, er1   ; 10 71
0x026B70  shll.l    #2, er1   ; 10 71
0x026B72  shll.l    #2, er1   ; 10 71
0x026B74  shll.l    #2, er1   ; 10 71
0x026B76  add.l     er1, er0   ; 0a 90
0x026B78  sub.l     er1, er1   ; 1a 91
0x026B7A  mov.b     @(0x9,er6), r1l   ; 6e 69 00 09
0x026B7E  add.l     er1, er0   ; 0a 90
0x026B80  mov.l     er0, @0x40040c   ; 01 00 6b a0 00 40 04 0c
0x026B88  mov.b     @(0xa,er6), r0l   ; 6e 68 00 0a
0x026B8C  extu.w    r0   ; 17 50
0x026B8E  mov.b     r0l, r0h   ; 0c 80
0x026B90  sub.b     r0l, r0l   ; 18 88
0x026B92  mov.b     @(0xb,er6), r1l   ; 6e 69 00 0b
0x026B96  extu.w    r1   ; 17 51
0x026B98  add.w     r1, r0   ; 09 10
0x026B9A  mov.w     r0, @er5   ; 69 d0
0x026B9C  mov.b     @(0xc,er6), r0l   ; 6e 68 00 0c
0x026BA0  mov.b     r0l, @0x400413   ; 6a a8 00 40 04 13
0x026BA6  mov.b     @(0xd,er6), r0l   ; 6e 68 00 0d
0x026BAA  mov.b     r0l, @0x400414   ; 6a a8 00 40 04 14
0x026BB0  bt        0x026bd2   ; 40 20
0x026BD2  mov.b     @er6, r0l   ; 68 68
0x026BD4  extu.w    r0   ; 17 50
0x026BD6  bset      #6, r0h   ; 70 60
0x026BD8  mov.w     r0, @0x400400   ; 6b a0 00 40 04 00
0x026BDE  mov.b     #0x01, r0l   ; f8 01
0x026BE0  mov.b     r0l, @0x4007c8   ; 6a a8 00 40 07 c8
0x026BE6  sub.w     r0, r0   ; 19 00
0x026BE8  mov.w     r0, @0x400438   ; 6b a0 00 40 04 38
0x026BEE  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x026BF2  mov.l     @sp+, er3   ; 01 00 6d 73
0x026BF6  rts          ; 54 70
