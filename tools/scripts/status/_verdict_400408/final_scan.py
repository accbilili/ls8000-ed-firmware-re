import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
BASE=0x10000
D=open(sample('LS8000_111_ROM.bin'),'rb').read()
def ab(v): return bytes([(v>>24)&255,(v>>16)&255,(v>>8)&255,v&255])
def scan(tag, prefix, addr, tail=b''):
    pat = prefix + ab(addr) + tail
    out=[];i=0
    while True:
        i=D.find(pat,i)
        if i<0: break
        out.append(i+BASE); i+=1
    print('  %-40s %s' % (tag, ' '.join('0x%06X'%h for h in out) if out else '(none)'))
    return out

targets=[0x400408,0x40040A,0x40040C,0x400410,0x400411,0x400412,0x400413,0x400414]
print('### 全 ROM 全寄存器变体扫描（H8 绝对寻址唯一编码形式）###')
for a in targets:
    print('--- 0x%06X ---'%a)
    scan('写32  MOV.L ERm,@abs32', b'\x01\x00\x6b\xa0', a)
    scan('写16  MOV.W Rm,@abs32 ', b'\x6b\xa0', a)
    scan('写8   MOV.B Rm,@abs32 ', b'\x6a\xa0', a)
    scan('读32  MOV.L @abs32,ERn', b'\x01\x00\x6b\x20', a)
    scan('读16  MOV.W @abs32,Rm ', b'\x6b\x20', a)
    scan('读8   MOV.B @abs32,Rm ', b'\x6a\x20', a)
