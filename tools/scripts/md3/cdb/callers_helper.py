"""Shared helpers: call-target set and entry resolution."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import TEXT_LO, TEXT_HI, cfg
from capstone.x86 import X86_OP_IMM

def call_targets(ins):
    return sorted({i.operands[0].imm for i in ins
                   if i.mnemonic == 'call' and i.operands and i.operands[0].type == X86_OP_IMM
                   and TEXT_LO <= i.operands[0].imm < TEXT_HI})

def entry_of(va, targets):
    cands = [e for e in targets if e <= va]
    for e in reversed(cands):
        if va - e > 0x2000: break
        if va in cfg(e): return e
    return None
