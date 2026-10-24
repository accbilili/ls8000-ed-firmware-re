# -*- coding: utf-8 -*-
# st_emit.py — 生成 statics.json
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import re, json, struct, os, datetime
P = sample('driver/LS8000.md3')
OUT = r'<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\03_analysis\md3\statics.json'
W = os.path.dirname(os.path.abspath(__file__))
d = open(P, 'rb').read()
IB = 0x10000000
SEC = [('.text', 0x1000, 0xBD000, 0x10001000, 0xBCA9A),
       ('.rdata', 0xBE000, 0x13000, 0x100BE000, 0x127F8),
       ('.data', 0xD1000, 0x8000, 0x100D1000, 0x8E08),
       ('.rsrc', 0xD9000, 0x7000, 0x100DA000, 0x6008)]

# ---- 引用索引：.text 中指向 .rdata/.data 的 imm32 ----
text = d[0x1000:0x1000+0xBD000]; TV = 0x10001000
refs = {}
for i in range(len(text)-4):
    v = struct.unpack_from('<I', text, i)[0]
    if 0x100BE000 <= v < 0x100E0000:
        refs.setdefault(v, []).append(TV+i)

# ---- ASCII 串 ----
strings = []
for name, praw, rs, v, vs in SEC:
    if name not in ('.rdata', '.data'):
        continue
    buf = d[praw:praw+min(rs, vs)]
    for m in re.finditer(rb'[\x20-\x7E]{4,}', buf):
        va = v + m.start()
        t = m.group().decode('latin1')
        rr = []
        for k in range(0, min(len(t), 24)):
            rr += refs.get(va+k, [])
        strings.append({'va': hex(va), 'text': t, 'enc': 'A', 'sec': name,
                        'refs': [hex(x) for x in sorted(set(rr))]})
# ---- RT_STRING ----
strtab = json.load(open(os.path.join(W, 'st_strtab.json')))
for s in strtab:
    strings.append({'va': s['va'], 'text': s['text'], 'enc': 'U', 'sec': '.rsrc',
                    'id': s['id'], 'src': 'RT_STRING', 'refs': []})
strings.sort(key=lambda x: int(x['va'], 16))

# ---- 表 ----
tables = [
 {'va': '0x100D0798', 'count': 3, 'width': 4, 'kind': 'u32 RVA[]',
  'note': '导出函数 RVA 表 {0x91850 NkCtrlEntry, 0x27600 MAIDEntryPoint, 0xB520 NkMDCtrlEntry}；被 0x100D0780 描述符 +0x0C 指向'},
 {'va': '0x100D07A4', 'count': 3, 'width': 4, 'kind': 'char*[]',
  'note': '导出名指针表 {0x100D07C1 "?NkCtrlEntry@@YGFFFFPAX@Z", 0x100D07DB "MAIDEntryPoint", 0x100D07EA "NkMDCtrlEntry"}'},
 {'va': '0x100D07B0', 'count': 1, 'width': 6, 'kind': 'u16[3]+char[]',
  'note': '{0,1,2} + "LS8000.md3"，模块名/序号描述符'},
 {'va': '0x100D1000', 'count': 15, 'width': 4, 'kind': 'vftable',
  'note': '首项 0，后 13 项为 .text 函数指针（0x100B828F…0x100BD900），末项 0'},
 {'va': '0x100D1158', 'count': 128, 'width': 8, 'kind': 'double[128]',
  'note': 'EV/增益阶梯：4 段 × 32 项；[0..31] 为 EV 设定 -3.00…+1.30（步长 0.15），[32..] 为对应增益倍数 0.316…3.11 / 0.737…3.425 / 0.886…4.038'},
 {'va': '0x100C7040', 'count': 128, 'width': 1, 'kind': 'u8[128]',
  'note': '0x00..0x7F 递增字节表（CRT ctype 区，非 Nikon 参数）'},
]
for t in tables:
    t['refs'] = [hex(x) for x in refs.get(int(t['va'], 16), [])]

