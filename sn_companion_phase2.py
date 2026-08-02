"""
SuperNinja Windows Companion — Full Pipeline (Auto-Discover) [HARDENED]

Runs on the Windows PC. Polls the SuperNinja cloud endpoint outbound,
fetches commands, forwards them to the local bridge (127.0.0.1:8765)
which queues them for the Unreal Python client to pick up.
The Unreal client executes the command and posts the result back to the bridge.
The companion then picks up the result and posts it back to the cloud.

Pipeline: Cloud → Companion → Bridge → Unreal → Bridge → Companion → Cloud

Run: python sn_companion_phase2.py
Requires: pip install requests

The cloud URL is auto-discovered by:
1. Checking the SN_CLOUD_URL environment variable
2. Checking a cloud_url.txt file in the same directory
3. Checking known tunnel URLs
4. Asking the user

Hardening (Sprint 75 batch A):
- Specific exception types instead of bare `except:`
- File lock when reading/writing cloud_url.txt
- Companion-side allowlist sanity check (defense in depth)
- sys.exit(1) on fatal startup errors (already present, kept)
- All HTTP calls already use `requests` with timeouts
"""

import json
import time
import os
import base64
import sys
import logging
import requests  # pip install requests
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    Timeout, RequestException, HTTPError,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=os.environ.get("SN_LOG_LEVEL", "INFO"),
    format="[Companion] %(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("sn.companion")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CLOUD_URL = None
BRIDGE_URL = "http://127.0.0.1:8765"

SCREENSHOT_DIR = os.path.join(
    os.environ.get("USERPROFILE", r"C:\Users\sbcam"),
    "OneDrive", "Desktop", "sn_screenshots"
)

CLOUD_POLL_INTERVAL = 1.0
BRIDGE_RESULT_POLL = 0.5
RESULT_WAIT_TIMEOUT = 60.0  # raised for long-running skills (task 15)

MAX_SCREENSHOT_SIZE = 10 * 1024 * 1024

KNOWN_TUNNEL_URLS = [
    "https://refined-tough-museums-florence.trycloudflare.com",
    "https://receivers-brakes-madrid-sunset.trycloudflare.com",
]

CLOUD_URL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cloud_url.txt")

# Companion-side allowlist (defense in depth — task 8).
# This MUST be a superset of any command we are willing to forward to the bridge.
ALLOWED_COMMANDS = {
    # Core
    "ping", "echo", "log", "safe_log", "stop", "screenshot",
    # Lighting
    "add_directional_light", "add_point_light", "add_spot_light",
    "add_sky_light", "adjust_light", "light_scene",
    # Placement
    "spawn_actor", "move_actor", "rotate_actor", "scale_actor",
    "scatter_actors", "scatter_props", "delete_actor", "delete_duplicates",
    # Analysis
    "list_actors", "find_actors", "get_scene_info", "take_screenshot",
    # Camera
    "frame_viewport",
    # Environment
    "add_exponential_height_fog", "add_sky_atmosphere", "add_volumetric_cloud",
    "add_post_process_volume", "set_skybox",
    # Procedural
    "add_foliage", "add_landscape",
    # Utility
    "run_python_snippet", "save_to_file", "load_from_file",
    "clear_scene", "undo_last_command", "export_scene_json", "import_scene_json",
    "batch_execute", "replay",
    # Knowledge
    "kb_query", "kb_recommend",
}

# String -> bool helper (task 14)
_TRUTHY = {"1", "true", "yes", "on", "y", "t"}
_FALSY = {"0", "false", "no", "off", "n", "f", ""}

def _to_bool(v, default=False):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in _TRUTHY:
            return True
        if s in _FALSY:
            return False
    return default


# ---------------------------------------------------------------------------
# File-locked read/write of cloud_url.txt (task 11)
# ---------------------------------------------------------------------------
def _locked_read_url():
    """Read CLOUD_URL_FILE with a best-effort cross-platform file lock."""
    if not os.path.exists(CLOUD_URL_FILE):
        return ""
    try:
        with open(CLOUD_URL_FILE, "r", encoding="utf-8") as f:
            try:
                # Unix
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            except (ImportError, OSError):
                pass  # Windows / unsupported FS — fall back to no lock
            return f.read().strip()
    except OSError as e:
        log.warning("Could not read %s: %s", CLOUD_URL_FILE, e)
        return ""


def _locked_write_url(url):
    """Atomically write CLOUD_URL_FILE."""
    tmp = CLOUD_URL_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            try:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            except (ImportError, OSError):
                pass
            f.write(url)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, CLOUD_URL_FILE)
        return True
    except OSError as e:
        log.warning("Could not write %s: %s", CLOUD_URL_FILE, e)
        return False


