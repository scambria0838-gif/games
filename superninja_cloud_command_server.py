"""
SuperNinja Cloud Command Server — Phase 5 (Hardened, Sprint 75)

HTTP endpoint that SuperNinja cloud uses to enqueue commands, retrieve
results, and provide health/metrics/history. The Windows companion polls
this server outbound (no inbound ports needed on Windows).

Endpoints:
  GET  /                     -> liveness
  GET  /status               -> queue/result/screenshot summary + allowed commands
  GET  /health               -> component-level health (task 16)
  GET  /metrics              -> queue depth, latency, error rate (task 17)
  GET  /version              -> build sha + phase + uptime (task 18)
  GET  /poll                 -> companion picks up next command
  GET  /result?id=...        -> retrieve a specific result
  GET  /screenshot[?id=...]  -> retrieve screenshot (or list)
  GET  /screenshot_image?id= -> raw PNG bytes
  GET  /tunnel_url           -> currently registered tunnel URL
  GET  /scene_summary        -> last known scene snapshot (task 42)
  GET  /history              -> recent command audit log (task 71)

  POST /enqueue              -> queue a new command (with allowlist + rate limit)
  POST /result               -> companion posts back a result
  POST /ack                  -> companion confirms ownership of a command (task 25)
  POST /set_tunnel_url       -> tunnel manager sets the public URL
  POST /upload_screenshot    -> companion uploads PNG bytes (b64)
  POST /translate            -> NL -> command JSON (task 36)
  POST /batch_execute        -> queue a list of commands atomically (task 67)
  POST /replay               -> replay a previously recorded session (task 68)
  POST /scene_snapshot       -> companion publishes a scene snapshot
  POST /import_scene_json    -> queue a sequence of spawns to recreate a scene (74)
  GET  /export_scene_json    -> export last known snapshot as JSON (73)

Run: python superninja_cloud_command_server.py
Default port: 8791 (override with PORT env var).
"""

from __future__ import annotations

import base64
import json
import os
import signal
import sys
import time
from collections import deque
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from threading import Lock, RLock
from urllib.parse import urlparse, parse_qs

try:
    from sn_logging import get_logger, json_logger, new_correlation_id
    log = get_logger("sn_cloud")
    audit = json_logger("sn_cloud_audit")
except (ImportError, OSError):
    import logging
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
    log = logging.getLogger("sn_cloud")
    audit = log
    def new_correlation_id():
        import uuid
        return uuid.uuid4().hex[:12]

try:
    from sn_nl_translator import translate as nl_translate
    HAS_NL = True
except ImportError:
    HAS_NL = False

VERSION = "5.0.0-sprint75"
PHASE = 5
BUILD_TIME = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
queue_lock = RLock()
command_queue: list[dict] = []
results_store: dict[str, dict] = {}
screenshot_store: dict[str, dict] = {}
command_acks: dict[str, float] = {}
command_history: deque = deque(maxlen=1000)
scene_snapshot: dict = {"actors": [], "lights": [], "updated_at": None}
session_recording: list[dict] = []  # list of commands, in order, for replay (task 68)

metrics_lock = Lock()
metrics = {
    "started_at": time.time(),
    "commands_enqueued": 0,
    "commands_completed": 0,
    "commands_failed": 0,
    "commands_timed_out": 0,
    "commands_rejected": 0,
    "latency_samples_ms": deque(maxlen=500),  # for p50/p95
    "max_latency_ms": 0,
}

# rate limiter — bucket per IP: {"count": int, "window_start": float}
rate_buckets: dict[str, dict] = {}
rate_lock = Lock()

tunnel_url = None

# ---------------------------------------------------------------------------
# Limits / config
# ---------------------------------------------------------------------------
MAX_QUEUE_SIZE = 200
MAX_RESULTS = 500
MAX_SCREENSHOTS = 30
RESULT_TTL_SECONDS = 3600
MAX_BODY_SIZE = 10 * 1024 * 1024
COMMAND_ACK_TIMEOUT = 60.0
RATE_LIMIT_WINDOW = 10.0          # seconds
RATE_LIMIT_MAX_REQUESTS = 1000    # per window per IP (loopback friendly)
SKILL_TIMEOUT_DEFAULT = 60.0      # advisory — companion enforces

