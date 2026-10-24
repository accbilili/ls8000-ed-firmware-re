0x011F36  mov.l     er6, @-sp
0x011F3A  mov.l     sp, er6
0x011F3C  mov.l     er2, @-sp
0x011F40  sub.l     #0x0000200e, sp
0x011F46  bclr      #4, @0xffff2e
0x011F4E  jsr       0x0130b6
0x011F52  cmp.b     #0x01, r0l
0x011F54  beq       0x011f62
0x011F56  mov.b     @0x400d22, r0l
0x011F5C  cmp.b     #0x01, r0l
0x011F5E  bne       0x011ff4
0x011F62  mov.b     @0x400d22, r0l
0x011F68  cmp.b     #0x01, r0l
0x011F6A  bne       0x011fe8
0x011F6C  mov.b     @0x400d21, r0l
0x011F72  mov.b     r0l, @0x400d20
0x011F78  mov.l     @0x40031e, er0
0x011F80  mov.l     er0, @0x400d24
0x011F88  mov.l     @0x400322, er0
0x011F90  mov.l     er0, @0x400d28
0x011F98  mov.l     @0x400326, er0
0x011FA0  mov.l     er0, @0x400d34
0x011FA8  mov.l     @0x40032a, er0
0x011FB0  mov.l     er0, @(0xdff2,er6)
0x011FB6  mov.l     @0x40032e, er0
0x011FBE  mov.l     er0, @0x400d2c
0x011FC6  mov.l     @0x400332, er0
0x011FCE  mov.l     er0, @0x400d30
0x011FD6  mov.l     @0x400336, er0
0x011FDE  mov.l     er0, @0x400d58
0x011FE6  bt        0x011ff4
0x011FE8  sub.w     r0, r0
0x011FEA  mov.w     r0, @0x400436   <<< 0x400436
0x011FF0  jmp       0x01256e
0x011FF4  mov.b     #0x01, r0l
0x011FF6  mov.b     r0l, @0x400d22
0x011FFC  mov.b     @0x400d20, r0l
0x012002  cmp.b     #0x01, r0l
0x012004  bne       0x012008
0x012006  bt        0x01205a
0x012008  mov.b     @0x40043d, r0l
0x01200E  extu.w    r0
0x012010  and.w     #0x0018, r0
0x012014  beq       0x012024
0x012016  mov.w     #0x0050, r0
0x01201A  mov.w     r0, @0x400436   <<< 0x400436
0x012020  jmp       0x01256e
0x012024  mov.b     @0x400445, r0l
0x01202A  beq       0x01203a
0x01202C  mov.w     #0x0050, r0
0x012030  mov.w     r0, @0x400436   <<< 0x400436
0x012036  jmp       0x01256e
0x01203A  mov.b     @0x40043d, r0l
0x012040  extu.w    r0
0x012042  and.w     #0x0007, r0
0x012046  cmp.w     #0x0005, r0
0x01204A  beq       0x01205a
0x01204C  mov.w     #0x0050, r0
0x012050  mov.w     r0, @0x400436   <<< 0x400436
0x012056  jmp       0x01256e
0x01205A  mov.b     @0x400d3a, r0l
0x012060  bne       0x0123ea
0x012064  mov.b     @0x400d20, r0l
0x01206A  bne       0x01207c
0x01206C  bsr       0x01280c
0x012070  mov.w     @0x400436, r0   <<< 0x400436
0x012076  beq       0x01207c
0x012078  jmp       0x01256e
0x01207C  sub.b     r0l, r0l
0x01207E  mov.b     r0l, @0x400d20
0x012084  sub.w     r0, r0
0x012086  mov.w     r0, @(0xdff0,er6)
0x01208A  bt        0x0120b6
0x01208C  mov.w     @(0xdff0,er6), r0
0x012090  extu.l    er0
0x012092  mov.w     @(0xdff0,er6), r1
0x012096  extu.l    er1
0x012098  mov.l     #0xffffdffc, er2
0x01209E  add.l     er6, er2
0x0120A0  add.l     er1, er2
0x0120A2  mov.b     @(0x400d3d,er0), r0l
0x0120AA  mov.b     r0l, @er2
0x0120AC  mov.w     @(0xdff0,er6), r0
0x0120B0  inc.w     #1, r0
0x0120B2  mov.w     r0, @(0xdff0,er6)
0x0120B6  mov.w     @(0xdff0,er6), r0
0x0120BA  cmp.w     #0x0018, r0
0x0120BE  bcs       0x01208c
0x0120C0  sub.l     er0, er0
0x0120C2  mov.b     @0x400442, r0l
0x0120C8  mov.w     r0, e0
0x0120CA  sub.w     r0, r0
0x0120CC  sub.l     er1, er1
0x0120CE  mov.b     @0x400443, r1l
0x0120D4  shll.l    #2, er1
0x0120D6  shll.l    #2, er1
0x0120D8  shll.l    #2, er1
0x0120DA  shll.l    #2, er1
0x0120DC  add.l     er1, er0
0x0120DE  sub.l     er1, er1
0x0120E0  mov.b     @0x400444, r1l
0x0120E6  add.l     er1, er0
0x0120E8  mov.l     er0, @(0xdff6,er6)
0x0120EE  mov.l     @(0xdff6,er6), er0
0x0120F4  cmp.l     #0x00002000, er0
0x0120FA  bcc       0x012106
0x0120FC  mov.w     @(0xdff8,er6), r0
0x012100  mov.w     r0, @(0xdffa,er6)
0x012104  bt        0x01210e
0x012106  mov.w     #0x2000, r0
0x01210A  mov.w     r0, @(0xdffa,er6)
0x01210E  mov.w     @(0xdffa,er6), r0
0x012112  extu.l    er0
0x012114  mov.l     @(0xdff6,er6), er1
0x01211A  sub.l     er0, er1
0x01211C  mov.l     er1, @(0xdff6,er6)
0x012122  bset      #4, @0xffff2e
0x01212A  mov.w     @(0xdffa,er6), r1
0x01212E  sub.w     #0x0018, r1
0x012132  mov.l     #0xffffe014, er0
0x012138  add.l     er6, er0
0x01213A  jsr       0x0118d0
0x01213E  bclr      #4, @0xffff2e
0x012146  mov.b     #0x01, r0l
0x012148  mov.b     r0l, @0x400d3a
0x01214E  mov.w     @0xfffed2, r0
0x012154  mov.w     r0, @(0xdfee,er6)
0x012158  mov.w     @(0xdfee,er6), r0
0x01215C  and.w     #0xfffc, r0
0x012160  or.w      #0x0003, r0
0x012164  mov.w     r0, @0xfffed2
0x01216A  jsr       0x017a80
0x01216E  mov.b     #0x01, r0l
0x012170  mov.b     r0l, @0x400ca0
0x012176  mov.b     #0x01, r0l
0x012178  mov.b     r0l, @0x400ca1
0x01217E  mov.l     #0x00004000, er0
0x012184  mov.l     er0, @0xffdc34
0x01218C  jsr       0x010bd2
0x012190  jsr       0x017a78
0x012194  jsr       0x010bd8
0x012198  mov.b     #0x02, r0l
0x01219A  mov.b     r0l, @0x400d38
0x0121A0  mov.l     #0x00400ca0, er0
0x0121A6  mov.l     er0, @0xffdc30
0x0121AE  jsr       0x010bd2
0x0121B2  jsr       0x017a7c
0x0121B6  jsr       0x010bd8
0x0121BA  sub.l     er0, er0
0x0121BC  mov.b     @(0xdffd,er6), r0l
0x0121C0  mov.w     r0, e0
0x0121C2  sub.w     r0, r0
0x0121C4  sub.l     er1, er1
0x0121C6  mov.b     @(0xdffe,er6), r1l
0x0121CA  shll.l    #2, er1
0x0121CC  shll.l    #2, er1
0x0121CE  shll.l    #2, er1
0x0121D0  shll.l    #2, er1
0x0121D2  add.l     er1, er0
0x0121D4  sub.l     er1, er1
0x0121D6  mov.b     @(0xdffc,er6), r1l
0x0121DA  mov.b     r1l, r1h
0x0121DC  sub.b     r1l, r1l
0x0121DE  mov.w     r1, e1
0x0121E0  sub.w     r1, r1
0x0121E2  add.l     er1, er0
0x0121E4  sub.l     er1, er1
0x0121E6  mov.b     @(0xdfff,er6), r1l
0x0121EA  add.l     er1, er0
0x0121EC  mov.l     er0, @0x400d24
0x0121F4  sub.l     er0, er0
0x0121F6  mov.b     @(0xe000,er6), r0l
0x0121FA  mov.b     r0l, r0h
0x0121FC  sub.b     r0l, r0l
0x0121FE  mov.w     r0, e0
0x012200  sub.w     r0, r0
0x012202  sub.l     er1, er1
0x012204  mov.b     @(0xe001,er6), r1l
0x012208  mov.w     r1, e1
0x01220A  sub.w     r1, r1
0x01220C  add.l     er1, er0
0x01220E  sub.l     er1, er1
0x012210  mov.b     @(0xe002,er6), r1l
0x012214  shll.l    #2, er1
0x012216  shll.l    #2, er1
0x012218  shll.l    #2, er1
0x01221A  shll.l    #2, er1
0x01221C  add.l     er1, er0
0x01221E  sub.l     er1, er1
0x012220  mov.b     @(0xe003,er6), r1l
0x012224  add.l     er1, er0
0x012226  mov.l     er0, @0x400d28
0x01222E  sub.l     er0, er0
0x012230  mov.b     @(0xe004,er6), r0l
0x012234  mov.b     r0l, r0h
0x012236  sub.b     r0l, r0l
0x012238  mov.w     r0, e0
0x01223A  sub.w     r0, r0
0x01223C  sub.l     er1, er1
0x01223E  mov.b     @(0xe005,er6), r1l
0x012242  mov.w     r1, e1
0x012244  sub.w     r1, r1
0x012246  add.l     er1, er0
0x012248  sub.l     er1, er1
0x01224A  mov.b     @(0xe006,er6), r1l
0x01224E  shll.l    #2, er1
0x012250  shll.l    #2, er1
0x012252  shll.l    #2, er1
0x012254  shll.l    #2, er1
0x012256  add.l     er1, er0
0x012258  sub.l     er1, er1
0x01225A  mov.b     @(0xe007,er6), r1l
0x01225E  add.l     er1, er0
0x012260  mov.l     er0, @0x400d34
0x012268  sub.l     er0, er0
0x01226A  mov.b     @(0xe008,er6), r0l
0x01226E  mov.b     r0l, r0h
0x012270  sub.b     r0l, r0l
0x012272  mov.w     r0, e0
0x012274  sub.w     r0, r0
0x012276  sub.l     er1, er1
0x012278  mov.b     @(0xe009,er6), r1l
0x01227C  mov.w     r1, e1
0x01227E  sub.w     r1, r1
0x012280  add.l     er1, er0
0x012282  sub.l     er1, er1
0x012284  mov.b     @(0xe00a,er6), r1l
0x012288  shll.l    #2, er1
0x01228A  shll.l    #2, er1
0x01228C  shll.l    #2, er1
0x01228E  shll.l    #2, er1
0x012290  add.l     er1, er0
0x012292  sub.l     er1, er1
0x012294  mov.b     @(0xe00b,er6), r1l
0x012298  add.l     er1, er0
0x01229A  mov.l     er0, @(0xdff2,er6)
0x0122A0  mov.l     @0x400d28, er0
0x0122A8  add.l     #0x0000007f, er0
0x0122AE  shlr.l    #2, er0
0x0122B0  shlr.l    #2, er0
0x0122B2  shlr.l    #2, er0
0x0122B4  shlr.l    er0
0x0122B6  shll.l    #2, er0
0x0122B8  shll.l    #2, er0
0x0122BA  shll.l    #2, er0
0x0122BC  shll.l    er0
0x0122BE  mov.l     er0, @0x400d2c
0x0122C6  mov.l     @0x400d2c, er0
0x0122CE  mov.l     @0x400d34, er1
0x0122D6  sub.l     er1, er0
0x0122D8  mov.l     @(0xdff2,er6), er1
0x0122DE  add.l     er1, er0
0x0122E0  mov.l     er0, @0x400d30
0x0122E8  sub.l     er0, er0
0x0122EA  mov.b     @(0xe014,er6), r0l
0x0122EE  mov.b     r0l, r0h
0x0122F0  sub.b     r0l, r0l
0x0122F2  mov.w     r0, e0
0x0122F4  sub.w     r0, r0
0x0122F6  sub.l     er1, er1
0x0122F8  mov.b     @(0xe015,er6), r1l
0x0122FC  mov.w     r1, e1
0x0122FE  sub.w     r1, r1
0x012300  add.l     er1, er0
0x012302  sub.l     er1, er1
0x012304  mov.b     @(0xe016,er6), r1l
0x012308  shll.l    #2, er1
0x01230A  shll.l    #2, er1
0x01230C  shll.l    #2, er1
0x01230E  shll.l    #2, er1
0x012310  add.l     er1, er0
0x012312  sub.l     er1, er1
0x012314  mov.b     @(0xe017,er6), r1l
0x012318  add.l     er1, er0
0x01231A  mov.l     er0, @0x400d58
0x012322  mov.l     @0x400d24, er0
0x01232A  mov.l     er0, @0xffdc34
0x012332  jsr       0x010bd2
0x012336  jsr       0x017a78
0x01233A  jsr       0x010bd8
0x01233E  mov.l     @0x400d2c, er0
0x012346  mov.l     er0, @0xffdc34
0x01234E  sub.b     r0l, r0l
0x012350  mov.b     r0l, @0x400d38
0x012356  sub.b     r0l, r0l
0x012358  mov.b     r0l, @0x400d39
0x01235E  jmp       0x0123e2
0x012362  mov.l     #0xffffdff6, er0
0x012368  add.l     er6, er0
0x01236A  mov.l     er0, @-sp
0x01236E  mov.l     #0xffffdffa, er1
0x012374  add.l     er6, er1
0x012376  mov.l     #0xffffdffc, er0
0x01237C  add.l     er6, er0
0x01237E  bsr       0x01258e
0x012382  adds.l    #4, sp
0x012384  mov.l     @(0xdff6,er6), er0
0x01238A  bne       0x01238e
0x01238C  bt        0x0123e6
0x01238E  mov.l     @(0xdff6,er6), er0
0x012394  cmp.l     #0x00002000, er0
0x01239A  bcc       0x0123a6
0x01239C  mov.w     @(0xdff8,er6), r0
0x0123A0  mov.w     r0, @(0xdffa,er6)
0x0123A4  bt        0x0123ae
0x0123A6  mov.w     #0x2000, r0
0x0123AA  mov.w     r0, @(0xdffa,er6)
0x0123AE  bset      #4, @0xffff2e
0x0123B6  mov.l     #0xffffdffc, er0
0x0123BC  add.l     er6, er0
0x0123BE  mov.w     @(0xdffa,er6), r1
0x0123C2  jsr       0x0118d0
0x0123C6  bclr      #4, @0xffff2e
0x0123CE  mov.w     @(0xdffa,er6), r0
0x0123D2  extu.l    er0
0x0123D4  mov.l     @(0xdff6,er6), er1
0x0123DA  sub.l     er0, er1
0x0123DC  mov.l     er1, @(0xdff6,er6)
0x0123E2  jmp       0x012362
0x0123E6  jmp       0x0124f4
0x0123EA  sub.l     er0, er0
0x0123EC  mov.b     @0x400442, r0l
0x0123F2  mov.w     r0, e0
0x0123F4  sub.w     r0, r0
0x0123F6  sub.l     er1, er1
0x0123F8  mov.b     @0x400443, r1l
0x0123FE  shll.l    #2, er1
0x012400  shll.l    #2, er1
0x012402  shll.l    #2, er1
0x012404  shll.l    #2, er1
0x012406  add.l     er1, er0
0x012408  sub.l     er1, er1
0x01240A  mov.b     @0x400444, r1l
0x012410  add.l     er1, er0
0x012412  mov.l     er0, @(0xdff6,er6)
0x012418  mov.l     @(0xdff6,er6), er0
0x01241E  cmp.l     #0x00002000, er0
0x012424  bcc       0x012430
0x012426  mov.w     @(0xdff8,er6), r0
0x01242A  mov.w     r0, @(0xdffa,er6)
0x01242E  bt        0x012438
0x012430  mov.w     #0x2000, r0
0x012434  mov.w     r0, @(0xdffa,er6)
0x012438  bset      #4, @0xffff2e
0x012440  mov.l     #0xffffdffc, er0
0x012446  add.l     er6, er0
0x012448  mov.w     @(0xdffa,er6), r1
0x01244C  jsr       0x0118d0
0x012450  bclr      #4, @0xffff2e
0x012458  mov.w     @(0xdffa,er6), r0
0x01245C  extu.l    er0
0x01245E  mov.l     @(0xdff6,er6), er1
0x012464  sub.l     er0, er1
0x012466  mov.l     er1, @(0xdff6,er6)
0x01246C  jmp       0x0124f0
0x012470  mov.l     #0xffffdff6, er0
0x012476  add.l     er6, er0
0x012478  mov.l     er0, @-sp
0x01247C  mov.l     #0xffffdffa, er1
0x012482  add.l     er6, er1
0x012484  mov.l     #0xffffdffc, er0
0x01248A  add.l     er6, er0
0x01248C  bsr       0x01258e
0x012490  adds.l    #4, sp
0x012492  mov.l     @(0xdff6,er6), er0
0x012498  bne       0x01249c
0x01249A  bt        0x0124f4
0x01249C  mov.l     @(0xdff6,er6), er0
0x0124A2  cmp.l     #0x00002000, er0
0x0124A8  bcc       0x0124b4
0x0124AA  mov.w     @(0xdff8,er6), r0
0x0124AE  mov.w     r0, @(0xdffa,er6)
0x0124B2  bt        0x0124bc
0x0124B4  mov.w     #0x2000, r0
0x0124B8  mov.w     r0, @(0xdffa,er6)
0x0124BC  bset      #4, @0xffff2e
0x0124C4  mov.l     #0xffffdffc, er0
0x0124CA  add.l     er6, er0
0x0124CC  mov.w     @(0xdffa,er6), r1
0x0124D0  jsr       0x0118d0
0x0124D4  bclr      #4, @0xffff2e
0x0124DC  mov.w     @(0xdffa,er6), r0
0x0124E0  extu.l    er0
0x0124E2  mov.l     @(0xdff6,er6), er1
0x0124E8  sub.l     er0, er1
0x0124EA  mov.l     er1, @(0xdff6,er6)
0x0124F0  jmp       0x012470
0x0124F4  mov.b     @0x400d20, r0l
0x0124FA  mov.b     r0l, @0x400d21
0x012500  mov.l     @0x400d24, er0
0x012508  mov.l     er0, @0x40031e
0x012510  mov.l     @0x400d28, er0
0x012518  mov.l     er0, @0x400322
0x012520  mov.l     @0x400d34, er0
0x012528  mov.l     er0, @0x400326
0x012530  mov.l     @(0xdff2,er6), er0
0x012536  mov.l     er0, @0x40032a
0x01253E  mov.l     @0x400d2c, er0
0x012546  mov.l     er0, @0x40032e
0x01254E  mov.l     @0x400d30, er0
0x012556  mov.l     er0, @0x400332
0x01255E  mov.l     @0x400d58, er0
0x012566  mov.l     er0, @0x400336
0x01256E  sub.b     r0l, r0l
0x012570  mov.b     r0l, @0x400d22
0x012576  bset      #4, @0xffff2e
0x01257E  add.l     #0x0000200e, sp
0x012584  mov.l     @sp+, er2
0x012588  mov.l     @sp+, er6
0x01258C  rts       
