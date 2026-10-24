0x017A80  mov.l     er0, @-sp   ; 01 00 6d f0
0x017A84  mov.l     er1, @-sp   ; 01 00 6d f1
0x017A88  mov.l     er2, @-sp   ; 01 00 6d f2
0x017A8C  mov.l     #0x00017ab4, er0   ; 7a 00 00 01 7a b4
0x017A92  mov.l     #0x00400f5a, er1   ; 7a 01 00 40 0f 5a
0x017A98  mov.w     @er0+, r2   ; 6d 02
0x017A9A  mov.w     r2, @er1   ; 69 92
0x017A9C  inc.l     #2, er1   ; 0b f1
0x017A9E  cmp.l     #0x00017f04, er0   ; 7a 20 00 01 7f 04
0x017AA4  bcs       0x017a98   ; 45 f2
0x017AA6  mov.l     @sp+, er2   ; 01 00 6d 72
0x017AAA  mov.l     @sp+, er1   ; 01 00 6d 71
0x017AAE  mov.l     @sp+, er0   ; 01 00 6d 70
0x017AB2  rts          ; 54 70
