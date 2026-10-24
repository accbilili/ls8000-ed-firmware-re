#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
codec_probe.py —— FIRMDATA 是否经过压缩/编码的只读探测工具

纪律
  * 目标文件以 'rb' 打开，仅读取，绝不写入。
  * 只有真正解出数据时才报告"某算法存在"；否则一律报告"未检出（≠ 不存在）"。
  * 第 5 项（指令集）只给弱证据，脚本内不做架构断言。

用法
  python codec_probe.py                 # 全部检测
  python codec_probe.py --skip-scan     # 跳过最慢的逐字节解压扫描
  python codec_probe.py --json out.json
"""
import argparse
import bz2
import collections
import json
import lzma
import math
import random
import sys
import time
import zlib

TARGET = (r"<HOME>/Videos/LS8000fw111_win/SUPERCOOLSCAN8000ED_111"
          r"/.rsrc/0/RCDATA/FIRMDATA")

SCAN_WINDOW = 64 * 1024      # 前 64KB 逐字节扫描
SCAN_INPUT = 8192            # 每个起点最多投喂 8KB
MIN_OK = 1024                # "解出了东西"的门槛
LOG2 = math.log(2.0)


# ========================= 基础统计 =========================
def entropy(counts, n):
    if n <= 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c:
            p = c / n
            h -= p * math.log(p, 2)
    return h


def mm_correction(bins_possible, n):
    """Miller-Madow 偏差修正量 ≈ (m-1)/(2 n ln2)。m 必须用**字母表大小**，
    不能用"观测到的非空箱数"，否则严重低估偏差。"""
    if n <= 0:
        return 0.0
    return (bins_possible - 1) / (2.0 * n * LOG2)


def chi2_uniform(counts, n):
    k = len(counts)
    exp = n / k
    return sum((c - exp) ** 2 / exp for c in counts), k - 1


def byte_counts(data):
    c = collections.Counter(data)
    return [c.get(i, 0) for i in range(256)]


def collision_stats(data, width):
    n = len(data) // width
    ctr = collections.Counter()
    for i in range(n):
        ctr[data[i * width:(i + 1) * width]] += 1
    obs_pairs = sum(v * (v - 1) // 2 for v in ctr.values())
    m = 1 << (8 * width)
    exp_pairs = n * (n - 1) / 2.0 / m
    obs_distinct = len(ctr)
    exp_distinct = m * (1.0 - math.exp(-n / float(m)))
    return n, obs_pairs, exp_pairs, obs_distinct, exp_distinct, ctr


def max_run(data):
    best, cur, bestb = 1, 1, data[0] if data else 0
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            cur += 1
            if cur > best:
                best, bestb = cur, data[i]
        else:
            cur = 1
    return best, bestb


# ========================= 1) 标准流解压扫描 =========================
def _try_zlib(blob, wbits, min_out=MIN_OK):
    try:
        d = zlib.decompressobj(wbits)
        out = d.decompress(blob, min_out * 2)
        if d.unconsumed_tail:
            out += d.decompress(d.unconsumed_tail, 65536)
        return len(out), bool(d.eof), out[:32]
    except Exception:
        return None


def _try_bz2(blob, min_out=MIN_OK):
    try:
        d = bz2.BZ2Decompressor()
        out = d.decompress(blob, min_out * 2)
        return len(out), bool(d.eof), out[:32]
    except Exception:
        return None


def _try_lzma(blob, fmt, min_out=MIN_OK):
    try:
        d = lzma.LZMADecompressor(format=fmt)
        out = d.decompress(blob, min_out * 2)
        return len(out), bool(d.eof), out[:32]
    except Exception:
        return None


def find_magic(data):
    pats = {b'\x1f\x8b': 'gzip', b'\x5d\x00\x00': 'lzma_alone_5d0000',
            b'BZh': 'bzip2', b'\xfd7zXZ\x00': 'xz'}
    out = {}
    for m, name in pats.items():
        pos, s = [], 0
        while True:
            p = data.find(m, s)
            if p < 0:
                break
            pos.append(p)
            s = p + 1
        out[name] = {'count': len(pos), 'first20': pos[:20]}
    zh = []
    for i in range(len(data) - 2):
        if data[i] == 0x78 and data[i + 1] in (0x01, 0x5e, 0x9c, 0xda):
            if (data[i] << 8 | data[i + 1]) % 31 == 0:
                zh.append(i)
    out['zlib_header'] = {'count': len(zh), 'first20': zh[:20]}
    return out


def confirm_candidate(data, off, wbits, cap=32 << 20):
    """对扫描得到的候选起点做"全量确认"。
    真正的压缩流应当：喂完剩余全部数据后 eof=True（流自然结束），
    且解出内容长度与输入不呈 1:1（假阳性常表现为输出≈输入）。
    """
    blob = data[off:off + cap]
    try:
        d = zlib.decompressobj(wbits)
        out = d.decompress(blob, cap)
        eof = bool(d.eof)
        err = None
    except Exception as e:
        return {'offset': off, 'eof': False, 'error': str(e)[:80],
                'out_len': 0, 'entropy': None}
    c = collections.Counter(out)
    e = entropy(c.values(), len(out)) if out else 0.0
    consumed = len(blob) - len(d.unused_data) - len(d.unconsumed_tail)
    return {'offset': off, 'eof': eof, 'error': err, 'out_len': len(out),
            'in_len': len(blob), 'consumed_in': consumed,
            'expand_ratio': round(len(out) / len(blob), 4),
            'entropy': round(e, 3), 'head_hex': out[:24].hex(),
            'verdict': ('候选成立' if (eof and len(out) > MIN_OK) else
                        '假阳性（未自然结束/输出≈输入/高熵乱码）')}


def scan_streams(data, do_scan=True):
    res = {'magic': find_magic(data)}
    win = min(len(data), SCAN_WINDOW)
    res['window'] = win

    for name, wb in (('raw_deflate_wbits-15', -15), ('zlib_wbits15', 15),
                     ('gzip_wbits31', 31)):
        t0 = time.time()
        best = (0, -1, False, b'')
        n_any = n_1k = 0
        cands = []
        for off in range(win):
            b0 = data[off]
            # 头字段预筛与 zlib 自身的头校验等价，只是提前短路，不改变"是否存在"的结论
            if wb == 15:
                if (b0 & 0x0F) != 8 or off + 1 >= len(data):
                    continue
                if ((b0 << 8) | data[off + 1]) % 31 != 0:
                    continue
            elif wb == 31:
                if b0 != 0x1F or off + 1 >= len(data) or data[off + 1] != 0x8B:
                    continue
            r = _try_zlib(data[off:off + SCAN_INPUT], wb)
            if r and r[0] > 0:
                n_any += 1
                if r[0] >= MIN_OK:
                    n_1k += 1
                    cands.append(off)
                    if r[0] > best[0]:
                        best = (r[0], off, r[1], r[2])
        res[name] = {'offsets_considered': win, 'offsets_with_output': n_any,
                     'offsets_gt_1KB': n_1k, 'best_out_len': best[0],
                     'best_offset': best[1], 'best_eof_clean': best[2],
                     'best_head_hex': best[3].hex(),
                     'elapsed_s': round(time.time() - t0, 2)}
        # 对 >1KB 的候选做全量确认
        res[name]['confirmed'] = [confirm_candidate(data, o, wb)
                                  for o in cands[:8]]

    t0 = time.time()
    bb = (0, -1, False)
    for off in range(win):
        if not data.startswith(b'BZh', off):
            continue
        r = _try_bz2(data[off:off + SCAN_INPUT])
        if r and r[0] > bb[0]:
            bb = (r[0], off, r[1])
    res['bz2'] = {'offsets_considered': win, 'best_out_len': bb[0],
                  'best_offset': bb[1], 'best_eof_clean': bb[2],
                  'elapsed_s': round(time.time() - t0, 2)}

    t0 = time.time()
    lb = (0, -1, False)
    tried = 0
    for off in range(win):
        if data[off] > 0xE0:          # lzma-alone 属性字节上限
            continue
        tried += 1
        r = _try_lzma(data[off:off + SCAN_INPUT], lzma.FORMAT_ALONE)
        if r and r[0] > lb[0]:
            lb = (r[0], off, r[1])
    res['lzma_alone'] = {'offsets_considered': tried, 'best_out_len': lb[0],
                         'best_offset': lb[1], 'best_eof_clean': lb[2],
                         'elapsed_s': round(time.time() - t0, 2)}

    xz = []
    for p in res['magic']['xz']['first20']:
        r = _try_lzma(data[p:p + (1 << 20)], lzma.FORMAT_XZ)
        if r:
            xz.append([p, r[0]])
    res['xz'] = {'candidates': len(xz), 'hits': xz}

    # ---- 零假设对照：同一套 raw-deflate 扫描跑在 (a) 打乱序列 (b) 均匀随机 上 ----
    # 若真实数据的命中数与对照相当，则"命中"只是概率性假阳性，不构成证据。
    if do_scan:
        ctrl = {}
        rnd = random.Random(7)
        variants = {'shuffled': bytes(rnd.sample(data, len(data))),
                    'uniform_random': bytes(rnd.getrandbits(8) for _ in range(len(data)))}
        for name, blob in variants.items():
            n_any = n_1k = 0
            best = 0
            for off in range(win):
                rr = _try_zlib(blob[off:off + SCAN_INPUT], -15)
                if rr and rr[0] > 0:
                    n_any += 1
                    best = max(best, rr[0])
                    if rr[0] >= MIN_OK:
                        n_1k += 1
            ctrl[name] = {'offsets_with_output': n_any, 'offsets_gt_1KB': n_1k,
                          'best_out_len': best}
        res['null_control_raw_deflate'] = ctrl

        # 多轮打乱：估计"偶然解出 >1KB"的假阳性率
        reps = []
        for s in range(12):
            r2 = random.Random(1000 + s)
            blob = bytes(r2.sample(data, len(data)))
            n1k = 0
            best = 0
            for off in range(win):
                rr = _try_zlib(blob[off:off + SCAN_INPUT], -15)
                if rr and rr[0] > 0:
                    best = max(best, rr[0])
                    if rr[0] >= MIN_OK:
                        n1k += 1
            reps.append({'seed': 1000 + s, 'offsets_gt_1KB': n1k, 'best_out_len': best})
        res['null_control_reps'] = {
            'n_shuffles': len(reps), 'reps': reps,
            'mean_gt1KB': round(sum(x['offsets_gt_1KB'] for x in reps) / len(reps), 2),
            'max_best_out': max(x['best_out_len'] for x in reps)}
    return res


# ========================= 2) 分布 / 重复 / 游程 =========================
def distribution_tests(data):
    n = len(data)
    counts = byte_counts(data)
    h = entropy(counts, n)
    chi2, df = chi2_uniform(counts, n)
    out = {'n': n, 'distinct_bytes': sum(1 for c in counts if c),
           'entropy_bits': round(h, 4),
           'entropy_bits_mm': round(h + mm_correction(256, n), 4),
           'chi2': round(chi2, 1), 'df': df, 'chi2_per_df': round(chi2 / df, 2),
           'chi2_crit_df255': {'p=0.05': 293.2, 'p=0.001': 330.5, 'p=1e-6': 400.0},
           'exp_per_bin': round(n / 256.0, 2),
           'top8': [[hex(i), counts[i], round(counts[i] / n * 100, 2)]
                    for i in sorted(range(256), key=lambda i: -counts[i])[:8]],
           'bottom3': [[hex(i), counts[i]] for i in
                       sorted(range(256), key=lambda i: counts[i])[:3]],
           'monobit': None}

    total_bits = 8 * n
    ones = sum(bin(b).count('1') for b in data)
    out['monobit'] = {'ones': ones, 'bits': total_bits,
                      'ratio': round(ones / total_bits, 5),
                      'z': round((ones - total_bits / 2) /
                                 (math.sqrt(total_bits) / 2), 2)}

    rep = {}
    tops = {}
    for w in (2, 3, 4):
        ns, obs, exp, od, ed, ctr = collision_stats(data, w)
        rep[f'{w}B'] = {'samples': ns, 'obs_pairs': obs, 'exp_pairs': round(exp, 3),
                        'ratio_vs_random': round(obs / exp, 3) if exp else None,
                        'obs_distinct': od, 'exp_distinct': round(ed, 1),
                        'distinct_ratio': round(od / ed, 4) if ed else None}
        if w >= 3:
            tops[f'{w}B'] = [[v.hex(), c] for v, c in ctr.most_common(8)]
    out['repeat'] = rep
    out['repeat_top'] = tops

    # 4 字节重复的偏移分布（看是否成对/周期性出现）
    _, _, _, _, _, c4 = collision_stats(data, 4)
    dup = [(v, c) for v, c in c4.items() if c > 1]
    dup.sort(key=lambda x: -x[1])
    offs = []
    for v, c in dup[:5]:
        pos, s = [], 0
        while True:
            p = data.find(v, s)
            if p < 0:
                break
            pos.append(p)
            s = p + 1
        offs.append([v.hex(), c, pos[:12]])
    out['dup4_offsets'] = offs

    mr, mb = max_run(data)
    out['max_run'] = {'len': mr, 'byte': hex(mb),
                      'expected_iid': round(math.log(n) / math.log(256), 2)}
    return out


# ========================= 3) 位打包检测 =========================
def bitpack_tests(data):
    n = len(data)
    ones = [0] * 8
    for b in data:
        for k in range(8):
            if b >> k & 1:
                ones[k] += 1
    bit_p = [round(ones[k] / n, 4) for k in range(8)]

    hi, lo = [0] * 16, [0] * 16
    for b in data:
        hi[b >> 4] += 1
        lo[b & 0xF] += 1

    nw = n // 2
    words = [(data[2 * i] << 8) | data[2 * i + 1] for i in range(nw)]
    top_nib = [0] * 16
    for w in words:
        top_nib[w >> 12] += 1
    wbits = [0] * 16
    for w in words:
        for k in range(16):
            if w >> (15 - k) & 1:
                wbits[k] += 1
    wbit_p = [round(wbits[k] / nw, 4) for k in range(16)]
    active = [k for k in range(16) if 0.02 < wbit_p[k] < 0.98]

    # 固定位宽假设：若高 k 位恒为 0，则字值 <2^(16-k)
    frac_below = {str(b): round(sum(1 for w in words if w < (1 << b)) / nw, 4)
                  for b in (8, 10, 12, 14)}

    def unpack12(order):
        v, i = [], 0
        while i + 3 <= n:
            a, b, c = data[i], data[i + 1], data[i + 2]
            if order == 'be':
                v.append((a << 4) | (b >> 4))
                v.append(((b & 0xF) << 8) | c)
            else:
                v.append(((b >> 4) << 8) | a)
                v.append((c << 4) | (b & 0xF))
            i += 3
        return v

    u12 = {}
    for o in ('be', 'le'):
        v = unpack12(o)
        c12 = collections.Counter(v)
        h12 = entropy([c12.get(i, 0) for i in range(4096)], len(v))
        u12[o] = {'values': len(v), 'entropy_bits': round(h12, 4),
                  'entropy_mm': round(h12 + mm_correction(4096, len(v)), 4),
                  'mean': round(sum(v) / len(v), 1),
                  'frac_top_bit_set': round(sum(1 for x in v if x & 0x800) / len(v), 4)}

    cw = collections.Counter(words)
    hw = entropy(cw.values(), nw)
    hb = entropy(byte_counts(data), n)

    # 奇偶位字节画像：若为 16 位大端指令流，偶数位(操作码)应显著偏向 <0x80，
    # 且奇偶两侧的字节直方图应明显不同。
    even, odd = data[0::2], data[1::2]
    def prof(s):
        return {'n': len(s), 'frac_lt_0x80': round(sum(1 for b in s if b < 0x80) / len(s), 4),
                'frac_lt_0x10': round(sum(1 for b in s if b < 0x10) / len(s), 4),
                'top3': [[hex(v), round(k / len(s), 4)]
                         for v, k in collections.Counter(s).most_common(3)]}
    parity = {'even': prof(even), 'odd': prof(odd)}
    parity['frac_lt_0x80_gap'] = round(abs(parity['even']['frac_lt_0x80']
                                           - parity['odd']['frac_lt_0x80']), 4)
    # 同一侧内部的等值率（lag1）：A 流与 B 流的局部重复性是否不同
    def eq1(s):
        return round(sum(1 for i in range(len(s) - 1) if s[i] == s[i + 1]) / (len(s) - 1), 5)
    parity['eq1_even'] = eq1(even)
    parity['eq1_odd'] = eq1(odd)
    return {
        'bit_p_one': bit_p,
        'bit_dev_from_50_max': round(max(abs(p - 0.5) for p in bit_p), 4),
        'nibble_hi_counts': hi, 'nibble_lo_counts': lo,
        'nibble_hi_entropy': round(entropy(hi, n), 4),
        'nibble_lo_entropy': round(entropy(lo, n), 4),
        'word16_topnibble_counts': top_nib,
        'word16_topnibble_entropy': round(entropy(top_nib, nw), 4),
        'word16_bit_p': wbit_p,
        'word16_active_bits': len(active),
        'word16_frac_below': frac_below,
        'word16_entropy': round(hw, 4),
        'word16_entropy_mm': round(hw + mm_correction(65536, nw), 4),
        'word16_entropy_max': 16.0,
        'byte_entropy': round(hb, 4),
        'word16_vs_2byte_ratio': round((hw + mm_correction(65536, nw)) / (2 * hb), 4),
        'unpack12': u12,
        'parity_profile': parity,
    }


# ========================= 4) 压缩器指纹 =========================
def mi_raw(data, lag=1):
    n = len(data) - lag
    c = collections.Counter(zip(data[:n], data[lag:]))
    hp = entropy(c.values(), n)
    return 2 * entropy(byte_counts(data), len(data)) - hp, len(c)


def lz_fingerprint(data, seed=1234):
    n = len(data)
    out = {}

    # --- 交错/奇偶熵：16/32 位字结构会让某个同余类显著不同 ---
    res = {}
    for p in (1, 2, 4, 8, 9, 16):
        ents, chis = [], []
        for r in range(p):
            sub = data[r::p]
            if len(sub) < 64:
                ents.append(None)
                chis.append(None)
                continue
            c = byte_counts(sub)
            ents.append(round(entropy(c, len(sub)), 4))
            chi, _ = chi2_uniform(c, len(sub))
            chis.append(round(chi / 255.0, 1))
        valid = [e for e in ents if e is not None]
        res[f'p{p}'] = {'entropy': ents,
                        'entropy_spread': round(max(valid) - min(valid), 4),
                        'chi2_per_df': chis}
    out['residue_entropy'] = res

    # --- 16 位字高位字节 = 0x00 / 0xFF 的比例（LZ77 距对指纹）---
    hz = {}
    for parity in (0, 1):
        hb = [data[i] for i in range(parity, n - 1, 2)]
        hz[f'parity{parity}'] = {
            'n': len(hb),
            'frac_hi_0x00': round(hb.count(0) / len(hb), 4),
            'frac_hi_0xFF': round(hb.count(0xFF) / len(hb), 4),
            'uniform_expect': 0.003906,
            'excess_ratio_0x00': round((hb.count(0) / len(hb)) / 0.003906, 2)}
    out['high_byte_pattern'] = hz

    # --- 邻接互信息 + 打乱零假设（避免稀疏偏差导致的假 MI）---
    obs_mi, bins = mi_raw(data, 1)
    rnd = random.Random(seed)
    null = []
    buf = bytearray(data)
    for _ in range(20):
        rnd.shuffle(buf)
        null.append(mi_raw(bytes(buf), 1)[0])
    null_mean = sum(null) / len(null)
    null_sd = (sum((x - null_mean) ** 2 for x in null) / len(null)) ** 0.5
    out['adjacent_MI'] = {
        'observed_raw_bits': round(obs_mi, 4),
        'shuffle_null_mean': round(null_mean, 4),
        'shuffle_null_sd': round(null_sd, 5),
        'excess_bits': round(obs_mi - null_mean, 4),
        'z_vs_null': round((obs_mi - null_mean) / null_sd, 2) if null_sd else None,
        'pair_bins': bins}

    # --- 字节数值自相关（lag 1..16）---
    mean = sum(data) / n
    var = sum((b - mean) ** 2 for b in data) / n
    ac = []
    for lag in range(1, 17):
        s = sum((data[i] - mean) * (data[i + lag] - mean) for i in range(n - lag))
        ac.append(round((s / (n - lag)) / var, 5))
    out['autocorr_lag1_16'] = ac
    out['autocorr_se'] = round(1 / math.sqrt(n), 5)

    # --- 4KB 分块熵 ---
    blocks = []
    for i in range(0, n, 4096):
        blk = data[i:i + 4096]
        c = byte_counts(blk)
        blocks.append([i, len(blk), round(entropy(c, len(blk)), 3)])
    out['blocks4k_entropy'] = blocks

    # --- 可压缩性上界：若本身已是压缩流，再压几乎无收益 ---
    comp = []
    for lvl in (1, 9):
        z = zlib.compressobj(lvl, zlib.DEFLATED, -15)
        cz = z.compress(data) + z.flush()
        comp.append({'level': lvl, 'out_bytes': len(cz),
                     'ratio': round(len(cz) / n, 4)})
    out['recompress_deflate'] = comp

    # --- 长连片 ---
    runs, i = [], 0
    while i < n:
        j = i
        while j < n and data[j] == data[i]:
            j += 1
        if j - i >= 32:
            runs.append([i, j - i, hex(data[i])])
        i = j
    out['runs_ge32'] = runs[:40]
    out['runs_ge32_count'] = len(runs)

    # --- 等值率(同位置字节相等的比例) 与 记录周期检测 ---
    # 用打乱后的同一序列作零假设，抵消字节直方图带来的基线偏移。
    shuf = bytes(random.Random(99).sample(data, len(data)))
    lags = list(range(1, 17)) + [32, 64, 128, 256, 512, 1024, 2048, 4096]
    eq = {}
    for k in lags:
        a = sum(1 for i in range(n - k) if data[i] == data[i + k]) / (n - k)
        b = sum(1 for i in range(n - k) if shuf[i] == shuf[i + k]) / (n - k)
        eq[str(k)] = {'obs': round(a, 5), 'null': round(b, 5),
                      'excess': round(a - b, 5)}
    out['equal_rate_by_lag'] = eq
    out['equal_rate_note'] = 'obs≈null 表示该周期上不存在重复结构；正值越大越像周期性记录'

    # --- 重复块检测（记录级重复）---
    dup = {}
    for bs in (16, 32, 64):
        blocks = collections.Counter(data[i:i + bs] for i in range(0, n - bs + 1, bs))
        rep = {k: v for k, v in blocks.items() if v > 1}
        dup[f'{bs}B'] = {'blocks': sum(blocks.values()),
                         'distinct': len(blocks),
                         'dup_groups': len(rep),
                         'extra_copies': sum(v - 1 for v in rep.values()),
                         'top': [[k.hex(), v] for k, v in
                                 sorted(rep.items(), key=lambda x: -x[1])[:3]]}
    out['dup_blocks'] = dup
    return out


# ========================= 5) 指令流粗判（弱证据）=========================
# H8/300H 首字节 → 指令长度。按手册 opcode map 的粗粒度分组：
#   0x00-0x3F 寄存器类运算/移位/比较，2B
#   0x40-0x5F 分支(disp8)，2B
#   0x60-0x6F 间接寻址类，2B（0x6A-0x6B JMP/JSR @aa:24 实为 4B，本表保守取 2B）
#   0x70-0x77 索引寻址，2B
#   0x78-0x7B MOV.L @aa:32，6B
#   0x7C-0x7F 绝对寻址(16 位)，4B
#   0x80-0xDF 绝对寻址 MOV，4B
#   0xE0-0xEF 乘除/杂项，2B
#   0xF0-0xF7 扩展，2B；0xF8-0xFF 带立即数，4B
H8_LEN = [2] * 256
for _b in range(0x78, 0x7C):
    H8_LEN[_b] = 6
for _b in range(0x7C, 0x80):
    H8_LEN[_b] = 4
for _b in range(0x80, 0xE0):
    H8_LEN[_b] = 4
for _b in range(0xF8, 0x100):
    H8_LEN[_b] = 4


def h8_walk(data):
    n = len(data)
    p, lens = 0, []
    while p < n:
        ln = H8_LEN[data[p]]
        if p + ln > n:
            break
        lens.append(ln)
        p += ln
    dist = collections.Counter(lens)
    avg = sum(lens) / len(lens)
    # 零功率对照：同样的表作用在"只保留字节直方图、顺序打乱"的数据上，
    # 期望平均长度只由直方图决定 → 若两者相等，则该指标没有区分能力。
    cnt = byte_counts(data)
    exp_avg = sum(cnt[b] * H8_LEN[b] for b in range(256)) / n
    return {
        'steps': len(lens), 'avg_len': round(avg, 3),
        'avg_len_null_from_histogram': round(exp_avg, 3),
        'end_offset': p, 'consumed_frac': round(p / n, 4),
        'len_hist': {k: dist[k] for k in sorted(dist)},
        'frac_firstbyte_in_H8_table': 1.0,
        'note': ('H8/300H 首字节 0x00-0xFF 几乎全被 opcode map 覆盖，'
                 '"合法首字节比例"恒等于 1，无区分力；avg_len 只由字节直方图决定，'
                 '与顺序无关，同样无区分力。'),
    }


def alignment_probe(data, width, name):
    n = len(data)
    groups = []
    for a in range(width):
        sub = data[a::width]
        c = byte_counts(sub)
        chi, _ = chi2_uniform(c, len(sub))
        cs = collections.Counter(sub)
        groups.append({'align': a, 'entropy': round(entropy(c, len(sub)), 4),
                       'chi2_per_df': round(chi / 255.0, 1),
                       'top3': [[hex(v), round(k / len(sub), 4)]
                                for v, k in cs.most_common(3)]})
    # 操作码字段集中度：对每个同余类，看"字段值分布"的最大占比
    def field_stats(residues, shift, mask):
        out = []
        for a in residues:
            f = collections.Counter((data[i] >> shift) & mask
                                    for i in range(a, n, 4))
            tot = sum(f.values())
            out.append({'align': a, 'bins': mask + 1,
                        'max_frac': round(max(f.values()) / tot, 4),
                        'top3': [[hex(v), round(k / tot, 4)]
                                 for v, k in f.most_common(3)]})
        return out
    return {'name': name, 'byte_groups': groups,
            'opcode_field_4B': field_stats(range(4), 4, 0xF) if width == 4 else None,
            'nibble_field_2B': [{'align': a,
                                 'max_frac': round(max(collections.Counter(
                                     (data[i] >> 4) & 0xF for i in range(a, n, 2)
                                 ).values()) / (n // 2), 4)}
                                for a in (0, 1)] if width == 2 else None}


def isa_probe(data):
    out = {'h8_300h': h8_walk(data),
           'arm32': alignment_probe(data, 4, 'ARM(4B 定长)'),
           'mips32': alignment_probe(data, 4, 'MIPS(4B 定长)'),
           'sh4': alignment_probe(data, 2, 'SH-4(2B 定长)')}
    # ARM 专用：cond 字段(高 4 位)==0xE(AL) 的占比。真实 ARM 代码通常 >40%。
    n = len(data)
    cond = {}
    for a in range(4):
        c = collections.Counter(data[i] >> 4 for i in range(a, n, 4))
        tot = sum(c.values())
        cond[f'align{a}'] = {'frac_cond_0xE': round(c.get(0xE, 0) / tot, 4),
                             'max_frac': round(max(c.values()) / tot, 4)}
    out['arm_cond_test'] = cond

    # MIPS 专用：opcode = 字的高 6 位。真实 MIPS 代码 opcode 高度集中
    # (0x00 SPECIAL / 0x23 LW / 0x27 SW / 0x2B SW / 0x0F LUI 常占 10-30%)
    nw = n // 4
    mips = {}
    for a in range(4):
        c = collections.Counter(data[4 * i + a] >> 2 for i in range(nw))
        tot = sum(c.values())
        mips[f'align{a}'] = {'max_frac': round(max(c.values()) / tot, 4),
                             'top3': [[hex(v), round(k / tot, 4)]
                                      for v, k in c.most_common(3)]}
    out['mips_opcode6_test'] = mips

    # 用户给的经验区间质量（仅描述，不用于判定）
    cnt = byte_counts(data)
    rng = {'0x00-0x7F': sum(cnt[0x00:0x80]), '0x40-0x7F': sum(cnt[0x40:0x80]),
           '0x78-0x7F': sum(cnt[0x78:0x80]), '0xE0-0xEF': sum(cnt[0xE0:0xF0]),
           '0xF0-0xFF': sum(cnt[0xF0:0x100])}
    out['h8_range_mass'] = {k: round(v / n, 4) for k, v in rng.items()}
    out['caveat'] = ('定长 ISA 在任何对齐下都"自动对齐"，对齐规律性本身不构成证据。'
                     '只有操作码字段出现强集中（ARM cond≈0xE、MIPS opcode 集中 0x00/0x23/0x27 等）'
                     '才算弱提示。本项不得用于断言架构。')
    return out


# ========================= main =========================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip-scan', action='store_true')
    ap.add_argument('--json', default=None)
    ap.add_argument('--target', default=TARGET)
    a = ap.parse_args()

    with open(a.target, 'rb') as f:      # 只读
        data = f.read()
    print(f'[i] file={a.target}')
    print(f'[i] size={len(data)}  sha256_head={__import__("hashlib").sha256(data).hexdigest()[:16]}')

    r = {'target': a.target, 'size': len(data), 'head64': data[:64].hex()}
    r['dist'] = distribution_tests(data)
    r['bits'] = bitpack_tests(data)
    r['lz'] = lz_fingerprint(data)
    r['isa'] = isa_probe(data)
    print('[i] decompression scan ...')
    r['scan'] = scan_streams(data, do_scan=not a.skip_scan)

    for k, title in (('scan', '1) 解压扫描'), ('dist', '2) 分布/重复'),
                     ('bits', '3) 位打包'), ('lz', '4) LZ 指纹'),
                     ('isa', '5) ISA 粗判')):
        print(f'\n=== {title} ===')
        print(json.dumps(r[k], indent=1, ensure_ascii=False))

    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(r, f, indent=1, ensure_ascii=False)
        print(f'\n[i] json -> {a.json}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
