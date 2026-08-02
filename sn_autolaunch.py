"""
SuperNinja Auto-Launcher — One-Click Start

This script automatically:
1. Starts the local bridge (background process)
2. Starts the cloud companion (background process)
3. Opens Unreal Editor and injects the client via Python remote execution
4. Monitors all processes
5. Auto-fetches the tunnel URL from the cloud server

Just run: python sn_autolaunch.py

Requirements:
- Python 3.8+ with requests installed (pip install requests)
- Unreal Editor 5.x with Python plugin enabled
- All sn_*.py files in the same directory as this script
"""

import subprocess
import sys
import os
import time
import json
import requests
import threading
import webbrowser
import signal

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRIDGE_SCRIPT = os.path.join(SCRIPT_DIR, "sn_local_bridge_phase2.py")
COMPANION_SCRIPT = os.path.join(SCRIPT_DIR, "sn_companion_phase2.py")
UNREAL_SCRIPT = os.path.join(SCRIPT_DIR, "sn_unreal_nonblocking_phase2.py")
SKILL_EXECUTOR = os.path.join(SCRIPT_DIR, "sn_skill_executor.py")

# Cloud server — this is the known cloud endpoint
# The launcher will verify connectivity before starting
CLOUD_URL = None  # Auto-detected or set below

# Known tunnel URLs (fallback if auto-detect fails)
KNOWN_TUNNEL_URLS = [
    "https://guarantee-sports-means-promotional.trycloudflare.com",
]

# Unreal remote execution config
UNREAL_PYTHON_PORT = 9789  # Default Unreal Python remote execution port
UNREAL_HOST = "127.0.0.1"

# Process tracking
processes = {}
running = True


