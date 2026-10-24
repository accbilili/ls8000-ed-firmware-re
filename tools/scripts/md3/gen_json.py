"""Emit dispatch_caps.json from caps_raw.json."""
import json

d = json.load(open('caps_raw.json', encoding='utf-8'))
caps = d['caps']
meta = d['_meta']

groups = {}
for r in caps:
    groups.setdefault(r['group'], []).append(r['cap_id'])
gsum = {}
for g, ids in sorted(groups.items()):
    ids = sorted(ids)
    subs = [i & 0xFF for i in ids]
    # continuity
    runs = []
    a = b = subs[0]
    for x in subs[1:]:
        if x == b + 1:
            b = x
        else:
            runs.append((a, b))
            a = b = x
    runs.append((a, b))
    gsum[g] = dict(count=len(ids), subs=['%02X' % x for x in subs],
                   runs=['%02X-%02X' % r if r[0] != r[1] else '%02X' % r[0] for r in runs])

sel_tables = [
    dict(name='NkCtrlEntry.selector', export='?NkCtrlEntry@@YGFFFFPAX@Z', va='0x10091850',
         impl='0x10091D50', site='0x10091DBD', table='0x10091F88', entries=11,
         index='idx = selector - 1  (dec ebx @0x10091DB3, cmp ebx,0xA @0x10091DB4, ja @0x10091DB7)',
         specials=['0x0003,0x0004 -> 0x10091F34', '0x1000 -> 0x10091F7C', '0x2000 -> 0x10091F0F',
                   '0x2100 -> 0x10091EEA', 'default -> 0x10091EDA (ret 6)'],
         note='sel 3/4 的表格项 0x10091EDA 是死项，被 0x10091D8D 的 cmp ax,3/ax,4 提前截走'),
    dict(name='NkMDCtrlEntry.selector', export='NkMDCtrlEntry', va='0x1000B520',
         site='0x1000B52A', table='0x1000B57C', entries=4,
         index='idx = selector - 1  (dec eax @0x1000B524, cmp 3 @0x1000B525, ja @0x1000B528)',
         specials=['default 0x1000B571 -> eax=0x1001 (非法选择子)'], note='selector=5 落到 default'),
    dict(name='MAIDEntryPoint.func_id', export='MAIDEntryPoint', va='0x10027600',
         site='0x1002760E', table='0x10027840', entries=16,
         index='idx = funcId  (取 [esp+8] @0x10027600, cmp 0xF @0x10027604, ja @0x10027608, 无基址变换)',
         specials=['default 0x1002780E -> eax=0xFFFFFF81, 且有回调指针时先回调'], note='16/16 有效'),
]

meta['selector_tables'] = sel_tables
meta['cap_groups'] = gsum
meta['rdata_static_table'] = 'none: 42 段指针密集区全部是 C++ vtable, 指针前 2 字节恒为 0x1000..0x100B(上一指针高半字), 无 (u16 id,u32 handler) 记录'
meta['caveat'] = ('handler 是该能力 ID 分支里第一个被调用的构造函数; 若分支内联构造(cap 0x8007)则 handler=分支 VA; '
                  '构造器只完成对象建立, 能力行为在其 vtable 里')
json.dump({'_meta': meta, 'caps': caps}, open('dispatch_caps.json', 'w', encoding='utf-8'), indent=1)
print('caps', len(caps), 'groups', len(gsum))
for g in sorted(gsum):
    print(' ', g, gsum[g])
