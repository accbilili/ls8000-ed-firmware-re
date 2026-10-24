# fn 0x018E9E (helper_div32b) : 29 insns
0x018E9E  mov.l     er0, er0
0x018EA0  beq       0x018edc
0x018EA2  mov.w     r2, @-sp
0x018EA4  mov.w     r1, @-sp
0x018EA6  mov.b     #0x9f, r1l
0x018EA8  dec.b     #1, r1l
0x018EAA  shll.l    er0
0x018EAC  bcc       0x018ea8
0x018EAE  rotxr.l   er0
0x018EB0  btst      #7, r0l
0x018EB2  beq       0x018ec8
0x018EB4  mov.w     r0, r2
0x018EB6  and.w     #0x017f, r2
0x018EBA  beq       0x018ec8
0x018EBC  add.l     #0x00000100, er0
0x018EC2  bcc       0x018ec8
0x018EC4  rotxr.l   er0
0x018EC6  inc.b     #1, r1l
0x018EC8  shll.l    er0
0x018ECA  mov.w     e0, r2
0x018ECC  mov.b     r0h, r0l
0x018ECE  mov.b     r2l, r0h
0x018ED0  mov.b     r2h, r2l
0x018ED2  mov.b     r1l, r2h
0x018ED4  mov.w     r2, e0
0x018ED6  shlr.l    er0
0x018ED8  mov.w     @sp+, r1
0x018EDA  mov.w     @sp+, r2
0x018EDC  rts       
