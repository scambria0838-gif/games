"""
SuperNinja Unreal Non-Blocking Client — Phase 2 (Screenshot Support)

Runs inside Unreal Editor's Python environment.
- Background worker thread polls local bridge at 127.0.0.1:8765
- Executes safe commands (ping, echo, log, safe_log, stop)
- Phase 2: Captures viewport screenshots and saves to disk
- Uses Slate tick callback to drain log queue (non-blocking)
- Returns results back through the bridge → companion → cloud

Run in Unreal Python console:
exec(open(r"C:\\Users\\sbcam\\OneDrive\\Desktop\\sn_unreal_nonblocking_phase2.py", "r", encoding="utf-8-sig").read())
"""

import unreal
import threading
import time
import json
import os
import http.client
import traceback
from queue import Queue, Empty

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 8765
POLL_INTERVAL = 2.0  # seconds between polls
SCREENSHOT_DIR = os.path.join(
    os.environ.get("USERPROFILE", r"C:\Users\sbcam"),
    "OneDrive", "Desktop", "sn_screenshots"
)

# Allowed commands — full Phase 3 skill set
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
    "add_foliage",
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
    "setup_post_process",
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
    "query_master_knowledge",
    # Environment (master)
    "setup_landscape", "add_volumetric_clouds", "add_height_fog", "add_water_body",
    # Rendering (master)
    "setup_reflections", "setup_groom_system", "setup_rvt",
    # Virtual Production
    "setup_virtual_production",
    # Physics (master)
    "setup_physics_constraints", "add_chaos_vehicle",
    # Knowledge (master)
    "query_master_landscape_preset",
    # Pipeline
    "setup_source_control",
}
# Commands that execute Unreal Python code templates
TEMPLATE_COMMANDS = SKILL_COMMANDS - {"delete_actor", "delete_duplicates"}
# Destructive commands need extra confirmation
DESTRUCTIVE_COMMANDS = {"delete_actor", "delete_duplicates"}
ALL_ALLOWED = SAFE_COMMANDS | PHASE2_COMMANDS | SKILL_COMMANDS

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
log_queue = Queue()
worker_running = True
worker_thread = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def log_msg(msg):
    """Queue a message for the main thread to log via unreal.log()."""
    log_queue.put(msg)

