; ==== function 0x018686 (59 insns) ====
; call/jmp edges:
;   0x0185D6 jmp   -> 0x0186FA  bt 0x0186fa
;   0x0185E0 jmp   -> 0x0186E8  bt 0x0186e8
;   0x018688 bcc   -> 0x01868C  beq 0x01868c
;   0x018690 bcc   -> 0x018696  bne 0x018696
;   0x01869A bcc   -> 0x0185DA  bge 0x0185da
;   0x0186A2 bcc   -> 0x0185D0  bmi 0x0185d0
;   0x0186A8 bcc   -> 0x0186D0  bgt 0x0186d0
;   0x0186AC bcc   -> 0x0186B0  bcc 0x0186b0
;   0x0186B2 bcc   -> 0x0186B8  bpl 0x0186b8
;   0x0186B6 jmp   -> 0x0186AA  bt 0x0186aa
;   0x0186BA bcc   -> 0x0186CE  beq 0x0186ce
;   0x0186C2 bcc   -> 0x0186CE  beq 0x0186ce
;   0x0186CA bcc   -> 0x0186CE  bpl 0x0186ce
;   0x0186CE jmp   -> 0x0186E8  bt 0x0186e8
;   0x0186D2 bcc   -> 0x0186E8  beq 0x0186e8
;   0x0186DA bcc   -> 0x0186E8  beq 0x0186e8
;   0x0186E2 bcc   -> 0x0186E8  bcc 0x0186e8
0x0185D0:  sub.l    er0, er0                                 ; [1A 80]
0x0185D2:  shll.w   e5                                       ; [10 1D]
0x0185D4:  rotxr.w  e0                                       ; [13 18]
0x0185D6:  bt       0x0186fa                                 ; [58 00 01 20]
0x0185DA:  mov.w    #0x00ff, r2                              ; [79 02 00 FF]
0x0185DE:  sub.l    er1, er1                                 ; [1A 91]
0x0185E0:  bt       0x0186e8                                 ; [58 00 01 04]
0x018686:  mov.l    er0, er0                                 ; [0F 80]
0x018688:  beq      0x01868c                                 ; [47 02]
0x01868A:  or.b     #0x20, r1l                               ; [C9 20]
0x01868C:  mov.w    e1, r5                                   ; [0D 95]
0x01868E:  btst     #7, r5h                                  ; [73 75]
0x018690:  bne      0x018696                                 ; [46 04]
0x018692:  shll.l   er1                                      ; [10 31]
0x018694:  dec.w    #1, r2                                   ; [1B 52]
0x018696:  cmp.w    #0x00ff, r2                              ; [79 22 00 FF]
0x01869A:  bge      0x0185da                                 ; [58 C0 FF 3C]
0x01869E:  cmp.w    #0xffe9, r2                              ; [79 22 FF E9]
0x0186A2:  bmi      0x0185d0                                 ; [58 B0 FF 2A]
0x0186A6:  mov.w    r2, r2                                   ; [0D 22]
0x0186A8:  bgt      0x0186d0                                 ; [4E 26]
0x0186AA:  shlr.l   er1                                      ; [11 31]
0x0186AC:  bcc      0x0186b0                                 ; [44 02]
0x0186AE:  bset     #0, r1l                                  ; [70 09]
0x0186B0:  mov.w    r2, r2                                   ; [0D 22]
0x0186B2:  bpl      0x0186b8                                 ; [4A 04]
0x0186B4:  inc.w    #1, r2                                   ; [0B 52]
0x0186B6:  bt       0x0186aa                                 ; [40 F2]
0x0186B8:  btst     #7, r1l                                  ; [73 79]
0x0186BA:  beq      0x0186ce                                 ; [47 12]
0x0186BC:  mov.w    r1, r5                                   ; [0D 15]
0x0186BE:  and.w    #0x017f, r5                              ; [79 65 01 7F]
0x0186C2:  beq      0x0186ce                                 ; [47 0A]
0x0186C4:  add.l    #0x00000100, er1                         ; [7A 11 00 00 01 00]
0x0186CA:  bpl      0x0186ce                                 ; [4A 02]
0x0186CC:  inc.w    #1, r2                                   ; [0B 52]
0x0186CE:  bt       0x0186e8                                 ; [40 18]
0x0186D0:  btst     #7, r1l                                  ; [73 79]
0x0186D2:  beq      0x0186e8                                 ; [47 14]
0x0186D4:  mov.w    r1, r5                                   ; [0D 15]
0x0186D6:  and.w    #0x017f, r5                              ; [79 65 01 7F]
0x0186DA:  beq      0x0186e8                                 ; [47 0C]
0x0186DC:  add.l    #0x00000100, er1                         ; [7A 11 00 00 01 00]
0x0186E2:  bcc      0x0186e8                                 ; [44 04]
0x0186E4:  rotxr.l  er1                                      ; [13 31]
0x0186E6:  inc.w    #1, r2                                   ; [0B 52]
0x0186E8:  shll.l   er1                                      ; [10 31]
0x0186EA:  mov.w    e1, r5                                   ; [0D 95]
0x0186EC:  mov.b    r5l, r0h                                 ; [0C D0]
0x0186EE:  mov.b    r1h, r0l                                 ; [0C 18]
0x0186F0:  mov.b    r5h, r5l                                 ; [0C 5D]
0x0186F2:  mov.b    r2l, r5h                                 ; [0C A5]
0x0186F4:  mov.w    r5, e0                                   ; [0D 58]
0x0186F6:  shll.w   e5                                       ; [10 1D]
0x0186F8:  rotxr.l  er0                                      ; [13 30]
0x0186FA:  mov.l    @sp+, er1                                ; [01 00 6D 71]
0x0186FE:  ldm.l    @sp+, er2-er3                            ; [01 10 6D 73]
0x018702:  ldm.l    @sp+, er4-er5                            ; [01 10 6D 75]
0x018706:  rts                                               ; [54 70]
