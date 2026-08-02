"""
SuperNinja Tunnel Manager

Automatically:
1. Starts a Cloudflare quick tunnel
2. Detects the public URL
3. Publishes it to the cloud server's /set_tunnel_url endpoint
4. Writes it to cloud_url.txt for the Windows companion to download
5. Monitors the tunnel and restarts if it goes down
6. Serves cloud_url.txt via HTTP so companions can auto-discover

Run: python sn_tunnel_manager.py
"""

import subprocess
import sys
import os
import time
import re
import requests
import threading
import signal

CLOUD_SERVER_PORT = 8791
CLOUD_SERVER_HOST = "localhost"
CLOUD_SERVER_URL = f"http://{CLOUD_SERVER_HOST}:{CLOUD_SERVER_PORT}"

# File where the current tunnel URL is saved (Windows companion can download this)
CLOUD_URL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cloud_url.txt")

# Known tunnel URLs from previous runs (for companions to try)
KNOWN_URLS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "known_tunnels.txt")

running = True
tunnel_process = None
current_tunnel_url = None


def start_tunnel():
    """Start a Cloudflare quick tunnel and return the public URL."""
    global tunnel_process
    
    print("[TunnelManager] Starting Cloudflare tunnel...")
    
    # Start cloudflared
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{CLOUD_SERVER_PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    tunnel_process = process
    
    # Read output to find the URL
    url = None
    start_time = time.time()
    timeout = 30
    
    while time.time() - start_time < timeout:
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None:
                print(f"[TunnelManager] cloudflared exited with code {process.returncode}")
                return None
            time.sleep(0.5)
            continue
        
        # Look for the URL in the output
        match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
        
        # Print important lines
        if any(kw in line for kw in ["ERR", "INF |", "Registered", "Your quick"]):
            print(f"[TunnelManager] {line.strip()}")
    
    if url:
        print(f"[TunnelManager] ✅ Tunnel active: {url}")
    else:
        print(f"[TunnelManager] ❌ Could not detect tunnel URL")
    
    return url


def publish_tunnel_url(url):
    """Publish the tunnel URL to the cloud server and save to file."""
    global current_tunnel_url
    current_tunnel_url = url
    
    # 1. Tell the cloud server
    try:
        resp = requests.post(
            f"{CLOUD_SERVER_URL}/set_tunnel_url",
            json={"tunnel_url": url},
            timeout=5
        )
        if resp.status_code == 200:
            print(f"[TunnelManager] ✅ Published to cloud server")
        else:
            print(f"[TunnelManager] ⚠️  Cloud server responded: {resp.status_code}")
    except Exception as e:
        print(f"[TunnelManager] ⚠️  Could not publish to cloud server: {e}")
    
    # 2. Write to file
    try:
        with open(CLOUD_URL_FILE, 'w') as f:
            f.write(url)
        print(f"[TunnelManager] ✅ Saved to {CLOUD_URL_FILE}")
    except Exception as e:
        print(f"[TunnelManager] ⚠️  Could not save URL file: {e}")
    
    # 3. Append to known URLs
    try:
        known = set()
        if os.path.exists(KNOWN_URLS_FILE):
            with open(KNOWN_URLS_FILE, 'r') as f:
                known = set(line.strip() for line in f if line.strip())
        known.add(url)
        with open(KNOWN_URLS_FILE, 'w') as f:
            for u in sorted(known):
                f.write(u + '\n')
    except Exception as e:
        print(f"[TunnelManager] ⚠️  Could not update known URLs: {e}")


def verify_tunnel(url):
    """Verify the tunnel is working by making a request through it."""
    try:
        resp = requests.get(f"{url}/status", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[TunnelManager] ✅ Tunnel verified — Phase {data.get('phase')}, {len(data.get('allowed_commands', []))} commands")
            return True
        else:
            print(f"[TunnelManager] ⚠️  Tunnel responded with {resp.status_code}")
            return False
    except Exception as e:
        print(f"[TunnelManager] ❌ Tunnel verification failed: {e}")
        return False


def monitor_tunnel():
    """Monitor the tunnel process and restart if it dies."""
    global running
    
    print("[TunnelManager] 🔄 Monitoring tunnel... (Ctrl+C to stop)")
    
    while running:
        # Check if tunnel process is still alive
        if tunnel_process and tunnel_process.poll() is not None:
            print(f"[TunnelManager] ⚠️  Tunnel process died (code: {tunnel_process.returncode})")
            print("[TunnelManager] 🔄 Restarting tunnel...")
            
            url = start_tunnel()
            if url:
                publish_tunnel_url(url)
                verify_tunnel(url)
            else:
                print("[TunnelManager] ❌ Failed to restart tunnel, retrying in 10s...")
                time.sleep(10)
                continue
        
        # Verify the tunnel is reachable
        if current_tunnel_url:
            try:
                resp = requests.get(f"{current_tunnel_url}/status", timeout=10)
                if resp.status_code != 200:
                    print(f"[TunnelManager] ⚠️  Tunnel not responding correctly")
            except:
                print(f"[TunnelManager] ⚠️  Tunnel not reachable, may need restart")
        
        time.sleep(30)  # Check every 30 seconds


def cleanup(signum=None, frame=None):
    global running
    running = False
    
    if tunnel_process:
        print("[TunnelManager] Stopping tunnel...")
        tunnel_process.terminate()
        try:
            tunnel_process.wait(timeout=5)
        except:
            tunnel_process.kill()
    
    print("[TunnelManager] Done.")
    sys.exit(0)


def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          SuperNinja Tunnel Manager                          ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  Automatically manages the Cloudflare tunnel                ║")
    print("║  Publishes URL to cloud server + file                       ║")
    print("║  Monitors and restarts if needed                            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Verify cloud server is running
    try:
        resp = requests.get(f"{CLOUD_SERVER_URL}/status", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[TunnelManager] ✅ Cloud server running (Phase {data.get('phase')})")
        else:
            print(f"[TunnelManager] ⚠️  Cloud server responded with {resp.status_code}")
    except:
        print(f"[TunnelManager] ❌ Cloud server not running on port {CLOUD_SERVER_PORT}")
        print(f"[TunnelManager]    Start it first: python superninja_cloud_command_server.py")
        sys.exit(1)
    
    # Start the tunnel
    url = start_tunnel()
    if not url:
        print("[TunnelManager] ❌ Failed to start tunnel")
        sys.exit(1)
    
    # Publish the URL
    publish_tunnel_url(url)
    
    # Verify it works
    verify_tunnel(url)
    
    # Print info for the user
    print()
    print(f"🔗 Tunnel URL: {url}")
    print(f"📄 URL saved to: {CLOUD_URL_FILE}")
    print()
    print("📋 Windows companion can auto-discover this URL by:")
    print(f"   1. Reading {CLOUD_URL_FILE}")
    print(f"   2. Checking the cloud server's /tunnel_url endpoint")
    print(f"   3. Setting SN_CLOUD_URL env var to: {url}")
    print()
    
    # Register cleanup handler
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # Monitor the tunnel
    monitor_tunnel()


if __name__ == "__main__":
    main()
