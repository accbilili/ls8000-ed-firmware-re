"""把 36 个 fix 函数与「已知语义锚点」对齐：主命令分派表 / 作业表 / 已知助手函数。

只读工作区与 D: 样本，输出写本 _verify 目录。
"""
import os as _os, sys as _sys
_p = _os.path.dirname(_os.path.abspath(__file__))
while _p and not _os.path.isfile(_os.path.join(_p, "paths.py")):
    _q = _os.path.dirname(_p)
    if _q == _p:
        break
    _p = _q
_sys.path.insert(0, _p)
from paths import sample
import os, re, json, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'firmware', '_jobfuncs')
BASE = 0x10000
d = open(sample('LS8000_111_ROM.bin'), 'rb').read()


def rd(a, n):
    return d[a - BASE:a - BASE + n]


# --- 主命令分派表 0x03E2E8 (20 x 8B) ---
DISPATCH = []
for i in range(20):
    b = rd(0x03E2E8 + i * 8, 8)
    DISPATCH.append((b[0], struct.unpack('>I', b[4:8])[0]))

# --- 作业表 0x03EDE8 (u8 key, u8 pad, u32 fn) ---
JOB = {}
a = 0x03EDE8
while True:
    b = rd(a, 6)
    key = b[0]
    fn = struct.unpack('>I', b[2:6])[0]
    if fn == 0:
        break
    JOB.setdefault(fn, []).append(key)
    a += 6

# --- 已知语义锚点（来自工作区文档） ---
ANCHOR = {
    0x010B56: '设备就绪等待(全固件同步原语)',
    0x010BD2: '中断屏蔽-关',
    0x010BD8: '中断屏蔽-恢复',
    0x0118D0: 'data-out 相位 payload 拷贝',
    0x0118E8: 'payload 拷贝辅助',
    0x011900: '通用 flash 读(≤16B)',
    0x011930: 'flash/介质读辅助',
    0x016022: '块传输原语',
    0x01605A: '块传输辅助',
    0x017F04: '介质读辅助',
    0x017FD2: '双精度绝对差',
    0x0185EE: '64 位除法原语',
    0x01872E: '32 位除法',
    0x01876A: '双精度→int32(截断)',
    0x018860: '64 位乘法原语',
    0x018AA0: '软件双精度乘法',
    0x018CAC: '定点乘法辅助',
    0x018E1E: '32 位乘法',
    0x018E36: '算术辅助',
    0x018E68: '移位式 32×32→64 乘法',
    0x018E9E: '算术辅助',
    0x018EDE: '算术辅助',
    0x0211B6: '状态码→sense 索引(查 0x03E390)',
    0x0211E4: '状态码→sense 辅助',
    0x02159C: 'SCSI TUR(0x00)',
    0x025A56: 'CMD/参数块校验引擎',
    0x02896C: '清 10×0x22B 传感器表 0x41FFD4',
    0x028148: 'ASIC 前端配置×5',
    0x0289B4: '片夹识别主流程',
    0x028E30: '单排光学采样+自适应阈值',
    0x0290A0: '类型消费: 清4张表+查0x3EEF0向量',
    0x02ACBA: '走片轴就绪等待',
    0x02ADCE: '走片轴「走到目标位」',
    0x02B87C: '轴1/第二轴定位',
    0x02C8B4: '轴2 就绪等待',
    0x02C9E4: '轴2「走到目标位」',
    0x02D0DE: '定位辅助',
    0x02D1DC: 'ASIC 寄存器装配(0x2001C2/1C4/0x200102)',
    0x02D694: '定位辅助',
    0x02DA8E: '通道/槽位参数取数',
    0x02DAA2: '槽位参数取数',
    0x02ED5A: '配置广播(电机/ASIC/灯光/扫描 4 模块)',
    0x02EEE2: '片夹识别收尾钩子',
    0x02FFE6: '片夹识别收尾钩子',
    0x02FF32: '配置项查找',
    0x031E02: '扫描参数辅助',
    0x0321A0: '扫描参数辅助',
    0x0322B4: '位置换算',
    0x03316C: '通道配置辅助',
    0x0330AA: '曝光/位置表辅助',
    0x0330FA: '曝光/位置表辅助',
    0x0331F8: '扫描参数辅助',
    0x033284: '扫描参数辅助',
    0x0332BE: '槽位参数辅助',
    0x03338E: '扫描参数辅助',
    0x033422: 'ROM→RAM 表拷贝',
    0x0337A2: '扫描参数辅助',
    0x0337FE: '扫描参数辅助',
    0x034782: 'ROM→RAM 表拷贝',
    0x03655E: '片夹配置解析器(0x40064E 描述表)',
    0x03A284: '位深/gamma 表写入',
    0x03A2D8: '位深/gamma 表写入',
    0x03A334: '位深/gamma 换算',
    0x03A3D4: '扫描启动(A0 作业处理函数)',
    0x03A994: '扫描自检',
    0x03ADF6: '曝光/位置表计算',
    0x03B58E: '曝光/位置表计算',
    0x03C030: '区域查找+扫描位置计算',
    0x03C194: '每行算术',
    0x03D3C2: '扫描参数辅助',
    0x03D474: 'ROM 0x3D4A8→RAM 0xFFDD00',
    0x03DB20: '扫描参数辅助',
    0x03DDB2: '扫描参数辅助',
    0x02FA6C: '片夹/模式查表',
    0x02FF00: '配置广播入口',
    0x02FF32: '配置项查找',
    0x0368EC: '扫描流程辅助',
    0x039D70: '扫描流程辅助',
    0x035696: '预扫描/对焦(模式01/10)',
    0x027DC4: '进片状态机',
    0x028148: 'ASIC 前端配置×5',
    0x028152: 'ASIC 前端配置',
    0x03C2B6: 'AF 定位',
    0x03C2D0: 'AF 定位',
    0x02BE32: '扫描时序/曝光总时间',
    0x02C8E0: '轴2 归零等待',
    0x02CBB0: '轴2 归零等待',
    0x02CF60: '轴状态机',
    0x02CFA0: '轴状态机',
    0x02CFE0: '轴状态机',
    0x02D000: '轴状态机',
    0x02B038: '走片轴回零',
    0x02CC04: '轴2 参考点测定',
    0x02BAA6: '轴1 三节拍',
    0x0118E8: 'payload 拷贝辅助',
    0x02E13C: '错误上报辅助',
    0x025A56: 'CMD/参数块校验引擎',
}


