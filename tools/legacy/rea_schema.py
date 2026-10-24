import json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rea_client import ReaClient

WANT = {"open_binary", "binary_overview", "analyze_function", "procedure_pseudo_code",
        "procedure_assembly", "search_strings", "list_strings", "search_bytes",
        "read_bytes", "xrefs", "list_procedures", "close_binary",
        "inspect_firmware_regions", "extract_firmware", "inspect_pe_resources"}

c = ReaClient()
r = c._rpc("tools/list", {}, timeout=120)
tools = r.get("result", {}).get("tools", [])
print("total:", len(tools), "nextCursor:", r.get("result", {}).get("nextCursor"))

names = [t["name"] for t in tools]
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rea_tools.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(names)))

for t in tools:
    if t["name"] in WANT:
        print("\n###", t["name"])
        print("   desc:", (t.get("description") or "")[:300].replace("\n", " "))
        print("   schema:", json.dumps(t.get("inputSchema"), ensure_ascii=False)[:1200])
c.close()
