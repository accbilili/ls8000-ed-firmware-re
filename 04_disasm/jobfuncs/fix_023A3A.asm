0x023A3A  stm.l     er2-er3, @-sp
0x023A3E  stm.l     er4-er6, @-sp
0x023A42  sub.l     #0x00000424, sp
0x023A48  mov.l     #0x00400436, er4
0x023A4E  mov.l     sp, er6
0x023A50  mov.b     @0x40043d, r0l
0x023A56  and.b     #0x1f, r0l
0x023A58  bne       0x023d12
0x023A5C  mov.b     @0x40043f, r0l
0x023A62  bne       0x023d12
0x023A66  mov.b     @0x400445, r0l
0x023A6C  bne       0x023d12
0x023A70  sub.b     r5l, r5l
0x023A72  mov.l     #0x0040043e, er3
0x023A78  mov.b     r5l, r0l
0x023A7A  extu.w    r0
0x023A7C  mov.w     #0x000a, e0
0x023A80  mulxu.w   e0, er0
0x023A82  mov.b     @er3, r1l
0x023A84  mov.b     @(0x3e59c,er0), r0l
0x023A8C  cmp.b     r0l, r1l
0x023A8E  bne       0x023ac4
0x023A90  extu.w    r5
0x023A92  mov.w     r5, r0
0x023A94  mov.w     #0x000a, e0
0x023A98  mulxu.w   e0, er0
0x023A9A  add.l     #0x0003e59c, er0
0x023AA0  mov.l     er0, @(0x420,sp)
0x023AA6  mov.b     @(0x1,er0), r5h
0x023AAA  mov.l     @(0x420,sp), er0
0x023AB0  mov.l     @(0x2,er0), er1
0x023AB6  mov.l     er1, @(0x41c,sp)
0x023ABC  mov.l     @(0x6,er0), er3
0x023AC2  bt        0x023ae0
0x023AC4  mov.b     r5l, r0l
0x023AC6  extu.w    r0
0x023AC8  mov.w     #0x000a, e0
0x023ACC  mulxu.w   e0, er0
0x023ACE  mov.b     @(0x3e59c,er0), r0l
0x023AD6  cmp.b     #0xff, r0l
0x023AD8  beq       0x023d12
0x023ADC  inc.b     #1, r5l
0x023ADE  bt        0x023a78
0x023AE0  mov.b     @0x40043e, r2h
0x023AE6  mov.b     @0x400440, r5l
0x023AEC  mov.b     @0x400441, r0l
0x023AF2  cmp.b     r5h, r0l
0x023AF4  bne       0x023d12
0x023AF8  mov.b     @0x400443, r0l
0x023AFE  extu.w    r0
0x023B00  mov.b     r0l, r0h
0x023B02  sub.b     r0l, r0l
0x023B04  mov.b     @0x400444, r1l
0x023B0A  extu.w    r1
0x023B0C  or.w      r1, r0
0x023B0E  extu.l    er0
0x023B10  sub.l     er1, er1
0x023B12  mov.b     @0x400442, r1l
0x023B18  mov.w     r1, e1
0x023B1A  sub.w     r1, r1
0x023B1C  or.l      er1, er0
0x023B20  mov.l     er0, @(0x420,sp)
0x023B26  mov.b     r2h, r0l
0x023B28  cmp.b     #0x03, r0l
0x023B2A  beq       0x023b4e
0x023B2C  cmp.b     #0x84, r0l
0x023B2E  beq       0x023be6
0x023B32  cmp.b     #0x85, r0l
0x023B34  beq       0x023c4c
0x023B38  cmp.b     #0x88, r0l
0x023B3A  beq       0x023cbc
0x023B3E  cmp.b     #0x8d, r0l
0x023B40  beq       0x023ccc
0x023B44  cmp.b     #0xe0, r0l
0x023B46  beq       0x023cf8
0x023B4A  jmp       0x023cf8
0x023B4E  mov.l     #0x0003e4e8, er3
0x023B54  mov.b     r5l, r5l
0x023B56  bne       0x023b62
0x023B58  mov.l     @(0x4,er3), er3
0x023B5E  mov.b     #0x01, r2l
0x023B60  bt        0x023b92
0x023B62  cmp.b     #0x01, r5l
0x023B64  bcs       0x023b80
0x023B66  cmp.b     #0x03, r5l
0x023B68  bhi       0x023b80
0x023B6A  mov.b     r5l, r0l
0x023B6C  extu.w    r0
0x023B6E  extu.l    er0
0x023B70  shll.l    #2, er0
0x023B72  add.l     er0, er3
0x023B74  subs.l    #4, er3
0x023B76  mov.l     @er3, er3
0x023B7A  add.b     #0xff, r5l
0x023B7C  mov.b     r5l, r2l
0x023B7E  bt        0x023b92
0x023B80  cmp.b     #0x09, r5l
0x023B82  bne       0x023b8e
0x023B84  mov.l     @(0xc,er3), er3
0x023B8A  mov.b     #0x03, r2l
0x023B8C  bt        0x023b92
0x023B8E  jmp       0x023d12
0x023B92  mov.w     @(0x422,sp), r0
0x023B96  btst      #0, r0l
0x023B98  bne       0x023d12
0x023B9C  mov.w     @0x400406, r0
0x023BA2  and.w     #0x00ff, r0
0x023BA6  cmp.w     #0x0001, r0
0x023BAA  bne       0x023bb4
0x023BAC  mov.b     @0x400d78, r0l
0x023BB2  beq       0x023bba
0x023BB4  jsr       0x010b56
0x023BB8  bt        0x023b9c
0x023BBA  mov.b     #0x01, r0l
0x023BBC  mov.b     r0l, @0x400d74
0x023BC2  sub.l     er5, er5
0x023BC4  mov.b     r2l, r5l
0x023BC6  mov.b     #0x0e, r0l
0x023BC8  mov.b     r0l, @(0x400eb5,er5)
0x023BD0  sub.b     r0l, r0l
0x023BD2  mov.b     r0l, @0x400eba
0x023BD8  sub.b     r0l, r0l
0x023BDA  mov.b     r0l, @(0x400f2e,er5)
0x023BE2  jmp       0x023cf8
0x023BE6  mov.b     r5l, r5l
0x023BE8  bne       0x023bf4
0x023BEA  mov.l     @0x03e50c, er3
0x023BF2  bt        0x023c20
0x023BF4  cmp.b     #0x01, r5l
0x023BF6  bcs       0x023c0e
0x023BF8  cmp.b     #0x03, r5l
0x023BFA  bhi       0x023c0e
0x023BFC  sub.l     er3, er3
0x023BFE  mov.b     r5l, r3l
0x023C00  shll.l    #2, er3
0x023C02  mov.l     @(0x3e504,er3), er3
0x023C0C  bt        0x023c20
0x023C0E  cmp.b     #0x09, r5l
0x023C10  bne       0x023c1c
0x023C12  mov.l     @0x03e514, er3
0x023C1A  bt        0x023c20
0x023C1C  jmp       0x023d12
0x023C20  mov.w     @(0x422,sp), r0
0x023C24  btst      #0, r0l
0x023C26  bne       0x023d12
0x023C2A  mov.l     #0x00004e20, er0
0x023C30  mov.l     er0, @(0x41c,sp)
0x023C36  mov.w     @0x400406, r0
0x023C3C  and.w     #0x00ff, r0
0x023C40  cmp.w     #0x0001, r0
0x023C44  beq       0x023cb2
0x023C46  jsr       0x010b56
0x023C4A  bt        0x023c36
0x023C4C  mov.b     r5l, r5l
0x023C4E  bne       0x023c5a
0x023C50  mov.l     @0x03e4fc, er3
0x023C58  bt        0x023c86
0x023C5A  cmp.b     #0x01, r5l
0x023C5C  bcs       0x023c74
0x023C5E  cmp.b     #0x03, r5l
0x023C60  bhi       0x023c74
0x023C62  sub.l     er3, er3
0x023C64  mov.b     r5l, r3l
0x023C66  shll.l    #2, er3
0x023C68  mov.l     @(0x3e4f4,er3), er3
0x023C72  bt        0x023c86
0x023C74  cmp.b     #0x09, r5l
0x023C76  bne       0x023c82
0x023C78  mov.l     @0x03e504, er3
0x023C80  bt        0x023c86
0x023C82  jmp       0x023d12
0x023C86  mov.w     @(0x422,sp), r0
0x023C8A  btst      #0, r0l
0x023C8C  bne       0x023d12
0x023C90  mov.l     #0x00004e20, er0
0x023C96  mov.l     er0, @(0x41c,sp)
0x023C9C  mov.w     @0x400406, r0
0x023CA2  and.w     #0x00ff, r0
0x023CA6  cmp.w     #0x0001, r0
0x023CAA  beq       0x023cb2
0x023CAC  jsr       0x010b56
0x023CB0  bt        0x023c9c
0x023CB2  mov.b     #0x01, r0l
0x023CB4  mov.b     r0l, @0x400d74
0x023CBA  bt        0x023cf8
0x023CBC  mov.l     @(0x420,sp), er0
0x023CC2  and.l     #0x00000003, er0
0x023CC8  beq       0x023cf8
0x023CCA  bt        0x023d12
0x023CCC  mov.b     r5l, r5l
0x023CCE  bne       0x023cd4
0x023CD0  mov.b     #0x01, r5h
0x023CD2  bt        0x023ce8
0x023CD4  cmp.b     #0x01, r5l
0x023CD6  bcs       0x023ce2
0x023CD8  cmp.b     #0x03, r5l
0x023CDA  bhi       0x023ce2
0x023CDC  add.b     #0xff, r5l
0x023CDE  mov.b     r5l, r5h
0x023CE0  bt        0x023ce8
0x023CE2  cmp.b     #0x09, r5l
0x023CE4  bne       0x023ce8
0x023CE6  mov.b     #0x03, r5h
0x023CE8  mov.b     r5h, r3l
0x023CEA  extu.w    r3
0x023CEC  mov.w     #0x001c, e3
0x023CF0  mulxu.w   e3, er3
0x023CF2  add.l     #0x004007e5, er3
0x023CF8  mov.l     @(0x420,sp), er0
0x023CFE  beq       0x023f92
0x023D02  mov.l     @(0x420,sp), er0
0x023D08  mov.l     @(0x41c,sp), er1
0x023D0E  cmp.l     er1, er0
0x023D10  bls       0x023d1a
0x023D12  mov.w     #0x0050, r0
0x023D16  jmp       0x023f12
0x023D1A  mov.b     r2h, r0l
0x023D1C  cmp.b     #0x88, r0l
0x023D1E  bne       0x023f7e
0x023D22  mov.b     @0x4003fb, r0l
0x023D28  cmp.b     #0x17, r0l
0x023D2A  beq       0x023d3a
0x023D2C  cmp.b     #0x18, r0l
0x023D2E  beq       0x023d3a
0x023D30  mov.w     #0x0053, r1
0x023D34  mov.w     r1, @er4
0x023D36  jmp       0x023f92
0x023D3A  mov.w     @(0x422,sp), r1
0x023D3E  mov.l     er6, er0
0x023D40  jsr       0x0118d0
0x023D44  mov.w     @er4, r0
0x023D46  bne       0x023f92
0x023D4A  mov.b     @(0x2,er6), r5l
0x023D4E  cmp.b     #0x01, r5l
0x023D50  bcs       0x023d56
0x023D52  cmp.b     #0x04, r5l
0x023D54  bls       0x023d5e
0x023D56  mov.w     #0x0053, r0
0x023D5A  jmp       0x023f12
0x023D5E  sub.l     er5, er5
0x023D60  mov.b     @er6, r5l
0x023D62  shll.l    #2, er5
0x023D64  shll.l    #2, er5
0x023D66  shll.l    #2, er5
0x023D68  shll.l    #2, er5
0x023D6A  sub.l     er0, er0
0x023D6C  mov.b     @(0x1,er6), r0l
0x023D70  add.l     er0, er5
0x023D72  mov.b     @(0x2,er6), r0l
0x023D76  extu.w    r0
0x023D78  shll.w    #2, r0
0x023D7A  shll.w    #2, r0
0x023D7C  add.w     #0x0004, r0
0x023D80  extu.w    r5
0x023D82  cmp.w     r5, r0
0x023D84  beq       0x023d8e
0x023D86  mov.w     #0x0053, r0
0x023D8A  jmp       0x023f12
0x023D8E  mov.b     @(0x2,er6), r0l
0x023D92  mov.b     r0l, @0x40041a
0x023D98  sub.b     r5h, r5h
0x023D9A  mov.b     #0x04, r5l
0x023D9C  jmp       0x023f68
0x023DA0  mov.b     r5l, r0l
0x023DA2  inc.b     #1, r5l
0x023DA4  extu.w    r0
0x023DA6  extu.l    er0
0x023DA8  add.l     er6, er0
0x023DAA  sub.l     er3, er3
0x023DAC  mov.b     @er0, r3l
0x023DAE  mov.b     r3l, r3h
0x023DB0  sub.b     r3l, r3l
0x023DB2  mov.w     r3, e3
0x023DB4  sub.w     r3, r3
0x023DB6  mov.b     r5l, r0l
0x023DB8  inc.b     #1, r5l
0x023DBA  extu.w    r0
0x023DBC  extu.l    er0
0x023DBE  add.l     er6, er0
0x023DC0  sub.l     er1, er1
0x023DC2  mov.b     @er0, r1l
0x023DC4  mov.w     r1, e1
0x023DC6  sub.w     r1, r1
0x023DC8  add.l     er1, er3
0x023DCA  mov.b     r5l, r0l
0x023DCC  inc.b     #1, r5l
0x023DCE  extu.w    r0
0x023DD0  extu.l    er0
0x023DD2  add.l     er6, er0
0x023DD4  sub.l     er1, er1
0x023DD6  mov.b     @er0, r1l
0x023DD8  shll.l    #2, er1
0x023DDA  shll.l    #2, er1
0x023DDC  shll.l    #2, er1
0x023DDE  shll.l    #2, er1
0x023DE0  add.l     er1, er3
0x023DE2  mov.b     r5l, r0l
0x023DE4  inc.b     #1, r5l
0x023DE6  extu.w    r0
0x023DE8  extu.l    er0
0x023DEA  add.l     er6, er0
0x023DEC  sub.l     er1, er1
0x023DEE  mov.b     @er0, r1l
0x023DF0  add.l     er1, er3
0x023DF2  mov.b     r5l, r0l
0x023DF4  inc.b     #1, r5l
0x023DF6  extu.w    r0
0x023DF8  extu.l    er0
0x023DFA  add.l     er6, er0
0x023DFC  sub.l     er1, er1
0x023DFE  mov.b     @er0, r1l
0x023E00  mov.b     r1l, r1h
0x023E02  sub.b     r1l, r1l
0x023E04  mov.w     r1, e1
0x023E06  sub.w     r1, r1
0x023E08  mov.b     r5l, r0l
0x023E0A  inc.b     #1, r5l
0x023E0C  extu.w    r0
0x023E0E  extu.l    er0
0x023E10  add.l     er6, er0
0x023E12  sub.l     er2, er2
0x023E14  mov.b     @er0, r2l
0x023E16  mov.w     r2, e2
0x023E18  sub.w     r2, r2
0x023E1A  add.l     er2, er1
0x023E1C  mov.b     r5l, r0l
0x023E1E  inc.b     #1, r5l
0x023E20  extu.w    r0
0x023E22  extu.l    er0
0x023E24  add.l     er6, er0
0x023E26  sub.l     er2, er2
0x023E28  mov.b     @er0, r2l
0x023E2A  shll.l    #2, er2
0x023E2C  shll.l    #2, er2
0x023E2E  shll.l    #2, er2
0x023E30  shll.l    #2, er2
0x023E32  add.l     er2, er1
0x023E34  mov.b     r5l, r0l
0x023E36  inc.b     #1, r5l
0x023E38  extu.w    r0
0x023E3A  extu.l    er0
0x023E3C  add.l     er6, er0
0x023E3E  sub.l     er2, er2
0x023E40  mov.b     @er0, r2l
0x023E42  add.l     er2, er1
0x023E44  mov.l     er1, @(0x41c,sp)
0x023E4A  mov.b     r5l, r0l
0x023E4C  inc.b     #1, r5l
0x023E4E  extu.w    r0
0x023E50  extu.l    er0
0x023E52  add.l     er6, er0
0x023E54  sub.l     er2, er2
0x023E56  mov.b     @er0, r2l
0x023E58  mov.b     r2l, r2h
0x023E5A  sub.b     r2l, r2l
0x023E5C  mov.w     r2, e2
0x023E5E  sub.w     r2, r2
0x023E60  mov.b     r5l, r0l
0x023E62  inc.b     #1, r5l
0x023E64  extu.w    r0
0x023E66  extu.l    er0
0x023E68  add.l     er6, er0
0x023E6A  sub.l     er1, er1
0x023E6C  mov.b     @er0, r1l
0x023E6E  mov.w     r1, e1
0x023E70  sub.w     r1, r1
0x023E72  add.l     er1, er2
0x023E74  mov.b     r5l, r0l
0x023E76  inc.b     #1, r5l
0x023E78  extu.w    r0
0x023E7A  extu.l    er0
0x023E7C  add.l     er6, er0
0x023E7E  sub.l     er1, er1
0x023E80  mov.b     @er0, r1l
0x023E82  shll.l    #2, er1
0x023E84  shll.l    #2, er1
0x023E86  shll.l    #2, er1
0x023E88  shll.l    #2, er1
0x023E8A  add.l     er1, er2
0x023E8C  mov.b     r5l, r0l
0x023E8E  inc.b     #1, r5l
0x023E90  extu.w    r0
0x023E92  extu.l    er0
0x023E94  add.l     er6, er0
0x023E96  sub.l     er1, er1
0x023E98  mov.b     @er0, r1l
0x023E9A  add.l     er1, er2
0x023E9C  mov.l     er2, @(0x412,sp)
0x023EA2  mov.b     r5l, r0l
0x023EA4  inc.b     #1, r5l
0x023EA6  extu.w    r0
0x023EA8  extu.l    er0
0x023EAA  add.l     er6, er0
0x023EAC  sub.l     er1, er1
0x023EAE  mov.b     @er0, r1l
0x023EB0  mov.b     r1l, r1h
0x023EB2  sub.b     r1l, r1l
0x023EB4  mov.w     r1, e1
0x023EB6  sub.w     r1, r1
0x023EB8  mov.b     r5l, r0l
0x023EBA  inc.b     #1, r5l
0x023EBC  extu.w    r0
0x023EBE  extu.l    er0
0x023EC0  add.l     er6, er0
0x023EC2  sub.l     er2, er2
0x023EC4  mov.b     @er0, r2l
0x023EC6  mov.w     r2, e2
0x023EC8  sub.w     r2, r2
0x023ECA  add.l     er2, er1
0x023ECC  mov.b     r5l, r0l
0x023ECE  inc.b     #1, r5l
0x023ED0  extu.w    r0
0x023ED2  extu.l    er0
0x023ED4  add.l     er6, er0
0x023ED6  sub.l     er2, er2
0x023ED8  mov.b     @er0, r2l
0x023EDA  shll.l    #2, er2
0x023EDC  shll.l    #2, er2
0x023EDE  shll.l    #2, er2
0x023EE0  shll.l    #2, er2
0x023EE2  add.l     er2, er1
0x023EE4  mov.b     r5l, r0l
0x023EE6  inc.b     #1, r5l
0x023EE8  extu.w    r0
0x023EEA  extu.l    er0
0x023EEC  add.l     er6, er0
0x023EEE  sub.l     er2, er2
0x023EF0  mov.b     @er0, r2l
0x023EF2  add.l     er2, er1
0x023EF4  mov.l     er1, @(0x416,sp)
0x023EFA  mov.l     @(0x412,sp), er0
0x023F00  cmp.l     er0, er3
0x023F02  bhi       0x023f0e
0x023F04  mov.l     @(0x41c,sp), er0
0x023F0A  cmp.l     er1, er0
0x023F0C  bls       0x023f16
0x023F0E  mov.w     #0x0053, r0
0x023F12  mov.w     r0, @er4
0x023F14  bt        0x023f92
0x023F16  mov.b     r5h, r0l
0x023F18  extu.w    r0
0x023F1A  extu.l    er0
0x023F1C  shll.l    #2, er0
0x023F1E  mov.l     er3, @(0x4203f8,er0)
0x023F28  mov.l     @(0x41c,sp), er1
0x023F2E  mov.l     er1, @(0x420308,er0)
0x023F38  mov.l     @(0x412,sp), er1
0x023F3E  sub.l     er3, er1
0x023F40  inc.l     #1, er1
0x023F42  mov.l     er1, @(0x4205d8,er0)
0x023F4C  mov.l     @(0x416,sp), er1
0x023F52  mov.l     @(0x41c,sp), er2
0x023F58  sub.l     er2, er1
0x023F5A  inc.l     #1, er1
0x023F5C  mov.l     er1, @(0x4204e8,er0)
0x023F66  inc.b     #1, r5h
0x023F68  mov.b     @0x40041a, r0l
0x023F6E  cmp.b     r0l, r5h
0x023F70  bcs       0x023da0
0x023F74  mov.b     #0x01, r0l
0x023F76  mov.b     r0l, @0x420267
0x023F7C  bt        0x023f92
0x023F7E  mov.w     @(0x422,sp), r1
0x023F82  mov.l     er3, er0
0x023F84  jsr       0x0118e8
0x023F88  sub.b     r0l, r0l
0x023F8A  mov.b     r0l, @0x400d74
0x023F90  mov.w     @er4, r0
0x023F92  add.l     #0x00000424, sp
0x023F98  ldm.l     @sp+, er4-er6
0x023F9C  ldm.l     @sp+, er2-er3
0x023FA0  rts       
