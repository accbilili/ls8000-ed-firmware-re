import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
d=open(sample('LS8000_111_ROM.bin'),'rb').read(); B=0x10000
want={0x28E30:[],0x289B4:[],0x28BB0:[],0x290A0:[]}
for o in range(0,len(d)-4,2):
    if d[o] in (0x5E,0x5A):
        t=int.from_bytes(d[o+1:o+4],'big')
        if t in want: want[t].append((hex(o+B),hex(d[o])))
for t in sorted(want): print(hex(t),want[t])
# 3-byte literal 0x00028E30 anywhere
pat=(0x00028E30).to_bytes(4,'big')[1:]
cnt=0
for o in range(len(d)-3):
    if d[o:o+3]==pat: cnt+=1
print('literal 0x28E30 3B occurrences:',cnt)
