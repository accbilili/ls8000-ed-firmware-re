; ==== function 0x013994 (78 insns) ====
; call/jmp edges:
;   0x0139A6 call  -> 0x0146EA  bsr 0x0146ea
;   0x0139B0 call  -> 0x0152B0  jsr 0x0152b0
;   0x0139B6 call  -> 0x015300  jsr 0x015300
;   0x0139BE call  -> 0x01380C  bsr 0x01380c
;   0x0139C2 call  -> 0x01528C  jsr 0x01528c
;   0x0139DA jmp   -> 0x013A8A  jmp 0x013a8a
;   0x0139EE bcc   -> 0x013A4A  bne 0x013a4a
;   0x0139F2 bcc   -> 0x013A02  beq 0x013a02
;   0x0139F6 bcc   -> 0x013A10  beq 0x013a10
;   0x0139FA bcc   -> 0x013A04  beq 0x013a04
;   0x0139FE bcc   -> 0x013A10  beq 0x013a10
;   0x013A00 jmp   -> 0x013A4A  bt 0x013a4a
;   0x013A02 jmp   -> 0x013A4C  bt 0x013a4c
;   0x013A08 call  -> 0x013840  bsr 0x013840
;   0x013A0E jmp   -> 0x013A8E  bt 0x013a8e
;   0x013A10 call  -> 0x01470E  bsr 0x01470e
;   0x013A16 bcc   -> 0x013A2C  beq 0x013a2c
;   0x013A2C call  -> 0x015350  jsr 0x015350
;   0x013A42 call  -> 0x013840  bsr 0x013840
;   0x013A48 jmp   -> 0x013A8E  bt 0x013a8e
;   0x013A4A jmp   -> 0x013A4C  bt 0x013a4c
;   0x013A5C bcc   -> 0x013A80  bcc 0x013a80
;   0x013A5E call  -> 0x01517C  jsr 0x01517c
;   0x013A62 call  -> 0x015350  jsr 0x015350
;   0x013A78 call  -> 0x013840  bsr 0x013840
;   0x013A7E jmp   -> 0x013A8E  bt 0x013a8e
;   0x013A8A jmp   -> 0x0139DE  jmp 0x0139de
0x013994:  mov.l    er6, @-sp                                ; [01 00 6D F6]
0x013998:  mov.l    sp, er6                                  ; [0F F6]
0x01399A:  stm.l    er4-er5, @-sp                            ; [01 10 6D F4]
0x01399E:  subs.l   #4, sp                                   ; [1B 97]
0x0139A0:  subs.l   #4, sp                                   ; [1B 97]
0x0139A2:  mov.l    er0, er5                                 ; [0F 85]
0x0139A4:  mov.l    er1, er4                                 ; [0F 94]
0x0139A6:  bsr      0x0146ea                                 ; [5C 00 0D 40]
0x0139AA:  mov.l    #0x00000001, er0                         ; [7A 00 00 00 00 01]
0x0139B0:  jsr      0x0152b0                                 ; [5E 01 52 B0]
0x0139B4:  mov.l    er4, er0                                 ; [0F C0]
0x0139B6:  jsr      0x015300                                 ; [5E 01 53 00]
0x0139BA:  mov.l    er4, er1                                 ; [0F C1]
0x0139BC:  mov.l    er5, er0                                 ; [0F D0]
0x0139BE:  bsr      0x01380c                                 ; [5C 00 FE 4A]
0x0139C2:  jsr      0x01528c                                 ; [5E 01 52 8C]
0x0139C6:  mov.l    @0x4003f6, er0                           ; [01 00 6B 20 00 40 03 F6]
0x0139CE:  add.l    #0x000927c0, er0                         ; [7A 10 00 09 27 C0]
0x0139D4:  mov.l    er0, @(0xfff0,er6)                       ; [01 00 6F E0 FF F0]
0x0139DA:  jmp      0x013a8a                                 ; [5A 01 3A 8A]
0x0139DE:  bset     #4, @0xffff2e                            ; [6A 38 00 FF FF 2E 70 40]
0x0139E6:  mov.w    @0x420748, r0                            ; [6B 20 00 42 07 48]
0x0139EC:  mov.b    r0h, r0h                                 ; [0C 00]
0x0139EE:  bne      0x013a4a                                 ; [46 5A]
0x0139F0:  cmp.b    #0x03, r0l                               ; [A8 03]
0x0139F2:  beq      0x013a02                                 ; [47 0E]
0x0139F4:  cmp.b    #0x04, r0l                               ; [A8 04]
0x0139F6:  beq      0x013a10                                 ; [47 18]
0x0139F8:  cmp.b    #0x05, r0l                               ; [A8 05]
0x0139FA:  beq      0x013a04                                 ; [47 08]
0x0139FC:  cmp.b    #0x06, r0l                               ; [A8 06]
0x0139FE:  beq      0x013a10                                 ; [47 10]
0x013A00:  bt       0x013a4a                                 ; [40 48]
0x013A02:  bt       0x013a4c                                 ; [40 48]
0x013A04:  mov.l    er4, er1                                 ; [0F C1]
0x013A06:  mov.l    er5, er0                                 ; [0F D0]
0x013A08:  bsr      0x013840                                 ; [5C 00 FE 34]
0x013A0C:  mov.l    er4, er0                                 ; [0F C0]
0x013A0E:  bt       0x013a8e                                 ; [40 7E]
0x013A10:  bsr      0x01470e                                 ; [5C 00 0C FA]
0x013A14:  mov.b    r0l, r0l                                 ; [0C 88]
0x013A16:  beq      0x013a2c                                 ; [47 14]
0x013A18:  sub.l    er0, er0                                 ; [1A 80]
0x013A1A:  mov.l    er0, @0x40042e                           ; [01 00 6B A0 00 40 04 2E]
0x013A22:  mov.w    #0x006f, r0                              ; [79 00 00 6F]
0x013A26:  mov.w    r0, @0x400436                            ; [6B A0 00 40 04 36]
0x013A2C:  jsr      0x015350                                 ; [5E 01 53 50]
0x013A30:  mov.l    er0, @(0xfff4,er6)                       ; [01 00 6F E0 FF F4]
0x013A36:  mov.l    @(0xfff4,er6), er0                       ; [01 00 6F 60 FF F4]
0x013A3C:  sub.l    er0, er4                                 ; [1A 84]
0x013A3E:  mov.l    er4, er1                                 ; [0F C1]
0x013A40:  mov.l    er5, er0                                 ; [0F D0]
0x013A42:  bsr      0x013840                                 ; [5C 00 FD FA]
0x013A46:  mov.l    er4, er0                                 ; [0F C0]
0x013A48:  bt       0x013a8e                                 ; [40 44]
0x013A4A:  bt       0x013a4c                                 ; [40 00]
0x013A4C:  mov.l    @(0xfff0,er6), er0                       ; [01 00 6F 60 FF F0]
0x013A52:  mov.l    @0x4003f6, er1                           ; [01 00 6B 21 00 40 03 F6]
0x013A5A:  cmp.l    er1, er0                                 ; [1F 90]
0x013A5C:  bcc      0x013a80                                 ; [44 22]
0x013A5E:  jsr      0x01517c                                 ; [5E 01 51 7C]
0x013A62:  jsr      0x015350                                 ; [5E 01 53 50]
0x013A66:  mov.l    er0, @(0xfff4,er6)                       ; [01 00 6F E0 FF F4]
0x013A6C:  mov.l    @(0xfff4,er6), er0                       ; [01 00 6F 60 FF F4]
0x013A72:  sub.l    er0, er4                                 ; [1A 84]
0x013A74:  mov.l    er4, er1                                 ; [0F C1]
0x013A76:  mov.l    er5, er0                                 ; [0F D0]
0x013A78:  bsr      0x013840                                 ; [5C 00 FD C4]
0x013A7C:  mov.l    er4, er0                                 ; [0F C0]
0x013A7E:  bt       0x013a8e                                 ; [40 0E]
0x013A80:  mov.w    #0x5a00, r0                              ; [79 00 5A 00]
0x013A84:  mov.w    r0, @0xffffbc                            ; [6B A0 00 FF FF BC]
0x013A8A:  jmp      0x0139de                                 ; [5A 01 39 DE]
0x013A8E:  adds.l   #4, sp                                   ; [0B 97]
0x013A90:  adds.l   #4, sp                                   ; [0B 97]
0x013A92:  ldm.l    @sp+, er4-er5                            ; [01 10 6D 75]
0x013A96:  mov.l    @sp+, er6                                ; [01 00 6D 76]
0x013A9A:  rts                                               ; [54 70]
