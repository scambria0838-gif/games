#!/usr/bin/env python3
"""
test_smoke.py — Sprint 75 task 35.

The simplest possible "system is alive" test. Ideal for a CI/cron health
gate. Returns 0 iff:
  - cloud /health is reachable AND status in {ok, warn}
  - cloud /version reports a version
  - cloud allowlist has > 60 commands
"""
from __future__ import annotations
import json, sys, urllib.request

CLOUD = "http://localhost:8791"


def _get(path):
    with urllib.request.urlopen(CLOUD + path, timeout=5) as r:
        return r.status, json.loads(r.read())


def main():
    try:
        sc, h = _get("/health")
        assert sc == 200 and h.get("status") in ("ok", "warn"), h
        sc, v = _get("/version")
        assert sc == 200 and v.get("version"), v
        sc, s = _get("/status")
        assert sc == 200 and len(s.get("allowed_commands", [])) > 60, s
    except Exception as e:
        print(f"SMOKE FAIL: {type(e).__name__}: {e}")
        return 1
    print(f"SMOKE OK — version={v['version']}  commands={len(s['allowed_commands'])}  health={h['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
