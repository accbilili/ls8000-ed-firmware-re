0x037C6A  stm.l     er2-er3, @-sp
0x037C6E  stm.l     er4-er6, @-sp
0x037C72  sub.l     #0x0000002c, sp
0x037C78  mov.l     #0x00400f32, er4
0x037C7E  mov.l     #0x00400e0c, er5
0x037C84  sub.b     r6h, r6h
0x037C86  mov.l     er5, er0
0x037C88  adds.l    #4, er0
0x037C8A  mov.l     er0, @(0x28,sp)
0x037C90  mov.l     er4, er0
0x037C92  adds.l    #4, er0
0x037C94  mov.l     er0, @(0x14,sp)
0x037C9A  mov.l     er5, er0
0x037C9C  adds.l    #4, er0
0x037C9E  adds.l    #4, er0
0x037CA0  mov.l     er0, @(0x18,sp)
0x037CA6  mov.l     er4, er0
0x037CA8  adds.l    #4, er0
0x037CAA  adds.l    #4, er0
0x037CAC  mov.l     er0, @(0x24,sp)
0x037CB2  mov.l     er5, er0
0x037CB4  add.l     #0x0000000c, er0
0x037CBA  mov.l     er0, @(0x20,sp)
0x037CC0  mov.l     er4, er0
0x037CC2  add.l     #0x0000000c, er0
0x037CC8  mov.l     er0, @(0x1c,sp)
0x037CCE  jmp       0x037e4c
0x037CD2  mov.b     r6h, r0l
0x037CD4  extu.w    r0
0x037CD6  extu.l    er0
0x037CD8  mov.b     @(0x400dab,er0), r6l
0x037CE0  mov.b     @0x400db4, r0l
0x037CE6  cmp.b     #0x01, r0l
0x037CE8  bne       0x037d60
0x037CEA  cmp.b     #0x03, r6l
0x037CEC  beq       0x037d1c
0x037CEE  sub.l     er3, er3
0x037CF0  mov.b     r6l, r3l
0x037CF2  shll.l    #2, er3
0x037CF4  mov.l     er5, er0
0x037CF6  add.l     er3, er0
0x037CF8  mov.l     er4, er1
0x037CFA  add.l     er3, er1
0x037CFC  mov.l     @er1, er1
0x037D00  mov.l     er0, @(0x8,sp)
0x037D06  mov.l     #0x0000000c, er0
0x037D0C  add.l     sp, er0
0x037D0E  jsr       0x018e68
0x037D12  mov.l     er0, er1
0x037D14  mov.l     #0x0003f828, er2
0x037D1A  bt        0x037d48
0x037D1C  sub.l     er3, er3
0x037D1E  mov.b     r6l, r3l
0x037D20  shll.l    #2, er3
0x037D22  mov.l     er5, er0
0x037D24  add.l     er3, er0
0x037D26  mov.l     er4, er1
0x037D28  add.l     er3, er1
0x037D2A  mov.l     @er1, er1
0x037D2E  mov.l     er0, @(0x8,sp)
0x037D34  mov.l     #0x0000000c, er0
0x037D3A  add.l     sp, er0
0x037D3C  jsr       0x018e68
0x037D40  mov.l     er0, er1
0x037D42  mov.l     #0x0003f830, er2
0x037D48  mov.l     sp, er0
0x037D4A  jsr       0x018aa0
0x037D4E  jsr       0x01876a
0x037D52  mov.l     @(0x8,sp), er1
0x037D58  mov.l     er0, @er1
0x037D5C  jmp       0x037e4a
0x037D60  mov.b     r6l, r0l
0x037D62  beq       0x037d76
0x037D64  cmp.b     #0x01, r0l
0x037D66  beq       0x037da6
0x037D68  cmp.b     #0x02, r0l
0x037D6A  beq       0x037ddc
0x037D6C  cmp.b     #0x03, r0l
0x037D6E  beq       0x037e12
0x037D72  jmp       0x037e4a
0x037D76  mov.l     @er4, er1
0x037D7A  mov.l     #0x0000000c, er0
0x037D80  add.l     sp, er0
0x037D82  jsr       0x018e68
0x037D86  mov.l     er0, er1
0x037D88  mov.l     #0x0003f838, er2
0x037D8E  mov.l     #0x00000004, er0
0x037D94  add.l     sp, er0
0x037D96  jsr       0x018aa0
0x037D9A  jsr       0x01876a
0x037D9E  mov.l     er0, @er5
0x037DA2  jmp       0x037e4a
0x037DA6  mov.l     @(0x14,sp), er1
0x037DAC  mov.l     @er1, er1
0x037DB0  mov.l     #0x0000000c, er0
0x037DB6  add.l     sp, er0
0x037DB8  jsr       0x018e68
0x037DBC  mov.l     er0, er1
0x037DBE  mov.l     #0x0003f840, er2
0x037DC4  mov.l     #0x00000004, er0
0x037DCA  add.l     sp, er0
0x037DCC  jsr       0x018aa0
0x037DD0  jsr       0x01876a
0x037DD4  mov.l     @(0x28,sp), er1
0x037DDA  bt        0x037e46
0x037DDC  mov.l     @(0x24,sp), er1
0x037DE2  mov.l     @er1, er1
0x037DE6  mov.l     #0x0000000c, er0
0x037DEC  add.l     sp, er0
0x037DEE  jsr       0x018e68
0x037DF2  mov.l     er0, er1
0x037DF4  mov.l     #0x0003f848, er2
0x037DFA  mov.l     #0x00000004, er0
0x037E00  add.l     sp, er0
0x037E02  jsr       0x018aa0
0x037E06  jsr       0x01876a
0x037E0A  mov.l     @(0x18,sp), er1
0x037E10  bt        0x037e46
0x037E12  mov.l     @(0x1c,sp), er1
0x037E18  mov.l     @er1, er1
0x037E1C  mov.l     #0x0000000c, er0
0x037E22  add.l     sp, er0
0x037E24  jsr       0x018e68
0x037E28  mov.l     er0, er1
0x037E2A  mov.l     #0x0003f830, er2
0x037E30  mov.l     #0x00000004, er0
0x037E36  add.l     sp, er0
0x037E38  jsr       0x018aa0
0x037E3C  jsr       0x01876a
0x037E40  mov.l     @(0x20,sp), er1
0x037E46  mov.l     er0, @er1
0x037E4A  inc.b     #1, r6h
0x037E4C  mov.b     @0x400daa, r0l
0x037E52  cmp.b     r0l, r6h
0x037E54  bcs       0x037cd2
0x037E58  add.l     #0x0000002c, sp
0x037E5E  ldm.l     @sp+, er4-er6
0x037E62  ldm.l     @sp+, er2-er3
0x037E66  rts       