def _ping_status(url, timeout=5):
    try:
        resp = requests.get(f"{url}/status", timeout=timeout)
        return resp.status_code == 200
    except (RequestsConnectionError, Timeout, RequestException):
        return False


# ---------------------------------------------------------------------------
# Cloud URL discovery
# ---------------------------------------------------------------------------
def discover_cloud_url():
    """Auto-discover the cloud server URL using multiple methods."""

    # 1) env var
    env_url = os.environ.get("SN_CLOUD_URL", "").strip()
    if env_url:
        if _ping_status(env_url):
            log.info("✅ Found cloud via env var: %s", env_url)
            return env_url
        log.warning("⚠️  SN_CLOUD_URL set but not reachable: %s", env_url)

    # 2) saved file
    saved_url = _locked_read_url()
    if saved_url and _ping_status(saved_url):
        log.info("✅ Found cloud via saved URL: %s", saved_url)
        return saved_url
    elif saved_url:
        log.warning("⚠️  Saved URL not reachable: %s", saved_url)

    # 3) local /tunnel_url
    for local_port in [8791]:
        try:
            resp = requests.get(f"http://localhost:{local_port}/tunnel_url", timeout=2)
            if resp.status_code == 200:
                tunnel_url = resp.json().get("tunnel_url")
                if tunnel_url and _ping_status(tunnel_url):
                    log.info("✅ Found cloud via local server tunnel: %s", tunnel_url)
                    _locked_write_url(tunnel_url)
                    return tunnel_url
        except (RequestsConnectionError, Timeout, RequestException, ValueError):
            pass

    # 4) known tunnel list
    log.info("🔍 Searching for active cloud server...")
    for url in KNOWN_TUNNEL_URLS:
        try:
            resp = requests.get(f"{url}/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                log.info("✅ Found cloud server: %s (commands=%d)",
                         url, len(data.get("allowed_commands", [])))
                _locked_write_url(url)
                return url
        except (RequestsConnectionError, Timeout, RequestException, ValueError):
            continue

    # 5) ask user (interactive only)
    log.warning("⚠️  Could not auto-discover cloud server")
    if not sys.stdin.isatty():
        return None
    url = input("[Companion] Enter cloud URL (or press Enter to exit): ").strip()
    if url:
        _locked_write_url(url)
        return url
    return None


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------
def poll_cloud():
    try:
        resp = requests.get(f"{CLOUD_URL}/poll", timeout=10)
        if resp.status_code == 200:
            return resp.json().get("command")
    except Timeout:
        log.debug("Poll timeout")
    except (RequestsConnectionError, RequestException) as e:
        log.warning("Poll error: %s", e)
    except ValueError as e:
        log.warning("Poll JSON decode error: %s", e)
    return None


