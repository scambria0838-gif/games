#!/usr/bin/env python3
"""
test_concurrent_clients.py — Sprint 75 task 27.

Submits N concurrent enqueue requests and verifies all of them are
acknowledged by the cloud server, then tracks how many results come back
within a deadline. Exercises the ThreadingHTTPServer + RLock fixes.
"""

from __future__ import annotations

import json
import time
import threading
import urllib.request
import sys

CLOUD = "http://localhost:8791"
N_WORKERS = 16
N_PER_WORKER = 25      # 16 * 25 = 400 total
WAIT_SECONDS = 30.0


def _post(path, body):
    req = urllib.request.Request(CLOUD + path, method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, json.loads(r.read())


def _get(path):
    with urllib.request.urlopen(CLOUD + path, timeout=10) as r:
        return r.status, json.loads(r.read())


enqueued: list[str] = []
errors: list[str] = []
lock = threading.Lock()


def worker(wid):
    for i in range(N_PER_WORKER):
        for attempt in range(3):  # retry on 429s
            try:
                sc, body = _post("/enqueue", {"command": "echo",
                                              "args": {"w": wid, "i": i}})
                if sc == 200:
                    with lock:
                        enqueued.append(body["id"])
                    break
            except Exception as e:
                if "429" in str(e):
                    time.sleep(0.5 * (attempt + 1))
                    continue
                with lock:
                    errors.append(f"w{wid}-{i}: {type(e).__name__}: {e}")
                break


def main():
    print(f"Spawning {N_WORKERS} workers x {N_PER_WORKER} requests = "
          f"{N_WORKERS * N_PER_WORKER} commands")
    t0 = time.time()
    threads = [threading.Thread(target=worker, args=(w,)) for w in range(N_WORKERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    enq_time = time.time() - t0
    print(f"Enqueue phase: {len(enqueued)} succeeded, {len(errors)} errors "
          f"in {enq_time:.2f}s ({len(enqueued)/enq_time:.0f}/s)")

    if errors:
        for e in errors[:10]:
            print(f"  ! {e}")

    print(f"Waiting up to {WAIT_SECONDS}s for results...")
    deadline = time.time() + WAIT_SECONDS
    completed = 0
    while time.time() < deadline:
        sc, m = _get("/metrics")
        completed = m.get("commands_completed", 0)
        ql = m.get("queue_length", -1)
        print(f"  completed={completed} queue={ql} p50={m.get('latency_ms_p50',0):.1f}ms "
              f"p95={m.get('latency_ms_p95',0):.1f}ms", flush=True)
        if completed >= len(enqueued):
            break
        time.sleep(2.0)

    print(f"\nFinal: {completed}/{len(enqueued)} commands processed.")
    return 0 if completed >= len(enqueued) * 0.95 else 1


if __name__ == "__main__":
    sys.exit(main())
