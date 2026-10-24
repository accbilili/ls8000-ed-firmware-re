0x026C46  0F C0                mov.l     er4, er0
0x026C48  0B F0                inc.l     #2, er0
0x026C4A  01 00 6F F0 00 16    mov.l     er0, @(0x16,sp)
0x026C50  01 00 6F 70 00 16    mov.l     @(0x16,sp), er0
0x026C56  0C B9                mov.b     r3l, r1l
0x026C58  17 51                extu.w    r1
0x026C5A  17 71                extu.l    er1
0x026C5C  10 31                shll.l    er1
0x026C5E  68 08                mov.b     @er0, r0l
0x026C60  78 10 6A 29 00 03 ED B8 mov.b     @(0x3edb8,er1), r1l
0x026C68  1C 98                cmp.b     r1l, r0l
0x026C6A  46 10                bne       0x026c7c
0x026C6C  1A 80                sub.l     er0, er0
0x026C6E  0C B8                mov.b     r3l, r0l
0x026C70  10 30                shll.l    er0
0x026C72  78 00 6A 23 00 03 ED B9 mov.b     @(0x3edb9,er0), r3h
0x026C7A  40 18                bt        0x026c94
0x026C7C  0C B8                mov.b     r3l, r0l
0x026C7E  17 50                extu.w    r0
0x026C80  17 70                extu.l    er0
0x026C82  10 30                shll.l    er0
0x026C84  78 00 6A 28 00 03 ED B8 mov.b     @(0x3edb8,er0), r0l
0x026C8C  A8 FF                cmp.b     #0xff, r0l
0x026C8E  47 4C                beq       0x026cdc
0x026C90  0A 0B                inc.b     #1, r3l
0x026C92  40 BC                bt        0x026c50
0x026C94  1A 80                sub.l     er0, er0
0x026C96  6E 48 00 06          mov.b     @(0x6,er4), r0l
0x026C9A  0D 08                mov.w     r0, e0
0x026C9C  19 00                sub.w     r0, r0
0x026C9E  1A 91                sub.l     er1, er1
0x026CA0  6E 49 00 07          mov.b     @(0x7,er4), r1l
0x026CA4  10 71                shll.l    #2, er1
0x026CA6  10 71                shll.l    #2, er1
0x026CA8  10 71                shll.l    #2, er1
0x026CAA  10 71                shll.l    #2, er1
0x026CAC  0A 90                add.l     er1, er0
0x026CAE  1A 91                sub.l     er1, er1
0x026CB0  6E 49 00 08          mov.b     @(0x8,er4), r1l
0x026CB4  0A 90                add.l     er1, er0
0x026CB6  01 00 6F F0 00 16    mov.l     er0, @(0x16,sp)
0x026CBC  1A 91                sub.l     er1, er1
0x026CBE  0C 39                mov.b     r3h, r1l
0x026CC0  1F 90                cmp.l     er1, er0
0x026CC2  44 0A                bcc       0x026cce
0x026CC4  79 01 00 50          mov.w     #0x0050, r1
0x026CC8  69 E1                mov.w     r1, @er6
0x026CCA  5A 02 6E EC          jmp       0x026eec
0x026CCE  01 00 6F 70 00 16    mov.l     @(0x16,sp), er0
0x026CD4  7A 20 00 00 00 0D    cmp.l     #0x0000000d, er0
0x026CDA  43 08                bls       0x026ce4
0x026CDC  79 00 00 50          mov.w     #0x0050, r0
0x026CE0  5A 02 6E B2          jmp       0x026eb2
0x026CE4  18 BB                sub.b     r3l, r3l
0x026CE6  0C B8                mov.b     r3l, r0l
0x026CE8  17 50                extu.w    r0
0x026CEA  17 70                extu.l    er0
0x026CEC  0A D0                add.l     er5, er0
0x026CEE  18 99                sub.b     r1l, r1l
0x026CF0  68 89                mov.b     r1l, @er0
0x026CF2  0A 0B                inc.b     #1, r3l
0x026CF4  AB 0D                cmp.b     #0x0d, r3l
0x026CF6  45 EE                bcs       0x026ce6
0x026CF8  01 00 6F 70 00 16    mov.l     @(0x16,sp), er0
0x026CFE  47 10                beq       0x026d10
0x026D00  6F 71 00 18          mov.w     @(0x18,sp), r1
0x026D04  0F D0                mov.l     er5, er0
0x026D06  5E 01 18 D0          jsr       0x0118d0
0x026D0A  69 60                mov.w     @er6, r0
0x026D0C  58 60 01 DC          bne       0x026eec
0x026D10  1A B3                sub.l     er3, er3
0x026D12  6E 5B 00 01          mov.b     @(0x1,er5), r3l
0x026D16  0C B3                mov.b     r3l, r3h
0x026D18  18 BB                sub.b     r3l, r3l
0x026D1A  0D 3B                mov.w     r3, e3
0x026D1C  19 33                sub.w     r3, r3
0x026D1E  1A 80                sub.l     er0, er0
0x026D20  6E 58 00 02          mov.b     @(0x2,er5), r0l
0x026D24  0D 08                mov.w     r0, e0
0x026D26  19 00                sub.w     r0, r0
0x026D28  0A 83                add.l     er0, er3
0x026D2A  1A 80                sub.l     er0, er0
0x026D2C  6E 58 00 03          mov.b     @(0x3,er5), r0l
0x026D30  10 70                shll.l    #2, er0
0x026D32  10 70                shll.l    #2, er0
0x026D34  10 70                shll.l    #2, er0
0x026D36  10 70                shll.l    #2, er0
0x026D38  0A 83                add.l     er0, er3
0x026D3A  1A 80                sub.l     er0, er0
0x026D3C  6E 58 00 04          mov.b     @(0x4,er5), r0l
0x026D40  0A 83                add.l     er0, er3
0x026D42  1A 80                sub.l     er0, er0
0x026D44  6E 58 00 05          mov.b     @(0x5,er5), r0l
0x026D48  0C 80                mov.b     r0l, r0h
0x026D4A  18 88                sub.b     r0l, r0l
0x026D4C  0D 08                mov.w     r0, e0
0x026D4E  19 00                sub.w     r0, r0
0x026D50  1A 91                sub.l     er1, er1
0x026D52  6E 59 00 06          mov.b     @(0x6,er5), r1l
0x026D56  0D 19                mov.w     r1, e1
0x026D58  19 11                sub.w     r1, r1
0x026D5A  0A 90                add.l     er1, er0
0x026D5C  1A 91                sub.l     er1, er1
0x026D5E  6E 59 00 07          mov.b     @(0x7,er5), r1l
0x026D62  10 71                shll.l    #2, er1
0x026D64  10 71                shll.l    #2, er1
0x026D66  10 71                shll.l    #2, er1
0x026D68  10 71                shll.l    #2, er1
0x026D6A  0A 90                add.l     er1, er0
0x026D6C  1A 91                sub.l     er1, er1
0x026D6E  6E 59 00 08          mov.b     @(0x8,er5), r1l
0x026D72  0A 90                add.l     er1, er0
0x026D74  01 00 6F F0 00 0E    mov.l     er0, @(0xe,sp)
0x026D7A  6B 20 00 40 07 BE    mov.w     @0x4007be, r0
