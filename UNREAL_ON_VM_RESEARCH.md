# Running Unreal Engine on Our VM — Full Research Report

**Date:** May 11, 2025
**Question:** Can we run Unreal Engine inside our SuperNinja sandbox/VM, or somehow leverage what we already have?
**Short Answer:** ❌ Not on **this** VM, but ✅ **YES** through several alternative paths.

---

## 1. Our Current VM — The Hard Numbers

I just inspected the actual sandbox we're operating in:

| Resource | What We Have | What UE5 Editor Needs | Verdict |
|----------|--------------|------------------------|---------|
| **OS** | Debian 12 (Docker container) | Linux supported, but headed | ⚠️ Container limits |
| **CPU** | 2 cores (Xeon, virtualized KVM) | 6+ cores recommended | ❌ Way under |
| **RAM** | 3.8 GB total, 2.8 GB free | 32 GB minimum, 64 GB recommended | ❌ Critical fail |
| **Disk** | 8.8 GB total, 3.5 GB free | 100+ GB for engine + assets | ❌ Critical fail |
| **GPU** | **None** (no VGA, no NVIDIA) | DX12 or Vulkan GPU mandatory | ❌ Critical fail |
| **Display** | None (Xvfb available) | Needs framebuffer | ⚠️ Partial |
| **Sudo** | Available | Needed for installs | ✅ |
| **Internet** | Working (HTTP 200) | Needed for downloads | ✅ |

### Bottom line on this VM

The UE5 editor binary is roughly **40 GB just to download and install**. We have **3.5 GB free**. Even if we had the disk space, the editor would refuse to launch without a GPU (Vulkan RHI rejects software rendering by default), and 3.8 GB of RAM is below the threshold for even loading an empty project.

**Running the full UE5 Editor in this sandbox is not physically possible.**

---

## 2. What IS Possible — 5 Real Options

I researched this thoroughly. Here are the realistic paths, ranked by feasibility:

---

### ⭐ Option 1: Headless UE5 Commandlet (Limited but free)

**What it is:** Unreal Engine has a "headless" mode where you run the editor binary as a command-line tool with the flags `-nullrhi -unattended` and execute Python scripts via commandlets. No GUI, no GPU rendering, no viewport.

**What works in this mode:**
- ✅ Load `.uproject` files
- ✅ Run Python scripts via `unreal.PythonScriptLibrary`
- ✅ Spawn actors, modify levels, save assets
- ✅ Cooking, packaging, asset import
- ✅ Most of our 60 skills (spawn, move, delete, materials, blueprints)

