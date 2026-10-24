0x02B1E4  stm.l     er4-er5, @-sp
0x02B1E8  mov.l     er0, er4
0x02B1EA  mov.l     @(0xc,sp), er5
0x02B1F0  cmp.l     #0x00010000, er4
0x02B1F6  bcc       0x02b200
0x02B1F8  mov.w     r4, @er5
0x02B1FA  mov.b     #0x01, r0l
0x02B1FC  mov.b     r0l, @er1
0x02B1FE  bt        0x02b228
0x02B200  cmp.l     #0x007fffff, er4
0x02B206  bcc       0x02b21e
0x02B208  mov.w     r4, r0
0x02B20A  bclr      #7, r0h
0x02B20C  add.w     #0x8000, r0
0x02B210  mov.w     r0, @er5
0x02B212  mov.b     #0x0f, r0l
0x02B214  shlr.l    er4
0x02B216  dec.b     #1, r0l
0x02B218  bgt       0x02b214
0x02B21A  mov.b     r4l, @er1
0x02B21C  bt        0x02b228
0x02B21E  mov.w     #0xffff, r0
0x02B222  mov.w     r0, @er5
0x02B224  mov.b     #0xff, r0l
0x02B226  mov.b     r0l, @er1
0x02B228  ldm.l     @sp+, er4-er5
0x02B22C  rts       
