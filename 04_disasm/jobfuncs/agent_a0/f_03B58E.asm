# fn 0x03B58E (paramcalc) : 523 insns
0x03B58E  stm.l     er2-er3, @-sp
0x03B592  stm.l     er4-er6, @-sp
0x03B596  sub.l     #0x00000056, sp
0x03B59C  mov.w     r0, e6
0x03B59E  mov.w     e0, r6
0x03B5A0  mov.b     r1l, @(0x36,sp)
0x03B5A4  mov.b     r1h, @(0x37,sp)
0x03B5A8  mov.w     e1, @(0x34,sp)
0x03B5AC  mov.w     r6, e3
0x03B5AE  mov.w     e6, r0
0x03B5B0  jsr       0x02b87c
0x03B5B4  mov.b     @(0x6f,sp), r0l
0x03B5B8  cmp.b     #0x03, r0l
0x03B5BA  bne       0x03b5d6
0x03B5BC  mov.b     #0x01, r0l
0x03B5BE  mov.b     r0l, @0x400dab
0x03B5C4  sub.b     r0l, r0l
0x03B5C6  mov.b     r0l, @0x400dac
0x03B5CC  mov.b     #0x02, r0l
0x03B5CE  mov.b     r0l, @0x400dad
0x03B5D4  bt        0x03b5fc
0x03B5D6  mov.b     @(0x6f,sp), r0l
0x03B5DA  cmp.b     #0x02, r0l
0x03B5DC  bne       0x03b5f0
0x03B5DE  mov.b     #0x02, r0l
0x03B5E0  mov.b     r0l, @0x400dab
0x03B5E6  mov.b     #0x03, r0l
0x03B5E8  mov.b     r0l, @0x400dac
0x03B5EE  bt        0x03b5fc
0x03B5F0  mov.b     @0x4491d4, r0l
0x03B5F6  mov.b     r0l, @0x400dab
0x03B5FC  sub.b     r3l, r3l
0x03B5FE  jmp       0x03bd30
0x03B602  btst      #7, @0x400400
0x03B60A  bne       0x03bd3a
0x03B60E  bt        0x03b626
0x03B610  sub.b     r0l, r0l
0x03B612  mov.w     r0, @-sp
0x03B614  mov.l     #0x00002710, er1
0x03B61A  mov.w     e3, r0
0x03B61C  jsr       0x02adce
0x03B620  adds.l    #2, sp
0x03B622  jsr       0x02acba
0x03B626  mov.w     @0x4202a2, r0
0x03B62C  cmp.w     r0, e3
0x03B62E  bne       0x03b610
0x03B630  sub.b     r6l, r6l
0x03B632  mov.b     r6l, r0h
0x03B634  sub.b     r0l, r0l
0x03B636  jsr       0x0322b4
0x03B63A  mov.b     r6l, r5l
0x03B63C  extu.w    r5
0x03B63E  extu.l    er5
0x03B640  shll.l    #2, er5
0x03B642  mov.l     @(0x400f32,er5), er0
0x03B64C  mov.l     @(0x400f42,er5), er1
0x03B656  add.l     er1, er0
0x03B658  mov.l     er0, @(0x4499d8,er5)
0x03B662  mov.l     er0, @(0x4499e8,er5)
0x03B66C  inc.b     #1, r6l
0x03B66E  cmp.b     #0x04, r6l
0x03B670  bcs       0x03b632
0x03B672  mov.l     #0x004499e8, er1
0x03B678  mov.b     @(0x6f,sp), r0l
0x03B67C  jsr       0x02d700
0x03B680  sub.b     r0l, r0l
0x03B682  mov.b     r0l, @(0x45,sp)
0x03B686  mov.b     r3l, r0l
0x03B688  extu.w    r0
0x03B68A  mov.w     #0x0030, e0
0x03B68E  mulxu.w   e0, er0
0x03B690  mov.l     er0, @(0x46,sp)
0x03B696  jmp       0x03ba54
0x03B69A  sub.l     er0, er0
0x03B69C  mov.b     @(0x45,sp), r0l
0x03B6A0  mov.b     @(0x400dab,er0), r3h
0x03B6A8  mov.w     #0x0001, r5
0x03B6AC  mov.b     r3h, r6l
0x03B6AE  extu.w    r6
0x03B6B0  extu.l    er6
0x03B6B2  shll.l    #2, er6
0x03B6B4  mov.l     @(0x420250,er6), er6
0x03B6BE  sub.w     e5, e5
0x03B6C0  bt        0x03b6ce
0x03B6C2  mov.w     @er6, r0
0x03B6C4  cmp.w     r5, r0
0x03B6C6  bls       0x03b6ca
0x03B6C8  mov.w     @er6, r5
0x03B6CA  inc.l     #2, er6
0x03B6CC  inc.w     #1, e5
0x03B6CE  mov.w     @0x400d60, r0
0x03B6D4  cmp.w     r0, e5
0x03B6D6  bcs       0x03b6c2
0x03B6D8  mov.w     #0x5a00, r0
0x03B6DC  mov.w     r0, @0xffffbc
0x03B6E2  mov.b     r3l, r4l
0x03B6E4  extu.w    r4
0x03B6E6  extu.l    er4
0x03B6E8  mov.l     er4, er0
0x03B6EA  shll.l    #2, er0
0x03B6EC  shll.l    #2, er0
0x03B6EE  shll.l    #2, er0
0x03B6F0  mov.b     r3h, r1l
0x03B6F2  extu.w    r1
0x03B6F4  extu.l    er1
0x03B6F6  mov.l     er1, @(0x52,sp)
0x03B6FC  shll.l    #2, er1
0x03B6FE  shll.l    #2, er1
0x03B700  add.l     #0x004490f2, er0
0x03B706  add.l     er1, er0
0x03B708  add.l     #0x0000000c, er0
0x03B70E  mov.w     r5, r1
0x03B710  extu.l    er1
0x03B712  mov.l     er1, @er0
0x03B716  mov.l     @(0x52,sp), er6
0x03B71C  shll.l    #2, er6
0x03B71E  shll.l    #2, er4
0x03B720  shll.l    #2, er4
0x03B722  add.l     #0x004498f8, er4
0x03B728  add.l     er6, er4
0x03B72A  mov.l     @(0x400f32,er6), er1
0x03B734  mov.l     #0x0000002c, er0
0x03B73A  add.l     sp, er0
0x03B73C  jsr       0x018e68
0x03B740  mov.w     r5, r1
0x03B742  mov.l     er0, @(0x20,sp)
0x03B748  mov.l     #0x00000024, er0
0x03B74E  add.l     sp, er0
0x03B750  jsr       0x018ede
0x03B754  mov.l     #0x0003f9bc, er1
0x03B75A  mov.l     er0, er2
0x03B75C  mov.l     #0x00000018, er0
0x03B762  add.l     sp, er0
0x03B764  jsr       0x01842c
0x03B768  mov.l     @(0x20,sp), er1
0x03B76E  mov.l     er0, er2
0x03B770  mov.l     #0x00000010, er0
0x03B776  add.l     sp, er0
0x03B778  jsr       0x018aa0
0x03B77C  jsr       0x01876a
0x03B780  mov.l     @(0x400f42,er6), er1
0x03B78A  add.l     er1, er0
0x03B78C  mov.l     er0, @er4
0x03B790  mov.w     @0x420274, e4
0x03B796  dec.w     #1, e4
0x03B798  sub.b     r4l, r4l
0x03B79A  mov.b     r3h, r0l
0x03B79C  extu.w    r0
0x03B79E  extu.l    er0
0x03B7A0  shll.l    #2, er0
0x03B7A2  add.l     #0x00420250, er0
0x03B7A8  mov.l     er0, @(0x38,sp)
0x03B7AE  mov.b     r3h, r0l
0x03B7B0  extu.w    r0
0x03B7B2  mov.w     #0x000c, e0
0x03B7B6  mulxu.w   e0, er0
0x03B7B8  mov.l     er0, @(0x4a,sp)
0x03B7BE  mov.w     #0x0001, r5
0x03B7C2  mov.b     r4l, r6l
0x03B7C4  extu.w    r6
0x03B7C6  extu.l    er6
0x03B7C8  shll.l    er6
0x03B7CA  mov.w     @(0x449086,er6), r6
0x03B7D2  extu.l    er6
0x03B7D4  shll.l    er6
0x03B7D6  mov.l     @(0x38,sp), er0
0x03B7DC  mov.l     @er0, er0
0x03B7E0  add.l     er0, er6
0x03B7E2  sub.l     er0, er0
0x03B7E4  mov.l     er0, @(0x4e,sp)
0x03B7EA  sub.w     e5, e5
0x03B7EC  bt        0x03b80c
0x03B7EE  mov.w     @er6, r0
0x03B7F0  cmp.w     r5, r0
0x03B7F2  bls       0x03b7f6
0x03B7F4  mov.w     @er6, r5
0x03B7F6  mov.w     @er6, r0
0x03B7F8  extu.l    er0
0x03B7FA  mov.l     @(0x4e,sp), er1
0x03B800  add.l     er0, er1
0x03B802  mov.l     er1, @(0x4e,sp)
0x03B808  inc.l     #2, er6
0x03B80A  inc.w     #1, e5
0x03B80C  cmp.w     e4, e5
0x03B80E  bcs       0x03b7ee
0x03B810  mov.w     #0x5a00, r0
0x03B814  mov.w     r0, @0xffffbc
0x03B81A  mov.w     @0x420274, r1
0x03B820  extu.l    er1
0x03B822  mov.l     @(0x4e,sp), er0
0x03B828  jsr       0x01872e
0x03B82C  mov.l     er0, @(0x4e,sp)
0x03B832  mov.b     r3l, r0l
0x03B834  extu.w    r0
0x03B836  extu.l    er0
0x03B838  mov.l     er0, @(0x52,sp)
0x03B83E  mov.l     #0x00000018, er1
0x03B844  jsr       0x018e1e
0x03B848  mov.b     r3h, r6l
0x03B84A  extu.w    r6
0x03B84C  extu.l    er6
0x03B84E  mov.l     er0, @(0x30,sp)
0x03B854  mov.l     er6, er0
0x03B856  mov.l     #0x00000006, er1
0x03B85C  jsr       0x018e1e
0x03B860  mov.l     @(0x30,sp), er1
0x03B866  add.l     #0x004491a2, er1
0x03B86C  add.l     er0, er1
0x03B86E  mov.b     r4l, r0l
0x03B870  extu.w    r0
0x03B872  extu.l    er0
0x03B874  mov.l     er0, @(0x40,sp)
0x03B87A  shll.l    er0
0x03B87C  add.l     er0, er1
0x03B87E  mov.w     @(0x50,sp), r0
0x03B882  mov.w     r0, @er1
0x03B884  mov.l     @(0x40,sp), er0
0x03B88A  shll.l    #2, er0
0x03B88C  mov.l     er0, @(0x3c,sp)
0x03B892  mov.l     @(0x52,sp), er1
0x03B898  shll.l    #2, er1
0x03B89A  shll.l    #2, er1
0x03B89C  shll.l    #2, er1
0x03B89E  mov.l     er6, er2
0x03B8A0  shll.l    #2, er2
0x03B8A2  shll.l    #2, er2
0x03B8A4  add.l     #0x004490f2, er1
0x03B8AA  add.l     er2, er1
0x03B8AC  add.l     er0, er1
0x03B8AE  mov.w     r5, r2
0x03B8B0  extu.l    er2
0x03B8B2  mov.l     er2, @er1
0x03B8B6  mov.l     er6, er0
0x03B8B8  mov.l     #0x0000000c, er1
0x03B8BE  jsr       0x018e1e
0x03B8C2  mov.l     er0, @(0x30,sp)
0x03B8C8  mov.l     @(0x52,sp), er0
0x03B8CE  mov.l     #0x00000030, er1
0x03B8D4  jsr       0x018e1e
0x03B8D8  add.l     #0x00449918, er0
0x03B8DE  mov.l     @(0x30,sp), er1
0x03B8E4  add.l     er1, er0
0x03B8E6  mov.l     @(0x3c,sp), er1
0x03B8EC  add.l     er1, er0
0x03B8EE  mov.l     er0, @(0x40,sp)
0x03B8F4  mov.l     er6, er1
0x03B8F6  shll.l    #2, er1
0x03B8F8  mov.l     er1, @(0x4e,sp)
0x03B8FE  mov.l     @(0x400f32,er1), er1
0x03B908  mov.l     er0, @(0x24,sp)
0x03B90E  mov.l     #0x00000028, er0
0x03B914  add.l     sp, er0
0x03B916  jsr       0x018e68
0x03B91A  mov.w     r5, r1
0x03B91C  mov.l     er0, @(0x18,sp)
0x03B922  mov.l     #0x0000001c, er0
0x03B928  add.l     sp, er0
0x03B92A  jsr       0x018ede
0x03B92E  mov.l     #0x0003f9c4, er1
0x03B934  mov.l     er0, er2
0x03B936  mov.l     #0x00000010, er0
0x03B93C  add.l     sp, er0
0x03B93E  jsr       0x01842c
0x03B942  mov.l     @(0x18,sp), er1
0x03B948  mov.l     er0, er2
0x03B94A  mov.l     #0x00000008, er0
0x03B950  add.l     sp, er0
0x03B952  jsr       0x018aa0
0x03B956  mov.l     er0, er1
0x03B958  mov.l     #0x0003f9cc, er2
0x03B95E  mov.l     sp, er0
0x03B960  jsr       0x018aa0
0x03B964  jsr       0x01876a
0x03B968  mov.l     @(0x4e,sp), er1
0x03B96E  mov.l     @(0x400f42,er1), er1
0x03B978  add.l     er1, er0
0x03B97A  mov.l     @(0x24,sp), er1
0x03B980  mov.l     er0, @er1
0x03B984  mov.l     @(0x52,sp), er0
0x03B98A  shll.l    #2, er0
0x03B98C  shll.l    #2, er0
0x03B98E  add.l     #0x004498f8, er0
0x03B994  mov.l     @(0x4e,sp), er1
0x03B99A  add.l     er1, er0
0x03B99C  mov.l     @(0x40,sp), er1
0x03B9A2  mov.l     @er0, er0
0x03B9A6  mov.l     @er1, er1
0x03B9AA  cmp.l     er1, er0
0x03B9AC  bhi       0x03ba0c
0x03B9AE  mov.b     r3l, r5l
0x03B9B0  extu.w    r5
0x03B9B2  extu.l    er5
0x03B9B4  mov.l     er5, er0
0x03B9B6  mov.l     #0x00000030, er1
0x03B9BC  jsr       0x018e1e
0x03B9C0  mov.b     r3h, r6l
0x03B9C2  extu.w    r6
0x03B9C4  extu.l    er6
0x03B9C6  mov.l     er0, @(0x30,sp)
0x03B9CC  mov.l     er6, er0
0x03B9CE  mov.l     #0x0000000c, er1
0x03B9D4  jsr       0x018e1e
0x03B9D8  mov.l     @(0x30,sp), er1
0x03B9DE  add.l     #0x00449978, er1
0x03B9E4  add.l     er0, er1
0x03B9E6  mov.b     r4l, r0l
0x03B9E8  extu.w    r0
0x03B9EA  extu.l    er0
0x03B9EC  shll.l    #2, er0
0x03B9EE  add.l     er0, er1
0x03B9F0  mov.l     er5, er0
0x03B9F2  shll.l    #2, er0
0x03B9F4  shll.l    #2, er0
0x03B9F6  mov.l     er6, er2
0x03B9F8  shll.l    #2, er2
0x03B9FA  add.l     #0x004498f8, er0
0x03BA00  add.l     er2, er0
0x03BA02  mov.l     @er0, er0
0x03BA06  mov.l     er0, @er1
0x03BA0A  bt        0x03ba42
0x03BA0C  mov.l     @(0x46,sp), er0
0x03BA12  mov.l     @(0x4a,sp), er1
0x03BA18  add.l     #0x00449978, er0
0x03BA1E  add.l     er1, er0
0x03BA20  mov.b     r4l, r6l
0x03BA22  extu.w    r6
0x03BA24  extu.l    er6
0x03BA26  shll.l    #2, er6
0x03BA28  add.l     er6, er0
0x03BA2A  mov.l     @(0x46,sp), er2
0x03BA30  add.l     #0x00449918, er2
0x03BA36  add.l     er1, er2
0x03BA38  add.l     er6, er2
0x03BA3A  mov.l     @er2, er2
0x03BA3E  mov.l     er2, @er0
0x03BA42  inc.b     #1, r4l
0x03BA44  cmp.b     #0x03, r4l
0x03BA46  bcs       0x03b7be
0x03BA4A  mov.b     @(0x45,sp), r0l
0x03BA4E  inc.b     #1, r0l
0x03BA50  mov.b     r0l, @(0x45,sp)
0x03BA54  mov.b     @(0x45,sp), r0l
0x03BA58  mov.b     @(0x6f,sp), r1l
0x03BA5C  cmp.b     r1l, r0l
0x03BA5E  bcs       0x03b69a
0x03BA62  sub.b     r5h, r5h
0x03BA64  jmp       0x03bd12
0x03BA68  mov.b     r5h, r0l
0x03BA6A  extu.w    r0
0x03BA6C  extu.l    er0
0x03BA6E  mov.b     @(0x400dab,er0), r5l
0x03BA76  mov.b     @(0x37,sp), r0l
0x03BA7A  cmp.b     #0x01, r0l
0x03BA7C  beq       0x03bbcc
0x03BA80  sub.b     r6l, r6l
0x03BA82  mov.b     r5l, r4l
0x03BA84  extu.w    r4
0x03BA86  extu.l    er4
0x03BA88  mov.l     er4, er0
0x03BA8A  shll.l    #2, er0
0x03BA8C  mov.l     er0, @(0x4a,sp)
0x03BA92  add.l     #0x004499d8, er0
0x03BA98  mov.l     er0, @(0x46,sp)
0x03BA9E  mov.b     r3l, r1l
0x03BAA0  extu.w    r1
0x03BAA2  extu.l    er1
0x03BAA4  mov.l     er1, @(0x52,sp)
0x03BAAA  mov.l     er0, @(0x30,sp)
0x03BAB0  mov.l     #0x00000030, er0
0x03BAB6  jsr       0x018e1e
0x03BABA  mov.l     er0, @(0x40,sp)
0x03BAC0  mov.l     er0, @(0x2c,sp)
0x03BAC6  mov.l     er4, er0
0x03BAC8  mov.l     #0x0000000c, er1
0x03BACE  jsr       0x018e1e
0x03BAD2  mov.l     er0, @(0x3c,sp)
0x03BAD8  mov.l     @(0x2c,sp), er1
0x03BADE  add.l     #0x00449978, er1
0x03BAE4  add.l     er0, er1
0x03BAE6  mov.b     r6l, r2l
0x03BAE8  extu.w    r2
0x03BAEA  extu.l    er2
0x03BAEC  mov.l     er2, @(0x4e,sp)
0x03BAF2  shll.l    #2, er2
0x03BAF4  add.l     er2, er1
0x03BAF6  mov.l     @er1, er1
0x03BAFA  mov.l     @(0x30,sp), er0
0x03BB00  mov.l     er1, @er0
0x03BB04  mov.l     @(0x46,sp), er0
0x03BB0A  mov.l     @er0, er0
0x03BB0E  jsr       0x018e9e
0x03BB12  sub.l     er1, er1
0x03BB14  mov.b     @(0x41ff6e,er4), r1l
0x03BB1C  shll.l    #2, er1
0x03BB1E  mov.l     @(0x400dda,er1), er1
0x03BB28  jsr       0x0185ee
0x03BB2C  jsr       0x018860
0x03BB30  mov.l     @(0x4a,sp), er1
0x03BB36  mov.l     er0, @(0x4499e8,er1)
0x03BB40  mov.l     #0x004499e8, er1
0x03BB46  mov.b     @(0x6f,sp), r0l
0x03BB4A  jsr       0x02d700
0x03BB4E  mov.b     r5l, @0x420265
0x03BB54  mov.b     r6l, r0h
0x03BB56  sub.b     r0l, r0l
0x03BB58  bsr       0x03b4f4
0x03BB5C  mov.l     @(0x40,sp), er0
0x03BB62  add.l     #0x00449092, er0
0x03BB68  mov.l     @(0x3c,sp), er1
0x03BB6E  add.l     er1, er0
0x03BB70  add.l     er2, er0
0x03BB72  mov.l     @0x420296, er1
0x03BB7A  mov.l     er1, @er0
0x03BB7E  mov.l     er4, er0
0x03BB80  mov.l     #0x00000006, er1
0x03BB86  jsr       0x018e1e
0x03BB8A  mov.l     er0, @(0x30,sp)
0x03BB90  mov.l     @(0x52,sp), er0
0x03BB96  mov.l     #0x00000018, er1
0x03BB9C  jsr       0x018e1e
0x03BBA0  add.l     #0x00449172, er0
0x03BBA6  mov.l     @(0x30,sp), er1
0x03BBAC  add.l     er1, er0
0x03BBAE  mov.l     @(0x4e,sp), er1
0x03BBB4  shll.l    er1
0x03BBB6  add.l     er1, er0
0x03BBB8  mov.w     @0x41ff76, r1
0x03BBBE  mov.w     r1, @er0
0x03BBC0  inc.b     #1, r6l
0x03BBC2  cmp.b     #0x03, r6l
0x03BBC4  bcs       0x03ba82
0x03BBC8  jmp       0x03bd10
0x03BBCC  mov.b     @0x4491d5, r4l
0x03BBD2  mov.b     r5l, r6l
0x03BBD4  extu.w    r6
0x03BBD6  extu.l    er6
0x03BBD8  mov.l     er6, er0
0x03BBDA  shll.l    #2, er0
0x03BBDC  mov.l     er0, @(0x52,sp)
0x03BBE2  add.l     #0x004499d8, er0
0x03BBE8  mov.l     er0, @(0x4e,sp)
0x03BBEE  mov.b     r3l, r1l
0x03BBF0  extu.w    r1
0x03BBF2  extu.l    er1
0x03BBF4  mov.l     er1, @(0x3c,sp)
0x03BBFA  mov.l     er0, @(0x30,sp)
0x03BC00  mov.l     #0x00000030, er0
0x03BC06  jsr       0x018e1e
0x03BC0A  mov.l     er0, @(0x4a,sp)
0x03BC10  mov.l     er0, @(0x2c,sp)
0x03BC16  mov.l     er6, er0
0x03BC18  mov.l     #0x0000000c, er1
0x03BC1E  jsr       0x018e1e
0x03BC22  mov.l     er0, @(0x46,sp)
0x03BC28  mov.l     @(0x2c,sp), er1
0x03BC2E  add.l     #0x00449978, er1
0x03BC34  add.l     er0, er1
0x03BC36  mov.b     r4l, r2l
0x03BC38  extu.w    r2
0x03BC3A  extu.l    er2
0x03BC3C  mov.l     er2, @(0x38,sp)
0x03BC42  shll.l    #2, er2
0x03BC44  add.l     er2, er1
0x03BC46  mov.l     @er1, er1
0x03BC4A  mov.l     @(0x30,sp), er0
0x03BC50  mov.l     er1, @er0
0x03BC54  mov.l     @(0x4e,sp), er0
0x03BC5A  mov.l     @er0, er0
0x03BC5E  jsr       0x018e9e
0x03BC62  sub.l     er1, er1
0x03BC64  mov.b     @(0x41ff6e,er6), r1l
0x03BC6C  shll.l    #2, er1
0x03BC6E  mov.l     @(0x400dda,er1), er1
0x03BC78  jsr       0x0185ee
0x03BC7C  jsr       0x018860
0x03BC80  mov.l     @(0x52,sp), er1
0x03BC86  mov.l     er0, @(0x4499e8,er1)
0x03BC90  mov.l     #0x004499e8, er1
0x03BC96  mov.b     @(0x6f,sp), r0l
0x03BC9A  jsr       0x02d700
0x03BC9E  mov.b     r5l, @0x420265
0x03BCA4  mov.b     r4l, r0h
0x03BCA6  sub.b     r0l, r0l
0x03BCA8  bsr       0x03b4f4
0x03BCAC  mov.l     @(0x4a,sp), er0
0x03BCB2  add.l     #0x00449092, er0
0x03BCB8  mov.l     @(0x46,sp), er1
0x03BCBE  add.l     er1, er0
0x03BCC0  add.l     er2, er0
0x03BCC2  mov.l     @0x420296, er1
0x03BCCA  mov.l     er1, @er0
0x03BCCE  mov.l     er6, er0
0x03BCD0  mov.l     #0x00000006, er1
0x03BCD6  jsr       0x018e1e
0x03BCDA  mov.l     er0, @(0x30,sp)
0x03BCE0  mov.l     @(0x3c,sp), er0
0x03BCE6  mov.l     #0x00000018, er1
0x03BCEC  jsr       0x018e1e
0x03BCF0  add.l     #0x00449172, er0
0x03BCF6  mov.l     @(0x30,sp), er1
0x03BCFC  add.l     er1, er0
0x03BCFE  mov.l     @(0x38,sp), er1
0x03BD04  shll.l    er1
0x03BD06  add.l     er1, er0
0x03BD08  mov.w     @0x41ff76, r1
0x03BD0E  mov.w     r1, @er0
0x03BD10  inc.b     #1, r5h
0x03BD12  mov.b     @(0x6f,sp), r0l
0x03BD16  cmp.b     r0l, r5h
0x03BD18  bcs       0x03ba68
0x03BD1C  mov.w     @(0x34,sp), r0
0x03BD20  add.w     e3, r0
0x03BD22  mov.w     r0, e3
0x03BD24  mov.l     #0x004499d8, er0
0x03BD2A  bsr       0x03c194
0x03BD2E  inc.b     #1, r3l
0x03BD30  mov.b     @(0x36,sp), r0l
0x03BD34  cmp.b     r0l, r3l
0x03BD36  bcs       0x03b602
0x03BD3A  add.l     #0x00000056, sp
0x03BD40  ldm.l     @sp+, er4-er6
0x03BD44  ldm.l     @sp+, er2-er3
0x03BD48  rts       
