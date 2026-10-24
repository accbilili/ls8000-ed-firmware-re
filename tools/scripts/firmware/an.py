import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import json
d=open(sample('LS8000_111_ROM.bin'),'rb').read()
B=0x10000
def rd(a,n): return d[a-B:a-B+n]
def u16(a): b=rd(a,2); return (b[0]<<8)|b[1]
T0=0x03E390
ents=[]
a=T0
while True:
    h=u16(a); f=u16(a+2)
    if h==0: break
    ents.append((a,h,f)); a+=4
print("entries:",len(ents),"end addr of last:",hex(ents[-1][0]),"terminator:",hex(a),"field2 of term:",u16(a+2))
print("span:",hex(ents[0][0]),"..",hex(a+3),"bytes:",a+4-T0)
T1=0x01914A
def rec(i): return rd(T1+i*5,5)
mx=max(e[2] for e in ents); mn=min(e[2] for e in ents)
print("field2 min/max:",hex(mn),hex(mx),"-> max rec addr",hex(T1+mx*5),"next byte",hex(T1+(mx+1)*5),rd(T1+(mx+1)*5,5).hex())
print("distinct field2:",len(set(e[2] for e in ents)))
print("48-prefix:",len(ents[:48]),"distinct:",len(set(e[2] for e in ents[:48])))
# table end check: 143rd record ends at 0x19414
print("rec142:",rec(142).hex(),"addr",hex(T1+142*5),"rec143:",rec(143).hex())
rows=[]
for i,(a,h,f) in enumerate(ents):
    r=rec(f)
    rows.append(dict(idx=i, addr=f'0x{a:06X}', host=f'0x{h:04X}', hi=f'{h>>8:02X}', lo=f'{h&0xFF:02X}',
                     field2=f'0x{f:02X}', rec=f'0x{T1+f*5:06X}', flags=f'0x{r[0]:02X}',
                     pay=' '.join(f'{x:02X}' for x in r[1:])))
json.dump(rows,open('rows.json','w'),indent=0)
for r in rows:
    print(f"{r['idx']:2d} {r['host']} f2={r['field2']} rec={r['rec']} fl={r['flags']} pay={r['pay']}")
