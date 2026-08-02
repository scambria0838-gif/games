#!/usr/bin/env python3
"""
sn_cli.py — SuperNinja command-line interface (Sprint 75 tasks 49, 50).

Usage:
    python3 sn_cli.py <command> [k=v ...]      # one-shot
    python3 sn_cli.py status                    # show health/metrics
    python3 sn_cli.py history [N]               # show last N audit records
    python3 sn_cli.py translate "<sentence>"    # NL -> commands (no execute)
    python3 sn_cli.py exec   "<sentence>"       # NL -> commands -> execute
    python3 sn_cli.py repl                      # interactive REPL

Examples:
    python3 sn_cli.py spawn_actor name=Hero shape=Cube
    python3 sn_cli.py exec "build me a forest"
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error

CLOUD = os.environ.get("SN_CLOUD_URL", "http://localhost:8791")
HEADERS = {"Content-Type": "application/json"}
if os.environ.get("SN_API_KEY"):
    HEADERS["X-API-Key"] = os.environ["SN_API_KEY"]


def _http(method, path, body=None, timeout=20):
    data = None
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(CLOUD + path, data=data, method=method,
                                 headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {}


def _coerce(v: str):
    """Coerce 'k=v' string values into ints/floats/bools/lists/json."""
    s = v.strip()
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if s.startswith("[") or s.startswith("{"):
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return s
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def parse_kv(args):
    out = {}
    for a in args:
        if "=" not in a:
            continue
        k, v = a.split("=", 1)
        out[k] = _coerce(v)
    return out


def cmd_run(name, args):
    sc, body = _http("POST", "/enqueue",
                     {"command": name, "args": parse_kv(args)})
    if sc != 200:
        print(f"❌ enqueue {sc}: {body}")
        return 1
    cmd_id = body["id"]
    print(f"➡️  {name}  id={cmd_id}")
    deadline = time.time() + 30
    while time.time() < deadline:
        sc, r = _http("GET", f"/result?id={cmd_id}")
        if sc == 200 and r.get("result"):
            print(json.dumps(r["result"], indent=2, default=str))
            return 0
        time.sleep(0.4)
    print("⏱  timeout (still queued?)")
    return 2


def cmd_status():
    sc, h = _http("GET", "/health")
    sc, m = _http("GET", "/metrics")
    sc, v = _http("GET", "/version")
    print(json.dumps({"health": h, "metrics": m, "version": v}, indent=2, default=str))


def cmd_history(args):
    n = int(args[0]) if args else 50
    sc, body = _http("GET", f"/history?limit={n}")
    for record in body.get("history", [])[-n:]:
        print(f"  [{record.get('ts')}] {record.get('kind'):8s} "
              f"id={record.get('id')} {record.get('command','')}")


def cmd_translate(text, execute=False):
    sc, body = _http("POST", "/translate", {"text": text})
    if sc != 200:
        print(f"❌ translate {sc}: {body}")
        return 1
    cmds = body.get("commands", [])
    print(f"📝 translated {len(cmds)} command(s):")
    for c in cmds:
        print(f"   • {c['command']}({c.get('args', {})})  conf={c.get('confidence')}")
    if not execute:
        return 0
    if not cmds:
        return 0
    sc, body = _http("POST", "/batch_execute",
                     {"commands": [{"command": c["command"],
                                    "args": c.get("args", {})} for c in cmds]})
    print(f"🚀 batch enqueued: {body.get('total')} (errors={len(body.get('errors', []))})")
    return 0


def cmd_repl():
    print("SuperNinja REPL — type 'help' for commands, 'quit' to exit.")
    while True:
        try:
            line = input("sn> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line:
            continue
        if line in ("quit", "exit"):
            return 0
        if line == "help":
            print("Available: status | history [N] | translate <text> | "
                  "exec <text> | <skill> k=v ... | quit")
            continue
        if line == "status":
            cmd_status()
            continue
        if line.startswith("history"):
            cmd_history(line.split()[1:])
            continue
        if line.startswith("translate "):
            cmd_translate(line[len("translate "):])
            continue
        if line.startswith("exec "):
            cmd_translate(line[len("exec "):], execute=True)
            continue
        parts = line.split()
        cmd_run(parts[0], parts[1:])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    sub = sys.argv[1]
    rest = sys.argv[2:]
    if sub == "status":
        cmd_status(); return 0
    if sub == "history":
        cmd_history(rest); return 0
    if sub == "translate":
        return cmd_translate(" ".join(rest))
    if sub == "exec":
        return cmd_translate(" ".join(rest), execute=True)
    if sub == "repl":
        return cmd_repl()
    return cmd_run(sub, rest)


if __name__ == "__main__":
    sys.exit(main())