**What does NOT work:**
- ❌ Viewport screenshots (no rendering)
- ❌ Any visual feedback
- ❌ Lighting builds (Lumen needs GPU)
- ❌ Niagara real-time previews
- ❌ Live editing (it's batch only)

**Disk requirement:** ~40 GB (full engine), or ~15 GB (Linux server target only)

**Verdict for this VM:** ❌ Still no — we don't have the disk space. Would need an upgrade to ≥60 GB disk and ≥8 GB RAM.

**If we had a bigger VM:** Could work for ~70% of our skills. The big loss is "show the user what you built."

---

### ⭐⭐ Option 2: Cloud GPU Rental (Most realistic)

Rent a GPU VM by the hour, install UE5, point our companion at it. This is the path that **actually puts a working Unreal in front of SuperNinja today**.

| Provider | GPU | Cost/hr | Notes |
|----------|-----|---------|-------|
| **Vast.ai** | RTX 3090 / 4090 | $0.20 – $0.50 | Cheapest, community marketplace |
| **RunPod** | RTX 4090 | $0.34 – $0.70 | Better UX, persistent volumes |
| **Paperspace** | A4000 / A6000 | $0.51 – $1.89 | Per-second billing, polished |
| **Google Cloud** | T4 / L4 / A100 | $0.35 – $3.67 | Windows workstation images exist |
| **AWS EC2 G4/G5** | T4 / A10G | $0.53 – $1.21 | Amazon's official UE5 guide exists |
| **Shadow PC** | GTX 1080+ | $30/month flat | Pre-configured "Unreal Engine 5" tier |

**Architecture would be:**
```
SuperNinja Cloud Server (this VM, port 8791)
       ↓ Cloudflare tunnel
Rented GPU VM (Windows or Linux + UE5 installed)
   ├─ sn_local_bridge.py    (port 8765)
   ├─ sn_companion.py
   └─ Unreal Editor running with our Python client injected
```

**Setup time:** 30–60 minutes the first time.
**Best fit:** Vast.ai with a Windows image at ~$0.30/hr. Spin up only when testing.

**This is what I recommend for actually validating the system.**

---

### ⭐⭐⭐ Option 3: User's Own Windows PC (Already designed for this!)

This is the **path SuperNinja was actually built around**, and it requires zero new infrastructure.

**Reality check:** Everything in `superninja_windows_package.zip` is already designed to run on a user's gaming PC. The cloud VM (us) hosts the brain. The user's Windows machine runs the bridge + companion + Unreal. The Cloudflare tunnel connects them.

**Why this is the right answer most of the time:**
- ✅ Free (user already owns hardware)
- ✅ Real GPU, real performance
- ✅ Already 100% built and packaged
- ✅ One-click launcher exists (`START_SUPERNINJA.bat`)
- ⚠️ Requires the user to start it

**If the user has a Windows PC with UE5 installed → we're done. The system works.**

---

### ⭐ Option 4: Cross-Compile a Custom Headless Target

Build a stripped-down UE binary that contains *only* the modules we need (CoreUObject, basic Engine) and runs on a tiny Linux VM. This is what the `slowburn.dev` article describes — a custom `Target.cs` that compiles to a few-hundred-MB binary instead of a 40 GB editor.

**Pros:**
- Tiny footprint (~500 MB instead of 40 GB)
- Can run on modest hardware
- No GPU needed

**Cons:**
- ❌ Requires UE5 source build (multi-hour compile, needs a dev machine first)
- ❌ Loses Editor scripting (no `EditorLevelLibrary`, no actor spawning the way we do it)
- ❌ Most of our 60 skills wouldn't work — they depend on Editor modules
- ❌ Weeks of dev work

**Verdict:** Theoretically interesting, practically wrong tool. We'd be rebuilding our system from scratch around a different API surface.

---

### ⭐ Option 5: Pixel Streaming (Stream the GPU output)

Run Unreal on a remote GPU machine and stream pixels over WebRTC to our cloud VM, which displays/forwards them. This is what services like Shadow.tech and AWS GameLift Streams do.

**Pros:**
- We "see" Unreal from our cloud VM
- Real GPU rendering
- Could embed in a web UI

**Cons:**
- Still requires a GPU machine somewhere (so this is really Option 2 with extra steps)
- Adds 100–200 ms latency per command
- More complex tunnel/streaming setup

**Verdict:** Useful **layered on top of** Option 2 if we want a web-based viewer for the user, but not a substitute for having a GPU machine.

---

## 3. What I Can Do Right Now From This VM

Even though we can't run UE5 *on* this VM, we can absolutely take meaningful steps from here:

### ✅ Already done / can do today (no upgrade needed)
- Run the **cloud server** (we're already doing this)
- Run the **AI Brain** + **Intelligent Brain** (already running)
- Run the **Cloudflare tunnel** (already running)
- Run the **tunnel manager** (built, ready)
- Serve the knowledge base (151 docs ready)
- Process commands from any UE5 instance that connects in
- Generate, package, and ship the Windows client

### 🔧 Could do with small infrastructure additions
- **Spin up a Vast.ai or RunPod GPU instance on-demand** (Option 2) and have SuperNinja drive it — fully automatable via their APIs
- **Build a Docker image** that contains UE5 headless + our skill executor, ready to deploy to any GPU host
- **Create an "Unreal-less mock"** that simulates the bridge for end-to-end testing without any real Unreal — this would let us test the cloud→companion→bridge pipeline without a Windows machine

### 🚫 Cannot do from this VM
- Open the UE5 editor here
- Render anything visually
- Generate real screenshots from a real scene

---

## 4. My Recommendation

There are really three paths forward, and they're not mutually exclusive:

### **Path A — Test on user's Windows PC (free, fastest)**
Use the package we already built. User runs `START_SUPERNINJA.bat`. Done.
- **Cost:** $0
- **Time:** 15 minutes of user setup
- **Result:** Full system working end-to-end

### **Path B — Rent a cheap GPU VM (cheap, autonomous)**
Spin up a Vast.ai instance with Windows + UE5 pre-installed. Connect our companion to it. Drive it from this cloud VM.
- **Cost:** ~$0.30/hr ($7/day if left on; cents per test session)
- **Time:** 1 hour first-time setup, then on-demand
- **Result:** SuperNinja can drive Unreal *without* needing the user's PC

### **Path C — Build the headless Docker fallback (free, partial)**
Create a Docker image with UE5 headless + our skill executor. Deploy to ANY VM that has at least 60 GB disk and 16 GB RAM (no GPU needed). Most of our 60 skills would still work, just without screenshots.
- **Cost:** $0 (uses existing free-tier VMs from many providers)
- **Time:** 1–2 days of dev work to build the Docker setup
- **Result:** SuperNinja can build scenes blindly, but can't render them. Useful for batch automation.

---

## 5. The Honest Answer to Your Question

> **"Can you open Unreal on your VM or somehow with what we have?"**

- **On THIS specific sandbox:** No. We have 2 cores, 3.8 GB RAM, 3.5 GB free disk, no GPU. UE5 needs at least 16x more disk, 8x more RAM, and a GPU.
- **With what we already built:** Yes — the entire system is *designed* to drive a remote Unreal instance. We just need to point it at one. The cheapest way is the user's own PC; the most autonomous way is a $0.30/hr rented GPU VM.
- **As a fully autonomous solution from this VM alone:** Only via Option 2 (rent + drive a GPU VM via API). I can write the orchestration code that spins up a Vast.ai / RunPod instance, installs UE5, runs our bridge inside it, and connects it back to us — all triggered from this sandbox.

---

## 6. What I'd Build Next If You Say Go

If you want to make SuperNinja truly autonomous (no user PC needed), the natural next phase is:

**Phase 12: Self-Hosted Unreal Runner**

1. Pick a provider (recommend Vast.ai for cost or RunPod for reliability)
2. Build a startup script that:
   - Provisions a GPU VM via their API
   - Installs UE5 (or boots from a pre-built image)
   - Auto-starts our bridge + companion inside it
   - Auto-registers with our cloud server's `/set_tunnel_url`
   - Tears down when idle for cost control
3. Add a `/spin_up_unreal` endpoint to our cloud server
4. SuperNinja can now say "let me boot up a Unreal instance" and 5 minutes later it has one

**Estimated effort:** 2–3 days of focused work. Costs ~$1–2 in test rentals during development.

---

**TL;DR:** This sandbox can't run Unreal — it has no GPU, 3.5 GB disk, and 3.8 GB RAM. But we don't need it to. SuperNinja's whole architecture is designed to drive a *remote* Unreal. The fastest win is the user's own PC (already packaged); the most autonomous win is renting a $0.30/hr GPU VM and driving it via API.
