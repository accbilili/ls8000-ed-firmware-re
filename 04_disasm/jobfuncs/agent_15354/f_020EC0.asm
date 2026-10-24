; ==== function 0x020EC0 (231 insns) ====
; call/jmp edges:
;   0x020EDC bcc   -> 0x020EFA  beq 0x020efa
;   0x020EE8 bcc   -> 0x020EF2  bne 0x020ef2
;   0x020EEE jmp   -> 0x021198  jmp 0x021198
;   0x020EF6 jmp   -> 0x021198  jmp 0x021198
;   0x020F00 jmp   -> 0x020F14  bt 0x020f14
;   0x020F0C bcc   -> 0x020F1C  beq 0x020f1c
;   0x020F1A bcc   -> 0x020F02  bne 0x020f02
;   0x020F22 bcc   -> 0x020F34  bne 0x020f34
;   0x020F2A bcc   -> 0x020F34  beq 0x020f34
;   0x020F30 jmp   -> 0x021198  jmp 0x021198
;   0x020F3A bcc   -> 0x020F44  bne 0x020f44
;   0x020F40 jmp   -> 0x021198  jmp 0x021198
;   0x020F46 bcc   -> 0x020FE8  bne 0x020fe8
;   0x020F5A bcc   -> 0x020FE8  beq 0x020fe8
;   0x020F6A call  -> 0x018E1E  jsr 0x018e1e
;   0x020F90 bcc   -> 0x020FA4  bne 0x020fa4
;   0x020FA0 jmp   -> 0x0211AC  jmp 0x0211ac
;   0x020FA6 jmp   -> 0x020FD4  bt 0x020fd4
;   0x020FE2 bcc   -> 0x020FA8  bcs 0x020fa8
;   0x020FE4 jmp   -> 0x0211AC  jmp 0x0211ac
;   0x020FF0 bcc   -> 0x021002  beq 0x021002
;   0x020FF2 call  -> 0x011642  jsr 0x011642
;   0x020FF8 bcc   -> 0x021002  bne 0x021002
;   0x020FFE jmp   -> 0x021198  jmp 0x021198
;   0x02100C bcc   -> 0x021016  beq 0x021016
;   0x021014 bcc   -> 0x021022  bne 0x021022
;   0x021018 bcc   -> 0x021022  bne 0x021022
;   0x02101E jmp   -> 0x021198  jmp 0x021198
;   0x02102A bcc   -> 0x02119C  bne 0x02119c
;   0x021030 bcc   -> 0x0210E8  beq 0x0210e8
;   0x021036 bcc   -> 0x0210E8  beq 0x0210e8
;   0x02103C bcc   -> 0x0210E8  beq 0x0210e8
;   0x021042 bcc   -> 0x0210E8  beq 0x0210e8
;   0x021048 bcc   -> 0x0210E8  beq 0x0210e8
;   0x02104E bcc   -> 0x0210E8  beq 0x0210e8
;   0x021054 bcc   -> 0x0210B8  beq 0x0210b8
;   0x021058 bcc   -> 0x0210B8  beq 0x0210b8
;   0x02105C bcc   -> 0x021118  beq 0x021118
;   0x021062 bcc   -> 0x021118  beq 0x021118
;   0x021068 bcc   -> 0x021118  beq 0x021118
;   0x02106E bcc   -> 0x021118  beq 0x021118
;   0x021074 bcc   -> 0x021118  beq 0x021118
;   0x02107A bcc   -> 0x02113E  beq 0x02113e
;   0x021080 bcc   -> 0x021118  beq 0x021118
;   0x021086 bcc   -> 0x021118  beq 0x021118
;   0x02108C bcc   -> 0x021118  beq 0x021118
;   0x021092 bcc   -> 0x021118  beq 0x021118
;   0x021098 bcc   -> 0x021118  beq 0x021118
;   0x02109E bcc   -> 0x021118  beq 0x021118
;   0x0210A2 bcc   -> 0x021118  beq 0x021118
;   0x0210A6 bcc   -> 0x021118  beq 0x021118
;   0x0210AA bcc   -> 0x021162  beq 0x021162
;   0x0210B0 bcc   -> 0x02117E  beq 0x02117e
;   0x0210B4 jmp   -> 0x02119C  jmp 0x02119c
;   0x0210C2 bcc   -> 0x0210D2  beq 0x0210d2
;   0x0210C6 bcc   -> 0x02119C  bne 0x02119c
;   0x0210CE jmp   -> 0x021198  jmp 0x021198
;   0x0210D4 bcc   -> 0x02119C  bne 0x02119c
;   0x0210E4 jmp   -> 0x021198  jmp 0x021198
;   0x0210F2 bcc   -> 0x021102  beq 0x021102
;   0x0210F6 bcc   -> 0x02119C  bne 0x02119c
;   0x0210FE jmp   -> 0x021198  jmp 0x021198
;   0x021104 bcc   -> 0x02119C  bne 0x02119c
;   0x021114 jmp   -> 0x021198  jmp 0x021198
;   0x02111A bcc   -> 0x02119C  bne 0x02119c
;   0x021128 bcc   -> 0x021130  beq 0x021130
;   0x02112E jmp   -> 0x021198  bt 0x021198
;   0x02113C jmp   -> 0x021198  bt 0x021198
;   0x021140 bcc   -> 0x021162  bne 0x021162
;   0x02114C bcc   -> 0x021154  beq 0x021154
;   0x021152 jmp   -> 0x021198  bt 0x021198
;   0x021160 jmp   -> 0x021198  bt 0x021198
;   0x021164 bcc   -> 0x02119C  bne 0x02119c
;   0x021170 bcc   -> 0x021178  beq 0x021178
;   0x021176 jmp   -> 0x021198  bt 0x021198
;   0x02117C jmp   -> 0x021198  bt 0x021198
;   0x021180 bcc   -> 0x02119C  bne 0x02119c
;   0x02118C bcc   -> 0x021194  beq 0x021194
;   0x021192 jmp   -> 0x021198  bt 0x021198
;   0x02119A jmp   -> 0x0211AC  bt 0x0211ac
;   0x0211AA call  ->        ?  jsr er3
0x020EC0:  mov.l    er3, @-sp                                ; [01 00 6D F3]
0x020EC4:  stm.l    er4-er6, @-sp                            ; [01 20 6D F4]
0x020EC8:  mov.l    #0x00400503, er5                         ; [7A 05 00 40 05 03]
0x020ECE:  mov.l    #0x00400436, er6                         ; [7A 06 00 40 04 36]
0x020ED4:  mov.l    @0x40042e, er0                           ; [01 00 6B 20 00 40 04 2E]
0x020EDC:  beq      0x020efa                                 ; [47 1C]
0x020EDE:  mov.b    @er5, r0l                                ; [68 58]
0x020EE0:  mov.b    @0x400508, r1l                           ; [6A 29 00 40 05 08]
0x020EE6:  cmp.b    r1l, r0l                                 ; [1C 98]
0x020EE8:  bne      0x020ef2                                 ; [46 08]
0x020EEA:  mov.w    #0x0070, r0                              ; [79 00 00 70]
0x020EEE:  jmp      0x021198                                 ; [5A 02 11 98]
0x020EF2:  mov.w    #0x0002, r0                              ; [79 00 00 02]
0x020EF6:  jmp      0x021198                                 ; [5A 02 11 98]
0x020EFA:  mov.l    #0x0003e2e8, er3                         ; [7A 03 00 03 E2 E8]
0x020F00:  bt       0x020f14                                 ; [40 12]
0x020F02:  mov.b    @er3, r0l                                ; [68 38]
0x020F04:  mov.b    @0x40043c, r1l                           ; [6A 29 00 40 04 3C]
0x020F0A:  cmp.b    r1l, r0l                                 ; [1C 98]
0x020F0C:  beq      0x020f1c                                 ; [47 0E]
0x020F0E:  add.l    #0x00000008, er3                         ; [7A 13 00 00 00 08]
0x020F14:  mov.l    @(0x4,er3), er0                          ; [01 00 6F 30 00 04]
0x020F1A:  bne      0x020f02                                 ; [46 E6]
0x020F1C:  mov.w    @(0x2,er3), r4                           ; [6F 34 00 02]
0x020F20:  btst     #0, r4l                                  ; [73 0C]
0x020F22:  bne      0x020f34                                 ; [46 10]
0x020F24:  mov.b    @0x400509, r0l                           ; [6A 28 00 40 05 09]
0x020F2A:  beq      0x020f34                                 ; [47 08]
0x020F2C:  mov.w    #0x0051, r0                              ; [79 00 00 51]
0x020F30:  jmp      0x021198                                 ; [5A 02 11 98]
0x020F34:  mov.l    @(0x4,er3), er0                          ; [01 00 6F 30 00 04]
0x020F3A:  bne      0x020f44                                 ; [46 08]
0x020F3C:  mov.w    #0x004f, r0                              ; [79 00 00 4F]
0x020F40:  jmp      0x021198                                 ; [5A 02 11 98]
0x020F44:  btst     #1, r4l                                  ; [73 1C]
0x020F46:  bne      0x020fe8                                 ; [58 60 00 9E]
0x020F4A:  sub.l    er0, er0                                 ; [1A 80]
0x020F4C:  mov.b    @0x400503, r0l                           ; [6A 28 00 40 05 03]
0x020F52:  mov.b    @(0x40033c,er0), r1l                     ; [78 00 6A 29 00 40 03 3C]
0x020F5A:  beq      0x020fe8                                 ; [58 70 00 8A]
0x020F5E:  sub.l    er4, er4                                 ; [1A C4]
0x020F60:  mov.b    @er5, r4l                                ; [68 5C]
0x020F62:  mov.l    er4, er0                                 ; [0F C0]
0x020F64:  mov.l    #0x00000014, er1                         ; [7A 01 00 00 00 14]
0x020F6A:  jsr      0x018e1e                                 ; [5E 01 8E 1E]
0x020F6E:  mov.w    @(0x400344,er0), r0                      ; [78 00 6B 20 00 40 03 44]
0x020F76:  mov.w    r0, @er6                                 ; [69 E0]
0x020F78:  add.l    #0x004003e4, er4                         ; [7A 14 00 40 03 E4]
0x020F7E:  mov.b    @er4, r0l                                ; [68 48]
0x020F80:  dec.b    #1, r0l                                  ; [1A 08]
0x020F82:  mov.b    r0l, @er4                                ; [68 C8]
0x020F84:  sub.l    er0, er0                                 ; [1A 80]
0x020F86:  mov.b    @er5, r0l                                ; [68 58]
0x020F88:  mov.b    @(0x4003e4,er0), r1l                     ; [78 00 6A 29 00 40 03 E4]
0x020F90:  bne      0x020fa4                                 ; [46 12]
0x020F92:  sub.l    er0, er0                                 ; [1A 80]
0x020F94:  mov.b    @er5, r0l                                ; [68 58]
0x020F96:  sub.b    r1l, r1l                                 ; [18 99]
0x020F98:  mov.b    r1l, @(0x40033c,er0)                     ; [78 00 6A A9 00 40 03 3C]
0x020FA0:  jmp      0x0211ac                                 ; [5A 02 11 AC]
0x020FA4:  sub.b    r4l, r4l                                 ; [18 CC]
0x020FA6:  bt       0x020fd4                                 ; [40 2C]
0x020FA8:  mov.b    @er5, r3l                                ; [68 5B]
0x020FAA:  extu.w   r3                                       ; [17 53]
0x020FAC:  mov.w    #0x0014, e3                              ; [79 0B 00 14]
0x020FB0:  mulxu.w  e3, er3                                  ; [52 B3]
0x020FB2:  add.l    #0x00400344, er3                         ; [7A 13 00 40 03 44]
0x020FB8:  mov.b    r4l, r0l                                 ; [0C C8]
0x020FBA:  extu.w   r0                                       ; [17 50]
0x020FBC:  extu.l   er0                                      ; [17 70]
0x020FBE:  shll.l   er0                                      ; [10 30]
0x020FC0:  add.l    er3, er0                                 ; [0A B0]
0x020FC2:  mov.b    r4l, r1l                                 ; [0C C9]
0x020FC4:  extu.w   r1                                       ; [17 51]
0x020FC6:  inc.w    #1, r1                                   ; [0B 51]
0x020FC8:  exts.l   er1                                      ; [17 F1]
0x020FCA:  shll.l   er1                                      ; [10 31]
0x020FCC:  add.l    er3, er1                                 ; [0A B1]
0x020FCE:  mov.w    @er1, r1                                 ; [69 11]
0x020FD0:  mov.w    r1, @er0                                 ; [69 81]
0x020FD2:  inc.b    #1, r4l                                  ; [0A 0C]
0x020FD4:  sub.l    er0, er0                                 ; [1A 80]
0x020FD6:  mov.b    @er5, r0l                                ; [68 58]
0x020FD8:  mov.b    @(0x4003e4,er0), r0l                     ; [78 00 6A 28 00 40 03 E4]
0x020FE0:  cmp.b    r0l, r4l                                 ; [1C 8C]
0x020FE2:  bcs      0x020fa8                                 ; [45 C4]
0x020FE4:  jmp      0x0211ac                                 ; [5A 02 11 AC]
0x020FE8:  btst     #7, @0x40033b                            ; [6A 30 00 40 03 3B 73 70]
0x020FF0:  beq      0x021002                                 ; [47 10]
0x020FF2:  jsr      0x011642                                 ; [5E 01 16 42]
0x020FF6:  and.w    r4, r0                                   ; [66 40]
0x020FF8:  bne      0x021002                                 ; [46 08]
0x020FFA:  mov.w    #0x0003, r0                              ; [79 00 00 03]
0x020FFE:  jmp      0x021198                                 ; [5A 02 11 98]
0x021002:  mov.w    @0x400406, r0                            ; [6B 20 00 40 04 06]
0x021008:  cmp.w    #0x0080, r0                              ; [79 20 00 80]
0x02100C:  beq      0x021016                                 ; [47 08]
0x02100E:  mov.w    @0x400406, r0                            ; [6B 20 00 40 04 06]
0x021014:  bne      0x021022                                 ; [46 0C]
0x021016:  btst     #7, r4l                                  ; [73 7C]
0x021018:  bne      0x021022                                 ; [46 08]
0x02101A:  mov.w    #0x0066, r0                              ; [79 00 00 66]
0x02101E:  jmp      0x021198                                 ; [5A 02 11 98]
0x021022:  mov.w    @0x400406, r0                            ; [6B 20 00 40 04 06]
0x021028:  mov.b    r0h, r0h                                 ; [0C 00]
0x02102A:  bne      0x02119c                                 ; [58 60 01 6E]
0x02102E:  cmp.b    #0x10, r0l                               ; [A8 10]
0x021030:  beq      0x0210e8                                 ; [58 70 00 B4]
0x021034:  cmp.b    #0x11, r0l                               ; [A8 11]
0x021036:  beq      0x0210e8                                 ; [58 70 00 AE]
0x02103A:  cmp.b    #0x12, r0l                               ; [A8 12]
0x02103C:  beq      0x0210e8                                 ; [58 70 00 A8]
0x021040:  cmp.b    #0x13, r0l                               ; [A8 13]
0x021042:  beq      0x0210e8                                 ; [58 70 00 A2]
0x021046:  cmp.b    #0x14, r0l                               ; [A8 14]
0x021048:  beq      0x0210e8                                 ; [58 70 00 9C]
0x02104C:  cmp.b    #0x15, r0l                               ; [A8 15]
0x02104E:  beq      0x0210e8                                 ; [58 70 00 96]
0x021052:  cmp.b    #0x20, r0l                               ; [A8 20]
0x021054:  beq      0x0210b8                                 ; [47 62]
0x021056:  cmp.b    #0x21, r0l                               ; [A8 21]
0x021058:  beq      0x0210b8                                 ; [47 5E]
0x02105A:  cmp.b    #0x40, r0l                               ; [A8 40]
0x02105C:  beq      0x021118                                 ; [58 70 00 B8]
0x021060:  cmp.b    #0x41, r0l                               ; [A8 41]
0x021062:  beq      0x021118                                 ; [58 70 00 B2]
0x021066:  cmp.b    #0x42, r0l                               ; [A8 42]
0x021068:  beq      0x021118                                 ; [58 70 00 AC]
0x02106C:  cmp.b    #0x45, r0l                               ; [A8 45]
0x02106E:  beq      0x021118                                 ; [58 70 00 A6]
0x021072:  cmp.b    #0x81, r0l                               ; [A8 81]
0x021074:  beq      0x021118                                 ; [58 70 00 A0]
0x021078:  cmp.b    #0xa0, r0l                               ; [A8 A0]
0x02107A:  beq      0x02113e                                 ; [58 70 00 C0]
0x02107E:  cmp.b    #0xb0, r0l                               ; [A8 B0]
0x021080:  beq      0x021118                                 ; [58 70 00 94]
0x021084:  cmp.b    #0xb1, r0l                               ; [A8 B1]
0x021086:  beq      0x021118                                 ; [58 70 00 8E]
0x02108A:  cmp.b    #0xb3, r0l                               ; [A8 B3]
0x02108C:  beq      0x021118                                 ; [58 70 00 88]
0x021090:  cmp.b    #0xc0, r0l                               ; [A8 C0]
0x021092:  beq      0x021118                                 ; [58 70 00 82]
0x021096:  cmp.b    #0xc1, r0l                               ; [A8 C1]
0x021098:  beq      0x021118                                 ; [58 70 00 7C]
0x02109C:  cmp.b    #0xd0, r0l                               ; [A8 D0]
0x02109E:  beq      0x021118                                 ; [47 78]
0x0210A0:  cmp.b    #0xd1, r0l                               ; [A8 D1]
0x0210A2:  beq      0x021118                                 ; [47 74]
0x0210A4:  cmp.b    #0xd2, r0l                               ; [A8 D2]
0x0210A6:  beq      0x021118                                 ; [47 70]
0x0210A8:  cmp.b    #0xf3, r0l                               ; [A8 F3]
0x0210AA:  beq      0x021162                                 ; [58 70 00 B4]
0x0210AE:  cmp.b    #0xf4, r0l                               ; [A8 F4]
0x0210B0:  beq      0x02117e                                 ; [58 70 00 CA]
0x0210B4:  jmp      0x02119c                                 ; [5A 02 11 9C]
0x0210B8:  mov.b    @0x400508, r0l                           ; [6A 28 00 40 05 08]
0x0210BE:  mov.b    @er5, r1l                                ; [68 59]
0x0210C0:  cmp.b    r1l, r0l                                 ; [1C 98]
0x0210C2:  beq      0x0210d2                                 ; [47 0E]
0x0210C4:  btst     #0, r4h                                  ; [73 04]
0x0210C6:  bne      0x02119c                                 ; [58 60 00 D2]
0x0210CA:  mov.w    #0x0065, r0                              ; [79 00 00 65]
0x0210CE:  jmp      0x021198                                 ; [5A 02 11 98]
0x0210D2:  btst     #6, r4l                                  ; [73 6C]
0x0210D4:  bne      0x02119c                                 ; [58 60 00 C4]
0x0210D8:  bset     #7, @0x400400                            ; [6A 38 00 40 04 00 70 70]
0x0210E0:  mov.w    #0x0056, r0                              ; [79 00 00 56]
0x0210E4:  jmp      0x021198                                 ; [5A 02 11 98]
0x0210E8:  mov.b    @0x400508, r0l                           ; [6A 28 00 40 05 08]
0x0210EE:  mov.b    @er5, r1l                                ; [68 59]
0x0210F0:  cmp.b    r1l, r0l                                 ; [1C 98]
0x0210F2:  beq      0x021102                                 ; [47 0E]
0x0210F4:  btst     #0, r4h                                  ; [73 04]
0x0210F6:  bne      0x02119c                                 ; [58 60 00 A2]
0x0210FA:  mov.w    #0x0065, r0                              ; [79 00 00 65]
0x0210FE:  jmp      0x021198                                 ; [5A 02 11 98]
0x021102:  btst     #1, r4h                                  ; [73 14]
0x021104:  bne      0x02119c                                 ; [58 60 00 94]
0x021108:  bset     #7, @0x400400                            ; [6A 38 00 40 04 00 70 70]
0x021110:  mov.w    #0x0056, r0                              ; [79 00 00 56]
0x021114:  jmp      0x021198                                 ; [5A 02 11 98]
0x021118:  btst     #0, r4h                                  ; [73 04]
0x02111A:  bne      0x02119c                                 ; [58 60 00 7E]
0x02111E:  mov.b    @0x400508, r0l                           ; [6A 28 00 40 05 08]
0x021124:  mov.b    @er5, r1l                                ; [68 59]
0x021126:  cmp.b    r1l, r0l                                 ; [1C 98]
0x021128:  beq      0x021130                                 ; [47 06]
0x02112A:  mov.w    #0x0065, r0                              ; [79 00 00 65]
0x02112E:  bt       0x021198                                 ; [40 68]
0x021130:  bset     #7, @0x400400                            ; [6A 38 00 40 04 00 70 70]
0x021138:  mov.w    #0x0056, r0                              ; [79 00 00 56]
0x02113C:  bt       0x021198                                 ; [40 5A]
0x02113E:  btst     #2, r4h                                  ; [73 24]
0x021140:  bne      0x021162                                 ; [46 20]
0x021142:  mov.b    @0x400508, r0l                           ; [6A 28 00 40 05 08]
0x021148:  mov.b    @er5, r1l                                ; [68 59]
0x02114A:  cmp.b    r1l, r0l                                 ; [1C 98]
0x02114C:  beq      0x021154                                 ; [47 06]
0x02114E:  mov.w    #0x0065, r0                              ; [79 00 00 65]
0x021152:  bt       0x021198                                 ; [40 44]
0x021154:  bset     #7, @0x400400                            ; [6A 38 00 40 04 00 70 70]
0x02115C:  mov.w    #0x0056, r0                              ; [79 00 00 56]
0x021160:  bt       0x021198                                 ; [40 36]
0x021162:  btst     #0, r4h                                  ; [73 04]
0x021164:  bne      0x02119c                                 ; [46 36]
0x021166:  mov.b    @0x400508, r0l                           ; [6A 28 00 40 05 08]
0x02116C:  mov.b    @er5, r1l                                ; [68 59]
0x02116E:  cmp.b    r1l, r0l                                 ; [1C 98]
0x021170:  beq      0x021178                                 ; [47 06]
0x021172:  mov.w    #0x0065, r0                              ; [79 00 00 65]
0x021176:  bt       0x021198                                 ; [40 20]
0x021178:  mov.w    #0x007a, r0                              ; [79 00 00 7A]
0x02117C:  bt       0x021198                                 ; [40 1A]
0x02117E:  btst     #0, r4h                                  ; [73 04]
0x021180:  bne      0x02119c                                 ; [46 1A]
0x021182:  mov.b    @0x400508, r0l                           ; [6A 28 00 40 05 08]
0x021188:  mov.b    @er5, r1l                                ; [68 59]
0x02118A:  cmp.b    r1l, r0l                                 ; [1C 98]
0x02118C:  beq      0x021194                                 ; [47 06]
0x02118E:  mov.w    #0x0065, r0                              ; [79 00 00 65]
0x021192:  bt       0x021198                                 ; [40 04]
0x021194:  mov.w    #0x007b, r0                              ; [79 00 00 7B]
0x021198:  mov.w    r0, @er6                                 ; [69 E0]
0x02119A:  bt       0x0211ac                                 ; [40 10]
0x02119C:  mov.b    @er5, r0l                                ; [68 58]
0x02119E:  mov.b    r0l, @0x400508                           ; [6A A8 00 40 05 08]
0x0211A4:  mov.l    @(0x4,er3), er3                          ; [01 00 6F 33 00 04]
0x0211AA:  jsr      er3                                      ; [5D 30]
0x0211AC:  ldm.l    @sp+, er4-er6                            ; [01 20 6D 76]
0x0211B0:  mov.l    @sp+, er3                                ; [01 00 6D 73]
0x0211B4:  rts                                               ; [54 70]
