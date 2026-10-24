"""Minimal MCP stdio client for the local REA server.

WorkBuddy did not inject the REA tools into this session, but the server itself
is healthy. This client speaks the same JSON-RPC over stdio, so the full tool
set stays usable.
"""
import json, subprocess, sys, threading, queue

NODE = r"C:\Program Files\nodejs\node.exe"
SCRIPT = r"<HOME>\AppData\Roaming\npm\node_modules\rea-agents\scripts\rea.mjs"


class ReaClient:
    def __init__(self):
        self.p = subprocess.Popen(
            [NODE, SCRIPT, "mcp"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
        self.q = queue.Queue()
        self.err = []
        threading.Thread(target=self._pump, args=(self.p.stdout,), daemon=True).start()
        threading.Thread(target=self._pump_err, daemon=True).start()
        self._id = 0
        self._rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "rea-client", "version": "1.0"},
        }, timeout=120)
        self._notify("notifications/initialized", {})

    def _pump(self, stream):
        for line in stream:
            self.q.put(line)

    def _pump_err(self):
        for line in self.p.stderr:
            self.err.append(line.rstrip())
            if len(self.err) > 200:
                self.err.pop(0)

    def _notify(self, method, params):
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method, "params": params}) + "\n")
        self.p.stdin.flush()

    def _rpc(self, method, params, timeout=600):
        self._id += 1
        rid = self._id
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params}) + "\n")
        self.p.stdin.flush()
        while True:
            try:
                line = self.q.get(timeout=timeout)
            except queue.Empty:
                return {"error": {"message": "timeout", "stderr": self.err[-10:]}}
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("id") == rid:
                return obj

    def call(self, tool, args=None, timeout=900):
        r = self._rpc("tools/call", {"name": tool, "arguments": args or {}}, timeout=timeout)
        if "error" in r:
            return {"ok": False, "error": r["error"]}
        res = r.get("result", {})
        if res.get("isError"):
            return {"ok": False, "error": res}
        return {"ok": True, "result": res}

    def close(self):
        try:
            self.p.kill()
        except Exception:
            pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    c = ReaClient()
    r = c.call("binary_session", {}, timeout=60)
    print(json.dumps(r, ensure_ascii=False)[:3000])
    c.close()
