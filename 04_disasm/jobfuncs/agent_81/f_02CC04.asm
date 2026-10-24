0x015FFC  stm.l     er4-er6, @-sp
0x016000  mov.l     #0x004003f6, er5
0x016006  mov.l     er0, er4
0x016008  mov.l     @er5, er6
0x01600C  bt        0x016012
0x01600E  jsr       0x010b56
0x016012  mov.l     @er5, er0
0x016016  sub.l     er6, er0
0x016018  cmp.l     er4, er0
0x01601A  bcs       0x01600e
0x01601C  ldm.l     @sp+, er4-er6
0x016020  rts       
0x018708  mov.w     r2, @-sp
0x01870A  mov.w     e0, r2
0x01870C  mov.b     r2h, r2l
0x01870E  bpl       0x018712
0x018710  neg.l     er0
0x018712  mov.w     e1, e1
0x018714  bpl       0x01871a
0x018716  xor.b     #0x80, r2h
0x018718  neg.l     er1
0x01871A  jsr       0x01872e
0x01871E  mov.b     r2h, r2h
0x018720  bpl       0x018724
0x018722  neg.l     er0
0x018724  mov.b     r2l, r2l
0x018726  bpl       0x01872a
0x018728  neg.l     er1
0x01872A  mov.w     @sp+, r2
0x01872C  rts       
0x029D2A  stm.l     er4-er6, @-sp
0x029D2E  mov.l     #0x00420301, er6
0x029D34  mov.b     r0l, r4l
0x029D36  sub.b     r0l, r0l
0x029D38  mov.b     r0l, @er6
0x029D3A  mov.l     #0x00ffff2f, er0
0x029D40  mov.b     @er0, r1l
0x029D42  and.b     #0xbe, r1l
0x029D44  mov.b     r1l, @er0
0x029D46  mov.b     @0x400d72, r0l
0x029D4C  cmp.b     #0x05, r0l
0x029D4E  bne       0x029d68
0x029D50  jsr       0x02cfa0
0x029D54  cmp.b     #0x01, r0l
0x029D56  beq       0x029d68
0x029D58  jsr       0x02cf60
0x029D5C  cmp.b     #0x01, r0l
0x029D5E  beq       0x029d68
0x029D60  jsr       0x02cfe0
0x029D64  cmp.b     #0x01, r0l
0x029D66  bne       0x029d6c
0x029D68  bset      #6, @er6
0x029D6C  mov.l     #0x004202ff, er5
0x029D72  sub.b     r0l, r0l
0x029D74  mov.b     r0l, @er5
0x029D76  mov.b     r4l, r4l
0x029D78  beq       0x029db4
0x029D7A  jsr       0x02cfa0
0x029D7E  cmp.b     #0x01, r0l
0x029D80  bne       0x029dac
0x029D82  mov.w     @0x4202ec, r0
0x029D88  mov.w     #0x000c, e0
0x029D8C  mulxu.w   e0, er0
0x029D8E  mov.w     @0x4202a2, r1
0x029D94  add.w     r0, r1
0x029D96  sub.l     er0, er0
0x029D98  mov.b     @0x4003fb, r0l
0x029D9E  shll.l    er0
0x029DA0  mov.w     @(0x3ee10,er0), r0
0x029DA8  cmp.w     r0, r1
0x029DAA  bcs       0x029db4
0x029DAC  mov.b     #0x01, r0l
0x029DAE  mov.b     r0l, @er5
0x029DB0  bset      #0, @er6
0x029DB4  ldm.l     @sp+, er4-er6
0x029DB8  rts       
0x02BF00  stm.l     er4-er6, @-sp
0x02BF04  mov.b     r0l, r6l
0x02BF06  mov.w     e0, e6
0x02BF08  mov.w     r1, r4
0x02BF0A  mov.l     @(0x10,sp), er5
0x02BF10  mov.b     r0h, r6h
0x02BF12  cmp.b     #0x01, r6l
0x02BF14  bne       0x02bf1c
0x02BF16  mov.b     #0x01, r0l
0x02BF18  jsr       0x029d2a
0x02BF1C  mov.b     #0x01, r0l
0x02BF1E  mov.b     r0l, @0x4202ee
0x02BF24  mov.l     er5, er5
0x02BF26  beq       0x02bf2e
0x02BF28  mov.l     er5, er0
0x02BF2A  bsr       0x02c0e2
0x02BF2E  sub.w     r0, r0
0x02BF30  mov.w     r0, @0x440fce
0x02BF36  mov.w     r4, @0x4202ea
0x02BF3C  mov.b     #0x04, r0l
0x02BF3E  mov.b     r0l, @0x440e64
0x02BF44  sub.w     r0, r0
0x02BF46  mov.w     r0, @0x440fd0
0x02BF4C  mov.w     r0, @0x440fd8
0x02BF52  mov.w     e6, @0x440fd4
0x02BF58  mov.w     e6, @0x440fd6
0x02BF5E  sub.w     r0, r0
0x02BF60  mov.w     r0, @0x440fd2
0x02BF66  mov.b     r6l, @0x440e63
0x02BF6C  mov.b     r6h, @0x4202f3
0x02BF72  mov.l     @(0x14,sp), er0
0x02BF78  mov.l     er0, @0x4202f4
0x02BF80  mov.b     r6l, r0l
0x02BF82  bsr       0x02c172
0x02BF86  bsr       0x02bfa8
0x02BF88  mov.l     er5, er5
0x02BF8A  bne       0x02bf9a
0x02BF8C  mov.b     #0x03, r0l
0x02BF8E  mov.b     r0l, @0x4202ee
0x02BF94  bsr       0x02c376
0x02BF98  bt        0x02bfa2
0x02BF9A  bset      #0, @0xfffe84
0x02BFA2  ldm.l     @sp+, er4-er6
0x02BFA6  rts       
0x02BFA8  stm.l     er4-er6, @-sp
0x02BFAC  mov.l     #0x00440fb2, er4
0x02BFB2  mov.l     #0x00440e7e, er5
0x02BFB8  mov.l     #0x00440fce, er6
0x02BFBE  mov.l     #0x00ffff48, er0
0x02BFC4  mov.w     @er0, r1
0x02BFC6  or.w      #0x0f00, r1
0x02BFCA  mov.w     r1, @er0
0x02BFCC  mov.b     @0x440e76, r0l
0x02BFD2  bsr       0x02ce74
0x02BFD6  bclr      #2, @0xffffc0
0x02BFDE  mov.b     #0x42, r0l
0x02BFE0  mov.b     r0l, @0xfffff0
0x02BFE6  mov.b     @0xfffff5, r0l
0x02BFEC  mov.b     r0l, @0x40041b
0x02BFF2  bclr      #0, @0xfffff5
0x02BFFA  mov.l     #0x00fffff4, er0
0x02C000  mov.b     @er0, r1l
0x02C002  and.b     #0x4c, r1l
0x02C004  mov.b     r1l, @er0
0x02C006  bset      #0, @0xfffff4
0x02C00E  mov.w     @er6, r0
0x02C010  beq       0x02c034
0x02C012  mov.w     @er5, r0
0x02C014  mov.w     r0, @0xfffffa
0x02C01A  mov.w     @er6, r0
0x02C01C  extu.l    er0
0x02C01E  shll.l    er0
0x02C020  add.l     er5, er0
0x02C022  mov.w     @er0, r1
0x02C024  extu.l    er1
0x02C026  mov.w     #0x0064, r0
0x02C02A  divxu.w   r0, er1
0x02C02C  mov.w     r1, @0xfffff8
0x02C032  bt        0x02c04c
0x02C034  mov.w     @er4, r0
0x02C036  mov.w     r0, @0xfffffa
0x02C03C  mov.w     @er4, r0
0x02C03E  extu.l    er0
0x02C040  mov.w     #0x012c, r1
0x02C044  divxu.w   r1, er0
0x02C046  mov.w     r0, @0xfffff8
0x02C04C  mov.b     @0xffff07, r0l
0x02C052  mov.b     r0l, @0x40041b
0x02C058  mov.w     @0xffff06, r0
0x02C05E  and.w     #0xaccc, r0
0x02C062  or.w      #0x0332, r0
0x02C066  mov.w     r0, @0xffff06
0x02C06C  mov.b     #0x2a, r0l
0x02C06E  mov.b     r0l, @0xffff02
0x02C074  mov.b     @0x440e64, r0l
0x02C07A  mov.b     r0l, @0xfffee7
0x02C080  mov.b     r0l, @0xfffee6
0x02C086  mov.l     #0x00440e65, er0
0x02C08C  mov.l     er0, @0xfffee0
0x02C094  mov.w     #0xff4e, r0
0x02C098  mov.w     r0, @0xfffee4
0x02C09E  mov.b     #0x8a, r0l
0x02C0A0  mov.b     r0l, @0xffff03
0x02C0A6  mov.b     @0x440e64, r0l
0x02C0AC  extu.w    r0
0x02C0AE  shlr.w    #2, r0
0x02C0B0  mov.w     r0, @0xfffeee
0x02C0B6  mov.w     @er6, r0
0x02C0B8  beq       0x02c0be
0x02C0BA  mov.l     er5, er0
0x02C0BC  bt        0x02c0c0
0x02C0BE  mov.l     er4, er0
0x02C0C0  inc.l     #2, er0
0x02C0C2  mov.l     er0, @0xfffee8
0x02C0CA  mov.w     #0xfffa, r0
0x02C0CE  mov.w     r0, @0xfffeec
0x02C0D4  mov.b     #0x03, r0l
0x02C0D6  mov.b     r0l, @0x4003ff
0x02C0DC  ldm.l     @sp+, er4-er6
0x02C0E0  rts       
0x02C0E2  stm.l     er4-er5, @-sp
0x02C0E6  mov.l     #0x00440e7c, er4
0x02C0EC  mov.l     er0, er5
0x02C0EE  mov.b     #0x22, r0l
0x02C0F0  mov.b     r0l, @0xfffe80
0x02C0F6  mov.b     @0xfffe85, r0l
0x02C0FC  mov.b     r0l, @0x40041b
0x02C102  bclr      #0, @0xfffe85
0x02C10A  sub.w     r0, r0
0x02C10C  mov.w     r0, @0xfffe86
0x02C112  mov.l     #0x00fffe84, er0
0x02C118  mov.b     @er0, r1l
0x02C11A  and.b     #0x60, r1l
0x02C11C  mov.b     r1l, @er0
0x02C11E  mov.b     #0x03, r0l
0x02C120  mov.b     r0l, @0x4003fe
0x02C126  mov.l     er5, er0
0x02C128  mov.l     #0x000003e8, er1
0x02C12E  jsr       0x018e1e
0x02C132  mov.l     #0x00000280, er1
0x02C138  jsr       0x01872e
0x02C13C  mov.l     er0, er5
0x02C13E  mov.b     #0x01, r0l
0x02C140  mov.b     r0l, @er4
0x02C142  cmp.l     #0x0000ffff, er5
0x02C148  bls       0x02c156
0x02C14A  shlr.l    er5
0x02C14C  mov.b     @er4, r0l
0x02C14E  mov.b     @er4, r1l
0x02C150  add.b     r0l, r1l
0x02C152  mov.b     r1l, @er4
0x02C154  bt        0x02c142
0x02C156  mov.b     @er4, r0l
0x02C158  mov.b     r0l, @0x440e7d
0x02C15E  mov.w     r5, @0xfffe88
0x02C164  bset      #3, @0xffffc0
0x02C16C  ldm.l     @sp+, er4-er5
0x02C170  rts       
0x02C172  mov.w     r6, @-sp
0x02C174  mov.b     r0l, r6l
0x02C176  bsr       0x02c180
0x02C178  bsr       0x02c27a
0x02C17C  mov.w     @sp+, r6
0x02C17E  rts       
0x02C180  stm.l     er2-er3, @-sp
0x02C184  stm.l     er4-er6, @-sp
0x02C188  sub.l     #0x0000000a, sp
0x02C18E  mov.b     r0l, r2l
0x02C190  mov.l     #0x0003f100, er4
0x02C196  mov.l     er4, er6
0x02C198  mov.b     @0x440e64, r1l
0x02C19E  extu.w    r1
0x02C1A0  dec.w     #1, r1
0x02C1A2  mov.w     r1, r5
0x02C1A4  sub.w     e1, e1
0x02C1A6  bt        0x02c1b8
0x02C1A8  mov.b     @er6, r0l
0x02C1AA  mov.b     @0x440e76, r1l
0x02C1B0  cmp.b     r1l, r0l
0x02C1B2  beq       0x02c1bc
0x02C1B4  inc.l     #1, er6
0x02C1B6  inc.w     #1, e1
0x02C1B8  cmp.w     r5, e1
0x02C1BA  ble       0x02c1a8
0x02C1BC  mov.l     #0x00000002, er3
0x02C1C2  mov.b     r2l, r0l
0x02C1C4  bne       0x02c1e8
0x02C1C6  mov.l     er6, er0
0x02C1C8  add.l     er3, er0
0x02C1CA  mov.w     r5, r1
0x02C1CC  exts.l    er1
0x02C1CE  add.l     er4, er1
0x02C1D0  cmp.l     er1, er0
0x02C1D2  bls       0x02c1e4
0x02C1D4  add.l     er6, er3
0x02C1D6  sub.l     er0, er0
0x02C1D8  mov.b     @0x440e64, r0l
0x02C1DE  sub.l     er0, er3
0x02C1E0  mov.l     er3, er6
0x02C1E2  bt        0x02c204
0x02C1E4  add.l     er3, er6
0x02C1E6  bt        0x02c204
0x02C1E8  mov.l     er6, er0
0x02C1EA  sub.l     er3, er0
0x02C1EC  cmp.l     er4, er0
0x02C1EE  bcc       0x02c202
0x02C1F0  mov.l     er6, er0
0x02C1F2  sub.l     er3, er0
0x02C1F4  sub.l     er1, er1
0x02C1F6  mov.b     @0x440e64, r1l
0x02C1FC  add.l     er1, er0
0x02C1FE  mov.l     er0, er6
0x02C200  bt        0x02c204
0x02C202  sub.l     er3, er6
0x02C204  mov.l     #0x00440e65, er0
0x02C20A  mov.l     er0, @(0x6,sp)
0x02C210  mov.b     r2l, r0l
0x02C212  bne       0x02c21a
0x02C214  mov.w     #0x0001, r3
0x02C218  bt        0x02c21e
0x02C21A  mov.w     #0xffff, r3
0x02C21E  sub.w     e1, e1
0x02C220  mov.w     r5, r0
0x02C222  exts.l    er0
0x02C224  add.l     er4, er0
0x02C226  mov.l     er0, er2
0x02C228  bt        0x02c254
0x02C22A  mov.l     @(0x6,sp), er0
0x02C230  inc.l     #1, er0
0x02C232  mov.l     er0, @(0x6,sp)
0x02C238  dec.l     #1, er0
0x02C23A  mov.b     @er6, r1l
0x02C23C  mov.b     r1l, @er0
0x02C23E  mov.w     r3, r0
0x02C240  exts.l    er0
0x02C242  add.l     er0, er6
0x02C244  mov.l     er2, er0
0x02C246  cmp.l     er0, er6
0x02C248  bls       0x02c24c
0x02C24A  mov.l     er4, er6
0x02C24C  cmp.l     er4, er6
0x02C24E  bcc       0x02c252
0x02C250  mov.l     er2, er6
0x02C252  inc.w     #1, e1
0x02C254  cmp.w     r5, e1
0x02C256  ble       0x02c22a
0x02C258  mov.w     r5, r0
0x02C25A  exts.l    er0
0x02C25C  add.l     #0x00440e64, er0
0x02C262  mov.l     er0, @0x440e78
0x02C26A  add.l     #0x0000000a, sp
0x02C270  ldm.l     @sp+, er4-er6
0x02C274  ldm.l     @sp+, er2-er3
0x02C278  rts       
0x02C27A  mov.l     er3, @-sp
0x02C27E  stm.l     er4-er6, @-sp
0x02C282  mov.l     #0x004202ea, er3
0x02C288  mov.l     #0x00440e7e, er4
0x02C28E  mov.l     #0x00440fce, er6
0x02C294  mov.w     @er6, r0
0x02C296  beq       0x02c33c
0x02C29A  sub.w     r5, r5
0x02C29C  bt        0x02c2f8
0x02C29E  mov.w     #0x5a00, r0
0x02C2A2  mov.w     r0, @0xffffbc
0x02C2A8  mov.w     @er3, r1
0x02C2AA  extu.l    er1
0x02C2AC  mov.l     #0x3b9aca00, er0
0x02C2B2  jsr       0x018708
0x02C2B6  mov.l     #0x002625a0, er1
0x02C2BC  sub.l     er0, er1
0x02C2BE  mov.w     r5, r0
0x02C2C0  exts.l    er0
0x02C2C2  jsr       0x018e1e
0x02C2C6  mov.w     @er6, r1
0x02C2C8  extu.l    er1
0x02C2CA  jsr       0x018708
0x02C2CE  mov.l     #0x002625a0, er1
0x02C2D4  sub.l     er0, er1
0x02C2D6  mov.l     er1, er0
0x02C2D8  mov.l     #0x00000280, er1
0x02C2DE  jsr       0x018708
0x02C2E2  mov.w     r5, r1
0x02C2E4  exts.l    er1
0x02C2E6  shll.l    er1
0x02C2E8  add.l     er4, er1
0x02C2EA  mov.w     r0, @er1
0x02C2EC  mov.w     #0x5a00, r0
0x02C2F0  mov.w     r0, @0xffffbc
0x02C2F6  inc.w     #1, r5
0x02C2F8  mov.w     @er6, r0
0x02C2FA  inc.w     #1, r0
0x02C2FC  cmp.w     r0, r5
0x02C2FE  bcs       0x02c29e
0x02C300  mov.w     @er6, r5
0x02C302  extu.l    er5
0x02C304  shll.l    er5
0x02C306  add.l     er4, er5
0x02C308  mov.w     @er5, r0
0x02C30A  mov.w     r0, @(0x2,er5)
0x02C30E  mov.w     @er6, r5
0x02C310  extu.l    er5
0x02C312  shll.l    er5
0x02C314  add.l     er4, er5
0x02C316  mov.w     @er5, r0
0x02C318  mov.w     r0, @(0x4,er5)
0x02C31C  mov.w     @er6, r5
0x02C31E  extu.l    er5
0x02C320  shll.l    er5
0x02C322  add.l     er4, er5
0x02C324  mov.w     @er5, r0
0x02C326  mov.w     r0, @(0x6,er5)
0x02C32A  mov.w     @er6, r0
0x02C32C  extu.l    er0
0x02C32E  shll.l    er0
0x02C330  add.l     er4, er0
0x02C332  adds.l    #4, er0
0x02C334  adds.l    #4, er0
0x02C336  mov.w     #0xffff, r1
0x02C33A  mov.w     r1, @er0
0x02C33C  sub.w     r5, r5
0x02C33E  mov.w     @er3, r1
0x02C340  extu.l    er1
0x02C342  mov.l     #0x3b9aca00, er0
0x02C348  jsr       0x018708
0x02C34C  mov.l     #0x00000280, er1
0x02C352  jsr       0x018708
0x02C356  mov.w     r5, r1
0x02C358  exts.l    er1
0x02C35A  shll.l    er1
0x02C35C  mov.w     r0, @(0x440fb2,er1)
0x02C364  inc.w     #1, r5
0x02C366  cmp.w     #0x0005, r5
0x02C36A  blt       0x02c33e
0x02C36C  ldm.l     @sp+, er4-er6
0x02C370  mov.l     @sp+, er3
0x02C374  rts       
0x02C376  mov.b     @0xffff46, r0l
0x02C37C  and.b     #0xcf, r0l
0x02C37E  or.b      #0x20, r0l
0x02C380  mov.b     r0l, @0xffff46
0x02C386  mov.b     @0xffff47, r0l
0x02C38C  and.b     #0xbb, r0l
0x02C38E  or.b      #0x48, r0l
0x02C390  mov.b     r0l, @0xffff47
0x02C396  mov.l     @0x440e78, er0
0x02C39E  mov.b     @(0x1,er0), r0l
0x02C3A2  mov.b     r0l, @0xffff4e
0x02C3A8  mov.b     @0xfffff5, r0l
0x02C3AE  mov.b     r0l, @0x40041b
0x02C3B4  bclr      #0, @0xfffff5
0x02C3BC  sub.w     r0, r0
0x02C3BE  mov.w     r0, @0xfffff6
0x02C3C4  bset      #2, @0xffffc0
0x02C3CC  mov.b     @0x440e63, r0l
0x02C3D2  cmp.b     #0x01, r0l
0x02C3D4  bne       0x02c3ee
0x02C3D6  mov.b     @0xffff2e, r0l
0x02C3DC  and.b     #0xbe, r0l
0x02C3DE  mov.b     @0x420301, r1l
0x02C3E4  and.b     #0x41, r1l
0x02C3E6  or.b      r1l, r0l
0x02C3E8  mov.b     r0l, @0xffff2e
0x02C3EE  rts       
0x02C8E0  mov.w     r6, @-sp
0x02C8E2  mov.b     @0x4202f3, r0l
0x02C8E8  bne       0x02c8ee
0x02C8EA  sub.b     r6l, r6l
0x02C8EC  bt        0x02c8f6
0x02C8EE  mov.b     #0x07, r6l
0x02C8F0  bt        0x02c8f6
0x02C8F2  jsr       0x010b56
0x02C8F6  mov.b     @0x4202ee, r0l
0x02C8FC  cmp.b     r6l, r0l
0x02C8FE  bne       0x02c8f2
0x02C900  mov.w     @sp+, r6
0x02C902  rts       
0x02CBB0  mov.b     @0x4202ee, r0l
0x02CBB6  beq       0x02cbbe
0x02CBB8  jsr       0x010b56
0x02CBBC  bt        0x02cbb0
0x02CBBE  mov.b     @0x440e62, r0l
0x02CBC4  beq       0x02cbd0
0x02CBC6  mov.w     #0x0110, r0
0x02CBCA  mov.w     r0, @0x400402
0x02CBD0  sub.b     r0l, r0l
0x02CBD2  mov.b     r0l, @0x440e62
0x02CBD8  rts       
0x02CC04  mov.w     r3, @-sp
0x02CC06  stm.l     er4-er6, @-sp
0x02CC0A  mov.w     #0x0190, r3
0x02CC0E  mov.l     #0x004202ec, er4
0x02CC14  mov.l     #0x00400402, er5
0x02CC1A  mov.l     #0x00440e62, er6
0x02CC20  sub.w     r0, r0
0x02CC22  mov.w     r0, @er5
0x02CC24  jsr       0x02cf60
0x02CC28  cmp.b     #0x01, r0l
0x02CC2A  bne       0x02cc74
0x02CC2C  sub.b     r0l, r0l
0x02CC2E  mov.b     r0l, @0x4202f2
0x02CC34  mov.b     #0x01, r0l
0x02CC36  mov.b     r0l, @er6
0x02CC38  mov.l     #0x000186a0, er0
0x02CC3E  mov.l     er0, @-sp
0x02CC42  sub.l     er0, er0
0x02CC44  mov.l     er0, @-sp
0x02CC48  sub.b     r0h, r0h
0x02CC4A  mov.w     r3, r1
0x02CC4C  mov.w     #0x0f0a, e0
0x02CC50  mov.b     #0x01, r0l
0x02CC52  bsr       0x02bf00
0x02CC56  adds.l    #4, sp
0x02CC58  adds.l    #4, sp
0x02CC5A  bsr       0x02c8e0
0x02CC5E  mov.b     @er6, r0l
0x02CC60  beq       0x02cc74
0x02CC62  mov.w     #0x0110, r0
0x02CC66  mov.w     r0, @er5
0x02CC68  mov.w     #0x0056, r0
0x02CC6C  mov.w     r0, @er4
0x02CC6E  sub.b     r0l, r0l
0x02CC70  mov.b     r0l, @er6
0x02CC72  bt        0x02ccac
0x02CC74  mov.b     #0x02, r0l
0x02CC76  mov.b     r0l, @er6
0x02CC78  mov.l     #0x000186a0, er0
0x02CC7E  mov.l     er0, @-sp
0x02CC82  sub.l     er0, er0
0x02CC84  mov.l     er0, @-sp
0x02CC88  sub.b     r0h, r0h
0x02CC8A  mov.w     r3, r1
0x02CC8C  mov.w     #0x03cb, e0
0x02CC90  sub.b     r0l, r0l
0x02CC92  bsr       0x02bf00
0x02CC96  adds.l    #4, sp
0x02CC98  adds.l    #4, sp
0x02CC9A  bsr       0x02cbb0
0x02CC9E  mov.w     @er5, r0
0x02CCA0  cmp.w     #0x0110, r0
0x02CCA4  bne       0x02ccb0
0x02CCA6  mov.w     #0x03cb, r0
0x02CCAA  mov.w     r0, @er4
0x02CCAC  sub.b     r0l, r0l
0x02CCAE  bt        0x02ccf4
0x02CCB0  mov.w     #0x00ab, r0
0x02CCB4  mov.w     r0, @er4
0x02CCB6  sub.b     r0l, r0l
0x02CCB8  mov.b     r0l, @er6
0x02CCBA  mov.b     r0l, @0x4202f2
0x02CCC0  mov.l     #0x000186a0, er0
0x02CCC6  mov.l     er0, @-sp
0x02CCCA  sub.l     er0, er0
0x02CCCC  mov.l     er0, @-sp
0x02CCD0  sub.b     r0h, r0h
0x02CCD2  mov.w     r3, r1
0x02CCD4  mov.w     #0x00fa, e0
0x02CCD8  sub.b     r0l, r0l
0x02CCDA  bsr       0x02bf00
0x02CCDE  adds.l    #4, sp
0x02CCE0  adds.l    #4, sp
0x02CCE2  bsr       0x02c8e0
0x02CCE6  mov.l     #0x0000012c, er0
0x02CCEC  jsr       0x015ffc
0x02CCF0  bsr       0x02cdae
0x02CCF4  ldm.l     @sp+, er4-er6
0x02CCF8  mov.w     @sp+, r3
0x02CCFA  rts       
0x02CDAE  mov.w     r6, @-sp
0x02CDB0  jsr       0x02cf60
0x02CDB4  cmp.b     #0x01, r0l
0x02CDB6  bne       0x02ce3c
0x02CDBA  sub.b     r0l, r0l
0x02CDBC  mov.b     r0l, @0x440e62
0x02CDC2  mov.w     #0x0190, r6
0x02CDC6  mov.l     #0x000186a0, er0
0x02CDCC  mov.l     er0, @-sp
0x02CDD0  sub.l     er0, er0
0x02CDD2  mov.l     er0, @-sp
0x02CDD6  sub.b     r0h, r0h
0x02CDD8  mov.w     r6, r1
0x02CDDA  mov.w     r6, e0
0x02CDDC  mov.b     #0x01, r0l
0x02CDDE  bsr       0x02bf00
0x02CDE2  adds.l    #4, sp
0x02CDE4  adds.l    #4, sp
0x02CDE6  bsr       0x02c8e0
0x02CDEA  mov.b     #0x02, r0l
0x02CDEC  mov.b     r0l, @0x440e62
0x02CDF2  mov.l     #0x000186a0, er0
0x02CDF8  mov.l     er0, @-sp
0x02CDFC  sub.l     er0, er0
0x02CDFE  mov.l     er0, @-sp
0x02CE02  sub.b     r0h, r0h
0x02CE04  mov.w     r6, r1
0x02CE06  mov.w     #0x00b4, e0
0x02CE0A  sub.b     r0l, r0l
0x02CE0C  bsr       0x02bf00
0x02CE10  adds.l    #4, sp
0x02CE12  adds.l    #4, sp
0x02CE14  bsr       0x02cbb0
0x02CE18  mov.w     @0x400402, r0
0x02CE1E  cmp.w     #0x0110, r0
0x02CE22  bne       0x02ce32
0x02CE24  mov.w     #0x00c9, r0
0x02CE28  mov.w     r0, @0x4202ec
0x02CE2E  sub.b     r0l, r0l
0x02CE30  bt        0x02ce3c
0x02CE32  mov.w     #0x00ab, r0
0x02CE36  mov.w     r0, @0x4202ec
0x02CE3C  mov.w     @sp+, r6
0x02CE3E  rts       
0x02CE74  stm.l     er4-er5, @-sp
0x02CE78  mov.l     #0x00ffffc0, er5
0x02CE7E  mov.l     #0x00fffff5, er4
0x02CE84  mov.b     r0l, r1h
0x02CE86  bclr      #2, @er5
0x02CE8A  sub.w     r0, r0
0x02CE8C  mov.w     r0, @0xfffff6
0x02CE92  mov.b     #0x20, r0l
0x02CE94  mov.b     r0l, @0xfffff0
0x02CE9A  bclr      #0, @er4
0x02CE9E  mov.l     #0x00fffff4, er0
0x02CEA4  mov.b     @er0, r1l
0x02CEA6  and.b     #0x4c, r1l
0x02CEA8  mov.b     r1l, @er0
0x02CEAA  mov.w     #0x0001, r0
0x02CEAE  mov.w     r0, @0xfffff8
0x02CEB4  mov.b     @0xffff46, r0l
0x02CEBA  and.b     #0xcf, r0l
0x02CEBC  or.b      #0x20, r0l
0x02CEBE  mov.b     r0l, @0xffff46
0x02CEC4  mov.b     @0xffff47, r0l
0x02CECA  and.b     #0xbb, r0l
0x02CECC  or.b      #0x40, r0l
0x02CECE  mov.b     r0l, @0xffff47
0x02CED4  mov.b     r1h, @0xffff4e
0x02CEDA  bset      #2, @er5
0x02CEDE  btst      #0, @er4
0x02CEE2  beq       0x02cede
0x02CEE4  bclr      #2, @er5
0x02CEE8  bclr      #0, @er4
0x02CEEC  ldm.l     @sp+, er4-er5
0x02CEF0  rts       
0x02CF60  sub.b     r1l, r1l
0x02CF62  sub.w     r0, r0
0x02CF64  bt        0x02cf76
0x02CF66  btst      #2, @0xffff55
0x02CF6E  bne       0x02cf74
0x02CF70  mov.b     #0x01, r1l
0x02CF72  bt        0x02cf7c
0x02CF74  inc.w     #1, r0
0x02CF76  cmp.w     #0x0014, r0
0x02CF7A  blt       0x02cf66
0x02CF7C  mov.b     r1l, r0l
0x02CF7E  rts       
0x02CFA0  sub.b     r1l, r1l
0x02CFA2  sub.w     r0, r0
0x02CFA4  bt        0x02cfb6
0x02CFA6  btst      #5, @0xffff55
0x02CFAE  bne       0x02cfb4
0x02CFB0  mov.b     #0x01, r1l
0x02CFB2  bt        0x02cfbc
0x02CFB4  inc.w     #1, r0
0x02CFB6  cmp.w     #0x0014, r0
0x02CFBA  blt       0x02cfa6
0x02CFBC  mov.b     r1l, r0l
0x02CFBE  rts       
0x02CFE0  sub.b     r1l, r1l
0x02CFE2  sub.w     r0, r0
0x02CFE4  bt        0x02cff6
0x02CFE6  btst      #4, @0xffff55
0x02CFEE  bne       0x02cff4
0x02CFF0  mov.b     #0x01, r1l
0x02CFF2  bt        0x02cffc
0x02CFF4  inc.w     #1, r0
0x02CFF6  cmp.w     #0x0014, r0
0x02CFFA  blt       0x02cfe6
0x02CFFC  mov.b     r1l, r0l
0x02CFFE  rts       
