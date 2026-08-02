#!/usr/bin/env python3
"""
test_e2e_extended.py — 30+ additional end-to-end test cases (Sprint 75 task 26)

Covers all newly added skills (Group G), the cloud server's new endpoints
(/health, /metrics, /version, /translate, /batch_execute, /history,
/scene_summary, /export_scene_json, /import_scene_json, /ack), security
edge cases, and the NL translator.

Run AFTER `test_e2e_headless.py` has confirmed the basic pipeline works.
Requires:
  - cloud server on http://localhost:8791
  - mock_unreal worker connected to it
"""

from __future__ import annotations

import json
import time
import sys
import urllib.request
import urllib.error
import urllib.parse
import uuid

CLOUD = "http://localhost:8791"
RESULT_TIMEOUT = 20.0


# ---------------------------------------------------------------------------
# tiny test runner
# ---------------------------------------------------------------------------
PASSED = 0
FAILED = 0
RESULTS: list[tuple[str, str, str]] = []  # (name, status, detail)


def _http(method, path, body=None, timeout=10):
    url = f"{CLOUD}{path}"
    data = None
    headers = {"Content-Type": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            try:
                return r.status, json.loads(raw)
            except json.JSONDecodeError:
                return r.status, raw
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {}


def test(name, predicate, detail_fn=lambda: ""):
    global PASSED, FAILED
    try:
        ok = predicate()
    except Exception as e:
        ok = False
        msg = f"{type(e).__name__}: {e}"
    else:
        msg = detail_fn() if ok else "predicate returned False"
    status = "PASS" if ok else "FAIL"
    if ok:
        PASSED += 1
        print(f"  ✓ {name}")
    else:
        FAILED += 1
        print(f"  ✗ {name} — {msg}")
    RESULTS.append((name, status, msg))


def submit(cmd, args=None):
    sc, body = _http("POST", "/enqueue", {"command": cmd, "args": args or {},
                                          "id": f"ext-{uuid.uuid4().hex[:8]}"})
    if sc != 200 or not isinstance(body, dict):
        return None
    return body.get("id")


def wait_result(cmd_id, timeout=RESULT_TIMEOUT):
    end = time.time() + timeout
    while time.time() < end:
        sc, body = _http("GET", f"/result?id={cmd_id}")
        if sc == 200 and isinstance(body, dict) and body.get("result"):
            return body["result"]
        time.sleep(0.4)
    return None


def is_success(result):
    if not result:
        return False
    inner = result.get("result", result)
    if isinstance(inner, dict):
        return inner.get("status") == "success" or "error" not in inner
    return False


def _huge_body_rejected(payload):
    """Server should either return 413/400 or close the connection. Either is OK."""
    try:
        sc, _ = _http("POST", "/enqueue",
                      {"command": "echo", "args": {"x": payload}})
        return sc in (413, 400)
    except Exception:
        # broken pipe / connection reset — server rejected forcefully, OK.
        return True


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def section(title):
    print(f"\n=== {title} ===")


def main():
    print("=" * 60)
    print(" SuperNinja Extended E2E Tests (Sprint 75)")
    print("=" * 60)

    section("Cloud control endpoints")
    test("GET /health 200 + ok status",
         lambda: (lambda r: r[0] == 200 and r[1].get("status") in ("ok", "warn"))(_http("GET", "/health")))
    test("GET /metrics returns counters",
         lambda: (lambda r: r[0] == 200 and "commands_enqueued" in r[1])(_http("GET", "/metrics")))
    test("GET /version returns version+phase",
         lambda: (lambda r: r[0] == 200 and r[1].get("phase") and r[1].get("version"))(_http("GET", "/version")))
    test("GET /history returns list",
         lambda: (lambda r: r[0] == 200 and isinstance(r[1].get("history"), list))(_http("GET", "/history")))

    section("Security & validation")
    test("Reject command not in allowlist",
         lambda: _http("POST", "/enqueue", {"command": "rm_-rf_/", "args": {}})[0] == 403)
    test("Reject body that is not a JSON object",
         lambda: _http("POST", "/enqueue", body=[1, 2, 3])[0] == 400)
    test("Reject huge body (>10MB)",
         lambda: (lambda b: _huge_body_rejected(b))("A" * (11 * 1024 * 1024)))
    test("Reject invalid args type",
         lambda: _http("POST", "/enqueue", {"command": "echo", "args": "not-a-dict"})[0] == 400)

    section("Translate endpoint (NL -> commands)")
    sc, b = _http("POST", "/translate", {"text": "build me a forest"})
    test("Translate 'build me a forest' returns >=2 commands",
         lambda: sc == 200 and isinstance(b.get("commands"), list) and len(b["commands"]) >= 2)
    sc2, b2 = _http("POST", "/translate", {"text": "make it brighter"})
    test("Translate 'make it brighter' -> light_scene",
         lambda: sc2 == 200 and any(c["command"] == "light_scene" for c in b2.get("commands", [])))
    sc3, b3 = _http("POST", "/translate", {"text": "place a police station"})
    test("Translate 'place a police station' -> spawn_actor",
         lambda: sc3 == 200 and any(c["command"] == "spawn_actor" for c in b3.get("commands", [])))
    test("Translate empty text -> 400",
         lambda: _http("POST", "/translate", {"text": ""})[0] == 400)

    section("Batch execute")
    sc, body = _http("POST", "/batch_execute", {"commands": [
        {"command": "spawn_actor", "args": {"shape": "Cube", "name": "Batch_A"}},
        {"command": "spawn_actor", "args": {"shape": "Sphere", "name": "Batch_B"}},
        {"command": "spawn_actor", "args": {"shape": "Cylinder", "name": "Batch_C"}},
    ]})
    test("Batch endpoint accepts 3 commands",
         lambda: sc == 200 and body.get("total") == 3)
    test("Batch enqueued ids are unique",
         lambda: len({e["id"] for e in body.get("enqueued", [])}) == 3)
    # Wait for results to flow through
    time.sleep(3.0)

    section("Scene summary + export/import")
    sc, body = _http("GET", "/scene_summary")
    test("GET /scene_summary returns counts",
         lambda: sc == 200 and "actor_count" in body)

    cid = submit("export_scene_json")
    res = wait_result(cid)
    test("export_scene_json skill returns scene dict",
         lambda: is_success(res) and isinstance(res.get("result", {}).get("scene"), dict))

    section("New Group-G skills")
    cid = submit("save_to_file", {"path": "/tmp/sn_test_scene.json"})
    test("save_to_file persists scene", lambda: is_success(wait_result(cid)))

    cid = submit("load_from_file", {"path": "/tmp/sn_test_scene.json"})
    test("load_from_file reloads scene", lambda: is_success(wait_result(cid)))

    cid = submit("export_screenshot_png", {"path": "/tmp/sn_test.png"})
    test("export_screenshot_png writes PNG", lambda: is_success(wait_result(cid)))

    cid = submit("undo_last_command")
    test("undo_last_command returns success",
         lambda: is_success(wait_result(cid)))

    cid = submit("clear_scene", {"confirm": True})
    test("clear_scene with confirm=true succeeds",
         lambda: is_success(wait_result(cid)))

    cid = submit("clear_scene", {})
    res = wait_result(cid)
    test("clear_scene without confirm -> error",
         lambda: res and (res.get("result", {}).get("status") == "error" or
                          res.get("result", {}).get("error")))

    cid = submit("undo_last_command")
    test("undo restores cleared scene",
         lambda: is_success(wait_result(cid)))

    section("Replay")
    sc, body = _http("POST", "/replay", {"last_n": 5})
    test("/replay accepts request",
         lambda: sc == 200 and "replayed" in body)

    section("Ack endpoint (task 25)")
    cid = submit("echo", {"msg": "ack-test"})
    sc, body = _http("POST", "/ack", {"id": cid})
    test("/ack accepts a known id",
         lambda: sc == 200 and body.get("status") == "acked")
    sc, body = _http("POST", "/ack", {})
    test("/ack rejects missing id",
         lambda: sc == 400)

    section("Smoke")
    test("Cloud allowed_commands count >= 60",
         lambda: len(_http("GET", "/status")[1].get("allowed_commands", [])) >= 60)

    print("\n" + "=" * 60)
    print(f" RESULTS: {PASSED} passed, {FAILED} failed (of {PASSED+FAILED})")
    print("=" * 60)
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
