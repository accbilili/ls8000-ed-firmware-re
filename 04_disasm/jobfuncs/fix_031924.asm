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
