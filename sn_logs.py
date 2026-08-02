#!/usr/bin/env python3
"""
sn_logs.py — Sprint 75 task 54. Tail+grep across all SuperNinja log files.

Usage:
    python3 sn_logs.py            # tail all logs (Ctrl+C to stop)
    python3 sn_logs.py grep "fail" # show all matching lines
    python3 sn_logs.py last 100   # last 100 lines per file
"""
from __future__ import annotations
import glob, os, sys, time

LOG_DIRS = [
    "/workspace/logs",
    "/var/log/supervisor",
    ".",
]

def find_logs():
    paths = []
    for d in LOG_DIRS:
        for ext in ("*.log", "*.jsonl", "8791_python*.log", "8765_python3*.log"):
            paths.extend(glob.glob(os.path.join(d, ext)))
    return sorted(set(paths))


def cmd_tail():
    paths = find_logs()
    if not paths:
        print("No logs found in:", LOG_DIRS); return 1
    print(f"Tailing {len(paths)} files (Ctrl+C to stop):")
    for p in paths: print(f"  • {p}")
    handles = {}
    for p in paths:
        try:
            f = open(p, "r")
            f.seek(0, os.SEEK_END)
            handles[p] = f
        except OSError:
            pass
    try:
        while True:
            for p, f in handles.items():
                line = f.readline()
                if line:
                    name = os.path.basename(p)
                    sys.stdout.write(f"[{name}] {line}")
                    sys.stdout.flush()
            time.sleep(0.3)
    except KeyboardInterrupt:
        return 0


def cmd_grep(pattern):
    paths = find_logs()
    matches = 0
    for p in paths:
        try:
            with open(p, "r", errors="replace") as f:
                for ln, line in enumerate(f, 1):
                    if pattern in line:
                        print(f"{os.path.basename(p)}:{ln}: {line.rstrip()}")
                        matches += 1
        except OSError:
            pass
    print(f"-- {matches} match(es)")


def cmd_last(n):
    for p in find_logs():
        print(f"\n===== {p} (last {n}) =====")
        try:
            with open(p, "r", errors="replace") as f:
                lines = f.readlines()[-n:]
                sys.stdout.writelines(lines)
        except OSError:
            print("(unreadable)")


def main():
    if len(sys.argv) == 1: return cmd_tail()
    sub = sys.argv[1]
    if sub == "grep" and len(sys.argv) >= 3: cmd_grep(sys.argv[2]); return 0
    if sub == "last": cmd_last(int(sys.argv[2]) if len(sys.argv) > 2 else 50); return 0
    print(__doc__); return 1

if __name__ == "__main__":
    sys.exit(main())
