import json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rea_client import ReaClient

TARGET = r"<HOME>\Videos\LS8000fw111_win\SUPERCOOLSCAN8000ED_111.exe"
OUT = r"<HOME>\WorkBuddy\2026-10-24-15-49-48\LS8000\02_analysis"

KEYS = {
    "0x40a33c": "FIRMDATA",
    "0x40a6c8": r"\Nikon\MaidMods\NKDSBP2.DLL",
    "0x40a6e4": r"\Nikon\MaidMods\NKDUSCAN.DLL",
    "0x40a31c": "%sUpdater.dat",
    "0x40a400": "[Sense %02X%02X%02X%02X]",
    "0x40a1a4": "RELEASENAME",
    "0x40a214": "INTERFACE",
    "0x40a228": "VERSIONVALUE",
}

c = ReaClient()
print("[*] open ...", flush=True)
r = c.call("open_binary", {"path": TARGET, "provider_id": "ghidra"}, timeout=1800)
if not r.get("ok"):
    print("OPEN FAILED", str(r)[:800]); c.close(); sys.exit(1)
print("[+] opened", flush=True)

summary = {}
callers = set()
for addr, label in KEYS.items():
    r = c.call("xrefs", {"address": addr}, timeout=300)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"xref_{addr}.json"), "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
    txt = ""
    if r.get("ok"):
        try:
            o = json.loads(r["result"]["content"][0]["text"])
            txt = json.dumps(o.get("normalized_result"), ensure_ascii=False)
            nr = o.get("normalized_result") or []
            if isinstance(nr, list):
                for it in nr:
                    if isinstance(it, dict):
                        a = it.get("from") or it.get("address") or it.get("from_address")
                        if a:
                            callers.add(str(a))
        except Exception as e:
            txt = f"parse:{e}"
    print(f"[xref] {label:<32} ok={r.get('ok')} -> {txt[:300]}", flush=True)

print(f"\n[*] unique caller addresses: {len(callers)}", flush=True)
for a in sorted(callers):
    print("   ", a, flush=True)

# 反编译调用者
made = 0
for a in sorted(callers):
    if made >= 8:
        break
    r = c.call("procedure_pseudo_code", {"procedure": a}, timeout=600)
    if not r.get("ok"):
        print(f"[decomp] {a} FAILED", flush=True)
        continue
    try:
        o = json.loads(r["result"]["content"][0]["text"])
        code = o.get("normalized_result") or o.get("raw_result")
        fn = os.path.join(OUT, f"decomp_{a.replace(':','_')}.c")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(json.dumps(code, ensure_ascii=False, indent=1) if not isinstance(code, str) else code)
        print(f"[decomp] {a} -> {os.path.basename(fn)} ({len(str(code))} chars)", flush=True)
        made += 1
    except Exception as e:
        print(f"[decomp] {a} parse err {e}", flush=True)

c.close()
print("[done]", flush=True)
