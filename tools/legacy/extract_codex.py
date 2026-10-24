import json, sys, os, re

sys.stdout.reconfigure(encoding="utf-8")

OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis\codex_sessions"
os.makedirs(OUT, exist_ok=True)

FILES = {
    "10-14_用REA分析LS-8000固件": r"<HOME>\.codex\archived_sessions\rollout-2026-10-14T12-07-52-01a13898-5e84-79b3-b1c7-2ab611e0232b.jsonl",
    "10-14_拆解软件并排查安装缺失DLL": r"<HOME>\.codex\archived_sessions\rollout-2026-10-14T16-16-31-01a1397c-04cf-7cd2-895f-bea2bb3bf167.jsonl",
    "10-21_使用REA分析固件": r"<HOME>\.codex\sessions\2026\10\21\rollout-2026-10-21T13-27-44-01a15cee-03c4-7bc3-902e-878e7d73452e.jsonl",
    "10-21_后续": r"<HOME>\.codex\sessions\2026\10\21\rollout-2026-10-21T13-29-12-01a15cef-5973-7410-98d6-444a4edc1018.jsonl",
}


def flatten(content):
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict):
                t = c.get("text")
                if isinstance(t, str):
                    parts.append(t)
    return "\n".join(parts)


for label, path in FILES.items():
    if not os.path.exists(path):
        print(f"[missing] {label}")
        continue
    msgs = []
    tools = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            p = o.get("payload") or {}
            if o.get("type") == "response_item":
                pt = p.get("type")
                if pt == "message":
                    role = p.get("role")
                    txt = flatten(p.get("content"))
                    if role in ("user", "assistant") and txt.strip():
                        msgs.append((o.get("timestamp", "")[:19], role, txt))
                elif pt in ("function_call", "custom_tool_call"):
                    name = p.get("name") or p.get("tool_name") or "?"
                    args = p.get("arguments") or p.get("input") or ""
                    if isinstance(args, str) and len(args) > 300:
                        args = args[:300] + " ..."
                    tools.append((name, str(args)))
            elif o.get("type") == "event_msg":
                if p.get("type") == "agent_message":
                    m = p.get("message")
                    if isinstance(m, str) and m.strip():
                        msgs.append((o.get("timestamp", "")[:19], "assistant", m))

    out = []
    out.append(f"# Codex 会话：{label}")
    out.append(f"源文件：{path}")
    out.append(f"消息数：{len(msgs)}，工具调用数：{len(tools)}\n")
    out.append("## 工具调用摘要")
    from collections import Counter
    for name, cnt in Counter(t[0] for t in tools).most_common(30):
        out.append(f"- {name}: {cnt}")
    out.append("\n## 对话正文")
    for ts, role, txt in msgs:
        txt = txt.strip()
        if role == "user" and len(txt) > 1200:
            txt = txt[:1200] + "\n...[truncated]"
        out.append(f"\n### [{ts}] {role.upper()}\n{txt}")

    md = "\n".join(out)
    fn = os.path.join(OUT, re.sub(r'[\\/:*?"<>|]', "_", label) + ".md")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[ok] {label}: {len(msgs)} msgs, {len(tools)} tool calls, {len(md)} chars -> {os.path.basename(fn)}")
