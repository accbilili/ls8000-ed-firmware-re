0x027C60  bne       0x027c6a   ; 46 08
0x027C62  mov.b     #0x01, r0l   ; f8 01
0x027C64  bsr       0x027a54   ; 5c 00 fd ec
0x027C68  bt        0x027c80   ; 40 16
0x027C6A  mov.b     @0x4206c8, r0l   ; 6a 28 00 42 06 c8
0x027C70  cmp.b     #0x02, r0l   ; a8 02
0x027C72  beq       0x027c7a   ; 47 06
0x027C74  mov.b     #0x02, r0l   ; f8 02
0x027C76  bsr       0x027a54   ; 5c 00 fd da
0x027C7A  jsr       0x010b56   ; 5e 01 0b 56
0x027C7E  bt        0x027c3a   ; 40 ba
0x027C80  mov.b     @0x4207f9, r0l   ; 6a 28 00 42 07 f9
0x027C86  bne       0x027cb0   ; 46 28
0x027C88  jsr       0x02ccfc   ; 5e 02 cc fc
0x027C8C  bclr      #1, @0xffff2e   ; 6a 38 00 ff ff 2e 72 10
0x027C94  bclr      #1, @0xffff2f   ; 6a 38 00 ff ff 2f 72 10
0x027C9C  mov.w     @er6, r0   ; 69 60
0x027C9E  bne       0x027cb0   ; 46 10
0x027CA0  jsr       0x02b038   ; 5e 02 b0 38
0x027CA4  sub.b     r0l, r0l   ; 18 88
0x027CA6  mov.b     r0l, @0x4207fb   ; 6a a8 00 42 07 fb
0x027CAC  jsr       0x02bcce   ; 5e 02 bc ce
0x027CB0  mov.b     #0x05, r0l   ; f8 05
0x027CB2  mov.b     r0l, @0x400d72   ; 6a a8 00 40 0d 72
0x027CB8  mov.b     #0x10, r0l   ; f8 10
0x027CBA  mov.b     r0l, @0x4003fc   ; 6a a8 00 40 03 fc
0x027CC0  mov.b     @er5, r0l   ; 68 58
0x027CC2  cmp.b     #0x01, r0l   ; a8 01
0x027CC4  beq       0x027dba   ; 58 70 00 f2
0x027CC8  mov.b     @0x41ffa6, r0l   ; 6a 28 00 41 ff a6
0x027CCE  bne       0x027cd8   ; 46 08
0x027CD0  bsr       0x02896c   ; 5c 00 0c 98
0x027CD4  bsr       0x027f44   ; 5c 00 02 6c
0x027CD8  mov.b     @er5, r0l   ; 68 58
0x027CDA  cmp.b     #0x01, r0l   ; a8 01
0x027CDC  beq       0x027dba   ; 58 70 00 da
0x027CE0  jsr       0x03c28e   ; 5e 03 c2 8e
0x027CE4  mov.b     #0x10, r0l   ; f8 10
0x027CE6  mov.b     r0l, @0x4003fc   ; 6a a8 00 40 03 fc
0x027CEC  mov.b     #0x01, r0l   ; f8 01
0x027CEE  mov.b     r0l, @0x41ffa6   ; 6a a8 00 41 ff a6
0x027CF4  mov.b     r0l, @0x4207f9   ; 6a a8 00 42 07 f9
0x027CFA  mov.w     @er6, r0   ; 69 60
0x027CFC  cmp.w     #0x0110, r0   ; 79 20 01 10
0x027D00  beq       0x027d22   ; 47 20
0x027D02  mov.w     @er6, r0   ; 69 60
0x027D04  cmp.w     #0x0120, r0   ; 79 20 01 20
0x027D08  beq       0x027d22   ; 47 18
0x027D0A  mov.w     @er6, r0   ; 69 60
0x027D0C  cmp.w     #0x0121, r0   ; 79 20 01 21
0x027D10  beq       0x027d22   ; 47 10
0x027D12  mov.w     @0x4202b4, r0   ; 6b 20 00 42 02 b4
0x027D18  mov.w     r0, @0x4202b2   ; 6b a0 00 42 02 b2
0x027D1E  jsr       0x02b0e8   ; 5e 02 b0 e8
0x027D22  mov.b     @er5, r0l   ; 68 58
0x027D24  cmp.b     #0x01, r0l   ; a8 01
0x027D26  beq       0x027dba   ; 58 70 00 90
0x027D2A  mov.b     #0x05, r0l   ; f8 05
0x027D2C  mov.b     r0l, @0x400d72   ; 6a a8 00 40 0d 72
0x027D32  bclr      #1, @0xffff2e   ; 6a 38 00 ff ff 2e 72 10
0x027D3A  mov.b     @0x4207fb, r0l   ; 6a 28 00 42 07 fb
