"""Build capability-ID -> handler map for the factory switch at 0x10071A60."""
import json, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OPT_SYNTAX_INTEL
from pe_md3 import PE
import sim_factory as S

p = PE()
T = p.sections[0]
TLO, THI = T['va'], T['va'] + T['vsize']
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
md.syntax = CS_OPT_SYNTAX_INTEL

FACT = 0x10071A60
DEFAULT = 0x10073700

# site, table, base of `add eax,-base`, guard count, byte remap table or None
DENSE = [
    (0x10071D15, 0x10073720, 0x4004, 5,    None),
    (0x10071EF5, 0x10073734, 0x5006, 43,   0x10073780),
    (0x10072231, 0x100737AC, 0x5035, 177,  0x10073844),
    (0x100728D1, 0x100738F8, 0x50E7, 11,   None),
    (0x10072A7B, 0x10073924, 0x5208, 125,  0x10073948),
    (0x10072C14, 0x100739C8, 0x5408, 25,   0x100739EC),
    (0x10072DAD, 0x10073A08, 0x5423, 252,  0x10073A1C),
    (0x10072F5D, 0x10073B18, 0x6004, 12,   None),
    (0x100730DF, 0x10073B48, 0x6016, 21,   None),
    (0x10073468, 0x10073B9C, 0x8003, 12,   None),
    (0x100735E1, 0x10073BCC, 0x8101, 5,    None),
]


def valid(v):
    return v is not None and TLO <= v < THI


tstats = []
for site, tab, base, cnt, bmap in DENSE:
    nslots = cnt
    good = 0
    if bmap:
        idxs = [p.read(bmap + i, 1)[0] for i in range(cnt)]
        nslots = max(idxs) + 1
    for i in range(nslots):
        tgt = p.u32(tab + 4 * i)
        good += 1 if valid(tgt) else 0
    tstats.append(dict(site='0x%08X' % site, table='0x%08X' % tab, base='0x%04X' % base,
                       range_n=cnt, slots=nslots, valid=good,
                       byte_map=('0x%08X' % bmap) if bmap else None))
    print('  site 0x%08X tab 0x%08X base 0x%04X range=%3d slots=%3d valid=%3d bmap=%s' %
          (site, tab, base, cnt, nslots, good, ('0x%08X' % bmap) if bmap else '-'))

# ---- authoritative cap -> arm from the symbolic walk ----
res = {}
for cap in range(0x10000):
    arm, tag = S.run(cap)
    if tag == 'new':
        res[cap] = arm

# group by arm
by_arm = {}
for cap, arm in res.items():
    by_arm.setdefault(arm, []).append(cap)


def ctor_of(arm):
    t = S.ctor_after(arm)
    return t


rows = []
for arm in sorted(by_arm):
    c = ctor_of(arm)
    for cap in sorted(by_arm[arm]):
        rows.append(dict(
            cap_id=cap,
            cap_hex='0x%04X' % cap,
            handler=('0x%08X' % c[0]) if c else '0x%08X' % arm,
            arm='0x%08X' % arm,
            ctor_site=('0x%08X' % c[1]) if c else None,
            group='0x%02X' % (cap >> 8),
            sub='0x%02X' % (cap & 0xFF),
        ))
rows.sort(key=lambda r: r['cap_id'])

# group summary
gsum = {}
for r in rows:
    g = r['group']
    gsum.setdefault(g, []).append(r['cap_id'])
print('\ngroups:')
for g in sorted(gsum):
    ids = sorted(gsum[g])
    print('  %s : %3d  sub=%s' % (g, len(ids), ','.join('%02X' % (i & 0xFF) for i in ids)))

meta = dict(
    entry_function='0x10071A60',
    entry_sig='void* __cdecl Create(u16 capId, u16 subId, void** out)',
    dispatch_kind='比较树 (cmp/je) + 11 张稠密跳转表 + 4 张字节重映射表；MSVC switch 降级',
    index_formula='dense: i = capId - base; j = bmap[i] (若有字节表, 否则 j=i); target = *(u32*)(table + 4*j)',
    cmp_tree=[0x10071A60, 0x100737E0],
    default_arm='0x10073700',
    tables=tstats,
    reachable_from='MAIDEntryPoint 0x10027600 (id 5..9,13) -> 0x100250A0 -> 0x100251DB -> 0x10071A60',
    total_caps=len(rows),
    distinct_arms=len(by_arm),
    groups={g: len(v) for g, v in gsum.items()},
)
json.dump({'_meta': meta, 'caps': rows}, open('caps_raw.json', 'w', encoding='utf-8'), indent=0)
print('\ntotal caps %d, arms %d' % (len(rows), len(by_arm)))
