0x02F68C  sub.l     er0, er0
0x02F68E  mov.b     @(0xfff7,er6), r0l
0x02F692  shll.l    #2, er0
0x02F694  mov.l     @(0xfff2,er6), er1
0x02F69A  add.l     er0, er1
0x02F69C  mov.l     @er1, er0
0x02F6A0  bne       0x02f6bc
0x02F6A2  sub.l     er0, er0
0x02F6A4  mov.b     @(0xfff7,er6), r0l
0x02F6A8  shll.l    #2, er0
0x02F6AA  mov.l     @(0xfff2,er6), er1
0x02F6B0  add.l     er0, er1
0x02F6B2  mov.l     #0x00000001, er0
0x02F6B8  mov.l     er0, @er1
0x02F6BC  mov.l     @(0xffee,er6), er0
0x02F6C2  mov.b     @(0x20,er0), r0l
0x02F6C6  cmp.b     #0x02, r0l
0x02F6C8  bne       0x02f7ba
0x02F6CC  sub.l     er0, er0
0x02F6CE  mov.b     @(0xfff7,er6), r0l
0x02F6D2  shll.l    #2, er0
0x02F6D4  shll.l    er0
0x02F6D6  sub.l     er1, er1
0x02F6D8  mov.b     @(0xfff7,er6), r1l
0x02F6DC  shll.l    #2, er1
0x02F6DE  mov.l     @(0xffee,er6), er2
0x02F6E4  add.l     er2, er1
0x02F6E6  mov.l     @er1, er1
0x02F6EA  mov.l     er0, @(0xffda,er6)
0x02F6F0  mov.l     #0xffffffde, er0
0x02F6F6  add.l     er6, er0
0x02F6F8  jsr       0x018e68
0x02F6FC  sub.l     er1, er1
0x02F6FE  mov.b     @(0xfff7,er6), r1l
0x02F702  shll.l    #2, er1
0x02F704  mov.l     @(0xfff2,er6), er2
0x02F70A  add.l     er2, er1
0x02F70C  mov.l     @er1, er1
0x02F710  mov.l     er0, @(0xffce,er6)
0x02F716  mov.l     #0xffffffd2, er0
0x02F71C  add.l     er6, er0
0x02F71E  jsr       0x018e68
0x02F722  mov.l     @(0xffce,er6), er1
0x02F728  mov.l     er0, er2
0x02F72A  mov.l     #0xffffffc6, er0
0x02F730  add.l     er6, er0
0x02F732  jsr       0x01842c
0x02F736  sub.l     er1, er1
0x02F738  mov.b     @(0xfff7,er6), r1l
0x02F73C  shll.l    er1
0x02F73E  mov.l     @(0xfff2,er6), er2
0x02F744  add.l     #0x00000010, er2
0x02F74A  add.l     er1, er2
0x02F74C  mov.w     @er2, r1
0x02F74E  mov.l     er0, @(0xffba,er6)
0x02F754  mov.l     #0xffffffbe, er0
0x02F75A  add.l     er6, er0
0x02F75C  jsr       0x018ede
0x02F760  sub.l     er1, er1
0x02F762  mov.b     @(0xfff7,er6), r1l
0x02F766  shll.l    er1
0x02F768  mov.l     @(0xffee,er6), er2
0x02F76E  add.l     #0x00000010, er2
0x02F774  add.l     er1, er2
0x02F776  mov.w     @er2, r1
0x02F778  mov.l     er0, @(0xffae,er6)
0x02F77E  mov.l     #0xffffffb2, er0
0x02F784  add.l     er6, er0
0x02F786  jsr       0x018ede
0x02F78A  mov.l     @(0xffae,er6), er1
0x02F790  mov.l     er0, er2
0x02F792  mov.l     #0xffffffa6, er0
0x02F798  add.l     er6, er0
0x02F79A  jsr       0x01842c
0x02F79E  mov.l     @(0xffba,er6), er1
0x02F7A4  mov.l     er0, er2
0x02F7A6  mov.l     @(0xffda,er6), er0
0x02F7AC  add.l     #0x00420108, er0
0x02F7B2  jsr       0x018aa0
0x02F7B6  jmp       0x02f8a4
0x02F7BA  sub.l     er0, er0
0x02F7BC  mov.b     @(0xfff7,er6), r0l
0x02F7C0  shll.l    #2, er0
0x02F7C2  shll.l    er0
0x02F7C4  sub.l     er1, er1
0x02F7C6  mov.b     @(0xfff7,er6), r1l
0x02F7CA  shll.l    #2, er1
0x02F7CC  mov.l     @(0xffee,er6), er2
0x02F7D2  add.l     er2, er1
0x02F7D4  mov.l     @er1, er1
0x02F7D8  mov.l     er0, @(0xffda,er6)
0x02F7DE  mov.l     #0xffffffde, er0
0x02F7E4  add.l     er6, er0
0x02F7E6  jsr       0x018e68
0x02F7EA  sub.l     er1, er1
0x02F7EC  mov.b     @(0xfff7,er6), r1l
0x02F7F0  shll.l    #2, er1
0x02F7F2  mov.l     @(0xfff2,er6), er2
0x02F7F8  add.l     er2, er1
0x02F7FA  mov.l     @er1, er1
0x02F7FE  mov.l     er0, @(0xffce,er6)
0x02F804  mov.l     #0xffffffd2, er0
0x02F80A  add.l     er6, er0
0x02F80C  jsr       0x018e68
0x02F810  mov.l     @(0xffce,er6), er1
0x02F816  mov.l     er0, er2
0x02F818  mov.l     #0xffffffc6, er0
0x02F81E  add.l     er6, er0
0x02F820  jsr       0x01842c
0x02F824  sub.l     er1, er1
0x02F826  mov.b     @(0xfff7,er6), r1l
0x02F82A  shll.l    er1
0x02F82C  mov.l     @(0xfff2,er6), er2
0x02F832  add.l     #0x00000018, er2
0x02F838  add.l     er1, er2
0x02F83A  mov.w     @er2, r1
0x02F83C  mov.l     er0, @(0xffba,er6)
0x02F842  mov.l     #0xffffffbe, er0
0x02F848  add.l     er6, er0
0x02F84A  jsr       0x018ede
0x02F84E  sub.l     er1, er1
0x02F850  mov.b     @(0xfff7,er6), r1l
0x02F854  shll.l    er1
0x02F856  mov.l     @(0xffee,er6), er2
0x02F85C  add.l     #0x00000018, er2
0x02F862  add.l     er1, er2
0x02F864  mov.w     @er2, r1
0x02F866  mov.l     er0, @(0xffae,er6)
0x02F86C  mov.l     #0xffffffb2, er0
0x02F872  add.l     er6, er0
0x02F874  jsr       0x018ede
0x02F878  mov.l     @(0xffae,er6), er1
0x02F87E  mov.l     er0, er2
0x02F880  mov.l     #0xffffffa6, er0
0x02F886  add.l     er6, er0
0x02F888  jsr       0x01842c
0x02F88C  mov.l     @(0xffba,er6), er1
0x02F892  mov.l     er0, er2
0x02F894  mov.l     @(0xffda,er6), er0
0x02F89A  add.l     #0x00420108, er0
0x02F8A0  jsr       0x018aa0
0x02F8A4  sub.l     er0, er0
0x02F8A6  mov.b     @(0xfff7,er6), r0l
0x02F8AA  shll.l    #2, er0
0x02F8AC  mov.l     @(0xfff2,er6), er1
0x02F8B2  add.l     er0, er1
0x02F8B4  sub.l     er0, er0
0x02F8B6  mov.b     @(0xfff7,er6), r0l
0x02F8BA  shll.l    #2, er0
0x02F8BC  mov.l     @er1, er1
0x02F8C0  mov.l     er1, @(0x400f32,er0)
0x02F8CA  mov.b     @(0xfff7,er6), r0l
0x02F8CE  inc.b     #1, r0l
0x02F8D0  mov.b     r0l, @(0xfff7,er6)
0x02F8D4  mov.b     @(0xfff7,er6), r0l
0x02F8D8  cmp.b     #0x04, r0l
0x02F8DA  bcs       0x02f68c
0x02F8DE  bt        0x02f93c
0x02F93C  jmp       0x02fa5a
0x02FA5A  add.l     #0x00000054, sp
0x02FA60  mov.w     @sp+, r5
0x02FA62  mov.l     @sp+, er2
0x02FA66  mov.l     @sp+, er6
0x02FA6A  rts       
