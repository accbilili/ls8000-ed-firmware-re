0x010B56  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x010B5A  mov.l     #0x00400d5c, er5   ; 7a 05 00 40 0d 5c
0x010B60  mov.l     #0x00ffff2e, er6   ; 7a 06 00 ff ff 2e
0x010B66  mov.w     @0x4003ec, r0   ; 6b 20 00 40 03 ec
0x010B6C  beq       0x010b72   ; 47 04
0x010B6E  jmp       0x010bb2   ; 5a 01 0b b2
0x010B72  mov.b     @er5, r0l   ; 68 58
0x010B74  cmp.b     #0x01, r0l   ; a8 01
0x010B76  beq       0x010b7c   ; 47 04
0x010B78  jmp       0x010b8e   ; 5a 01 0b 8e
0x010B7C  sub.b     r0l, r0l   ; 18 88
0x010B7E  mov.b     r0l, @er5   ; 68 d8
0x010B80  mov.b     @0x400515, r0l   ; 6a 28 00 40 05 15
0x010B86  and.b     #0x10, r0l   ; e8 10
0x010B88  mov.b     @er6, r1l   ; 68 69
0x010B8A  or.b      r0l, r1l   ; 14 89
0x010B8C  mov.b     r1l, @er6   ; 68 e9
0x010B8E  jsr       0x010bce   ; 5e 01 0b ce
0x010B92  mov.b     @er5, r0l   ; 68 58
0x010B94  cmp.b     #0x01, r0l   ; a8 01
0x010B96  beq       0x010b9c   ; 47 04
0x010B98  jmp       0x010bc8   ; 5a 01 0b c8
0x010B9C  sub.b     r0l, r0l   ; 18 88
0x010B9E  mov.b     r0l, @er5   ; 68 d8
0x010BA0  mov.b     @0x400515, r0l   ; 6a 28 00 40 05 15
0x010BA6  and.b     #0x10, r0l   ; e8 10
0x010BA8  mov.b     @er6, r1l   ; 68 69
0x010BAA  or.b      r0l, r1l   ; 14 89
0x010BAC  mov.b     r1l, @er6   ; 68 e9
0x010BAE  jmp       0x010bc8   ; 5a 01 0b c8
0x010BB2  mov.b     @er6, r4l   ; 68 6c
0x010BB4  mov.b     r4l, r0l   ; 0c c8
0x010BB6  and.b     #0xbe, r0l   ; e8 be
0x010BB8  mov.b     r0l, @er6   ; 68 e8
0x010BBA  jsr       0x010bce   ; 5e 01 0b ce
0x010BBE  mov.b     @er6, r0l   ; 68 68
0x010BC0  and.b     #0xbe, r0l   ; e8 be
0x010BC2  and.b     #0x41, r4l   ; ec 41
0x010BC4  or.b      r4l, r0l   ; 14 c8
0x010BC6  mov.b     r0l, @er6   ; 68 e8
0x010BC8  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x010BCC  rts          ; 54 70
