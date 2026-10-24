0x016D60  .byte 0x00
0x016D61  bcc       0x016cfd   ; 44 9a
0x016D63  xor.b     #0x01, r6h   ; d6 01
0x016D65  .byte 0x00
0x016D66  mov.w     r0, @0x449acc   ; 6b a0 00 44 9a cc
0x016D6C  mov.l     er5, @0x449ac8   ; 01 00 6b a5 00 44 9a c8
0x016D74  mov.w     @0x400406, r0   ; 6b 20 00 40 04 06
0x016D7A  and.w     #0x00ff, r0   ; 79 60 00 ff
0x016D7E  beq       0x016d84   ; 47 04
0x016D80  bsr       0x016e8e   ; 5c 00 01 0a
0x016D84  jsr       0x0176d6   ; 5e 01 76 d6
0x016D88  jsr       0x010bd2   ; 5e 01 0b d2
0x016D8C  mov.w     @0xfffed2, r0   ; 6b 20 00 ff fe d2
0x016D92  mov.w     r0, @(0xfff6,er6)   ; 6f e0 ff f6
0x016D96  mov.w     @(0xfff6,er6), r0   ; 6f 60 ff f6
0x016D9A  and.w     #0xfffc, r0   ; 79 60 ff fc
0x016D9E  or.w      #0x0003, r0   ; 79 40 00 03
0x016DA2  mov.w     r0, @0xfffed2   ; 6b a0 00 ff fe d2
0x016DA8  jsr       0x0176d2   ; 5e 01 76 d2
0x016DAC  mov.w     @0xfffed2, r0   ; 6b 20 00 ff fe d2
0x016DB2  mov.w     r0, @(0xfff6,er6)   ; 6f e0 ff f6
0x016DB6  mov.w     @(0xfff6,er6), r0   ; 6f 60 ff f6
0x016DBA  and.w     #0xfffc, r0   ; 79 60 ff fc
0x016DBE  or.w      #0x0003, r0   ; 79 40 00 03
0x016DC2  mov.w     r0, @0xfffed2   ; 6b a0 00 ff fe d2
0x016DC8  jsr       0x010bd8   ; 5e 01 0b d8
0x016DCC  mov.w     #0x5a00, r0   ; 79 00 5a 00
0x016DD0  mov.w     r0, @0xffffbc   ; 6b a0 00 ff ff bc
0x016DD6  mov.l     @0x449ad6, er0   ; 01 00 6b 20 00 44 9a d6
0x016DDE  mov.l     er0, @0x449ad0   ; 01 00 6b a0 00 44 9a d0
0x016DE6  mov.l     #0x00449ad6, er0   ; 7a 00 00 44 9a d6
0x016DEC  mov.l     @er0, er1   ; 01 00 69 01
0x016DF0  add.l     #0x00000020, er1   ; 7a 11 00 00 00 20
0x016DF6  mov.l     er1, @er0   ; 01 00 69 81
0x016DFA  add.l     #0x0000000a, sp   ; 7a 17 00 00 00 0a
0x016E00  mov.l     @sp+, er5   ; 01 00 6d 75
0x016E04  mov.l     @sp+, er6   ; 01 00 6d 76
0x016E08  rts          ; 54 70
0x016E0A  mov.l     er6, @-sp   ; 01 00 6d f6
0x016E0E  mov.l     sp, er6   ; 0f f6
0x016E10  mov.l     @0x449ad0, er0   ; 01 00 6b 20 00 44 9a d0
0x016E18  cmp.l     #0x00070000, er0   ; 7a 20 00 07 00 00
0x016E1E  bcc       0x016e2c   ; 44 0c
0x016E20  mov.l     #0x00070000, er0   ; 7a 00 00 07 00 00
0x016E26  bsr       0x016ec4   ; 5c 00 00 9a
0x016E2A  bt        0x016e36   ; 40 0a
0x016E2C  mov.l     #0x00060000, er0   ; 7a 00 00 06 00 00
0x016E32  bsr       0x016ec4   ; 5c 00 00 8e
0x016E36  mov.l     @sp+, er6   ; 01 00 6d 76
0x016E3A  rts          ; 54 70
0x016E3C  mov.l     er6, @-sp   ; 01 00 6d f6
0x016E40  mov.l     sp, er6   ; 0f f6
0x016E42  subs.l    #2, sp   ; 1b 87
0x016E44  mov.l     #0x00060000, er0   ; 7a 00 00 06 00 00
0x016E4A  bsr       0x016ec4   ; 55 78
0x016E4C  mov.l     #0x00070000, er0   ; 7a 00 00 07 00 00
0x016E52  bsr       0x016ec4   ; 55 70
0x016E54  sub.w     r0, r0   ; 19 00
0x016E56  mov.w     r0, @0x449ad4   ; 6b a0 00 44 9a d4
0x016E5C  mov.l     #0x00060000, er0   ; 7a 00 00 06 00 00
0x016E62  mov.l     er0, @0x449ad6   ; 01 00 6b a0 00 44 9a d6
0x016E6A  mov.l     @0x449ad6, er0   ; 01 00 6b 20 00 44 9a d6
0x016E72  mov.l     er0, @0x449ad0   ; 01 00 6b a0 00 44 9a d0
0x016E7A  mov.b     #0x01, r0l   ; f8 01
0x016E7C  mov.b     r0l, @0x449ada   ; 6a a8 00 44 9a da
0x016E82  bsr       0x01680a   ; 5c 00 f9 84
0x016E86  adds.l    #2, sp   ; 0b 87
0x016E88  mov.l     @sp+, er6   ; 01 00 6d 76
0x016E8C  rts          ; 54 70
0x016E8E  mov.l     er6, @-sp   ; 01 00 6d f6
0x016E92  mov.l     sp, er6   ; 0f f6
0x016E94  mov.b     @0x4202a4, r0l   ; 6a 28 00 42 02 a4
0x016E9A  beq       0x016ebe   ; 47 22
0x016E9C  bt        0x016ebc   ; 40 1e
0x016E9E  mov.w     @0x400406, r0   ; 6b 20 00 40 04 06
0x016EA4  and.w     #0x00ff, r0   ; 79 60 00 ff
0x016EA8  cmp.w     #0x00f3, r0   ; 79 20 00 f3
0x016EAC  beq       0x016eb8   ; 47 0a
0x016EAE  mov.b     @0x4202a4, r0l   ; 6a 28 00 42 02 a4
0x016EB4  bne       0x016eb8   ; 46 02
0x016EB6  bt        0x016ebe   ; 40 06
0x016EB8  jsr       0x010b56   ; 5e 01 0b 56
0x016EBC  bt        0x016e9e   ; 40 e0
0x016EBE  mov.l     @sp+, er6   ; 01 00 6d 76
0x016EC2  rts          ; 54 70
0x016EC4  mov.l     er6, @-sp   ; 01 00 6d f6
0x016EC8  mov.l     sp, er6   ; 0f f6
0x016ECA  mov.l     er5, @-sp   ; 01 00 6d f5
0x016ECE  subs.l    #2, sp   ; 1b 87
0x016ED0  mov.l     er0, er5   ; 0f 85
0x016ED2  bsr       0x016e8e   ; 55 ba
0x016ED4  mov.b     #0x01, r0l   ; f8 01
0x016ED6  mov.b     r0l, @0x449ac6   ; 6a a8 00 44 9a c6
0x016EDC  mov.l     er5, @0x449acc   ; 01 00 6b a5 00 44 9a cc
0x016EE4  jsr       0x0176d6   ; 5e 01 76 d6
0x016EE8  jsr       0x010bd2   ; 5e 01 0b d2
0x016EEC  mov.w     @0xfffed2, r0   ; 6b 20 00 ff fe d2
0x016EF2  mov.w     r0, @(0xfffa,er6)   ; 6f e0 ff fa
0x016EF6  mov.w     @(0xfffa,er6), r0   ; 6f 60 ff fa
0x016EFA  and.w     #0xfffc, r0   ; 79 60 ff fc
0x016EFE  or.w      #0x0003, r0   ; 79 40 00 03
0x016F02  mov.w     r0, @0xfffed2   ; 6b a0 00 ff fe d2
0x016F08  jsr       0x0176ce   ; 5e 01 76 ce
0x016F0C  mov.w     @0xfffed2, r0   ; 6b 20 00 ff fe d2
0x016F12  mov.w     r0, @(0xfffa,er6)   ; 6f e0 ff fa
0x016F16  mov.w     @(0xfffa,er6), r0   ; 6f 60 ff fa
0x016F1A  and.w     #0xfffc, r0   ; 79 60 ff fc
0x016F1E  or.w      #0x0003, r0   ; 79 40 00 03
0x016F22  mov.w     r0, @0xfffed2   ; 6b a0 00 ff fe d2
0x016F28  jsr       0x010bd8   ; 5e 01 0b d8
0x016F2C  mov.l     #0x00449ad4, er0   ; 7a 00 00 44 9a d4
0x016F32  mov.w     @er0, r1   ; 69 01
0x016F34  sub.w     #0x0800, r1   ; 79 31 08 00
0x016F38  mov.w     r1, @er0   ; 69 81
0x016F3A  adds.l    #2, sp   ; 0b 87
0x016F3C  mov.l     @sp+, er5   ; 01 00 6d 75
