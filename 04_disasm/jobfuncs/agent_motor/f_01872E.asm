0x01872E  mov.l     er2, @-sp
0x018732  mov.w     e1, e1
0x018734  bne       0x018746
0x018736  mov.w     e0, r2
0x018738  extu.l    er2
0x01873A  divxu.w   r1, er2
0x01873C  mov.w     e2, e0
0x01873E  divxu.w   r1, er0
0x018740  mov.w     e0, r1
0x018742  mov.w     r2, e0
0x018744  bt        0x018764
0x018746  mov.l     er1, er2
0x018748  mov.w     e0, r1
0x01874A  extu.l    er1
0x01874C  mov.w     #0x0010, e0
0x018750  rotxl.w   r0
0x018752  rotxl.l   er1
0x018754  sub.l     er2, er1
0x018756  bcc       0x01875a
0x018758  add.l     er2, er1
0x01875A  dec.w     #1, e0
0x01875C  bne       0x018750
0x01875E  rotxl.w   r0
0x018760  not.w     r0
0x018762  extu.l    er0
0x018764  mov.l     @sp+, er2
0x018768  rts       