def forward_to_bridge(cmd_data):
    try:
        resp = requests.post(f"{BRIDGE_URL}/command", json=cmd_data, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        log.warning("Bridge error: %s %s", resp.status_code, resp.text[:200])
    except (RequestsConnectionError, Timeout, RequestException) as e:
        log.warning("Bridge connection error: %s", e)
    except ValueError as e:
        log.warning("Bridge JSON decode error: %s", e)
    return None


def wait_for_bridge_result(cmd_id, timeout=RESULT_WAIT_TIMEOUT):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f"{BRIDGE_URL}/result?id={cmd_id}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                result = data.get("result")
                if result is not None:
                    return result
        except (RequestsConnectionError, Timeout, RequestException, ValueError):
            pass
        time.sleep(BRIDGE_RESULT_POLL)
    log.warning("Timeout waiting for result: %s", cmd_id)
    return None


def post_result_to_cloud(result_data):
    try:
        resp = requests.post(f"{CLOUD_URL}/result", json=result_data, timeout=15)
        if resp.status_code == 200:
            log.info("Result posted to cloud: %s", result_data.get("id"))
            return True
        log.warning("Cloud result error: %s", resp.status_code)
    except (RequestsConnectionError, Timeout, RequestException) as e:
        log.warning("Cloud result post error: %s", e)
    return False


def upload_screenshot_to_cloud(cmd_id, filepath):
    try:
        if not os.path.exists(filepath):
            log.warning("Screenshot file not found: %s", filepath)
            return False
        file_size = os.path.getsize(filepath)
        if file_size > MAX_SCREENSHOT_SIZE:
            log.warning("Screenshot too large: %d bytes", file_size)
            return False
        with open(filepath, "rb") as f:
            png_data = f.read()
        data_b64 = base64.b64encode(png_data).decode()
        filename = os.path.basename(filepath)
        resp = requests.post(
            f"{CLOUD_URL}/upload_screenshot",
            json={"id": cmd_id, "filename": filename, "data_b64": data_b64},
            timeout=30,
        )
        if resp.status_code == 200:
            log.info("Screenshot uploaded: %s (%d bytes)", filename, file_size)
            return True
        log.warning("Screenshot upload error: %s", resp.status_code)
    except (OSError, RequestsConnectionError, Timeout, RequestException) as e:
        log.warning("Screenshot upload error: %s", e)
    return False


def wait_for_screenshot(filepath, timeout=15.0):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(filepath):
            try:
                size1 = os.path.getsize(filepath)
                time.sleep(0.3)
                size2 = os.path.getsize(filepath)
                if size1 == size2 and size1 > 0:
                    return True
            except OSError:
                pass
        time.sleep(0.5)
    return False


def handle_command(cmd_data):
    cmd = cmd_data.get("command", "")
    cmd_id = cmd_data.get("id", "unknown")

    # Defense-in-depth allowlist (task 8) — refuse any command we don't recognize.
    if cmd not in ALLOWED_COMMANDS:
        log.warning("Refusing unknown command: %s (id=%s)", cmd, cmd_id)
        post_result_to_cloud({
            "id": cmd_id,
            "result": {"error": "command_not_allowed", "command": cmd},
            "is_screenshot": False,
        })
        return

    log.info("Processing: %s (id=%s)", cmd, cmd_id)

    bridge_resp = forward_to_bridge(cmd_data)
    if not bridge_resp or bridge_resp.get("status") != "queued":
        log.warning("Bridge queue failed: %s", bridge_resp)
        post_result_to_cloud({
            "id": cmd_id,
            "result": {"error": "bridge_queue_failed", "detail": str(bridge_resp)},
            "is_screenshot": False,
        })
        return

    bridge_result = wait_for_bridge_result(cmd_id)
    if bridge_result is None:
        post_result_to_cloud({
            "id": cmd_id,
            "result": {"error": "unreal_timeout", "command": cmd},
            "is_screenshot": False,
        })
        return

    if cmd == "screenshot" and bridge_result.get("result", {}).get("save_path"):
        save_path = bridge_result["result"]["save_path"]
        if wait_for_screenshot(save_path):
            upload_ok = upload_screenshot_to_cloud(cmd_id, save_path)
            bridge_result["result"]["upload_status"] = "uploaded" if upload_ok else "captured"

    post_result_to_cloud({
        "id": cmd_id,
        "result": bridge_result.get("result", {}),
        "is_screenshot": cmd == "screenshot",
    })


def main():
    global CLOUD_URL

    CLOUD_URL = discover_cloud_url()
    if len(sys.argv) > 1:
        arg_url = sys.argv[1].strip()
        if _ping_status(arg_url):
            CLOUD_URL = arg_url
            log.info("✅ Using command-line URL: %s", arg_url)
        else:
            log.warning("⚠️  Command-line URL not reachable: %s", arg_url)

    if not CLOUD_URL:
        log.error("❌ No cloud server found. Exiting.")
        log.error("   Usage: python sn_companion_phase2.py [CLOUD_URL]")
        log.error("   Or set SN_CLOUD_URL or create cloud_url.txt")
        sys.exit(1)

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  SuperNinja Windows Companion — Full Pipeline               ║")
    print(f"║  Cloud:  {CLOUD_URL[:43]:<43s}  ║")
    print(f"║  Bridge: {BRIDGE_URL[:43]:<43s}  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    try:
        resp = requests.get(f"{CLOUD_URL}/status", timeout=10)
        data = resp.json()
        log.info("☁️  Cloud connected: %d commands available",
                 len(data.get("allowed_commands", [])))
    except (RequestsConnectionError, Timeout, RequestException, ValueError) as e:
        log.warning("⚠️  Cannot reach cloud: %s", e)

    try:
        requests.get(f"{BRIDGE_URL}/status", timeout=5)
        log.info("🌉 Bridge connected")
    except (RequestsConnectionError, Timeout, RequestException) as e:
        log.warning("⚠️  Cannot reach bridge: %s", e)
        log.warning("   Make sure sn_local_bridge_phase2.py is running first!")

    log.info("Polling cloud every %.1fs... (Ctrl+C to stop)", CLOUD_POLL_INTERVAL)

    try:
        while True:
            cmd = poll_cloud()
            if cmd:
                handle_command(cmd)
            time.sleep(CLOUD_POLL_INTERVAL)
    except KeyboardInterrupt:
        log.info("Stopped.")


if __name__ == "__main__":
    main()
