import json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rea_client import ReaClient

TARGET = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111.exe"
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"
os.makedirs(OUT, exist_ok=True)

c = ReaClient()
print("[*] opening with ghidra ...", flush=True)
r = c.call("open_binary", {"path": TARGET, "provider_id": "ghidra"}, timeout=1800)
print("[open]", json.dumps(r, ensure_ascii=False)[:1500], flush=True)
if not r.get("ok"):
    c.close(); sys.exit(1)

def dump(name, tool, args=None, timeout=900):
    r = c.call(tool, args or {}, timeout=timeout)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
    n = len(json.dumps(r))
    print(f"[{tool}] -> {name} ({n} bytes) ok={r.get('ok')}", flush=True)
    return r

dump("rea_overview.json", "binary_overview")
dump("rea_strings.json", "list_strings")
dump("rea_procedures.json", "list_procedures")

# 关键字符串搜索
for pat in ["FIRMDATA", "RCDATA", "VERSIONVALUE", "INTERFACE", "RELEASENAME", ".dll", ".DLL"]:
    r = c.call("search_strings", {"pattern": pat, "mode": "literal", "case_sensitive": False}, timeout=300)
    print(f"[search:{pat}] ok={r.get('ok')}", flush=True)
    with open(os.path.join(OUT, f"rea_search_{pat.replace('.','_')}.json"), "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)

c.close()
print("[done]", flush=True)
