; ==== function 0x026E8E (29 insns) ====
; call/jmp edges:
;   0x026E94 bcc   -> 0x026EB6  ble 0x026eb6
;   0x026E9A jmp   -> 0x026EB2  bt 0x026eb2
;   0x026EB4 jmp   -> 0x026EEC  bt 0x026eec
;   0x026EC2 jmp   -> 0x026EDC  bt 0x026edc
;   0x026EEA bcc   -> 0x026EC4  bcs 0x026ec4
0x026E8E:  cmp.l    #0x0000012c, er3                         ; [7A 23 00 00 01 2C]
0x026E94:  ble      0x026eb6                                 ; [4F 20]
0x026E96:  mov.w    #0x0053, r0                              ; [79 00 00 53]
0x026E9A:  bt       0x026eb2                                 ; [40 16]
0x026EB2:  mov.w    r0, @er6                                 ; [69 E0]
0x026EB4:  bt       0x026eec                                 ; [40 36]
0x026EB6:  mov.b    @(0x2,er4), r0l                          ; [6E 48 00 02]
0x026EBA:  mov.b    r0l, @0x400c55                           ; [6A A8 00 40 0C 55]
0x026EC0:  sub.b    r3l, r3l                                 ; [18 BB]
0x026EC2:  bt       0x026edc                                 ; [40 18]
0x026EC4:  mov.b    r3l, r0l                                 ; [0C B8]
0x026EC6:  extu.w   r0                                       ; [17 50]
0x026EC8:  extu.l   er0                                      ; [17 70]
0x026ECA:  mov.l    er0, er2                                 ; [0F 82]
0x026ECC:  mov.l    er2, er1                                 ; [0F A1]
0x026ECE:  add.l    er5, er1                                 ; [0A D1]
0x026ED0:  mov.b    @er1, r1l                                ; [68 19]
0x026ED2:  mov.b    r1l, @(0x400c56,er0)                     ; [78 00 6A A9 00 40 0C 56]
0x026EDA:  inc.b    #1, r3l                                  ; [0A 0B]
0x026EDC:  mov.b    r3l, r0l                                 ; [0C B8]
0x026EDE:  extu.w   r0                                       ; [17 50]
0x026EE0:  extu.l   er0                                      ; [17 70]
0x026EE2:  mov.l    @(0x16,sp), er1                          ; [01 00 6F 71 00 16]
0x026EE8:  cmp.l    er1, er0                                 ; [1F 90]
0x026EEA:  bcs      0x026ec4                                 ; [45 D8]
0x026EEC:  add.l    #0x0000001a, sp                          ; [7A 17 00 00 00 1A]
0x026EF2:  ldm.l    @sp+, er4-er6                            ; [01 20 6D 76]
0x026EF6:  ldm.l    @sp+, er2-er3                            ; [01 10 6D 73]
0x026EFA:  rts                                               ; [54 70]
