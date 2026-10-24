import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
BASE=0x10000
hs=[0x25B2C,0x25B8A,0x25BE6,0x25C4C,0x25CC0,0x25D08,0x25DF8,0x25EEE,0x25F94,0x2604A,0x260AA,0x261FE,0x26246,0x2628E,0x262D4,0x2635E,0x263BE,0x26418,0x26472,0x264C2,0x25ADA,0x26506,0x25A56]
for t in hs:
    pat=t.to_bytes(4,'big'); i=0; hits=[]
    while True:
        i=d.find(pat,i)
        if i<0:break
        hits.append(i+BASE); i+=1
    print(hex(t), [hex(x) for x in hits])
# table entries: decode again to map table slot -> handler
print('--- table slots ---')
for i in range(26):
    a=0x3EBC0+i*16
    print(i, hex(a), hex(int.from_bytes(d[a-BASE+4:a-BASE+8],'big')))
