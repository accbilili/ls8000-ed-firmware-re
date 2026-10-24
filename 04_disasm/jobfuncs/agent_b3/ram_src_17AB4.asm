0x017AB4  mov.w     r0, @-sp   ; 6d f0
0x017AB6  mov.b     @0x00017e, r0l   ; 6a 28 00 00 01 7e
0x017ABC  cmp.b     #0x00, r0l   ; a8 00
0x017ABE  beq       0x017ad2   ; 58 70 00 10
0x017AC2  cmp.b     #0xff, r0l   ; a8 ff
0x017AC4  beq       0x017ad2   ; 58 70 00 0a
0x017AC8  cmp.b     #0x53, r0l   ; a8 53
0x017ACA  beq       0x017ada   ; 58 70 00 0c
0x017ACE  bt        0x017ae2   ; 58 00 00 10
0x017AD2  bsr       0x017ae6   ; 5c 00 00 10
0x017AD6  bt        0x017ae2   ; 58 00 00 08
0x017ADA  bsr       0x017c10   ; 5c 00 01 32
0x017ADE  bt        0x017ae2   ; 58 00 00 00
0x017AE2  mov.w     @sp+, r0   ; 6d 70
0x017AE4  rts          ; 54 70
0x017AE6  mov.l     er0, @-sp   ; 01 00 6d f0
0x017AEA  mov.l     er1, @-sp   ; 01 00 6d f1
0x017AEE  mov.l     er2, @-sp   ; 01 00 6d f2
0x017AF2  mov.l     er3, @-sp   ; 01 00 6d f3
0x017AF6  mov.l     er4, @-sp   ; 01 00 6d f4
0x017AFA  mov.l     er5, @-sp   ; 01 00 6d f5
0x017AFE  mov.l     er6, @-sp   ; 01 00 6d f6
0x017B02  orc       #0x07, exr   ; 01 41 04 07
0x017B06  mov.l     @0xffdc34, er6   ; 01 00 6b 06 dc 34
0x017B0C  mov.l     #0x00004000, er5   ; 7a 05 00 00 40 00
0x017B12  cmp.l     er6, er5   ; 1f e5
0x017B14  bne       0x017b1e   ; 58 60 00 06
0x017B18  mov.b     #0x01, r4l   ; fc 01
0x017B1A  bt        0x017b88   ; 58 00 00 6a
0x017B1E  mov.l     #0x00006000, er5   ; 7a 05 00 00 60 00
0x017B24  cmp.l     er6, er5   ; 1f e5
0x017B26  bne       0x017b30   ; 58 60 00 06
0x017B2A  mov.b     #0x01, r4l   ; fc 01
0x017B2C  bt        0x017b88   ; 58 00 00 58
0x017B30  mov.l     #0x00010000, er5   ; 7a 05 00 01 00 00
0x017B36  cmp.l     er6, er5   ; 1f e5
0x017B38  bne       0x017b48   ; 58 60 00 0c
0x017B3C  mov.b     #0x01, r4l   ; fc 01
0x017B3E  mov.l     #0x00010000, er5   ; 7a 05 00 01 00 00
0x017B44  bt        0x017b88   ; 58 00 00 40
0x017B48  mov.l     #0x00020000, er5   ; 7a 05 00 02 00 00
0x017B4E  cmp.l     er6, er5   ; 1f e5
0x017B50  bne       0x017b60   ; 58 60 00 0c
0x017B54  mov.b     #0x04, r4l   ; fc 04
0x017B56  mov.l     #0x00010000, er5   ; 7a 05 00 01 00 00
0x017B5C  bt        0x017b88   ; 58 00 00 28
0x017B60  mov.l     #0x00060000, er5   ; 7a 05 00 06 00 00
0x017B66  cmp.l     er6, er5   ; 1f e5
0x017B68  bne       0x017b78   ; 58 60 00 0c
0x017B6C  mov.b     #0x01, r4l   ; fc 01
0x017B6E  mov.l     #0x00010000, er5   ; 7a 05 00 01 00 00
0x017B74  bt        0x017b88   ; 58 00 00 10
0x017B78  mov.l     #0x00070000, er5   ; 7a 05 00 07 00 00
0x017B7E  cmp.l     er6, er5   ; 1f e5
0x017B80  mov.b     #0x01, r4l   ; fc 01
0x017B82  mov.l     #0x00010000, er5   ; 7a 05 00 01 00 00
0x017B88  mov.l     #0x00000aaa, er0   ; 7a 00 00 00 0a aa
0x017B8E  mov.w     #0x00aa, r1   ; 79 01 00 aa
0x017B92  mov.w     r1, @er0   ; 69 81
0x017B94  mov.l     #0x00000554, er0   ; 7a 00 00 00 05 54
0x017B9A  mov.w     #0x0055, r1   ; 79 01 00 55
0x017B9E  mov.w     r1, @er0   ; 69 81
0x017BA0  mov.l     #0x00000aaa, er0   ; 7a 00 00 00 0a aa
0x017BA6  mov.w     #0x0080, r1   ; 79 01 00 80
0x017BAA  mov.w     r1, @er0   ; 69 81
0x017BAC  mov.l     #0x00000aaa, er0   ; 7a 00 00 00 0a aa
0x017BB2  mov.w     #0x00aa, r1   ; 79 01 00 aa
0x017BB6  mov.w     r1, @er0   ; 69 81
0x017BB8  mov.l     #0x00000554, er0   ; 7a 00 00 00 05 54
0x017BBE  mov.w     #0x0055, r1   ; 79 01 00 55
0x017BC2  mov.w     r1, @er0   ; 69 81
0x017BC4  mov.w     #0x0030, r1   ; 79 01 00 30
0x017BC8  mov.w     r1, @er6   ; 69 e1
0x017BCA  dec.b     #1, r4l   ; 1a 0c
0x017BCC  beq       0x017bda   ; 58 70 00 0a
0x017BD0  mov.w     @er6, r1   ; 69 61
0x017BD2  add.l     er5, er6   ; 0a d6
0x017BD4  and.b     #0x08, r1l   ; e9 08
0x017BD6  beq       0x017bc4   ; 47 ec
0x017BD8  sub.l     er5, er6   ; 1a d6
0x017BDA  mov.w     @er6, r1   ; 69 61
0x017BDC  and.b     #0x80, r1l   ; e9 80
0x017BDE  bne       0x017bec   ; 58 60 00 0a
0x017BE2  mov.w     #0x5a00, r0   ; 79 00 5a 00
0x017BE6  mov.w     r0, @0xffffbc   ; 6b 80 ff bc
0x017BEA  bt        0x017bda   ; 40 ee
0x017BEC  add.l     er5, er6   ; 0a d6
0x017BEE  cmp.b     #0x00, r4l   ; ac 00
0x017BF0  bne       0x017b88   ; 46 96
0x017BF2  mov.l     @sp+, er6   ; 01 00 6d 76
0x017BF6  mov.l     @sp+, er5   ; 01 00 6d 75
0x017BFA  mov.l     @sp+, er4   ; 01 00 6d 74
0x017BFE  mov.l     @sp+, er3   ; 01 00 6d 73
0x017C02  mov.l     @sp+, er2   ; 01 00 6d 72
0x017C06  mov.l     @sp+, er1   ; 01 00 6d 71
0x017C0A  mov.l     @sp+, er0   ; 01 00 6d 70
0x017C0E  rts          ; 54 70
0x017C10  mov.l     er0, @-sp   ; 01 00 6d f0
0x017C14  mov.l     er1, @-sp   ; 01 00 6d f1
0x017C18  orc       #0x07, exr   ; 01 41 04 07
0x017C1C  mov.l     @0xffdc34, er0   ; 01 00 6b 00 dc 34
0x017C22  mov.w     #0x0004, e1   ; 79 09 00 04
0x017C26  cmp.l     #0x00000000, er0   ; 7a 20 00 00 00 00
0x017C2C  beq       0x017c96   ; 58 70 00 66
0x017C30  mov.w     #0x0002, e1   ; 79 09 00 02
0x017C34  cmp.l     #0x00004000, er0   ; 7a 20 00 00 40 00
0x017C3A  beq       0x017c96   ; 58 70 00 58
0x017C3E  mov.w     #0x0002, e1   ; 79 09 00 02
0x017C42  cmp.l     #0x00006000, er0   ; 7a 20 00 00 60 00
0x017C48  beq       0x017c96   ; 58 70 00 4a
0x017C4C  mov.w     #0x0008, e1   ; 79 09 00 08
0x017C50  cmp.l     #0x00008000, er0   ; 7a 20 00 00 80 00
0x017C56  beq       0x017c96   ; 58 70 00 3c
0x017C5A  mov.w     #0x0001, e1   ; 79 09 00 01
0x017C5E  cmp.l     #0x00010000, er0   ; 7a 20 00 01 00 00
0x017C64  beq       0x017c9e   ; 58 70 00 36
0x017C68  mov.w     #0x0004, e1   ; 79 09 00 04
0x017C6C  cmp.l     #0x00020000, er0   ; 7a 20 00 02 00 00
0x017C72  beq       0x017c9e   ; 58 70 00 28
0x017C76  mov.w     #0x0001, e1   ; 79 09 00 01
0x017C7A  cmp.l     #0x00060000, er0   ; 7a 20 00 06 00 00
0x017C80  beq       0x017c9e   ; 58 70 00 1a
0x017C84  mov.w     #0x0001, e1   ; 79 09 00 01
0x017C88  cmp.l     #0x00070000, er0   ; 7a 20 00 07 00 00
0x017C8E  beq       0x017c9e   ; 58 70 00 0c
0x017C92  bt        0x017ca6   ; 58 00 00 10
0x017C96  bsr       0x017cb0   ; 5c 00 00 16
0x017C9A  bt        0x017ca6   ; 58 00 00 08
0x017C9E  bsr       0x017cee   ; 5c 00 00 4c
0x017CA2  bt        0x017ca6   ; 58 00 00 00
0x017CA6  mov.l     @sp+, er1   ; 01 00 6d 71
0x017CAA  mov.l     @sp+, er0   ; 01 00 6d 70
0x017CAE  rts          ; 54 70
0x017CB0  mov.l     er0, @-sp   ; 01 00 6d f0
0x017CB4  mov.l     er1, @-sp   ; 01 00 6d f1
0x017CB8  mov.l     er2, @-sp   ; 01 00 6d f2
0x017CBC  mov.l     #0x00001000, er2   ; 7a 02 00 00 10 00
0x017CC2  bsr       0x017d2c   ; 5c 00 00 66
0x017CC6  mov.w     #0x0030, r1   ; 79 01 00 30
0x017CCA  mov.w     r1, @er0   ; 69 81
0x017CCC  mov.w     #0x5a00, r1   ; 79 01 5a 00
0x017CD0  mov.w     r1, @0xffffbc   ; 6b 81 ff bc
0x017CD4  mov.w     @er0, r1   ; 69 01
0x017CD6  and.b     #0x80, r1l   ; e9 80
0x017CD8  beq       0x017ccc   ; 47 f2
0x017CDA  add.l     er2, er0   ; 0a a0
0x017CDC  dec.w     #1, e1   ; 1b 59
0x017CDE  bne       0x017cc2   ; 46 e2
0x017CE0  mov.l     @sp+, er2   ; 01 00 6d 72
0x017CE4  mov.l     @sp+, er1   ; 01 00 6d 71
0x017CE8  mov.l     @sp+, er0   ; 01 00 6d 70
0x017CEC  rts          ; 54 70
0x017CEE  mov.l     er0, @-sp   ; 01 00 6d f0
0x017CF2  mov.l     er1, @-sp   ; 01 00 6d f1
0x017CF6  mov.l     er2, @-sp   ; 01 00 6d f2
0x017CFA  mov.l     #0x00010000, er2   ; 7a 02 00 01 00 00
0x017D00  bsr       0x017d2c   ; 5c 00 00 28
0x017D04  mov.w     #0x0050, r1   ; 79 01 00 50
0x017D08  mov.w     r1, @er0   ; 69 81
0x017D0A  mov.w     #0x5a00, r1   ; 79 01 5a 00
0x017D0E  mov.w     r1, @0xffffbc   ; 6b 81 ff bc
0x017D12  mov.w     @er0, r1   ; 69 01
0x017D14  and.b     #0x80, r1l   ; e9 80
0x017D16  beq       0x017d0a   ; 47 f2
0x017D18  add.l     er2, er0   ; 0a a0
0x017D1A  dec.w     #1, e1   ; 1b 59
0x017D1C  bne       0x017d00   ; 46 e2
0x017D1E  mov.l     @sp+, er2   ; 01 00 6d 72
0x017D22  mov.l     @sp+, er1   ; 01 00 6d 71
0x017D26  mov.l     @sp+, er0   ; 01 00 6d 70
0x017D2A  rts          ; 54 70
0x017D2C  mov.l     er0, @-sp   ; 01 00 6d f0
0x017D30  mov.w     r1, @-sp   ; 6d f1
0x017D32  mov.l     #0x0000aaaa, er0   ; 7a 00 00 00 aa aa
0x017D38  mov.w     #0x00aa, r1   ; 79 01 00 aa
0x017D3C  mov.w     r1, @er0   ; 69 81
0x017D3E  mov.l     #0x00005554, er0   ; 7a 00 00 00 55 54
0x017D44  mov.w     #0x0055, r1   ; 79 01 00 55
0x017D48  mov.w     r1, @er0   ; 69 81
0x017D4A  mov.l     #0x0000aaaa, er0   ; 7a 00 00 00 aa aa
0x017D50  mov.w     #0x0080, r1   ; 79 01 00 80
0x017D54  mov.w     r1, @er0   ; 69 81
0x017D56  mov.l     #0x0000aaaa, er0   ; 7a 00 00 00 aa aa
0x017D5C  mov.w     #0x00aa, r1   ; 79 01 00 aa
0x017D60  mov.w     r1, @er0   ; 69 81
0x017D62  mov.l     #0x00005554, er0   ; 7a 00 00 00 55 54
0x017D68  mov.w     #0x0055, r1   ; 79 01 00 55
0x017D6C  mov.w     r1, @er0   ; 69 81
0x017D6E  mov.w     @sp+, r1   ; 6d 71
0x017D70  mov.l     @sp+, er0   ; 01 00 6d 70
0x017D74  rts          ; 54 70
0x017D76  mov.w     r0, @-sp   ; 6d f0
0x017D78  mov.b     @0x00017e, r0l   ; 6a 28 00 00 01 7e
0x017D7E  cmp.b     #0x00, r0l   ; a8 00
0x017D80  beq       0x017d94   ; 58 70 00 10
0x017D84  cmp.b     #0xff, r0l   ; a8 ff
0x017D86  beq       0x017d94   ; 58 70 00 0a
0x017D8A  cmp.b     #0x53, r0l   ; a8 53
0x017D8C  beq       0x017d9c   ; 58 70 00 0c
0x017D90  bt        0x017da4   ; 58 00 00 10
0x017D94  bsr       0x017da8   ; 5c 00 00 10
0x017D98  bt        0x017da4   ; 58 00 00 08
0x017D9C  bsr       0x017e56   ; 5c 00 00 b6
0x017DA0  bt        0x017da4   ; 58 00 00 00
0x017DA4  mov.w     @sp+, r0   ; 6d 70
0x017DA6  rts          ; 54 70
0x017DA8  mov.l     er0, @-sp   ; 01 00 6d f0
0x017DAC  mov.l     er1, @-sp   ; 01 00 6d f1
0x017DB0  mov.l     er2, @-sp   ; 01 00 6d f2
0x017DB4  mov.l     er3, @-sp   ; 01 00 6d f3
0x017DB8  mov.l     er4, @-sp   ; 01 00 6d f4
0x017DBC  mov.l     er5, @-sp   ; 01 00 6d f5
0x017DC0  mov.l     er6, @-sp   ; 01 00 6d f6
0x017DC4  orc       #0x07, exr   ; 01 41 04 07
0x017DC8  mov.l     @0xffdc30, er5   ; 01 00 6b 05 dc 30
0x017DCE  mov.l     @0xffdc34, er6   ; 01 00 6b 06 dc 34
0x017DD4  mov.b     @0x400d38, r4l   ; 6a 2c 00 40 0d 38
0x017DDA  mov.b     #0x00, r4h   ; f4 00
0x017DDC  btst      #0, r4l   ; 73 0c
0x017DDE  beq       0x017de4   ; 58 70 00 02
0x017DE2  inc.w     #1, r4   ; 0b 54
0x017DE4  mov.w     @er5, r3   ; 69 53
0x017DE6  mov.l     #0x00000aaa, er0   ; 7a 00 00 00 0a aa
0x017DEC  mov.w     #0x00aa, r1   ; 79 01 00 aa
0x017DF0  mov.w     r1, @er0   ; 69 81
0x017DF2  mov.l     #0x00000554, er0   ; 7a 00 00 00 05 54
0x017DF8  mov.w     #0x0055, r1   ; 79 01 00 55
0x017DFC  mov.w     r1, @er0   ; 69 81
0x017DFE  mov.l     #0x00000aaa, er0   ; 7a 00 00 00 0a aa
0x017E04  mov.w     #0x00a0, r1   ; 79 01 00 a0
0x017E08  mov.w     r1, @er0   ; 69 81
0x017E0A  mov.w     r3, @er6   ; 69 e3
0x017E0C  mov.w     @er5, r0   ; 69 50
0x017E0E  and.b     #0x80, r0l   ; e8 80
0x017E10  mov.w     @er6, r1   ; 69 61
0x017E12  and.b     #0x80, r1l   ; e9 80
0x017E14  cmp.b     r0l, r1l   ; 1c 89
0x017E16  beq       0x017e24   ; 58 70 00 0a
0x017E1A  mov.w     #0x5a00, r0   ; 79 00 5a 00
0x017E1E  mov.w     r0, @0xffffbc   ; 6b 80 ff bc
0x017E22  bt        0x017e0c   ; 40 e8
0x017E24  inc.l     #2, er5   ; 0b f5
0x017E26  inc.l     #2, er6   ; 0b f6
0x017E28  dec.w     #2, r4   ; 1b d4
0x017E2A  bne       0x017de4   ; 46 b8
0x017E2C  mov.l     er5, @0xffdc30   ; 01 00 6b 85 dc 30
0x017E32  mov.l     er6, @0xffdc34   ; 01 00 6b 86 dc 34
0x017E38  mov.l     @sp+, er6   ; 01 00 6d 76
0x017E3C  mov.l     @sp+, er5   ; 01 00 6d 75
0x017E40  mov.l     @sp+, er4   ; 01 00 6d 74
0x017E44  mov.l     @sp+, er3   ; 01 00 6d 73
0x017E48  mov.l     @sp+, er2   ; 01 00 6d 72
0x017E4C  mov.l     @sp+, er1   ; 01 00 6d 71
0x017E50  mov.l     @sp+, er0   ; 01 00 6d 70
0x017E54  rts          ; 54 70
0x017E56  mov.l     er0, @-sp   ; 01 00 6d f0
0x017E5A  mov.l     er1, @-sp   ; 01 00 6d f1
0x017E5E  mov.l     er2, @-sp   ; 01 00 6d f2
0x017E62  mov.l     er3, @-sp   ; 01 00 6d f3
0x017E66  mov.l     er4, @-sp   ; 01 00 6d f4
0x017E6A  mov.l     er5, @-sp   ; 01 00 6d f5
0x017E6E  mov.l     er6, @-sp   ; 01 00 6d f6
0x017E72  orc       #0x07, exr   ; 01 41 04 07
0x017E76  mov.l     @0xffdc30, er5   ; 01 00 6b 05 dc 30
0x017E7C  mov.l     @0xffdc34, er6   ; 01 00 6b 06 dc 34
0x017E82  mov.b     @0x400d38, r4l   ; 6a 2c 00 40 0d 38
0x017E88  mov.b     #0x00, r4h   ; f4 00
0x017E8A  btst      #0, r4l   ; 73 0c
0x017E8C  beq       0x017e92   ; 58 70 00 02
0x017E90  inc.w     #1, r4   ; 0b 54
0x017E92  mov.w     @er5, r3   ; 69 53
0x017E94  mov.l     #0x0000aaaa, er0   ; 7a 00 00 00 aa aa
0x017E9A  mov.w     #0x00aa, r1   ; 79 01 00 aa
0x017E9E  mov.w     r1, @er0   ; 69 81
0x017EA0  mov.l     #0x00005554, er0   ; 7a 00 00 00 55 54
0x017EA6  mov.w     #0x0055, r1   ; 79 01 00 55
0x017EAA  mov.w     r1, @er0   ; 69 81
0x017EAC  mov.l     #0x0000aaaa, er0   ; 7a 00 00 00 aa aa
0x017EB2  mov.w     #0x00a0, r1   ; 79 01 00 a0
0x017EB6  mov.w     r1, @er0   ; 69 81
0x017EB8  mov.w     r3, @er6   ; 69 e3
0x017EBA  mov.w     @er5, r0   ; 69 50
0x017EBC  and.b     #0x80, r0l   ; e8 80
0x017EBE  mov.w     @er6, r1   ; 69 61
0x017EC0  and.b     #0x80, r1l   ; e9 80
0x017EC2  cmp.b     r0l, r1l   ; 1c 89
0x017EC4  beq       0x017ed2   ; 58 70 00 0a
0x017EC8  mov.w     #0x5a00, r0   ; 79 00 5a 00
0x017ECC  mov.w     r0, @0xffffbc   ; 6b 80 ff bc
0x017ED0  bt        0x017eba   ; 40 e8
0x017ED2  inc.l     #2, er5   ; 0b f5
0x017ED4  inc.l     #2, er6   ; 0b f6
0x017ED6  dec.w     #2, r4   ; 1b d4
0x017ED8  bne       0x017e92   ; 46 b8
0x017EDA  mov.l     er5, @0xffdc30   ; 01 00 6b 85 dc 30
0x017EE0  mov.l     er6, @0xffdc34   ; 01 00 6b 86 dc 34
0x017EE6  mov.l     @sp+, er6   ; 01 00 6d 76
0x017EEA  mov.l     @sp+, er5   ; 01 00 6d 75
0x017EEE  mov.l     @sp+, er4   ; 01 00 6d 74
0x017EF2  mov.l     @sp+, er3   ; 01 00 6d 73
0x017EF6  mov.l     @sp+, er2   ; 01 00 6d 72
0x017EFA  mov.l     @sp+, er1   ; 01 00 6d 71
0x017EFE  mov.l     @sp+, er0   ; 01 00 6d 70
0x017F02  rts          ; 54 70
