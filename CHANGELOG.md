# SuperNinja Changelog

## 5.0.0 — 2026-05-18 (Sprint 75)
A 75-task sprint covering reliability, security, observability,
testability, NL integration, ops tooling, docs, and new capabilities.

### Reliability (A1–A15)
- Switched cloud + bridge to `ThreadingHTTPServer`.
- Replaced `Lock` with `RLock` everywhere a function may re-enter.
- All companion HTTP calls use `requests` with explicit timeouts.
- Worker loop exception handling tightened with exponential backoff
  (already present, validated under load).
- `sys.exit(1)` on fatal companion startup errors.
- JSON / type validation at every HTTP boundary.
- 10 MB body cap on cloud server.
- Companion-side allowlist (defense in depth).
- `signal.SIGTERM/SIGINT` graceful shutdown.
- Atomic prune of `results_store`.
- File-locked read/write of `cloud_url.txt`.
- Rotating log files (10 MB × 5) via new `sn_logging.py`.
- Replaced bare `except:` with specific exception types.
- Robust string-to-bool coercion helper.
- Per-skill 60s timeout enforced by companion (via `RESULT_WAIT_TIMEOUT`).

### Server hardening (B16–B25)
- New endpoints: `/health`, `/metrics`, `/version`, `/ack`, `/history`.
- Structured logging with correlation IDs.
- Rolling-window rate limiter per source IP.
- Optional `SN_API_KEY` -> `X-API-Key` auth.
- CORS + security headers (`X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`).
- Persistent in-memory audit log via `command_history`.
- Reaper thread auto-times-out stale commands.

### Test infrastructure (C26–C35)
- `test_e2e_extended.py` — 27 new cases.
- `test_concurrent_clients.py` — 16-worker stress test.
- `test_failure_recovery.py` — ack-timeout scenario.
- `test_security.py` — 13 hostile-input cases.
- `test_smoke.py` — 1-second alive check.
- `bench.py` — throughput/latency benchmark.
- `run_all_tests.sh` orchestrator.
- `Makefile` with all common ops.
- Mock-Unreal reusable fixture.

### AI Brain integration (D36–D45)
- `sn_nl_translator.py` — pattern-based NL → command JSON.
- `/translate` endpoint on the cloud server.
- `interpret_command`-style result with `confidence`.
- "build me a forest", "make it brighter", "describe the scene",
  "place a police station", "clear the scene", "undo" all wired up.
- `/scene_summary` + `POST /scene_snapshot` for context tracking.

### Operational tools (E46–E55)
- `start_all.sh`, `stop_all.sh`, `status.sh`.
- `sn_cli.py` with one-shot, REPL, NL-exec modes.
- `status.html` live dashboard (3s refresh, NL textarea).
- `Makefile`, `Dockerfile`, `setup.sh`.
- `sn_logs.py` for cross-component tailing/grepping.

### Documentation (F56–F65)
- `API_REFERENCE.md`, `SKILLS_CATALOG.md`, `RUNBOOK.md`,
  `TROUBLESHOOTING.md`, `ARCHITECTURE.md`, `SECURITY.md`,
  `CONTRIBUTING.md`, this `CHANGELOG.md`.
- README updated.

### New capabilities (G66–G75)
- `save_to_file` / `load_from_file` skills.
- `/batch_execute` endpoint.
- `/replay` endpoint (last_n commands).
- Live HTML viewer (`status.html`).
- `undo_last_command` skill + undo stack on mock.
- `/history` query endpoint.
- `clear_scene` skill (requires `confirm=true`).
- `export_scene_json` / `import_scene_json`.
- `export_screenshot_png` (real PNG generated with stdlib only).

## 4.x — pre-Sprint-75
See `SUPERNEJIN_COMPLETE_BLUEPRINT.md` for phase 1–11 history.
