# fn 0x033422 (callee_success1) : 261 insns
0x033422  stm.l     er4-er6, @-sp
0x033426  mov.l     #0x00440fdc, er6
0x03342C  mov.l     #0x0041ffae, er1
0x033432  mov.l     #0x0041ffac, er4
0x033438  mov.l     #0x0041ffb2, er5
0x03343E  mov.b     @0x4007c9, r0l
0x033444  beq       0x033494
0x033446  mov.b     @0x4007ca, r0l
0x03344C  cmp.b     #0x01, r0l
0x03344E  beq       0x033454
0x033450  mov.b     r0l, r0l
0x033452  bne       0x033494
0x033454  mov.l     #0x0085c000, er0
0x03345A  mov.l     er0, @0x41ffa8
0x033462  mov.l     #0x00820000, er0
0x033468  mov.l     er0, @er1
0x03346C  mov.w     #0x7800, r0
0x033470  mov.w     r0, @er4
0x033472  mov.w     r0, @er5
0x033474  sub.b     r5l, r5l
0x033476  mov.b     r5l, r4l
0x033478  extu.w    r4
0x03347A  extu.l    er4
0x03347C  mov.l     er6, er0
0x03347E  add.l     er4, er0
0x033480  mov.b     @(0x3f112,er4), r1l
0x033488  mov.b     r1l, @er0
0x03348A  inc.b     #1, r5l
0x03348C  cmp.b     #0x04, r5l
0x03348E  bcs       0x033476
0x033490  jmp       0x03379c
0x033494  mov.b     @0x4007c9, r0l
0x03349A  beq       0x0334ea
0x03349C  mov.b     @0x4007ca, r0l
0x0334A2  cmp.b     #0x02, r0l
0x0334A4  bne       0x0334ea
0x0334A6  mov.l     #0x00898000, er0
0x0334AC  mov.l     er0, @0x41ffa8
0x0334B4  mov.l     #0x00820000, er0
0x0334BA  mov.l     er0, @er1
0x0334BE  mov.w     #0x4000, r0
0x0334C2  mov.w     r0, @er4
0x0334C4  mov.w     #0x7800, r0
0x0334C8  mov.w     r0, @er5
0x0334CA  sub.b     r5l, r5l
0x0334CC  mov.b     r5l, r4l
0x0334CE  extu.w    r4
0x0334D0  extu.l    er4
0x0334D2  mov.l     er6, er0
0x0334D4  add.l     er4, er0
0x0334D6  mov.b     @(0x3f116,er4), r1l
0x0334DE  mov.b     r1l, @er0
0x0334E0  inc.b     #1, r5l
0x0334E2  cmp.b     #0x04, r5l
0x0334E4  bcs       0x0334cc
0x0334E6  jmp       0x03379c
0x0334EA  mov.b     @0x4007c9, r0l
0x0334F0  beq       0x033540
0x0334F2  mov.b     @0x4007ca, r0l
0x0334F8  cmp.b     #0x03, r0l
0x0334FA  bne       0x033540
0x0334FC  mov.l     #0x008b8000, er0
0x033502  mov.l     er0, @0x41ffa8
0x03350A  mov.l     #0x00820000, er0
0x033510  mov.l     er0, @er1
0x033514  mov.w     #0x2800, r0
0x033518  mov.w     r0, @er4
0x03351A  mov.w     #0x7800, r0
0x03351E  mov.w     r0, @er5
0x033520  sub.b     r5l, r5l
0x033522  mov.b     r5l, r4l
0x033524  extu.w    r4
0x033526  extu.l    er4
0x033528  mov.l     er6, er0
0x03352A  add.l     er4, er0
0x03352C  mov.b     @(0x3f11a,er4), r1l
0x033534  mov.b     r1l, @er0
0x033536  inc.b     #1, r5l
0x033538  cmp.b     #0x04, r5l
0x03353A  bcs       0x033522
0x03353C  jmp       0x03379c
0x033540  mov.b     @0x4007c9, r0l
0x033546  beq       0x033596
0x033548  mov.b     @0x4007ca, r0l
0x03354E  cmp.b     #0x04, r0l
0x033550  bne       0x033596
0x033552  mov.l     #0x008cc000, er0
0x033558  mov.l     er0, @0x41ffa8
0x033560  mov.l     #0x00820000, er0
0x033566  mov.l     er0, @er1
0x03356A  mov.w     #0x2000, r0
0x03356E  mov.w     r0, @er4
0x033570  mov.w     #0x7800, r0
0x033574  mov.w     r0, @er5
0x033576  sub.b     r5l, r5l
0x033578  mov.b     r5l, r4l
0x03357A  extu.w    r4
0x03357C  extu.l    er4
0x03357E  mov.l     er6, er0
0x033580  add.l     er4, er0
0x033582  mov.b     @(0x3f11e,er4), r1l
0x03358A  mov.b     r1l, @er0
0x03358C  inc.b     #1, r5l
0x03358E  cmp.b     #0x04, r5l
0x033590  bcs       0x033578
0x033592  jmp       0x03379c
0x033596  mov.b     @0x4007c9, r0l
0x03359C  beq       0x0335ec
0x03359E  mov.b     @0x4007ca, r0l
0x0335A4  cmp.b     #0x06, r0l
0x0335A6  bne       0x0335ec
0x0335A8  mov.l     #0x008cc000, er0
0x0335AE  mov.l     er0, @0x41ffa8
0x0335B6  mov.l     #0x00820000, er0
0x0335BC  mov.l     er0, @er1
0x0335C0  mov.w     #0x2000, r0
0x0335C4  mov.w     r0, @er4
0x0335C6  mov.w     #0x7800, r0
0x0335CA  mov.w     r0, @er5
0x0335CC  sub.b     r5l, r5l
0x0335CE  mov.b     r5l, r4l
0x0335D0  extu.w    r4
0x0335D2  extu.l    er4
0x0335D4  mov.l     er6, er0
0x0335D6  add.l     er4, er0
0x0335D8  mov.b     @(0x3f122,er4), r1l
0x0335E0  mov.b     r1l, @er0
0x0335E2  inc.b     #1, r5l
0x0335E4  cmp.b     #0x04, r5l
0x0335E6  bcs       0x0335ce
0x0335E8  jmp       0x03379c
0x0335EC  mov.b     @0x4007c9, r0l
0x0335F2  bne       0x033646
0x0335F4  mov.b     @0x4007ca, r0l
0x0335FA  cmp.b     #0x01, r0l
0x0335FC  beq       0x033602
0x0335FE  mov.b     r0l, r0l
0x033600  bne       0x033646
0x033602  mov.l     #0x008e8000, er0
0x033608  mov.l     er0, @0x41ffa8
0x033610  mov.l     #0x00820000, er0
0x033616  mov.l     er0, @er1
0x03361A  mov.w     #0x2800, r0
0x03361E  mov.w     r0, @er4
0x033620  mov.w     #0x7800, r0
0x033624  mov.w     r0, @er5
0x033626  sub.b     r5l, r5l
0x033628  mov.b     r5l, r4l
0x03362A  extu.w    r4
0x03362C  extu.l    er4
0x03362E  mov.l     er6, er0
0x033630  add.l     er4, er0
0x033632  mov.b     @(0x3f126,er4), r1l
0x03363A  mov.b     r1l, @er0
0x03363C  inc.b     #1, r5l
0x03363E  cmp.b     #0x04, r5l
0x033640  bcs       0x033628
0x033642  jmp       0x03379c
0x033646  mov.b     @0x4007c9, r0l
0x03364C  bne       0x03369c
0x03364E  mov.b     @0x4007ca, r0l
0x033654  cmp.b     #0x02, r0l
0x033656  bne       0x03369c
0x033658  mov.l     #0x008cc000, er0
0x03365E  mov.l     er0, @0x41ffa8
0x033666  mov.l     #0x00820000, er0
0x03366C  mov.l     er0, @er1
0x033670  mov.w     #0x2000, r0
0x033674  mov.w     r0, @er4
0x033676  mov.w     #0x7800, r0
0x03367A  mov.w     r0, @er5
0x03367C  sub.b     r5l, r5l
0x03367E  mov.b     r5l, r4l
0x033680  extu.w    r4
0x033682  extu.l    er4
0x033684  mov.l     er6, er0
0x033686  add.l     er4, er0
0x033688  mov.b     @(0x3f12a,er4), r1l
0x033690  mov.b     r1l, @er0
0x033692  inc.b     #1, r5l
0x033694  cmp.b     #0x04, r5l
0x033696  bcs       0x03367e
0x033698  jmp       0x03379c
0x03369C  mov.b     @0x4007c9, r0l
0x0336A2  bne       0x0336f2
0x0336A4  mov.b     @0x4007ca, r0l
0x0336AA  cmp.b     #0x03, r0l
0x0336AC  bne       0x0336f2
0x0336AE  mov.l     #0x008cc000, er0
0x0336B4  mov.l     er0, @0x41ffa8
0x0336BC  mov.l     #0x00820000, er0
0x0336C2  mov.l     er0, @er1
0x0336C6  mov.w     #0x2000, r0
0x0336CA  mov.w     r0, @er4
0x0336CC  mov.w     #0x7800, r0
0x0336D0  mov.w     r0, @er5
0x0336D2  sub.b     r5l, r5l
0x0336D4  mov.b     r5l, r4l
0x0336D6  extu.w    r4
0x0336D8  extu.l    er4
0x0336DA  mov.l     er6, er0
0x0336DC  add.l     er4, er0
0x0336DE  mov.b     @(0x3f12e,er4), r1l
0x0336E6  mov.b     r1l, @er0
0x0336E8  inc.b     #1, r5l
0x0336EA  cmp.b     #0x04, r5l
0x0336EC  bcs       0x0336d4
0x0336EE  jmp       0x03379c
0x0336F2  mov.b     @0x4007c9, r0l
0x0336F8  bne       0x033746
0x0336FA  mov.b     @0x4007ca, r0l
0x033700  cmp.b     #0x04, r0l
0x033702  bne       0x033746
0x033704  mov.l     #0x008cc000, er0
0x03370A  mov.l     er0, @0x41ffa8
0x033712  mov.l     #0x00820000, er0
0x033718  mov.l     er0, @er1
0x03371C  mov.w     #0x2000, r0
0x033720  mov.w     r0, @er4
0x033722  mov.w     #0x7800, r0
0x033726  mov.w     r0, @er5
0x033728  sub.b     r5l, r5l
0x03372A  mov.b     r5l, r4l
0x03372C  extu.w    r4
0x03372E  extu.l    er4
0x033730  mov.l     er6, er0
0x033732  add.l     er4, er0
0x033734  mov.b     @(0x3f132,er4), r1l
0x03373C  mov.b     r1l, @er0
0x03373E  inc.b     #1, r5l
0x033740  cmp.b     #0x04, r5l
0x033742  bcs       0x03372a
0x033744  bt        0x03379c
0x033746  mov.b     @0x4007c9, r0l
0x03374C  bne       0x03379a
0x03374E  mov.b     @0x4007ca, r0l
0x033754  cmp.b     #0x06, r0l
0x033756  bne       0x03379a
0x033758  mov.l     #0x008fc000, er0
0x03375E  mov.l     er0, @0x41ffa8
0x033766  mov.l     #0x00820000, er0
0x03376C  mov.l     er0, @er1
0x033770  mov.w     #0x0800, r0
0x033774  mov.w     r0, @er4
0x033776  mov.w     #0x7800, r0
0x03377A  mov.w     r0, @er5
0x03377C  sub.b     r5l, r5l
0x03377E  mov.b     r5l, r4l
0x033780  extu.w    r4
0x033782  extu.l    er4
0x033784  mov.l     er6, er0
0x033786  add.l     er4, er0
0x033788  mov.b     @(0x3f136,er4), r1l
0x033790  mov.b     r1l, @er0
0x033792  inc.b     #1, r5l
0x033794  cmp.b     #0x04, r5l
0x033796  bcs       0x03377e
0x033798  bt        0x03379c
0x03379A  bt        0x03379a
0x03379C  ldm.l     @sp+, er4-er6
0x0337A0  rts       
