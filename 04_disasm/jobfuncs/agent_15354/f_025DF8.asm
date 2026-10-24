; ==== function 0x025DF8 (82 insns) ====
; call/jmp edges:
;   0x025E14 bcc   -> 0x025EE6  bhi 0x025ee6
;   0x025E1E bcc   -> 0x025EE6  bhi 0x025ee6
;   0x025E28 call  -> 0x01605A  jsr 0x01605a
;   0x025E38 bcc   -> 0x025E50  bne 0x025e50
;   0x025E40 bcc   -> 0x025ED6  bcs 0x025ed6
;   0x025E4A bcc   -> 0x025E5E  bls 0x025e5e
;   0x025E4C jmp   -> 0x025ED6  jmp 0x025ed6
;   0x025E54 bcc   -> 0x025ED6  bcs 0x025ed6
;   0x025E5C bcc   -> 0x025ED6  bhi 0x025ed6
;   0x025E78 bcc   -> 0x025E9A  bls 0x025e9a
;   0x025E80 bcc   -> 0x025E9A  bls 0x025e9a
;   0x025E8C call  -> 0x0160DE  jsr 0x0160de
;   0x025EA4 bcc   -> 0x025EDA  beq 0x025eda
;   0x025EB0 bcc   -> 0x025EDA  beq 0x025eda
;   0x025EB6 bcc   -> 0x025EDA  beq 0x025eda
;   0x025EBC bcc   -> 0x025EDA  beq 0x025eda
;   0x025EC2 bcc   -> 0x025EDA  beq 0x025eda
;   0x025EC8 bcc   -> 0x025EDA  beq 0x025eda
;   0x025ECE bcc   -> 0x025EDA  beq 0x025eda
;   0x025ED4 bcc   -> 0x025EDA  beq 0x025eda
;   0x025ED8 jmp   -> 0x025EE8  bt 0x025ee8
0x025DF8:  stm.l    er4-er6, @-sp                            ; [01 20 6D F4]
0x025DFC:  mov.l    #0x00400316, er4                         ; [7A 04 00 40 03 16]
0x025E02:  mov.l    er0, er6                                 ; [0F 86]
0x025E04:  mov.w    r1, r5                                   ; [0D 15]
0x025E06:  mov.w    @er6, e5                                 ; [69 6D]
0x025E08:  mov.l    @(0x10,sp), er0                          ; [01 00 6F 70 00 10]
0x025E0E:  sub.w    r1, r1                                   ; [19 11]
0x025E10:  mov.w    r1, @er0                                 ; [69 81]
0x025E12:  cmp.w    r5, e5                                   ; [1D 5D]
0x025E14:  bhi      0x025ee6                                 ; [58 20 00 CE]
0x025E18:  mov.w    e5, r0                                   ; [0D D0]
0x025E1A:  inc.w    #1, r0                                   ; [0B 50]
0x025E1C:  cmp.w    r5, r0                                   ; [1D 50]
0x025E1E:  bhi      0x025ee6                                 ; [58 20 00 C4]
0x025E22:  mov.w    e5, r1                                   ; [0D D1]
0x025E24:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025E28:  jsr      0x01605a                                 ; [5E 01 60 5A]
0x025E2C:  mov.w    r0, r5                                   ; [0D 05]
0x025E2E:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025E32:  mov.b    @(0x2a,er0), r0l                         ; [6E 08 00 2A]
0x025E36:  btst     #1, r0l                                  ; [73 18]
0x025E38:  bne      0x025e50                                 ; [46 16]
0x025E3A:  mov.w    @(0xa,er6), r0                           ; [6F 60 00 0A]
0x025E3E:  cmp.w    r0, r5                                   ; [1D 05]
0x025E40:  bcs      0x025ed6                                 ; [58 50 00 92]
0x025E44:  mov.w    @(0xe,er6), r6                           ; [6F 66 00 0E]
0x025E48:  cmp.w    r6, r5                                   ; [1D 65]
0x025E4A:  bls      0x025e5e                                 ; [43 12]
0x025E4C:  jmp      0x025ed6                                 ; [5A 02 5E D6]
0x025E50:  cmp.w    #0x0053, r5                              ; [79 25 00 53]
0x025E54:  bcs      0x025ed6                                 ; [58 50 00 7E]
0x025E58:  cmp.w    #0x0053, r5                              ; [79 25 00 53]
0x025E5C:  bhi      0x025ed6                                 ; [42 78]
0x025E5E:  mov.w    #0x0fa0, r0                              ; [79 00 0F A0]
0x025E62:  extu.l   er0                                      ; [17 70]
0x025E64:  divxu.w  r5, er0                                  ; [53 50]
0x025E66:  mov.w    r0, r6                                   ; [0D 06]
0x025E68:  mov.w    #0x0fa0, r1                              ; [79 01 0F A0]
0x025E6C:  extu.l   er1                                      ; [17 71]
0x025E6E:  divxu.w  r0, er1                                  ; [53 01]
0x025E70:  mov.w    r1, e6                                   ; [0D 1E]
0x025E72:  sub.w    r5, r1                                   ; [19 51]
0x025E74:  cmp.w    #0x0002, r1                              ; [79 21 00 02]
0x025E78:  bls      0x025e9a                                 ; [43 20]
0x025E7A:  sub.w    e6, r5                                   ; [19 E5]
0x025E7C:  cmp.w    #0x0002, r5                              ; [79 25 00 02]
0x025E80:  bls      0x025e9a                                 ; [43 18]
0x025E82:  inc.w    #2, e5                                   ; [0B DD]
0x025E84:  mov.w    e6, e1                                   ; [0D E9]
0x025E86:  mov.w    e5, r1                                   ; [0D D1]
0x025E88:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025E8C:  jsr      0x0160de                                 ; [5E 01 60 DE]
0x025E90:  mov.w    #0x0004, r0                              ; [79 00 00 04]
0x025E94:  mov.w    r0, @0x400436                            ; [6B A0 00 40 04 36]
0x025E9A:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025E9E:  mov.b    @(0x2a,er0), r0l                         ; [6E 08 00 2A]
0x025EA2:  btst     #0, r0l                                  ; [73 08]
0x025EA4:  beq      0x025eda                                 ; [47 34]
0x025EA6:  mov.l    @er4, er0                                ; [01 00 69 40]
0x025EAA:  mov.b    @(0x2c,er0), r0l                         ; [6E 08 00 2C]
0x025EAE:  btst     #6, r0l                                  ; [73 68]
0x025EB0:  beq      0x025eda                                 ; [47 28]
0x025EB2:  cmp.w    #0x0001, r6                              ; [79 26 00 01]
0x025EB6:  beq      0x025eda                                 ; [47 22]
0x025EB8:  cmp.w    #0x0002, r6                              ; [79 26 00 02]
0x025EBC:  beq      0x025eda                                 ; [47 1C]
0x025EBE:  cmp.w    #0x0003, r6                              ; [79 26 00 03]
0x025EC2:  beq      0x025eda                                 ; [47 16]
0x025EC4:  cmp.w    #0x0004, r6                              ; [79 26 00 04]
0x025EC8:  beq      0x025eda                                 ; [47 10]
0x025ECA:  cmp.w    #0x0006, r6                              ; [79 26 00 06]
0x025ECE:  beq      0x025eda                                 ; [47 0A]
0x025ED0:  cmp.w    #0x000c, r6                              ; [79 26 00 0C]
0x025ED4:  beq      0x025eda                                 ; [47 04]
0x025ED6:  sub.b    r0l, r0l                                 ; [18 88]
0x025ED8:  bt       0x025ee8                                 ; [40 0E]
0x025EDA:  mov.l    @(0x10,sp), er0                          ; [01 00 6F 70 00 10]
0x025EE0:  mov.w    #0x0002, r1                              ; [79 01 00 02]
0x025EE4:  mov.w    r1, @er0                                 ; [69 81]
0x025EE6:  mov.b    #0x01, r0l                               ; [F8 01]
0x025EE8:  ldm.l    @sp+, er4-er6                            ; [01 20 6D 76]
0x025EEC:  rts                                               ; [54 70]
