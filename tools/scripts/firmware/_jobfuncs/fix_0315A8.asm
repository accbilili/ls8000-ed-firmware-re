0x031356  mov.b     @0x4206ec, r0l
0x03135C  bne       0x0313a8
0x03135E  sub.l     er1, er1
0x031360  mov.b     @er6, r1l
0x031362  mov.l     er1, @(0x80,sp)
0x031368  shll.l    #2, er1
0x03136A  mov.l     #0x00000030, er0
0x031370  add.l     sp, er0
0x031372  add.l     er0, er1
0x031374  mov.l     @er1, er1
0x031378  mov.l     #0x00000028, er0
0x03137E  add.l     sp, er0
0x031380  jsr       0x018e68
0x031384  mov.l     @(0x80,sp), er2
0x03138A  shll.l    #2, er2
0x03138C  shll.l    er2
0x03138E  add.l     #0x00420108, er2
0x031394  mov.l     er0, er1
0x031396  mov.l     #0x00000020, er0
0x03139C  add.l     sp, er0
0x03139E  jsr       0x018aa0
0x0313A2  jsr       0x01876a
0x0313A6  bt        0x0313ae
0x0313A8  mov.l     #0x0007a120, er0
0x0313AE  mov.l     er0, @er4
0x0313B2  sub.b     r0l, r0l
0x0313B4  mov.b     r0l, @(0x85,sp)
0x0313B8  sub.w     r0, r0
0x0313BA  mov.w     r0, @(0x98,sp)
0x0313BE  sub.l     er0, er0
0x0313C0  mov.b     @er6, r0l
0x0313C2  shll.l    er0
0x0313C4  mov.l     #0x00000074, er1
0x0313CA  add.l     sp, er1
0x0313CC  add.l     er0, er1
0x0313CE  mov.w     @er1, r0
0x0313D0  bne       0x0313e8
0x0313D2  sub.l     er0, er0
0x0313D4  mov.b     @er6, r0l
0x0313D6  shll.l    er0
0x0313D8  mov.l     #0x00000074, er1
0x0313DE  add.l     sp, er1
0x0313E0  add.l     er0, er1
0x0313E2  mov.w     #0x0001, r0
0x0313E6  mov.w     r0, @er1
0x0313E8  mov.l     @er4, er1
0x0313EC  mov.l     #0x00000028, er0
0x0313F2  add.l     sp, er0
0x0313F4  jsr       0x018e68
0x0313F8  mov.w     @(0x94,sp), r1
0x0313FC  mov.l     er0, @(0x1c,sp)
0x031402  mov.l     #0x00000020, er0
0x031408  add.l     sp, er0
0x03140A  jsr       0x018ede
0x03140E  mov.l     @(0x1c,sp), er1
0x031414  mov.l     er0, er2
0x031416  mov.l     #0x00000014, er0
0x03141C  add.l     sp, er0
0x03141E  jsr       0x018aa0
0x031422  sub.l     er1, er1
0x031424  mov.b     @er6, r1l
0x031426  shll.l    er1
0x031428  mov.l     #0x00000074, er2
0x03142E  add.l     sp, er2
0x031430  add.l     er1, er2
0x031432  mov.w     @er2, r1
0x031434  mov.l     er0, @(0x8,sp)
0x03143A  mov.l     #0x0000000c, er0
0x031440  add.l     sp, er0
0x031442  jsr       0x018ede
0x031446  mov.l     @(0x8,sp), er1
0x03144C  mov.l     er0, er2
0x03144E  mov.l     sp, er0
0x031450  jsr       0x01842c
0x031454  jsr       0x01876a
0x031458  mov.l     er0, @er4
0x03145C  bne       0x031468
0x03145E  mov.l     #0x00000001, er0
0x031464  mov.l     er0, @er4
0x031468  mov.b     @0x4206ec, r0l
0x03146E  bne       0x0314ac
0x031470  sub.l     er0, er0
0x031472  mov.b     @er6, r0l
0x031474  shll.l    #2, er0
0x031476  mov.l     #0x00000044, er1
0x03147C  add.l     sp, er1
0x03147E  add.l     er0, er1
0x031480  mov.l     @er4, er0
0x031484  mov.l     @er1, er1
0x031488  cmp.l     er1, er0
0x03148A  bls       0x0314ac
0x03148C  mov.b     @0x41ffa4, r0l
0x031492  bne       0x0314a0
0x031494  mov.b     @er6, r0l
0x031496  extu.w    r0
0x031498  inc.w     #1, r0
0x03149A  or.w      #0x0840, r0
0x03149E  bt        0x0314cc
0x0314A0  mov.b     @er6, r0l
0x0314A2  extu.w    r0
0x0314A4  inc.w     #1, r0
0x0314A6  or.w      #0x08a0, r0
0x0314AA  bt        0x0314cc
0x0314AC  mov.b     @0x4206ec, r0l
0x0314B2  cmp.b     #0x01, r0l
0x0314B4  bne       0x0314d4
0x0314B6  mov.l     @er4, er0
0x0314BA  cmp.l     #0x01c9c380, er0
0x0314C0  bls       0x0314d4
0x0314C2  mov.b     @er6, r0l
0x0314C4  extu.w    r0
0x0314C6  inc.w     #1, r0
0x0314C8  or.w      #0x0840, r0
0x0314CC  mov.w     r0, @(0x98,sp)
0x0314D0  jmp       0x0315a8
0x0314D4  mov.b     @er6, r1l
0x0314D6  extu.w    r1
0x0314D8  mov.w     #0x0006, e1
0x0314DC  mulxu.w   e1, er1
0x0314DE  add.l     #0x0041ff3e, er1
0x0314E4  mov.b     @er6, r0l
0x0314E6  jsr       0x02da8e
0x0314EA  sub.l     er0, er0
0x0314EC  mov.b     @er6, r0l
0x0314EE  mov.b     @(0x41ff6e,er0), r0h
0x0314F6  mov.b     @er6, r0l
0x0314F8  jsr       0x02daa2
0x0314FC  bsr       0x033284
0x031500  btst      #7, @0x400400
0x031508  bne       0x031976
0x03150C  mov.b     @0x41ffa4, r0l
0x031512  bne       0x03152c
0x031514  sub.l     er0, er0
0x031516  mov.b     @er6, r0l
0x031518  shll.l    er0
0x03151A  mov.l     #0x00000074, er1
0x031520  add.l     sp, er1
0x031522  add.l     er0, er1
0x031524  mov.w     @0x41ff74, r0
0x03152A  bt        0x031542
0x03152C  sub.l     er0, er0
0x03152E  mov.b     @er6, r0l
0x031530  shll.l    er0
0x031532  mov.l     #0x00000074, er1
0x031538  add.l     sp, er1
0x03153A  add.l     er0, er1
0x03153C  mov.w     @0x41ff76, r0
0x031542  mov.w     r0, @er1
0x031544  sub.l     er0, er0
0x031546  mov.b     @er6, r0l
0x031548  shll.l    er0
0x03154A  mov.l     #0x00000074, er1
0x031550  add.l     sp, er1
0x031552  add.l     er0, er1
0x031554  mov.w     @er1, r1
0x031556  mov.w     @(0x90,sp), r0
0x03155A  cmp.w     r0, r1
0x03155C  bls       0x03156c
0x03155E  mov.b     @er6, r0l
0x031560  extu.w    r0
0x031562  inc.w     #1, r0
0x031564  or.w      #0x0830, r0
0x031568  mov.w     r0, @(0x98,sp)
0x03156C  sub.l     er0, er0
0x03156E  mov.b     @er6, r0l
0x031570  shll.l    er0
0x031572  mov.l     #0x00000074, er1
0x031578  add.l     sp, er1
0x03157A  add.l     er0, er1
0x03157C  mov.w     @er1, r1
0x03157E  mov.w     @(0x8e,sp), r0
0x031582  cmp.w     r0, r1
0x031584  bcc       0x0315a8
0x031586  mov.b     @0x41ffa4, r0l
0x03158C  bne       0x03159a
0x03158E  mov.b     @er6, r0l
0x031590  extu.w    r0
0x031592  inc.w     #1, r0
0x031594  or.w      #0x0840, r0
0x031598  bt        0x0315a4
0x03159A  mov.b     @er6, r0l
0x03159C  extu.w    r0
0x03159E  inc.w     #1, r0
0x0315A0  or.w      #0x08a0, r0
0x0315A4  mov.w     r0, @(0x98,sp)
0x0315A8  mov.w     @(0x98,sp), r0
0x0315AC  beq       0x0315f6
0x0315AE  mov.b     @(0x85,sp), r0l
0x0315B2  inc.b     #1, r0l
0x0315B4  mov.b     r0l, @(0x85,sp)
0x0315B8  cmp.b     #0x10, r0l
0x0315BA  bls       0x0313b8
0x0315BE  mov.w     @(0x98,sp), r0
0x0315C2  mov.w     r0, @0x400402
0x0315C8  sub.l     er0, er0
0x0315CA  mov.b     @er6, r0l
0x0315CC  mov.l     er0, @(0x86,sp)
0x0315D2  mov.b     @(0x3fbe2,er0), r0l
0x0315DA  mov.b     @er3, r1l
0x0315DC  and.b     r0l, r1l
0x0315DE  mov.b     r1l, @er3
0x0315E0  mov.b     #0x01, r0l
0x0315E2  mov.b     r0l, @(0x9b,sp)
0x0315E6  mov.l     #0x00000040, er0
0x0315EC  add.l     sp, er0
0x0315EE  mov.l     @(0x86,sp), er1
0x0315F4  bt        0x03164e
0x0315F6  mov.b     @0x41ffa4, r0l
0x0315FC  cmp.b     #0x01, r0l
0x0315FE  bne       0x031654
0x031600  mov.w     @0x41ff74, r0
0x031606  shlr.w    r0
0x031608  mov.w     @0x41ff72, r1
0x03160E  cmp.w     r0, r1
0x031610  bhi       0x031654
0x031612  mov.b     @er6, r0l
0x031614  extu.w    r0
0x031616  inc.w     #1, r0
0x031618  or.w      #0x0890, r0
0x03161C  mov.w     r0, @0x400402
0x031622  sub.l     er0, er0
0x031624  mov.b     @er6, r0l
0x031626  mov.l     er0, @(0x80,sp)
0x03162C  mov.b     @(0x3fbe2,er0), r0l
0x031634  mov.b     @er3, r1l
0x031636  and.b     r0l, r1l
0x031638  mov.b     r1l, @er3
0x03163A  mov.b     #0x01, r0l
0x03163C  mov.b     r0l, @(0x9b,sp)
0x031640  mov.l     #0x00000040, er0
0x031646  add.l     sp, er0
0x031648  mov.l     @(0x80,sp), er1
0x03164E  add.l     er1, er0
0x031650  mov.b     #0x01, r1l
0x031652  mov.b     r1l, @er0
0x031654  mov.l     @er4, er0
0x031658  beq       0x03166c
0x03165A  sub.l     er0, er0
0x03165C  mov.b     @er6, r0l
0x03165E  shll.l    #2, er0
0x031660  add.l     er5, er0
0x031662  mov.l     @er4, er1
0x031666  mov.l     er1, @er0
0x03166A  bt        0x031688
0x03166C  sub.l     er0, er0
0x03166E  mov.b     @er6, r0l
0x031670  shll.l    #2, er0
0x031672  add.l     er5, er0
0x031674  mov.l     #0x00000001, er1
0x03167A  mov.l     er1, @er0
0x03167E  mov.l     #0x00000001, er0
0x031684  mov.l     er0, @er4
0x031688  mov.b     @(0x97,sp), r0l
0x03168C  extu.w    r0
0x03168E  mov.w     #0x0022, e0
0x031692  mulxu.w   e0, er0
0x031694  add.l     #0x0041ffb4, er0
0x03169A  mov.l     er0, @(0x86,sp)
0x0316A0  sub.l     er1, er1
0x0316A2  mov.b     @er6, r1l
0x0316A4  shll.l    er1
0x0316A6  add.l     #0x00000010, er0
0x0316AC  add.l     er1, er0
0x0316AE  mov.w     @0x41ff76, r1
0x0316B4  mov.w     r1, @er0
0x0316B6  sub.l     er0, er0
0x0316B8  mov.b     @er6, r0l
0x0316BA  shll.l    er0
0x0316BC  mov.l     @(0x86,sp), er1
0x0316C2  add.l     #0x00000018, er1
0x0316C8  add.l     er0, er1
0x0316CA  mov.w     @0x41ff74, r0
0x0316D0  mov.w     r0, @er1
0x0316D2  mov.b     @er6, r0l
0x0316D4  inc.b     #1, r0l
0x0316D6  mov.b     r0l, @er6
0x0316D8  mov.b     @(0x93,sp), r1l
0x0316DC  cmp.b     r1l, r0l
0x0316DE  bcs       0x031356
0x0316E2  mov.b     @0x4206ec, r0l
0x0316E8  cmp.b     #0x03, r0l
0x0316EA  bne       0x03171e
0x0316EC  sub.b     r0l, r0l
0x0316EE  bt        0x031718
0x0316F0  sub.l     er0, er0
0x0316F2  mov.b     @er6, r0l
0x0316F4  shll.l    #2, er0
0x0316F6  add.l     er5, er0
0x0316F8  mov.l     @er4, er1
0x0316FC  mov.l     er1, @er0
0x031700  sub.l     er0, er0
0x031702  mov.b     @er6, r0l
0x031704  shll.l    er0
0x031706  mov.w     @0x400f52, r1
0x03170C  mov.w     r1, @(0x400f52,er0)
0x031714  mov.b     @er6, r0l
0x031716  inc.b     #1, r0l
0x031718  mov.b     r0l, @er6
0x03171A  cmp.b     #0x04, r0l
0x03171C  bcs       0x0316f0
0x03171E  mov.b     @0x4206ec, r0l
0x031724  beq       0x031780
0x031726  sub.b     r0l, r0l
0x031728  bt        0x031772
0x03172A  sub.l     er0, er0
0x03172C  mov.b     @er6, r0l
0x03172E  shll.l    #2, er0
0x031730  sub.l     er1, er1
0x031732  mov.l     er1, @(0x400f42,er0)
0x03173C  sub.l     er0, er0
0x03173E  mov.b     @er6, r0l
0x031740  shll.l    er0
0x031742  mov.w     @(0x400e5c,er0), r1
0x03174A  bne       0x03176e
0x03174C  sub.l     er0, er0
0x03174E  mov.b     @er6, r0l
0x031750  shll.l    er0
0x031752  mov.l     er0, @(0x86,sp)
0x031758  mov.l     @(0x86,sp), er1
0x03175E  mov.w     @(0x400f52,er1), r1
0x031766  mov.w     r1, @(0x400e5c,er0)
0x03176E  mov.b     @er6, r0l
0x031770  inc.b     #1, r0l
0x031772  mov.b     r0l, @er6
0x031774  cmp.b     #0x04, r0l
0x031776  bcs       0x03172a
0x031778  bsr       0x0321a0
0x03177C  jmp       0x031976
0x031780  mov.b     @0x41ffa4, r0l
0x031786  cmp.b     #0x01, r0l
0x031788  bne       0x031958
0x03178C  sub.b     r0l, r0l
0x03178E  jmp       0x031924
0x031792  sub.l     er0, er0
0x031794  mov.b     @er6, r0l
0x031796  shll.l    #2, er0
0x031798  add.l     er5, er0
0x03179A  mov.l     er0, @(0x86,sp)
0x0317A0  mov.l     @(0x86,sp), er1
0x0317A6  mov.l     @er1, er1
0x0317AA  mov.l     er0, @(0x24,sp)
0x0317B0  mov.l     #0x00000028, er0
0x0317B6  add.l     sp, er0
0x0317B8  jsr       0x018e68
0x0317BC  mov.l     er0, er1
0x0317BE  mov.l     #0x0003f7a6, er2
0x0317C4  mov.l     #0x0000001c, er0
0x0317CA  add.l     sp, er0
0x0317CC  jsr       0x018aa0
0x0317D0  mov.w     @(0x94,sp), r1
0x0317D4  mov.l     er0, @(0x10,sp)
0x0317DA  mov.l     #0x00000014, er0
0x0317E0  add.l     sp, er0
0x0317E2  jsr       0x018ede
0x0317E6  mov.l     @(0x10,sp), er1
0x0317EC  mov.l     er0, er2
0x0317EE  mov.l     #0x00000008, er0
0x0317F4  add.l     sp, er0
0x0317F6  jsr       0x01842c
0x0317FA  jsr       0x01876a
0x0317FE  mov.l     @(0x24,sp), er1
0x031804  mov.l     er0, @er1
0x031808  mov.l     #0x0000007c, er0
0x03180E  add.l     sp, er0
0x031810  bsr       0x031b20
0x031814  sub.l     er0, er0
0x031816  mov.b     @er6, r0l
0x031818  shll.l    #2, er0
0x03181A  add.l     er5, er0
0x03181C  mov.l     er0, @(0x86,sp)
0x031822  mov.l     @(0x86,sp), er1
0x031828  mov.l     @er1, er1
0x03182C  mov.l     @(0x7c,sp), er2
0x031832  sub.l     er2, er1
0x031834  mov.l     er1, @er0
0x031838  sub.l     er1, er1
0x03183A  mov.b     @er6, r1l
0x03183C  shll.l    #2, er1
0x03183E  mov.l     @(0x7c,sp), er2
0x031844  mov.l     er2, @(0x400f42,er1)
0x03184E  sub.l     er1, er1
0x031850  mov.b     @er6, r1l
0x031852  shll.l    er1
0x031854  mov.w     @(0x400e5c,er1), r2
0x03185C  bne       0x031880
0x03185E  sub.l     er1, er1
0x031860  mov.b     @er6, r1l
0x031862  shll.l    er1
0x031864  mov.l     er1, @(0x86,sp)
0x03186A  mov.l     @(0x86,sp), er2
0x031870  mov.w     @(0x400f52,er2), r2
0x031878  mov.w     r2, @(0x400e5c,er1)
0x031880  mov.b     @0x006020, r0l
0x031886  bne       0x031920
0x03188A  mov.w     @0x400402, r0
0x031890  bne       0x031920
0x031894  sub.l     er0, er0
0x031896  mov.b     @er6, r0l
0x031898  shll.l    #2, er0
0x03189A  mov.l     er0, @(0x86,sp)
0x0318A0  add.l     er5, er0
0x0318A2  mov.l     #0x00000054, er1
0x0318A8  add.l     sp, er1
0x0318AA  mov.l     @(0x86,sp), er2
0x0318B0  add.l     er2, er1
0x0318B2  mov.l     @er1, er1
0x0318B6  mov.l     er0, @(0x2c,sp)
0x0318BC  mov.l     #0x0000000a, er0
0x0318C2  jsr       0x018e1e
0x0318C6  mov.l     #0x00000006, er1
0x0318CC  jsr       0x01872e
0x0318D0  mov.l     @(0x2c,sp), er1
0x0318D6  mov.l     @er1, er1
0x0318DA  cmp.l     er0, er1
0x0318DC  bls       0x031920
0x0318DE  mov.b     @er6, r0l
0x0318E0  extu.w    r0
0x0318E2  inc.w     #1, r0
0x0318E4  or.w      #0x08b0, r0
0x0318E8  mov.w     r0, @0x400402
0x0318EE  sub.l     er0, er0
0x0318F0  mov.b     @er6, r0l
0x0318F2  mov.l     er0, @(0x86,sp)
0x0318F8  mov.b     @(0x3fbe2,er0), r0l
0x031900  mov.b     @er3, r1l
0x031902  and.b     r0l, r1l
0x031904  mov.b     r1l, @er3
0x031906  mov.b     #0x01, r0l
0x031908  mov.b     r0l, @(0x9b,sp)
0x03190C  mov.l     #0x00000040, er0
0x031912  add.l     sp, er0
0x031914  mov.l     @(0x86,sp), er1
0x03191A  add.l     er1, er0
0x03191C  mov.b     #0x01, r1l
0x03191E  mov.b     r1l, @er0
0x031920  mov.b     @er6, r0l
0x031922  inc.b     #1, r0l
0x031924  mov.b     r0l, @er6
0x031926  cmp.b     #0x04, r0l
0x031928  bcs       0x031792
0x03192C  mov.w     @0x400406, r0
0x031932  and.w     #0x00ff, r0
0x031936  cmp.w     #0x0080, r0
0x03193A  bne       0x031940
0x03193C  bsr       0x031e02
0x031940  mov.b     @(0x97,sp), r0l
0x031944  extu.w    r0
0x031946  mov.w     #0x0022, e0
0x03194A  mulxu.w   e0, er0
0x03194C  mov.b     #0x02, r1l
0x03194E  mov.b     r1l, @(0x41ffd4,er0)
0x031956  bt        0x031976
0x031958  mov.b     @0x41ffa4, r0l
0x03195E  bne       0x031976
0x031960  mov.b     @(0x97,sp), r0l
0x031964  extu.w    r0
0x031966  mov.w     #0x0022, e0
0x03196A  mulxu.w   e0, er0
0x03196C  mov.b     #0x01, r1l
0x03196E  mov.b     r1l, @(0x41ffd4,er0)
0x031976  sub.b     r0l, r0l
0x031978  mov.b     r0l, @0x2001c1
0x03197E  mov.b     #0x80, r0l
0x031980  mov.b     r0l, @0x200001
0x031986  mov.b     @0x4206ec, r0l
0x03198C  bne       0x031ac6
0x031990  mov.w     @0x400406, r0
0x031996  and.w     #0x00ff, r0
0x03199A  cmp.w     #0x0080, r0
0x03199E  bne       0x031a90
0x0319A2  mov.l     @er5, er0
0x0319A6  mov.l     er0, @(0x80,sp)
0x0319AC  beq       0x0319c6
0x0319AE  mov.l     @(0x80,sp), er0
0x0319B4  mov.l     @(0x44,sp), er1
0x0319BA  cmp.l     er1, er0
0x0319BC  bhi       0x0319c6
0x0319BE  mov.b     @(0x40,sp), r0l
0x0319C2  cmp.b     #0x01, r0l
0x0319C4  bne       0x0319da
0x0319C6  mov.l     #0x0001d4c0, er0
0x0319CC  mov.l     er0, @er5
0x0319D0  sub.l     er0, er0
0x0319D2  mov.l     er0, @0x400f42
0x0319DA  mov.l     @(0x4,er5), er0
0x0319E0  mov.l     er0, @(0x80,sp)
0x0319E6  beq       0x031a00
0x0319E8  mov.l     @(0x80,sp), er0
0x0319EE  mov.l     @(0x48,sp), er1
0x0319F4  cmp.l     er1, er0
0x0319F6  bhi       0x031a00
0x0319F8  mov.b     @(0x41,sp), r0l
0x0319FC  cmp.b     #0x01, r0l
0x0319FE  bne       0x031a16
0x031A00  mov.l     #0x0001d4c0, er0
0x031A06  mov.l     er0, @(0x4,er5)
0x031A0C  sub.l     er0, er0
0x031A0E  mov.l     er0, @0x400f46
0x031A16  mov.l     @(0x8,er5), er0
0x031A1C  mov.l     er0, @(0x80,sp)
0x031A22  beq       0x031a3c
0x031A24  mov.l     @(0x80,sp), er0
0x031A2A  mov.l     @(0x4c,sp), er1
0x031A30  cmp.l     er1, er0
0x031A32  bhi       0x031a3c
0x031A34  mov.b     @(0x42,sp), r0l
0x031A38  cmp.b     #0x01, r0l
0x031A3A  bne       0x031a52
0x031A3C  mov.l     #0x0001d4c0, er0
0x031A42  mov.l     er0, @(0x8,er5)
0x031A48  sub.l     er0, er0
0x031A4A  mov.l     er0, @0x400f4a
0x031A52  mov.l     @(0xc,er5), er0
0x031A58  mov.l     er0, @(0x80,sp)
0x031A5E  beq       0x031a78
0x031A60  mov.l     @(0x80,sp), er0
0x031A66  mov.l     @(0x50,sp), er1
0x031A6C  cmp.l     er1, er0
0x031A6E  bhi       0x031a78
0x031A70  mov.b     @(0x43,sp), r0l
0x031A74  cmp.b     #0x01, r0l
0x031A76  bne       0x031ac6
0x031A78  mov.l     #0x0001d4c0, er0
0x031A7E  mov.l     er0, @(0xc,er5)
0x031A84  sub.l     er0, er0
0x031A86  mov.l     er0, @0x400f4e
0x031A8E  bt        0x031ac6
0x031A90  mov.b     @(0x9b,sp), r0l
0x031A94  cmp.b     #0x01, r0l
0x031A96  bne       0x031ac6
0x031A98  mov.l     @(0x64,sp), er0
0x031A9E  mov.l     er0, @er5
0x031AA2  mov.l     @(0x68,sp), er0
0x031AA8  mov.l     er0, @(0x4,er5)
0x031AAE  mov.l     @(0x6c,sp), er0
0x031AB4  mov.l     er0, @(0x8,er5)
0x031ABA  mov.l     @(0x70,sp), er0
0x031AC0  mov.l     er0, @(0xc,er5)
0x031AC6  sub.b     r0l, r0l
0x031AC8  mov.b     r0l, @er6
0x031ACA  mov.b     @(0x97,sp), r0l
0x031ACE  extu.w    r0
0x031AD0  mov.w     #0x0022, e0
0x031AD4  mulxu.w   e0, er0
0x031AD6  add.l     #0x0041ffb4, er0
0x031ADC  mov.l     er0, @(0x8a,sp)
0x031AE2  bt        0x031b02
0x031AE4  sub.l     er0, er0
0x031AE6  mov.b     @er6, r0l
0x031AE8  shll.l    #2, er0
0x031AEA  mov.l     @(0x8a,sp), er1
0x031AF0  add.l     er0, er1
0x031AF2  add.l     er5, er0
0x031AF4  mov.l     @er0, er0
0x031AF8  mov.l     er0, @er1
0x031AFC  mov.b     @er6, r0l
0x031AFE  inc.b     #1, r0l
0x031B00  mov.b     r0l, @er6
0x031B02  mov.b     @er6, r0l
0x031B04  cmp.b     #0x04, r0l
0x031B06  bcs       0x031ae4
0x031B08  sub.b     r0l, r0l
0x031B0A  mov.b     r0l, @0x420246
0x031B10  add.l     #0x0000009c, sp
0x031B16  ldm.l     @sp+, er4-er6
0x031B1A  ldm.l     @sp+, er2-er3
0x031B1E  rts       
