# fn 0x018860 (helper_y) : 43 insns
0x018860  mov.l     er1, @-sp
0x018864  mov.w     e0, e1
0x018866  shll.l    er0
0x018868  mov.w     e0, r1
0x01886A  mov.b     r1h, r1l
0x01886C  sub.b     r1h, r1h
0x01886E  shll.l    #2, er0
0x018870  shll.l    #2, er0
0x018872  shll.l    #2, er0
0x018874  shll.l    #2, er0
0x018876  sub.w     #0x007f, r1
0x01887A  bmi       0x0188be
0x01887C  cmp.w     #0x0036, r1
0x018880  bgt       0x0188be
0x018882  shlr.l    er0
0x018884  or.w      #0x8000, e0
0x018888  add.w     #0xffe1, r1
0x01888C  bmi       0x0188a2
0x01888E  beq       0x0188b2
0x018890  btst      #0, r1l
0x018892  beq       0x01889a
0x018894  shll.l    er0
0x018896  dec.w     #1, r1
0x018898  ble       0x0188b2
0x01889A  shll.l    #2, er0
0x01889C  dec.w     #2, r1
0x01889E  bgt       0x01889a
0x0188A0  bt        0x0188b2
0x0188A2  btst      #0, r1l
0x0188A4  beq       0x0188ac
0x0188A6  shlr.l    er0
0x0188A8  inc.w     #1, r1
0x0188AA  bpl       0x0188b2
0x0188AC  shlr.l    #2, er0
0x0188AE  inc.w     #2, r1
0x0188B0  bmi       0x0188a2
0x0188B2  mov.w     e1, e1
0x0188B4  bpl       0x0188b8
0x0188B6  neg.l     er0
0x0188B8  mov.l     @sp+, er1
0x0188BC  rts       
0x0188BE  sub.l     er0, er0
0x0188C0  bt        0x0188b8
