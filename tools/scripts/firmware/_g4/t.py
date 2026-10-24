import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
d = open(sample('LS8000_111_ROM.bin'),'rb').read()
BASE=0x10000
def rd(a,n): return d[a-BASE:a-BASE+n]
print("== 0x03E2E8 .. 0x03E3A0 raw ==")
for i in range(0, 0xB8, 8):
    a = 0x03E2E8+i
    b = rd(a,8)
    code_be = (b[0]<<8)|b[1]
    fl = (b[2]<<8)|b[3]
    h  = (b[4]<<24)|(b[5]<<16)|(b[6]<<8)|b[7]
    print(f"{a:06X}  {b.hex(' ')}  u16code={code_be:04X} b0={b[0]:02X} b1={b[1]:02X} flags/len={fl:04X} handler={h:06X}")
print()
print("== 0x03EDB8 (E0 subfn/len table) ==")
for i in range(0,32,2):
    a=0x03EDB8+i
    b=rd(a,2)
    print(f"{a:06X}  {b[0]:02X} {b[1]:02X}")
print()
print("== 0x03ED60 whitelist 11 x 8 ==")
for i in range(0,88,8):
    a=0x03ED60+i
    b=rd(a,8)
    s=(b[0]<<24)|(b[1]<<16)|(b[2]<<8)|b[3]
    e=(b[4]<<24)|(b[5]<<16)|(b[6]<<8)|b[7]
    print(f"{a:06X}  start={s:08X} end={e:08X} len={e-s+1 if e>=s else 0}")
