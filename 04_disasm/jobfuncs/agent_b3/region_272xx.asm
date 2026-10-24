0x027200  mov.b     r0l, @(0x4,er6)   ; 6e e8 00 04
0x027204  mov.b     r0l, @(0x5,er6)   ; 6e e8 00 05
0x027208  mov.b     r0l, @(0x6,er6)   ; 6e e8 00 06
0x02720C  mov.b     r0l, @(0x7,er6)   ; 6e e8 00 07
0x027210  sub.b     r0l, r0l   ; 18 88
0x027212  mov.b     r0l, @(0x8,er6)   ; 6e e8 00 08
0x027216  mov.b     r0l, @(0x9,er6)   ; 6e e8 00 09
0x02721A  mov.b     r0l, @(0xa,er6)   ; 6e e8 00 0a
0x02721E  mov.b     r0l, @(0xb,er6)   ; 6e e8 00 0b
0x027222  sub.b     r0l, r0l   ; 18 88
0x027224  mov.b     r0l, @(0xc,er6)   ; 6e e8 00 0c
0x027228  bt        0x027246   ; 40 1c
0x02722A  mov.b     @0x42029e, r0l   ; 6a 28 00 42 02 9e
0x027230  bt        0x027238   ; 40 06
0x027232  mov.b     @0x42029f, r0l   ; 6a 28 00 42 02 9f
0x027238  mov.b     r0l, @(0x4,er6)   ; 6e e8 00 04
0x02723C  bt        0x027246   ; 40 08
0x02723E  mov.w     #0x0056, r0   ; 79 00 00 56
0x027242  mov.w     r0, @er4   ; 69 c0
0x027244  bt        0x027250   ; 40 0a
0x027246  mov.w     @(0x22,sp), r1   ; 6f 71 00 22
0x02724A  mov.l     er6, er0   ; 0f e0
0x02724C  jsr       0x011900   ; 5e 01 19 00
0x027250  add.l     #0x00000024, sp   ; 7a 17 00 00 00 24
0x027256  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x02725A  ldm.l     @sp+, er2-er3   ; 01 10 6d 73
0x02725E  rts          ; 54 70
0x027260  mov.b     #0x01, r0l   ; f8 01
0x027262  mov.b     r0l, @0x4003fa   ; 6a a8 00 40 03 fa
0x027268  jsr       0x012ae2   ; 5e 01 2a e2
0x02726C  rts          ; 54 70
0x02726E  mov.l     er6, @-sp   ; 01 00 6d f6
0x027272  mov.l     #0x00fffed2, er6   ; 7a 06 00 ff fe d2
0x027278  mov.w     @er6, r0   ; 69 60
0x02727A  and.w     #0xfffc, r0   ; 79 60 ff fc
0x02727E  or.w      #0x0003, r0   ; 79 40 00 03
0x027282  mov.w     r0, @er6   ; 69 e0
0x027284  jsr       0x017a80   ; 5e 01 7a 80
0x027288  mov.l     #0x00006000, er0   ; 7a 00 00 00 60 00
0x02728E  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x027296  jsr       0x010bd2   ; 5e 01 0b d2
0x02729A  jsr       0x017a78   ; 5e 01 7a 78
0x02729E  jsr       0x010bd8   ; 5e 01 0b d8
0x0272A2  mov.b     #0x0e, r0l   ; f8 0e
0x0272A4  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x0272AA  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x0272B0  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x0272B8  jsr       0x010bd2   ; 5e 01 0b d2
0x0272BC  jsr       0x017a7c   ; 5e 01 7a 7c
0x0272C0  jsr       0x010bd8   ; 5e 01 0b d8
0x0272C4  mov.w     @er6, r0   ; 69 60
0x0272C6  and.w     #0xfffc, r0   ; 79 60 ff fc
0x0272CA  or.w      #0x0003, r0   ; 79 40 00 03
0x0272CE  mov.w     r0, @er6   ; 69 e0
0x0272D0  mov.l     @sp+, er6   ; 01 00 6d 76
0x0272D4  rts          ; 54 70
0x0272D6  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x0272DA  mov.l     #0x00400ca0, er5   ; 7a 05 00 40 0c a0
0x0272E0  mov.l     #0x0040052a, er4   ; 7a 04 00 40 05 2a
0x0272E6  sub.b     r6l, r6l   ; 18 ee
0x0272E8  mov.l     er5, er0   ; 0f d0
0x0272EA  inc.l     #1, er5   ; 0b 75
0x0272EC  mov.b     @er4+, r1l   ; 6c 49
0x0272EE  mov.b     r1l, @er0   ; 68 89
0x0272F0  inc.b     #1, r6l   ; 0a 0e
0x0272F2  cmp.b     #0x04, r6l   ; ae 04
0x0272F4  bcs       0x0272e8   ; 45 f2
0x0272F6  sub.b     r0l, r0l   ; 18 88
0x0272F8  mov.b     r0l, @er5   ; 68 d8
0x0272FA  jsr       0x016e8e   ; 5e 01 6e 8e
0x0272FE  jsr       0x017a80   ; 5e 01 7a 80
0x027302  mov.l     #0x00008000, er0   ; 7a 00 00 00 80 00
0x027308  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x027310  jsr       0x010bd2   ; 5e 01 0b d2
0x027314  mov.l     #0x00fffed2, er6   ; 7a 06 00 ff fe d2
0x02731A  mov.w     @er6, r5   ; 69 65
0x02731C  and.w     #0xfffc, r5   ; 79 65 ff fc
0x027320  or.w      #0x0003, r5   ; 79 45 00 03
0x027324  mov.w     r5, @er6   ; 69 e5
0x027326  jsr       0x017a78   ; 5e 01 7a 78
0x02732A  jsr       0x010bd8   ; 5e 01 0b d8
0x02732E  mov.b     #0x05, r0l   ; f8 05
0x027330  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x027336  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x02733C  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x027344  jsr       0x010bd2   ; 5e 01 0b d2
0x027348  jsr       0x017a7c   ; 5e 01 7a 7c
0x02734C  jsr       0x010bd8   ; 5e 01 0b d8
0x027350  mov.w     @er6, r5   ; 69 65
0x027352  and.w     #0xfffc, r5   ; 79 65 ff fc
0x027356  or.w      #0x0003, r5   ; 79 45 00 03
0x02735A  mov.w     r5, @er6   ; 69 e5
0x02735C  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x027360  rts          ; 54 70
0x027362  mov.l     er3, @-sp   ; 01 00 6d f3
0x027366  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x02736A  mov.l     er0, er3   ; 0f 83
0x02736C  mov.l     #0x00400ca0, er6   ; 7a 06 00 40 0c a0
0x027372  mov.l     #0x00006000, er4   ; 7a 04 00 00 60 00
0x027378  sub.b     r5l, r5l   ; 18 dd
0x02737A  mov.l     er6, er0   ; 0f e0
0x02737C  inc.l     #1, er6   ; 0b 76
0x02737E  mov.b     @er4+, r1l   ; 6c 49
0x027380  mov.b     r1l, @er0   ; 68 89
0x027382  inc.b     #1, r5l   ; 0a 0d
0x027384  cmp.b     #0x10, r5l   ; ad 10
0x027386  bcs       0x02737a   ; 45 f2
0x027388  mov.l     er3, er4   ; 0f b4
0x02738A  sub.b     r5l, r5l   ; 18 dd
0x02738C  mov.l     er6, er0   ; 0f e0
0x02738E  inc.l     #1, er6   ; 0b 76
0x027390  mov.b     @er4+, r1l   ; 6c 49
0x027392  mov.b     r1l, @er0   ; 68 89
0x027394  inc.b     #1, r5l   ; 0a 0d
0x027396  cmp.b     #0x10, r5l   ; ad 10
0x027398  bcs       0x02738c   ; 45 f2
0x02739A  sub.b     r0l, r0l   ; 18 88
0x02739C  mov.b     r0l, @er6   ; 68 e8
0x02739E  jsr       0x016e8e   ; 5e 01 6e 8e
0x0273A2  jsr       0x017a80   ; 5e 01 7a 80
0x0273A6  jsr       0x010bd2   ; 5e 01 0b d2
0x0273AA  mov.l     #0x00006000, er0   ; 7a 00 00 00 60 00
0x0273B0  mov.l     er0, @0xffdc34   ; 01 00 6b a0 00 ff dc 34
0x0273B8  mov.l     #0x00fffed2, er6   ; 7a 06 00 ff fe d2
0x0273BE  mov.w     @er6, r5   ; 69 65
0x0273C0  and.w     #0xfffc, r5   ; 79 65 ff fc
0x0273C4  or.w      #0x0003, r5   ; 79 45 00 03
0x0273C8  mov.w     r5, @er6   ; 69 e5
0x0273CA  jsr       0x017a78   ; 5e 01 7a 78
0x0273CE  jsr       0x010bd8   ; 5e 01 0b d8
0x0273D2  mov.b     #0x21, r0l   ; f8 21
0x0273D4  mov.b     r0l, @0x400d38   ; 6a a8 00 40 0d 38
0x0273DA  mov.l     #0x00400ca0, er0   ; 7a 00 00 40 0c a0
0x0273E0  mov.l     er0, @0xffdc30   ; 01 00 6b a0 00 ff dc 30
0x0273E8  jsr       0x010bd2   ; 5e 01 0b d2
0x0273EC  jsr       0x017a7c   ; 5e 01 7a 7c
0x0273F0  mov.w     @er6, r5   ; 69 65
0x0273F2  and.w     #0xfffc, r5   ; 79 65 ff fc
0x0273F6  or.w      #0x0003, r5   ; 79 45 00 03
0x0273FA  mov.w     r5, @er6   ; 69 e5
0x0273FC  jsr       0x010bd8   ; 5e 01 0b d8
0x027400  ldm.l     @sp+, er4-er6   ; 01 20 6d 76
0x027404  mov.l     @sp+, er3   ; 01 00 6d 73
0x027408  rts          ; 54 70
0x02740A  mov.l     er3, @-sp   ; 01 00 6d f3
0x02740E  stm.l     er4-er6, @-sp   ; 01 20 6d f4
0x027412  mov.l     #0x00400400, er3   ; 7a 03 00 40 04 00
0x027418  mov.l     #0x00400404, er5   ; 7a 05 00 40 04 04
0x02741E  mov.l     #0x00400406, er6   ; 7a 06 00 40 04 06
