0x030A46  mov.l     @(0x2c,sp), er0
0x030A4C  sub.l     er1, er1
0x030A4E  mov.b     @er0, r1l
0x030A50  shll.l    #2, er1
0x030A52  shll.l    #2, er1
0x030A54  sub.l     er6, er6
0x030A56  mov.b     @er4, r6l
0x030A58  sub.l     er0, er0
0x030A5A  mov.b     @(0x41ff6e,er6), r0l
0x030A62  shll.l    #2, er0
0x030A64  shll.l    er0
0x030A66  add.l     #0x0003f74a, er1
0x030A6C  add.l     er1, er0
0x030A6E  mov.l     er6, er1
0x030A70  shll.l    er1
0x030A72  add.l     er1, er0
0x030A74  mov.w     @er0, r0
0x030A76  extu.l    er0
0x030A78  mov.w     @0x400d6a, r1
0x030A7E  extu.l    er1
0x030A80  mov.w     #0x0003, r2
0x030A84  divxu.w   r2, er1
0x030A86  extu.l    er1
0x030A88  jsr       0x018e1e
0x030A8C  mov.l     #0x00000064, er1
0x030A92  jsr       0x018708
0x030A96  mov.l     er0, @(0x60,sp)
0x030A9C  bsr       0x032d2c
0x030AA0  sub.l     er0, er0
0x030AA2  mov.b     @er4, r0l
0x030AA4  mov.b     @(0x41ff6e,er0), r0h
0x030AAC  mov.b     @er4, r0l
0x030AAE  jsr       0x02daa2
0x030AB2  sub.b     r6h, r6h
0x030AB4  sub.b     r0l, r0l
0x030AB6  mov.b     r0l, @(0x59,sp)
0x030ABA  mov.l     @(0x30,sp), er0
0x030AC0  mov.w     #0x01fe, r1
0x030AC4  mov.w     r1, @er0
0x030AC6  mov.l     @(0x34,sp), er0
0x030ACC  mov.w     r1, @er0
0x030ACE  mov.w     r1, @er3
0x030AD0  mov.l     @(0x24,sp), er0
0x030AD6  sub.w     r1, r1
0x030AD8  mov.w     r1, @er0
0x030ADA  mov.l     @(0x28,sp), er0
0x030AE0  mov.w     r1, @er0
0x030AE2  mov.w     r1, @(0x14,sp)
0x030AE6  mov.l     @(0x38,sp), er0
0x030AEC  mov.w     #0x00ff, r1
0x030AF0  mov.w     r1, @er0
0x030AF2  mov.l     @(0x20,sp), er0
0x030AF8  mov.w     r1, @er0
0x030AFA  mov.w     r1, @er5
0x030AFC  mov.w     #0x0080, e6
0x030B00  mov.l     er5, er1
0x030B02  mov.b     @er4, r0l
0x030B04  jsr       0x03a2d8
0x030B08  bsr       0x0330aa
0x030B0C  btst      #7, @0x400400
0x030B14  bne       0x030f6e
0x030B18  sub.b     r6l, r6l
0x030B1A  jmp       0x030d12
0x030B1E  mov.b     r6l, r0l
0x030B20  extu.w    r0
0x030B22  mov.w     #0x0001, r1
0x030B26  dec.b     #1, r0l
0x030B28  bmi       0x030b2e
0x030B2A  shll.w    r1
0x030B2C  bt        0x030b26
0x030B2E  mov.b     r6h, r0l
0x030B30  extu.w    r0
0x030B32  and.w     r0, r1
0x030B34  bne       0x030d10
0x030B38  mov.b     r6l, r0l
0x030B3A  extu.w    r0
0x030B3C  extu.l    er0
0x030B3E  shll.l    #2, er0
0x030B40  mov.l     @(0x41ff7c,er0), er0
0x030B4A  mov.l     @(0x60,sp), er1
0x030B50  cmp.l     er1, er0
0x030B52  bge       0x030bb2
0x030B54  mov.b     r6l, r0l
0x030B56  extu.w    r0
0x030B58  extu.l    er0
0x030B5A  shll.l    er0
0x030B5C  mov.l     #0x00000014, er1
0x030B62  add.l     sp, er1
0x030B64  add.l     er0, er1
0x030B66  add.l     er5, er0
0x030B68  mov.l     er0, @(0x44,sp)
0x030B6E  mov.w     @er0, r0
0x030B70  mov.w     r0, @er1
0x030B72  mov.l     @(0x44,sp), er0
0x030B78  mov.w     @er0, r0
0x030B7A  add.w     e6, r0
0x030B7C  cmp.w     #0x01fe, r0
0x030B80  bhi       0x030b9e
0x030B82  mov.b     r6l, r0l
0x030B84  extu.w    r0
0x030B86  extu.l    er0
0x030B88  shll.l    er0
0x030B8A  add.l     er5, er0
0x030B8C  mov.l     er0, @(0x44,sp)
0x030B92  mov.l     @(0x44,sp), er1
0x030B98  mov.w     @er1, r1
0x030B9A  add.w     e6, r1
0x030B9C  bt        0x030bac
0x030B9E  mov.b     r6l, r0l
0x030BA0  extu.w    r0
0x030BA2  extu.l    er0
0x030BA4  shll.l    er0
0x030BA6  add.l     er5, er0
0x030BA8  mov.w     #0x01fe, r1
0x030BAC  mov.w     r1, @er0
0x030BAE  jmp       0x030c3a
0x030BB2  mov.b     r6l, r0l
0x030BB4  extu.w    r0
0x030BB6  extu.l    er0
0x030BB8  shll.l    #2, er0
0x030BBA  mov.l     @(0x41ff7c,er0), er0
0x030BC4  mov.l     @(0x60,sp), er1
0x030BCA  cmp.l     er1, er0
0x030BCC  ble       0x030c28
0x030BCE  mov.b     r6l, r0l
0x030BD0  extu.w    r0
0x030BD2  extu.l    er0
0x030BD4  shll.l    er0
0x030BD6  mov.l     er0, @(0x40,sp)
0x030BDC  add.l     er3, er0
0x030BDE  mov.l     @(0x40,sp), er1
0x030BE4  add.l     er5, er1
0x030BE6  mov.l     er1, @(0x44,sp)
0x030BEC  mov.w     @er1, r1
0x030BEE  mov.w     r1, @er0
0x030BF0  mov.l     @(0x44,sp), er0
0x030BF6  mov.w     @er0, r0
0x030BF8  cmp.w     e6, r0
0x030BFA  bcs       0x030c18
0x030BFC  mov.b     r6l, r0l
0x030BFE  extu.w    r0
0x030C00  extu.l    er0
0x030C02  shll.l    er0
0x030C04  add.l     er5, er0
0x030C06  mov.l     er0, @(0x44,sp)
0x030C0C  mov.l     @(0x44,sp), er1
0x030C12  mov.w     @er1, r1
0x030C14  sub.w     e6, r1
0x030C16  bt        0x030c24
0x030C18  mov.b     r6l, r0l
0x030C1A  extu.w    r0
0x030C1C  extu.l    er0
0x030C1E  shll.l    er0
0x030C20  add.l     er5, er0
0x030C22  sub.w     r1, r1
0x030C24  mov.w     r1, @er0
0x030C26  bt        0x030c3a
0x030C28  mov.b     r6l, r0l
0x030C2A  extu.w    r0
0x030C2C  mov.w     #0x0001, r1
0x030C30  dec.b     #1, r0l
0x030C32  bmi       0x030d06
0x030C36  shll.w    r1
0x030C38  bt        0x030c30
0x030C3A  mov.b     r6l, r0l
0x030C3C  extu.w    r0
0x030C3E  extu.l    er0
0x030C40  shll.l    er0
0x030C42  mov.l     er0, @(0x44,sp)
0x030C48  add.l     er3, er0
0x030C4A  mov.l     #0x00000014, er1
0x030C50  add.l     sp, er1
0x030C52  mov.l     @(0x44,sp), er2
0x030C58  add.l     er2, er1
0x030C5A  mov.w     @er0, r0
0x030C5C  mov.w     @er1, r1
0x030C5E  cmp.w     r1, r0
0x030C60  bcs       0x030cbe
0x030C62  mov.b     r6l, r0l
0x030C64  extu.w    r0
0x030C66  extu.l    er0
0x030C68  shll.l    er0
0x030C6A  mov.l     er0, @(0x44,sp)
0x030C70  add.l     er3, er0
0x030C72  mov.l     #0x00000014, er1
0x030C78  add.l     sp, er1
0x030C7A  mov.l     @(0x44,sp), er2
0x030C80  add.l     er2, er1
0x030C82  mov.w     @er0, r0
0x030C84  mov.w     @er1, r1
0x030C86  sub.w     r1, r0
0x030C88  cmp.w     #0x0001, r0
0x030C8C  bhi       0x030d10
0x030C90  mov.b     r6l, r0l
0x030C92  extu.w    r0
0x030C94  extu.l    er0
0x030C96  shll.l    er0
0x030C98  mov.l     er0, @(0x44,sp)
0x030C9E  add.l     er5, er0
0x030CA0  mov.l     @(0x44,sp), er1
0x030CA6  add.l     er3, er1
0x030CA8  mov.w     @er1, r1
0x030CAA  mov.w     r1, @er0
0x030CAC  mov.b     r6l, r0l
0x030CAE  extu.w    r0
0x030CB0  mov.w     #0x0001, r1
0x030CB4  dec.b     #1, r0l
0x030CB6  bmi       0x030cbc
0x030CB8  shll.w    r1
0x030CBA  bt        0x030cb4
0x030CBC  bt        0x030d06
0x030CBE  mov.b     r6l, r0l
0x030CC0  extu.w    r0
0x030CC2  extu.l    er0
0x030CC4  shll.l    er0
0x030CC6  mov.l     er0, er2
0x030CC8  add.l     er5, er0
0x030CCA  mov.l     er2, er1
0x030CCC  add.l     er3, er1
0x030CCE  mov.l     er1, @(0x44,sp)
0x030CD4  mov.w     @er1, r1
0x030CD6  mov.w     r1, @er0
0x030CD8  mov.l     #0x00000014, er0
0x030CDE  add.l     sp, er0
0x030CE0  mov.l     er2, er1
0x030CE2  add.l     er1, er0
0x030CE4  mov.l     @(0x44,sp), er1
0x030CEA  mov.w     @er0, r0
0x030CEC  mov.w     @er1, r1
0x030CEE  sub.w     r1, r0
0x030CF0  cmp.w     #0x0002, r0
0x030CF4  bhi       0x030d0a
0x030CF6  mov.b     r6l, r0l
0x030CF8  extu.w    r0
0x030CFA  mov.w     #0x0001, r1
0x030CFE  dec.b     #1, r0l
0x030D00  bmi       0x030d06
0x030D02  shll.w    r1
0x030D04  bt        0x030cfe
0x030D06  or.b      r1l, r6h
0x030D08  bt        0x030d10
0x030D0A  sub.b     r0l, r0l
0x030D0C  mov.b     r0l, @(0x59,sp)
0x030D10  inc.b     #1, r6l
0x030D12  cmp.b     #0x03, r6l
0x030D14  bcs       0x030b1e
0x030D18  mov.b     r6h, r0l
0x030D1A  and.b     #0x07, r0l
0x030D1C  cmp.b     #0x07, r0l
0x030D1E  bne       0x030d28
0x030D20  mov.b     #0x01, r0l
0x030D22  mov.b     r0l, @(0x59,sp)
0x030D26  bt        0x030d32
0x030D28  mov.w     e6, e6
0x030D2A  beq       0x030d32
0x030D2C  shlr.w    e6
0x030D2E  jmp       0x030b00
0x030D32  mov.b     @(0x59,sp), r0l
0x030D36  bne       0x030d56
0x030D38  mov.b     @er4, r0l
0x030D3A  extu.w    r0
0x030D3C  inc.w     #1, r0
0x030D3E  or.w      #0x0810, r0
0x030D42  mov.w     r0, @0x400402
0x030D48  mov.l     #0x004206ed, er0
0x030D4E  mov.b     @er0, r1l
0x030D50  and.b     #0x0b, r1l
0x030D52  jmp       0x030f5c
0x030D56  and.b     #0x0f, r6h
0x030D58  sub.b     r0l, r0l
0x030D5A  mov.b     r0l, @(0x51,sp)
0x030D5E  mov.w     #0x0001, e6
0x030D62  sub.w     r0, r0
0x030D64  jmp       0x030f36
0x030D68  mov.l     er5, er1
0x030D6A  mov.b     @er4, r0l
0x030D6C  jsr       0x03a2d8
0x030D70  mov.b     #0x02, r0l
0x030D72  bsr       0x0330fa
0x030D76  btst      #7, @0x400400
0x030D7E  bne       0x030f6e
0x030D82  sub.b     r6l, r6l
0x030D84  jmp       0x030f1a
0x030D88  mov.b     r6l, r0l
0x030D8A  extu.w    r0
0x030D8C  mov.w     #0x0010, r1
0x030D90  dec.b     #1, r0l
0x030D92  bmi       0x030d98
0x030D94  shll.w    r1
0x030D96  bt        0x030d90
0x030D98  mov.b     r6h, r0l
0x030D9A  extu.w    r0
0x030D9C  and.w     r0, r1
0x030D9E  bne       0x030f18
0x030DA2  mov.b     r6l, r0l
0x030DA4  extu.w    r0
0x030DA6  extu.l    er0
0x030DA8  shll.l    #2, er0
0x030DAA  mov.l     @(0x41ff7c,er0), er0
0x030DB4  mov.l     @(0x60,sp), er1
0x030DBA  cmp.l     er1, er0
0x030DBC  bge       0x030df6
0x030DBE  mov.b     r6l, r0l
0x030DC0  extu.w    r0
0x030DC2  extu.l    er0
0x030DC4  shll.l    er0
0x030DC6  add.l     er5, er0
0x030DC8  mov.w     @er0, r0
0x030DCA  add.w     e6, r0
0x030DCC  cmp.w     #0x01fe, r0
0x030DD0  bcc       0x030de2
0x030DD2  mov.b     r6l, r0l
0x030DD4  extu.w    r0
0x030DD6  extu.l    er0
0x030DD8  shll.l    er0
0x030DDA  add.l     er5, er0
0x030DDC  mov.w     @er0, r1
0x030DDE  add.w     e6, r1
0x030DE0  bt        0x030df0
0x030DE2  mov.b     r6l, r0l
0x030DE4  extu.w    r0
0x030DE6  extu.l    er0
0x030DE8  shll.l    er0
0x030DEA  add.l     er5, er0
0x030DEC  mov.w     #0x01fe, r1
0x030DF0  mov.w     r1, @er0
0x030DF2  jmp       0x030f18
0x030DF6  mov.b     r6l, r0l
0x030DF8  extu.w    r0
0x030DFA  extu.l    er0
0x030DFC  mov.l     er0, @(0x48,sp)
0x030E02  shll.l    er0
0x030E04  mov.l     er0, @(0x5a,sp)
0x030E0A  mov.b     @er4, r1l
0x030E0C  extu.w    r1
0x030E0E  mov.w     #0x0006, e1
0x030E12  mulxu.w   e1, er1
0x030E14  add.l     #0x0041ff3e, er1
0x030E1A  add.l     er0, er1
0x030E1C  add.l     er5, er0
0x030E1E  mov.l     er0, @(0x4c,sp)
0x030E24  mov.w     @er0, r0
0x030E26  mov.w     r0, @er1
0x030E28  mov.l     @(0x4c,sp), er0
0x030E2E  mov.b     @er4, r1l
0x030E30  extu.w    r1
0x030E32  mov.w     #0x0006, e1
0x030E36  mulxu.w   e1, er1
0x030E38  mov.l     @(0x3c,sp), er2
0x030E3E  add.l     er1, er2
0x030E40  mov.l     @(0x5a,sp), er1
0x030E46  add.l     er1, er2
0x030E48  mov.w     @er0, r0
0x030E4A  mov.w     r0, @er2
0x030E4C  mov.l     @(0x48,sp), er0
0x030E52  shll.l    #2, er0
0x030E54  mov.l     @(0x41ff88,er0), er0
0x030E5E  shlr.l    er0
0x030E60  mov.w     r0, @(0x5e,sp)
0x030E64  bne       0x030e6e
0x030E66  mov.w     #0x0001, r0
0x030E6A  mov.w     r0, @(0x5e,sp)
0x030E6E  mov.b     r6l, r0l
0x030E70  extu.w    r0
0x030E72  extu.l    er0
0x030E74  mov.l     er0, @(0x4c,sp)
0x030E7A  shll.l    er0
0x030E7C  mov.l     er0, @(0x48,sp)
0x030E82  mov.b     @er4, r1l
0x030E84  extu.w    r1
0x030E86  mov.w     #0x0006, e1
0x030E8A  mulxu.w   e1, er1
0x030E8C  add.l     #0x0041ff56, er1
0x030E92  add.l     er0, er1
0x030E94  mov.l     @(0x4c,sp), er0
0x030E9A  shll.l    #2, er0
0x030E9C  mov.l     @(0x41ff7c,er0), er0
0x030EA6  mov.l     @(0x60,sp), er2
0x030EAC  sub.l     er2, er0
0x030EAE  mov.w     @(0x5e,sp), r2
0x030EB2  extu.l    er2
0x030EB4  mov.l     er1, @sp
0x030EB8  mov.l     er2, er1
0x030EBA  jsr       0x018708
0x030EBE  mov.l     @sp, er1
0x030EC2  mov.w     r0, @er1
0x030EC4  mov.b     @er4, r0l
0x030EC6  extu.w    r0
0x030EC8  mov.w     #0x0006, e0
0x030ECC  mulxu.w   e0, er0
0x030ECE  add.l     #0x0041ff56, er0
0x030ED4  mov.l     @(0x48,sp), er1
0x030EDA  add.l     er1, er0
0x030EDC  mov.w     @er0, r1
0x030EDE  beq       0x030f06
0x030EE0  jsr       0x010b56
0x030EE4  mov.b     @er4, r0l
0x030EE6  extu.w    r0
0x030EE8  mov.w     #0x0006, e0
0x030EEC  mulxu.w   e0, er0
0x030EEE  mov.b     r6l, r1l
0x030EF0  extu.w    r1
0x030EF2  extu.l    er1
0x030EF4  shll.l    er1
0x030EF6  add.l     #0x0041ff56, er0
0x030EFC  add.l     er1, er0
0x030EFE  mov.w     @er0, e0
0x030F00  mov.b     r6l, r0l
0x030F02  jsr       0x03ddb2
0x030F06  mov.b     r6l, r0l
0x030F08  extu.w    r0
0x030F0A  mov.w     #0x0010, r1
0x030F0E  dec.b     #1, r0l
0x030F10  bmi       0x030f16
0x030F12  shll.w    r1
0x030F14  bt        0x030f0e
0x030F16  or.b      r1l, r6h
0x030F18  inc.b     #1, r6l
0x030F1A  cmp.b     #0x03, r6l
0x030F1C  bcs       0x030d88
0x030F20  mov.b     r6h, r0l
0x030F22  and.b     #0x70, r0l
0x030F24  cmp.b     #0x70, r0l
0x030F26  bne       0x030f30
0x030F28  mov.b     #0x01, r0l
0x030F2A  mov.b     r0l, @(0x51,sp)
0x030F2E  bt        0x030f42
0x030F30  mov.w     @(0x52,sp), r0
0x030F34  inc.w     #1, r0
0x030F36  mov.w     r0, @(0x52,sp)
0x030F3A  cmp.w     #0x0040, r0
0x030F3E  bcs       0x030d68
0x030F42  mov.b     @(0x51,sp), r0l
0x030F46  bne       0x030f60
0x030F48  mov.w     #0x0810, r0
0x030F4C  mov.w     r0, @0x400402
0x030F52  mov.l     #0x004206ed, er0
0x030F58  mov.b     @er0, r1l
0x030F5A  and.b     #0x0d, r1l
0x030F5C  mov.b     r1l, @er0
0x030F5E  bt        0x030f6e
0x030F60  mov.b     @er4, r0l
0x030F62  inc.b     #1, r0l
0x030F64  mov.b     r0l, @er4
0x030F66  mov.b     @er4, r0l
0x030F68  cmp.b     #0x04, r0l
0x030F6A  bcs       0x030a46
0x030F6E  sub.b     r0l, r0l
0x030F70  mov.b     r0l, @0x2001c1
0x030F76  mov.b     #0x80, r0l
0x030F78  mov.b     r0l, @0x200001
0x030F7E  add.l     #0x00000064, sp
0x030F84  ldm.l     @sp+, er4-er6
0x030F88  ldm.l     @sp+, er2-er3
0x030F8C  rts       
