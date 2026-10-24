0x010B56  stm.l     er4-er6, @-sp
0x010B5A  mov.l     #0x00400d5c, er5
0x010B60  mov.l     #0x00ffff2e, er6
0x010B66  mov.w     @0x4003ec, r0
0x010B6C  beq       0x010b72
0x010B6E  jmp       0x010bb2
0x010B72  mov.b     @er5, r0l
0x010B74  cmp.b     #0x01, r0l
0x010B76  beq       0x010b7c
0x010B78  jmp       0x010b8e
0x010B7C  sub.b     r0l, r0l
0x010B7E  mov.b     r0l, @er5
0x010B80  mov.b     @0x400515, r0l
0x010B86  and.b     #0x10, r0l
0x010B88  mov.b     @er6, r1l
0x010B8A  or.b      r0l, r1l
0x010B8C  mov.b     r1l, @er6
0x010B8E  jsr       0x010bce
0x010B92  mov.b     @er5, r0l
0x010B94  cmp.b     #0x01, r0l
0x010B96  beq       0x010b9c
0x010B98  jmp       0x010bc8
0x010B9C  sub.b     r0l, r0l
0x010B9E  mov.b     r0l, @er5
0x010BA0  mov.b     @0x400515, r0l
0x010BA6  and.b     #0x10, r0l
0x010BA8  mov.b     @er6, r1l
0x010BAA  or.b      r0l, r1l
0x010BAC  mov.b     r1l, @er6
0x010BAE  jmp       0x010bc8
0x010BB2  mov.b     @er6, r4l
0x010BB4  mov.b     r4l, r0l
0x010BB6  and.b     #0xbe, r0l
0x010BB8  mov.b     r0l, @er6
0x010BBA  jsr       0x010bce
0x010BBE  mov.b     @er6, r0l
0x010BC0  and.b     #0xbe, r0l
0x010BC2  and.b     #0x41, r4l
0x010BC4  or.b      r4l, r0l
0x010BC6  mov.b     r0l, @er6
0x010BC8  ldm.l     @sp+, er4-er6
0x010BCC  rts       
