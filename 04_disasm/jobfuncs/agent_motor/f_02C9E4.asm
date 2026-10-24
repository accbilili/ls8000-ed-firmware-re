0x02C9E4  stm.l     er2-er3, @-sp
0x02C9E8  stm.l     er4-er6, @-sp
0x02C9EC  mov.l     #0x00440fda, er6
0x02C9F2  mov.w     r0, r5
0x02C9F4  mov.l     er1, er2
0x02C9F6  cmp.w     #0x0f60, r5
0x02C9FA  bls       0x02ca04
0x02C9FC  mov.w     #0x0f60, r0
0x02CA00  mov.w     r0, @er6
0x02CA02  bt        0x02ca06
0x02CA04  mov.w     r5, @er6
0x02CA06  mov.l     #0x004202ec, er5
0x02CA0C  mov.w     @er6, r0
0x02CA0E  mov.w     @er5, r1
0x02CA10  cmp.w     r1, r0
0x02CA12  beq       0x02ca6e
0x02CA14  mov.w     @er6, r0
0x02CA16  mov.w     @er5, r1
0x02CA18  cmp.w     r1, r0
0x02CA1A  bls       0x02ca38
0x02CA1C  sub.b     r4l, r4l
0x02CA1E  mov.w     @er6, r0
0x02CA20  mov.w     @er5, r5
0x02CA22  sub.w     r5, r0
0x02CA24  mov.w     r0, r5
0x02CA26  cmp.w     #0x012f, r0
0x02CA2A  bcs       0x02ca32
0x02CA2C  mov.w     #0x02bc, e5
0x02CA30  bt        0x02ca50
0x02CA32  mov.w     #0x0190, e5
0x02CA36  bt        0x02ca50
0x02CA38  mov.b     #0x01, r4l
0x02CA3A  mov.w     @er5, r5
0x02CA3C  mov.w     @er6, r0
0x02CA3E  sub.w     r0, r5
0x02CA40  cmp.w     #0x012f, r5
0x02CA44  bcs       0x02ca4c
0x02CA46  mov.w     #0x02bc, e5
0x02CA4A  bt        0x02ca50
0x02CA4C  mov.w     #0x0190, e5
0x02CA50  sub.l     er3, er3
0x02CA52  mov.l     er2, er0
0x02CA54  mov.l     er0, @-sp
0x02CA58  mov.l     er3, @-sp
0x02CA5C  mov.b     @(0x21,sp), r0h
0x02CA60  mov.w     e5, r1
0x02CA62  mov.w     r5, e0
0x02CA64  mov.b     r4l, r0l
0x02CA66  bsr       0x02be32
0x02CA6A  adds.l    #4, sp
0x02CA6C  adds.l    #4, sp
0x02CA6E  ldm.l     @sp+, er4-er6
0x02CA72  ldm.l     @sp+, er2-er3
0x02CA76  rts       
