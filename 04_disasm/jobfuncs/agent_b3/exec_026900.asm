0x026900  mov.b     @(0x2,er4), r0l   ; 6e 48 00 02
0x026904  cmp.b     #0x03, r0l   ; a8 03
0x026906  bne       0x02691a   ; 46 12
0x026908  mov.l     #0x00008000, er6   ; 7a 06 00 00 80 00
0x02690E  inc.l     #1, er6   ; 0b 76
0x026910  mov.w     r5, r1   ; 0d 51
0x026912  mov.l     er6, er0   ; 0f e0
0x026914  jsr       0x011900   ; 5e 01 19 00
0x026918  bt        0x026940   ; 40 26
0x02691A  mov.b     @(0x2,er4), r4l   ; 6e 4c 00 02
0x02691E  cmp.b     #0x04, r4l   ; ac 04
0x026920  bne       0x02693a   ; 46 18
0x026922  cmp.l     #0x00000010, er5   ; 7a 25 00 00 00 10
0x026928  bhi       0x02693a   ; 42 10
0x02692A  mov.l     #0x00006010, er6   ; 7a 06 00 00 60 10
0x026930  mov.w     r5, r1   ; 0d 51
0x026932  mov.l     er6, er0   ; 0f e0
0x026934  jsr       0x011900   ; 5e 01 19 00
0x026938  bt        0x026940   ; 40 06
0x02693A  mov.w     #0x0050, r0   ; 79 00 00 50
0x02693E  mov.w     r0, @er3   ; 69 b0
0x026940  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x026944  ldm.l     @sp+, er2-er3   ; 01 10 6d 73
0x026948  rts          ; 54 70
0x02694A  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x02694E  mov.l     #0x00400436, er4   ; 7a 04 00 40 04 36
0x026954  mov.l     #0x0040043c, er5   ; 7a 05 00 40 04 3c
0x02695A  mov.b     @(0x1,er5), r0l   ; 6e 58 00 01
0x02695E  and.b     #0x1f, r0l   ; e8 1f
0x026960  bne       0x026972   ; 46 10
0x026962  mov.b     #0x02, r6l   ; fe 02
0x026964  bt        0x02697c   ; 40 16
0x026966  mov.b     r6l, r0l   ; 0c e8
0x026968  extu.w    r0   ; 17 50
0x02696A  extu.l    er0   ; 17 70
0x02696C  add.l     er5, er0   ; 0a d0
0x02696E  mov.b     @er0, r1l   ; 68 09
0x026970  beq       0x02697a   ; 47 08
0x026972  mov.w     #0x0050, r0   ; 79 00 00 50
0x026976  mov.w     r0, @er4   ; 69 c0
0x026978  bt        0x0269a0   ; 40 26
0x02697A  inc.b     #1, r6l   ; 0a 0e
0x02697C  cmp.b     #0x06, r6l   ; ae 06
0x02697E  bcs       0x026966   ; 45 e6
0x026980  mov.l     #0x00400400, er6   ; 7a 06 00 40 04 00
0x026986  btst      #6, @er6   ; 7c 60 73 60
0x02698A  beq       0x0269a0   ; 47 14
0x02698C  bset      #7, @er6   ; 7d 60 70 70
0x026990  mov.b     #0x01, r0l   ; f8 01
0x026992  mov.b     r0l, @0x4007c8   ; 6a a8 00 40 07 c8
0x026998  sub.w     r0, r0   ; 19 00
0x02699A  mov.w     r0, @0x400438   ; 6b a0 00 40 04 38
0x0269A0  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x0269A4  rts          ; 54 70
0x0269A6  mov.l     er3, @-sp   ; 01 00 6d f3
0x0269AA  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x0269AE  mov.l     #0x0040043c, er3   ; 7a 03 00 40 04 3c
0x0269B4  mov.l     #0x00400436, er4   ; 7a 04 00 40 04 36
0x0269BA  mov.l     #0x00400c55, er6   ; 7a 06 00 40 0c 55
0x0269C0  mov.b     @(0x1,er3), r0l   ; 6e 38 00 01
0x0269C4  and.b     #0x1f, r0l   ; e8 1f
0x0269C6  bne       0x0269d8   ; 46 10
0x0269C8  mov.b     #0x02, r5l   ; fd 02
0x0269CA  bt        0x0269e2   ; 40 16
0x0269CC  mov.b     r5l, r0l   ; 0c d8
0x0269CE  extu.w    r0   ; 17 50
0x0269D0  extu.l    er0   ; 17 70
0x0269D2  add.l     er3, er0   ; 0a b0
0x0269D4  mov.b     @er0, r1l   ; 68 09
0x0269D6  beq       0x0269e0   ; 47 08
0x0269D8  mov.w     #0x0050, r0   ; 79 00 00 50
0x0269DC  jmp       0x026bce   ; 5a 02 6b ce
0x0269E0  inc.b     #1, r5l   ; 0a 0d
0x0269E2  cmp.b     #0x06, r5l   ; ad 06
0x0269E4  bcs       0x0269cc   ; 45 e6
0x0269E6  mov.l     #0x00400410, er5   ; 7a 05 00 40 04 10
0x0269EC  mov.b     @er6, r0l   ; 68 68
0x0269EE  cmp.b     #0x40, r0l   ; a8 40
0x0269F0  beq       0x026a3e   ; 47 4c
0x0269F2  cmp.b     #0x41, r0l   ; a8 41
0x0269F4  beq       0x026a3e   ; 47 48
0x0269F6  cmp.b     #0x42, r0l   ; a8 42
0x0269F8  beq       0x026a3e   ; 47 44
0x0269FA  cmp.b     #0x80, r0l   ; a8 80
0x0269FC  beq       0x026a2e   ; 47 30
0x0269FE  cmp.b     #0x81, r0l   ; a8 81
0x026A00  beq       0x026bd2   ; 58 70 01 ce
0x026A04  cmp.b     #0x91, r0l   ; a8 91
0x026A06  beq       0x026bb2   ; 58 70 01 a8
0x026A0A  cmp.b     #0x92, r0l   ; a8 92
0x026A0C  beq       0x026bbe   ; 58 70 01 ae
0x026A10  cmp.b     #0xa0, r0l   ; a8 a0
0x026A12  beq       0x026a92   ; 47 7e
0x026A14  cmp.b     #0xb0, r0l   ; a8 b0
0x026A16  beq       0x026bd2   ; 58 70 01 b8
0x026A1A  cmp.b     #0xb3, r0l   ; a8 b3
0x026A1C  beq       0x026b0a   ; 58 70 00 ea
0x026A20  cmp.b     #0xc1, r0l   ; a8 c1
0x026A22  beq       0x026a54   ; 47 30
0x026A24  cmp.b     #0xd0, r0l   ; a8 d0
0x026A26  beq       0x026bd2   ; 58 70 01 a8
0x026A2A  jmp       0x026bca   ; 5a 02 6b ca
0x026A2E  mov.b     #0x01, r0l   ; f8 01
0x026A30  mov.b     r0l, @0x400d3b   ; 6a a8 00 40 0d 3b
0x026A36  jmp       0x026bee   ; 5a 02 6b ee
0x026A3A  jmp       0x026bd2   ; 5a 02 6b d2
0x026A3E  mov.b     @(0xa,er6), r0l   ; 6e 68 00 0a
0x026A42  extu.w    r0   ; 17 50
0x026A44  mov.b     r0l, r0h   ; 0c 80
0x026A46  sub.b     r0l, r0l   ; 18 88
0x026A48  mov.b     @(0xb,er6), r1l   ; 6e 69 00 0b
0x026A4C  extu.w    r1   ; 17 51
0x026A4E  add.w     r1, r0   ; 09 10
0x026A50  sub.w     r0, r0   ; 19 00
0x026A52  mov.w     r0, @er5   ; 69 d0
0x026A54  sub.l     er0, er0   ; 1a 80
0x026A56  mov.b     @(0x2,er6), r0l   ; 6e 68 00 02
0x026A5A  mov.b     r0l, r0h   ; 0c 80
0x026A5C  sub.b     r0l, r0l   ; 18 88
0x026A5E  mov.w     r0, e0   ; 0d 08
0x026A60  sub.w     r0, r0   ; 19 00
0x026A62  sub.l     er1, er1   ; 1a 91
0x026A64  mov.b     @(0x3,er6), r1l   ; 6e 69 00 03
0x026A68  mov.w     r1, e1   ; 0d 19
0x026A6A  sub.w     r1, r1   ; 19 11
0x026A6C  add.l     er1, er0   ; 0a 90
0x026A6E  sub.l     er1, er1   ; 1a 91
0x026A70  mov.b     @(0x4,er6), r1l   ; 6e 69 00 04
0x026A74  shll.l    #2, er1   ; 10 71
0x026A76  shll.l    #2, er1   ; 10 71
0x026A78  shll.l    #2, er1   ; 10 71
0x026A7A  shll.l    #2, er1   ; 10 71
0x026A7C  add.l     er1, er0   ; 0a 90
0x026A7E  sub.l     er1, er1   ; 1a 91
0x026A80  mov.b     @(0x5,er6), r1l   ; 6e 69 00 05
0x026A84  add.l     er1, er0   ; 0a 90
0x026A86  mov.l     er0, @0x400408   ; 01 00 6b a0 00 40 04 08
0x026A8E  jmp       0x026bd2   ; 5a 02 6b d2
