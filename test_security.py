#!/usr/bin/env python3
"""
test_security.py — Sprint 75 task 29.

Exercises hostile inputs against the cloud server.
"""
from __future__ import annotations
import json
import sys
import urllib.request
import urllib.error

CLOUD = "http://localhost:8791"


def _post(path, body=None, raw=None, headers=None):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if raw is not None:
        data = raw
    else:
        data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(CLOUD + path, data=data, method="POST",
                                 headers=h)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _try(fn):
    """Wrap a callable so connection-reset/broken-pipe counts as 'rejected'."""
    try:
        sc, _ = fn()
        return sc
    except Exception:
        return -1  # treat as rejection


CASES = [
    ("oversize body rejected",
     lambda: _try(lambda: _post("/enqueue", raw=b"A" * (11 * 1024 * 1024))) in (413, 400, -1)),
    ("malformed JSON rejected",
     lambda: _post("/enqueue", raw=b"{not-json")[0] == 400),
    ("array body rejected (must be object)",
     lambda: _post("/enqueue", body=[1, 2, 3])[0] == 400),
    ("empty body rejected",
     lambda: _post("/enqueue", raw=b"")[0] == 400),
    ("disallowed command rejected (403)",
     lambda: _post("/enqueue", body={"command": "/bin/sh", "args": {}})[0] == 403),
    ("missing command rejected",
     lambda: _post("/enqueue", body={"args": {}})[0] in (400, 403)),
    ("non-dict args rejected",
     lambda: _post("/enqueue", body={"command": "echo", "args": "x"})[0] == 400),
    ("ack without id rejected",
     lambda: _post("/ack", body={})[0] == 400),
    ("translate empty rejected",
     lambda: _post("/translate", body={"text": ""})[0] == 400),
    ("batch with non-list rejected",
     lambda: _post("/batch_execute", body={"commands": "no"})[0] == 400),
    ("batch oversized rejected",
     lambda: _post("/batch_execute", body={"commands": [{"command": "echo"}] * 500})[0] == 413),
    ("upload_screenshot missing id rejected",
     lambda: _post("/upload_screenshot", body={"data_b64": "AAAA"})[0] == 400),
    ("upload_screenshot bad b64 rejected",
     lambda: _post("/upload_screenshot", body={"id": "x", "data_b64": "&&!!"})[0] == 400),
]


def main():
    passed = 0
    failed = 0
    for name, fn in CASES:
        try:
            ok = fn()
        except Exception as e:
            ok = False
            print(f"  ✗ {name} — {type(e).__name__}: {e}")
            failed += 1
            continue
        if ok:
            passed += 1
            print(f"  ✓ {name}")
        else:
            failed += 1
            print(f"  ✗ {name}")
    print(f"\nSecurity tests: {passed} passed, {failed} failed (of {passed+failed})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
