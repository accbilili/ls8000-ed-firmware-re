0x02DC4A  stm.l     er2-er3, @-sp
0x02DC4E  stm.l     er4-er6, @-sp
0x02DC52  subs.l    #4, sp
0x02DC54  subs.l    #2, sp
0x02DC56  mov.l     #0x00000020, er4
0x02DC5C  mov.l     #0x00ffffbc, er5
0x02DC62  mov.b     r0l, r2h
0x02DC64  extu.w    r0
0x02DC66  extu.l    er0
0x02DC68  mov.b     @(0x400eb5,er0), r0l
0x02DC70  cmp.b     #0x08, r0l
0x02DC72  bne       0x02dc78
0x02DC74  mov.b     #0x06, r2l
0x02DC76  bt        0x02dc7c
0x02DC78  sub.b     r0l, r0l
0x02DC7A  mov.b     r0l, r2l
0x02DC7C  mov.w     #0x5a00, r0
0x02DC80  mov.w     r0, @er5
0x02DC82  mov.b     @0x400eb9, r0l
0x02DC88  cmp.b     #0x01, r0l
0x02DC8A  bne       0x02dde8
0x02DC8E  sub.l     er6, er6
0x02DC90  mov.b     r2h, r6l
0x02DC92  mov.b     #0x0f, r0l
0x02DC94  shll.l    er6
0x02DC96  dec.b     #1, r0l
0x02DC98  bgt       0x02dc94
0x02DC9A  add.l     #0x00800000, er6
0x02DCA0  mov.b     r2l, r0l
0x02DCA2  cmp.b     #0x06, r0l
0x02DCA4  bne       0x02dd78
0x02DCA8  sub.l     er3, er3
0x02DCAA  mov.l     er6, er0
0x02DCAC  inc.l     #2, er6
0x02DCAE  mov.l     er3, er1
0x02DCB0  add.l     er4, er1
0x02DCB2  shlr.l    #2, er1
0x02DCB4  shlr.l    #2, er1
0x02DCB6  shlr.l    #2, er1
0x02DCB8  mov.w     r1, @er0
0x02DCBA  inc.l     #1, er3
0x02DCBC  cmp.l     #0x00001000, er3
0x02DCC2  bcs       0x02dcaa
0x02DCC4  mov.w     #0x5a00, r0
0x02DCC8  mov.w     r0, @er5
0x02DCCA  jsr       0x010b56
0x02DCCE  mov.l     #0x00001000, er3
0x02DCD4  mov.l     er6, er0
0x02DCD6  inc.l     #2, er6
0x02DCD8  mov.l     er3, er1
0x02DCDA  add.l     er4, er1
0x02DCDC  shlr.l    #2, er1
0x02DCDE  shlr.l    #2, er1
0x02DCE0  shlr.l    #2, er1
0x02DCE2  mov.w     r1, @er0
0x02DCE4  inc.l     #1, er3
0x02DCE6  cmp.l     #0x00002000, er3
0x02DCEC  bcs       0x02dcd4
0x02DCEE  mov.w     #0x5a00, r0
0x02DCF2  mov.w     r0, @er5
0x02DCF4  jsr       0x010b56
0x02DCF8  mov.l     #0x00002000, er3
0x02DCFE  mov.l     er6, er0
0x02DD00  inc.l     #2, er6
0x02DD02  mov.l     er3, er1
0x02DD04  add.l     er4, er1
0x02DD06  shlr.l    #2, er1
0x02DD08  shlr.l    #2, er1
0x02DD0A  shlr.l    #2, er1
0x02DD0C  mov.w     r1, @er0
0x02DD0E  inc.l     #1, er3
0x02DD10  cmp.l     #0x00003000, er3
0x02DD16  bcs       0x02dcfe
0x02DD18  mov.w     #0x5a00, r0
0x02DD1C  mov.w     r0, @er5
0x02DD1E  jsr       0x010b56
0x02DD22  mov.l     #0x00003000, er3
0x02DD28  mov.l     er6, er0
0x02DD2A  inc.l     #2, er6
0x02DD2C  mov.l     er3, er1
0x02DD2E  add.l     er4, er1
0x02DD30  shlr.l    #2, er1
0x02DD32  shlr.l    #2, er1
0x02DD34  shlr.l    #2, er1
0x02DD36  mov.w     r1, @er0
0x02DD38  inc.l     #1, er3
0x02DD3A  cmp.l     #0x00003fc1, er3
0x02DD40  bcs       0x02dd28
0x02DD42  mov.w     #0x5a00, r0
0x02DD46  mov.w     r0, @er5
0x02DD48  jsr       0x010b56
0x02DD4C  mov.l     #0x00003fc1, er3
0x02DD52  mov.l     er6, er0
0x02DD54  inc.l     #2, er6
0x02DD56  mov.l     er3, er1
0x02DD58  shlr.l    #2, er1
0x02DD5A  shlr.l    #2, er1
0x02DD5C  shlr.l    #2, er1
0x02DD5E  mov.w     r1, @er0
0x02DD60  inc.l     #1, er3
0x02DD62  cmp.l     #0x00004000, er3
0x02DD68  bcs       0x02dd52
0x02DD6A  mov.w     #0x5a00, r0
0x02DD6E  mov.w     r0, @er5
0x02DD70  jsr       0x010b56
0x02DD74  jmp       0x02e126
0x02DD78  sub.l     er3, er3
0x02DD7A  mov.l     er6, er0
0x02DD7C  inc.l     #2, er6
0x02DD7E  mov.w     r3, @er0
0x02DD80  inc.l     #1, er3
0x02DD82  cmp.l     #0x00001000, er3
0x02DD88  bcs       0x02dd7a
0x02DD8A  mov.w     #0x5a00, r0
0x02DD8E  mov.w     r0, @er5
0x02DD90  mov.l     #0x00001000, er3
0x02DD96  mov.l     er6, er0
0x02DD98  inc.l     #2, er6
0x02DD9A  mov.w     r3, @er0
0x02DD9C  inc.l     #1, er3
0x02DD9E  cmp.l     #0x00002000, er3
0x02DDA4  bcs       0x02dd96
0x02DDA6  mov.w     #0x5a00, r0
0x02DDAA  mov.w     r0, @er5
0x02DDAC  mov.l     #0x00002000, er3
0x02DDB2  mov.l     er6, er0
0x02DDB4  inc.l     #2, er6
0x02DDB6  mov.w     r3, @er0
0x02DDB8  inc.l     #1, er3
0x02DDBA  cmp.l     #0x00003000, er3
0x02DDC0  bcs       0x02ddb2
0x02DDC2  mov.w     #0x5a00, r0
0x02DDC6  mov.w     r0, @er5
0x02DDC8  mov.l     #0x00003000, er3
0x02DDCE  mov.l     er6, er0
0x02DDD0  inc.l     #2, er6
0x02DDD2  mov.w     r3, @er0
0x02DDD4  inc.l     #1, er3
0x02DDD6  cmp.l     #0x00004000, er3
0x02DDDC  bcs       0x02ddce
0x02DDDE  mov.w     #0x5a00, r0
0x02DDE2  mov.w     r0, @er5
0x02DDE4  jmp       0x02e126
0x02DDE8  mov.b     r2h, r0l
0x02DDEA  cmp.b     #0x03, r0l
0x02DDEC  beq       0x02dfd2
0x02DDF0  mov.w     #0x5a00, r0
0x02DDF4  mov.w     r0, @er5
0x02DDF6  sub.l     er3, er3
0x02DDF8  mov.b     r2h, r3l
0x02DDFA  mov.l     er3, er6
0x02DDFC  mov.b     #0x0f, r0l
0x02DDFE  shll.l    er6
0x02DE00  dec.b     #1, r0l
0x02DE02  bgt       0x02ddfe
0x02DE04  add.l     #0x00800000, er6
0x02DE0A  shll.l    #2, er3
0x02DE0C  mov.l     @(0x3f166,er3), er3
0x02DE16  mov.b     @er3+, r0l
0x02DE18  extu.w    r0
0x02DE1A  mov.b     r0l, r0h
0x02DE1C  sub.b     r0l, r0l
0x02DE1E  mov.b     @er3+, r1l
0x02DE20  extu.w    r1
0x02DE22  add.w     r1, r0
0x02DE24  mov.w     r0, @er6
0x02DE26  mov.l     #0x00000001, er0
0x02DE2C  mov.l     er0, @sp
0x02DE30  mov.w     @er6+, r0
0x02DE32  mov.b     @er3+, r1l
0x02DE34  extu.w    r1
0x02DE36  sub.w     r1, r0
0x02DE38  mov.w     r0, @er6
0x02DE3A  mov.l     @sp, er0
0x02DE3E  inc.l     #1, er0
0x02DE40  mov.l     er0, @sp
0x02DE44  cmp.l     #0x00001000, er0
0x02DE4A  bcs       0x02de30
0x02DE4C  mov.w     #0x5a00, r0
0x02DE50  mov.w     r0, @er5
0x02DE52  mov.l     #0x00001000, er0
0x02DE58  mov.l     er0, @sp
0x02DE5C  mov.w     @er6+, r0
0x02DE5E  mov.b     @er3+, r1l
0x02DE60  extu.w    r1
0x02DE62  sub.w     r1, r0
0x02DE64  mov.w     r0, @er6
0x02DE66  mov.l     @sp, er0
0x02DE6A  inc.l     #1, er0
0x02DE6C  mov.l     er0, @sp
0x02DE70  cmp.l     #0x00002000, er0
0x02DE76  bcs       0x02de5c
0x02DE78  mov.w     #0x5a00, r0
0x02DE7C  mov.w     r0, @er5
0x02DE7E  jsr       0x010b56
0x02DE82  mov.l     #0x00002000, er0
0x02DE88  mov.l     er0, @sp
0x02DE8C  mov.w     @er6+, r0
0x02DE8E  mov.b     @er3+, r1l
0x02DE90  extu.w    r1
0x02DE92  sub.w     r1, r0
0x02DE94  mov.w     r0, @er6
0x02DE96  mov.l     @sp, er0
0x02DE9A  inc.l     #1, er0
0x02DE9C  mov.l     er0, @sp
0x02DEA0  cmp.l     #0x00003000, er0
0x02DEA6  bcs       0x02de8c
0x02DEA8  mov.w     #0x5a00, r0
0x02DEAC  mov.w     r0, @er5
0x02DEAE  jsr       0x010b56
0x02DEB2  mov.l     #0x00003000, er0
0x02DEB8  mov.l     er0, @sp
0x02DEBC  mov.w     @er6+, r0
0x02DEBE  mov.b     @er3+, r1l
0x02DEC0  extu.w    r1
0x02DEC2  sub.w     r1, r0
0x02DEC4  mov.w     r0, @er6
0x02DEC6  mov.l     @sp, er0
0x02DECA  inc.l     #1, er0
0x02DECC  mov.l     er0, @sp
0x02DED0  cmp.l     #0x00004000, er0
0x02DED6  bcs       0x02debc
0x02DED8  mov.w     #0x5a00, r0
0x02DEDC  mov.w     r0, @er5
0x02DEDE  jsr       0x010b56
0x02DEE2  mov.b     r2l, r0l
0x02DEE4  beq       0x02e120
0x02DEE8  sub.l     er6, er6
0x02DEEA  mov.b     r2h, r6l
0x02DEEC  mov.b     #0x0f, r0l
0x02DEEE  shll.l    er6
0x02DEF0  dec.b     #1, r0l
0x02DEF2  bgt       0x02deee
0x02DEF4  add.l     #0x00800000, er6
0x02DEFA  sub.l     er3, er3
0x02DEFC  mov.w     @er6, r0
0x02DEFE  add.w     #0x0020, r0
0x02DF02  shlr.w    #2, r0
0x02DF04  shlr.w    #2, r0
0x02DF06  shlr.w    #2, r0
0x02DF08  mov.w     r0, @er6
0x02DF0A  cmp.w     #0x00ff, r0
0x02DF0E  bls       0x02df16
0x02DF10  mov.w     #0x00ff, r0
0x02DF14  mov.w     r0, @er6
0x02DF16  inc.l     #2, er6
0x02DF18  inc.l     #1, er3
0x02DF1A  cmp.l     #0x00001000, er3
0x02DF20  bcs       0x02defc
0x02DF22  mov.w     #0x5a00, r0
0x02DF26  mov.w     r0, @er5
0x02DF28  jsr       0x010b56
0x02DF2C  mov.l     #0x00001000, er3
0x02DF32  mov.w     @er6, r0
0x02DF34  add.w     #0x0020, r0
0x02DF38  shlr.w    #2, r0
0x02DF3A  shlr.w    #2, r0
0x02DF3C  shlr.w    #2, r0
0x02DF3E  mov.w     r0, @er6
0x02DF40  cmp.w     #0x00ff, r0
0x02DF44  bls       0x02df4c
0x02DF46  mov.w     #0x00ff, r0
0x02DF4A  mov.w     r0, @er6
0x02DF4C  inc.l     #2, er6
0x02DF4E  inc.l     #1, er3
0x02DF50  cmp.l     #0x00002000, er3
0x02DF56  bcs       0x02df32
0x02DF58  mov.w     #0x5a00, r0
0x02DF5C  mov.w     r0, @er5
0x02DF5E  jsr       0x010b56
0x02DF62  mov.l     #0x00002000, er3
0x02DF68  mov.w     @er6, r0
0x02DF6A  add.w     #0x0020, r0
0x02DF6E  shlr.w    #2, r0
0x02DF70  shlr.w    #2, r0
0x02DF72  shlr.w    #2, r0
0x02DF74  mov.w     r0, @er6
0x02DF76  cmp.w     #0x00ff, r0
0x02DF7A  bls       0x02df82
0x02DF7C  mov.w     #0x00ff, r0
0x02DF80  mov.w     r0, @er6
0x02DF82  inc.l     #2, er6
0x02DF84  inc.l     #1, er3
0x02DF86  cmp.l     #0x00003000, er3
0x02DF8C  bcs       0x02df68
0x02DF8E  mov.w     #0x5a00, r0
0x02DF92  mov.w     r0, @er5
0x02DF94  jsr       0x010b56
0x02DF98  mov.l     #0x00003000, er3
0x02DF9E  mov.w     @er6, r0
0x02DFA0  add.w     #0x0020, r0
0x02DFA4  shlr.w    #2, r0
0x02DFA6  shlr.w    #2, r0
0x02DFA8  shlr.w    #2, r0
0x02DFAA  mov.w     r0, @er6
0x02DFAC  cmp.w     #0x00ff, r0
0x02DFB0  bls       0x02dfb8
0x02DFB2  mov.w     #0x00ff, r0
0x02DFB6  mov.w     r0, @er6
0x02DFB8  inc.l     #2, er6
0x02DFBA  inc.l     #1, er3
0x02DFBC  cmp.l     #0x00004000, er3
0x02DFC2  bcs       0x02df9e
0x02DFC4  mov.w     #0x5a00, r0
0x02DFC8  mov.w     r0, @er5
0x02DFCA  jsr       0x010b56
0x02DFCE  jmp       0x02e120
0x02DFD2  mov.l     #0x00818000, er6
0x02DFD8  mov.b     r2l, r0l
0x02DFDA  cmp.b     #0x06, r0l
0x02DFDC  bne       0x02e0a4
0x02DFE0  sub.l     er3, er3
0x02DFE2  mov.l     er6, er0
0x02DFE4  inc.l     #2, er6
0x02DFE6  mov.l     er3, er1
0x02DFE8  add.l     er4, er1
0x02DFEA  shlr.l    #2, er1
0x02DFEC  shlr.l    #2, er1
0x02DFEE  shlr.l    #2, er1
0x02DFF0  mov.w     r1, @er0
0x02DFF2  inc.l     #1, er3
0x02DFF4  cmp.l     #0x00001000, er3
0x02DFFA  bcs       0x02dfe2
0x02DFFC  mov.w     #0x5a00, r0
0x02E000  mov.w     r0, @er5
0x02E002  jsr       0x010b56
0x02E006  mov.l     #0x00001000, er3
0x02E00C  mov.l     er6, er0
0x02E00E  inc.l     #2, er6
0x02E010  mov.l     er3, er1
0x02E012  add.l     er4, er1
0x02E014  shlr.l    #2, er1
0x02E016  shlr.l    #2, er1
0x02E018  shlr.l    #2, er1
0x02E01A  mov.w     r1, @er0
0x02E01C  inc.l     #1, er3
0x02E01E  cmp.l     #0x00002000, er3
0x02E024  bcs       0x02e00c
0x02E026  mov.w     #0x5a00, r0
0x02E02A  mov.w     r0, @er5
0x02E02C  jsr       0x010b56
0x02E030  mov.l     #0x00002000, er3
0x02E036  mov.l     er6, er0
0x02E038  inc.l     #2, er6
0x02E03A  mov.l     er3, er1
0x02E03C  add.l     er4, er1
0x02E03E  shlr.l    #2, er1
0x02E040  shlr.l    #2, er1
0x02E042  shlr.l    #2, er1
0x02E044  mov.w     r1, @er0
0x02E046  inc.l     #1, er3
0x02E048  cmp.l     #0x00003000, er3
0x02E04E  bcs       0x02e036
0x02E050  mov.w     #0x5a00, r0
0x02E054  mov.w     r0, @er5
0x02E056  jsr       0x010b56
0x02E05A  mov.l     #0x00003000, er3
0x02E060  mov.l     er6, er0
0x02E062  inc.l     #2, er6
0x02E064  mov.l     er3, er1
0x02E066  add.l     er4, er1
0x02E068  shlr.l    #2, er1
0x02E06A  shlr.l    #2, er1
0x02E06C  shlr.l    #2, er1
0x02E06E  mov.w     r1, @er0
0x02E070  inc.l     #1, er3
0x02E072  cmp.l     #0x00003fc1, er3
0x02E078  bcs       0x02e060
0x02E07A  mov.w     #0x5a00, r0
0x02E07E  mov.w     r0, @er5
0x02E080  jsr       0x010b56
0x02E084  mov.l     #0x00003fc1, er3
0x02E08A  mov.l     er6, er0
0x02E08C  inc.l     #2, er6
0x02E08E  mov.l     er3, er1
0x02E090  shlr.l    #2, er1
0x02E092  shlr.l    #2, er1
0x02E094  shlr.l    #2, er1
0x02E096  mov.w     r1, @er0
0x02E098  inc.l     #1, er3
0x02E09A  cmp.l     #0x00004000, er3
0x02E0A0  bcs       0x02e08a
0x02E0A2  bt        0x02e120
0x02E0A4  sub.l     er3, er3
0x02E0A6  mov.l     er6, er0
0x02E0A8  inc.l     #2, er6
0x02E0AA  mov.w     r3, @er0
0x02E0AC  inc.l     #1, er3
0x02E0AE  cmp.l     #0x00001000, er3
0x02E0B4  bcs       0x02e0a6
0x02E0B6  mov.w     #0x5a00, r0
0x02E0BA  mov.w     r0, @er5
0x02E0BC  jsr       0x010b56
0x02E0C0  mov.l     #0x00001000, er3
0x02E0C6  mov.l     er6, er0
0x02E0C8  inc.l     #2, er6
0x02E0CA  mov.w     r3, @er0
0x02E0CC  inc.l     #1, er3
0x02E0CE  cmp.l     #0x00002000, er3
0x02E0D4  bcs       0x02e0c6
0x02E0D6  mov.w     #0x5a00, r0
0x02E0DA  mov.w     r0, @er5
0x02E0DC  jsr       0x010b56
0x02E0E0  mov.l     #0x00002000, er3
0x02E0E6  mov.l     er6, er0
0x02E0E8  inc.l     #2, er6
0x02E0EA  mov.w     r3, @er0
0x02E0EC  inc.l     #1, er3
0x02E0EE  cmp.l     #0x00003000, er3
0x02E0F4  bcs       0x02e0e6
0x02E0F6  mov.w     #0x5a00, r0
0x02E0FA  mov.w     r0, @er5
0x02E0FC  jsr       0x010b56
0x02E100  mov.l     #0x00003000, er3
0x02E106  mov.l     er6, er0
0x02E108  inc.l     #2, er6
0x02E10A  mov.w     r3, @er0
0x02E10C  inc.l     #1, er3
0x02E10E  cmp.l     #0x00004000, er3
0x02E114  bcs       0x02e106
0x02E116  mov.w     #0x5a00, r0
0x02E11A  mov.w     r0, @er5
0x02E11C  jsr       0x010b56
0x02E120  mov.w     #0x5a00, r0
0x02E124  mov.w     r0, @er5
0x02E126  mov.b     #0x01, r0l
0x02E128  mov.b     r0l, @0x400eba
0x02E12E  adds.l    #2, sp
0x02E130  adds.l    #4, sp
0x02E132  ldm.l     @sp+, er4-er6
0x02E136  ldm.l     @sp+, er2-er3
0x02E13A  rts       
