; ==== function 0x02BD18 (18 insns) ====
; call/jmp edges:
;   0x02BD1E bcc   -> 0x02BD40  blt 0x02bd40
;   0x02BD2E bcc   -> 0x02BD40  bgt 0x02bd40
;   0x02BD3E jmp   -> 0x02BD46  bt 0x02bd46
;   0x02BD4E call  -> 0x02B8EA  bsr 0x02b8ea
;   0x02BD52 call  -> 0x02B82A  bsr 0x02b82a
0x02BD18:  cmp.l    #0xfffffed4, er0                         ; [7A 20 FF FF FE D4]
0x02BD1E:  blt      0x02bd40                                 ; [4D 20]
0x02BD20:  mov.l    @0x006000, er0                           ; [01 00 6B 20 00 00 60 00]
0x02BD28:  cmp.l    #0x0000012c, er0                         ; [7A 20 00 00 01 2C]
0x02BD2E:  bgt      0x02bd40                                 ; [4E 10]
0x02BD30:  mov.l    @0x006000, er6                           ; [01 00 6B 26 00 00 60 00]
0x02BD38:  add.l    #0x0000014d, er6                         ; [7A 16 00 00 01 4D]
0x02BD3E:  bt       0x02bd46                                 ; [40 06]
0x02BD40:  mov.l    #0x0000014d, er6                         ; [7A 06 00 00 01 4D]
0x02BD46:  sub.b    r1l, r1l                                 ; [18 99]
0x02BD48:  mov.w    #0x0064, e0                              ; [79 08 00 64]
0x02BD4C:  mov.w    r6, r0                                   ; [0D 60]
0x02BD4E:  bsr      0x02b8ea                                 ; [5C 00 FB 98]
0x02BD52:  bsr      0x02b82a                                 ; [5C 00 FA D4]
0x02BD56:  mov.w    #0x00e2, r0                              ; [79 00 00 E2]
0x02BD5A:  mov.w    r0, @0x4202e0                            ; [6B A0 00 42 02 E0]
0x02BD60:  mov.l    @sp+, er6                                ; [01 00 6D 76]
0x02BD64:  rts                                               ; [54 70]
