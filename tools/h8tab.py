
import re
def load_entries(path):
    ent=[]
    for l in open(path, encoding="utf-8", errors="replace"):
        m=re.match(r"^([0-9a-f]{2,8})\s+([0-9a-f]{2,8})\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)(?:\s+(\S+))?", l)
        if not m: continue
        val,mask,skip,name,am1,am2,ot=m.group(1),m.group(2),int(m.group(3)),m.group(4),m.group(5),m.group(6),(m.group(7) or "undefined")
        def hb(s): return [int(s[i:i+2],16) for i in range(0,len(s),2)]
        V,M=hb(val),hb(mask)
        if len(M)==2: slot=0; vm=(M[0]<<8)|M[1]; vv=(V[0]<<8)|V[1]; vm2=vv2=0
        elif len(M)==4:
            slot=skip+1; vm=(M[0]<<24)|(M[1]<<16)|(M[2]<<8)|M[3]; vv=(V[0]<<24)|(V[1]<<16)|(V[2]<<8)|V[3]; vm2=vv2=0
        else:
            slot=4; vm=(M[2]<<24)|(M[3]<<16)|(M[4]<<8)|M[5]; vv=(V[2]<<24)|(V[3]<<16)|(V[4]<<8)|V[5]
            vm2=(M[0]<<8)|M[1]; vv2=(V[0]<<8)|V[1]
        extra=0
        if (am1 in("abs16","abs16e","abs22e","abs24e") or am2 in("abs16","abs16e","abs22e","abs24e")) and skip==0: extra+=1
        if (am1=="abs32" or am2=="abs32") and skip==0: extra+=2
        if am1 in("imm16","rel16","r16d16h","r32d16h") or am2 in("imm16","rel16","r16d16h","r32d16h"): extra+=1
        if am1 in("imm32","r32d32hh") or am2 in("imm32","r32d32hh"): extra+=2
        ent.append(dict(slot=slot,vm=vm,vv=vv,vm2=vm2,vv2=vv2,size=len(V)+2*skip+2*extra,
                        name=name,am1=am1,am2=am2,ot=ot))
    # priority: h/undefined first, then o
    A=[e for e in ent if e["ot"]!="o"]; B=[e for e in ent if e["ot"]=="o"]
    return A+B
