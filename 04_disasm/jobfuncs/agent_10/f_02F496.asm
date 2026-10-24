0x02F496  mov.l     er6, @-sp
0x02F49A  mov.l     sp, er6
0x02F49C  mov.l     er2, @-sp
0x02F4A0  mov.w     r5, @-sp
0x02F4A2  sub.l     #0x00000054, sp
0x02F4A8  mov.b     r0l, r5l
0x02F4AA  mov.b     r0h, r5h
0x02F4AC  sub.b     r0h, r0h
0x02F4AE  sub.b     r0l, r0l
0x02F4B0  bsr       0x02ff00
0x02F4B4  mov.b     r0l, @(0xfff8,er6)
0x02F4B8  mov.b     @(0xfff8,er6), r0l
0x02F4BC  extu.w    r0
0x02F4BE  mov.w     #0x0022, e0
0x02F4C2  mulxu.w   e0, er0
0x02F4C4  add.l     #0x0041ffb4, er0
0x02F4CA  mov.l     er0, @(0xfff2,er6)
0x02F4D0  mov.l     #0xffffffe6, er1
0x02F4D6  add.l     er6, er1
0x02F4D8  mov.b     r5h, r0h
0x02F4DA  mov.b     r5l, r0l
0x02F4DC  bsr       0x02ff32
0x02F4E0  mov.l     @(0xffe6,er6), er0
0x02F4E6  mov.b     @(0x15,er0), r0l
0x02F4EA  mov.b     r0l, @(0xfff9,er6)
0x02F4EE  mov.b     @(0xfff9,er6), r0l
0x02F4F2  extu.w    r0
0x02F4F4  mov.w     #0x0022, e0
0x02F4F8  mulxu.w   e0, er0
0x02F4FA  add.l     #0x0041ffb4, er0
0x02F500  mov.l     er0, @(0xffee,er6)
0x02F506  mov.l     @(0xffe6,er6), er0
0x02F50C  mov.l     @(0x10,er0), er0
0x02F512  mov.l     er0, @(0xffea,er6)
0x02F518  sub.b     r0l, r0l
0x02F51A  mov.b     r0l, @(0xfff7,er6)
0x02F51E  bt        0x02f548
0x02F520  sub.l     er0, er0
0x02F522  mov.b     @(0xfff7,er6), r0l
0x02F526  mov.l     @(0xffea,er6), er1
0x02F52C  add.l     er0, er1
0x02F52E  sub.l     er0, er0
0x02F530  mov.b     @(0xfff7,er6), r0l
0x02F534  mov.b     @er1, r1l
0x02F536  mov.b     r1l, @(0x440fdc,er0)
0x02F53E  mov.b     @(0xfff7,er6), r0l
0x02F542  inc.b     #1, r0l
0x02F544  mov.b     r0l, @(0xfff7,er6)
0x02F548  mov.b     @(0xfff7,er6), r0l
0x02F54C  cmp.b     #0x04, r0l
0x02F54E  bcs       0x02f520
0x02F550  mov.b     r5l, r5l
0x02F552  bne       0x02f556
0x02F554  mov.b     #0x01, r5l
0x02F556  mov.l     @(0xffee,er6), er0
0x02F55C  mov.b     @(0x20,er0), r1l
0x02F560  bne       0x02f65a
0x02F564  mov.b     @0x4206ec, r0l
0x02F56A  beq       0x02f5a6
0x02F56C  mov.l     #0x00100590, er0
0x02F572  mov.l     er0, @0x400f32
0x02F57A  mov.l     #0x00100590, er0
0x02F580  mov.l     er0, @0x400f36
0x02F588  mov.l     #0x00100590, er0
0x02F58E  mov.l     er0, @0x400f3a
0x02F596  mov.l     #0x00100590, er0
0x02F59C  mov.l     er0, @0x400f3e
0x02F5A4  bt        0x02f5de
0x02F5A6  mov.l     #0x00027100, er0
0x02F5AC  mov.l     er0, @0x400f32
0x02F5B4  mov.l     #0x000249f0, er0
0x02F5BA  mov.l     er0, @0x400f36
0x02F5C2  mov.l     #0x000186a0, er0
0x02F5C8  mov.l     er0, @0x400f3a
0x02F5D0  mov.l     #0x00064190, er0
0x02F5D6  mov.l     er0, @0x400f3e
0x02F5DE  mov.b     r5l, r5l
0x02F5E0  beq       0x02f5e6
0x02F5E2  cmp.b     #0x01, r5l
0x02F5E4  bne       0x02f616
0x02F5E6  mov.l     #0x0003f736, er0
0x02F5EC  mov.l     #0x00420120, er1
0x02F5F2  jsr       0x018e36
0x02F5F6  mov.l     #0x00420118, er1
0x02F5FC  jsr       0x018e36
0x02F600  mov.l     #0x00420110, er1
0x02F606  jsr       0x018e36
0x02F60A  mov.l     #0x00420108, er1
0x02F610  jsr       0x018e36
0x02F614  bt        0x02f656
0x02F616  mov.b     r5l, r1l
0x02F618  extu.w    r1
0x02F61A  mov.l     #0xffffffde, er0
0x02F620  add.l     er6, er0
0x02F622  jsr       0x018ede
0x02F626  mov.l     #0x0003f73e, er1
0x02F62C  mov.l     er0, er2
0x02F62E  mov.l     #0x00420120, er0
0x02F634  jsr       0x01842c
0x02F638  mov.l     #0x00420118, er1
0x02F63E  jsr       0x018e36
0x02F642  mov.l     #0x00420110, er1
0x02F648  jsr       0x018e36
0x02F64C  mov.l     #0x00420108, er1
0x02F652  jsr       0x018e36
0x02F656  jmp       0x02fa5a
0x02F65A  mov.l     @(0xffee,er6), er0
0x02F660  mov.l     @(0xfff2,er6), er1
0x02F666  mov.b     @(0x20,er0), r0l
0x02F66A  mov.b     @(0x20,er1), r1l
0x02F66E  cmp.b     r1l, r0l
0x02F670  bne       0x02f940
0x02F674  mov.b     @(0xfff9,er6), r0l
0x02F678  mov.b     @(0xfff8,er6), r1l
0x02F67C  cmp.b     r1l, r0l
0x02F67E  beq       0x02f8e0
0x02F682  sub.b     r0l, r0l
0x02F684  mov.b     r0l, @(0xfff7,er6)
0x02F688  jmp       0x02f8d4
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
0x02F8E0  sub.b     r0l, r0l
0x02F8E2  mov.b     r0l, @(0xfff7,er6)
0x02F8E6  bt        0x02f934
0x02F8E8  sub.l     er0, er0
0x02F8EA  mov.b     @(0xfff7,er6), r0l
0x02F8EE  shll.l    #2, er0
0x02F8F0  mov.l     @(0xfff2,er6), er1
0x02F8F6  add.l     er0, er1
0x02F8F8  sub.l     er0, er0
0x02F8FA  mov.b     @(0xfff7,er6), r0l
0x02F8FE  shll.l    #2, er0
0x02F900  mov.l     @er1, er1
0x02F904  mov.l     er1, @(0x400f32,er0)
0x02F90E  sub.l     er0, er0
0x02F910  mov.b     @(0xfff7,er6), r0l
0x02F914  shll.l    #2, er0
0x02F916  shll.l    er0
0x02F918  mov.l     #0x00420108, er1
0x02F91E  add.l     er0, er1
0x02F920  mov.l     #0x0003f736, er0
0x02F926  jsr       0x018e36
0x02F92A  mov.b     @(0xfff7,er6), r0l
0x02F92E  inc.b     #1, r0l
0x02F930  mov.b     r0l, @(0xfff7,er6)
0x02F934  mov.b     @(0xfff7,er6), r0l
0x02F938  cmp.b     #0x04, r0l
0x02F93A  bcs       0x02f8e8
0x02F93C  jmp       0x02fa5a
0x02F940  mov.b     r5l, r5l
0x02F942  beq       0x02f94a
0x02F944  cmp.b     #0x01, r5l
0x02F946  bne       0x02f9d8
0x02F94A  mov.l     #0x0003f736, er0
0x02F950  mov.l     #0x00420120, er1
0x02F956  jsr       0x018e36
0x02F95A  mov.l     #0x00420118, er1
0x02F960  jsr       0x018e36
0x02F964  mov.l     #0x00420110, er1
0x02F96A  jsr       0x018e36
0x02F96E  mov.l     #0x00420108, er1
0x02F974  jsr       0x018e36
0x02F978  sub.b     r0l, r0l
0x02F97A  mov.b     r0l, @(0xfff7,er6)
0x02F97E  bt        0x02f9cc
0x02F980  sub.l     er0, er0
0x02F982  mov.b     @(0xfff7,er6), r0l
0x02F986  shll.l    #2, er0
0x02F988  shll.l    er0
0x02F98A  mov.l     #0x00420108, er1
0x02F990  add.l     er0, er1
0x02F992  mov.l     #0x0003f736, er0
0x02F998  jsr       0x018e36
0x02F99C  sub.l     er0, er0
0x02F99E  mov.b     @(0xfff7,er6), r0l
0x02F9A2  shll.l    #2, er0
0x02F9A4  mov.l     @(0xffee,er6), er1
0x02F9AA  add.l     er0, er1
0x02F9AC  sub.l     er0, er0
0x02F9AE  mov.b     @(0xfff7,er6), r0l
0x02F9B2  shll.l    #2, er0
0x02F9B4  mov.l     @er1, er1
0x02F9B8  mov.l     er1, @(0x400f32,er0)
0x02F9C2  mov.b     @(0xfff7,er6), r0l
0x02F9C6  inc.b     #1, r0l
0x02F9C8  mov.b     r0l, @(0xfff7,er6)
0x02F9CC  mov.b     @(0xfff7,er6), r0l
0x02F9D0  cmp.b     #0x04, r0l
0x02F9D2  bcs       0x02f980
0x02F9D4  jmp       0x02fa5a
0x02F9D8  sub.b     r0l, r0l
0x02F9DA  mov.b     r0l, @(0xfff7,er6)
0x02F9DE  bt        0x02fa52
0x02F9E0  sub.l     er0, er0
0x02F9E2  mov.b     @(0xfff7,er6), r0l
0x02F9E6  shll.l    #2, er0
0x02F9E8  shll.l    er0
0x02F9EA  mov.b     r5l, r1l
0x02F9EC  extu.w    r1
0x02F9EE  mov.l     er0, @(0xffda,er6)
0x02F9F4  mov.l     #0xffffffde, er0
0x02F9FA  add.l     er6, er0
0x02F9FC  jsr       0x018ede
0x02FA00  mov.l     #0x0003f736, er1
0x02FA06  mov.l     er0, er2
0x02FA08  mov.l     @(0xffda,er6), er0
0x02FA0E  add.l     #0x00420108, er0
0x02FA14  jsr       0x01842c
0x02FA18  sub.l     er0, er0
0x02FA1A  mov.b     @(0xfff7,er6), r0l
0x02FA1E  shll.l    #2, er0
0x02FA20  mov.l     @(0xffee,er6), er1
0x02FA26  add.l     er1, er0
0x02FA28  mov.b     r5l, r1l
0x02FA2A  extu.w    r1
0x02FA2C  extu.l    er1
0x02FA2E  mov.l     @er0, er0
0x02FA32  jsr       0x018e1e
0x02FA36  sub.l     er1, er1
0x02FA38  mov.b     @(0xfff7,er6), r1l
0x02FA3C  shll.l    #2, er1
0x02FA3E  mov.l     er0, @(0x400f32,er1)
0x02FA48  mov.b     @(0xfff7,er6), r0l
0x02FA4C  inc.b     #1, r0l
0x02FA4E  mov.b     r0l, @(0xfff7,er6)
0x02FA52  mov.b     @(0xfff7,er6), r0l
0x02FA56  cmp.b     #0x04, r0l
0x02FA58  bcs       0x02f9e0
0x02FA5A  add.l     #0x00000054, sp
0x02FA60  mov.w     @sp+, r5
0x02FA62  mov.l     @sp+, er2
0x02FA66  mov.l     @sp+, er6
0x02FA6A  rts       