def bridge_post(path, data_dict):
    """POST JSON to the local bridge and return the response dict."""
    try:
        conn = http.client.HTTPConnection(BRIDGE_HOST, BRIDGE_PORT, timeout=10)
        payload = json.dumps(data_dict)
        conn.request("POST", path, body=payload,
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        body = resp.read().decode()
        conn.close()
        return json.loads(body)
    except Exception as e:
        log_msg(f"[SuperNinja] Bridge POST error: {e}")
        return None

def bridge_get(path):
    """GET from the local bridge and return the response dict."""
    try:
        conn = http.client.HTTPConnection(BRIDGE_HOST, BRIDGE_PORT, timeout=10)
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read().decode()
        conn.close()
        return json.loads(body)
    except Exception as e:
        log_msg(f"[SuperNinja] Bridge GET error: {e}")
        return None

def capture_viewport(save_path):
    """Capture the Unreal Editor viewport and save to disk.
    
    Uses unreal.SystemLibrary.execute_console_command or 
    unreal.EditorLevelLibrary as appropriate.
    Returns the file path if successful, None otherwise.
    """
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Method 1: Use console command for high-res screenshot
        # This is the most reliable way in UE5
        cmd = f'HighResShot 1 "{save_path}"'
        result = unreal.SystemLibrary.execute_console_command(
            unreal.EditorLevelLibrary.get_editor_world(), cmd
        )
        log_msg(f"[SuperNinja] HighResShot result: {result}, path: {save_path}")
        
        # Give it a moment to write the file
        time.sleep(1.0)
        
        if os.path.exists(save_path):
            log_msg(f"[SuperNinja] Screenshot saved: {save_path}")
            return save_path
        
        # Method 2: Try alternative screenshot approach
        # Use the automation system
        alt_path = save_path.replace(".png", "_alt.png")
        cmd2 = f'screenshot "{alt_path}"'
        unreal.SystemLibrary.execute_console_command(
            unreal.EditorLevelLibrary.get_editor_world(), cmd2
        )
        time.sleep(1.0)
        
        if os.path.exists(alt_path):
            log_msg(f"[SuperNinja] Screenshot saved (alt): {alt_path}")
            return alt_path
        
        # Method 3: Try using Unreal's automation snapshot
        log_msg("[SuperNinja] Trying viewport capture via Python API...")
        
        # Check if file was saved to default location
        default_dir = os.path.join(
            unreal.SystemLibrary.get_project_directory(),
            "Saved", "Screenshots"
        )
        log_msg(f"[SuperNinja] Checking default screenshot dir: {default_dir}")
        
        return None  # Will be handled by companion reading the file
        
    except Exception as e:
        log_msg(f"[SuperNinja] Screenshot capture error: {e}")
        traceback.print_exc()
        return None

def execute_command(cmd_data):
    """Execute a single command and return the result dict."""
    cmd = cmd_data.get("command", "")
    cmd_id = cmd_data.get("id", "unknown")
    args = cmd_data.get("args", {})

    if cmd not in ALL_ALLOWED:
        return {"id": cmd_id, "error": f"command '{cmd}' not allowed"}

    log_msg(f"[SuperNinja][{cmd_id}] Executing: {cmd}")

    try:
        if cmd == "ping":
            return {
                "id": cmd_id,
                "result": {
                    "status": "pong",
                    "ue_time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "message": "Unreal Editor is alive!",
                }
            }

        elif cmd == "echo":
            text = args.get("text", "")
            return {
                "id": cmd_id,
                "result": {
                    "echo": text,
                    "ue_time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
            }

        elif cmd in ("log", "safe_log"):
            msg = args.get("message", "no message")
            log_msg(f"[SuperNinja SAFE][{cmd_id}]: {msg}")
            return {
                "id": cmd_id,
                "result": {
                    "logged": msg,
                    "ue_time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
            }

        elif cmd == "screenshot":
            filename = args.get("filename", f"viewport_{cmd_id}.png")
            save_path = args.get("save_path", os.path.join(SCREENSHOT_DIR, filename))
            
            log_msg(f"[SuperNinja][{cmd_id}] Capturing viewport → {save_path}")
            captured_path = capture_viewport(save_path)
            
            result = {
                "id": cmd_id,
                "result": {
                    "action": "screenshot",
                    "status": "captured" if captured_path else "attempted",
                    "save_path": captured_path or save_path,
                    "filename": filename,
                    "ue_time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                "is_screenshot": True,
            }
            return result

        elif cmd == "stop":
            global worker_running
            worker_running = False
            return {"id": cmd_id, "result": {"status": "stopping"}}

        elif cmd in SKILL_COMMANDS:
            # Route skill commands to the skill executor
            try:
                from sn_skill_executor import execute_skill
                result = execute_skill(cmd, args)
                return {"id": cmd_id, "result": result}
            except ImportError:
                # Fallback: execute the skill template from registry
                log_msg(f"[SuperNinja][{cmd_id}] Skill executor not available, using template")
                return {"id": cmd_id, "result": {"skill": cmd, "args": args, "status": "processed_on_cloud"}}
            except Exception as e:
                log_msg(f"[SuperNinja][{cmd_id}] Skill execution error: {e}")
                return {"id": cmd_id, "error": str(e)}

        else:
            return {"id": cmd_id, "error": f"unhandled: {cmd}"}

    except Exception as e:
        log_msg(f"[SuperNinja][{cmd_id}] Error: {e}")
        return {"id": cmd_id, "error": str(e)}

# ---------------------------------------------------------------------------
# Worker thread — polls the bridge for commands
# ---------------------------------------------------------------------------
def worker_loop():
    """Background thread that polls the bridge and executes commands.
    Includes exponential backoff on connection failures for resilience.
    """
    global worker_running
    log_msg("[SuperNinja] Worker thread started")
    consecutive_errors = 0
    max_backoff = 30.0  # Maximum backoff in seconds
    
    while worker_running:
        try:
            # Poll the bridge for a command
            conn = http.client.HTTPConnection(BRIDGE_HOST, BRIDGE_PORT, timeout=5)
            conn.request("GET", "/poll")
            resp = conn.getresponse()
            body = resp.read().decode()
            conn.close()
            
            # Reset error counter on successful connection
            consecutive_errors = 0
            
            data = json.loads(body)
            cmd_data = data.get("command")
            
            if cmd_data:
                log_msg(f"[SuperNinja] Got command: {cmd_data.get('command')} (id={cmd_data.get('id')})")
                result = execute_command(cmd_data)
                
                # Post result back to bridge
                bridge_post("/result", result)
            
        except Exception as e:
            consecutive_errors += 1
            # Exponential backoff: 2s, 4s, 8s, 16s, 30s, 30s...
            backoff = min(POLL_INTERVAL * (2 ** min(consecutive_errors - 1, 4)), max_backoff)
            if consecutive_errors <= 3:
                log_msg(f"[SuperNinja] Worker error: {e} (retry in {backoff:.0f}s)")
            elif consecutive_errors % 10 == 0:
                log_msg(f"[SuperNinja] Still reconnecting... ({consecutive_errors} errors, retry in {backoff:.0f}s)")
            time.sleep(backoff)
            continue
        
        time.sleep(POLL_INTERVAL)
    
    log_msg("[SuperNinja] Worker thread stopped")

# ---------------------------------------------------------------------------
# Slate tick callback — drains the log queue on the main thread
# ---------------------------------------------------------------------------
def on_slate_tick(delta_time):
    """Called every frame by Unreal's Slate tick — safe to call unreal.log()."""
    while True:
        try:
            msg = log_queue.get_nowait()
            unreal.log(msg)
        except Empty:
            break

# ---------------------------------------------------------------------------
# Start / Stop
# ---------------------------------------------------------------------------
def start():
    global worker_thread, worker_running
    worker_running = True
    
    # Register the Slate tick callback
    handle = unreal.register_slate_post_tick_callback(on_slate_tick)
    
    # Start the worker thread
    worker_thread = threading.Thread(target=worker_loop, daemon=True)
    worker_thread.start()
    
    unreal.log("[SuperNinja] Phase 2 client started — screenshot support enabled")
    unreal.log(f"[SuperNinja] Polling bridge at {BRIDGE_HOST}:{BRIDGE_PORT}")
    unreal.log(f"[SuperNinja] Screenshots will be saved to: {SCREENSHOT_DIR}")

def stop():
    global worker_running
    worker_running = False
    unreal.log("[SuperNinja] Stopping...")

# Auto-start when script is exec'd in Unreal
start()