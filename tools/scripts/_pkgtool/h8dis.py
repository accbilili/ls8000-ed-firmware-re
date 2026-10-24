
R8=["r0h","r1h","r2h","r3h","r4h","r5h","r6h","r7h","r0l","r1l","r2l","r3l","r4l","r5l","r6l","r7l"]
R16=["r0","r1","r2","r3","r4","r5","r6","r7","e0","e1","e2","e3","e4","e5","e6","e7"]
R32=["er0","er1","er2","er3","er4","er5","er6","sp"]
def s8(x): return x-256 if x>=128 else x
def s16(x): return x-65536 if x>=32768 else x
class H8:
    def __init__(self, data, entries, base=0):
        self.d=data; self.n=len(data); self.e=entries; self.base=base
    def u8(self,p): return self.d[p] if 0<=p<self.n else 0
    def u16(self,p): return (self.u8(p)<<8)|self.u8(p+1)
    def u32(self,p): return (self.u16(p)<<16)|self.u16(p+2)
    def am(self,a,pc,op,slot,size):
        epc=pc+size
        if a=="r8l": return R8[op&15]
        if a=="r8h": return R8[(op>>4)&15]
        if a=="r8u": return R8[(op>>8)&15]
        if a=="r16l": return R16[op&15]
        if a=="r16h": return R16[(op>>4)&15]
        if a=="r32l": return R32[op&7]
        if a=="r32h": return R32[(op>>4)&7]
        if a=="r16ih": return "@"+R16[(op>>4)&7]
        if a=="r16ihh": return "@"+R16[(op>>20)&7]
        if a=="pr16h": return "@-"+R16[(op>>4)&7]
        if a=="r16ph": return "@"+R16[(op>>4)&7]+"+"
        if a=="r16d16h": return "@(0x%x,%s)"%(self.u16(epc-2),R16[(op>>4)&7])
        if a=="r32ih": return "@"+R32[(op>>4)&7]
        if a=="r32ihh": return "@"+R32[(op>>20)&7]
        if a=="pr32h": return "@-"+R32[(op>>4)&7]
        if a=="r32pl": return "@"+R32[op&7]+"+"
        if a=="r32ph": return "@"+R32[(op>>4)&7]+"+"
        if a=="r32d16h": return "@(0x%x,%s)"%(self.u16(epc-2),R32[(op>>4)&7])
        if a=="r32d32hh": return "@(0x%x,%s)"%(self.u32(epc-4),R32[(op>>20)&7])
        if a=="psp": return "@-sp"
        if a=="spp": return "@sp+"
        if a=="r32n2l": return "%s-%s"%(R32[op&6],R32[(op&6)+1])
        if a=="r32n3l": return "%s-%s"%(R32[op&4],R32[(op&4)+2])
        if a=="r32n4l": return "%s-%s"%(R32[op&4],R32[(op&4)+3])
        if a=="abs8": return "@0x%06x"%(0xffff00|self.u8(pc+1))
        if a=="abs16":
            v=s16(self.u16(epc-4)) if slot==2 else s16(self.u16(epc-2)); return "@0x%06x"%(v&0xffffff)
        if a=="abs32": return "@0x%06x"%(self.u32(epc-6) if slot==3 else self.u32(epc-4))
        if a=="abs8i": return "@0x%02x"%self.u8(pc+1)
        if a=="abs16e": return "0x%04x"%self.u16(pc+2)
        if a=="abs22e": return "0x%06x"%(self.u32(pc)&0x3fffff)
        if a=="abs24e": return "0x%06x"%(self.u32(pc)&0xffffff)
        if a=="rel8": return "0x%06x"%((self.base+pc+2+s8(self.u8(pc+1)))&0xffffff)
        if a=="rel16": return "0x%06x"%((self.base+pc+4+s16(self.u16(pc+2)))&0xffffff)
        if a=="one": return "#1"
        if a=="two": return "#2"
        if a=="four": return "#4"
        if a=="imm2": return "#%x"%((op>>4)&3)
        if a=="imm3": return "#%x"%((op>>4)&7)
        if a=="imm6l": return "#%x"%(op&0x3f)
        if a=="imm8": return "#0x%02x"%self.u8(epc-1)
        if a=="imm16": return "#0x%04x"%self.u16(pc+2)
        if a=="imm32": return "#0x%08x"%self.u32(pc+2)
        if a in ("ccr","exr","bankl","bankh","macl","mach"): return a
        if a=="-": return None
        return "<%s>"%a
    def decode(self,pc):
        s0=self.u16(pc); s1=self.u32(pc); s2=(self.u16(pc)<<16)|self.u16(pc+4)
        s3=(self.u16(pc)<<16)|self.u16(pc+6); s4=self.u32(pc+2)
        slots=[s0,s1,s2,s3,s4]
        for e in self.e:
            if (slots[e["slot"]]&e["vm"])==e["vv"] and (s0&e["vm2"])==e["vv2"]:
                op=slots[e["slot"]]
                a1=self.am(e["am1"],pc,op,e["slot"],e["size"])
                a2=self.am(e["am2"],pc,op,e["slot"],e["size"])
                return e["size"], e["name"], a1, a2, pc+e["size"]
        return None,None,None,None,pc+2
    def iscall(self,nm): return nm in ("jsr","bsr")
    def isjmp(self,nm): return nm=="jmp"
    def iscond(self,nm): return nm in ("bra","brn","bhi","bls","bcc","bcs","bne","beq","bvc","bvs","bpl","bmi","bge","blt","bgt","ble","bt","bf")
