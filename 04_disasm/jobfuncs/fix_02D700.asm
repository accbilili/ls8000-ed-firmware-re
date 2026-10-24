0x02D700  stm.l     er2-er3, @-sp
0x02D704  stm.l     er4-er6, @-sp
0x02D708  subs.l    #4, sp
0x02D70A  subs.l    #2, sp
0x02D70C  mov.l     #0x00400dab, er6
0x02D712  mov.b     r0l, @(0x5,sp)
0x02D716  mov.l     er1, @sp
0x02D71A  mov.b     @er6, r2l
0x02D71C  shll.b    #2, r2l
0x02D71E  shll.b    #2, r2l
0x02D720  mov.l     er6, er5
0x02D722  inc.l     #1, er5
0x02D724  mov.b     @er5, r0h
0x02D726  or.b      r0h, r2l
0x02D728  mov.b     r2l, @0x400df6
0x02D72E  mov.l     er6, er3
0x02D730  inc.l     #2, er3
0x02D732  mov.b     @er3, r2l
0x02D734  shll.b    #2, r2l
0x02D736  shll.b    #2, r2l
0x02D738  mov.l     er6, er4
0x02D73A  adds.l    #2, er4
0x02D73C  inc.l     #1, er4
0x02D73E  mov.b     @er4, r0h
0x02D740  or.b      r0h, r2l
0x02D742  mov.b     r2l, @0x400df7
0x02D748  mov.b     @er6, r2l
0x02D74A  shll.b    #2, r2l
0x02D74C  shll.b    #2, r2l
0x02D74E  mov.b     @er5, r5l
0x02D750  or.b      r5l, r2l
0x02D752  mov.b     r2l, @0x400df4
0x02D758  mov.b     @er3, r3l
0x02D75A  shll.b    #2, r3l
0x02D75C  shll.b    #2, r3l
0x02D75E  mov.b     @er4, r4l
0x02D760  or.b      r4l, r3l
0x02D762  mov.b     r3l, @0x400df5
0x02D768  mov.b     @er6, r5l
0x02D76A  sub.l     er2, er2
0x02D76C  mov.b     r5l, r2l
0x02D76E  mov.b     @(0x400d89,er2), r2l
0x02D776  cmp.b     #0x01, r2l
0x02D778  bne       0x02d788
0x02D77A  mov.b     @0x400df4, r2l
0x02D780  or.b      #0x80, r2l
0x02D782  mov.b     r2l, @0x400df4
0x02D788  mov.b     @(0x1,er6), r5l
0x02D78C  sub.l     er0, er0
0x02D78E  mov.b     r5l, r0l
0x02D790  mov.b     @(0x400d89,er0), r0l
0x02D798  cmp.b     #0x01, r0l
0x02D79A  bne       0x02d7aa
0x02D79C  mov.b     @0x400df4, r0l
0x02D7A2  or.b      #0x08, r0l
0x02D7A4  mov.b     r0l, @0x400df4
0x02D7AA  mov.b     @(0x2,er6), r5l
0x02D7AE  sub.l     er0, er0
0x02D7B0  mov.b     r5l, r0l
0x02D7B2  mov.b     @(0x400d89,er0), r0l
0x02D7BA  cmp.b     #0x01, r0l
0x02D7BC  bne       0x02d7cc
0x02D7BE  mov.b     @0x400df5, r0l
0x02D7C4  or.b      #0x80, r0l
0x02D7C6  mov.b     r0l, @0x400df5
0x02D7CC  mov.b     @(0x3,er6), r5l
0x02D7D0  sub.l     er0, er0
0x02D7D2  mov.b     r5l, r0l
0x02D7D4  mov.b     @(0x400d89,er0), r0l
0x02D7DC  cmp.b     #0x01, r0l
0x02D7DE  bne       0x02d7ee
0x02D7E0  mov.b     @0x400df5, r0l
0x02D7E6  or.b      #0x08, r0l
0x02D7E8  mov.b     r0l, @0x400df5
0x02D7EE  sub.b     r3l, r3l
0x02D7F0  bt        0x02d86c
0x02D7F2  mov.b     r3l, r0l
0x02D7F4  extu.w    r0
0x02D7F6  extu.l    er0
0x02D7F8  add.l     er6, er0
0x02D7FA  mov.b     @er0, r5l
0x02D7FC  mov.b     r5l, r4l
0x02D7FE  extu.w    r4
0x02D800  extu.l    er4
0x02D802  mov.l     er4, er0
0x02D804  mov.l     #0x00000006, er1
0x02D80A  jsr       0x018e1e
0x02D80E  mov.l     #0x0041ff3e, er1
0x02D814  add.l     er0, er1
0x02D816  mov.b     r5l, r0l
0x02D818  bsr       0x02da8e
0x02D81C  mov.b     @(0x41ff6e,er4), r0h
0x02D824  mov.b     r5l, r0l
0x02D826  bsr       0x02daa2
0x02D82A  mov.l     er4, er5
0x02D82C  shll.l    #2, er5
0x02D82E  mov.l     @sp, er0
0x02D832  add.l     er5, er0
0x02D834  mov.l     @er0, er0
0x02D838  mov.l     er0, @0x42024c
0x02D840  mov.l     @(0x3f146,er5), er0
0x02D84A  mov.l     @0x42024c, er1
0x02D852  mov.l     er1, @er0
0x02D856  mov.l     @(0x3f156,er5), er5
0x02D860  mov.b     @(0x440fdc,er4), r4l
0x02D868  mov.b     r4l, @er5
0x02D86A  inc.b     #1, r3l
0x02D86C  mov.b     @(0x5,sp), r0l
0x02D870  cmp.b     r0l, r3l
0x02D872  bcs       0x02d7f2
0x02D876  sub.b     r0l, r0l
0x02D878  mov.b     r0l, @0x200147
0x02D87E  mov.b     r0l, @0x200148
0x02D884  sub.b     r0l, r0l
0x02D886  mov.b     r0l, @0x200149
0x02D88C  mov.b     @0x400df4, r0l
0x02D892  mov.b     r0l, @0x2001ca
0x02D898  mov.b     @0x400df5, r0l
0x02D89E  mov.b     r0l, @0x2001cb
0x02D8A4  mov.w     #0x7800, r0
0x02D8A8  mov.w     r0, @0x20014e
0x02D8AE  mov.b     @0x400df6, r0l
0x02D8B4  mov.b     r0l, @0x200152
0x02D8BA  mov.b     @0x400df7, r0l
0x02D8C0  mov.b     r0l, @0x200153
0x02D8C6  mov.b     @0x4007c9, r0l
0x02D8CC  bne       0x02d8d8
0x02D8CE  mov.b     @(0x5,sp), r0l
0x02D8D2  add.b     #0xff, r0l
0x02D8D4  and.b     #0x07, r0l
0x02D8D6  bt        0x02d8e2
0x02D8D8  mov.b     @(0x5,sp), r0l
0x02D8DC  add.b     #0xff, r0l
0x02D8DE  and.b     #0x07, r0l
0x02D8E0  or.b      #0x20, r0l
0x02D8E2  mov.b     r0l, @0x2001c0
0x02D8E8  sub.b     r0l, r0l
0x02D8EA  mov.b     r0l, @0x2001a6
0x02D8F0  mov.b     #0x80, r0l
0x02D8F2  mov.b     r0l, @0x2001c1
0x02D8F8  btst      #1, @0x200002
0x02D900  beq       0x02d90e
0x02D902  mov.w     #0x5a00, r0
0x02D906  mov.w     r0, @0xffffbc
0x02D90C  bt        0x02d8f8
0x02D90E  jsr       0x010bd2
0x02D912  mov.b     #0xc0, r0l
0x02D914  mov.b     r0l, @0x200001
0x02D91A  jsr       0x010bd8
0x02D91E  mov.w     #0x5a00, r0
0x02D922  mov.w     r0, @0xffffbc
0x02D928  btst      #5, @0x200002
0x02D930  bne       0x02d928
0x02D932  mov.w     #0x5a00, r0
0x02D936  mov.w     r0, @0xffffbc
0x02D93C  sub.b     r0l, r0l
0x02D93E  mov.b     r0l, @0x2001c1
0x02D944  mov.b     #0x80, r0l
0x02D946  mov.b     r0l, @0x200001
0x02D94C  sub.b     r5l, r5l
0x02D94E  mov.l     #0x00c00000, er4
0x02D954  mov.b     r5l, r0l
0x02D956  extu.w    r0
0x02D958  extu.l    er0
0x02D95A  shll.l    #2, er0
0x02D95C  mov.l     er4, @(0x420250,er0)
0x02D966  inc.b     #1, r5l
0x02D968  add.l     #0x0000f000, er4
0x02D96E  cmp.b     #0x04, r5l
0x02D970  bcs       0x02d954
0x02D972  adds.l    #2, sp
0x02D974  adds.l    #4, sp
0x02D976  ldm.l     @sp+, er4-er6
0x02D97A  ldm.l     @sp+, er2-er3
0x02D97E  rts       