def nearest_handler(addr):
    """addr 落在哪个已知分派处理函数的地址区间（按表项地址升序近似）。"""
    best = None
    for op, fn in DISPATCH:
        if fn <= addr:
            if best is None or fn > best[1]:
                best = (op, fn)
    return best


def main():
    sig = json.load(open(os.path.join(HERE, 'sem_signal.json'), encoding='utf-8'))
    ver = json.load(open(os.path.join(HERE, 'verify_result.json'), encoding='utf-8'))
    vmap = {r['entry']: r for r in ver['rows']}
    out = []
    for name in sorted(sig):
        addr = int(name.split('_')[1], 16)
        s = sig[name]
        v = vmap.get('0x%06X' % addr, {})
        calls = {}
        for c, n in s['calls'].items():
            t = int(c, 16)
            calls[c] = (n, ANCHOR.get(t, '未知助手'))
        dh = nearest_handler(addr)
        out.append(dict(
            entry='0x%06X' % addr,
            holes=v.get('holes'), fix_ins=v.get('fix_ins'), new_decoded=v.get('new_decoded'),
            old_ins=v.get('old_ins'), old_byte_breaks=v.get('old_byte_breaks'),
            hole_addrs=v.get('hole_addrs'),
            nearest_dispatch=(f'op=0x{dh[0]:02X} fn=0x{dh[1]:06X}' if dh else None),
            job_keys=JOB.get(addr),
            addrs=list(s['addrs'].keys())[:14],
            imms=list(s['imms'].keys())[:12],
            calls=calls,
            mnem=s['mn'],
        ))
    with open(os.path.join(HERE, 'sem_table.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for r in out:
        print(f"{r['entry']}  holes={r['holes']}  fix={r['fix_ins']:4d}  new={r['new_decoded']:3d}  "
              f"oldBB={r['old_byte_breaks']}  disp={r['nearest_dispatch']}  job={r['job_keys']}")
        print(f"    addrs: {r['addrs'][:10]}")
        print(f"    calls: { {k: v[1] for k, v in list(r['calls'].items())[:8]} }")


if __name__ == '__main__':
    main()
