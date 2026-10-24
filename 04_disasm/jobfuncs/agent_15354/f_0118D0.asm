; ==== function 0x0118D0 (9 insns) ====
; call/jmp edges:
;   0x0118DE call  -> 0x013994  jsr 0x013994
0x0118D0:  stm.l    er4-er5, @-sp                            ; [01 10 6D F4]
0x0118D4:  mov.l    er0, er5                                 ; [0F 85]
0x0118D6:  mov.w    r1, r4                                   ; [0D 14]
0x0118D8:  extu.l   er4                                      ; [17 74]
0x0118DA:  mov.l    er4, er1                                 ; [0F C1]
0x0118DC:  mov.l    er5, er0                                 ; [0F D0]
0x0118DE:  jsr      0x013994                                 ; [5E 01 39 94]
0x0118E2:  ldm.l    @sp+, er4-er5                            ; [01 10 6D 75]
0x0118E6:  rts                                               ; [54 70]
