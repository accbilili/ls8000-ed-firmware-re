0x012100  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x012104  bt        0x01210e   ; 40 08
0x012106  mov.w     #0x2000, r0   ; 79 00 20 00
0x01210A  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x01210E  mov.w     @(0xdffa,er6), r0   ; 6f 60 df fa
0x012112  extu.l    er0   ; 17 70
0x012114  mov.l     @(0xdff6,er6), er1   ; 01 00 6f 61 df f6
0x01211A  sub.l     er0, er1   ; 1a 81
0x01211C  mov.l     er1, @(0xdff6,er6)   ; 01 00 6f e1 df f6
0x012122  bset      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 70 40
0x01212A  mov.w     @(0xdffa,er6), r1   ; 6f 61 df fa
0x01212E  sub.w     #0x0018, r1   ; 79 31 00 18
0x012132  mov.l     #0xffffe014, er0   ; 7a 00 ff ff e0 14
0x012138  add.l     er6, er0   ; 0a e0
0x01213A  jsr       0x0118d0   ; 5e 01 18 d0
0x01213E  bclr      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 72 40
0x012146  mov.b     #0x01, r0l   ; f8 01
0x012148  mov.b     r0l, @0x400d3a   ; 6a a8 00 40 0d 3a
0x01214E  mov.w     @0xfffed2, r0   ; 6b 20 00 ff fe d2
0x012154  mov.w     r0, @(0xdfee,er6)   ; 6f e0 df ee
0x012158  mov.w     @(0xdfee,er6), r0   ; 6f 60 df ee
0x01215C  and.w     #0xfffc, r0   ; 79 60 ff fc
0x012160  or.w      #0x0003, r0   ; 79 40 00 03
0x012164  mov.w     r0, @0xfffed2   ; 6b a0 00 ff fe d2
0x01216A  jsr       0x017a80   ; 5e 01 7a 80
0x01216E  mov.b     #0x01, r0l   ; f8 01
0x012170  mov.b     r0l, @0x400ca0   ; 6a a8 00 40 0c a0
0x012176  mov.b     #0x01, r0l   ; f8 01
0x012178  mov.b     r0l, @0x400ca1   ; 6a a8 00 40 0c a1
0x01217E  mov.l     #0x00004000, er0   ; 7a 00 00 00 40 00
0x012184  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x01218C  jsr       0x010bd2   ; 5e 01 0b d2
0x012190  jsr       0x017a78   ; 5e 01 7a 78
0x012194  jsr       0x010bd8   ; 5e 01 0b d8
0x012198  mov.b     #0x02, r0l   ; f8 02
0x01219A  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x0121A0  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x0121A6  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x0121AE  jsr       0x010bd2   ; 5e 01 0b d2
0x0121B2  jsr       0x017a7c   ; 5e 01 7a 7c
0x0121B6  jsr       0x010bd8   ; 5e 01 0b d8
0x0121BA  sub.l     er0, er0   ; 1a 80
0x0121BC  mov.b     @(0xdffd,er6), r0l   ; 6e 68 df fd
0x0121C0  mov.w     r0, e0   ; 0d 08
0x0121C2  sub.w     r0, r0   ; 19 00
0x0121C4  sub.l     er1, er1   ; 1a 91
0x0121C6  mov.b     @(0xdffe,er6), r1l   ; 6e 69 df fe
0x0121CA  shll.l    #2, er1   ; 10 71
0x0121CC  shll.l    #2, er1   ; 10 71
0x0121CE  shll.l    #2, er1   ; 10 71
0x0121D0  shll.l    #2, er1   ; 10 71
0x0121D2  add.l     er1, er0   ; 0a 90
0x0121D4  sub.l     er1, er1   ; 1a 91
0x0121D6  mov.b     @(0xdffc,er6), r1l   ; 6e 69 df fc
0x0121DA  mov.b     r1l, r1h   ; 0c 91
0x0121DC  sub.b     r1l, r1l   ; 18 99
0x0121DE  mov.w     r1, e1   ; 0d 19
0x0121E0  sub.w     r1, r1   ; 19 11
0x0121E2  add.l     er1, er0   ; 0a 90
0x0121E4  sub.l     er1, er1   ; 1a 91
0x0121E6  mov.b     @(0xdfff,er6), r1l   ; 6e 69 df ff
0x0121EA  add.l     er1, er0   ; 0a 90
0x0121EC  mov.l     er0, @0x400d24   ; 01 00 6b a0 00 40 0d 24
0x0121F4  sub.l     er0, er0   ; 1a 80
0x0121F6  mov.b     @(0xe000,er6), r0l   ; 6e 68 e0 00
0x0121FA  mov.b     r0l, r0h   ; 0c 80
0x0121FC  sub.b     r0l, r0l   ; 18 88
0x0121FE  mov.w     r0, e0   ; 0d 08
0x012200  sub.w     r0, r0   ; 19 00
0x012202  sub.l     er1, er1   ; 1a 91
0x012204  mov.b     @(0xe001,er6), r1l   ; 6e 69 e0 01
0x012208  mov.w     r1, e1   ; 0d 19
0x01220A  sub.w     r1, r1   ; 19 11
0x01220C  add.l     er1, er0   ; 0a 90
0x01220E  sub.l     er1, er1   ; 1a 91
0x012210  mov.b     @(0xe002,er6), r1l   ; 6e 69 e0 02
0x012214  shll.l    #2, er1   ; 10 71
0x012216  shll.l    #2, er1   ; 10 71
0x012218  shll.l    #2, er1   ; 10 71
0x01221A  shll.l    #2, er1   ; 10 71
0x01221C  add.l     er1, er0   ; 0a 90
0x01221E  sub.l     er1, er1   ; 1a 91
0x012220  mov.b     @(0xe003,er6), r1l   ; 6e 69 e0 03
0x012224  add.l     er1, er0   ; 0a 90
0x012226  mov.l     er0, @0x400d28   ; 01 00 6b a0 00 40 0d 28
0x01222E  sub.l     er0, er0   ; 1a 80
0x012230  mov.b     @(0xe004,er6), r0l   ; 6e 68 e0 04
0x012234  mov.b     r0l, r0h   ; 0c 80
0x012236  sub.b     r0l, r0l   ; 18 88
0x012238  mov.w     r0, e0   ; 0d 08
0x01223A  sub.w     r0, r0   ; 19 00
0x01223C  sub.l     er1, er1   ; 1a 91
0x01223E  mov.b     @(0xe005,er6), r1l   ; 6e 69 e0 05
0x012242  mov.w     r1, e1   ; 0d 19
0x012244  sub.w     r1, r1   ; 19 11
0x012246  add.l     er1, er0   ; 0a 90
0x012248  sub.l     er1, er1   ; 1a 91
0x01224A  mov.b     @(0xe006,er6), r1l   ; 6e 69 e0 06
0x01224E  shll.l    #2, er1   ; 10 71
0x012250  shll.l    #2, er1   ; 10 71
0x012252  shll.l    #2, er1   ; 10 71
0x012254  shll.l    #2, er1   ; 10 71
0x012256  add.l     er1, er0   ; 0a 90
0x012258  sub.l     er1, er1   ; 1a 91
0x01225A  mov.b     @(0xe007,er6), r1l   ; 6e 69 e0 07
0x01225E  add.l     er1, er0   ; 0a 90
0x012260  mov.l     er0, @0x400d34   ; 01 00 6b a0 00 40 0d 34
0x012268  sub.l     er0, er0   ; 1a 80
0x01226A  mov.b     @(0xe008,er6), r0l   ; 6e 68 e0 08
0x01226E  mov.b     r0l, r0h   ; 0c 80
0x012270  sub.b     r0l, r0l   ; 18 88
0x012272  mov.w     r0, e0   ; 0d 08
0x012274  sub.w     r0, r0   ; 19 00
0x012276  sub.l     er1, er1   ; 1a 91
0x012278  mov.b     @(0xe009,er6), r1l   ; 6e 69 e0 09
0x01227C  mov.w     r1, e1   ; 0d 19
0x01227E  sub.w     r1, r1   ; 19 11
0x012280  add.l     er1, er0   ; 0a 90
0x012282  sub.l     er1, er1   ; 1a 91
0x012284  mov.b     @(0xe00a,er6), r1l   ; 6e 69 e0 0a
0x012288  shll.l    #2, er1   ; 10 71
0x01228A  shll.l    #2, er1   ; 10 71
0x01228C  shll.l    #2, er1   ; 10 71
0x01228E  shll.l    #2, er1   ; 10 71
0x012290  add.l     er1, er0   ; 0a 90
0x012292  sub.l     er1, er1   ; 1a 91
0x012294  mov.b     @(0xe00b,er6), r1l   ; 6e 69 e0 0b
0x012298  add.l     er1, er0   ; 0a 90
0x01229A  mov.l     er0, @(0xdff2,er6)   ; 01 00 6f e0 df f2
0x0122A0  mov.l     @0x400d28, er0   ; 01 00 6b 20 00 40 0d 28
0x0122A8  add.l     #0x0000007f, er0   ; 7a 10 00 00 00 7f
0x0122AE  shlr.l    #2, er0   ; 11 70
0x0122B0  shlr.l    #2, er0   ; 11 70
0x0122B2  shlr.l    #2, er0   ; 11 70
0x0122B4  shlr.l    er0   ; 11 30
0x0122B6  shll.l    #2, er0   ; 10 70
0x0122B8  shll.l    #2, er0   ; 10 70
0x0122BA  shll.l    #2, er0   ; 10 70
0x0122BC  shll.l    er0   ; 10 30
0x0122BE  mov.l     er0, @0x400d2c   ; 01 00 6b a0 00 40 0d 2c
0x0122C6  mov.l     @0x400d2c, er0   ; 01 00 6b 20 00 40 0d 2c
0x0122CE  mov.l     @0x400d34, er1   ; 01 00 6b 21 00 40 0d 34
0x0122D6  sub.l     er1, er0   ; 1a 90
0x0122D8  mov.l     @(0xdff2,er6), er1   ; 01 00 6f 61 df f2
0x0122DE  add.l     er1, er0   ; 0a 90
0x0122E0  mov.l     er0, @0x400d30   ; 01 00 6b a0 00 40 0d 30
0x0122E8  sub.l     er0, er0   ; 1a 80
0x0122EA  mov.b     @(0xe014,er6), r0l   ; 6e 68 e0 14
0x0122EE  mov.b     r0l, r0h   ; 0c 80
0x0122F0  sub.b     r0l, r0l   ; 18 88
0x0122F2  mov.w     r0, e0   ; 0d 08
0x0122F4  sub.w     r0, r0   ; 19 00
0x0122F6  sub.l     er1, er1   ; 1a 91
0x0122F8  mov.b     @(0xe015,er6), r1l   ; 6e 69 e0 15
0x0122FC  mov.w     r1, e1   ; 0d 19
0x0122FE  sub.w     r1, r1   ; 19 11
0x012300  add.l     er1, er0   ; 0a 90
0x012302  sub.l     er1, er1   ; 1a 91
0x012304  mov.b     @(0xe016,er6), r1l   ; 6e 69 e0 16
0x012308  shll.l    #2, er1   ; 10 71
0x01230A  shll.l    #2, er1   ; 10 71
0x01230C  shll.l    #2, er1   ; 10 71
0x01230E  shll.l    #2, er1   ; 10 71
0x012310  add.l     er1, er0   ; 0a 90
0x012312  sub.l     er1, er1   ; 1a 91
0x012314  mov.b     @(0xe017,er6), r1l   ; 6e 69 e0 17
0x012318  add.l     er1, er0   ; 0a 90
0x01231A  mov.l     er0, @0x400d58   ; 01 00 6b a0 00 40 0d 58
0x012322  mov.l     @0x400d24, er0   ; 01 00 6b 20 00 40 0d 24
0x01232A  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x012332  jsr       0x010bd2   ; 5e 01 0b d2
0x012336  jsr       0x017a78   ; 5e 01 7a 78
0x01233A  jsr       0x010bd8   ; 5e 01 0b d8
0x01233E  mov.l     @0x400d2c, er0   ; 01 00 6b 20 00 40 0d 2c
0x012346  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x01234E  sub.b     r0l, r0l   ; 18 88
0x012350  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x012356  sub.b     r0l, r0l   ; 18 88
0x012358  mov.b     r0l, @0x400d39   ; 6a a8 00 40 0d 39
0x01235E  jmp       0x0123e2   ; 5a 01 23 e2
0x012362  mov.l     #0xffffdff6, er0   ; 7a 00 ff ff df f6
0x012368  add.l     er6, er0   ; 0a e0
0x01236A  mov.l     er0, @-sp   ; 01 00 6d f0
0x01236E  mov.l     #0xffffdffa, er1   ; 7a 01 ff ff df fa
0x012374  add.l     er6, er1   ; 0a e1
0x012376  mov.l     #0xffffdffc, er0   ; 7a 00 ff ff df fc
0x01237C  add.l     er6, er0   ; 0a e0
0x01237E  bsr       0x01258e   ; 5c 00 02 0c
0x012382  adds.l    #4, sp   ; 0b 97
0x012384  mov.l     @(0xdff6,er6), er0   ; 01 00 6f 60 df f6
0x01238A  bne       0x01238e   ; 46 02
0x01238C  bt        0x0123e6   ; 40 58
0x01238E  mov.l     @(0xdff6,er6), er0   ; 01 00 6f 60 df f6
0x012394  cmp.l     #0x00002000, er0   ; 7a 20 00 00 20 00
0x01239A  bcc       0x0123a6   ; 44 0a
0x01239C  mov.w     @(0xdff8,er6), r0   ; 6f 60 df f8
0x0123A0  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x0123A4  bt        0x0123ae   ; 40 08
0x0123A6  mov.w     #0x2000, r0   ; 79 00 20 00
0x0123AA  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x0123AE  bset      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 70 40
0x0123B6  mov.l     #0xffffdffc, er0   ; 7a 00 ff ff df fc
0x0123BC  add.l     er6, er0   ; 0a e0
0x0123BE  mov.w     @(0xdffa,er6), r1   ; 6f 61 df fa
0x0123C2  jsr       0x0118d0   ; 5e 01 18 d0
0x0123C6  bclr      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 72 40
0x0123CE  mov.w     @(0xdffa,er6), r0   ; 6f 60 df fa
0x0123D2  extu.l    er0   ; 17 70
0x0123D4  mov.l     @(0xdff6,er6), er1   ; 01 00 6f 61 df f6
0x0123DA  sub.l     er0, er1   ; 1a 81
0x0123DC  mov.l     er1, @(0xdff6,er6)   ; 01 00 6f e1 df f6
0x0123E2  jmp       0x012362   ; 5a 01 23 62
0x0123E6  jmp       0x0124f4   ; 5a 01 24 f4
0x0123EA  sub.l     er0, er0   ; 1a 80
0x0123EC  mov.b     @0x400442, r0l   ; 6a 28 00 40 04 42
0x0123F2  mov.w     r0, e0   ; 0d 08
0x0123F4  sub.w     r0, r0   ; 19 00
0x0123F6  sub.l     er1, er1   ; 1a 91
0x0123F8  mov.b     @0x400443, r1l   ; 6a 29 00 40 04 43
0x0123FE  shll.l    #2, er1   ; 10 71
0x012400  shll.l    #2, er1   ; 10 71
0x012402  shll.l    #2, er1   ; 10 71
0x012404  shll.l    #2, er1   ; 10 71
0x012406  add.l     er1, er0   ; 0a 90
0x012408  sub.l     er1, er1   ; 1a 91
0x01240A  mov.b     @0x400444, r1l   ; 6a 29 00 40 04 44
0x012410  add.l     er1, er0   ; 0a 90
0x012412  mov.l     er0, @(0xdff6,er6)   ; 01 00 6f e0 df f6
0x012418  mov.l     @(0xdff6,er6), er0   ; 01 00 6f 60 df f6
0x01241E  cmp.l     #0x00002000, er0   ; 7a 20 00 00 20 00
0x012424  bcc       0x012430   ; 44 0a
0x012426  mov.w     @(0xdff8,er6), r0   ; 6f 60 df f8
0x01242A  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x01242E  bt        0x012438   ; 40 08
0x012430  mov.w     #0x2000, r0   ; 79 00 20 00
0x012434  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x012438  bset      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 70 40
0x012440  mov.l     #0xffffdffc, er0   ; 7a 00 ff ff df fc
0x012446  add.l     er6, er0   ; 0a e0
0x012448  mov.w     @(0xdffa,er6), r1   ; 6f 61 df fa
0x01244C  jsr       0x0118d0   ; 5e 01 18 d0
0x012450  bclr      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 72 40
0x012458  mov.w     @(0xdffa,er6), r0   ; 6f 60 df fa
0x01245C  extu.l    er0   ; 17 70
0x01245E  mov.l     @(0xdff6,er6), er1   ; 01 00 6f 61 df f6
0x012464  sub.l     er0, er1   ; 1a 81
0x012466  mov.l     er1, @(0xdff6,er6)   ; 01 00 6f e1 df f6
0x01246C  jmp       0x0124f0   ; 5a 01 24 f0
0x012470  mov.l     #0xffffdff6, er0   ; 7a 00 ff ff df f6
0x012476  add.l     er6, er0   ; 0a e0
0x012478  mov.l     er0, @-sp   ; 01 00 6d f0
0x01247C  mov.l     #0xffffdffa, er1   ; 7a 01 ff ff df fa
0x012482  add.l     er6, er1   ; 0a e1
0x012484  mov.l     #0xffffdffc, er0   ; 7a 00 ff ff df fc
0x01248A  add.l     er6, er0   ; 0a e0
0x01248C  bsr       0x01258e   ; 5c 00 00 fe
0x012490  adds.l    #4, sp   ; 0b 97
0x012492  mov.l     @(0xdff6,er6), er0   ; 01 00 6f 60 df f6
0x012498  bne       0x01249c   ; 46 02
0x01249A  bt        0x0124f4   ; 40 58
0x01249C  mov.l     @(0xdff6,er6), er0   ; 01 00 6f 60 df f6
0x0124A2  cmp.l     #0x00002000, er0   ; 7a 20 00 00 20 00
0x0124A8  bcc       0x0124b4   ; 44 0a
0x0124AA  mov.w     @(0xdff8,er6), r0   ; 6f 60 df f8
0x0124AE  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x0124B2  bt        0x0124bc   ; 40 08
0x0124B4  mov.w     #0x2000, r0   ; 79 00 20 00
0x0124B8  mov.w     r0, @(0xdffa,er6)   ; 6f e0 df fa
0x0124BC  bset      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 70 40
0x0124C4  mov.l     #0xffffdffc, er0   ; 7a 00 ff ff df fc
0x0124CA  add.l     er6, er0   ; 0a e0
0x0124CC  mov.w     @(0xdffa,er6), r1   ; 6f 61 df fa
0x0124D0  jsr       0x0118d0   ; 5e 01 18 d0
0x0124D4  bclr      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 72 40
0x0124DC  mov.w     @(0xdffa,er6), r0   ; 6f 60 df fa
0x0124E0  extu.l    er0   ; 17 70
0x0124E2  mov.l     @(0xdff6,er6), er1   ; 01 00 6f 61 df f6
0x0124E8  sub.l     er0, er1   ; 1a 81
0x0124EA  mov.l     er1, @(0xdff6,er6)   ; 01 00 6f e1 df f6
0x0124F0  jmp       0x012470   ; 5a 01 24 70
0x0124F4  mov.b     @0x400d20, r0l   ; 6a 28 00 40 0d 20
0x0124FA  mov.b     r0l, @0x400d21   ; 6a a8 00 40 0d 21
0x012500  mov.l     @0x400d24, er0   ; 01 00 6b 20 00 40 0d 24
0x012508  mov.l     er0, @0x40031e   ; 01 00 6b a0 00 40 03 1e
0x012510  mov.l     @0x400d28, er0   ; 01 00 6b 20 00 40 0d 28
0x012518  mov.l     er0, @0x400322   ; 01 00 6b a0 00 40 03 22
0x012520  mov.l     @0x400d34, er0   ; 01 00 6b 20 00 40 0d 34
0x012528  mov.l     er0, @0x400326   ; 01 00 6b a0 00 40 03 26
0x012530  mov.l     @(0xdff2,er6), er0   ; 01 00 6f 60 df f2
0x012536  mov.l     er0, @0x40032a   ; 01 00 6b a0 00 40 03 2a
0x01253E  mov.l     @0x400d2c, er0   ; 01 00 6b 20 00 40 0d 2c
0x012546  mov.l     er0, @0x40032e   ; 01 00 6b a0 00 40 03 2e
0x01254E  mov.l     @0x400d30, er0   ; 01 00 6b 20 00 40 0d 30
0x012556  mov.l     er0, @0x400332   ; 01 00 6b a0 00 40 03 32
0x01255E  mov.l     @0x400d58, er0   ; 01 00 6b 20 00 40 0d 58
0x012566  mov.l     er0, @0x400336   ; 01 00 6b a0 00 40 03 36
0x01256E  sub.b     r0l, r0l   ; 18 88
0x012570  mov.b     r0l, @0x400d22   ; 6a a8 00 40 0d 22
0x012576  bset      #4, @0xffff2e   ; 6a 38 00 ff ff 2e 70 40
0x01257E  add.l     #0x0000200e, sp   ; 7a 17 00 00 20 0e
0x012584  mov.l     @sp+, er2   ; 01 00 6d 72
0x012588  mov.l     @sp+, er6   ; 01 00 6d 76
0x01258C  rts          ; 54 70
0x01258E  mov.l     er6, @-sp   ; 01 00 6d f6
0x012592  mov.l     sp, er6   ; 0f f6
0x012594  mov.l     er2, @-sp   ; 01 00 6d f2
0x012598  stm.l     er4-er5, @-sp   ; 01 10 6d f4
0x01259C  subs.l    #4, sp   ; 1b 97
0x01259E  subs.l    #4, sp   ; 1b 97
0x0125A0  mov.l     er0, er5   ; 0f 85
0x0125A2  mov.l     er1, er4   ; 0f 94
0x0125A4  sub.w     r0, r0   ; 19 00
0x0125A6  mov.w     r0, @(0xfff2,er6)   ; 6f e0 ff f2
0x0125AA  jmp       0x0127ee   ; 5a 01 27 ee
0x0125AE  mov.l     #0x00400d38, er0   ; 7a 00 00 40 0d 38
0x0125B4  mov.b     @er0, r1l   ; 68 09
0x0125B6  inc.b     #1, r1l   ; 0a 09
0x0125B8  mov.b     r1l, @er0   ; 68 89
0x0125BA  dec.b     #1, r1l   ; 1a 09
0x0125BC  extu.w    r1   ; 17 51
0x0125BE  extu.l    er1   ; 17 71
0x0125C0  mov.w     @(0xfff2,er6), r0   ; 6f 60 ff f2
0x0125C4  inc.w     #1, r0   ; 0b 50
0x0125C6  mov.w     r0, @(0xfff2,er6)   ; 6f e0 ff f2
0x0125CA  dec.w     #1, r0   ; 1b 50
0x0125CC  extu.l    er0   ; 17 70
0x0125CE  add.l     er5, er0   ; 0a d0
0x0125D0  mov.b     @er0, r0l   ; 68 08
0x0125D2  mov.b     r0l, @(0x400ca0,er1)   ; 78 10 6a a8 00 40 0c a0
0x0125DA  mov.w     #0x5a00, r0   ; 79 00 5a 00
0x0125DE  mov.w     r0, @0xffffbc   ; 6b a0 00 ff ff bc
0x0125E4  sub.l     er0, er0   ; 1a 80
0x0125E6  mov.b     @0x400d38, r0l   ; 6a 28 00 40 0d 38
0x0125EC  mov.l     @0xffdc34, er1   ; 01 00 6b 21 00 ff dc 34
0x0125F4  add.l     er0, er1   ; 0a 81
0x0125F6  mov.l     @0x400d30, er0   ; 01 00 6b 20 00 40 0d 30
0x0125FE  cmp.l     er0, er1   ; 1f 81
0x012600  bne       0x012648   ; 46 46
0x012602  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x012608  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x012610  jsr       0x010bd2   ; 5e 01 0b d2
0x012614  jsr       0x017a7c   ; 5e 01 7a 7c
0x012618  jsr       0x010bd8   ; 5e 01 0b d8
0x01261C  mov.b     #0x01, r0l   ; f8 01
0x01261E  mov.b     r0l, @0x400d39   ; 6a a8 00 40 0d 39
0x012624  sub.l     er0, er0   ; 1a 80
0x012626  mov.b     @0x400d38, r0l   ; 6a 28 00 40 0d 38
0x01262C  mov.l     #0x00400d34, er1   ; 7a 01 00 40 0d 34
0x012632  mov.l     @er1, er2   ; 01 00 69 12
0x012636  add.l     er0, er2   ; 0a 82
0x012638  mov.l     er2, @er1   ; 01 00 69 92
0x01263C  sub.b     r0l, r0l   ; 18 88
0x01263E  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x012644  jmp       0x01274e   ; 5a 01 27 4e
0x012648  sub.l     er0, er0   ; 1a 80
0x01264A  mov.b     @0x400d38, r0l   ; 6a 28 00 40 0d 38
0x012650  mov.l     @0xffdc34, er1   ; 01 00 6b 21 00 ff dc 34
0x012658  add.l     er0, er1   ; 0a 81
0x01265A  mov.l     @0x400d28, er0   ; 01 00 6b 20 00 40 0d 28
0x012662  cmp.l     er0, er1   ; 1f 81
0x012664  bne       0x01274e   ; 58 60 00 e6
0x012668  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x01266E  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x012676  jsr       0x010bd2   ; 5e 01 0b d2
0x01267A  jsr       0x017a7c   ; 5e 01 7a 7c
0x01267E  jsr       0x010bd8   ; 5e 01 0b d8
0x012682  mov.l     @0x400d2c, er0   ; 01 00 6b 20 00 40 0d 2c
0x01268A  mov.l     @0x400d58, er1   ; 01 00 6b 21 00 40 0d 58
0x012692  add.l     er1, er0   ; 0a 90
0x012694  mov.l     er0, @(0xffee,er6)   ; 01 00 6f e0 ff ee
0x01269A  mov.w     #0x0007, r0   ; 79 00 00 07
0x01269E  mov.w     r0, @-sp   ; 6d f0
0x0126A0  mov.l     @(0xffee,er6), er1   ; 01 00 6f 61 ff ee
0x0126A6  mov.l     #0x00019448, er0   ; 7a 00 00 01 94 48
0x0126AC  bsr       0x0128a2   ; 5c 00 01 f2
0x0126B0  adds.l    #2, sp   ; 0b 87
0x0126B2  cmp.b     #0x01, r0l   ; a8 01
0x0126B4  beq       0x0126c4   ; 47 0e
0x0126B6  mov.b     @0x200041, r0l   ; 6a 28 00 20 00 41
0x0126BC  extu.w    r0   ; 17 50
0x0126BE  and.w     #0x0003, r0   ; 79 60 00 03
0x0126C2  bne       0x012714   ; 46 50
0x0126C4  mov.b     @0x004000, r0l   ; 6a 28 00 00 40 00
0x0126CA  mov.b     r0l, @0x400ca0   ; 6a a8 00 40 0c a0
0x0126D0  sub.b     r0l, r0l   ; 18 88
0x0126D2  mov.b     r0l, @0x400ca1   ; 6a a8 00 40 0c a1
0x0126D8  mov.l     #0x00004000, er0   ; 7a 00 00 00 40 00
0x0126DE  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x0126E6  jsr       0x010bd2   ; 5e 01 0b d2
0x0126EA  jsr       0x017a78   ; 5e 01 7a 78
0x0126EE  jsr       0x010bd8   ; 5e 01 0b d8
0x0126F2  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x0126F8  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x012700  mov.b     #0x02, r0l   ; f8 02
0x012702  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x012708  jsr       0x010bd2   ; 5e 01 0b d2
0x01270C  jsr       0x017a7c   ; 5e 01 7a 7c
0x012710  jsr       0x010bd8   ; 5e 01 0b d8
0x012714  mov.w     #0x0060, e0   ; 79 08 00 60
0x012718  mov.b     @0x400508, r0l   ; 6a 28 00 40 05 08
0x01271E  jsr       0x0119a6   ; 5e 01 19 a6
0x012722  sub.b     r0l, r0l   ; 18 88
0x012724  mov.b     r0l, @0x400d3a   ; 6a a8 00 40 0d 3a
0x01272A  mov.w     @0xfffed2, r0   ; 6b 20 00 ff fe d2
0x012730  mov.w     r0, @(0xffec,er6)   ; 6f e0 ff ec
0x012734  mov.w     @(0xffec,er6), r0   ; 6f 60 ff ec
0x012738  and.w     #0xfffc, r0   ; 79 60 ff fc
0x01273C  or.w      #0x0003, r0   ; 79 40 00 03
0x012740  mov.w     r0, @0xfffed2   ; 6b a0 00 ff fe d2
0x012746  mov.b     #0x02, r0l   ; f8 02
0x012748  mov.b     r0l, @0x400d39   ; 6a a8 00 40 0d 39
0x01274E  mov.b     @0x400d39, r0l   ; 6a 28 00 40 0d 39
0x012754  cmp.b     #0x01, r0l   ; a8 01
0x012756  bne       0x0127a2   ; 46 4a
0x012758  sub.l     er0, er0   ; 1a 80
0x01275A  mov.b     @0x400d38, r0l   ; 6a 28 00 40 0d 38
0x012760  mov.l     @0x400d34, er1   ; 01 00 6b 21 00 40 0d 34
0x012768  add.l     er0, er1   ; 0a 81
0x01276A  mov.l     @0x400d24, er0   ; 01 00 6b 20 00 40 0d 24
0x012772  cmp.l     er0, er1   ; 1f 81
0x012774  bne       0x0127a2   ; 46 2c
0x012776  sub.l     er0, er0   ; 1a 80
0x012778  mov.l     er0, @0x400d34   ; 01 00 6b a0 00 40 0d 34
0x012780  sub.b     r0l, r0l   ; 18 88
0x012782  mov.b     r0l, @0x400d39   ; 6a a8 00 40 0d 39
0x012788  mov.l     @0x400d24, er0   ; 01 00 6b 20 00 40 0d 24
0x012790  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x012798  sub.b     r0l, r0l   ; 18 88
0x01279A  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x0127A0  bt        0x0127ee   ; 40 4c
0x0127A2  mov.b     @0x400d38, r0l   ; 6a 28 00 40 0d 38
0x0127A8  cmp.b     #0x80, r0l   ; a8 80
0x0127AA  bne       0x0127ee   ; 46 42
0x0127AC  mov.b     @0x400d39, r0l   ; 6a 28 00 40 0d 39
0x0127B2  bne       0x0127ce   ; 46 1a
0x0127B4  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x0127BA  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x0127C2  jsr       0x010bd2   ; 5e 01 0b d2
0x0127C6  jsr       0x017a7c   ; 5e 01 7a 7c
0x0127CA  jsr       0x010bd8   ; 5e 01 0b d8
0x0127CE  sub.l     er0, er0   ; 1a 80
0x0127D0  mov.b     @0x400d38, r0l   ; 6a 28 00 40 0d 38
0x0127D6  mov.l     #0x00400d34, er1   ; 7a 01 00 40 0d 34
0x0127DC  mov.l     @er1, er2   ; 01 00 69 12
0x0127E0  add.l     er0, er2   ; 0a 82
0x0127E2  mov.l     er2, @er1   ; 01 00 69 92
0x0127E6  sub.b     r0l, r0l   ; 18 88
0x0127E8  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x0127EE  mov.w     @er4, r0   ; 69 40
0x0127F0  mov.w     @(0xfff2,er6), r1   ; 6f 61 ff f2
0x0127F4  cmp.w     r1, r0   ; 1d 10
0x0127F6  bne       0x0125ae   ; 58 60 fd b4
0x0127FA  adds.l    #4, sp   ; 0b 97
0x0127FC  adds.l    #4, sp   ; 0b 97
0x0127FE  ldm.l     @sp+, er4-er5   ; 01 10 6d 75
