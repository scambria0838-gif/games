# SuperNinja Architecture (Phase 5, post-Sprint-75)

## High-level data flow

```
   ┌───────────────────────────┐
   │   Client / Web UI / CLI   │
   └────────────┬──────────────┘
                │ HTTPS (POST /enqueue, /batch_execute, /translate)
                ▼
   ┌──────────────────────────────────┐
   │   Cloud Command Server (8791)    │   <— this VM
   │   superninja_cloud_command_      │
   │   server.py  (ThreadingHTTPSrv)  │
   │                                  │
   │   • RLock-guarded queue          │
   │   • Rate limit / API-key auth    │
   │   • /health /metrics /version    │
   │   • Reaper thread (ack timeout)  │
   │   • NL -> command via /translate │
   └────────────┬─────────────────────┘
                │ Cloudflare quick tunnel
                ▼
   ┌──────────────────────────────────┐
   │   Windows Companion              │   <— user's PC
   │   sn_companion_phase2.py         │
   │   • polls /poll                  │
   │   • forwards to local bridge     │
   │   • posts /result and uploads    │
   │     screenshots                  │
   └────────────┬─────────────────────┘
                │ HTTP (localhost:8765)
                ▼
   ┌──────────────────────────────────┐
   │   Local Bridge                   │
   │   sn_local_bridge_phase2.py      │
   │   (ThreadingHTTPSrv + RLock)     │
   └────────────┬─────────────────────┘
                │ HTTP (UE5 Python polls)
                ▼
   ┌──────────────────────────────────┐
   │   UE5 Editor (Python plugin)     │
   │   sn_unreal_nonblocking_phase2.py│
   │   • exponential-backoff polling  │
   │   • Slate-tick log drainer       │
   │   • routes to sn_skill_executor  │
   └──────────────────────────────────┘
```

## Headless test substitution

For CI / sandboxes without UE5, `sn_mock_unreal.py` plays both the bridge
and the editor in pure Python. It maintains an in-memory `VirtualScene`
and provides ~30 mock skills (incl. all Group-G additions).

## Threading & concurrency

| Component | Server class | Lock |
|---|---|---|
| Cloud command server | `ThreadingHTTPServer` | `RLock` (`queue_lock`), `Lock` (`metrics_lock`, `rate_lock`) |
| Local bridge | `ThreadingHTTPServer` | `RLock` |
| Mock Unreal worker | single thread | `RLock` (scene), bound queue |

The reaper thread runs every 15s and times out commands whose ack age
exceeds `COMMAND_ACK_TIMEOUT` (60s).

## Persistence

The cloud server is **stateless** across restarts (in-memory only).
Long-lived state lives in:
- `/workspace/scenes/*.json` — scene exports written by `save_to_file`.
- `/workspace/screenshots/*.png` — PNG exports written by `export_screenshot_png`.
- `/workspace/logs/*.log` — rotating logs (10 MB × 5 backups by default).
- `/workspace/cloud_url.txt` — last-known cloud URL on the companion side.

## Security

- Allowlist enforced at every layer (cloud, companion, worker).
- POST request body capped at 10 MB; oversized bodies rejected `413`.
- JSON object validation (no arrays, no null bodies, no scalar bodies).
- Per-IP rate limit (1000 req / 10s default).
- Optional API key (`SN_API_KEY` env → `X-API-Key` header).
- CORS permissive by design (front-end is trusted origin; tighten in prod).
- Strict base64 validation on screenshot uploads (`b64decode(..., validate=True)`).
- `clear_scene` requires `confirm=true`.
- `delete_actor`, `delete_duplicates`, `clear_scene` are flagged
  `DESTRUCTIVE_COMMANDS` and recorded in audit trail.
