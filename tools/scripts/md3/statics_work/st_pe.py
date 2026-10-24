# -*- coding: utf-8 -*-
# st_pe.py — LS8000.md3 PE 头 / 导入 / 导出 / 资源 全解（只读）
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import json, os
import pefile

P = sample('driver/LS8000.md3')
OUT = os.path.dirname(os.path.abspath(__file__))
pe = pefile.PE(P, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
out = {'imgbase': hex(IB)}
out['machine'] = hex(pe.FILE_HEADER.Machine)
out['timestamp'] = pe.FILE_HEADER.TimeDateStamp
import datetime
out['ts_str'] = str(datetime.datetime.utcfromtimestamp(pe.FILE_HEADER.TimeDateStamp))
out['subsystem'] = pe.OPTIONAL_HEADER.Subsystem
out['dllchar'] = hex(pe.OPTIONAL_HEADER.DllCharacteristics)
out['size_of_image'] = hex(pe.OPTIONAL_HEADER.SizeOfImage)
out['entry'] = hex(IB + pe.OPTIONAL_HEADER.AddressOfEntryPoint)
out['sections'] = [{'name': s.Name.rstrip(b'\x00').decode('latin1'),
                    'va': hex(IB + s.VirtualAddress), 'vs': hex(s.Misc_VirtualSize),
                    'praw': hex(s.PointerToRawData), 'rs': hex(s.SizeOfRawData)}
                   for s in pe.sections]

pe.parse_data_directories(directories=[
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT']])

imps = []
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        for f in e.imports:
            imps.append({'dll': e.dll.decode('latin1'),
                         'name': f.name.decode('latin1') if f.name else 'ord#%d' % f.ordinal,
                         'iat_va': hex(IB + f.address)})
out['imports'] = imps
out['delay_imports'] = []
if hasattr(pe, 'DIRECTORY_ENTRY_DELAY_IMPORT'):
    for e in pe.DIRECTORY_ENTRY_DELAY_IMPORT:
        for f in e.imports:
            out['delay_imports'].append({'dll': str(e.dll), 'name': f.name.decode('latin1') if f.name else '?'})
out['exports'] = [{'ord': s.ordinal, 'name': s.name.decode('latin1') if s.name else None,
                   'va': hex(IB + s.address)}
                  for s in getattr(pe.DIRECTORY_ENTRY_EXPORT, 'symbols', [])] if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else []

res = []
def walk(entries, path, typ):
    for e in entries:
        nm = str(e.id) if e.name is None else e.name.string.decode('utf-16le', 'ignore')
        if getattr(e, 'directory', None):
            walk(e.directory.entries, path + [nm], typ if typ else nm)
        elif getattr(e, 'data', None) is not None:
            st = e.data.struct
            res.append({'type': typ, 'name': nm, 'lang': path[-1],
                        'rva': st.OffsetToData, 'va': IB + st.OffsetToData,
                        'size': st.Size,
                        'data': pe.get_data(st.OffsetToData, st.Size)})
if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    walk(pe.DIRECTORY_ENTRY_RESOURCE.entries, [], None)

out['resources'] = [{'type': r['type'], 'name': r['name'], 'lang': r['lang'],
                     'va': hex(r['va']), 'size': r['size']} for r in res]
json.dump(out, open(os.path.join(OUT, 'st_pe.json'), 'w'), indent=1, ensure_ascii=False)

print('== sections ==')
for s in out['sections']:
    print(' ', s['name'], s['va'], s['vs'], s['praw'], s['rs'])
print('== exports ==')
for e in out['exports']:
    print(' ', e['ord'], e['name'], e['va'])
print('== imports: %d funcs / %d dlls ==' % (len(imps), len({i['dll'] for i in imps})))
cur = None
for i in imps:
    if i['dll'] != cur:
        cur = i['dll']; print(' [%s]' % cur)
    print('   %-38s iat=%s' % (i['name'], i['iat_va']))
print('== delay imports ==', out['delay_imports'])
print('== resources ==')
for r in out['resources']:
    print(' type=%-5s name=%-6s lang=%s %s %d' % (r['type'], r['name'], r['lang'], r['va'], r['size']))

for r in res:
    if r['type'] == '16':
        fn = os.path.join(OUT, 'st_version.bin')
        open(fn, 'wb').write(r['data'])
        print('wrote', fn, len(r['data']))
    if r['type'] == '6':
        fn = os.path.join(OUT, 'st_strtab.bin')
        open(fn, 'wb').write(r['data'])
        print('wrote', fn, len(r['data']))
