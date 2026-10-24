0x03A3D4  stm.l     er2-er3, @-sp
0x03A3D8  stm.l     er4-er6, @-sp
0x03A3DC  sub.l     #0x00000036, sp
0x03A3E2  mov.l     #0x00400402, er4
0x03A3E8  mov.l     #0x004491d6, er5
0x03A3EE  mov.l     #0x004491d4, er6
0x03A3F4  mov.l     #0x00449b0e, er0
0x03A3FA  mov.b     @er0, r1l
0x03A3FC  inc.b     #1, r1l
0x03A3FE  mov.b     r1l, @er0
0x03A400  mov.w     @0x4202e0, r0
0x03A406  mov.w     r0, @0x42026c
0x03A40C  sub.w     r0, r0
0x03A40E  mov.w     r0, @er4
0x03A410  bsr       0x03a994
0x03A414  mov.w     @er4, r0
0x03A416  beq       0x03a438
0x03A418  mov.w     @0x40040a, r0
0x03A41E  mov.w     r0, @0x420272
0x03A424  mov.l     @0x40040c, er0
0x03A42C  mov.l     er0, @0x42026e
0x03A434  jmp       0x03a984
0x03A438  sub.b     r0l, r0l
0x03A43A  mov.b     r0l, @0x4007c9
0x03A440  mov.b     r0l, @0x4007ca
0x03A446  jsr       0x033422
0x03A44A  mov.b     #0x03, r0l
0x03A44C  mov.b     r0l, @0x400dab
0x03A452  mov.b     #0x01, r0l
0x03A454  mov.b     r0l, @0x400daa
0x03A45A  mov.b     r0l, @0x4007cb
0x03A460  jsr       0x034782
0x03A464  jsr       0x03d474
0x03A468  sub.w     r3, r3
0x03A46A  bt        0x03a486
0x03A46C  mov.w     r3, r0
0x03A46E  exts.l    er0
0x03A470  mov.b     #0x01, r1l
0x03A472  mov.b     r1l, @(0x400d89,er0)
0x03A47A  sub.b     r1l, r1l
0x03A47C  mov.b     r1l, @(0x41ff6e,er0)
0x03A484  inc.w     #1, r3
0x03A486  cmp.w     #0x0004, r3
0x03A48A  blt       0x03a46c
0x03A48C  jsr       0x02d1dc
0x03A490  sub.w     r0, r0
0x03A492  mov.w     r0, @0x400404
0x03A498  mov.w     #0x0930, r0
0x03A49C  mov.w     r0, @er4
0x03A49E  mov.w     #0x01c2, r0
0x03A4A2  mov.w     r0, @(0xe,sp)
0x03A4A6  sub.b     r0l, r0l
0x03A4A8  mov.b     r0l, @0x4491d5
0x03A4AE  mov.b     r0l, @er5
0x03A4B0  mov.b     #0x03, r0l
0x03A4B2  mov.b     r0l, @er6
0x03A4B4  mov.b     #0x01, r0l
0x03A4B6  mov.b     r0l, @(0x2c,sp)
0x03A4BA  mov.b     #0x01, r1l
0x03A4BC  mov.b     #0x01, r2l
0x03A4BE  sub.w     e0, e0
0x03A4C0  mov.w     e0, @(0x28,sp)
0x03A4C4  mov.l     #0x00400f3e, er3
0x03A4CA  mov.l     @er3, er0
0x03A4CE  mov.l     er0, @(0x32,sp)
0x03A4D4  shll.l    #2, er0
0x03A4D6  shll.l    #2, er0
0x03A4D8  shll.l    er0
0x03A4DA  mov.l     er0, @er3
0x03A4DE  mov.w     r2, @-sp
0x03A4E0  sub.l     er0, er0
0x03A4E2  mov.b     @er5, r0l
0x03A4E4  shll.l    er0
0x03A4E6  mov.w     @(0x2a,sp), e1
0x03A4EA  mov.b     r1l, r1h
0x03A4EC  mov.b     @(0x2e,sp), r1l
0x03A4F0  mov.w     @(0x44908c,er0), e0
0x03A4F8  mov.w     @(0x10,sp), r0
0x03A4FC  bsr       0x03b58e
0x03A500  adds.l    #2, sp
0x03A502  mov.l     @(0x32,sp), er0
0x03A508  mov.l     er0, @er3
0x03A50C  mov.b     @0x4003fb, r0l
0x03A512  cmp.b     #0x12, r0l
0x03A514  bne       0x03a51c
0x03A516  mov.w     #0x03e8, r3
0x03A51A  bt        0x03a520
0x03A51C  mov.w     #0x01e0, r3
0x03A520  mov.b     @er6, r0l
0x03A522  extu.w    r0
0x03A524  mov.w     #0x0006, e0
0x03A528  mulxu.w   e0, er0
0x03A52A  mov.w     @(0x4491a2,er0), r0
0x03A532  cmp.w     r3, r0
0x03A534  bcs       0x03a782
0x03A538  sub.w     r3, r3
0x03A53A  mov.l     #0x00420128, er0
0x03A540  mov.l     er0, @(0x20,sp)
0x03A546  bt        0x03a5aa
0x03A548  mov.w     #0x0006, r0
0x03A54C  mulxs.w   r3, er0
0x03A550  mov.l     er0, @(0x24,sp)
0x03A556  add.l     #0x0041ff3e, er0
0x03A55C  mov.l     er0, @(0x2e,sp)
0x03A562  mov.l     @(0x20,sp), er1
0x03A568  mov.l     @(0x24,sp), er2
0x03A56E  add.l     er2, er1
0x03A570  add.l     #0x00000078, er1
0x03A576  mov.l     er1, @(0x32,sp)
0x03A57C  mov.w     @er1, r1
0x03A57E  mov.w     r1, @er0
0x03A580  mov.l     @(0x32,sp), er0
0x03A586  inc.l     #2, er0
0x03A588  mov.l     @(0x2e,sp), er1
0x03A58E  inc.l     #2, er1
0x03A590  mov.w     @er0, r0
0x03A592  mov.w     r0, @er1
0x03A594  mov.l     @(0x32,sp), er0
0x03A59A  adds.l    #4, er0
0x03A59C  mov.l     @(0x2e,sp), er1
0x03A5A2  adds.l    #4, er1
0x03A5A4  mov.w     @er0, r0
0x03A5A6  mov.w     r0, @er1
0x03A5A8  inc.w     #1, r3
0x03A5AA  cmp.w     #0x0004, r3
0x03A5AE  blt       0x03a548
0x03A5B0  mov.b     #0xa2, r0l
0x03A5B2  mov.b     r0l, @0x200102
0x03A5B8  sub.w     r0, r0
0x03A5BA  mov.w     r0, @0x200182
0x03A5C0  mov.w     r0, @0x200184
0x03A5C6  sub.w     r0, r0
0x03A5C8  mov.w     r0, @0x200186
0x03A5CE  sub.w     r0, r0
0x03A5D0  mov.w     r0, @0x200188
0x03A5D6  btst      #7, @0x400400
0x03A5DE  bne       0x03a93e
0x03A5E2  sub.b     r0l, r0l
0x03A5E4  mov.b     r0l, @0x4491d5
0x03A5EA  mov.b     #0x01, r0l
0x03A5EC  mov.b     r0l, @er6
0x03A5EE  mov.b     #0x01, r1l
0x03A5F0  mov.b     #0x01, r2l
0x03A5F2  sub.w     r3, r3
0x03A5F4  mov.w     r2, @-sp
0x03A5F6  sub.l     er2, er2
0x03A5F8  mov.b     @er5, r2l
0x03A5FA  shll.l    er2
0x03A5FC  mov.w     r3, e1
0x03A5FE  mov.b     r1l, r1h
0x03A600  mov.b     r0l, r1l
0x03A602  mov.w     @(0x44908c,er2), e0
0x03A60A  mov.w     @(0x10,sp), r0
0x03A60E  bsr       0x03b58e
0x03A612  adds.l    #2, sp
0x03A614  mov.b     @er6, r1l
0x03A616  extu.w    r1
0x03A618  mov.w     #0x0006, e1
0x03A61C  mulxu.w   e1, er1
0x03A61E  mov.w     @(0x4491a2,er1), r1
0x03A626  mov.l     sp, er0
0x03A628  jsr       0x018ede
0x03A62C  mov.l     #0x0003f9b4, er1
0x03A632  jsr       0x0188d2
0x03A636  mov.w     r0, r0
0x03A638  bne       0x03a782
0x03A63C  mov.l     @0x420296, er0
0x03A644  mov.l     er0, @0x4498f0
0x03A64C  mov.l     #0x00420276, er3
0x03A652  sub.l     er0, er0
0x03A654  mov.b     @er6, r0l
0x03A656  mov.l     er0, er2
0x03A658  shll.l    #2, er0
0x03A65A  add.l     er3, er0
0x03A65C  mov.l     er0, @(0x4,sp)
0x03A662  mov.l     er2, er0
0x03A664  mov.l     #0x0000000c, er1
0x03A66A  jsr       0x018e1e
0x03A66E  sub.l     er1, er1
0x03A670  mov.b     @0x4491d5, r1l
0x03A676  shll.l    #2, er1
0x03A678  add.l     #0x00449978, er0
0x03A67E  add.l     er1, er0
0x03A680  mov.l     @er0, er0
0x03A684  mov.l     @(0x4,sp), er1
0x03A68A  mov.l     er0, @er1
0x03A68E  mov.l     er3, er0
0x03A690  bsr       0x03c194
0x03A694  sub.l     er0, er0
0x03A696  mov.b     @er6, r0l
0x03A698  mov.l     er0, @(0x1a,sp)
0x03A69E  shll.l    #2, er0
0x03A6A0  mov.l     er0, @(0x16,sp)
0x03A6A6  mov.l     @(0x16,sp), er1
0x03A6AC  add.l     er3, er1
0x03A6AE  mov.l     er0, @(0x4,sp)
0x03A6B4  mov.l     @er1, er0
0x03A6B8  jsr       0x018e9e
0x03A6BC  mov.l     @(0x1a,sp), er1
0x03A6C2  sub.l     er2, er2
0x03A6C4  mov.b     @(0x41ff6e,er1), r2l
0x03A6CC  shll.l    #2, er2
0x03A6CE  mov.l     @(0x400dda,er2), er1
0x03A6D8  jsr       0x0185ee
0x03A6DC  jsr       0x018860
0x03A6E0  mov.l     @(0x4,sp), er1
0x03A6E6  mov.l     er0, @(0x420286,er1)
0x03A6F0  mov.b     #0x01, r0l
0x03A6F2  mov.l     #0x0000000e, er1
0x03A6F8  add.l     sp, er1
0x03A6FA  bsr       0x03adf6
0x03A6FE  cmp.b     #0x01, r0l
0x03A700  bne       0x03a724
0x03A702  mov.l     @0x4491dc, er0
0x03A70A  mov.l     er0, @0x4498f0
0x03A712  mov.w     @(0xe,sp), r0
0x03A716  bsr       0x03b546
0x03A71A  cmp.b     #0x01, r0l
0x03A71C  beq       0x03a93e
0x03A720  jmp       0x03a932
0x03A724  btst      #7, @0x400400
0x03A72C  bne       0x03a93e
0x03A730  sub.b     r0l, r0l
0x03A732  mov.b     r0l, @er6
0x03A734  mov.b     #0x01, r0l
0x03A736  mov.b     #0x01, r1l
0x03A738  mov.b     #0x01, r2l
0x03A73A  sub.w     e0, e0
0x03A73C  mov.w     r2, @-sp
0x03A73E  sub.l     er2, er2
0x03A740  mov.b     @er5, r2l
0x03A742  shll.l    er2
0x03A744  mov.w     e0, e1
0x03A746  mov.b     r1l, r1h
0x03A748  mov.b     r0l, r1l
0x03A74A  mov.w     @(0x44908c,er2), e0
0x03A752  mov.w     @(0x10,sp), r0
0x03A756  bsr       0x03b58e
0x03A75A  adds.l    #2, sp
0x03A75C  mov.b     @er6, r1l
0x03A75E  extu.w    r1
0x03A760  mov.w     #0x0006, e1
0x03A764  mulxu.w   e1, er1
0x03A766  mov.w     @(0x4491a2,er1), r1
0x03A76E  mov.l     sp, er0
0x03A770  jsr       0x018ede
0x03A774  mov.l     #0x0003f9b4, er1
0x03A77A  jsr       0x0188d2
0x03A77E  mov.w     r0, r0
0x03A780  beq       0x03a78c
0x03A782  mov.w     #0x0950, r0
0x03A786  mov.w     r0, @er4
0x03A788  jmp       0x03a93e
0x03A78C  mov.l     @0x420296, er0
0x03A794  mov.l     er0, @0x4498f0
0x03A79C  sub.l     er0, er0
0x03A79E  mov.b     @er6, r0l
0x03A7A0  mov.l     er0, @(0x24,sp)
0x03A7A6  shll.l    #2, er0
0x03A7A8  add.l     er3, er0
0x03A7AA  mov.l     er0, @(0x4,sp)
0x03A7B0  mov.l     @(0x24,sp), er0
0x03A7B6  mov.l     #0x0000000c, er1
0x03A7BC  jsr       0x018e1e
0x03A7C0  sub.l     er1, er1
0x03A7C2  mov.b     @0x4491d5, r1l
0x03A7C8  shll.l    #2, er1
0x03A7CA  add.l     #0x00449978, er0
0x03A7D0  add.l     er1, er0
0x03A7D2  mov.l     @er0, er0
0x03A7D6  mov.l     @(0x4,sp), er1
0x03A7DC  mov.l     er0, @er1
0x03A7E0  mov.l     er3, er0
0x03A7E2  bsr       0x03c194
0x03A7E6  sub.l     er0, er0
0x03A7E8  mov.b     @er6, r0l
0x03A7EA  mov.l     er0, @(0x24,sp)
0x03A7F0  shll.l    #2, er0
0x03A7F2  mov.l     er0, @(0x20,sp)
0x03A7F8  mov.l     @(0x20,sp), er1
0x03A7FE  add.l     er1, er3
0x03A800  mov.l     er0, @(0x4,sp)
0x03A806  mov.l     @er3, er0
0x03A80A  jsr       0x018e9e
0x03A80E  mov.l     @(0x24,sp), er1
0x03A814  sub.l     er2, er2
0x03A816  mov.b     @(0x41ff6e,er1), r2l
0x03A81E  shll.l    #2, er2
0x03A820  mov.l     @(0x400dda,er2), er1
0x03A82A  jsr       0x0185ee
0x03A82E  jsr       0x018860
0x03A832  mov.l     @(0x4,sp), er1
0x03A838  mov.l     er0, @(0x420286,er1)
0x03A842  mov.b     #0x01, r3l
0x03A844  mov.l     #0x0000000e, er1
0x03A84A  add.l     sp, er1
0x03A84C  mov.b     r3l, r0l
0x03A84E  bsr       0x03adf6
0x03A852  cmp.b     #0x01, r0l
0x03A854  bne       0x03a878
0x03A856  mov.l     @0x4491dc, er0
0x03A85E  mov.l     er0, @0x4498f0
0x03A866  mov.w     @(0xe,sp), r0
0x03A86A  bsr       0x03b546
0x03A86E  cmp.b     #0x01, r0l
0x03A870  beq       0x03a93e
0x03A874  jmp       0x03a932
0x03A878  sub.b     r0l, r0l
0x03A87A  mov.b     r0l, @(0x2c,sp)
0x03A87E  btst      #7, @0x400400
0x03A886  bne       0x03a93e
0x03A88A  mov.w     #0x00e2, r0
0x03A88E  mov.w     r0, @(0xe,sp)
0x03A892  mov.b     #0x01, r0l
0x03A894  mov.b     r0l, @(0x2d,sp)
0x03A898  mov.b     #0x03, r3h
0x03A89A  mov.b     #0x02, r3l
0x03A89C  sub.w     e3, e3
0x03A89E  mov.w     r3, @-sp
0x03A8A0  sub.l     er1, er1
0x03A8A2  mov.b     @er5, r1l
0x03A8A4  shll.l    er1
0x03A8A6  mov.l     er1, @(0x6,sp)
0x03A8AC  mov.w     e3, e1
0x03A8AE  mov.b     r3h, r1h
0x03A8B0  mov.b     r0l, r1l
0x03A8B2  mov.l     @(0x6,sp), er2
0x03A8B8  mov.w     @(0x44908c,er2), e0
0x03A8C0  mov.w     @(0x10,sp), r0
0x03A8C4  bsr       0x03b58e
0x03A8C8  adds.l    #2, sp
0x03A8CA  btst      #7, @0x400400
0x03A8D2  bne       0x03a93e
0x03A8D4  sub.b     r0l, r0l
0x03A8D6  mov.b     r0l, @0x4491d5
0x03A8DC  mov.w     r3, @-sp
0x03A8DE  sub.l     er0, er0
0x03A8E0  mov.b     @er5, r0l
0x03A8E2  shll.l    er0
0x03A8E4  mov.b     @(0x2f,sp), r1h
0x03A8E8  mov.b     r3h, r1l
0x03A8EA  mov.w     @(0x44908c,er0), r0
0x03A8F2  bsr       0x03bd4a
0x03A8F6  adds.l    #2, sp
0x03A8F8  btst      #7, @0x400400
0x03A900  bne       0x03a93e
0x03A902  mov.l     #0x0000000e, er1
0x03A908  add.l     sp, er1
0x03A90A  mov.b     @(0x2c,sp), r0l
0x03A90E  bsr       0x03adf6
0x03A912  cmp.b     #0x01, r0l
0x03A914  bne       0x03a932
0x03A916  mov.l     @0x4491dc, er0
0x03A91E  mov.l     er0, @0x4498f0
0x03A926  mov.w     @(0xe,sp), r0
0x03A92A  bsr       0x03b546
0x03A92E  cmp.b     #0x01, r0l
0x03A930  beq       0x03a93e
0x03A932  mov.b     @er5, r0l
0x03A934  inc.b     #1, r0l
0x03A936  mov.b     r0l, @er5
0x03A938  cmp.b     #0x03, r0l
0x03A93A  bcs       0x03a5d6
0x03A93E  mov.b     #0x01, r0l
0x03A940  mov.b     r0l, @0x400d77
0x03A946  mov.b     r0l, @0x400d78
0x03A94C  btst      #7, @0x400400
0x03A954  beq       0x03a95a
0x03A956  sub.w     r0, r0
0x03A958  mov.w     r0, @er4
0x03A95A  mov.w     @er4, r0
0x03A95C  beq       0x03a97a
0x03A95E  mov.w     @0x40040a, r0
0x03A964  mov.w     r0, @0x420272
0x03A96A  mov.l     @0x40040c, er0
0x03A972  mov.l     er0, @0x42026e
0x03A97A  mov.w     @0x42026c, r0
0x03A980  jsr       0x02b87c
0x03A984  add.l     #0x00000036, sp
0x03A98A  ldm.l     @sp+, er4-er6
0x03A98E  ldm.l     @sp+, er2-er3
0x03A992  rts       
