0x02BCCE  mov.l     er6, @-sp   ; 01 00 6d f6
0x02BCD2  mov.l     #0x00ffff48, er0   ; 7a 00 00 ff ff 48
0x02BCD8  mov.w     @er0, r1   ; 69 01
0x02BCDA  or.w      #0xf000, r1   ; 79 41 f0 00
0x02BCDE  mov.w     r1, @er0   ; 69 81
0x02BCE0  mov.b     @0x03f0f9, r0l   ; 6a 28 00 03 f0 f9
0x02BCE6  mov.b     r0l, @0x440e50   ; 6a a8 00 44 0e 50
0x02BCEC  bsr       0x02baa6   ; 5c 00 fd b6
0x02BCF0  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x02BCF6  cmp.w     #0x0120, r0   ; 79 20 01 20
0x02BCFA  beq       0x02bd60   ; 47 64
0x02BCFC  mov.w     @0x400402, r0   ; 6b 20 00 40 04 02
0x02BD02  cmp.w     #0x0121, r0   ; 79 20 01 21
0x02BD06  beq       0x02bd60   ; 47 58
0x02BD08  mov.b     @0x00600d, r0l   ; 6a 28 00 00 60 0d
0x02BD0E  bne       0x02bd40   ; 46 30
0x02BD10  mov.l     @0x006000, er0   ; 01 00 6b 20 00 00 60 00
0x02BD18  cmp.l     #0xfffffed4, er0   ; 7a 20 ff ff fe d4
0x02BD1E  blt       0x02bd40   ; 4d 20
0x02BD20  mov.l     @0x006000, er0   ; 01 00 6b 20 00 00 60 00
0x02BD28  cmp.l     #0x0000012c, er0   ; 7a 20 00 00 01 2c
0x02BD2E  bgt       0x02bd40   ; 4e 10
0x02BD30  mov.l     @0x006000, er6   ; 01 00 6b 26 00 00 60 00
0x02BD38  add.l     #0x0000014d, er6   ; 7a 16 00 00 01 4d
0x02BD3E  bt        0x02bd46   ; 40 06
0x02BD40  mov.l     #0x0000014d, er6   ; 7a 06 00 00 01 4d
0x02BD46  sub.b     r1l, r1l   ; 18 99
0x02BD48  mov.w     #0x0064, e0   ; 79 08 00 64
0x02BD4C  mov.w     r6, r0   ; 0d 60
0x02BD4E  bsr       0x02b8ea   ; 5c 00 fb 98
0x02BD52  bsr       0x02b82a   ; 5c 00 fa d4
0x02BD56  mov.w     #0x00e2, r0   ; 79 00 00 e2
0x02BD5A  mov.w     r0, @0x4202e0   ; 6b a0 00 42 02 e0
0x02BD60  mov.l     @sp+, er6   ; 01 00 6d 76
0x02BD64  rts          ; 54 70
