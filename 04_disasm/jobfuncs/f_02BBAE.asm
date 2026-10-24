0x02BBAE  stm.l     er4-er6, @-sp
0x02BBB2  mov.l     #0x00400ca0, er6
0x02BBB8  jsr       0x017a80
0x02BBBC  jsr       0x016e8e
0x02BBC0  mov.l     #0x00400408, er5
0x02BBC6  mov.w     @er5, r0
0x02BBC8  sub.w     e0, e0
0x02BBCA  mov.b     r0h, r0l
0x02BBCC  sub.b     r0h, r0h
0x02BBCE  mov.b     r0l, @er6
0x02BBD0  mov.w     @er5, r0
0x02BBD2  mov.b     r0l, @(0x1,er6)
0x02BBD6  mov.b     @(0x2,er5), r0l
0x02BBDA  sub.b     r0h, r0h
0x02BBDC  mov.b     r0l, @(0x2,er6)
0x02BBE0  mov.b     @(0x3,er5), r5l
0x02BBE4  mov.b     r5l, @(0x3,er6)
0x02BBE8  mov.l     #0x0040040c, er5
0x02BBEE  mov.w     @er5, r0
0x02BBF0  sub.w     e0, e0
0x02BBF2  mov.b     r0h, r0l
0x02BBF4  sub.b     r0h, r0h
0x02BBF6  mov.b     r0l, @(0x4,er6)
0x02BBFA  mov.w     @er5, r0
0x02BBFC  mov.b     r0l, @(0x5,er6)
0x02BC00  mov.b     @(0x2,er5), r0l
0x02BC04  sub.b     r0h, r0h
0x02BC06  mov.b     r0l, @(0x6,er6)
0x02BC0A  mov.b     @(0x3,er5), r5l
0x02BC0E  mov.b     r5l, @(0x7,er6)
0x02BC12  mov.b     @0x400410, r0l
0x02BC18  mov.b     r0l, @(0x8,er6)
0x02BC1C  mov.b     @0x400411, r0l
0x02BC22  mov.b     r0l, @(0x9,er6)
0x02BC26  mov.b     @0x400413, r0l
0x02BC2C  mov.b     r0l, @(0xa,er6)
0x02BC30  mov.b     @0x400414, r0l
0x02BC36  mov.b     r0l, @(0xb,er6)
0x02BC3A  mov.b     @0x400412, r0l
0x02BC40  mov.b     r0l, @(0xc,er6)
0x02BC44  sub.b     r0l, r0l
0x02BC46  mov.b     r0l, @(0xd,er6)
0x02BC4A  mov.b     #0xff, r0l
0x02BC4C  mov.b     r0l, @(0xe,er6)
0x02BC50  mov.b     r0l, @(0xf,er6)
0x02BC54  mov.l     #0x00006010, er4
0x02BC5A  sub.b     r5l, r5l
0x02BC5C  mov.b     @er4+, r0l
0x02BC5E  mov.b     r5l, r1l
0x02BC60  extu.w    r1
0x02BC62  add.w     #0x0010, r1
0x02BC66  exts.l    er1
0x02BC68  add.l     er6, er1
0x02BC6A  mov.b     r0l, @er1
0x02BC6C  inc.b     #1, r5l
0x02BC6E  cmp.b     #0x11, r5l
0x02BC70  bcs       0x02bc5c
0x02BC72  mov.l     #0x00006000, er0
0x02BC78  mov.l     er0, @0xffdc34
0x02BC80  jsr       0x010bd2
0x02BC84  mov.l     #0x00fffed2, er5
0x02BC8A  mov.w     @er5, r4
0x02BC8C  and.w     #0xfffc, r4
0x02BC90  or.w      #0x0003, r4
0x02BC94  mov.w     r4, @er5
0x02BC96  jsr       0x017a78
0x02BC9A  jsr       0x010bd8
0x02BC9E  mov.b     #0x21, r0l
0x02BCA0  mov.b     r0l, @0x400d38
0x02BCA6  mov.l     er6, @0xffdc30
0x02BCAE  jsr       0x010bd2
0x02BCB2  jsr       0x017a7c
0x02BCB6  mov.w     @er5, r4
0x02BCB8  and.w     #0xfffc, r4
0x02BCBC  or.w      #0x0003, r4
0x02BCC0  mov.w     r4, @er5
0x02BCC2  jsr       0x010bd8
0x02BCC6  bsr       0x02bcce
0x02BCC8  ldm.l     @sp+, er4-er6
0x02BCCC  rts       
