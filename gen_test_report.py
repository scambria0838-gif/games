#!/usr/bin/env python3
"""
gen_test_report.py — Sprint 75 task 32. Render a test_report.html
from running each suite and capturing stdout.
"""
from __future__ import annotations
import html, os, subprocess, time, sys

SUITES = [
    ("Smoke",                "test_smoke.py"),
    ("End-to-end (core)",    "test_e2e_headless.py"),
    ("End-to-end (extended)","test_e2e_extended.py"),
    ("Security",             "test_security.py"),
]


def run(script):
    t0 = time.time()
    try:
        out = subprocess.check_output(["python3", script],
                                      stderr=subprocess.STDOUT, timeout=120)
        rc = 0
    except subprocess.CalledProcessError as e:
        out = e.output; rc = e.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.output or b"") + b"\n[TIMEOUT]"; rc = 124
    return rc, time.time() - t0, out.decode(errors="replace")


def main():
    rows = []
    total_pass = total_fail = 0
    for label, script in SUITES:
        rc, dt, body = run(script)
        # extract final "X passed, Y failed"
        passed = failed = 0
        for line in body.splitlines()[::-1]:
            if "passed" in line and "failed" in line:
                try:
                    parts = line.replace(",", " ").split()
                    passed = int(parts[parts.index("passed")-1])
                    failed = int(parts[parts.index("failed")-1])
                    break
                except (ValueError, IndexError):
                    pass
        if not (passed or failed):
            passed = 1 if rc == 0 else 0
            failed = 0 if rc == 0 else 1
        total_pass += passed; total_fail += failed
        rows.append((label, script, rc, dt, passed, failed, body))

    bg_ok = "#0d8a4f"; bg_fail = "#a8332a"
    overall_color = bg_ok if total_fail == 0 else bg_fail
    parts = [f"""<!doctype html><html><head><meta charset="utf-8">
<title>SuperNinja Test Report</title>
<style>
body {{ font: 14px/1.4 -apple-system, BlinkMacSystemFont, sans-serif;
       background:#1a1f33; color:#e6e8f0; margin:0; padding:24px; }}
h1 {{ color:#7fd4ff; margin:0; }}
.summary {{ background:{overall_color}; padding:14px 18px; border-radius:8px;
            margin:16px 0; font-size:18px; }}
table {{ border-collapse:collapse; width:100%; }}
th, td {{ border-bottom:1px solid #2a324d; padding:8px 12px; text-align:left; }}
th {{ background:#0e132b; }}
.pass {{ color:#5be3a1; }} .fail {{ color:#ff6b6b; }}
pre {{ background:#0a0e1c; padding:12px; border-radius:6px; overflow:auto;
       max-height:400px; }}
details {{ margin:14px 0; }}
</style></head><body>
<h1>SuperNinja — Test Report</h1>
<div class="summary">{total_pass} passed · {total_fail} failed · generated {time.strftime("%Y-%m-%d %H:%M:%S")}</div>
<table><tr><th>Suite</th><th>Script</th><th>Pass</th><th>Fail</th><th>Time</th><th>Exit</th></tr>"""]
    for (label, script, rc, dt, p, f, _) in rows:
        cls = "pass" if rc == 0 and f == 0 else "fail"
        parts.append(f"<tr><td>{html.escape(label)}</td><td>{html.escape(script)}</td>"
                     f"<td class='pass'>{p}</td><td class='{cls}'>{f}</td>"
                     f"<td>{dt:.2f}s</td><td>{rc}</td></tr>")
    parts.append("</table>")
    for (label, script, rc, dt, p, f, body) in rows:
        parts.append(f"<details><summary><b>{html.escape(label)}</b> — {script}</summary>"
                     f"<pre>{html.escape(body)}</pre></details>")
    parts.append("</body></html>")
    out_path = "test_report.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"wrote {out_path} — {total_pass} passed, {total_fail} failed")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
