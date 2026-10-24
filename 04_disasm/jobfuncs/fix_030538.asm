0x030442  sub.l     er0, er0
0x030444  mov.b     @er5, r0l
0x030446  mov.b     @(0x41ff6e,er0), r0h
0x03044E  mov.b     @er5, r0l
0x030450  jsr       0x02daa2
0x030454  bsr       0x032d2c
0x030458  mov.b     #0x02, r0h
0x03045A  mov.b     #0x08, r0l
0x03045C  bsr       0x0331f8
0x030460  mov.b     #0x01, r6h
0x030462  sub.b     r0l, r0l
0x030464  mov.b     r0l, @er4
0x030466  sub.b     r6l, r6l
0x030468  bt        0x0304d2
0x03046A  mov.b     r6l, r0l
0x03046C  extu.w    r0
0x03046E  extu.l    er0
0x030470  shll.l    #2, er0
0x030472  mov.l     @(0x420224,er0), er1
0x03047C  bne       0x030480
0x03047E  sub.b     r6h, r6h
0x030480  mov.b     r6l, r3l
0x030482  extu.w    r3
0x030484  extu.l    er3
0x030486  shll.l    #2, er3
0x030488  mov.w     @0x400d6a, r1
0x03048E  extu.l    er1
0x030490  mov.w     #0x0003, r0
0x030494  divxu.w   r0, er1
0x030496  extu.l    er1
0x030498  mov.l     @(0x420218,er3), er0
0x0304A2  jsr       0x01872e
0x0304A6  mov.l     @(0x420230,er3), er1
0x0304B0  sub.l     er0, er1
0x0304B2  cmp.l     #0x00000200, er1
0x0304B8  bcs       0x0304d0
0x0304BA  mov.b     r6l, r0l
0x0304BC  extu.w    r0
0x0304BE  mov.w     #0x0080, r1
0x0304C2  dec.b     #1, r0l
0x0304C4  bmi       0x0304ca
0x0304C6  shar.w    r1
0x0304C8  bt        0x0304c2
0x0304CA  mov.b     @er4, r0l
0x0304CC  or.b      r1l, r0l
0x0304CE  mov.b     r0l, @er4
0x0304D0  inc.b     #1, r6l
0x0304D2  cmp.b     #0x03, r6l
0x0304D4  bcs       0x03046a
0x0304D6  mov.b     @er4, r0l
0x0304D8  and.b     #0xe0, r0l
0x0304DA  bne       0x030516
0x0304DC  mov.w     @0x41ffb2, r0
0x0304E2  extu.l    er0
0x0304E4  sub.l     er1, er1
0x0304E6  mov.b     @er5, r1l
0x0304E8  jsr       0x018e1e
0x0304EC  mov.w     @0x400d6c, r6
0x0304F2  extu.l    er6
0x0304F4  add.l     er0, er6
0x0304F6  shll.l    er6
0x0304F8  mov.l     @0x41ffae, er0
0x030500  add.l     er0, er6
0x030502  mov.w     @0x400d6a, e1
0x030508  sub.w     r1, r1
0x03050A  mov.l     er6, er0
0x03050C  bsr       0x0337a2
0x030510  bsr       0x0337fe
0x030514  bt        0x030534
0x030516  mov.b     #0x01, r0h
0x030518  mov.b     #0x18, r0l
0x03051A  bsr       0x0331f8
0x03051E  btst      #7, @0x400400
0x030526  bne       0x030540
0x030528  jsr       0x010b56
0x03052C  jsr       0x03db20
0x030530  jsr       0x010b56
0x030534  mov.b     @er5, r0l
0x030536  inc.b     #1, r0l
0x030538  mov.b     r0l, @er5
0x03053A  cmp.b     #0x04, r0l
0x03053C  bcs       0x030442
0x030540  sub.b     r0l, r0l
0x030542  mov.b     r0l, @0x2001c1
0x030548  mov.b     #0x80, r0l
0x03054A  mov.b     r0l, @0x200001
0x030550  ldm.l     @sp+, er4-er6
0x030554  mov.l     @sp+, er3
0x030558  rts       
