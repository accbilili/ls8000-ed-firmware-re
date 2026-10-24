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
