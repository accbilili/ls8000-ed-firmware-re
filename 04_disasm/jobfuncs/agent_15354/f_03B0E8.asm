; ==== function 0x03B0E8 (146 insns) ====
; call/jmp edges:
;   0x03B0FC call  -> 0x018E9E  jsr 0x018e9e
;   0x03B106 call  -> 0x0185EE  jsr 0x0185ee
;   0x03B116 call  -> 0x018948  jsr 0x018948
;   0x03B11C bcc   -> 0x03B12C  beq 0x03b12c
;   0x03B12A jmp   -> 0x03B138  bt 0x03b138
;   0x03B138 call  -> 0x0181B2  jsr 0x0181b2
;   0x03B152 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B16E call  -> 0x018E9E  jsr 0x018e9e
;   0x03B17A call  -> 0x0185EE  jsr 0x0185ee
;   0x03B186 call  -> 0x018948  jsr 0x018948
;   0x03B18C bcc   -> 0x03B198  beq 0x03b198
;   0x03B196 jmp   -> 0x03B1A0  bt 0x03b1a0
;   0x03B1A0 call  -> 0x0181B2  jsr 0x0181b2
;   0x03B1B2 call  -> 0x018948  jsr 0x018948
;   0x03B1B8 bcc   -> 0x03B1D0  beq 0x03b1d0
;   0x03B1C2 call  -> 0x018948  jsr 0x018948
;   0x03B1C8 bcc   -> 0x03B1D0  beq 0x03b1d0
;   0x03B1CC jmp   -> 0x03B3BE  jmp 0x03b3be
;   0x03B1D8 call  -> 0x018948  jsr 0x018948
;   0x03B1DE bcc   -> 0x03B3BE  beq 0x03b3be
;   0x03B1EA call  -> 0x018948  jsr 0x018948
;   0x03B1F0 bcc   -> 0x03B3BE  beq 0x03b3be
;   0x03B1F6 jmp   -> 0x03B3BE  jmp 0x03b3be
;   0x03B3C4 call  -> 0x03BFBE  bsr 0x03bfbe
;   0x03B3DE call  -> 0x018E1E  jsr 0x018e1e
;   0x03B3EA call  -> 0x01872E  jsr 0x01872e
;   0x03B3F4 bcc   -> 0x03B486  bcc 0x03b486
;   0x03B40A bcc   -> 0x03B486  bls 0x03b486
;   0x03B40E bcc   -> 0x03B486  beq 0x03b486
;   0x03B414 bcc   -> 0x03B486  beq 0x03b486
;   0x03B484 jmp   -> 0x03B4E4  bt 0x03b4e4
;   0x03B48C bcc   -> 0x03B4E2  beq 0x03b4e2
;   0x03B49C call  -> 0x018E1E  jsr 0x018e1e
;   0x03B4A8 call  -> 0x01872E  jsr 0x01872e
;   0x03B4B2 bcc   -> 0x03B4D8  bcc 0x03b4d8
;   0x03B4C6 bcc   -> 0x03B4D8  bls 0x03b4d8
;   0x03B4CA bcc   -> 0x03B4D2  beq 0x03b4d2
;   0x03B4D0 bcc   -> 0x03B4D8  bne 0x03b4d8
;   0x03B4D6 jmp   -> 0x03B4DC  bt 0x03b4dc
0x03B0E8:  mov.l    @(0xe,sp), er1                           ; [01 00 6F 71 00 0E]
0x03B0EE:  add.l    #0x00000010, er1                         ; [7A 11 00 00 00 10]
0x03B0F4:  mov.l    er0, @sp                                 ; [01 00 69 F0]
0x03B0F8:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B0FC:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B100:  mov.l    er0, er1                                 ; [0F 81]
0x03B102:  mov.l    @sp, er0                                 ; [01 00 69 70]
0x03B106:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B10A:  mov.l    er0, @(0x18,sp)                          ; [01 00 6F F0 00 18]
0x03B110:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B116:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B11A:  mov.w    r0, r0                                   ; [0D 00]
0x03B11C:  beq      0x03b12c                                 ; [47 0E]
0x03B11E:  mov.l    #0x3f800000, er0                         ; [7A 00 3F 80 00 00]
0x03B124:  mov.l    @(0x18,sp), er1                          ; [01 00 6F 71 00 18]
0x03B12A:  bt       0x03b138                                 ; [40 0C]
0x03B12C:  mov.l    @(0x18,sp), er0                          ; [01 00 6F 70 00 18]
0x03B132:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B138:  jsr      0x0181b2                                 ; [5E 01 81 B2]
0x03B13C:  mov.l    er0, @(0x18,sp)                          ; [01 00 6F F0 00 18]
0x03B142:  mov.w    r6, r1                                   ; [0D 61]
0x03B144:  sub.w    #0x0008, r1                              ; [79 31 00 08]
0x03B148:  extu.l   er1                                      ; [17 71]
0x03B14A:  shll.l   #2, er1                                  ; [10 71]
0x03B14C:  add.l    er5, er1                                 ; [0A D1]
0x03B14E:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B152:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B156:  mov.w    r6, r1                                   ; [0D 61]
0x03B158:  extu.l   er1                                      ; [17 71]
0x03B15A:  shll.l   #2, er1                                  ; [10 71]
0x03B15C:  add.l    er5, er1                                 ; [0A D1]
0x03B15E:  add.l    #0x00000010, er1                         ; [7A 11 00 00 00 10]
0x03B164:  mov.l    er0, @(0x4,sp)                           ; [01 00 6F F0 00 04]
0x03B16A:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B16E:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B172:  mov.l    er0, er1                                 ; [0F 81]
0x03B174:  mov.l    @(0x4,sp), er0                           ; [01 00 6F 70 00 04]
0x03B17A:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B17E:  mov.l    er0, er2                                 ; [0F 82]
0x03B180:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B186:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B18A:  mov.w    r0, r0                                   ; [0D 00]
0x03B18C:  beq      0x03b198                                 ; [47 0A]
0x03B18E:  mov.l    #0x3f800000, er0                         ; [7A 00 3F 80 00 00]
0x03B194:  mov.l    er2, er1                                 ; [0F A1]
0x03B196:  bt       0x03b1a0                                 ; [40 08]
0x03B198:  mov.l    er2, er0                                 ; [0F A0]
0x03B19A:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B1A0:  jsr      0x0181b2                                 ; [5E 01 81 B2]
0x03B1A4:  mov.l    er0, er2                                 ; [0F 82]
0x03B1A6:  mov.l    @(0x18,sp), er0                          ; [01 00 6F 70 00 18]
0x03B1AC:  mov.l    @(0x14,sp), er1                          ; [01 00 6F 71 00 14]
0x03B1B2:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B1B6:  mov.w    r0, r0                                   ; [0D 00]
0x03B1B8:  beq      0x03b1d0                                 ; [47 16]
0x03B1BA:  mov.l    @(0x18,sp), er0                          ; [01 00 6F 70 00 18]
0x03B1C0:  mov.l    er2, er1                                 ; [0F A1]
0x03B1C2:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B1C6:  mov.w    r0, r0                                   ; [0D 00]
0x03B1C8:  beq      0x03b1d0                                 ; [47 06]
0x03B1CA:  dec.w    #1, r6                                   ; [1B 56]
0x03B1CC:  jmp      0x03b3be                                 ; [5A 03 B3 BE]
0x03B1D0:  mov.l    er2, er0                                 ; [0F A0]
0x03B1D2:  mov.l    @(0x14,sp), er1                          ; [01 00 6F 71 00 14]
0x03B1D8:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B1DC:  mov.w    r0, r0                                   ; [0D 00]
0x03B1DE:  beq      0x03b3be                                 ; [58 70 01 DC]
0x03B1E2:  mov.l    er2, er0                                 ; [0F A0]
0x03B1E4:  mov.l    @(0x18,sp), er1                          ; [01 00 6F 71 00 18]
0x03B1EA:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B1EE:  mov.w    r0, r0                                   ; [0D 00]
0x03B1F0:  beq      0x03b3be                                 ; [58 70 01 CA]
0x03B1F4:  dec.w    #2, r6                                   ; [1B D6]
0x03B1F6:  jmp      0x03b3be                                 ; [5A 03 B3 BE]
0x03B3BE:  mov.w    @0x4491d2, r0                            ; [6B 20 00 44 91 D2]
0x03B3C4:  bsr      0x03bfbe                                 ; [5C 00 0B F6]
0x03B3C8:  mov.l    er0, @0x4491d8                           ; [01 00 6B A0 00 44 91 D8]
0x03B3D0:  mov.l    @0x4491e0, er0                           ; [01 00 6B 20 00 44 91 E0]
0x03B3D8:  mov.l    #0x000000ff, er1                         ; [7A 01 00 00 00 FF]
0x03B3DE:  jsr      0x018e1e                                 ; [5E 01 8E 1E]
0x03B3E2:  mov.l    @0x4491dc, er1                           ; [01 00 6B 21 00 44 91 DC]
0x03B3EA:  jsr      0x01872e                                 ; [5E 01 87 2E]
0x03B3EE:  cmp.l    #0x000000a0, er0                         ; [7A 20 00 00 00 A0]
0x03B3F4:  bcc      0x03b486                                 ; [58 40 00 8E]
0x03B3F8:  mov.l    @0x4491dc, er0                           ; [01 00 6B 20 00 44 91 DC]
0x03B400:  mov.l    @0x4491d8, er1                           ; [01 00 6B 21 00 44 91 D8]
0x03B408:  cmp.l    er1, er0                                 ; [1F 90]
0x03B40A:  bls      0x03b486                                 ; [43 7A]
0x03B40C:  mov.w    r6, r6                                   ; [0D 66]
0x03B40E:  beq      0x03b486                                 ; [47 76]
0x03B410:  cmp.w    #0x01c2, r6                              ; [79 26 01 C2]
0x03B414:  beq      0x03b486                                 ; [47 70]
0x03B416:  mov.l    @(0x8,sp), er1                           ; [01 00 6F 71 00 08]
0x03B41C:  mov.w    r6, @er1                                 ; [69 96]
0x03B41E:  mov.w    r6, @0x449a2a                            ; [6B A6 00 44 9A 2A]
0x03B424:  mov.w    r6, @0x42026c                            ; [6B A6 00 42 02 6C]
0x03B42A:  sub.w    r0, r0                                   ; [19 00]
0x03B42C:  mov.w    r0, @0x400402                            ; [6B A0 00 40 04 02]
0x03B432:  sub.l    er0, er0                                 ; [1A 80]
0x03B434:  mov.b    @0x4491d5, r0l                           ; [6A 28 00 44 91 D5]
0x03B43A:  shll.l   er0                                      ; [10 30]
0x03B43C:  mov.w    @0x400d60, r1                            ; [6B 21 00 40 0D 60]
0x03B442:  mov.w    @(0x449086,er0), r0                      ; [78 00 6B 20 00 44 90 86]
0x03B44A:  sub.w    r0, r1                                   ; [19 01]
0x03B44C:  mov.w    @0x420274, r0                            ; [6B 20 00 42 02 74]
0x03B452:  shlr.w   r0                                       ; [11 10]
0x03B454:  sub.w    r0, r1                                   ; [19 01]
0x03B456:  mov.w    r1, @0x420272                            ; [6B A1 00 42 02 72]
0x03B45C:  mov.w    @0x4202f8, r0                            ; [6B 20 00 42 02 F8]
0x03B462:  sub.w    #0x00ab, r0                              ; [79 30 00 AB]
0x03B466:  mov.w    #0x000c, e0                              ; [79 08 00 0C]
0x03B46A:  mulxu.w  e0, er0                                  ; [52 80]
0x03B46C:  mov.w    @0x4202a2, r1                            ; [6B 21 00 42 02 A2]
0x03B472:  add.w    r1, r0                                   ; [09 10]
0x03B474:  add.w    #0xe13e, r0                              ; [79 10 E1 3E]
0x03B478:  extu.l   er0                                      ; [17 70]
0x03B47A:  mov.l    er0, @0x42026e                           ; [01 00 6B A0 00 42 02 6E]
0x03B482:  mov.b    #0x01, r0l                               ; [F8 01]
0x03B484:  bt       0x03b4e4                                 ; [40 5E]
0x03B486:  mov.b    @(0xd,sp), r0l                           ; [6E 78 00 0D]
0x03B48A:  cmp.b    #0x01, r0l                               ; [A8 01]
0x03B48C:  beq      0x03b4e2                                 ; [47 54]
0x03B48E:  mov.l    @0x4491e0, er0                           ; [01 00 6B 20 00 44 91 E0]
0x03B496:  mov.l    #0x000000ff, er1                         ; [7A 01 00 00 00 FF]
0x03B49C:  jsr      0x018e1e                                 ; [5E 01 8E 1E]
0x03B4A0:  mov.l    @0x4491dc, er1                           ; [01 00 6B 21 00 44 91 DC]
0x03B4A8:  jsr      0x01872e                                 ; [5E 01 87 2E]
0x03B4AC:  cmp.l    #0x000000a0, er0                         ; [7A 20 00 00 00 A0]
0x03B4B2:  bcc      0x03b4d8                                 ; [44 24]
0x03B4B4:  mov.l    @0x4491dc, er0                           ; [01 00 6B 20 00 44 91 DC]
0x03B4BC:  mov.l    @0x4491d8, er1                           ; [01 00 6B 21 00 44 91 D8]
0x03B4C4:  cmp.l    er1, er0                                 ; [1F 90]
0x03B4C6:  bls      0x03b4d8                                 ; [43 10]
0x03B4C8:  mov.w    r6, r6                                   ; [0D 66]
0x03B4CA:  beq      0x03b4d2                                 ; [47 06]
0x03B4CC:  cmp.w    #0x01c2, r6                              ; [79 26 01 C2]
0x03B4D0:  bne      0x03b4d8                                 ; [46 06]
0x03B4D2:  mov.w    #0x0920, r0                              ; [79 00 09 20]
0x03B4D6:  bt       0x03b4dc                                 ; [40 04]
0x03B4D8:  mov.w    #0x0930, r0                              ; [79 00 09 30]
0x03B4DC:  mov.w    r0, @0x400402                            ; [6B A0 00 40 04 02]
0x03B4E2:  sub.b    r0l, r0l                                 ; [18 88]
0x03B4E4:  add.l    #0x00000020, sp                          ; [7A 17 00 00 00 20]
0x03B4EA:  ldm.l    @sp+, er4-er6                            ; [01 20 6D 76]
0x03B4EE:  ldm.l    @sp+, er2-er3                            ; [01 10 6D 73]
0x03B4F2:  rts                                               ; [54 70]
