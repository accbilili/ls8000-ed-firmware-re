0x02ED5A  mov.l     er6, @-sp
0x02ED5E  mov.l     sp, er6
0x02ED60  mov.w     r5, @-sp
0x02ED62  mov.b     r0l, r5l
0x02ED64  mov.b     r0h, r5h
0x02ED66  mov.b     r5h, r0h
0x02ED68  mov.b     r5l, r0l
0x02ED6A  bsr       0x02f496
0x02ED6E  mov.b     r5h, r0h
0x02ED70  mov.b     r5l, r0l
0x02ED72  bsr       0x02ed8a
0x02ED74  mov.b     r5h, r0l
0x02ED76  jsr       0x03a18c
0x02ED7A  mov.b     r5h, r0h
0x02ED7C  mov.b     r5l, r0l
0x02ED7E  bsr       0x02ee6e
0x02ED82  mov.w     @sp+, r5
0x02ED84  mov.l     @sp+, er6
0x02ED88  rts       
