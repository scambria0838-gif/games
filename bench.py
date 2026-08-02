#!/usr/bin/env python3
"""
bench.py — Sprint 75 task 33. Measures throughput & latency.
"""
from __future__ import annotations
import argparse
import json
import threading
import time
import urllib.request

CLOUD = "http://localhost:8791"


def _post(path, body):
    req = urllib.request.Request(CLOUD + path, method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def _get(path):
    with urllib.request.urlopen(CLOUD + path, timeout=10) as r:
        return json.loads(r.read())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--total", type=int, default=400)
    args = p.parse_args()

    per = args.total // args.workers
    print(f"Bench: {args.workers}x{per} = {args.workers*per} commands")
    enq_lat = []
    enq_lock = threading.Lock()

    def w():
        for _ in range(per):
            t0 = time.time()
            try:
                _post("/enqueue", {"command": "echo", "args": {"x": 1}})
                with enq_lock:
                    enq_lat.append((time.time() - t0) * 1000)
            except Exception:
                pass

    t0 = time.time()
    threads = [threading.Thread(target=w) for _ in range(args.workers)]
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.time() - t0
    enq_lat.sort()
    p50 = enq_lat[len(enq_lat)//2] if enq_lat else 0
    p95 = enq_lat[int(len(enq_lat)*0.95)] if enq_lat else 0
    print(f"Enqueue: {len(enq_lat)} commands in {elapsed:.2f}s "
          f"({len(enq_lat)/elapsed:,.0f}/s)  p50={p50:.1f}ms p95={p95:.1f}ms")

    # Tail metrics
    time.sleep(2)
    m = _get("/metrics")
    print(f"Server metrics: completed={m.get('commands_completed')} "
          f"queue={m.get('queue_length')} "
          f"server-side p50={m.get('latency_ms_p50'):.1f}ms "
          f"p95={m.get('latency_ms_p95'):.1f}ms")


if __name__ == "__main__":
    main()