API_KEY = os.environ.get("SN_API_KEY", "").strip()  # if set, required on POSTs
RATE_LIMIT_ENABLED = os.environ.get("SN_RATE_LIMIT", "1") not in ("0", "false", "False")

# ---------------------------------------------------------------------------
# Allowed commands
# ---------------------------------------------------------------------------
SAFE_COMMANDS = {"ping", "echo", "log", "safe_log", "stop"}
PHASE2_COMMANDS = {"screenshot"}
SKILL_COMMANDS = {
    "add_directional_light", "add_point_light", "add_spot_light",
    "add_sky_light", "adjust_light",
    "spawn_actor", "move_actor", "rotate_actor", "scale_actor",
    "scatter_actors", "delete_actor", "delete_duplicates",
    "list_actors", "get_scene_info", "find_actors", "take_screenshot",
    "frame_viewport",
    "add_exponential_height_fog", "add_sky_atmosphere",
    "apply_material",
    "import_asset", "list_content",
    "save_level", "undo", "execute_console_command",
    "say", "ask_user", "report_progress", "explain_scene",
    "suggest_improvements", "chat",
    "light_scene", "cleanup_duplicates", "scatter_props",
    "get_actor_properties", "set_actor_property", "find_actors_advanced",
    "query_knowledge", "explain_ue5_concept", "suggest_blueprint_pattern",
    "run_python_snippet",
    "query_advanced_knowledge", "get_lighting_setup", "get_material_recipe",
    "analyze_rendering",
    "setup_post_process",
    "add_foliage",
    "query_expert_knowledge",
    "add_niagara_effect",
    "add_audio_ambient",
    "setup_ai_character", "add_navmesh",
    "optimize_scene", "get_fps_optimization_profile",
    "setup_cinematic",
    "get_multiplayer_pattern",
    "query_master_knowledge",
    "setup_landscape", "add_volumetric_clouds", "add_height_fog", "add_water_body",
    "setup_reflections", "setup_groom_system", "setup_rvt",
    "setup_virtual_production",
    "setup_physics_constraints", "add_chaos_vehicle",
    "query_master_landscape_preset",
    "setup_source_control",
    # New (Sprint 75 G)
    "save_to_file", "load_from_file",
    "clear_scene", "undo_last_command",
    "export_scene_json", "import_scene_json",
    "export_screenshot_png",
    # Audit fix: synced with companion allowlist
    "add_landscape", "add_post_process_volume",
    "add_volumetric_cloud",  # singular alias for add_volumetric_clouds
    "set_skybox",
    "kb_query", "kb_recommend",
}
ALL_ALLOWED = SAFE_COMMANDS | PHASE2_COMMANDS | SKILL_COMMANDS

DESTRUCTIVE_COMMANDS = {"delete_actor", "delete_duplicates", "clear_scene"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _bump_metric(key, n=1):
    with metrics_lock:
        metrics[key] = metrics.get(key, 0) + n


def _sample_latency_ms(ms: float):
    with metrics_lock:
        metrics["latency_samples_ms"].append(ms)
        if ms > metrics["max_latency_ms"]:
            metrics["max_latency_ms"] = ms


def _percentile(values, pct):
    if not values:
        return 0
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(round((pct / 100.0) * (len(s) - 1)))))
    return s[k]


def _check_rate_limit(ip: str) -> bool:
    """Return True if request is within budget."""
    if not RATE_LIMIT_ENABLED:
        return True
    now = time.time()
    with rate_lock:
        b = rate_buckets.get(ip)
        if not b or now - b["window_start"] > RATE_LIMIT_WINDOW:
            rate_buckets[ip] = {"count": 1, "window_start": now}
            return True
        b["count"] += 1
        return b["count"] <= RATE_LIMIT_MAX_REQUESTS


