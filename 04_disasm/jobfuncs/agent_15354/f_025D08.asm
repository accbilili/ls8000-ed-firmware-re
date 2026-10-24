; ==== function 0x025D08 (80 insns) ====
; call/jmp edges:
;   0x025D28 bcc   -> 0x025DEC  bhi 0x025dec
;   0x025D32 bcc   -> 0x025DEC  bhi 0x025dec
;   0x025D3C call  -> 0x01605A  jsr 0x01605a
;   0x025D4C bcc   -> 0x025D62  bne 0x025d62
;   0x025D54 bcc   -> 0x025DDC  bcs 0x025ddc
;   0x025D5E bcc   -> 0x025D6E  bls 0x025d6e
;   0x025D60 jmp   -> 0x025DDC  bt 0x025ddc
;   0x025D66 bcc   -> 0x025DDC  bcs 0x025ddc
;   0x025D6C bcc   -> 0x025DDC  bhi 0x025ddc
;   0x025D88 bcc   -> 0x025DA6  bls 0x025da6
;   0x025D90 bcc   -> 0x025DA6  bls 0x025da6
;   0x025D98 call  -> 0x0160DE  jsr 0x0160de
;   0x025DB0 bcc   -> 0x025DE0  beq 0x025de0
;   0x025DBC bcc   -> 0x025DE0  beq 0x025de0
;   0x025DC2 bcc   -> 0x025DE0  beq 0x025de0
;   0x025DC8 bcc   -> 0x025DE0  beq 0x025de0
;   0x025DCE bcc   -> 0x025DE0  beq 0x025de0
;   0x025DD4 bcc   -> 0x025DE0  beq 0x025de0
;   0x025DDA bcc   -> 0x025DE0  beq 0x025de0
;   0x025DDE jmp   -> 0x025DEE  bt 0x025dee
0x025D08:  mov.l    er3, @-sp                                ; [01 00 6D F3]
0x025D0C:  stm.l    er4-er6, @-sp                            ; [01 20 6D F4]
0x025D10:  mov.l    #0x00400316, er4                         ; [7A 04 00 40 03 16]
0x025D16:  mov.l    er0, er3                                 ; [0F 83]
0x025D18:  mov.w    r1, r6                                   ; [0D 16]
0x025D1A:  mov.w    @er3, r5                                 ; [69 35]
0x025D1C:  mov.l    @(0x14,sp), er0                          ; [01 00 6F 70 00 14]
0x025D22:  sub.w    r1, r1                                   ; [19 11]
0x025D24:  mov.w    r1, @er0                                 ; [69 81]
0x025D26:  cmp.w    r6, r5                                   ; [1D 65]
0x025D28:  bhi      0x025dec                                 ; [58 20 00 C0]
0x025D2C:  mov.w    r5, r0                                   ; [0D 50]
0x025D2E:  inc.w    #1, r0                                   ; [0B 50]
0x025D30:  cmp.w    r6, r0                                   ; [1D 60]
0x025D32:  bhi      0x025dec                                 ; [58 20 00 B6]
0x025D36:  mov.w    r5, r1                                   ; [0D 51]
0x025D38:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025D3C:  jsr      0x01605a                                 ; [5E 01 60 5A]
0x025D40:  mov.w    r0, r6                                   ; [0D 06]
0x025D42:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025D46:  mov.b    @(0x2a,er0), r0l                         ; [6E 08 00 2A]
0x025D4A:  btst     #1, r0l                                  ; [73 18]
0x025D4C:  bne      0x025d62                                 ; [46 14]
0x025D4E:  mov.w    @(0xa,er3), r0                           ; [6F 30 00 0A]
0x025D52:  cmp.w    r0, r6                                   ; [1D 06]
0x025D54:  bcs      0x025ddc                                 ; [58 50 00 84]
0x025D58:  mov.w    @(0xe,er3), r3                           ; [6F 33 00 0E]
0x025D5C:  cmp.w    r3, r6                                   ; [1D 36]
0x025D5E:  bls      0x025d6e                                 ; [43 0E]
0x025D60:  bt       0x025ddc                                 ; [40 7A]
0x025D62:  cmp.w    #0x0053, r6                              ; [79 26 00 53]
0x025D66:  bcs      0x025ddc                                 ; [45 74]
0x025D68:  cmp.w    #0x0053, r6                              ; [79 26 00 53]
0x025D6C:  bhi      0x025ddc                                 ; [42 6E]
0x025D6E:  mov.w    #0x0fa0, r0                              ; [79 00 0F A0]
0x025D72:  extu.l   er0                                      ; [17 70]
0x025D74:  divxu.w  r6, er0                                  ; [53 60]
0x025D76:  mov.w    r0, e6                                   ; [0D 0E]
0x025D78:  mov.w    #0x0fa0, r1                              ; [79 01 0F A0]
0x025D7C:  extu.l   er1                                      ; [17 71]
0x025D7E:  divxu.w  r0, er1                                  ; [53 01]
0x025D80:  mov.w    r1, e5                                   ; [0D 1D]
0x025D82:  sub.w    r6, r1                                   ; [19 61]
0x025D84:  cmp.w    #0x0002, r1                              ; [79 21 00 02]
0x025D88:  bls      0x025da6                                 ; [43 1C]
0x025D8A:  sub.w    e5, r6                                   ; [19 D6]
0x025D8C:  cmp.w    #0x0002, r6                              ; [79 26 00 02]
0x025D90:  bls      0x025da6                                 ; [43 14]
0x025D92:  mov.l    er5, er1                                 ; [0F D1]
0x025D94:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025D98:  jsr      0x0160de                                 ; [5E 01 60 DE]
0x025D9C:  mov.w    #0x0004, r0                              ; [79 00 00 04]
0x025DA0:  mov.w    r0, @0x400436                            ; [6B A0 00 40 04 36]
0x025DA6:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025DAA:  mov.b    @(0x2a,er0), r0l                         ; [6E 08 00 2A]
0x025DAE:  btst     #0, r0l                                  ; [73 08]
0x025DB0:  beq      0x025de0                                 ; [47 2E]
0x025DB2:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025DB6:  mov.b    @(0x2b,er0), r0l                         ; [6E 08 00 2B]
0x025DBA:  btst     #2, r0l                                  ; [73 28]
0x025DBC:  beq      0x025de0                                 ; [47 22]
0x025DBE:  cmp.w    #0x0001, e6                              ; [79 2E 00 01]
0x025DC2:  beq      0x025de0                                 ; [47 1C]
0x025DC4:  cmp.w    #0x0002, e6                              ; [79 2E 00 02]
0x025DC8:  beq      0x025de0                                 ; [47 16]
0x025DCA:  cmp.w    #0x0003, e6                              ; [79 2E 00 03]
0x025DCE:  beq      0x025de0                                 ; [47 10]
0x025DD0:  cmp.w    #0x0004, e6                              ; [79 2E 00 04]
0x025DD4:  beq      0x025de0                                 ; [47 0A]
0x025DD6:  cmp.w    #0x0006, e6                              ; [79 2E 00 06]
0x025DDA:  beq      0x025de0                                 ; [47 04]
0x025DDC:  sub.b    r0l, r0l                                 ; [18 88]
0x025DDE:  bt       0x025dee                                 ; [40 0E]
0x025DE0:  mov.l    @(0x14,sp), er0                          ; [01 00 6F 70 00 14]
0x025DE6:  mov.w    #0x0002, r1                              ; [79 01 00 02]
0x025DEA:  mov.w    r1, @er0                                 ; [69 81]
0x025DEC:  mov.b    #0x01, r0l                               ; [F8 01]
0x025DEE:  ldm.l    @sp+, er4-er6                            ; [01 20 6D 76]
0x025DF2:  mov.l    @sp+, er3                                ; [01 00 6D 73]
0x025DF6:  rts                                               ; [54 70]