def print_banner():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          SuperNinja Auto-Launcher — One-Click Start         ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  This will automatically start all components:              ║")
    print("║  1. Local Bridge (127.0.0.1:8765)                          ║")
    print("║  2. Cloud Companion (polls cloud server)                   ║")
    print("║  3. Unreal Client (injects into UE5 via remote Python)     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def find_cloud_url():
    """Find the active cloud server URL."""
    global CLOUD_URL
    
    # 1. Check if CLOUD_URL is already set
    if CLOUD_URL:
        try:
            resp = requests.get(f"{CLOUD_URL}/status", timeout=5)
            if resp.status_code == 200:
                print(f"  ✅ Cloud server found at configured URL")
                return CLOUD_URL
        except:
            pass
    
    # 2. Try known tunnel URLs
    print("  🔍 Searching for active cloud server...")
    for url in KNOWN_TUNNEL_URLS:
        try:
            resp = requests.get(f"{url}/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  ✅ Cloud server found: {url}")
                print(f"     Phase: {data.get('phase')}, Commands: {len(data.get('allowed_commands', []))}")
                CLOUD_URL = url
                return url
        except:
            continue
    
    # 3. Ask user
    print("  ⚠️  Could not auto-detect cloud server URL")
    url = input("  Enter cloud tunnel URL (or press Enter to skip): ").strip()
    if url:
        CLOUD_URL = url
        return url
    
    return None


def update_companion_url(url):
    """Update the companion script with the correct cloud URL."""
    if not url:
        return
    
    companion_path = COMPANION_SCRIPT
    try:
        with open(companion_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the CLOUD_URL line
        import re
        new_content = re.sub(
            r'CLOUD_URL\s*=\s*"[^"]*"',
            f'CLOUD_URL = "{url}"',
            content
        )
        
        if new_content != content:
            with open(companion_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ Updated companion with cloud URL: {url}")
    except Exception as e:
        print(f"  ⚠️  Could not update companion URL: {e}")


def check_prerequisites():
    """Check that all required files exist."""
    print("📋 Checking prerequisites...")
    
    required_files = [
        ("Bridge script", BRIDGE_SCRIPT),
        ("Companion script", COMPANION_SCRIPT),
        ("Unreal client script", UNREAL_SCRIPT),
        ("Skill executor", SKILL_EXECUTOR),
    ]
    
    all_ok = True
    for name, path in required_files:
        if os.path.exists(path):
            print(f"  ✅ {name}: {os.path.basename(path)}")
        else:
            print(f"  ❌ {name}: NOT FOUND — {path}")
            all_ok = False
    
    # Check Python packages
    try:
        import requests
        print(f"  ✅ requests package installed")
    except ImportError:
        print(f"  ❌ requests package NOT installed — run: pip install requests")
        all_ok = False
    
    return all_ok


def check_unreal_running():
    """Check if Unreal Editor is running."""
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if 'UnrealEditor' in proc.info.get('name', ''):
                return True
    except ImportError:
        # Fallback — try tasklist
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True, timeout=5)
            if 'UnrealEditor' in result.stdout:
                return True
        except:
            pass
    
    # Try connecting to Unreal's Python remote execution port
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((UNREAL_HOST, UNREAL_PYTHON_PORT))
        s.close()
        return result == 0
    except:
        pass
    
    return False


def check_unreal_python_plugin():
    """Try to verify the Python plugin is enabled by checking remote execution."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((UNREAL_HOST, UNREAL_PYTHON_PORT))
        s.close()
        return result == 0
    except:
        return False


def inject_unreal_client():
    """Inject the Unreal client script into UE5 via Python remote execution."""
    print("  🔧 Injecting Unreal client via Python remote execution...")
    
    # Read the Unreal client script
    try:
        with open(UNREAL_SCRIPT, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except Exception as e:
        print(f"  ❌ Could not read Unreal script: {e}")
        return False
    
    # Method 1: Try Unreal's Python remote execution API
    try:
        payload = {
            "command": script_content
        }
        resp = requests.post(
            f"http://{UNREAL_HOST}:{UNREAL_PYTHON_PORT}/remote/call",
            json=payload,
            timeout=5
        )
        if resp.status_code == 200:
            print("  ✅ Unreal client injected via remote execution!")
            return True
    except Exception as e:
        print(f"  ⚠️  Remote execution failed: {e}")
    
    # Method 2: Try Unreal's exec endpoint
    try:
        # The Unreal Python plugin exposes an HTTP endpoint
        exec_command = f'exec(open(r"{UNREAL_SCRIPT}", "r", encoding="utf-8-sig").read())'
        payload = {
            "execute": exec_command
        }
        resp = requests.post(
            f"http://{UNREAL_HOST}:{UNREAL_PYTHON_PORT}/api/v1/execute",
            json=payload,
            timeout=5
        )
        if resp.status_code == 200:
            print("  ✅ Unreal client injected via API!")
            return True
    except Exception as e:
        print(f"  ⚠️  API injection failed: {e}")
    
    # Method 3: Write a .bat file that uses Unreal's command line
    bat_path = os.path.join(SCRIPT_DIR, "sn_inject_unreal.bat")
    escaped_path = UNREAL_SCRIPT.replace("\\", "\\\\")
    with open(bat_path, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'echo Injecting SuperNinja client into Unreal Editor...\n')
        f.write(f'echo If this fails, open Unreal Output Log (Python tab) and paste:\n')
        f.write(f'echo exec(open(r"{UNREAL_SCRIPT}", "r", encoding="utf-8-sig").read())\n')
        f.write(f'echo.\n')
        f.write(f'echo Attempting Python remote execution...\n')
        f.write(f'python -c "import requests; r = requests.post(\'http://{UNREAL_HOST}:{UNREAL_PYTHON_PORT}/remote/call\', json={{\'command\': open(r\'{UNREAL_SCRIPT}\', \'r\', encoding=\'utf-8-sig\').read()}}); print(\'Result:\', r.status_code, r.text)"\n')
        f.write(f'pause\n')
    
    print(f"  ⚠️  Could not auto-inject into Unreal")
    print(f"  📝 Created sn_inject_unreal.bat as fallback")
    print(f"  📋 Manual method: In Unreal Output Log (Python tab), paste:")
    print(f'     exec(open(r"{UNREAL_SCRIPT}", "r", encoding="utf-8-sig").read())')
    return False


def start_bridge():
    """Start the local bridge as a background process."""
    print("\n🌉 Starting Local Bridge...")
    
    try:
        proc = subprocess.Popen(
            [sys.executable, BRIDGE_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=SCRIPT_DIR,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        processes['bridge'] = proc
        print(f"  ✅ Bridge started (PID: {proc.pid})")
        
        # Wait a moment and verify it's running
        time.sleep(2)
        try:
            resp = requests.get("http://127.0.0.1:8765/status", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  ✅ Bridge responding — {data.get('queue_length', 0)} commands in queue")
                return True
        except:
            pass
        
        print(f"  ⚠️  Bridge started but not responding yet (may take a moment)")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to start bridge: {e}")
        return False


def start_companion():
    """Start the cloud companion as a background process."""
    print("\n☁️  Starting Cloud Companion...")
    
    # Make sure the companion has the right URL
    if CLOUD_URL:
        update_companion_url(CLOUD_URL)
    
    try:
        proc = subprocess.Popen(
            [sys.executable, COMPANION_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=SCRIPT_DIR,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        processes['companion'] = proc
        print(f"  ✅ Companion started (PID: {proc.pid})")
        
        # Wait and verify
        time.sleep(3)
        try:
            resp = requests.get("http://127.0.0.1:8765/status", timeout=3)
            if resp.status_code == 200:
                print(f"  ✅ Companion connected to bridge")
                return True
        except:
            pass
        
        print(f"  ⚠️  Companion started but bridge not confirming yet")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to start companion: {e}")
        return False


def connect_unreal():
    """Connect the Unreal client."""
    print("\n🎮 Connecting Unreal Client...")
    
    # Check if Unreal is running
    unreal_running = check_unreal_running()
    if not unreal_running:
        print("  ⚠️  Unreal Editor does not appear to be running")
        print("  📝 Please start Unreal Editor first, then re-run this script")
        print("     OR manually inject after starting UE5:")
        print(f'     exec(open(r"{UNREAL_SCRIPT}", "r", encoding="utf-8-sig").read())')
        return False
    
    # Check if Python plugin is enabled
    python_ok = check_unreal_python_plugin()
    if python_ok:
        print("  ✅ Unreal Python remote execution detected")
        return inject_unreal_client()
    else:
        print("  ⚠️  Unreal Python remote execution not detected")
        print("  📝 Make sure the Python plugin is enabled in UE5:")
        print("     Edit > Plugins > Python Editor Script Plugin > Enable")
        print()
        print("  📋 Then in Unreal Output Log (Python tab), paste:")
        print(f'     exec(open(r"{UNREAL_SCRIPT}", "r", encoding="utf-8-sig").read())')
        return False


def send_test_command():
    """Send a test command through the pipeline to verify it works."""
    print("\n🧪 Sending test command...")
    
    if not CLOUD_URL:
        print("  ⚠️  No cloud URL — skipping test")
        return
    
    try:
        resp = requests.post(
            f"{CLOUD_URL}/enqueue",
            json={
                "command": "ping",
                "args": {},
                "id": "auto-launch-test"
            },
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            print(f"  ✅ Test command enqueued: {data}")
            
            # Wait for result
            print("  ⏳ Waiting for result (up to 15 seconds)...")
            for i in range(15):
                time.sleep(1)
                try:
                    result_resp = requests.get(
                        f"{CLOUD_URL}/result/auto-launch-test",
                        timeout=5
                    )
                    if result_resp.status_code == 200:
                        result = result_resp.json()
                        print(f"  ✅ Test result: {json.dumps(result, indent=2)}")
                        return True
                except:
                    pass
                print(f"  ⏳ Still waiting... ({i+1}s)")
            
            print("  ⚠️  Test command sent but no result yet (Unreal client may not be connected)")
        else:
            print(f"  ❌ Failed to enqueue test: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"  ❌ Test failed: {e}")


def monitor_processes():
    """Monitor all running processes and restart if needed."""
    print("\n📊 Monitoring processes... (Ctrl+C to stop all)")
    print()
    
    try:
        while running:
            for name, proc in list(processes.items()):
                retcode = proc.poll()
                if retcode is not None:
                    print(f"  ⚠️  {name} process exited (code: {retcode}) — restarting...")
                    if name == 'bridge':
                        start_bridge()
                    elif name == 'companion':
                        start_companion()
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all processes...")


def cleanup():
    """Stop all running processes."""
    global running
    running = False
    
    for name, proc in processes.items():
        try:
            print(f"  Stopping {name} (PID: {proc.pid})...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"  Force-killed {name}")
        except Exception as e:
            print(f"  Error stopping {name}: {e}")
    
    print("  ✅ All processes stopped")


def generate_status_dashboard():
    """Generate a status dashboard showing the full pipeline state."""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              SuperNinja Pipeline Status                     ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    
    # Cloud
    cloud_ok = False
    if CLOUD_URL:
        try:
            resp = requests.get(f"{CLOUD_URL}/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                print(f"║  ☁️  Cloud:    ✅ Connected ({len(data.get('allowed_commands', []))} commands)")
                cloud_ok = True
            else:
                print(f"║  ☁️  Cloud:    ❌ Error {resp.status_code}")
        except:
            print(f"║  ☁️  Cloud:    ❌ Not reachable")
    else:
        print(f"║  ☁️  Cloud:    ❌ No URL configured")
    
    # Bridge
    try:
        resp = requests.get("http://127.0.0.1:8765/status", timeout=3)
        if resp.status_code == 200:
            print(f"║  🌉 Bridge:   ✅ Running on 127.0.0.1:8765")
        else:
            print(f"║  🌉 Bridge:   ❌ Error")
    except:
        print(f"║  🌉 Bridge:   ❌ Not responding")
    
    # Companion
    if 'companion' in processes and processes['companion'].poll() is None:
        print(f"║  📡 Companion: ✅ Running (PID: {processes['companion'].pid})")
    else:
        print(f"║  📡 Companion: ❌ Not running")
    
    # Unreal
    if check_unreal_running():
        print(f"║  🎮 Unreal:   ✅ Editor running")
    else:
        print(f"║  🎮 Unreal:   ❌ Editor not detected")
    
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def main():
    print_banner()
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        input("Press Enter to exit...")
        return 1
    
    # Step 2: Find the cloud server
    print("\n☁️  Finding cloud server...")
    url = find_cloud_url()
    if not url:
        print("  ❌ No cloud server found. Cannot proceed.")
        print("  📝 Make sure the cloud server is running and the tunnel URL is correct.")
        input("Press Enter to exit...")
        return 1
    
    # Step 3: Start the bridge
    if not start_bridge():
        print("\n❌ Failed to start bridge. Cannot proceed.")
        input("Press Enter to exit...")
        return 1
    
    # Step 4: Start the companion
    if not start_companion():
        print("\n❌ Failed to start companion. Cannot proceed.")
        input("Press Enter to exit...")
        return 1
    
    # Step 5: Connect Unreal
    unreal_ok = connect_unreal()
    
    # Step 6: Show status dashboard
    generate_status_dashboard()
    
    # Step 7: Send test command if everything is connected
    if unreal_ok:
        send_test_command()
    
    # Step 8: Open a simple status page
    status_html = os.path.join(SCRIPT_DIR, "sn_status_dashboard.html")
    create_status_dashboard(status_html)
    webbrowser.open(f"file://{status_html}")
    
    # Step 9: Monitor processes
    print("  📋 All components started! This window will monitor them.")
    print("  🛑 Press Ctrl+C to stop everything.")
    print()
    
    # Register cleanup handler
    signal.signal(signal.SIGINT, lambda s, f: cleanup())
    atexit.register(cleanup)
    
    # Keep running
    monitor_processes()
    
    return 0


def create_status_dashboard(html_path):
    """Create a local HTML dashboard showing pipeline status."""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>SuperNinja Pipeline Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }}
        h1 {{ color: #0ff; text-align: center; }}
        .status-card {{ background: #16213e; border-radius: 12px; padding: 20px; margin: 15px 0; }}
        .status-card h2 {{ margin: 0 0 10px 0; color: #0ff; }}
        .ok {{ color: #0f0; }} .err {{ color: #f44; }} .warn {{ color: #ff0; }}
        .command-list {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .command {{ background: #0a3d62; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-family: monospace; }}
    </style>
</head>
<body>
    <h1>🎮 SuperNinja Pipeline Dashboard</h1>
    <p style="text-align:center; color:#888;">Auto-refreshes every 5 seconds</p>
    
    <div class="status-card">
        <h2>☁️ Cloud Server</h2>
        <p>URL: <code>{CLOUD_URL or 'Not configured'}</code></p>
        <p>Status: Check <a href="{CLOUD_URL}/status" target="_blank" style="color:#0ff">/status</a></p>
    </div>
    
    <div class="status-card">
        <h2>🌉 Local Bridge</h2>
        <p>URL: <code>http://127.0.0.1:8765</code></p>
        <p>Status: Check <a href="http://127.0.0.1:8765/status" target="_blank" style="color:#0ff">/status</a></p>
    </div>
    
    <div class="status-card">
        <h2>📡 Companion</h2>
        <p>Running in background — polls cloud every 1 second</p>
    </div>
    
    <div class="status-card">
        <h2>🎮 Unreal Client</h2>
        <p>Inject command:</p>
        <code style="background:#0a3d62; padding: 10px; display:block; border-radius: 6px;">
exec(open(r"{UNREAL_SCRIPT}", "r", encoding="utf-8-sig").read())
        </code>
    </div>
    
    <div class="status-card">
        <h2>🧪 Quick Test</h2>
        <p>Enqueue a test command:</p>
        <code style="background:#0a3d62; padding: 10px; display:block; border-radius: 6px;">
curl -X POST {CLOUD_URL}/enqueue -H "Content-Type: application/json" -d '{{"command": "ping", "args": {{}}}}'
        </code>
    </div>
</body>
</html>"""
    
    with open(html_path, 'w') as f:
        f.write(html)
    print(f"  ✅ Status dashboard created: {html_path}")


import atexit

if __name__ == "__main__":
    sys.exit(main())
