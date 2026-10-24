0x03655E  stm.l     er2-er3, @-sp
0x036562  stm.l     er4-er6, @-sp
0x036566  sub.l     #0x00000012, sp
0x03656C  mov.l     #0x0040064e, er4
0x036572  mov.l     sp, er6
0x036574  sub.b     r0l, r0l
0x036576  mov.b     r0l, @0x420264
0x03657C  mov.b     @0x4007c0, r0l
0x036582  mov.b     r0l, @0x400daa
0x036588  sub.b     r5l, r5l
0x03658A  bt        0x0365da
0x03658C  mov.b     r5l, r3l
0x03658E  extu.w    r3
0x036590  extu.l    er3
0x036592  mov.l     er3, @(0xe,sp)
0x036598  add.l     er6, er3
0x03659A  mov.l     @(0xe,sp), er0
0x0365A0  mov.b     @(0x4007c1,er0), r0l
0x0365A8  mov.b     r0l, @er3
0x0365AA  mov.b     @er3, r3l
0x0365AC  cmp.b     #0x09, r3l
0x0365AE  bne       0x0365be
0x0365B0  mov.b     r5l, r0l
0x0365B2  extu.w    r0
0x0365B4  extu.l    er0
0x0365B6  add.l     er6, er0
0x0365B8  mov.b     #0x04, r1l
0x0365BA  mov.b     r1l, @er0
0x0365BC  bt        0x0365d8
0x0365BE  mov.b     r5l, r0l
0x0365C0  extu.w    r0
0x0365C2  extu.l    er0
0x0365C4  add.l     er6, er0
0x0365C6  mov.b     @er0, r0l
0x0365C8  cmp.b     #0x04, r0l
0x0365CA  bne       0x0365d8
0x0365CC  mov.b     r5l, r0l
0x0365CE  extu.w    r0
0x0365D0  extu.l    er0
0x0365D2  add.l     er6, er0
0x0365D4  mov.b     #0x05, r1l
0x0365D6  mov.b     r1l, @er0
0x0365D8  inc.b     #1, r5l
0x0365DA  mov.b     @0x400daa, r0l
0x0365E0  cmp.b     r0l, r5l
0x0365E2  bcs       0x03658c
0x0365E4  mov.b     @er6, r3l
0x0365E6  mov.b     r3l, r0l
0x0365E8  extu.w    r0
0x0365EA  mov.w     #0x003a, e0
0x0365EE  mulxu.w   e0, er0
0x0365F0  add.l     er4, er0
0x0365F2  add.l     #0x00000028, er0
0x0365F8  mov.b     @er0, r0l
0x0365FA  and.b     #0x0f, r0l
0x0365FC  mov.b     r0l, r5l
0x0365FE  beq       0x036650
0x036600  sub.l     er0, er0
0x036602  mov.b     r5l, r0l
0x036604  mov.b     @er6, r1l
0x036606  mov.b     r1l, @(0x400daa,er0)
0x03660E  mov.b     #0x01, r5l
0x036610  bt        0x036642
0x036612  mov.b     r5l, r0l
0x036614  extu.w    r0
0x036616  extu.l    er0
0x036618  add.l     er6, er0
0x03661A  mov.b     @er0, r3h
0x03661C  mov.b     r3h, r0l
0x03661E  extu.w    r0
0x036620  mov.w     #0x003a, e0
0x036624  mulxu.w   e0, er0
0x036626  add.l     er4, er0
0x036628  add.l     #0x00000028, er0
0x03662E  mov.b     @er0, r0l
0x036630  and.b     #0x0f, r0l
0x036632  mov.b     r0l, r5h
0x036634  extu.w    r0
0x036636  extu.l    er0
0x036638  mov.b     r3h, @(0x400daa,er0)
0x036640  inc.b     #1, r5l
0x036642  mov.b     @0x400daa, r0l
0x036648  cmp.b     r0l, r5l
0x03664A  bcs       0x036612
0x03664C  jmp       0x0366f4
0x036650  sub.b     r5l, r5l
0x036652  mov.b     r5l, r0l
0x036654  extu.w    r0
0x036656  extu.l    er0
0x036658  mov.l     #0x00000004, er1
0x03665E  add.l     sp, er1
0x036660  add.l     er0, er1
0x036662  sub.b     r0l, r0l
0x036664  mov.b     r0l, @er1
0x036666  inc.b     #1, r5l
0x036668  cmp.b     #0x05, r5l
0x03666A  bls       0x036652
0x03666C  sub.l     er0, er0
0x03666E  mov.b     @er6, r0l
0x036670  mov.l     #0x00000004, er1
0x036676  add.l     sp, er1
0x036678  add.l     er0, er1
0x03667A  mov.b     #0x01, r0l
0x03667C  mov.b     r0l, @er1
0x03667E  mov.b     #0x01, r5l
0x036680  bt        0x03669e
0x036682  mov.b     r5l, r0l
0x036684  extu.w    r0
0x036686  extu.l    er0
0x036688  add.l     er6, er0
0x03668A  sub.l     er1, er1
0x03668C  mov.b     @er0, r1l
0x03668E  mov.l     #0x00000004, er0
0x036694  add.l     sp, er0
0x036696  add.l     er1, er0
0x036698  mov.b     #0x01, r1l
0x03669A  mov.b     r1l, @er0
0x03669C  inc.b     #1, r5l
0x03669E  mov.b     @0x400daa, r0l
0x0366A4  cmp.b     r0l, r5l
0x0366A6  bcs       0x036682
0x0366A8  sub.b     r5h, r5h
0x0366AA  sub.b     r5l, r5l
0x0366AC  mov.b     r5l, r0l
0x0366AE  extu.w    r0
0x0366B0  extu.l    er0
0x0366B2  shll.l    er0
0x0366B4  mov.w     @(0x3f81c,er0), r0
0x0366BC  exts.l    er0
0x0366BE  mov.l     #0x00000004, er1
0x0366C4  add.l     sp, er1
0x0366C6  add.l     er0, er1
0x0366C8  mov.b     @er1, r1l
0x0366CA  cmp.b     #0x01, r1l
0x0366CC  bne       0x0366ee
0x0366CE  mov.b     r5h, r0l
0x0366D0  inc.b     #1, r5h
0x0366D2  extu.w    r0
0x0366D4  extu.l    er0
0x0366D6  mov.b     r5l, r1l
0x0366D8  extu.w    r1
0x0366DA  extu.l    er1
0x0366DC  shll.l    er1
0x0366DE  mov.b     @(0x3f81d,er1), r1l
0x0366E6  mov.b     r1l, @(0x400dab,er0)
0x0366EE  inc.b     #1, r5l
0x0366F0  cmp.b     #0x05, r5l
0x0366F2  bls       0x0366ac
0x0366F4  mov.b     r3l, r0l
0x0366F6  extu.w    r0
0x0366F8  mov.w     #0x003a, e0
0x0366FC  mulxu.w   e0, er0
0x0366FE  add.l     er4, er0
0x036700  add.l     #0x0000002a, er0
0x036706  mov.b     @er0, r0l
0x036708  mov.b     r0l, @0x400d7a
0x03670E  mov.b     @0x4206ec, r0l
0x036714  bne       0x03672e
0x036716  mov.b     r3l, r0l
0x036718  extu.w    r0
0x03671A  mov.w     #0x003a, e0
0x03671E  mulxu.w   e0, er0
0x036720  add.l     er4, er0
0x036722  add.l     #0x00000032, er0
0x036728  mov.b     @er0, r0l
0x03672A  and.b     #0x01, r0l
0x03672C  bt        0x036730
0x03672E  mov.b     #0x01, r0l
0x036730  mov.b     r0l, @0x400db7
0x036736  mov.b     r3l, r0l
0x036738  extu.w    r0
0x03673A  mov.w     #0x003a, e0
0x03673E  mulxu.w   e0, er0
0x036740  add.l     er4, er0
0x036742  add.l     #0x00000029, er0
0x036748  mov.b     @er0, r5l
0x03674A  mov.b     r5l, r0l
0x03674C  and.b     #0x80, r0l
0x03674E  rotl.b    r0l
0x036750  and.b     #0x01, r0l
0x036752  mov.b     r0l, @0x400da0
0x036758  mov.b     @0x4206ec, r0l
0x03675E  bne       0x03676a
0x036760  and.b     #0x01, r5l
0x036762  mov.b     r5l, @0x400db4
0x036768  bt        0x036772
0x03676A  mov.b     #0x01, r0l
0x03676C  mov.b     r0l, @0x400db4
0x036772  mov.b     r3l, r5l
0x036774  extu.w    r5
0x036776  mov.w     #0x003a, e5
0x03677A  mulxu.w   e5, er5
0x03677C  add.l     er4, er5
0x03677E  mov.b     @(0x2c,er5), r0l
0x036782  and.b     #0x03, r0l
0x036784  mov.b     r0l, @0x400db3
0x03678A  mov.b     @(0x2b,er5), r5l
0x03678E  btst      #4, r5l
0x036790  beq       0x0367ae
0x036792  mov.b     r3l, r0l
0x036794  extu.w    r0
0x036796  mov.w     #0x003a, e0
0x03679A  mulxu.w   e0, er0
0x03679C  add.l     er4, er0
0x03679E  add.l     #0x00000028, er0
0x0367A4  mov.b     @er0, r0l
0x0367A6  and.b     #0xf0, r0l
0x0367A8  shlr.b    #2, r0l
0x0367AA  shlr.b    #2, r0l
0x0367AC  bt        0x0367b0
0x0367AE  sub.b     r0l, r0l
0x0367B0  mov.b     r0l, @0x400db5
0x0367B6  mov.b     r3l, r0l
0x0367B8  extu.w    r0
0x0367BA  mov.w     #0x003a, e0
0x0367BE  mulxu.w   e0, er0
0x0367C0  add.l     er4, er0
0x0367C2  add.l     #0x0000002b, er0
0x0367C8  mov.b     @er0, r0l
0x0367CA  and.b     #0x40, r0l
0x0367CC  rotl.b    #2, r0l
0x0367CE  and.b     #0x03, r0l
0x0367D0  mov.b     r0l, @0x400db6
0x0367D6  sub.b     r5l, r5l
0x0367D8  mov.l     er4, @(0xe,sp)
0x0367DE  cmp.b     #0x01, r5l
0x0367E0  bne       0x03682a
0x0367E2  mov.b     @0x4007c7, r0l
0x0367E8  cmp.b     #0x01, r0l
0x0367EA  bne       0x03682a
0x0367EC  mov.b     r5l, r3l
0x0367EE  extu.w    r3
0x0367F0  extu.l    er3
0x0367F2  mov.l     er3, er2
0x0367F4  shll.l    er2
0x0367F6  mov.l     @(0xe,sp), er0
0x0367FC  mov.w     #0x0033, r1
0x036800  jsr       0x01605a
0x036804  mov.w     r0, @(0x400da2,er2)
0x03680C  mov.l     @(0xe,sp), er0
0x036812  add.l     #0x0000002d, er0
0x036818  mov.b     @er0, r0l
0x03681A  mov.b     r0l, @(0x400db8,er3)
0x036822  mov.l     @(0xe,sp), er0
0x036828  bt        0x03687a
0x03682A  mov.b     r5l, r3l
0x03682C  extu.w    r3
0x03682E  extu.l    er3
0x036830  mov.l     er3, er2
0x036832  shll.l    er2
0x036834  mov.l     er3, er0
0x036836  mov.l     #0x0000003a, er1
0x03683C  jsr       0x018e1e
0x036840  add.l     er4, er0
0x036842  add.l     #0x0000003a, er0
0x036848  mov.l     er0, @(0xa,sp)
0x03684E  mov.w     #0x0033, r1
0x036852  jsr       0x01605a
0x036856  mov.w     r0, @(0x400da2,er2)
0x03685E  mov.l     @(0xa,sp), er0
0x036864  add.l     #0x0000002d, er0
0x03686A  mov.b     @er0, r0l
0x03686C  mov.b     r0l, @(0x400db8,er3)
0x036874  mov.l     @(0xa,sp), er0
0x03687A  add.l     #0x00000039, er0
0x036880  mov.b     @er0, r0l
0x036882  mov.b     r0l, @(0x400dbc,er3)
0x03688A  inc.b     #1, r5l
0x03688C  cmp.b     #0x03, r5l
0x03688E  bls       0x0367de
0x036892  mov.b     @0x400d7a, r0l
0x036898  cmp.b     #0x10, r0l
0x03689A  bne       0x0368dc
0x03689C  mov.b     #0x01, r0l
0x03689E  mov.b     r0l, @0x400db7
0x0368A4  sub.b     r0l, r0l
0x0368A6  mov.b     r0l, @0x400da0
0x0368AC  sub.b     r5l, r5l
0x0368AE  mov.b     r5l, r3l
0x0368B0  extu.w    r3
0x0368B2  extu.l    er3
0x0368B4  mov.b     #0xff, r0l
0x0368B6  mov.b     r0l, @(0x400db8,er3)
0x0368BE  mov.l     er3, er0
0x0368C0  shll.l    er0
0x0368C2  sub.w     r1, r1
0x0368C4  mov.w     r1, @(0x400da2,er0)
0x0368CC  sub.b     r0l, r0l
0x0368CE  mov.b     r0l, @(0x400dbc,er3)
0x0368D6  inc.b     #1, r5l
0x0368D8  cmp.b     #0x03, r5l
0x0368DA  bls       0x0368ae
0x0368DC  add.l     #0x00000012, sp
0x0368E2  ldm.l     @sp+, er4-er6
0x0368E6  ldm.l     @sp+, er2-er3
0x0368EA  rts       
