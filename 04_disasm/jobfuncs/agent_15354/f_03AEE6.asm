; ==== function 0x03AEE6 (408 insns) ====
; call/jmp edges:
;   0x03AEEA bcc   -> 0x03AED2  bls 0x03aed2
;   0x03AEEC jmp   -> 0x03AFBE  jmp 0x03afbe
;   0x03AEF8 bcc   -> 0x03AF02  beq 0x03af02
;   0x03AEFA call  -> 0x02B7F6  jsr 0x02b7f6
;   0x03AEFE jmp   -> 0x03B4E2  jmp 0x03b4e2
;   0x03AF0A call  -> 0x02D700  jsr 0x02d700
;   0x03AF16 bcc   -> 0x03AF30  blt 0x03af30
;   0x03AF2C call  -> 0x02B8EA  jsr 0x02b8ea
;   0x03AF38 call  -> 0x03B4F4  bsr 0x03b4f4
;   0x03AF5A bcc   -> 0x03AF72  bls 0x03af72
;   0x03AF80 bcc   -> 0x03AF8E  bcc 0x03af8e
;   0x03AF98 bcc   -> 0x03AFA2  bls 0x03afa2
;   0x03AFAC bcc   -> 0x03AFB6  bcc 0x03afb6
;   0x03AFBA call  -> 0x02B82A  jsr 0x02b82a
;   0x03AFC0 bcc   -> 0x03AEF0  bge 0x03aef0
;   0x03AFC4 call  -> 0x02B7F6  jsr 0x02b7f6
;   0x03AFCC bcc   -> 0x03B3BE  bcs 0x03b3be
;   0x03AFD4 bcc   -> 0x03B3BE  bhi 0x03b3be
;   0x03AFFE bcc   -> 0x03B3BE  beq 0x03b3be
;   0x03B028 bcc   -> 0x03B1FA  bcc 0x03b1fa
;   0x03B040 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B05A call  -> 0x018E9E  jsr 0x018e9e
;   0x03B066 call  -> 0x0185EE  jsr 0x0185ee
;   0x03B076 call  -> 0x018948  jsr 0x018948
;   0x03B07C bcc   -> 0x03B08C  beq 0x03b08c
;   0x03B08A jmp   -> 0x03B098  bt 0x03b098
;   0x03B098 call  -> 0x0181B2  jsr 0x0181b2
;   0x03B0B6 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B0D0 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B0DA call  -> 0x0181BC  jsr 0x0181bc
;   0x03B0E4 call  -> 0x0185EE  jsr 0x0185ee
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
;   0x03B20E call  -> 0x018E9E  jsr 0x018e9e
;   0x03B228 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B234 call  -> 0x0185EE  jsr 0x0185ee
;   0x03B244 call  -> 0x018948  jsr 0x018948
;   0x03B24A bcc   -> 0x03B25A  beq 0x03b25a
;   0x03B258 jmp   -> 0x03B266  bt 0x03b266
;   0x03B266 call  -> 0x0181B2  jsr 0x0181b2
;   0x03B284 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B29E call  -> 0x018E9E  jsr 0x018e9e
;   0x03B2A8 call  -> 0x0181BC  jsr 0x0181bc
;   0x03B2B2 call  -> 0x0185EE  jsr 0x0185ee
;   0x03B2CA call  -> 0x018E9E  jsr 0x018e9e
;   0x03B2D4 call  -> 0x0185EE  jsr 0x0185ee
;   0x03B2E0 call  -> 0x018948  jsr 0x018948
;   0x03B2E6 bcc   -> 0x03B2F2  beq 0x03b2f2
;   0x03B2F0 jmp   -> 0x03B2FA  bt 0x03b2fa
;   0x03B2FA call  -> 0x0181B2  jsr 0x0181b2
;   0x03B310 call  -> 0x018E9E  jsr 0x018e9e
;   0x03B32C call  -> 0x018E9E  jsr 0x018e9e
;   0x03B338 call  -> 0x0185EE  jsr 0x0185ee
;   0x03B348 call  -> 0x018948  jsr 0x018948
;   0x03B34E bcc   -> 0x03B35E  beq 0x03b35e
;   0x03B35C jmp   -> 0x03B36A  bt 0x03b36a
;   0x03B36A call  -> 0x0181B2  jsr 0x0181b2
;   0x03B37C call  -> 0x018948  jsr 0x018948
;   0x03B382 bcc   -> 0x03B398  beq 0x03b398
;   0x03B38C call  -> 0x018948  jsr 0x018948
;   0x03B392 bcc   -> 0x03B398  beq 0x03b398
;   0x03B396 jmp   -> 0x03B3BE  bt 0x03b3be
;   0x03B3A4 call  -> 0x018948  jsr 0x018948
;   0x03B3AA bcc   -> 0x03B3BE  beq 0x03b3be
;   0x03B3B4 call  -> 0x018948  jsr 0x018948
;   0x03B3BA bcc   -> 0x03B3BE  beq 0x03b3be
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
0x03AED2:  mov.w    r2, r0                                   ; [0D 20]
0x03AED4:  extu.l   er0                                      ; [17 70]
0x03AED6:  shll.l   #2, er0                                  ; [10 70]
0x03AED8:  add.l    er5, er0                                 ; [0A D0]
0x03AEDA:  sub.l    er1, er1                                 ; [1A 91]
0x03AEDC:  mov.l    er1, @er0                                ; [01 00 69 81]
0x03AEE0:  mov.w    r2, r0                                   ; [0D 20]
0x03AEE2:  inc.w    #1, r0                                   ; [0B 50]
0x03AEE4:  mov.w    r0, r2                                   ; [0D 02]
0x03AEE6:  cmp.w    #0x01c2, r0                              ; [79 20 01 C2]
0x03AEEA:  bls      0x03aed2                                 ; [43 E6]
0x03AEEC:  jmp      0x03afbe                                 ; [5A 03 AF BE]
0x03AEF0:  btst     #7, @0x400400                            ; [6A 30 00 40 04 00 73 70]
0x03AEF8:  beq      0x03af02                                 ; [47 08]
0x03AEFA:  jsr      0x02b7f6                                 ; [5E 02 B7 F6]
0x03AEFE:  jmp      0x03b4e2                                 ; [5A 03 B4 E2]
0x03AF02:  mov.l    #0x00420286, er1                         ; [7A 01 00 42 02 86]
0x03AF08:  mov.b    #0x01, r0l                               ; [F8 01]
0x03AF0A:  jsr      0x02d700                                 ; [5E 02 D7 00]
0x03AF0E:  mov.w    e6, r0                                   ; [0D E0]
0x03AF10:  sub.w    #0x0004, r0                              ; [79 30 00 04]
0x03AF14:  mov.w    r0, r0                                   ; [0D 00]
0x03AF16:  blt      0x03af30                                 ; [4D 18]
0x03AF18:  mov.b    #0x01, r0l                               ; [F8 01]
0x03AF1A:  mov.b    r0l, @0x4202e9                           ; [6A A8 00 42 02 E9]
0x03AF20:  mov.w    e6, r0                                   ; [0D E0]
0x03AF22:  sub.w    #0x0004, r0                              ; [79 30 00 04]
0x03AF26:  mov.b    #0x01, r1l                               ; [F9 01]
0x03AF28:  mov.w    #0x0014, e0                              ; [79 08 00 14]
0x03AF2C:  jsr      0x02b8ea                                 ; [5E 02 B8 EA]
0x03AF30:  mov.b    @0x4491d5, r0h                           ; [6A 20 00 44 91 D5]
0x03AF36:  sub.b    r0l, r0l                                 ; [18 88]
0x03AF38:  bsr      0x03b4f4                                 ; [5C 00 05 B8]
0x03AF3C:  mov.w    e6, r0                                   ; [0D E0]
0x03AF3E:  exts.l   er0                                      ; [17 F0]
0x03AF40:  shll.l   #2, er0                                  ; [10 70]
0x03AF42:  add.l    er5, er0                                 ; [0A D0]
0x03AF44:  mov.l    @er4, er1                                ; [01 00 69 41]
0x03AF48:  mov.l    er1, @er0                                ; [01 00 69 81]
0x03AF4C:  mov.l    @er4, er0                                ; [01 00 69 40]
0x03AF50:  mov.l    @0x4491dc, er1                           ; [01 00 6B 21 00 44 91 DC]
0x03AF58:  cmp.l    er1, er0                                 ; [1F 90]
0x03AF5A:  bls      0x03af72                                 ; [43 16]
0x03AF5C:  mov.l    @er4, er0                                ; [01 00 69 40]
0x03AF60:  mov.l    er0, @0x4491dc                           ; [01 00 6B A0 00 44 91 DC]
0x03AF68:  mov.w    @er3, r0                                 ; [69 30]
0x03AF6A:  mov.w    r0, @0x4491d2                            ; [6B A0 00 44 91 D2]
0x03AF70:  mov.w    e6, r6                                   ; [0D E6]
0x03AF72:  mov.l    @er4, er0                                ; [01 00 69 40]
0x03AF76:  mov.l    @0x4491e0, er1                           ; [01 00 6B 21 00 44 91 E0]
0x03AF7E:  cmp.l    er1, er0                                 ; [1F 90]
0x03AF80:  bcc      0x03af8e                                 ; [44 0C]
0x03AF82:  mov.l    @er4, er0                                ; [01 00 69 40]
0x03AF86:  mov.l    er0, @0x4491e0                           ; [01 00 6B A0 00 44 91 E0]
0x03AF8E:  mov.w    @er3, r0                                 ; [69 30]
0x03AF90:  mov.w    @0x449a2c, r1                            ; [6B 21 00 44 9A 2C]
0x03AF96:  cmp.w    r1, r0                                   ; [1D 10]
0x03AF98:  bls      0x03afa2                                 ; [43 08]
0x03AF9A:  mov.w    @er3, r0                                 ; [69 30]
0x03AF9C:  mov.w    r0, @0x449a2c                            ; [6B A0 00 44 9A 2C]
0x03AFA2:  mov.w    @er3, r0                                 ; [69 30]
0x03AFA4:  mov.w    @0x449a2e, r1                            ; [6B 21 00 44 9A 2E]
0x03AFAA:  cmp.w    r1, r0                                   ; [1D 10]
0x03AFAC:  bcc      0x03afb6                                 ; [44 08]
0x03AFAE:  mov.w    @er3, r0                                 ; [69 30]
0x03AFB0:  mov.w    r0, @0x449a2e                            ; [6B A0 00 44 9A 2E]
0x03AFB6:  sub.w    #0x0004, e6                              ; [79 3E 00 04]
0x03AFBA:  jsr      0x02b82a                                 ; [5E 02 B8 2A]
0x03AFBE:  mov.w    e6, e6                                   ; [0D EE]
0x03AFC0:  bge      0x03aef0                                 ; [58 C0 FF 2C]
0x03AFC4:  jsr      0x02b7f6                                 ; [5E 02 B7 F6]
0x03AFC8:  cmp.w    #0x0008, r6                              ; [79 26 00 08]
0x03AFCC:  bcs      0x03b3be                                 ; [58 50 03 EE]
0x03AFD0:  cmp.w    #0x01ba, r6                              ; [79 26 01 BA]
0x03AFD4:  bhi      0x03b3be                                 ; [58 20 03 E6]
0x03AFD8:  mov.w    r6, r0                                   ; [0D 60]
0x03AFDA:  extu.l   er0                                      ; [17 70]
0x03AFDC:  shll.l   #2, er0                                  ; [10 70]
0x03AFDE:  add.l    er5, er0                                 ; [0A D0]
0x03AFE0:  mov.l    er0, @(0xe,sp)                           ; [01 00 6F F0 00 0E]
0x03AFE6:  mov.l    @(0xe,sp), er1                           ; [01 00 6F 71 00 0E]
0x03AFEC:  sub.l    #0x00000010, er1                         ; [7A 31 00 00 00 10]
0x03AFF2:  mov.l    @(0x10,er0), er0                         ; [01 00 6F 00 00 10]
0x03AFF8:  mov.l    @er1, er1                                ; [01 00 69 11]
0x03AFFC:  cmp.l    er1, er0                                 ; [1F 90]
0x03AFFE:  beq      0x03b3be                                 ; [58 70 03 BC]
0x03B002:  mov.w    r6, r0                                   ; [0D 60]
0x03B004:  extu.l   er0                                      ; [17 70]
0x03B006:  shll.l   #2, er0                                  ; [10 70]
0x03B008:  add.l    er5, er0                                 ; [0A D0]
0x03B00A:  mov.l    er0, @(0xe,sp)                           ; [01 00 6F F0 00 0E]
0x03B010:  mov.l    @(0xe,sp), er1                           ; [01 00 6F 71 00 0E]
0x03B016:  sub.l    #0x00000010, er1                         ; [7A 31 00 00 00 10]
0x03B01C:  mov.l    @(0x10,er0), er0                         ; [01 00 6F 00 00 10]
0x03B022:  mov.l    @er1, er1                                ; [01 00 69 11]
0x03B026:  cmp.l    er1, er0                                 ; [1F 90]
0x03B028:  bcc      0x03b1fa                                 ; [58 40 01 CE]
0x03B02C:  mov.w    r6, r0                                   ; [0D 60]
0x03B02E:  extu.l   er0                                      ; [17 70]
0x03B030:  shll.l   #2, er0                                  ; [10 70]
0x03B032:  add.l    er5, er0                                 ; [0A D0]
0x03B034:  mov.l    er0, @(0xe,sp)                           ; [01 00 6F F0 00 0E]
0x03B03A:  mov.l    @(0xfff0,er0), er0                       ; [01 00 6F 00 FF F0]
0x03B040:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B044:  mov.l    @(0xe,sp), er1                           ; [01 00 6F 71 00 0E]
0x03B04A:  add.l    #0x00000010, er1                         ; [7A 11 00 00 00 10]
0x03B050:  mov.l    er0, @(0x4,sp)                           ; [01 00 6F F0 00 04]
0x03B056:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B05A:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B05E:  mov.l    er0, er1                                 ; [0F 81]
0x03B060:  mov.l    @(0x4,sp), er0                           ; [01 00 6F 70 00 04]
0x03B066:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B06A:  mov.l    er0, @(0x14,sp)                          ; [01 00 6F F0 00 14]
0x03B070:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B076:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B07A:  mov.w    r0, r0                                   ; [0D 00]
0x03B07C:  beq      0x03b08c                                 ; [47 0E]
0x03B07E:  mov.l    #0x3f800000, er0                         ; [7A 00 3F 80 00 00]
0x03B084:  mov.l    @(0x14,sp), er1                          ; [01 00 6F 71 00 14]
0x03B08A:  bt       0x03b098                                 ; [40 0C]
0x03B08C:  mov.l    @(0x14,sp), er0                          ; [01 00 6F 70 00 14]
0x03B092:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B098:  jsr      0x0181b2                                 ; [5E 01 81 B2]
0x03B09C:  mov.l    er0, @(0x14,sp)                          ; [01 00 6F F0 00 14]
0x03B0A2:  mov.w    r6, r0                                   ; [0D 60]
0x03B0A4:  extu.l   er0                                      ; [17 70]
0x03B0A6:  shll.l   #2, er0                                  ; [10 70]
0x03B0A8:  add.l    er5, er0                                 ; [0A D0]
0x03B0AA:  mov.l    er0, @(0xe,sp)                           ; [01 00 6F F0 00 0E]
0x03B0B0:  mov.l    @(0xfff0,er0), er0                       ; [01 00 6F 00 FF F0]
0x03B0B6:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B0BA:  mov.w    r6, r1                                   ; [0D 61]
0x03B0BC:  sub.w    #0x0008, r1                              ; [79 31 00 08]
0x03B0C0:  extu.l   er1                                      ; [17 71]
0x03B0C2:  shll.l   #2, er1                                  ; [10 71]
0x03B0C4:  add.l    er5, er1                                 ; [0A D1]
0x03B0C6:  mov.l    er0, @(0x4,sp)                           ; [01 00 6F F0 00 04]
0x03B0CC:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B0D0:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B0D4:  mov.l    @(0x4,sp), er1                           ; [01 00 6F 71 00 04]
0x03B0DA:  jsr      0x0181bc                                 ; [5E 01 81 BC]
0x03B0DE:  mov.l    #0x40000000, er1                         ; [7A 01 40 00 00 00]
0x03B0E4:  jsr      0x0185ee                                 ; [5E 01 85 EE]
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
0x03B1FA:  mov.w    r6, r0                                   ; [0D 60]
0x03B1FC:  extu.l   er0                                      ; [17 70]
0x03B1FE:  shll.l   #2, er0                                  ; [10 70]
0x03B200:  add.l    er5, er0                                 ; [0A D0]
0x03B202:  mov.l    er0, @(0xe,sp)                           ; [01 00 6F F0 00 0E]
0x03B208:  mov.l    @(0x10,er0), er0                         ; [01 00 6F 00 00 10]
0x03B20E:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B212:  mov.l    @(0xe,sp), er1                           ; [01 00 6F 71 00 0E]
0x03B218:  sub.l    #0x00000010, er1                         ; [7A 31 00 00 00 10]
0x03B21E:  mov.l    er0, @(0x4,sp)                           ; [01 00 6F F0 00 04]
0x03B224:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B228:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B22C:  mov.l    er0, er1                                 ; [0F 81]
0x03B22E:  mov.l    @(0x4,sp), er0                           ; [01 00 6F 70 00 04]
0x03B234:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B238:  mov.l    er0, @(0x14,sp)                          ; [01 00 6F F0 00 14]
0x03B23E:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B244:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B248:  mov.w    r0, r0                                   ; [0D 00]
0x03B24A:  beq      0x03b25a                                 ; [47 0E]
0x03B24C:  mov.l    #0x3f800000, er0                         ; [7A 00 3F 80 00 00]
0x03B252:  mov.l    @(0x14,sp), er1                          ; [01 00 6F 71 00 14]
0x03B258:  bt       0x03b266                                 ; [40 0C]
0x03B25A:  mov.l    @(0x14,sp), er0                          ; [01 00 6F 70 00 14]
0x03B260:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B266:  jsr      0x0181b2                                 ; [5E 01 81 B2]
0x03B26A:  mov.l    er0, @(0x14,sp)                          ; [01 00 6F F0 00 14]
0x03B270:  mov.w    r6, r0                                   ; [0D 60]
0x03B272:  extu.l   er0                                      ; [17 70]
0x03B274:  shll.l   #2, er0                                  ; [10 70]
0x03B276:  add.l    er5, er0                                 ; [0A D0]
0x03B278:  mov.l    er0, @(0xe,sp)                           ; [01 00 6F F0 00 0E]
0x03B27E:  mov.l    @(0x10,er0), er0                         ; [01 00 6F 00 00 10]
0x03B284:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B288:  mov.w    r6, r1                                   ; [0D 61]
0x03B28A:  add.w    #0x0008, r1                              ; [79 11 00 08]
0x03B28E:  extu.l   er1                                      ; [17 71]
0x03B290:  shll.l   #2, er1                                  ; [10 71]
0x03B292:  add.l    er5, er1                                 ; [0A D1]
0x03B294:  mov.l    er0, @(0x4,sp)                           ; [01 00 6F F0 00 04]
0x03B29A:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B29E:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B2A2:  mov.l    @(0x4,sp), er1                           ; [01 00 6F 71 00 04]
0x03B2A8:  jsr      0x0181bc                                 ; [5E 01 81 BC]
0x03B2AC:  mov.l    #0x40000000, er1                         ; [7A 01 40 00 00 00]
0x03B2B2:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B2B6:  mov.l    @(0xe,sp), er1                           ; [01 00 6F 71 00 0E]
0x03B2BC:  sub.l    #0x00000010, er1                         ; [7A 31 00 00 00 10]
0x03B2C2:  mov.l    er0, @sp                                 ; [01 00 69 F0]
0x03B2C6:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B2CA:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B2CE:  mov.l    er0, er1                                 ; [0F 81]
0x03B2D0:  mov.l    @sp, er0                                 ; [01 00 69 70]
0x03B2D4:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B2D8:  mov.l    er0, er2                                 ; [0F 82]
0x03B2DA:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B2E0:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B2E4:  mov.w    r0, r0                                   ; [0D 00]
0x03B2E6:  beq      0x03b2f2                                 ; [47 0A]
0x03B2E8:  mov.l    #0x3f800000, er0                         ; [7A 00 3F 80 00 00]
0x03B2EE:  mov.l    er2, er1                                 ; [0F A1]
0x03B2F0:  bt       0x03b2fa                                 ; [40 08]
0x03B2F2:  mov.l    er2, er0                                 ; [0F A0]
0x03B2F4:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B2FA:  jsr      0x0181b2                                 ; [5E 01 81 B2]
0x03B2FE:  mov.l    er0, er2                                 ; [0F 82]
0x03B300:  mov.w    r6, r1                                   ; [0D 61]
0x03B302:  add.w    #0x0008, r1                              ; [79 11 00 08]
0x03B306:  extu.l   er1                                      ; [17 71]
0x03B308:  shll.l   #2, er1                                  ; [10 71]
0x03B30A:  add.l    er5, er1                                 ; [0A D1]
0x03B30C:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B310:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B314:  mov.w    r6, r1                                   ; [0D 61]
0x03B316:  extu.l   er1                                      ; [17 71]
0x03B318:  shll.l   #2, er1                                  ; [10 71]
0x03B31A:  add.l    er5, er1                                 ; [0A D1]
0x03B31C:  sub.l    #0x00000010, er1                         ; [7A 31 00 00 00 10]
0x03B322:  mov.l    er0, @(0x4,sp)                           ; [01 00 6F F0 00 04]
0x03B328:  mov.l    @er1, er0                                ; [01 00 69 10]
0x03B32C:  jsr      0x018e9e                                 ; [5E 01 8E 9E]
0x03B330:  mov.l    er0, er1                                 ; [0F 81]
0x03B332:  mov.l    @(0x4,sp), er0                           ; [01 00 6F 70 00 04]
0x03B338:  jsr      0x0185ee                                 ; [5E 01 85 EE]
0x03B33C:  mov.l    er0, @(0x18,sp)                          ; [01 00 6F F0 00 18]
0x03B342:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B348:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B34C:  mov.w    r0, r0                                   ; [0D 00]
0x03B34E:  beq      0x03b35e                                 ; [47 0E]
0x03B350:  mov.l    #0x3f800000, er0                         ; [7A 00 3F 80 00 00]
0x03B356:  mov.l    @(0x18,sp), er1                          ; [01 00 6F 71 00 18]
0x03B35C:  bt       0x03b36a                                 ; [40 0C]
0x03B35E:  mov.l    @(0x18,sp), er0                          ; [01 00 6F 70 00 18]
0x03B364:  mov.l    #0x3f800000, er1                         ; [7A 01 3F 80 00 00]
0x03B36A:  jsr      0x0181b2                                 ; [5E 01 81 B2]
0x03B36E:  mov.l    er0, @(0x18,sp)                          ; [01 00 6F F0 00 18]
0x03B374:  mov.l    er2, er0                                 ; [0F A0]
0x03B376:  mov.l    @(0x14,sp), er1                          ; [01 00 6F 71 00 14]
0x03B37C:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B380:  mov.w    r0, r0                                   ; [0D 00]
0x03B382:  beq      0x03b398                                 ; [47 14]
0x03B384:  mov.l    er2, er0                                 ; [0F A0]
0x03B386:  mov.l    @(0x18,sp), er1                          ; [01 00 6F 71 00 18]
0x03B38C:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B390:  mov.w    r0, r0                                   ; [0D 00]
0x03B392:  beq      0x03b398                                 ; [47 04]
0x03B394:  inc.w    #1, r6                                   ; [0B 56]
0x03B396:  bt       0x03b3be                                 ; [40 26]
0x03B398:  mov.l    @(0x18,sp), er0                          ; [01 00 6F 70 00 18]
0x03B39E:  mov.l    @(0x14,sp), er1                          ; [01 00 6F 71 00 14]
0x03B3A4:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B3A8:  mov.w    r0, r0                                   ; [0D 00]
0x03B3AA:  beq      0x03b3be                                 ; [47 12]
0x03B3AC:  mov.l    @(0x18,sp), er0                          ; [01 00 6F 70 00 18]
0x03B3B2:  mov.l    er2, er1                                 ; [0F A1]
0x03B3B4:  jsr      0x018948                                 ; [5E 01 89 48]
0x03B3B8:  mov.w    r0, r0                                   ; [0D 00]
0x03B3BA:  beq      0x03b3be                                 ; [47 02]
0x03B3BC:  inc.w    #2, r6                                   ; [0B D6]
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