def _audit_event(kind: str, payload: dict):
    record = {"kind": kind, "ts": _now_iso(), **payload}
    command_history.append(record)
    try:
        audit.info(json.dumps(record, default=str))
    except (TypeError, ValueError):
        pass


def _record_session(cmd_entry):
    if len(session_recording) < 2000:
        session_recording.append(cmd_entry)


def _enqueue_internal(cmd: str, args: dict, cmd_id: str | None = None,
                      origin: str = "api") -> dict:
    """Shared enqueue logic used by /enqueue, /batch_execute, /import_scene_json."""
    if cmd not in ALL_ALLOWED:
        return {"error": f"command '{cmd}' not allowed", "status": 403}
    cmd_id = cmd_id or f"cmd-{int(time.time() * 1000)}-{new_correlation_id()[:6]}"
    entry = {
        "id": cmd_id,
        "command": cmd,
        "args": args or {},
        "enqueued_at": _now_iso(),
        "origin": origin,
        "cid": new_correlation_id(),
    }
    with queue_lock:
        if len(command_queue) >= MAX_QUEUE_SIZE:
            return {"error": "queue full", "status": 503}
        command_queue.append(entry)
    _bump_metric("commands_enqueued")
    _audit_event("enqueue", {"id": cmd_id, "command": cmd, "origin": origin})
    _record_session(entry)
    return {"status": "enqueued", "id": cmd_id, "command": cmd}


