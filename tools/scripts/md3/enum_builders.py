"""Enumerate CDB-builder functions: functions that write byte at [reg+8] and return 6/10."""
import sys, os, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md3lib import *
from oracle import D, cfg, sweep
from fnresolve import entry_of, callers_of
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

hits = pickle.load(open('memwr.pkl','rb'))
# byte writes at disp == 8 (CDB buffer offset in command object)
cand = [h for h in hits if h[3]==1 and h[2]==8]
print('byte-writes at disp 8:', len(cand))

groups = collections.defaultdict(list)
for va, base, disp, sz, val in cand:
    e = entry_of(va)
    groups[e].append((va, val))

print('distinct enclosing functions:', len(groups))
for e in sorted(groups, key=lambda x: (x is None, x or 0)):
    ls = sorted(groups[e])
    body = cfg(e) if e else {}
    ret6 = ret10 = False
    for a in sorted(body):
        i = body[a]
        if i.mnemonic=='mov' and i.operands and i.operands[0].type==0 and i.op_str.startswith('eax, '):
            v = i.op_str[5:]
            if v in ('6','0xa','0x0a'): ret6 = True
            if v in ('0xa','0x0a','10'): ret10 = True
    print('fn 0x%08X size=%-4d ret6=%-5s cdb0writes=%s' %
          (e or 0, len(body), ret6, [(hex(a), hex(v) if v is not None else 'r') for a,v in ls]))
