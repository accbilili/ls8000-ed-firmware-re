0x02510C  stm.l     er2-er3, @-sp
0x025110  stm.l     er4-er6, @-sp
0x025114  sub.l     #0x00000054, sp
0x02511A  mov.l     #0x0040064e, er3
0x025120  mov.l     #0x00400436, er5
0x025126  mov.l     #0x00000004, er6
0x02512C  add.l     sp, er6
0x02512E  sub.b     r0l, r0l
0x025130  mov.b     r0l, @0x4007ca
0x025136  mov.b     r0l, @0x4007c9
0x02513C  sub.b     r0l, r0l
0x02513E  mov.b     r0l, @0x4007c5
0x025144  mov.b     r0l, @0x4007c6
0x02514A  sub.b     r0l, r0l
0x02514C  mov.b     r0l, @0x400d5d
0x025152  mov.b     #0xff, r0l
0x025154  mov.b     r0l, @0x4206e3
0x02515A  mov.b     @0x40043d, r0l
0x025160  and.b     #0x1f, r0l
0x025162  bne       0x0251c4
0x025164  mov.b     #0x02, r4l
0x025166  bt        0x02517a
0x025168  mov.b     r4l, r0l
0x02516A  extu.w    r0
0x02516C  extu.l    er0
0x02516E  mov.b     @(0x40043c,er0), r1l
0x025176  bne       0x0251c4
0x025178  inc.b     #1, r4l
0x02517A  cmp.b     #0x06, r4l
0x02517C  bcs       0x025168
0x02517E  mov.b     @0x400445, r0l
0x025184  and.b     #0x7f, r0l
0x025186  bne       0x0251c4
0x025188  mov.b     @0x400443, r4l
0x02518E  extu.w    r4
0x025190  mov.b     r4l, r4h
0x025192  sub.b     r4l, r4l
0x025194  mov.b     @0x400444, r0l
0x02519A  extu.w    r0
0x02519C  or.w      r0, r4
0x02519E  extu.l    er4
0x0251A0  sub.l     er0, er0
0x0251A2  mov.b     @0x400442, r0l
0x0251A8  mov.w     r0, e0
0x0251AA  sub.w     r0, r0
0x0251AC  or.l      er0, er4
0x0251B0  beq       0x0254e6
0x0251B4  cmp.l     #0x00000008, er4
0x0251BA  bcs       0x0251c4
0x0251BC  cmp.l     #0x00000042, er4
0x0251C2  bls       0x0251cc
0x0251C4  mov.w     #0x0050, r0
0x0251C8  jmp       0x02533c
0x0251CC  mov.w     @0x400406, r0
0x0251D2  and.w     #0x00ff, r0
0x0251D6  cmp.w     #0x0001, r0
0x0251DA  bne       0x0251e4
0x0251DC  mov.b     @0x400d78, r0l
0x0251E2  beq       0x0251ea
0x0251E4  jsr       0x010b56
0x0251E8  bt        0x0251cc
0x0251EA  mov.w     r4, r1
0x0251EC  mov.l     er6, er0
0x0251EE  jsr       0x0118d0
0x0251F2  mov.w     @er5, r0
0x0251F4  bne       0x0254e6
0x0251F8  subs.l    #4, er4
0x0251FA  subs.l    #4, er4
0x0251FC  mov.b     @(0x6,er6), r0l
0x025200  extu.w    r0
0x025202  mov.b     r0l, r0h
0x025204  sub.b     r0l, r0l
0x025206  mov.b     @(0x7,er6), r1l
0x02520A  extu.w    r1
0x02520C  or.w      r1, r0
0x02520E  extu.l    er0
0x025210  cmp.l     er0, er4
0x025212  beq       0x02521c
0x025214  mov.w     #0x0053, r0
0x025218  jmp       0x02533c
0x02521C  mov.l     er4, er4
0x02521E  beq       0x0254e6
0x025222  mov.w     @0x4007be, r0
0x025228  cmp.w     #0x04b0, r0
0x02522C  bne       0x02523c
0x02522E  mov.l     #0x000031d2, er0
0x025234  mov.l     er0, @0x400c78
0x02523C  mov.w     @0x4007be, r0
0x025242  cmp.w     #0x0fa0, r0
0x025246  bne       0x025256
0x025248  mov.l     #0x0000a616, er0
0x02524E  mov.l     er0, @0x400c78
0x025256  sub.w     r0, r0
0x025258  mov.w     r0, @(0x46,sp)
0x02525C  mov.l     #0x00000046, er0
0x025262  add.l     sp, er0
0x025264  mov.l     er0, @-sp
0x025268  mov.l     er6, er0
0x02526A  adds.l    #4, er0
0x02526C  adds.l    #4, er0
0x02526E  mov.w     r4, r1
0x025270  bsr       0x025a56
0x025274  adds.l    #4, sp
0x025276  mov.w     @(0x46,sp), r0
0x02527A  cmp.w     r4, r0
0x02527C  bcc       0x025288
0x02527E  mov.w     @er5, r0
0x025280  cmp.w     #0x0053, r0
0x025284  beq       0x0254e6
0x025288  mov.l     er6, er4
0x02528A  adds.l    #4, er4
0x02528C  adds.l    #4, er4
0x02528E  mov.l     er4, er2
0x025290  mov.b     @er4, r4l
0x025292  cmp.b     #0x09, r4l
0x025294  bne       0x0252a8
0x025296  mov.l     #0x000000e8, er0
0x02529C  add.l     er3, er0
0x02529E  mov.l     er0, @(0x4e,sp)
0x0252A4  mov.b     #0x04, r4l
0x0252A6  bt        0x0252da
0x0252A8  mov.b     @(0x8,er6), r0l
0x0252AC  cmp.b     #0x04, r0l
0x0252AE  bne       0x0252c2
0x0252B0  mov.l     #0x00000122, er0
0x0252B6  add.l     er3, er0
0x0252B8  mov.l     er0, @(0x4e,sp)
0x0252BE  mov.b     #0x05, r4l
0x0252C0  bt        0x0252da
0x0252C2  mov.b     @(0x8,er6), r4h
0x0252C6  mov.b     r4h, r0l
0x0252C8  extu.w    r0
0x0252CA  mov.w     #0x003a, e0
0x0252CE  mulxu.w   e0, er0
0x0252D0  add.l     er3, er0
0x0252D2  mov.l     er0, @(0x4e,sp)
0x0252D8  mov.b     r4h, r4l
0x0252DA  mov.l     er2, er0
0x0252DC  mov.b     @(0x29,er0), r0l
0x0252E0  and.b     #0x01, r0l
0x0252E2  mov.b     r0l, @(0x49,sp)
0x0252E6  sub.b     r4h, r4h
0x0252E8  bt        0x025308
0x0252EA  mov.l     @(0x4e,sp), er0
0x0252F0  inc.l     #1, er0
0x0252F2  mov.l     er0, @(0x4e,sp)
0x0252F8  dec.l     #1, er0
0x0252FA  mov.l     er2, er1
0x0252FC  inc.l     #1, er1
0x0252FE  mov.l     er1, er2
0x025300  dec.l     #1, er1
0x025302  mov.b     @er1, r1l
0x025304  mov.b     r1l, @er0
0x025306  inc.b     #1, r4h
0x025308  mov.b     @(0x47,sp), r0l
0x02530C  cmp.b     r0l, r4h
0x02530E  bcs       0x0252ea
0x025310  mov.l     er6, er0
0x025312  adds.l    #4, er0
0x025314  adds.l    #4, er0
0x025316  mov.l     er0, @(0x4e,sp)
0x02531C  mov.b     @er0, r0l
0x02531E  jsr       0x02dab2
0x025322  btst      #7, @0x400445
0x02532A  bne       0x025342
0x02532C  mov.l     @(0x4e,sp), er0
0x025332  mov.b     @er0, r0l
0x025334  cmp.b     #0x09, r0l
0x025336  bne       0x025342
0x025338  mov.w     #0x0050, r0
0x02533C  mov.w     r0, @er5
0x02533E  jmp       0x0254e6
0x025342  mov.w     #0x005d, e0
0x025346  mov.b     @0x400508, r0l
0x02534C  jsr       0x0119a6
0x025350  mov.b     r4l, r0l
0x025352  extu.w    r0
0x025354  mov.w     #0x003a, e0
0x025358  mulxu.w   e0, er0
0x02535A  add.l     er3, er0
0x02535C  add.l     #0x0000002a, er0
0x025362  mov.b     @er0, r0l
0x025364  and.b     #0x13, r0l
0x025366  extu.w    r0
0x025368  beq       0x0254e6
0x02536C  mov.b     @(0x8,er6), r0l
0x025370  bne       0x02537a
0x025372  mov.b     #0x01, r0l
0x025374  mov.b     r0l, @(0x53,sp)
0x025378  bt        0x0253a0
0x02537A  mov.b     @(0x8,er6), r0l
0x02537E  cmp.b     #0x09, r0l
0x025380  bne       0x02538a
0x025382  mov.b     #0x03, r0l
0x025384  mov.b     r0l, @(0x53,sp)
0x025388  bt        0x0253a0
0x02538A  mov.b     @(0x8,er6), r0l
0x02538E  cmp.b     #0x04, r0l
0x025390  bne       0x025396
0x025392  sub.b     r0l, r0l
0x025394  bt        0x02539c
0x025396  mov.b     @(0x8,er6), r0l
0x02539A  add.b     #0xff, r0l
0x02539C  mov.b     r0l, @(0x53,sp)
0x0253A0  mov.w     @(0x46,sp), r0
0x0253A4  cmp.w     #0x0034, r0
0x0253A8  bcs       0x0253fa
0x0253AA  mov.b     r4l, r0l
0x0253AC  extu.w    r0
0x0253AE  mov.w     #0x003a, e0
0x0253B2  mulxu.w   e0, er0
0x0253B4  add.l     er3, er0
0x0253B6  mov.w     #0x0033, r1
0x0253BA  jsr       0x01605a
0x0253BE  mov.w     r0, e4
0x0253C0  beq       0x0253fa
0x0253C2  mov.b     @(0x53,sp), r0l
0x0253C6  extu.w    r0
0x0253C8  mov.w     #0x0006, e0
0x0253CC  mulxu.w   e0, er0
0x0253CE  add.l     #0x0041ff3e, er0
0x0253D4  mov.l     er0, @(0x4e,sp)
0x0253DA  mov.w     e4, r1
0x0253DC  dec.w     #1, r1
0x0253DE  mov.w     r1, @er0
0x0253E0  mov.w     e4, r0
0x0253E2  dec.w     #1, r0
0x0253E4  mov.l     @(0x4e,sp), er1
0x0253EA  inc.l     #2, er1
0x0253EC  mov.w     r0, @er1
0x0253EE  dec.w     #1, e4
0x0253F0  mov.l     @(0x4e,sp), er0
0x0253F6  adds.l    #4, er0
0x0253F8  mov.w     e4, @er0
0x0253FA  mov.w     @(0x46,sp), r0
0x0253FE  cmp.w     #0x0039, r0
0x025402  bcs       0x025424
0x025404  extu.w    r4
0x025406  mov.w     #0x003a, r0
0x02540A  mulxu.w   r4, er0
0x02540C  add.l     er3, er0
0x02540E  add.l     #0x00000039, er0
0x025414  mov.b     @er0, r4h
0x025416  beq       0x025424
0x025418  add.b     #0xff, r4h
0x02541A  mov.b     @(0x53,sp), r0h
0x02541E  mov.b     r4h, r0l
0x025420  jsr       0x0322b4
0x025424  mov.w     @(0x46,sp), r0
0x025428  cmp.w     #0x0031, r0
0x02542C  bcs       0x02546e
0x02542E  mov.b     r4l, r0l
0x025430  extu.w    r0
0x025432  mov.w     #0x003a, e0
0x025436  mulxu.w   e0, er0
0x025438  add.l     er3, er0
0x02543A  mov.w     #0x002e, r1
0x02543E  jsr       0x016022
0x025442  mov.l     er0, @(0x4e,sp)
0x025448  beq       0x02546e
0x02544A  sub.l     er0, er0
0x02544C  mov.b     @(0x49,sp), r0l
0x025450  shll.l    #2, er0
0x025452  shll.l    #2, er0
0x025454  sub.l     er1, er1
0x025456  mov.b     @(0x53,sp), r1l
0x02545A  shll.l    #2, er1
0x02545C  add.l     #0x00400e1c, er0
0x025462  add.l     er1, er0
0x025464  mov.l     @(0x4e,sp), er1
0x02546A  mov.l     er1, @er0
0x02546E  mov.w     @(0x46,sp), r0
0x025472  cmp.w     #0x0038, r0
0x025476  bcs       0x0254e6
0x025478  mov.b     r4l, r0l
0x02547A  extu.w    r0
0x02547C  mov.w     #0x003a, e0
0x025480  mulxu.w   e0, er0
0x025482  add.l     er3, er0
0x025484  mov.w     #0x0035, r1
0x025488  jsr       0x016022
0x02548C  mov.l     er0, er4
0x02548E  beq       0x0254e6
0x025490  sub.l     er0, er0
0x025492  mov.b     @(0x49,sp), r0l
0x025496  shll.l    #2, er0
0x025498  shll.l    #2, er0
0x02549A  sub.l     er1, er1
0x02549C  mov.b     @(0x53,sp), r1l
0x0254A0  mov.l     er1, @(0x4e,sp)
0x0254A6  shll.l    #2, er1
0x0254A8  add.l     #0x00400e1c, er0
0x0254AE  add.l     er1, er0
0x0254B0  mov.l     er0, @sp
0x0254B4  mov.l     er4, er0
0x0254B6  jsr       0x018e9e
0x0254BA  mov.l     @(0x4e,sp), er1
0x0254C0  sub.l     er2, er2
0x0254C2  mov.b     @(0x41ff6e,er1), r2l
0x0254CA  shll.l    #2, er2
0x0254CC  mov.l     @(0x400dda,er2), er1
0x0254D6  jsr       0x018cac
0x0254DA  jsr       0x018860
0x0254DE  mov.l     @sp, er1
0x0254E2  mov.l     er0, @er1
0x0254E6  add.l     #0x00000054, sp
0x0254EC  ldm.l     @sp+, er4-er6
0x0254F0  ldm.l     @sp+, er2-er3
0x0254F4  rts       
