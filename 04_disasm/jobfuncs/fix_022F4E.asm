0x022F4E  orc       #0x40, ccr
0x022F50  mov.b     @(0x1,er0), r2l
0x022F54  mov.l     @(0x440,sp), er0
0x022F5A  mov.l     @(0x2,er0), er1
0x022F60  mov.l     er1, @(0x43c,sp)
0x022F66  mov.l     @(0x6,er0), er4
0x022F6C  mov.b     @(0xa,er0), r1l
0x022F70  mov.b     r1l, @(0x427,sp)
0x022F74  bt        0x022f8c
0x022F8C  mov.b     @0x40043e, r0l
0x022F92  mov.b     r0l, @(0x433,sp)
0x022F96  mov.b     @0x400440, r5l
0x022F9C  mov.b     @0x400441, r5h
0x022FA2  mov.b     r0l, r0l
0x022FA4  bne       0x022fc8
0x022FA6  cmp.b     #0x01, r5h
0x022FA8  bls       0x022fb2
0x022FAA  mov.w     #0x0050, r0
0x022FAE  jmp       0x023822
0x022FB2  mov.w     @0x400402, r0
0x022FB8  beq       0x022fd6
0x022FBA  mov.w     @0x400402, r0
0x022FC0  jsr       0x0211b6
0x022FC4  jmp       0x023822
0x022FC8  mov.b     r2l, r0l
0x022FCA  cmp.b     r0l, r5h
0x022FCC  beq       0x022fd6
0x022FCE  mov.w     #0x0050, r0
0x022FD2  jmp       0x023822
0x022FD6  mov.b     @0x400443, r0l
0x022FDC  extu.w    r0
0x022FDE  mov.b     r0l, r0h
0x022FE0  sub.b     r0l, r0l
0x022FE2  mov.b     @0x400444, r1l
0x022FE8  extu.w    r1
0x022FEA  or.w      r1, r0
0x022FEC  extu.l    er0
0x022FEE  sub.l     er1, er1
0x022FF0  mov.b     @0x400442, r1l
0x022FF6  mov.w     r1, e1
0x022FF8  sub.w     r1, r1
0x022FFA  or.l      er1, er0
0x022FFE  mov.l     er0, @(0x440,sp)
0x023004  mov.b     @(0x433,sp), r0l
0x023008  beq       0x023042
0x02300A  cmp.b     #0x03, r0l
0x02300C  beq       0x02305a
0x02300E  cmp.b     #0x81, r0l
0x023010  beq       0x02319c
0x023014  cmp.b     #0x84, r0l
0x023016  beq       0x023102
0x02301A  cmp.b     #0x87, r0l
0x02301C  beq       0x02320a
0x023020  cmp.b     #0x88, r0l
0x023022  beq       0x023214
0x023026  cmp.b     #0x8a, r0l
0x023028  beq       0x0234a2
0x02302C  cmp.b     #0x8c, r0l
0x02302E  beq       0x0234f6
0x023032  cmp.b     #0x8d, r0l
0x023034  beq       0x02358c
0x023038  cmp.b     #0xe0, r0l
0x02303A  beq       0x023770
0x02303E  jmp       0x023774
0x023042  cmp.b     #0x01, r5h
0x023044  bne       0x023774
0x023048  mov.w     @(0x442,sp), r0
0x02304C  btst      #0, r0l
0x02304E  beq       0x023774
0x023052  mov.w     #0x0050, r0
0x023056  jmp       0x023822
0x02305A  mov.b     r5l, r5l
0x02305C  bne       0x02306e
0x02305E  mov.l     @0x03e4ec, er4
0x023066  mov.b     #0x01, r0l
0x023068  mov.b     r0l, @(0x42d,sp)
0x02306C  bt        0x0230ac
0x02306E  cmp.b     #0x01, r5l
0x023070  bcs       0x023090
0x023072  cmp.b     #0x03, r5l
0x023074  bhi       0x023090
0x023076  mov.b     r5l, r4l
0x023078  extu.w    r4
0x02307A  extu.l    er4
0x02307C  shll.l    #2, er4
0x02307E  mov.l     @(0x3e4e4,er4), er4
0x023088  add.b     #0xff, r5l
0x02308A  mov.b     r5l, @(0x42d,sp)
0x02308E  bt        0x0230ac
0x023090  cmp.b     #0x09, r5l
0x023092  bne       0x0230a4
0x023094  mov.l     @0x03e4f4, er4
0x02309C  mov.b     #0x03, r0l
0x02309E  mov.b     r0l, @(0x42d,sp)
0x0230A2  bt        0x0230ac
0x0230A4  mov.w     #0x0050, r0
0x0230A8  jmp       0x023822
0x0230AC  btst      #7, @0x400445
0x0230B4  bne       0x0230d0
0x0230B6  sub.l     er0, er0
0x0230B8  mov.b     @(0x42d,sp), r0l
0x0230BC  mov.b     @(0x400f2e,er0), r0l
0x0230C4  cmp.b     #0x01, r0l
0x0230C6  bne       0x0230d0
0x0230C8  mov.l     @0x03e4f4, er4
0x0230D0  mov.w     @(0x442,sp), r0
0x0230D4  btst      #0, r0l
0x0230D6  beq       0x0230e0
0x0230D8  mov.w     #0x0050, r0
0x0230DC  jmp       0x023822
0x0230E0  sub.w     r5, r5
0x0230E2  mov.w     @0x400406, r0
0x0230E8  and.w     #0x00ff, r0
0x0230EC  cmp.w     #0x0001, r0
0x0230F0  bne       0x0230fc
0x0230F2  mov.b     @0x400d78, r0l
0x0230F8  beq       0x023190
0x0230FC  jsr       0x010b56
0x023100  bt        0x0230e2
0x023102  mov.l     #0x0003e508, er4
0x023108  mov.b     r5l, r5l
0x02310A  bne       0x02311a
0x02310C  mov.l     @(0x4,er4), er4
0x023112  mov.b     #0x01, r0l
0x023114  mov.b     r0l, @(0x42d,sp)
0x023118  bt        0x023154
0x02311A  cmp.b     #0x01, r5l
0x02311C  bcs       0x02313a
0x02311E  cmp.b     #0x03, r5l
0x023120  bhi       0x02313a
0x023122  mov.b     r5l, r0l
0x023124  extu.w    r0
0x023126  extu.l    er0
0x023128  shll.l    #2, er0
0x02312A  add.l     er0, er4
0x02312C  subs.l    #4, er4
0x02312E  mov.l     @er4, er4
0x023132  add.b     #0xff, r5l
0x023134  mov.b     r5l, @(0x42d,sp)
0x023138  bt        0x023154
0x02313A  cmp.b     #0x09, r5l
0x02313C  bne       0x02314c
0x02313E  mov.l     @(0xc,er4), er4
0x023144  mov.b     #0x03, r0l
0x023146  mov.b     r0l, @(0x42d,sp)
0x02314A  bt        0x023154
0x02314C  mov.w     #0x0050, r0
0x023150  jmp       0x023822
0x023154  mov.w     @(0x442,sp), r0
0x023158  btst      #0, r0l
0x02315A  beq       0x023164
0x02315C  mov.w     #0x0050, r0
0x023160  jmp       0x023822
0x023164  mov.l     @(0x43c,sp), er0
0x02316A  add.l     #0x00004e20, er0
0x023170  mov.l     er0, @(0x43c,sp)
0x023176  mov.w     #0x0006, r5
0x02317A  mov.w     @0x400406, r0
0x023180  and.w     #0x00ff, r0
0x023184  cmp.w     #0x0001, r0
0x023188  beq       0x023190
0x02318A  jsr       0x010b56
0x02318E  bt        0x02317a
0x023190  mov.b     #0x01, r0l
0x023192  mov.b     r0l, @0x400d74
0x023198  jmp       0x023774
0x02319C  mov.l     #0x00400e5c, er4
0x0231A2  mov.w     @er4, r0
0x0231A4  mov.w     r0, @sp
0x0231A6  mov.w     @(0x2,er4), r0
0x0231AA  mov.w     r0, @(0x2,sp)
0x0231AE  mov.w     @(0x4,er4), r0
0x0231B2  mov.w     r0, @(0x4,sp)
0x0231B6  mov.w     @(0x6,er4), r4
0x0231BA  mov.w     r4, @(0x6,sp)
0x0231BE  mov.b     r5l, r5l
0x0231C0  bne       0x0231cc
0x0231C2  mov.l     #0x00000002, er4
0x0231C8  add.l     sp, er4
0x0231CA  bt        0x0231f8
0x0231CC  cmp.b     #0x01, r5l
0x0231CE  bcs       0x0231e2
0x0231D0  cmp.b     #0x03, r5l
0x0231D2  bhi       0x0231e2
0x0231D4  sub.l     er4, er4
0x0231D6  mov.b     r5l, r4l
0x0231D8  shll.l    er4
0x0231DA  mov.l     sp, er0
0x0231DC  add.l     er0, er4
0x0231DE  dec.l     #2, er4
0x0231E0  bt        0x0231f8
0x0231E2  cmp.b     #0x09, r5l
0x0231E4  bne       0x0231f0
0x0231E6  mov.l     #0x00000006, er4
0x0231EC  add.l     sp, er4
0x0231EE  bt        0x0231f8
0x0231F0  mov.w     #0x0050, r0
0x0231F4  jmp       0x023822
0x0231F8  mov.w     @(0x442,sp), r0
0x0231FC  btst      #0, r0l
0x0231FE  beq       0x02376a
0x023202  mov.w     #0x0050, r0
0x023206  jmp       0x023822
0x02320A  mov.l     #0x004007d1, er4
0x023210  jmp       0x02376a
0x023214  mov.l     @(0x440,sp), er0
0x02321A  subs.l    #4, er0
0x02321C  dec.l     #2, er0
0x02321E  and.l     #0x00000003, er0
0x023224  beq       0x02322e
0x023226  mov.w     #0x0050, r0
0x02322A  jmp       0x023822
0x02322E  mov.b     @0x4003fb, r0l
0x023234  cmp.b     #0x17, r0l
0x023236  beq       0x023246
0x023238  cmp.b     #0x18, r0l
0x02323A  beq       0x023246
0x02323C  mov.w     #0x0053, r1
0x023240  mov.w     r1, @er3
0x023242  jmp       0x023a2a
0x023246  mov.b     @0x40041a, r0l
0x02324C  extu.w    r0
0x02324E  shll.w    #2, r0
0x023250  shll.w    #2, r0
0x023252  add.w     #0x0004, r0
0x023256  exts.l    er0
0x023258  mov.l     er0, @(0x43c,sp)
0x02325E  mov.b     r0h, r0l
0x023260  sub.b     r0h, r0h
0x023262  mov.b     r0l, @(0x6,er6)
0x023266  mov.b     @(0x43f,sp), r0l
0x02326A  mov.b     r0l, @(0x7,er6)
0x02326E  mov.b     @0x40041a, r0l
0x023274  mov.b     r0l, @(0x8,er6)
0x023278  sub.b     r0l, r0l
0x02327A  mov.b     r0l, @(0x9,er6)
0x02327E  mov.w     #0x000a, r5
0x023282  sub.w     e5, e5
0x023284  jmp       0x023480
0x023288  mov.w     r5, r0
0x02328A  inc.w     #1, r5
0x02328C  extu.l    er0
0x02328E  add.l     er6, er0
0x023290  mov.w     e5, r1
0x023292  extu.l    er1
0x023294  shll.l    #2, er1
0x023296  mov.l     er1, @(0x42e,sp)
0x02329C  add.l     #0x004203f8, er1
0x0232A2  mov.l     er1, @(0x438,sp)
0x0232A8  mov.w     @er1, r2
0x0232AA  sub.w     e2, e2
0x0232AC  mov.b     r2h, r2l
0x0232AE  sub.b     r2h, r2h
0x0232B0  mov.b     r2l, @er0
0x0232B2  mov.w     r5, r0
0x0232B4  inc.w     #1, r5
0x0232B6  extu.l    er0
0x0232B8  add.l     er6, er0
0x0232BA  mov.l     @(0x438,sp), er1
0x0232C0  mov.w     @er1, r2
0x0232C2  mov.b     r2l, @er0
0x0232C4  mov.w     r5, r0
0x0232C6  inc.w     #1, r5
0x0232C8  extu.l    er0
0x0232CA  add.l     er6, er0
0x0232CC  mov.b     @(0x2,er1), r2l
0x0232D0  sub.b     r2h, r2h
0x0232D2  mov.b     r2l, @er0
0x0232D4  mov.w     r5, r0
0x0232D6  inc.w     #1, r5
0x0232D8  extu.l    er0
0x0232DA  add.l     er6, er0
0x0232DC  mov.b     @(0x3,er1), r1l
0x0232E0  mov.b     r1l, @er0
0x0232E2  mov.w     r5, r0
0x0232E4  inc.w     #1, r5
0x0232E6  extu.l    er0
0x0232E8  add.l     er6, er0
0x0232EA  mov.l     @(0x42e,sp), er1
0x0232F0  add.l     #0x00420308, er1
0x0232F6  mov.l     er1, @(0x434,sp)
0x0232FC  mov.w     @er1, r2
0x0232FE  sub.w     e2, e2
0x023300  mov.b     r2h, r2l
0x023302  sub.b     r2h, r2h
0x023304  mov.b     r2l, @er0
0x023306  mov.w     r5, r0
0x023308  inc.w     #1, r5
0x02330A  extu.l    er0
0x02330C  add.l     er6, er0
0x02330E  mov.l     @(0x434,sp), er1
0x023314  mov.w     @er1, r2
0x023316  mov.b     r2l, @er0
0x023318  mov.w     r5, r0
0x02331A  inc.w     #1, r5
0x02331C  extu.l    er0
0x02331E  add.l     er6, er0
0x023320  mov.b     @(0x2,er1), r2l
0x023324  sub.b     r2h, r2h
0x023326  mov.b     r2l, @er0
0x023328  mov.w     r5, r0
0x02332A  inc.w     #1, r5
0x02332C  extu.l    er0
0x02332E  add.l     er6, er0
0x023330  mov.b     @(0x3,er1), r1l
0x023334  mov.b     r1l, @er0
0x023336  mov.w     r5, r0
0x023338  inc.w     #1, r5
0x02333A  extu.l    er0
0x02333C  add.l     er6, er0
0x02333E  mov.l     @(0x438,sp), er1
0x023344  mov.l     @(0x42e,sp), er2
0x02334A  add.l     #0x004205d8, er2
0x023350  mov.l     er2, @(0x428,sp)
0x023356  mov.l     @er1, er1
0x02335A  mov.l     @er2, er2
0x02335E  add.l     er2, er1
0x023360  dec.l     #1, er1
0x023362  mov.w     e1, r1
0x023364  sub.w     e1, e1
0x023366  mov.b     r1h, r1l
0x023368  sub.b     r1h, r1h
0x02336A  mov.b     r1l, @er0
0x02336C  mov.w     r5, r0
0x02336E  inc.w     #1, r5
0x023370  extu.l    er0
0x023372  add.l     er6, er0
0x023374  mov.l     @(0x438,sp), er1
0x02337A  mov.l     @(0x428,sp), er2
0x023380  mov.l     @er1, er1
0x023384  mov.l     @er2, er2
0x023388  add.l     er2, er1
0x02338A  dec.l     #1, er1
0x02338C  mov.w     e1, r1
0x02338E  sub.w     e1, e1
0x023390  mov.b     r1l, @er0
0x023392  mov.w     r5, r0
0x023394  inc.w     #1, r5
0x023396  extu.l    er0
0x023398  add.l     er6, er0
0x02339A  mov.l     @(0x438,sp), er1
0x0233A0  mov.l     @(0x428,sp), er2
0x0233A6  mov.w     @(0x2,er1), r1
0x0233AA  mov.w     @(0x2,er2), r2
0x0233AE  add.w     r2, r1
0x0233B0  dec.w     #1, r1
0x0233B2  mov.b     r1h, r1l
0x0233B4  sub.b     r1h, r1h
0x0233B6  mov.b     r1l, @er0
0x0233B8  mov.w     r5, r0
0x0233BA  inc.w     #1, r5
0x0233BC  extu.l    er0
0x0233BE  add.l     er6, er0
0x0233C0  mov.l     @(0x438,sp), er1
0x0233C6  mov.l     @(0x428,sp), er2
0x0233CC  mov.b     @(0x3,er1), r1l
0x0233D0  mov.b     @(0x3,er2), r2l
0x0233D4  add.b     r2l, r1l
0x0233D6  add.b     #0xff, r1l
0x0233D8  mov.b     r1l, @er0
0x0233DA  mov.w     r5, r0
0x0233DC  inc.w     #1, r5
0x0233DE  extu.l    er0
0x0233E0  add.l     er6, er0
0x0233E2  mov.l     @(0x434,sp), er1
0x0233E8  mov.l     @(0x42e,sp), er2
0x0233EE  add.l     #0x004204e8, er2
0x0233F4  mov.l     er2, @(0x438,sp)
0x0233FA  mov.l     @er1, er1
0x0233FE  mov.l     @er2, er2
0x023402  add.l     er2, er1
0x023404  dec.l     #1, er1
0x023406  mov.w     e1, r1
0x023408  sub.w     e1, e1
0x02340A  mov.b     r1h, r1l
0x02340C  sub.b     r1h, r1h
0x02340E  mov.b     r1l, @er0
0x023410  mov.w     r5, r0
0x023412  inc.w     #1, r5
0x023414  extu.l    er0
0x023416  add.l     er6, er0
0x023418  mov.l     @(0x434,sp), er1
0x02341E  mov.l     @(0x438,sp), er2
0x023424  mov.l     @er1, er1
0x023428  mov.l     @er2, er2
0x02342C  add.l     er2, er1
0x02342E  dec.l     #1, er1
0x023430  mov.w     e1, r1
0x023432  sub.w     e1, e1
0x023434  mov.b     r1l, @er0
0x023436  mov.w     r5, r0
0x023438  inc.w     #1, r5
0x02343A  extu.l    er0
0x02343C  add.l     er6, er0
0x02343E  mov.l     @(0x434,sp), er1
0x023444  mov.l     @(0x438,sp), er2
0x02344A  mov.w     @(0x2,er1), r1
0x02344E  mov.w     @(0x2,er2), r2
0x023452  add.w     r2, r1
0x023454  dec.w     #1, r1
0x023456  mov.b     r1h, r1l
0x023458  sub.b     r1h, r1h
0x02345A  mov.b     r1l, @er0
0x02345C  mov.w     r5, r0
0x02345E  inc.w     #1, r5
0x023460  extu.l    er0
0x023462  add.l     er6, er0
0x023464  mov.l     @(0x434,sp), er1
0x02346A  mov.l     @(0x438,sp), er2
0x023470  mov.b     @(0x3,er1), r1l
0x023474  mov.b     @(0x3,er2), r2l
0x023478  add.b     r2l, r1l
0x02347A  add.b     #0xff, r1l
0x02347C  mov.b     r1l, @er0
0x02347E  inc.w     #1, e5
0x023480  mov.b     @0x40041a, r0l
0x023486  extu.w    r0
0x023488  cmp.w     r0, e5
0x02348A  bcs       0x023288
0x02348E  mov.l     @(0x43c,sp), er0
0x023494  adds.l    #4, er0
0x023496  inc.l     #2, er0
0x023498  mov.l     er0, @(0x43c,sp)
0x02349E  jmp       0x02376a
0x0234A2  mov.l     @(0x440,sp), er0
0x0234A8  subs.l    #4, er0
0x0234AA  dec.l     #2, er0
0x0234AC  and.l     #0x00000003, er0
0x0234B2  beq       0x0234bc
0x0234B4  mov.w     #0x0050, r0
0x0234B8  jmp       0x023822
0x0234BC  mov.l     #0x00400dda, er4
0x0234C2  mov.b     @er4+, r0l
0x0234C4  mov.b     r0l, @(0x6,er6)
0x0234C8  mov.b     @er4+, r0l
0x0234CA  mov.b     r0l, @(0x7,er6)
0x0234CE  mov.b     @er4+, r0l
0x0234D0  mov.b     r0l, @(0x8,er6)
0x0234D4  mov.b     @er4+, r0l
0x0234D6  mov.b     r0l, @(0x9,er6)
0x0234DA  mov.b     @er4+, r0l
0x0234DC  mov.b     r0l, @(0xa,er6)
0x0234E0  mov.b     @er4+, r0l
0x0234E2  mov.b     r0l, @(0xb,er6)
0x0234E6  mov.b     @er4+, r0l
0x0234E8  mov.b     r0l, @(0xc,er6)
0x0234EC  mov.b     @er4, r0l
0x0234EE  mov.b     r0l, @(0xd,er6)
0x0234F2  jmp       0x02376a
0x0234F6  mov.l     #0x00400f32, er4
0x0234FC  mov.b     r5l, r5l
0x0234FE  bne       0x023518
0x023500  mov.l     @(0x4,er4), er4
0x023506  mov.l     @0x400f46, er0
0x02350E  add.l     er0, er4
0x023510  mov.l     er4, @(0x418,sp)
0x023516  bt        0x023566
0x023518  cmp.b     #0x01, r5l
0x02351A  bcs       0x023542
0x02351C  cmp.b     #0x03, r5l
0x02351E  bhi       0x023542
0x023520  sub.l     er0, er0
0x023522  mov.b     r5l, r0l
0x023524  shll.l    #2, er0
0x023526  add.l     er0, er4
0x023528  subs.l    #4, er4
0x02352A  mov.l     @er4, er4
0x02352E  mov.l     @(0x400f3e,er0), er0
0x023538  add.l     er0, er4
0x02353A  mov.l     er4, @(0x418,sp)
0x023540  bt        0x023566
0x023542  cmp.b     #0x09, r5l
0x023544  bne       0x02355e
0x023546  mov.l     @(0xc,er4), er4
0x02354C  mov.l     @0x400f4e, er0
0x023554  add.l     er0, er4
0x023556  mov.l     er4, @(0x418,sp)
0x02355C  bt        0x023566
0x02355E  mov.w     #0x0050, r0
0x023562  jmp       0x023822
0x023566  mov.l     @(0x440,sp), er0
0x02356C  subs.l    #4, er0
0x02356E  dec.l     #2, er0
0x023570  and.l     #0x00000003, er0
0x023576  beq       0x023580
0x023578  mov.w     #0x0050, r0
0x02357C  jmp       0x023822
0x023580  mov.l     #0x00000418, er4
0x023586  add.l     sp, er4
0x023588  jmp       0x02376a
0x02358C  mov.b     r5l, r5l
0x02358E  bne       0x023594
0x023590  mov.b     #0x01, r4l
0x023592  bt        0x0235b2
0x023594  cmp.b     #0x01, r5l
0x023596  bcs       0x0235a2
0x023598  cmp.b     #0x03, r5l
0x02359A  bhi       0x0235a2
0x02359C  add.b     #0xff, r5l
0x02359E  mov.b     r5l, r4l
0x0235A0  bt        0x0235b2
0x0235A2  cmp.b     #0x09, r5l
0x0235A4  bne       0x0235aa
0x0235A6  mov.b     #0x03, r4l
0x0235A8  bt        0x0235b2
0x0235AA  mov.w     #0x0050, r0
0x0235AE  jmp       0x023822
0x0235B2  mov.l     @(0x440,sp), er0
0x0235B8  cmp.l     #0x00000006, er0
0x0235BE  bcc       0x0235c8
0x0235C0  mov.w     #0x0050, r0
0x0235C4  jmp       0x023822
0x0235C8  sub.l     er0, er0
0x0235CA  mov.b     r4l, r0l
0x0235CC  mov.l     er0, er2
0x0235CE  mov.l     #0x0000001c, er1
0x0235D4  jsr       0x018e1e
0x0235D8  mov.l     #0x004007e5, er5
0x0235DE  add.l     er0, er5
0x0235E0  mov.l     er5, er4
0x0235E2  sub.b     r0l, r0l
0x0235E4  mov.b     r0l, @er5
0x0235E6  mov.b     #0x18, r0l
0x0235E8  mov.b     r0l, @(0x1,er5)
0x0235EC  sub.b     r0l, r0l
0x0235EE  mov.b     r0l, @(0x2,er5)
0x0235F2  mov.l     er2, er0
0x0235F4  shll.l    er0
0x0235F6  mov.l     er0, @(0x428,sp)
0x0235FC  add.l     #0x00400ec6, er0
0x023602  mov.l     er0, @(0x41c,sp)
0x023608  mov.b     @er0, r1l
0x02360A  sub.b     r1h, r1h
0x02360C  mov.b     r1l, @(0x3,er5)
0x023610  mov.l     @(0x41c,sp), er0
0x023616  mov.b     @(0x1,er0), r0l
0x02361A  mov.b     r0l, @(0x4,er5)
0x02361E  mov.l     er2, er0
0x023620  shll.l    #2, er0
0x023622  mov.l     er0, @(0x42e,sp)
0x023628  add.l     #0x00400ede, er0
0x02362E  mov.l     er0, @(0x434,sp)
0x023634  mov.w     @er0, r1
0x023636  sub.w     e1, e1
0x023638  mov.b     r1h, r1l
0x02363A  sub.b     r1h, r1h
0x02363C  mov.b     r1l, @(0x5,er5)
0x023640  mov.l     @(0x434,sp), er0
0x023646  mov.w     @er0, r1
0x023648  mov.b     r1l, @(0x6,er5)
0x02364C  mov.b     @(0x2,er0), r1l
0x023650  sub.b     r1h, r1h
0x023652  mov.b     r1l, @(0x7,er5)
0x023656  mov.b     @(0x3,er0), r0l
0x02365A  mov.b     r0l, @(0x8,er5)
0x02365E  mov.l     @(0x42e,sp), er0
0x023664  add.l     #0x00400eee, er0
0x02366A  mov.l     er0, @(0x434,sp)
0x023670  mov.w     @er0, r1
0x023672  sub.w     e1, e1
0x023674  mov.b     r1h, r1l
0x023676  sub.b     r1h, r1h
0x023678  mov.b     r1l, @(0x9,er5)
0x02367C  mov.l     @(0x434,sp), er0
0x023682  mov.w     @er0, r1
0x023684  mov.b     r1l, @(0xa,er5)
0x023688  mov.b     @(0x2,er0), r1l
0x02368C  sub.b     r1h, r1h
0x02368E  mov.b     r1l, @(0xb,er5)
0x023692  mov.b     @(0x3,er0), r0l
0x023696  mov.b     r0l, @(0xc,er5)
0x02369A  mov.b     #0x01, r0l
0x02369C  mov.b     r0l, @(0xd,er5)
0x0236A0  mov.b     r0l, @(0xe,er5)
0x0236A4  mov.l     @(0x42e,sp), er0
0x0236AA  add.l     #0x00400efe, er0
0x0236B0  mov.l     er0, @(0x434,sp)
0x0236B6  mov.w     @er0, r1
0x0236B8  sub.w     e1, e1
0x0236BA  mov.b     r1h, r1l
0x0236BC  sub.b     r1h, r1h
0x0236BE  mov.b     r1l, @(0xf,er5)
0x0236C2  mov.l     @(0x434,sp), er0
0x0236C8  mov.w     @er0, r1
0x0236CA  mov.b     r1l, @(0x10,er5)
0x0236CE  mov.b     @(0x2,er0), r1l
0x0236D2  sub.b     r1h, r1h
0x0236D4  mov.b     r1l, @(0x11,er5)
0x0236D8  mov.b     @(0x3,er0), r0l
0x0236DC  mov.b     r0l, @(0x12,er5)
0x0236E0  mov.l     @(0x42e,sp), er0
0x0236E6  add.l     #0x00400f0e, er0
0x0236EC  mov.l     er0, @(0x434,sp)
0x0236F2  mov.w     @er0, r1
0x0236F4  sub.w     e1, e1
0x0236F6  mov.b     r1h, r1l
0x0236F8  sub.b     r1h, r1h
0x0236FA  mov.b     r1l, @(0x13,er5)
0x0236FE  mov.l     @(0x434,sp), er0
0x023704  mov.w     @er0, r1
0x023706  mov.b     r1l, @(0x14,er5)
0x02370A  mov.b     @(0x2,er0), r1l
0x02370E  sub.b     r1h, r1h
0x023710  mov.b     r1l, @(0x15,er5)
0x023714  mov.b     @(0x3,er0), r0l
0x023718  mov.b     r0l, @(0x16,er5)
0x02371C  mov.l     @(0x428,sp), er0
0x023722  add.l     #0x00400f1e, er0
0x023728  mov.l     er0, @(0x41c,sp)
0x02372E  mov.b     @er0, r1l
0x023730  mov.b     r1l, @(0x17,er5)
0x023734  mov.l     @(0x41c,sp), er0
0x02373A  mov.b     @(0x1,er0), r0l
0x02373E  mov.b     r0l, @(0x18,er5)
0x023742  mov.l     @(0x428,sp), er0
0x023748  add.l     #0x00400f26, er0
0x02374E  mov.l     er0, @(0x41c,sp)
0x023754  mov.b     @er0, r1l
0x023756  sub.b     r1h, r1h
0x023758  mov.b     r1l, @(0x19,er5)
0x02375C  mov.l     @(0x41c,sp), er0
0x023762  mov.b     @(0x1,er0), r0l
0x023766  mov.b     r0l, @(0x1a,er5)
0x02376A  mov.w     #0x0006, r5
0x02376E  bt        0x023774
0x023770  mov.w     #0x0006, r5
0x023774  mov.l     @(0x440,sp), er0
0x02377A  beq       0x023a2a
0x02377E  mov.l     @(0x43c,sp), er0
0x023784  beq       0x0237be
0x023786  mov.l     @(0x440,sp), er0
0x02378C  mov.l     @(0x43c,sp), er1
0x023792  cmp.l     er1, er0
0x023794  bls       0x0237be
0x023796  mov.w     #0x006f, r0
0x02379A  mov.w     r0, @er3
0x02379C  mov.l     @(0x440,sp), er0
0x0237A2  mov.l     @(0x43c,sp), er1
0x0237A8  sub.l     er1, er0
0x0237AA  mov.l     er0, @0x400426
0x0237B2  mov.l     @(0x43c,sp), er0
0x0237B8  mov.l     er0, @(0x440,sp)
0x0237BE  mov.b     @(0x433,sp), r0l
0x0237C2  bne       0x023828
0x0237C4  mov.w     @0x400406, r0
0x0237CA  and.w     #0x0020, r0
0x0237CE  cmp.w     #0x0020, r0
0x0237D2  beq       0x0237ee
0x0237D4  mov.w     #0x0056, r0
0x0237D8  mov.w     r0, @er3
0x0237DA  mov.w     @0x400400, r0
0x0237E0  and.w     #0x4000, r0
0x0237E4  cmp.w     #0x4000, r0
0x0237E8  bne       0x023a2a
0x0237EC  bt        0x02383e
0x0237EE  mov.l     @(0x440,sp), er0
0x0237F4  mov.l     er0, @0x40051e
0x0237FC  mov.l     @(0x440,sp), er0
0x023802  mov.l     er0, @0x400522
0x02380A  jsr       0x0211e4
0x02380E  mov.w     @0x400402, r0
0x023814  beq       0x023a2a
0x023818  mov.w     @0x400402, r0
0x02381E  jsr       0x0211b6
0x023822  mov.w     r0, @er3
0x023824  jmp       0x023a2a
0x023828  mov.w     @0x400406, r0
0x02382E  and.w     #0x0020, r0
0x023832  cmp.w     #0x0020, r0
0x023836  bne       0x02384a
0x023838  mov.w     #0x0056, r0
0x02383C  mov.w     r0, @er3
0x02383E  bset      #7, @0x400400
0x023846  jmp       0x023a2a
0x02384A  mov.b     @(0x433,sp), r0l
0x02384E  cmp.b     #0x03, r0l
0x023850  beq       0x023858
0x023852  cmp.b     #0x84, r0l
0x023854  bne       0x023986
0x023858  mov.b     @0x420264, r0l
0x02385E  bne       0x023868
0x023860  mov.l     #0x00c40000, er0
0x023866  bt        0x02386e
0x023868  mov.l     #0x00c00000, er0
0x02386E  mov.l     er0, @(0x428,sp)
0x023874  cmp.w     #0x0006, r5
0x023878  bne       0x0238da
0x02387A  mov.l     @(0x428,sp), er0
0x023880  inc.l     #2, er0
0x023882  mov.l     er0, @(0x428,sp)
0x023888  dec.l     #2, er0
0x02388A  mov.b     @(0x427,sp), r1l
0x02388E  extu.w    r1
0x023890  mov.b     r1l, r1h
0x023892  sub.b     r1l, r1l
0x023894  mov.b     @(0x433,sp), r2l
0x023898  extu.w    r2
0x02389A  or.w      r2, r1
0x02389C  mov.w     r1, @er0
0x02389E  mov.l     @(0x428,sp), er0
0x0238A4  inc.l     #2, er0
0x0238A6  mov.l     er0, @(0x428,sp)
0x0238AC  dec.l     #2, er0
0x0238AE  mov.l     @(0x43c,sp), er1
0x0238B4  subs.l    #4, er1
0x0238B6  dec.l     #2, er1
0x0238B8  mov.l     er1, @(0x41c,sp)
0x0238BE  mov.w     e1, r1
0x0238C0  sub.w     e1, e1
0x0238C2  mov.w     r1, @er0
0x0238C4  mov.l     @(0x428,sp), er0
0x0238CA  inc.l     #2, er0
0x0238CC  mov.l     er0, @(0x428,sp)
0x0238D2  dec.l     #2, er0
0x0238D4  mov.w     @(0x41e,sp), r1
0x0238D8  mov.w     r1, @er0
0x0238DA  mov.b     @(0x433,sp), r0l
0x0238DE  cmp.b     #0x03, r0l
0x0238E0  bne       0x02390a
0x0238E2  sub.l     er0, er0
0x0238E4  mov.b     @(0x42d,sp), r0l
0x0238E8  mov.b     @(0x400eb5,er0), r0l
0x0238F0  cmp.b     #0x08, r0l
0x0238F2  bne       0x02390a
0x0238F4  mov.l     @(0x428,sp), er0
0x0238FA  mov.l     er0, @-sp
0x0238FE  mov.l     er4, er1
0x023900  mov.b     #0x0e, r0l
0x023902  jsr       0x02e13c
0x023906  adds.l    #4, sp
0x023908  bt        0x023978
0x02390A  mov.b     @0xffff06, r0l
0x023910  and.b     #0x53, r0l
0x023912  or.b      #0x80, r0l
0x023914  mov.b     r0l, @0xffff06
0x02391A  mov.l     er4, @0xfffef0
0x023922  mov.l     @(0x428,sp), er0
0x023928  mov.l     er0, @0xfffef8
0x023930  mov.w     @(0x442,sp), r0
0x023934  sub.w     r5, r0
0x023936  shlr.w    r0
0x023938  mov.w     r0, @0xfffef6
0x02393E  mov.b     #0xa0, r0l
0x023940  mov.b     r0l, @0xffff04
0x023946  mov.b     #0x27, r0l
0x023948  mov.b     r0l, @0xffff05
0x02394E  mov.b     @0xffff07, r0l
0x023954  mov.b     r0l, @0x40041b
0x02395A  mov.b     #0xc0, r0l
0x02395C  mov.b     r0l, @0xffff07
0x023962  btst      #6, @0xffff07
0x02396A  beq       0x023978
0x02396C  mov.w     #0x5a00, r0
0x023970  mov.w     r0, @0xffffbc
0x023976  bt        0x023962
0x023978  mov.l     @(0x440,sp), er0
0x02397E  jsr       0x011930
0x023982  jmp       0x023a22
0x023986  cmp.w     #0x0006, r5
0x02398A  bne       0x0239dc
0x02398C  mov.b     @(0x433,sp), r0l
0x023990  mov.b     r0l, @er6
0x023992  mov.b     @(0x427,sp), r0l
0x023996  mov.b     r0l, @(0x1,er6)
0x02399A  mov.l     @(0x43c,sp), er0
0x0239A0  subs.l    #4, er0
0x0239A2  dec.l     #2, er0
0x0239A4  mov.l     er0, @(0x41c,sp)
0x0239AA  mov.w     e0, r0
0x0239AC  sub.w     e0, e0
0x0239AE  and.l     #0x0000ffff, er0
0x0239B4  mov.l     er0, @(0x434,sp)
0x0239BA  mov.b     r0h, r0l
0x0239BC  sub.b     r0h, r0h
0x0239BE  mov.b     r0l, @(0x2,er6)
0x0239C2  mov.b     @(0x437,sp), r0l
0x0239C6  mov.b     r0l, @(0x3,er6)
0x0239CA  mov.b     @(0x41e,sp), r0l
0x0239CE  sub.b     r0h, r0h
0x0239D0  mov.b     r0l, @(0x4,er6)
0x0239D4  mov.b     @(0x41f,sp), r0l
0x0239D8  mov.b     r0l, @(0x5,er6)
0x0239DC  mov.b     @(0x433,sp), r0l
0x0239E0  cmp.b     #0x88, r0l
0x0239E2  beq       0x023a18
0x0239E4  cmp.b     #0x8a, r0l
0x0239E6  beq       0x023a18
0x0239E8  mov.w     #0x5a00, r1
0x0239EC  mov.w     r1, @0xffffbc
0x0239F2  bt        0x023a00
0x0239F4  mov.b     @er4+, r0l
0x0239F6  mov.w     r5, r1
0x0239F8  extu.l    er1
0x0239FA  add.l     er6, er1
0x0239FC  mov.b     r0l, @er1
0x0239FE  inc.w     #1, r5
0x023A00  mov.w     r5, r0
0x023A02  extu.l    er0
0x023A04  mov.l     @(0x440,sp), er1
0x023A0A  cmp.l     er1, er0
0x023A0C  bcs       0x0239f4
0x023A0E  mov.w     #0x5a00, r0
0x023A12  mov.w     r0, @0xffffbc
0x023A18  mov.w     @(0x442,sp), r1
0x023A1C  mov.l     er6, er0
0x023A1E  jsr       0x011900
0x023A22  sub.b     r0l, r0l
0x023A24  mov.b     r0l, @0x400d74
0x023A2A  add.l     #0x00000444, sp
0x023A30  ldm.l     @sp+, er4-er6
0x023A34  ldm.l     @sp+, er2-er3
0x023A38  rts       
