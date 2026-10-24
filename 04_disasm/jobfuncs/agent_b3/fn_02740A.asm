0x02740A  mov.l     er3, @-sp   ; 01 00 6d f3
0x02740E  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x027412  mov.l     #0x00400400, er3   ; 7a 03 00 40 04 00
0x027418  mov.l     #0x00400404, er5   ; 7a 05 00 40 04 04
0x02741E  mov.l     #0x00400406, er6   ; 7a 06 00 40 04 06
0x027424  mov.b     @0x4207f8, r0l   ; 6a 28 00 42 07 f8
0x02742A  cmp.b     #0x01, r0l   ; a8 01
0x02742C  beq       0x0274b0   ; 58 70 00 80
0x027430  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x027436  cmp.w     #0x0010, r0   ; 79 20 00 10
0x02743A  bne       0x02744e   ; 46 12
0x02743C  mov.w     #0x2000, r0   ; 79 00 20 00
0x027440  mov.w     r0, @er5   ; 69 d0
0x027442  mov.b     #0x02, r0l   ; f8 02
0x027444  bsr       0x027a54   ; 5c 00 06 0c
0x027448  jsr       0x010b56   ; 5e 01 0b 56
0x02744C  bt        0x027448   ; 40 fa
0x02744E  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x027454  bne       0x02747a   ; 46 24
0x027456  mov.b     @0x420245, r0l   ; 6a 28 00 42 02 45
0x02745C  cmp.b     #0x01, r0l   ; a8 01
0x02745E  beq       0x027470   ; 47 10
0x027460  jsr       0x02dc38   ; 5e 02 dc 38
0x027464  jsr       0x02ed14   ; 5e 02 ed 14
0x027468  mov.b     #0x01, r0l   ; f8 01
0x02746A  mov.b     r0l, @0x420245   ; 6a a8 00 42 02 45
0x027470  bsr       0x027b1e   ; 5c 00 06 aa
0x027474  bsr       0x027afa   ; 5c 00 06 82
0x027478  bt        0x0274b4   ; 40 3a
0x02747A  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x027480  cmp.b     #0x01, r0l   ; a8 01
0x027482  beq       0x027488   ; 47 04
0x027484  cmp.b     #0x05, r0l   ; a8 05
0x027486  bne       0x0274b4   ; 46 2c
0x027488  jsr       0x0208c2   ; 5e 02 08 c2
0x02748C  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x027492  cmp.w     #0x0010, r0   ; 79 20 00 10
0x027496  bne       0x0274aa   ; 46 12
0x027498  mov.w     #0x2000, r0   ; 79 00 20 00
0x02749C  mov.w     r0, @er5   ; 69 d0
0x02749E  mov.b     #0x02, r0l   ; f8 02
0x0274A0  bsr       0x027a54   ; 5c 00 05 b0
0x0274A4  jsr       0x010b56   ; 5e 01 0b 56
0x0274A8  bt        0x0274a4   ; 40 fa
0x0274AA  jsr       0x03a130   ; 5e 03 a1 30
0x0274AE  bt        0x0274b4   ; 40 04
0x0274B0  bsr       0x0283dc   ; 5c 00 0f 28
0x0274B4  mov.w     @er6, r0   ; 69 60
0x0274B6  and.w     #0xff00, r0   ; 79 60 ff 00
0x0274BA  bset      #0, r0l   ; 70 08
0x0274BC  mov.w     r0, @er6   ; 69 e0
0x0274BE  mov.b     #0x01, r0l   ; f8 01
0x0274C0  mov.b     r0l, @0x4207f8   ; 6a a8 00 42 07 f8
0x0274C6  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x0274CC  beq       0x0274d8   ; 47 0a
0x0274CE  mov.b     #0xff, r0l   ; f8 ff
0x0274D0  mov.b     r0l, @0x200042   ; 6a a8 00 20 00 42
0x0274D6  bt        0x027526   ; 40 4e
0x0274D8  mov.w     @er5, r0   ; 69 50
0x0274DA  cmp.w     #0x2000, r0   ; 79 20 20 00
0x0274DE  beq       0x0274ea   ; 47 0a
0x0274E0  mov.b     @0x40041c, r0l   ; 6a 28 00 40 04 1c
0x0274E6  cmp.b     #0x01, r0l   ; a8 01
0x0274E8  bne       0x027526   ; 46 3c
0x0274EA  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x0274F0  cmp.w     #0x0110, r0   ; 79 20 01 10
0x0274F4  beq       0x027518   ; 47 22
0x0274F6  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x0274FC  cmp.w     #0x0120, r0   ; 79 20 01 20
0x027500  beq       0x027518   ; 47 16
0x027502  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x027508  cmp.w     #0x0121, r0   ; 79 20 01 21
0x02750C  beq       0x027518   ; 47 0a
0x02750E  mov.b     @0x40041c, r0l   ; 6a 28 00 40 04 1c
0x027514  cmp.b     #0x01, r0l   ; a8 01
0x027516  bne       0x027526   ; 46 0e
0x027518  bclr      #1, @0xffff2e   ; 6a 38 00 ff ff 2e 72 10
0x027520  jsr       0x010b56   ; 5e 01 0b 56
0x027524  bt        0x027520   ; 40 fa
0x027526  mov.w     @0x4202a2, r0   ; 6b 20 00 42 02 a2
0x02752C  mov.w     r0, @0x4202b2   ; 6b a0 00 42 02 b2
0x027532  mov.w     @0x4202ec, r0   ; 6b 20 00 42 02 ec
0x027538  mov.w     r0, @0x4202fc   ; 6b a0 00 42 02 fc
0x02753E  mov.b     @0x40041c, r0l   ; 6a 28 00 40 04 1c
0x027544  cmp.b     #0x01, r0l   ; a8 01
0x027546  bne       0x027556   ; 46 0e
0x027548  bclr      #1, @0xffff2e   ; 6a 38 00 ff ff 2e 72 10
0x027550  jsr       0x010b56   ; 5e 01 0b 56
0x027554  bt        0x027550   ; 40 fa
0x027556  mov.b     @0x4206ec, r0l   ; 6a 28 00 42 06 ec
0x02755C  bne       0x0275b4   ; 46 56
0x02755E  bsr       0x027676   ; 5c 00 01 14
0x027562  mov.w     @er5, r0   ; 69 50
0x027564  cmp.w     #0x0e10, r0   ; 79 20 0e 10
0x027568  beq       0x0275b8   ; 47 4e
0x02756A  mov.w     @er5, r0   ; 69 50
0x02756C  cmp.w     #0x3000, r0   ; 79 20 30 00
0x027570  beq       0x0275b8   ; 47 46
0x027572  mov.w     @er5, r0   ; 69 50
0x027574  cmp.w     #0x2000, r0   ; 79 20 20 00
0x027578  beq       0x0275b8   ; 47 3e
0x02757A  mov.b     @0x400d72, r0l   ; 6a 28 00 40 0d 72
0x027580  cmp.b     #0x01, r0l   ; a8 01
0x027582  beq       0x02758c   ; 47 08
0x027584  mov.w     #0x9000, r0   ; 79 00 90 00
0x027588  mov.w     r0, @er5   ; 69 d0
0x02758A  bt        0x0275b8   ; 40 2c
0x02758C  mov.b     @0x400d79, r0l   ; 6a 28 00 40 0d 79
0x027592  cmp.b     #0x01, r0l   ; a8 01
0x027594  beq       0x02759e   ; 47 08
0x027596  mov.w     #0x5000, r0   ; 79 00 50 00
0x02759A  mov.w     r0, @er5   ; 69 d0
0x02759C  bt        0x0275b2   ; 40 14
0x02759E  mov.b     @0x4003fb, r0l   ; 6a 28 00 40 03 fb
0x0275A4  cmp.b     #0x10, r0l   ; a8 10
0x0275A6  bne       0x0275ae   ; 46 06
0x0275A8  mov.w     #0x1100, r0   ; 79 00 11 00
0x0275AC  bt        0x0275b0   ; 40 02
0x0275AE  sub.w     r0, r0   ; 19 00
0x0275B0  mov.w     r0, @er5   ; 69 d0
0x0275B2  bt        0x0275b8   ; 40 04
0x0275B4  jsr       0x03c31e   ; 5e 03 c3 1e
0x0275B8  btst      #6, @er3   ; 7c 30 73 60
0x0275BC  beq       0x027668   ; 58 70 00 a8
