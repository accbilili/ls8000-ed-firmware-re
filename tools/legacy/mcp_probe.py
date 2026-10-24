import json, subprocess, sys, threading, queue, time

sys.stdout.reconfigure(encoding="utf-8")

NODE = r"C:\Program Files\nodejs\node.exe"
SCRIPT = r"<HOME>\AppData\Roaming\npm\node_modules\rea-agents\scripts\rea.mjs"

p = subprocess.Popen(
    [NODE, SCRIPT, "mcp"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, encoding="utf-8", errors="replace", bufsize=1,
)

q = queue.Queue()
errq = queue.Queue()


def pump(stream, target):
    for line in stream:
        target.put(line)


threading.Thread(target=pump, args=(p.stdout, q), daemon=True).start()
threading.Thread(target=pump, args=(p.stderr, errq), daemon=True).start()


def send(obj):
    p.stdin.write(json.dumps(obj) + "\n")
    p.stdin.flush()


def recv(timeout=120):
    try:
        return q.get(timeout=timeout)
    except queue.Empty:
        return None


send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "probe", "version": "1.0"}}})
r = recv(120)
print("=== initialize ===")
if not r:
    print("NO RESPONSE (120s)")
    while not errq.empty():
        print("STDERR:", errq.get().rstrip())
    p.kill()
    sys.exit(1)
print(r.strip()[:600])

send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
time.sleep(0.5)

send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
r = recv(180)
print("\n=== tools/list ===")
if not r:
    print("NO RESPONSE")
else:
    try:
        d = json.loads(r)
        tools = d.get("result", {}).get("tools", [])
        print("tool count:", len(tools))
        for t in tools:
            print(" -", t.get("name"))
        if d.get("result", {}).get("nextCursor"):
            print("nextCursor:", d["result"]["nextCursor"])
    except Exception as e:
        print("parse error:", e)
        print(r[:2000])

p.kill()
