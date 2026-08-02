#!/usr/bin/env python3
"""
test_e2e_headless.py - End-to-end test harness for SuperNinja
=============================================================

Submits a series of commands to the cloud server, then polls for results,
validating that the entire pipeline works:

  Test client -> Cloud server -> [poll picked up by Mock Unreal worker] -> Result -> Test client

Run AFTER starting sn_mock_unreal.py.
"""

import json
import time
import urllib.request
import urllib.error

CLOUD_URL = "http://localhost:8791"


def post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(CLOUD_URL + path, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def get(path):
    with urllib.request.urlopen(CLOUD_URL + path, timeout=10) as r:
        return json.loads(r.read().decode())


def submit_and_wait(skill, args=None, timeout=15):
    """Submit a command and wait for the result."""
    args = args or {}
    payload = {"command": skill, "args": args}
    resp = post("/enqueue", payload)
    cmd_id = resp.get("id") or resp.get("command_id")
    if not cmd_id:
        return {"error": "no id returned", "resp": resp}

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            result = get(f"/result?id={cmd_id}")
            if result and "result" in result:
                return result
        except urllib.error.HTTPError as e:
            if e.code == 404:
                pass  # not ready yet, keep polling
            else:
                raise
        except Exception:
            pass
        time.sleep(0.3)
    return {"error": "timeout", "id": cmd_id}


def assert_success(r, label=""):
    """Validate that the round-trip actually returned a success result."""
    if r.get("error") == "timeout":
        raise AssertionError(f"{label}: TIMEOUT - command never completed")
    inner = r.get("result", {})
    # The cloud server wraps it in {"result": <our_post_payload>}
    # and our payload has its own "result": <skill_result>
    # So peel one or two layers:
    if isinstance(inner, dict) and "result" in inner:
        inner = inner["result"]
    if isinstance(inner, dict) and "status" in inner:
        if inner["status"] != "success":
            raise AssertionError(f"{label}: status={inner.get('status')} err={inner.get('error')}")
        return inner
    return inner


# ============================================================================
# TEST CASES
# ============================================================================

TESTS = []

def test(name):
    def deco(fn):
        TESTS.append((name, fn))
        return fn
    return deco


@test("01 - Cloud server health")
def t01():
    r = get("/")
    assert r.get("status") == "ok", f"bad status: {r}"
    return r


@test("02 - Cloud server status")
def t02():
    r = get("/status")
    assert "allowed_commands" in r
    return {"queue": r.get("queue_length"),
            "results": r.get("results_available"),
            "commands_count": len(r.get("allowed_commands", []))}


@test("03 - Echo round-trip")
def t03():
    r = submit_and_wait("echo", {"message": "hello"})
    assert "result" in r, f"no result: {r}"
    return r["result"]


@test("04 - Spawn a Cube")
def t04():
    r = submit_and_wait("spawn_actor", {"shape": "Cube", "location": [0, 0, 0]})
    inner = assert_success(r, "spawn cube")
    return {"actor": inner.get("actor", {}).get("name")}


@test("05 - Spawn a Sphere at custom location")
def t05():
    r = submit_and_wait("spawn_actor", {"shape": "Sphere", "location": [500, 300, 100]})
    inner = assert_success(r, "spawn sphere")
    return {"actor": inner.get("actor", {}).get("name"), "loc": inner.get("actor", {}).get("location")}


@test("06 - Spawn a Police Station (custom mesh path)")
def t06():
    r = submit_and_wait("spawn_actor", {
        "shape": "PoliceStation",
        "mesh_path": "/Game/Architecture/SM_PoliceStation",
        "location": [-300, -200, 0],
        "name": "PoliceStation_HQ"
    })
    inner = assert_success(r, "spawn police")
    return {"actor": inner.get("actor", {}).get("name"),
            "mesh": inner.get("actor", {}).get("mesh_path")}


@test("07 - List all actors")
def t07():
    r = submit_and_wait("list_actors", {})
    inner = assert_success(r, "list")
    return {"count": inner.get("count")}


@test("08 - Move PoliceStation_HQ")
def t08():
    r = submit_and_wait("move_actor", {"name": "PoliceStation_HQ", "location": [1000, 0, 0]})
    inner = assert_success(r, "move")
    return {"new_loc": inner.get("actor", {}).get("location")}


@test("09 - Add cinematic lighting")
def t09():
    r = submit_and_wait("light_scene", {"preset": "cinematic"})
    inner = assert_success(r, "light")
    return {"preset": inner.get("preset"), "lights_count": len(inner.get("lights_added", []))}


@test("10 - Scatter 15 props")
def t10():
    r = submit_and_wait("scatter_props", {"count": 15, "radius": 800})
    inner = assert_success(r, "scatter")
    return {"spawned": inner.get("spawned_count")}


@test("11 - Add 30 foliage")
def t11():
    r = submit_and_wait("add_foliage", {"count": 30, "radius": 1500})
    inner = assert_success(r, "foliage")
    return {"foliage": inner.get("foliage_count")}


@test("12 - Take ASCII screenshot")
def t12():
    r = submit_and_wait("screenshot", {})
    inner = assert_success(r, "screenshot")
    preview = inner.get("preview", "")
    return {"preview_lines": preview.count("\n"), "first_chars": preview[:40]}


@test("13 - Run python snippet (count actors)")
def t13():
    code = "result = len(SCENE.actors); print(f'Total actors: {result}')"
    r = submit_and_wait("run_python_snippet", {"code": code})
    inner = assert_success(r, "py")
    return {"stdout": inner.get("stdout", "").strip()}


@test("14 - Find actors with 'Cube'")
def t14():
    r = submit_and_wait("find_actors", {"pattern": "Cube"})
    inner = assert_success(r, "find")
    return {"matches": inner.get("count")}


@test("15 - Cleanup duplicates (dry run)")
def t15():
    r = submit_and_wait("cleanup_duplicates", {"dry_run": True})
    inner = assert_success(r, "dedup")
    return {"dupes_found": inner.get("duplicates_found")}


@test("16 - Delete PoliceStation_HQ")
def t16():
    r = submit_and_wait("delete_actor", {"name": "PoliceStation_HQ"})
    inner = assert_success(r, "delete")
    return {"deleted": inner.get("deleted", {}).get("name")}


@test("17 - Final screenshot of full scene")
def t17():
    r = submit_and_wait("screenshot", {})
    inner = assert_success(r, "final-screenshot")
    preview = inner.get("preview", "")
    return {"\n_PREVIEW_": "\n" + preview}


# ============================================================================
# RUN
# ============================================================================

def main():
    print("=" * 70)
    print(" SuperNinja END-TO-END HEADLESS TEST")
    print("=" * 70)
    print(f" Tests: {len(TESTS)}")
    print(f" Cloud: {CLOUD_URL}")
    print("=" * 70)
    print()

    passed = 0
    failed = 0
    results = []

    for name, fn in TESTS:
        t0 = time.time()
        try:
            out = fn()
            elapsed = (time.time() - t0) * 1000
            print(f"  ✓ {name:50s} {elapsed:6.0f}ms")
            if out is not None:
                # Pretty-print short results inline
                txt = json.dumps(out, default=str)
                if len(txt) > 500:
                    # Likely a screenshot - print on multiple lines
                    if isinstance(out, dict) and "\n_PREVIEW_" in out:
                        print(out["\n_PREVIEW_"])
                    else:
                        print(f"      {txt[:200]}...({len(txt)} chars)")
                else:
                    print(f"      {txt}")
            passed += 1
            results.append((name, "PASS", out))
        except Exception as e:
            elapsed = (time.time() - t0) * 1000
            print(f"  ✗ {name:50s} {elapsed:6.0f}ms")
            print(f"      ERROR: {type(e).__name__}: {e}")
            failed += 1
            results.append((name, "FAIL", str(e)))
        print()

    print("=" * 70)
    print(f" RESULTS: {passed} passed, {failed} failed (of {len(TESTS)})")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    import sys
    ok = main()
    sys.exit(0 if ok else 1)
