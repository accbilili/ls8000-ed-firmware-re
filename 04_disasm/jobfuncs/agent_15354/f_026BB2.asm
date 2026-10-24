; ==== function 0x026BB2 (14 insns) ====
; call/jmp edges:
;   0x026BBC jmp   -> 0x026BD2  bt 0x026bd2
0x026BB2:  mov.b    @(0x5,er6), r0l                          ; [6E 68 00 05]
0x026BB6:  mov.b    r0l, @0x42029e                           ; [6A A8 00 42 02 9E]
0x026BBC:  bt       0x026bd2                                 ; [40 14]
0x026BD2:  mov.b    @er6, r0l                                ; [68 68]
0x026BD4:  extu.w   r0                                       ; [17 50]
0x026BD6:  bset     #6, r0h                                  ; [70 60]
0x026BD8:  mov.w    r0, @0x400400                            ; [6B A0 00 40 04 00]
0x026BDE:  mov.b    #0x01, r0l                               ; [F8 01]
0x026BE0:  mov.b    r0l, @0x4007c8                           ; [6A A8 00 40 07 C8]
0x026BE6:  sub.w    r0, r0                                   ; [19 00]
0x026BE8:  mov.w    r0, @0x400438                            ; [6B A0 00 40 04 38]
0x026BEE:  ldm.l    @sp+, er4-er6                            ; [01 20 6D 76]
0x026BF2:  mov.l    @sp+, er3                                ; [01 00 6D 73]
0x026BF6:  rts                                               ; [54 70]
