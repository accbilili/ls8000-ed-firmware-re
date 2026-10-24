0x027F44  stm.l     er2-er3, @-sp
0x027F48  stm.l     er4-er6, @-sp
0x027F4C  sub.l     #0x00000010, sp
0x027F52  mov.l     #0x00400402, er4
0x027F58  mov.l     #0x004007ca, er6
0x027F5E  sub.b     r0l, r0l
0x027F60  mov.b     r0l, @0x41ffa6
0x027F66  mov.b     #0x01, r0l
0x027F68  mov.b     r0l, @0x4007c9
0x027F6E  sub.b     r0l, r0l
0x027F70  mov.b     r0l, @er6
0x027F72  bsr       0x028148
0x027F76  mov.b     #0x02, r0l
0x027F78  mov.b     r0l, @er6
0x027F7A  bsr       0x028148
0x027F7E  mov.b     #0x03, r0l
0x027F80  mov.b     r0l, @er6
0x027F82  bsr       0x028148
0x027F86  mov.b     #0x04, r0l
0x027F88  mov.b     r0l, @er6
0x027F8A  bsr       0x028148
0x027F8E  mov.l     #0x008cc000, er2
