0x032814  sub.l     er1, er1
0x032816  mov.b     @er6, r1l
0x032818  mov.l     er1, @(0x18,sp)
0x03281E  shll.l    #2, er1
0x032820  mov.l     @(0x400f32,er1), er1
0x03282A  mov.l     #0x00000008, er0
0x032830  add.l     sp, er0
0x032832  jsr       0x018e68
0x032836  mov.l     @(0x18,sp), er2
0x03283C  shll.l    #2, er2
0x03283E  shll.l    er2
0x032840  add.l     #0x00420108, er2
0x032846  mov.l     er0, er1
0x032848  mov.l     sp, er0
0x03284A  jsr       0x018aa0
0x03284E  jsr       0x01876a
0x032852  mov.l     er0, @er5
0x032856  bne       0x032862
0x032858  mov.l     #0x00000001, er0
0x03285E  mov.l     er0, @er5
0x032862  mov.b     @er6, r1l
0x032864  extu.w    r1
0x032866  mov.w     #0x0006, e1
0x03286A  mulxu.w   e1, er1
0x03286C  add.l     #0x0041ff3e, er1
0x032872  mov.b     @er6, r0l
0x032874  jsr       0x02da8e
0x032878  sub.l     er0, er0
0x03287A  mov.b     @er6, r0l
0x03287C  mov.b     @(0x41ff6e,er0), r0h
0x032884  mov.b     @er6, r0l
0x032886  jsr       0x02daa2
0x03288A  mov.b     r3l, r0h
0x03288C  mov.b     #0x10, r0l
0x03288E  bsr       0x03316c
0x032892  btst      #7, @0x400400
0x03289A  bne       0x0328ee
0x03289C  sub.l     er0, er0
0x03289E  mov.b     @er6, r0l
0x0328A0  mov.l     er0, @(0x18,sp)
0x0328A6  shll.l    #2, er0
0x0328A8  mov.l     @(0x3f156,er0), er0
0x0328B2  mov.l     @(0x18,sp), er1
0x0328B8  mov.b     @(0x440fdc,er1), r1l
0x0328C0  mov.b     r1l, @er0
0x0328C2  mov.w     @0x41ff74, r0
0x0328C8  mov.w     #0x3fff, e0
0x0328CC  mulxu.w   e0, er0
0x0328CE  mov.l     er0, @0x41ffa0
0x0328D6  jsr       0x03d3c2
0x0328DA  mov.b     @er6, r0l
0x0328DC  inc.b     #1, r0l
0x0328DE  mov.b     r0l, @er6
0x0328E0  cmp.b     #0x04, r0l
0x0328E2  bcs       0x032814
0x0328E6  mov.b     #0x01, r0l
0x0328E8  mov.b     r0l, @0x41ffa4
0x0328EE  sub.b     r0l, r0l
0x0328F0  mov.b     r0l, @0x420246
0x0328F6  mov.b     r0l, @0x2001c1
0x0328FC  mov.b     #0x80, r0l
0x0328FE  mov.b     r0l, @0x200001
0x032904  add.l     #0x0000001c, sp
0x03290A  ldm.l     @sp+, er4-er6
0x03290E  ldm.l     @sp+, er2-er3
0x032912  rts       
