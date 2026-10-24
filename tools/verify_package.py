"""
LS8000 固件逆向交付包 —— 完整性校验

逐文件比对 MANIFEST.txt 中的 SHA256 与字节数，确认交付包未被篡改或损坏。

用法
----
    python verify_package.py                  # 校验当前包
    python verify_package.py <包根目录>        # 校验指定目录

退出码
------
    0 = 全部通过
    1 = 找不到 MANIFEST.txt
    2 = 存在异常（缺失 / 大小不符 / 哈希不符）
"""
import hashlib
import os
import re
import sys


def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def find_root(start):
    """从 start 向上查找含 MANIFEST.txt 的目录。"""
    p = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(p, 'MANIFEST.txt')):
            return p
        q = os.path.dirname(p)
        if q == p:
            return None
        p = q


def verify(root):
    mf = os.path.join(root, 'MANIFEST.txt')
    if not os.path.isfile(mf):
        print('找不到 MANIFEST.txt: %s' % mf)
        return 1

    # MANIFEST 行格式： SHA256  字节数  相对路径
    # 用正则精确切分（路径可能含中文与多空格，split 会错位）
    line_re = re.compile(r'^([0-9a-fA-F]{64})\s+(\d+)\s+(\S.*)$')
    rows = []
    for line in open(mf, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#'):
            continue
        m = line_re.match(line)
        if not m:
            continue
        rows.append((m.group(1), int(m.group(2)), m.group(3).strip()))

    missing, mismatch, ok = [], [], 0
    for h, size, rel in rows:
        p = os.path.join(root, rel.replace('/', os.sep))
        if not os.path.isfile(p):
            missing.append(rel)
            continue
        if os.path.getsize(p) != size:
            mismatch.append((rel, '大小 %d != 清单 %d' % (os.path.getsize(p), size)))
            continue
        if sha256_of(p) != h:
            mismatch.append((rel, 'SHA256 不符'))
            continue
        ok += 1

    # 反向检查：包内存在但清单未收录的文件
    listed = {r[2] for r in rows}
    extra = []
    # 版本控制、CI 配置与样本目录属于仓库治理文件，不计入「清单未收录」。
    # Version-control, CI config and sample dirs are repo-housekeeping files and
    # must not be reported as "unlisted" — otherwise every clone would fail.
    # 注意：samples/ 已纳入版本库（官方固件原件），故不在排除列表内。
    EXCLUDE_DIRS = {'__pycache__', '.git', '.github'}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), root).replace('\\', '/')
            if rel == 'MANIFEST.txt' or rel in listed:
                continue
            extra.append(rel)

    print('LS8000 交付包完整性校验')
    print('=' * 62)
    print('  包根      : %s' % root)
    print('  清单条目  : %d' % len(rows))
    print('  通过      : %d' % ok)
    print('  缺失      : %d' % len(missing))
    print('  不符      : %d' % len(mismatch))
    print('  未收录    : %d' % len(extra))
    print()

    if missing:
        print('【缺失文件】')
        for r in missing[:50]:
            print('  - %s' % r)
        if len(missing) > 50:
            print('  ... 另有 %d 个' % (len(missing) - 50))
        print()
    if mismatch:
        print('【校验不符】')
        for r, why in mismatch[:50]:
            print('  - %s' % r)
            print('      %s' % why)
        if len(mismatch) > 50:
            print('  ... 另有 %d 个' % (len(mismatch) - 50))
        print()
    if extra:
        print('【清单未收录】（新增文件，不影响完整性，但提示包已改动）')
        for r in extra[:30]:
            print('  + %s' % r)
        if len(extra) > 30:
            print('  ... 另有 %d 个' % (len(extra) - 30))
        print()

    bad = len(missing) + len(mismatch)
    if bad == 0:
        print('结论: 全部通过 ✓')
    else:
        print('结论: 存在 %d 个异常 ✗' % bad)
    return 0 if bad == 0 else 2


if __name__ == '__main__':
    if len(sys.argv) > 1:
        root = os.path.abspath(sys.argv[1])
    else:
        root = find_root(os.path.dirname(os.path.abspath(__file__))) or os.getcwd()
    sys.exit(verify(root))