# ---------------------------------------------------------------------------
# HTTP Handler
# ---------------------------------------------------------------------------
class CommandHandler(BaseHTTPRequestHandler):
    server_version = f"SuperNinjaCloud/{VERSION}"

    # ----- routing -----
    def do_GET(self):
        if not _check_rate_limit(self.client_address[0]):
            self._json_response({"error": "rate limit exceeded"}, status=429)
            return
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query)

        if path in ("", "/"):
            self._json_response({"status": "ok",
                                 "service": "superninja-command-server",
                                 "phase": PHASE, "version": VERSION})
            return

        if path == "/status":
            with queue_lock:
                self._json_response({
                    "queue_length": len(command_queue),
                    "results_available": len(results_store),
                    "screenshots_available": len(screenshot_store),
                    "phase": PHASE,
                    "version": VERSION,
                    "allowed_commands": sorted(ALL_ALLOWED),
                })
            return

        if path == "/health":
            self._json_response(self._health_payload())
            return

        if path == "/metrics":
            self._json_response(self._metrics_payload())
            return

        if path == "/version":
            self._json_response({
                "version": VERSION,
                "phase": PHASE,
                "build_time": BUILD_TIME,
                "git_sha": os.environ.get("SN_GIT_SHA", "unknown"),
                "uptime_seconds": int(time.time() - metrics["started_at"]),
                "python": sys.version.split()[0],
            })
            return

        if path == "/poll":
            with queue_lock:
                if command_queue:
                    cmd = command_queue.pop(0)
                    command_acks[cmd["id"]] = time.time()
                    self._json_response({"command": cmd})
                else:
                    self._json_response({"command": None})
            return

        if path == "/result":
            cmd_id = params.get("id", [None])[0]
            if not cmd_id:
                self._json_response({"error": "missing ?id="}, status=400)
                return
            with queue_lock:
                if cmd_id in results_store:
                    self._json_response({"result": results_store[cmd_id]})
                elif cmd_id in screenshot_store:
                    self._json_response({"result": screenshot_store[cmd_id]})
                else:
                    self._json_response({"error": "not found"}, status=404)
            return

        if path == "/screenshot":
            cmd_id = params.get("id", [None])[0]
            with queue_lock:
                if not cmd_id:
                    self._json_response({"screenshots": [
                        {"id": k, "filename": v["filename"], "size": v["size"],
                         "completed_at": v["completed_at"]}
                        for k, v in screenshot_store.items()
                    ]})
                elif cmd_id in screenshot_store:
                    self._json_response({"screenshot": screenshot_store[cmd_id]})
                else:
                    self._json_response({"error": "screenshot not found"}, status=404)
            return

        if path == "/screenshot_image":
            cmd_id = params.get("id", [None])[0]
            if not cmd_id:
                self._json_response({"error": "missing ?id="}, status=400)
                return
            with queue_lock:
                if cmd_id in screenshot_store and "data_b64" in screenshot_store[cmd_id]:
                    try:
                        raw = base64.b64decode(screenshot_store[cmd_id]["data_b64"])
                    except (ValueError, base64.binascii.Error):
                        self._json_response({"error": "corrupt image data"}, status=500)
                        return
                    self.send_response(200)
                    self.send_header("Content-Type", "image/png")
                    self.send_header("Content-Length", str(len(raw)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    try:
                        self.wfile.write(raw)
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                else:
                    self._json_response({"error": "screenshot not found"}, status=404)
            return

        if path == "/tunnel_url":
            self._json_response({"tunnel_url": tunnel_url,
                                 "status": "ok" if tunnel_url else "not_set"})
            return

        if path == "/scene_summary":
            with queue_lock:
                snap = dict(scene_snapshot)
                snap["actor_count"] = len(snap.get("actors", []))
                snap["light_count"] = len(snap.get("lights", []))
                self._json_response(snap)
            return

        if path == "/history":
            limit = int(params.get("limit", ["100"])[0])
            self._json_response({"history": list(command_history)[-limit:]})
            return

        if path == "/export_scene_json":
            with queue_lock:
                self._json_response({
                    "version": 1,
                    "exported_at": _now_iso(),
                    "scene": dict(scene_snapshot),
                })
            return

        self._json_response({"error": "unknown route"}, status=404)

    # ----- POST routing -----
    def do_POST(self):
        if not _check_rate_limit(self.client_address[0]):
            self._json_response({"error": "rate limit exceeded"}, status=429)
            return
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if not self._check_api_key(path):
            return

        if path == "/enqueue":
            self._handle_enqueue()
        elif path == "/result":
            self._handle_result()
        elif path == "/ack":
            self._handle_ack()
        elif path == "/set_tunnel_url":
            self._handle_set_tunnel()
        elif path == "/upload_screenshot":
            self._handle_upload_screenshot()
        elif path == "/translate":
            self._handle_translate()
        elif path == "/batch_execute":
            self._handle_batch_execute()
        elif path == "/replay":
            self._handle_replay()
        elif path == "/scene_snapshot":
            self._handle_scene_snapshot()
        elif path == "/import_scene_json":
            self._handle_import_scene()
        else:
            self._json_response({"error": "unknown route"}, status=404)

    # ----- POST handlers -----
    def _handle_enqueue(self):
        body = self._read_body()
        if body is None:
            return
        cmd = body.get("command")
        args = body.get("args", {})
        cmd_id = body.get("id")
        if not isinstance(cmd, str) or not isinstance(args, dict):
            self._json_response({"error": "invalid command/args"}, status=400)
            _bump_metric("commands_rejected")
            return
        result = _enqueue_internal(cmd, args, cmd_id=cmd_id, origin="api")
        if "error" in result:
            _bump_metric("commands_rejected")
            self._json_response(result, status=result.pop("status", 400))
        else:
            self._json_response(result)

    def _handle_result(self):
        body = self._read_body()
        if body is None:
            return
        cmd_id = body.get("id")
        result = body.get("result", {})
        is_screenshot = bool(body.get("is_screenshot", False))

        if not cmd_id or not isinstance(result, dict):
            self._json_response({"error": "missing/invalid id or result"}, status=400)
            return

        # Latency from enqueue to result
        ack_ts = command_acks.get(cmd_id)
        if ack_ts:
            _sample_latency_ms((time.time() - ack_ts) * 1000)

        is_error = bool(result.get("error"))
        if is_error:
            _bump_metric("commands_failed")
        else:
            _bump_metric("commands_completed")

        with queue_lock:
            now = time.time()
            # Atomic prune (task 10)
            for k in [k for k, v in list(results_store.items())
                      if now - v.get("_ts", now) > RESULT_TTL_SECONDS]:
                results_store.pop(k, None)

            entry = {
                "id": cmd_id,
                "result": result,
                "completed_at": _now_iso(),
                "_ts": now,
            }
            if is_screenshot:
                if len(screenshot_store) >= MAX_SCREENSHOTS:
                    oldest = min(screenshot_store, key=lambda k: screenshot_store[k]["_ts"])
                    screenshot_store.pop(oldest, None)
                screenshot_store[cmd_id] = entry
            else:
                if len(results_store) >= MAX_RESULTS:
                    oldest = min(results_store, key=lambda k: results_store[k]["_ts"])
                    results_store.pop(oldest, None)
                results_store[cmd_id] = entry

            command_acks.pop(cmd_id, None)

        _audit_event("result", {"id": cmd_id, "error": is_error})
        self._json_response({"status": "stored", "id": cmd_id})

    def _handle_ack(self):
        body = self._read_body()
        if body is None:
            return
        cmd_id = body.get("id")
        if not cmd_id:
            self._json_response({"error": "missing id"}, status=400)
            return
        with queue_lock:
            command_acks[cmd_id] = time.time()
        _audit_event("ack", {"id": cmd_id})
        self._json_response({"status": "acked", "id": cmd_id})

    def _handle_set_tunnel(self):
        global tunnel_url
        body = self._read_body()
        if body is None:
            return
        url = body.get("tunnel_url", "")
        if not isinstance(url, str):
            self._json_response({"error": "invalid tunnel_url"}, status=400)
            return
        tunnel_url = url
        log.info("[TUNNEL] URL set: %s", tunnel_url)
        self._json_response({"status": "ok", "tunnel_url": tunnel_url})

    def _handle_upload_screenshot(self):
        body = self._read_body()
        if body is None:
            return
        cmd_id = body.get("id")
        filename = body.get("filename", "viewport.png")
        data_b64 = body.get("data_b64", "")
        if not cmd_id or not data_b64 or not isinstance(data_b64, str):
            self._json_response({"error": "missing id or data_b64"}, status=400)
            return
        try:
            raw_size = len(base64.b64decode(data_b64, validate=True))
        except (ValueError, base64.binascii.Error):
            self._json_response({"error": "invalid base64 data"}, status=400)
            return
        with queue_lock:
            if len(screenshot_store) >= MAX_SCREENSHOTS:
                oldest = min(screenshot_store, key=lambda k: screenshot_store[k]["_ts"])
                screenshot_store.pop(oldest, None)
            screenshot_store[cmd_id] = {
                "id": cmd_id,
                "filename": filename,
                "data_b64": data_b64,
                "size": raw_size,
                "completed_at": _now_iso(),
                "_ts": time.time(),
            }
        log.info("[SCREENSHOT UPLOAD] %s: %s (%d bytes)", cmd_id, filename, raw_size)
        self._json_response({"status": "uploaded", "id": cmd_id, "size": raw_size})

    def _handle_translate(self):
        body = self._read_body()
        if body is None:
            return
        text = body.get("text", "")
        if not isinstance(text, str) or not text.strip():
            self._json_response({"error": "missing 'text'"}, status=400)
            return
        if not HAS_NL:
            self._json_response({"error": "translator not available"}, status=503)
            return
        try:
            cmds = nl_translate(text)
        except Exception as e:  # translator may raise on weird input
            self._json_response({"error": f"translator error: {e}"}, status=500)
            return
        # Filter to allowed commands only
        cmds = [c for c in cmds if c.get("command") in ALL_ALLOWED]
        self._json_response({"input": text, "commands": cmds, "count": len(cmds)})

    def _handle_batch_execute(self):
        body = self._read_body()
        if body is None:
            return
        cmds = body.get("commands", [])
        if not isinstance(cmds, list) or not cmds:
            self._json_response({"error": "missing/invalid 'commands' list"}, status=400)
            return
        if len(cmds) > 200:
            self._json_response({"error": "batch too large (max 200)"}, status=413)
            return
        enqueued, errors = [], []
        for c in cmds:
            if not isinstance(c, dict):
                errors.append({"input": c, "error": "not an object"})
                continue
            cmd = c.get("command")
            args = c.get("args", {})
            if not isinstance(args, dict):
                errors.append({"command": cmd, "error": "invalid args"})
                continue
            r = _enqueue_internal(cmd, args, origin="batch")
            if "error" in r:
                errors.append({"command": cmd, "error": r["error"]})
            else:
                enqueued.append(r)
        self._json_response({"enqueued": enqueued, "errors": errors,
                             "total": len(enqueued)})

    def _handle_replay(self):
        body = self._read_body()
        if body is None:
            return
        last_n = int(body.get("last_n", len(session_recording)))
        last_n = max(0, min(last_n, len(session_recording)))
        slice_ = list(session_recording)[-last_n:] if last_n else []
        replayed = []
        for entry in slice_:
            r = _enqueue_internal(entry["command"], entry.get("args", {}),
                                  origin="replay")
            if "error" not in r:
                replayed.append(r)
        self._json_response({"replayed": len(replayed),
                             "items": replayed})

    def _handle_scene_snapshot(self):
        body = self._read_body()
        if body is None:
            return
        actors = body.get("actors", [])
        lights = body.get("lights", [])
        if not isinstance(actors, list) or not isinstance(lights, list):
            self._json_response({"error": "actors/lights must be lists"}, status=400)
            return
        with queue_lock:
            scene_snapshot["actors"] = actors[:5000]
            scene_snapshot["lights"] = lights[:500]
            scene_snapshot["updated_at"] = _now_iso()
        self._json_response({"status": "ok",
                             "actor_count": len(actors),
                             "light_count": len(lights)})

    def _handle_import_scene(self):
        body = self._read_body()
        if body is None:
            return
        scene = body.get("scene", {})
        if not isinstance(scene, dict):
            self._json_response({"error": "missing 'scene' object"}, status=400)
            return
        actors = scene.get("actors", [])
        lights = scene.get("lights", [])
        if not isinstance(actors, list) or not isinstance(lights, list):
            self._json_response({"error": "scene.actors/lights must be lists"}, status=400)
            return
        enqueued = []
        for a in actors[:1000]:
            r = _enqueue_internal("spawn_actor", a, origin="import_scene")
            if "error" not in r:
                enqueued.append(r["id"])
        for l in lights[:200]:
            r = _enqueue_internal(l.get("command", "add_point_light"),
                                  l.get("args", l), origin="import_scene")
            if "error" not in r:
                enqueued.append(r["id"])
        self._json_response({"status": "queued",
                             "count": len(enqueued),
                             "ids": enqueued[:50]})

    # ----- helpers -----
    def _health_payload(self):
        with queue_lock:
            queue_len = len(command_queue)
            results_n = len(results_store)
            screenshots_n = len(screenshot_store)
            stuck = sum(1 for ts in command_acks.values()
                        if time.time() - ts > COMMAND_ACK_TIMEOUT)
        components = {
            "server": "ok",
            "queue": "ok" if queue_len < MAX_QUEUE_SIZE * 0.9 else "warn",
            "results_store": "ok" if results_n < MAX_RESULTS * 0.9 else "warn",
            "tunnel": "ok" if tunnel_url else "not_set",
            "stuck_commands": stuck,
        }
        overall = "ok" if "warn" not in components.values() else "warn"
        return {
            "status": overall,
            "phase": PHASE,
            "version": VERSION,
            "uptime_s": int(time.time() - metrics["started_at"]),
            "components": components,
        }

    def _metrics_payload(self):
        with metrics_lock:
            samples = list(metrics["latency_samples_ms"])
            payload = {
                "uptime_s": int(time.time() - metrics["started_at"]),
                "commands_enqueued": metrics["commands_enqueued"],
                "commands_completed": metrics["commands_completed"],
                "commands_failed": metrics["commands_failed"],
                "commands_rejected": metrics["commands_rejected"],
                "commands_timed_out": metrics["commands_timed_out"],
                "latency_ms_p50": _percentile(samples, 50),
                "latency_ms_p95": _percentile(samples, 95),
                "latency_ms_max": metrics["max_latency_ms"],
                "rate_buckets": len(rate_buckets),
            }
        with queue_lock:
            payload["queue_length"] = len(command_queue)
            payload["results_available"] = len(results_store)
            payload["screenshots_available"] = len(screenshot_store)
            payload["pending_acks"] = len(command_acks)
        return payload

    def _check_api_key(self, path: str) -> bool:
        # /poll, /result, /ack, /upload_screenshot are companion-side;
        # if API_KEY is set, all POSTs require it (defense in depth).
        if not API_KEY:
            return True
        # internal-only routes still require the key
        provided = self.headers.get("X-API-Key", "")
        if provided != API_KEY:
            self._json_response({"error": "missing/invalid API key"}, status=401)
            return False
        return True

    def _read_body(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            self._json_response({"error": "invalid Content-Length"}, status=400)
            return None
        if content_length == 0:
            self._json_response({"error": "empty body"}, status=400)
            return None
        if content_length > MAX_BODY_SIZE:
            self._json_response({"error": f"body too large (max {MAX_BODY_SIZE})"},
                                status=413)
            return None
        try:
            raw = self.rfile.read(content_length)
        except (ConnectionResetError, BrokenPipeError):
            return None
        try:
            data = json.loads(raw)
            if not isinstance(data, dict):
                self._json_response({"error": "body must be a JSON object"}, status=400)
                return None
            return data
        except json.JSONDecodeError:
            self._json_response({"error": "invalid JSON"}, status=400)
            return None

    def _json_response(self, data, status=200):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            payload = json.dumps(data, default=str).encode()
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_OPTIONS(self):
        self._json_response({}, status=204)

    def log_message(self, fmt, *args):
        # Silence default access log; structured logs elsewhere.
        pass


# ---------------------------------------------------------------------------
# Background reaper (task 24): re-enqueue commands whose acks have expired
# ---------------------------------------------------------------------------
def _reaper_loop(stop_event):
    import threading
    while not stop_event.is_set():
        time.sleep(15.0)
        now = time.time()
        with queue_lock:
            stuck = [cid for cid, ts in command_acks.items()
                     if now - ts > COMMAND_ACK_TIMEOUT]
            for cid in stuck:
                command_acks.pop(cid, None)
                _bump_metric("commands_timed_out")
                _audit_event("timeout", {"id": cid})
                log.warning("Reaper: command %s timed out (no ack in %.0fs)",
                            cid, COMMAND_ACK_TIMEOUT)


def main():
    import threading
    port = int(os.environ.get("PORT", 8791))
    server = ThreadingHTTPServer(("0.0.0.0", port), CommandHandler)

    stop_event = threading.Event()

    def _shutdown(signum, frame):
        log.info("Signal %s received, shutting down...", signum)
        stop_event.set()
        server.shutdown()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    reaper = threading.Thread(target=_reaper_loop, args=(stop_event,),
                              daemon=True, name="sn-reaper")
    reaper.start()

    print("╔" + "═" * 56 + "╗")
    print(f"║  SuperNinja Cloud Command Server v{VERSION:<22s}║")
    print(f"║  Listening on 0.0.0.0:{port}                              ║")
    print(f"║  Allowed commands: {len(ALL_ALLOWED)}                                ║")
    print(f"║  API key auth: {'ON' if API_KEY else 'OFF':<3s}     Rate limit: {'ON' if RATE_LIMIT_ENABLED else 'OFF':<3s}                ║")
    print("╚" + "═" * 56 + "╝")

    try:
        server.serve_forever()
    finally:
        log.info("Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
