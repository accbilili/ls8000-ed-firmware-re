"""从 36 份 fix_*.asm 提取语义信号：jsr/bsr 目标、绝对地址常量、关键助记符分布。

只读工作区已有产物，输出写本 _verify 目录。
"""
import os, re, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')

CALL = re.compile(r'\b(?:jsr|bsr)\s+(0x[0-9a-fA-F]+)')
ADDR = re.compile(r'@(0x[0-9a-fA-F]{5,8})')
IMM = re.compile(r'#(0x[0-9a-fA-F]{4,8})')
LINE = re.compile(r'^(0x[0-9A-Fa-f]{6})\s+(\S+)\s*(.*)$')

# 已知 RAM/常量符号表（来自工作区文档）
SYM = {
    '0x004001': '镜像选择字节', '0x004002': '状态码', '0x004008': 'E0/C1参数暂存区',
    '0x00400c': 'E0子功能码区', '0x004001': '镜像选择字节',
    '0x0040033c': '待发1394-CDB', '0x00400344': '1394描述块160B',
    '0x0040033a': '状态字节A', '0x0040033b': '状态字节B',
    '0x004003e4': '附加块8B', '0x00420736': '缝隙第3状态字节',
}


def analyze(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    lines = [l for l in txt.split('\n') if l.strip()]
    calls = collections.Counter()
    addrs = collections.Counter()
    imms = collections.Counter()
    mn = collections.Counter()
    for l in lines:
        m = LINE.match(l.strip())
        if not m:
            continue
        op, args = m.group(2).lower(), m.group(3)
        mn[op] += 1
        if op in ('jsr', 'bsr'):
            c = re.match(r'\s*(0x[0-9a-fA-F]+)', args)
            if c:
                calls[c.group(1).lower()] += 1
        for a in ADDR.findall(args):
            addrs[a.lower()] += 1
        for i in IMM.findall(args):
            imms[i.lower()] += 1
    return dict(lines=len(lines), calls=dict(calls.most_common()),
                addrs=dict(addrs.most_common(24)), imms=dict(imms.most_common(20)),
                mn=dict(mn.most_common()), path=os.path.basename(path))


def main():
    out = {}
    for f in sorted(os.listdir(JOBS)):
        if re.match(r'^fix_[0-9A-Fa-f]{6}\.asm$', f):
            out[f[:-4]] = analyze(os.path.join(JOBS, f))
    with open(os.path.join(HERE, 'sem_signal.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    for k, v in out.items():
        print('=' * 70)
        print(k, 'lines=', v['lines'])
        print('  calls:', v['calls'])
        print('  addrs:', v['addrs'])
        print('  imms :', v['imms'])


if __name__ == '__main__':
    main()