out = {
 'meta': {
   'file': P, 'size': len(d),
   'imagebase': '0x10000000',
   'timestamp': 1170779456, 'timestamp_utc': '2007-02-06',
   'note': 'LS8000.md3 = Nikon Scan 的 LS-8000(E) 扫描仪 MAID 模块；本文件仅静态数据，不含代码语义结论',
 },
 'exports': json.load(open(os.path.join(W, 'st_pe.json')))['exports'],
 'imports': json.load(open(os.path.join(W, 'st_pe.json')))['imports'],
 'dynamic_loads': [
   {'dll': 'ICEDLL.dll', 'site': '0x10002A55', 'gpa': '0x10002A86',
    'funcs': ['DICELoad(0x100BE548)','DICEUnload','DICEVersion','DICENew','DICEDelete','DICEInit','DICEBegin',
              'DICEEnd','DICEAbort','DICEProcess','DICEComplete','DICEQueueInputBuff','DICEQueueOutputBuff',
              'DICEDequeueInputBuff','DICEDequeueOutputBuff','DICENeedInputBuff','DICENeedOutputBuff','DICEGetDefectPercent'],
    'hmod_global': '0x100D8440'},
   {'dll': 'Nkduscan.dll', 'site': '0x1009A5F5', 'gpa': '0x10099F64',
    'funcs': ['NkDriverEntry(0x100C2578)'], 'hmod': '[obj+8]', 'proc': '[obj+4]'},
   {'dll': 'Nkdsbp2.dll', 'site': '0x1009A615', 'gpa': '0x10099F64',
    'funcs': ['NkDriverEntry(0x100C2578)'], 'hmod': '[obj+8]', 'proc': '[obj+4]'},
   {'dll': 'user32.dll', 'site': '0x100B777B', 'gpa': '0x100B778B', 'funcs': ['MessageBoxA','GetActiveWindow','GetLastActivePopup','GetUserObjectInformationA','GetProcessWindowStation']},
 ],
 'scsi_api_scan': {
   'DeviceIoControl': 0, 'SCSI_PASS_THROUGH': 0, 'IOCTL_SCSISCAN': 0, '\\\\\\\\.\\\\': 0,
   'conclusion': '全文件 0 命中：md3 不直接下发 SCSI，全部经 Nkduscan.dll/Nkdsbp2.dll 的 NkDriverEntry [实证]',
 },
 'version': {
   'va': '0x100DAAF8', 'size': 840,
   'FixedFileInfo': {'FileVersion': '1, 3, 0, 3003', 'ProductVersion': '4, 0, 0, 0'},
   'StringFileInfo': {'040901B5': {
     'Comments': 'Nikon Scan Driver', 'CompanyName': 'Nikon Corporation',
     'FileDescription': 'Nikon Scan Driver', 'FileVersion': '1, 3, 0, 3003',
     'InternalName': 'LS8000', 'LegalCopyright': 'Copyright (C) Nikon Corporation. 1995 - 2007',
     'OriginalFilename': 'LS8000.MD3', 'ProductName': 'Nikon Scan', 'ProductVersion': '4, 0, 0, 0'}},
   'Translation': '0x0409 0x01B5（但实际资源语言为 1041 日语）',
 },
 'module_descriptor': {
   'va': '0x100D0780',
   'layout': '+0x00 u32=1 | +0x04 u32=3 | +0x08 u32=3 | +0x0C -> 0x100D0798(RVA[3]) | +0x10 -> 0x100D07A4(name*[3]) | +0x14 -> 0x100D07B0(u16[3]+"LS8000.md3")',
 },
 'signature_check': {
   'string_va': '0x100BE708', 'text': 'Nikon MD3.01IILS8000  ', 'len': 23,
   'sites': ['0x10008BB3', '0x10009C02', '0x1001A42A', '0x1001AC3B', '0x1001AED1'],
   'note': '5 处 memcmp(...,23) 校验模块型号签名，单机型硬绑定 [实证]',
 },
 'strings': strings,
 'tables': tables,
}
s = json.dumps(out, ensure_ascii=False, indent=0)
open(OUT, 'w', encoding='utf-8').write(s)
print('wrote', OUT, len(s), 'bytes; strings=', len(strings), 'imports=', len(out['imports']))
