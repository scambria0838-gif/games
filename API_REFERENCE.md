# SuperNinja Cloud Command Server — API Reference

**Base URL:** `http://<host>:8791` (default port; override with `PORT`).
All POST bodies must be `application/json`. CORS is permissive (`*`).
If the environment variable `SN_API_KEY` is set on the server, every POST
must include the header `X-API-Key: <value>`.

---

## Liveness & metadata

### `GET /`
Tiny liveness probe. Returns `{"status":"ok","service":"superninja-command-server","phase":5,"version":"…"}`.

### `GET /status`
```json
{
  "queue_length": 0,
  "results_available": 12,
  "screenshots_available": 1,
  "phase": 5,
  "version": "5.0.0-sprint75",
  "allowed_commands": ["add_directional_light", "add_foliage", "..."]
}
```

### `GET /health`
Component-level health. `status` is one of `ok`, `warn`.
```json
{
  "status": "ok",
  "phase": 5,
  "version": "5.0.0-sprint75",
  "uptime_s": 1234,
  "components": {
    "server": "ok",
    "queue": "ok",
    "results_store": "ok",
    "tunnel": "not_set",
    "stuck_commands": 0
  }
}
```

### `GET /metrics`
Numeric metrics for monitoring/alerting.
```json
{
  "uptime_s": 1234,
  "commands_enqueued": 212,
  "commands_completed": 212,
  "commands_failed": 0,
  "commands_rejected": 188,
  "commands_timed_out": 0,
  "latency_ms_p50": 0.72,
  "latency_ms_p95": 0.85,
  "latency_ms_max": 1.39,
  "queue_length": 0,
  "results_available": 212,
  "screenshots_available": 0,
  "pending_acks": 0,
  "rate_buckets": 1
}
```

### `GET /version`
```json
{
  "version": "5.0.0-sprint75",
  "phase": 5,
  "build_time": "2026-05-18T09:36:46Z",
  "git_sha": "unknown",
  "uptime_seconds": 14,
  "python": "3.11.14"
}
```

---

## Command queue

### `POST /enqueue`
Queue a single command for the worker to pick up.

Request:
```json
{ "command": "spawn_actor",
  "args": { "shape": "Cube", "name": "Hero" },
  "id": "optional-client-supplied-id" }
```

Response:
```json
{ "status": "enqueued", "id": "cmd-1234567890-abc123", "command": "spawn_actor" }
```

Errors: `400` (invalid JSON / wrong types), `403` (command not in allowlist),
`413` (body too large), `429` (rate limited), `503` (queue full).

### `POST /batch_execute`
Queue up to **200** commands at once. Errors per-command are collected.

Request: `{"commands":[{"command":"spawn_actor","args":{...}}, ...]}`
Response: `{"enqueued":[...], "errors":[...], "total": <n>}`

### `GET /poll`
The worker pulls the next command off the queue (FIFO).
- `200 {"command": null}` if empty.
- `200 {"command": {...}}` with the full envelope on hit.
The server records an internal `ack_timestamp` so the reaper can detect
commands that the worker pulled but never acknowledged.

### `POST /ack`
Worker confirms ownership of a pulled command.
Request: `{"id":"cmd-..."}` → `200 {"status":"acked","id":"..."}`.

### `POST /result`
Worker posts the result.
```json
{ "id":"cmd-...",
  "result": {"status":"success", ...},
  "is_screenshot": false }
```

### `GET /result?id=...`
Returns the stored result envelope or `404`.

### `POST /replay`
Replay a slice of recently-recorded commands.
`{"last_n": 10}` → re-enqueues those 10.

### `GET /history?limit=N`
Audit trail (`enqueue`, `result`, `ack`, `timeout` records).

---

## Screenshots

### `POST /upload_screenshot`
`{"id":"cmd-...", "filename":"viewport.png", "data_b64":"<png base64>"}`
Server validates strict base64.

### `GET /screenshot[?id=...]`
List or fetch a single screenshot record.

### `GET /screenshot_image?id=...`
Returns raw `image/png` bytes (suitable for `<img src="…">`).

---

## Scene state

### `POST /scene_snapshot`
Worker pushes its current scene state.
`{"actors":[...], "lights":[...]}`

### `GET /scene_summary`
`{"actors":[...], "lights":[...], "actor_count":n, "light_count":m, "updated_at":"..."}`

### `GET /export_scene_json`
Versioned export of the last snapshot.

### `POST /import_scene_json`
`{"scene":{"actors":[...], "lights":[...]}}` → enqueues the spawns.

---

## Tunnel registration

### `GET /tunnel_url` → `{"tunnel_url": "...", "status":"ok|not_set"}`
### `POST /set_tunnel_url` → `{"tunnel_url":"https://..."}`

---

## NL → command translation

### `POST /translate`
`{"text":"build me a forest"}` →
```json
{ "input":"build me a forest",
  "commands":[
    {"command":"scatter_props","args":{"mesh_path":"/Game/Foliage/Tree","count":50,"radius":3000.0},"confidence":0.9},
    {"command":"scatter_props","args":{"mesh_path":"/Game/Foliage/Rock","count":20,"radius":3000.0},"confidence":0.85},
    {"command":"light_scene","args":{"preset":"daylight"},"confidence":0.8}
  ],
  "count": 3 }
```

---

## Rate limit
Per source IP: 1000 requests / 10s. Disable with `SN_RATE_LIMIT=0`.
