"""
SuperNinja Local Bridge — Phase 2+ (Full Pipeline)

Runs on Windows at 127.0.0.1:8765
- Receives commands from the companion (which polls the cloud)
- Queues them for the Unreal Python client to pick up
- Unreal client polls /poll, executes, posts /result
- Companion picks up results and posts back to cloud
- Handles screenshots: captures viewport and returns image data

Run: python sn_local_bridge_phase2.py
"""

import json
import time
import os
import base64
import threading
import signal
import sys
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from collections import deque

# Bridge config
BRIDGE_PORT = 8765
SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "sn_screenshots")
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10MB max request body (DoS protection)
MAX_QUEUE_SIZE = 1000             # cap queue depth
MAX_RESULTS = 500                 # cap result store
RESULT_TTL_SECONDS = 3600         # 1 hour

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Command queue and result storage (thread-safe, RLock allows nested acquires)
command_queue = deque()
results_store = {}  # cmd_id -> {"result": ..., "_ts": float}
lock = threading.RLock()

# Server reference for graceful shutdown
_server_ref = {"server": None}

SAFE_COMMANDS = {"ping", "echo", "log", "safe_log", "stop"}
PHASE2_COMMANDS = {"screenshot"}
SKILL_COMMANDS = {
    # Lighting
    "add_directional_light", "add_point_light", "add_spot_light",
    "add_sky_light", "adjust_light",
    # Placement
    "spawn_actor", "move_actor", "rotate_actor", "scale_actor",
    "scatter_actors", "delete_actor", "delete_duplicates",
    # Analysis
    "list_actors", "get_scene_info",
    # Camera
    "frame_viewport",
    # Environment
    "add_exponential_height_fog", "add_sky_atmosphere",
    "add_foliage", "add_height_fog", "add_volumetric_clouds",
    "add_water_body", "setup_landscape",
    # Material
    "apply_material",
    # Asset
    "import_asset", "list_content",
    # Utility
    "save_level", "undo", "execute_console_command",
    # Conversational
    "say", "ask_user", "report_progress", "explain_scene",
    "suggest_improvements", "chat",
    # High-level composite
    "light_scene", "cleanup_duplicates", "scatter_props",
    # Knowledge & Intelligence
    "get_actor_properties", "set_actor_property", "find_actors_advanced",
    "query_knowledge", "explain_ue5_concept", "suggest_blueprint_pattern",
    "run_python_snippet",
    # Advanced Knowledge (Docs 21-60)
    "query_advanced_knowledge", "get_lighting_setup", "get_material_recipe",
    "analyze_rendering",
    # Rendering
    "setup_post_process", "setup_reflections", "setup_groom_system", "setup_rvt",
    # Expert Knowledge (Docs 61-100)
    "query_expert_knowledge",
    # VFX (Niagara)
    "add_niagara_effect",
    # Audio
    "add_audio_ambient",
    # AI
    "setup_ai_character", "add_navmesh",
    # Optimization
    "optimize_scene", "get_fps_optimization_profile",
    # Cinematics
    "setup_cinematic",
    # Networking
    "get_multiplayer_pattern",
    # Master Knowledge (Docs 101-151)
    "query_master_knowledge", "query_master_landscape_preset",
    # Virtual Production
    "setup_virtual_production",
    # Physics (master)
    "setup_physics_constraints", "add_chaos_vehicle",
    # Pipeline
    "setup_source_control",
}
ALL_ALLOWED = SAFE_COMMANDS | PHASE2_COMMANDS | SKILL_COMMANDS


class BridgeHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"[Bridge] {fmt % args}")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path == "/":
            self._json({"status": "ok", "service": "superninja-bridge", "phase": 2})

        elif path == "/status":
            self._json({
                "bridge": "running",
                "phase": 2,
                "queue_length": len(command_queue),
                "results_available": len(results_store),
                "allowed": sorted(ALL_ALLOWED),
            })

        elif path == "/poll":
            # Unreal client polls here to get next command
            with lock:
                if command_queue:
                    cmd_data = command_queue.popleft()
                    self._json({"command": cmd_data})
                else:
                    self._json({"command": None})

        elif path == "/result":
            # Companion checks for results from Unreal
            qs = parse_qs(parsed.query)
            cmd_id = qs.get("id", [None])[0]
            with lock:
                if cmd_id and cmd_id in results_store:
                    result = results_store.pop(cmd_id)
                    self._json({"result": result})
                else:
                    self._json({"result": None})

        else:
            self._json({"error": "unknown route"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/command":
            # Companion posts a command here (from cloud)
            body = self._read_body()
            if body is None:
                return

            cmd = body.get("command")
            cmd_id = body.get("id", "unknown")

            if cmd not in ALL_ALLOWED:
                self._json({"error": f"command '{cmd}' not allowed"}, status=403)
                return

            print(f"[Bridge] Queuing command: {cmd} (id={cmd_id})")

            # Queue the command for Unreal to pick up
            with lock:
                command_queue.append(body)

            self._json({"status": "queued", "id": cmd_id, "command": cmd})

        elif path == "/result":
            # Unreal client posts results here after executing
            body = self._read_body()
            if body is None:
                return

            cmd_id = body.get("id", "unknown")
            print(f"[Bridge] Got result for: {cmd_id}")

            with lock:
                results_store[cmd_id] = body

            self._json({"status": "stored", "id": cmd_id})

        else:
            self._json({"error": "unknown route"}, status=404)

    def _read_body(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            self._json({"error": "invalid Content-Length"}, status=400)
            return None
        if content_length == 0:
            self._json({"error": "empty body"}, status=400)
            return None
        if content_length > MAX_BODY_SIZE:
            self._json({"error": f"body too large (max {MAX_BODY_SIZE} bytes)"}, status=413)
            return None
        try:
            raw = self.rfile.read(content_length)
        except (ConnectionResetError, BrokenPipeError) as e:
            return None
        try:
            data = json.loads(raw)
            if not isinstance(data, dict):
                self._json({"error": "body must be a JSON object"}, status=400)
                return None
            return data
        except json.JSONDecodeError:
            self._json({"error": "invalid JSON"}, status=400)
            return None

    def _json(self, data, status=200):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Content-Type-Options", "nosniff")
            payload = json.dumps(data).encode()
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            pass  # client disconnected; nothing we can do

    def log_message(self, fmt, *args):
        # Silence default access log; we have our own logging
        pass


def _shutdown_handler(signum, frame):
    print(f"\n[Bridge] Received signal {signum}, shutting down...")
    server = _server_ref.get("server")
    if server:
        # Persist any pending results to a file before exit
        with lock:
            if results_store:
                try:
                    with open(os.path.join(SCREENSHOT_DIR, "pending_results.json"), "w") as f:
                        json.dump({k: v for k, v in results_store.items()}, f, default=str)
                    print(f"[Bridge] Saved {len(results_store)} pending results")
                except Exception as e:
                    print(f"[Bridge] Failed to persist results: {e}")
        threading.Thread(target=server.shutdown, daemon=True).start()
    sys.exit(0)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", BRIDGE_PORT), BridgeHandler)
    _server_ref["server"] = server

    # Register graceful shutdown handlers
    signal.signal(signal.SIGINT, _shutdown_handler)
    signal.signal(signal.SIGTERM, _shutdown_handler)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SuperNinja Local Bridge — Full Pipeline               ║")
    print(f"║  Listening on 127.0.0.1:{BRIDGE_PORT}                          ║")
    print(f"║  Queue + Result storage for Unreal ↔ Cloud             ║")
    print("╚══════════════════════════════════════════════════════════╝")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Bridge] Stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
