# SuperNinja Unreal AI — Complete System

> Autonomous AI agent that controls Unreal Editor remotely via cloud-based command architecture.
> Powered by an intelligent brain with UE5 knowledge base and LLM-style reasoning.

**Current release: v5.0.0 (Phase 5, post-Sprint-75).**
See `CHANGELOG.md` for the full 75-task improvement list.

## Quick start

```bash
./setup.sh                # one-time
./start_all.sh            # cloud server + mock unreal
./status.sh               # one-screen health
python3 test_smoke.py     # alive check
make test                 # full test battery (75+ cases)
```

Open `status.html` in a browser for the live dashboard with NL command box.

## Documentation map

| File | What it covers |
|---|---|
| `ARCHITECTURE.md` | Component diagram + data flow |
| `API_REFERENCE.md` | Every HTTP endpoint with examples |
| `SKILLS_CATALOG.md` | Every command the system accepts |
| `RUNBOOK.md` | Daily ops procedures |
| `TROUBLESHOOTING.md` | Symptom → fix table |
| `SECURITY.md` | Threat model + mitigations |
| `CONTRIBUTING.md` | How to add a new skill |
| `SUPERNEJIN_COMPLETE_BLUEPRINT.md` | Long-form project history (Phases 1–11) |
| `UNREAL_ON_VM_RESEARCH.md` | Why UE5 must run on the user's PC |
| `HEADLESS_TEST_RESULTS.md` | Headless validation report |
| `SPRINT_75_TASKS.md` | This sprint's task ledger |

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┬──────────────────┐     ┌──────────────────┐
│  SuperNinja AI   │────>│  Cloud Endpoint   │<────│  Windows       │────>│  Unreal      │
│  (this server)   │     │  (Cloudflare     │     │  Companion     │     │  Python      │
│  sn_ai_brain.py  │     │   tunnel)        │     │  (polls cloud) │     │  Client      │
└──────────────────┘     └──────────────────┘     └──────────────────┬──────────────────┘     └──────────────────┘
                                                          │
                                                          v
                                                ┌──────────────────┐
                                                │  Local Bridge    │
                                                │  127.0.0.1:8765  │
                                                └──────────────────┘
```

**How it works:**
1. SuperNinja cloud enqueues commands (skills) via HTTP
2. Windows companion polls the cloud endpoint outbound (no inbound ports needed)
3. Companion forwards commands to local bridge
4. Bridge routes to Unreal Python client
5. Unreal executes the command and returns results
6. Results (including screenshot images) flow back through the chain to cloud

## Files

| File | Runs Where | Purpose |
|------|-----------|---------|
| `superninja_cloud_command_server.py` | SuperNinja cloud | HTTP endpoint: enqueue, poll, results, screenshots |
| `sn_ai_brain.py` | SuperNinja cloud | AI decision engine — see/think/act/verify loop with intelligent narration |
| `sn_intelligent_brain.py` | SuperNinja cloud | LLM-powered reasoning engine using UE5 knowledge base |
| `sn_skills_registry.py` | Both sides | 64 skills definition (20 categories) |
| `sn_skill_executor.py` | Unreal Editor | Real Unreal Python API implementations for every skill |
| `sn_ue5_knowledge.py` | Both sides | Structured UE5 knowledge from 20 official documents (11 categories) |
| `sn_ue5_knowledge_advanced.py` | Both sides | Advanced UE5 knowledge from Docs 21-60 (14 categories: Lumen, Materials, Rendering, etc.) |
| `sn_ue5_knowledge_expert.py` | Both sides | Expert UE5 knowledge from Docs 61-100 (9 categories: Niagara, Audio, UI, AI, Networking, Optimization, Cinematics, Plugins) |
| `sn_ue5_knowledge_master.py` | Both sides | Master UE5 knowledge from Docs 101-151 (12 categories: Editor Scripting, Virtual Production, Quixel/Landscape, Volumetrics, Rendering, Groom/VT, Performance, Physics, Source Control, API/Pipeline, Production) |
| `sn_knowledge_base.py` | Both sides | Lighting presets, composition rules, scene templates, real-world values |
| `sn_companion_phase2.py` | Windows PC | Polls cloud, forwards to bridge, uploads screenshots |
| `sn_local_bridge_phase2.py` | Windows PC | Local HTTP bridge at 127.0.0.1:8765 |
| `sn_unreal_nonblocking_phase2.py` | Unreal Editor | Non-blocking Python client, executes skills |
| `sn_start_all.bat` | Windows PC | Quick-start batch file |

## Skills (51 total, 17 categories)

### Lighting (5 skills)
- `add_directional_light` — Sun light with intensity, color temp, shadows, angle
- `add_point_light` — Point light with attenuation, source radius
- `add_spot_light` — Spot light with inner/outer cone angles
- `add_sky_light` — Ambient sky illumination
- `adjust_light` — Modify existing light properties

### Placement (7 skills)
- `spawn_actor` — Spawn primitives (Cube, Sphere, Cylinder, etc.)
- `move_actor` — Move actor to new location
- `rotate_actor` — Rotate actor by name
- `scale_actor` — Uniform or non-uniform scale
- `scatter_actors` — Scatter copies of an actor in a region
- `delete_actor` — Delete actor by name (destructive)
- `delete_duplicates` — Clean up duplicate actors (e.g., PHX_ duplicates)

### Analysis (2 skills)
- `list_actors` — List all actors with transforms
- `get_scene_info` — Actor counts by type, lighting summary

### Camera (1 skill)
- `frame_viewport` — Position editor camera to frame a point or actor

### Environment (3 skills)
- `add_exponential_height_fog` — Atmospheric fog with density and falloff
- `add_sky_atmosphere` — Realistic sky rendering
- `add_foliage` — Paint foliage instances (trees, grass, rocks) with density and scale controls

### Material (1 skill)
- `apply_material` — Apply material to actor mesh by slot index

### Asset (2 skills)
- `import_asset` — Import FBX/OBJ/USD into content browser
- `list_content` — List assets in content browser folder

### Utility (3 skills)
- `save_level` — Save current level
- `undo` — Undo last editor action
- `execute_console_command` — Run arbitrary console command

### Conversation (9 skills)
- `chat` — General message with mood (friendly, excited, thinking, concerned, proud, apologetic)
- `say` — Display styled message (info, warning, error, success, thinking)
- `ask_user` — Ask a question with optional multiple-choice answers
- `report_progress` — Report current step/total with status (working, done, failed, waiting)
- `explain_scene` — Auto-analyze and describe the scene in natural language
- `suggest_improvements` — Suggest what could make the scene look better

### Knowledge & Intelligence (8 skills)
- `get_actor_properties` — Get detailed actor info (transform, components, materials, tags)
- `set_actor_property` — Set actor properties (mobility, hidden, tags, layers)
- `find_actors_advanced` — Search actors with multiple filters (class, tag, layer, regex, bounds)
- `query_knowledge` — Search the UE5 knowledge base for best practices and patterns
- `explain_ue5_concept` — Explain UE5 concepts in plain language (GameMode, Blueprints, etc.)
- `suggest_blueprint_pattern` — Get the right Blueprint communication pattern for your use case
- `run_python_snippet` — Execute arbitrary Python code inside Unreal Editor

### Advanced Knowledge (4 skills)
- `query_advanced_knowledge` — Search the advanced Docs 21-60 knowledge base (Lumen, Materials, Rendering, etc.)
- `get_lighting_setup` — Get complete lighting setup recommendation for scene type + mood
- `get_material_recipe` — Get PBR material recipe for surface types (concrete, metal, glass, etc.)
- `analyze_rendering` — Analyze rendering needs (Nanite, TSR, post-process, pipeline recommendations)

### Rendering (1 skill)
- `setup_post_process` — Add Post Process Volume with style presets (cinematic, horror, neon, etc.)

### Expert Knowledge (1 skill)
- `query_expert_knowledge` — Search the expert Docs 61-100 knowledge base (Niagara, Audio, UI, AI, Networking, Optimization, Cinematics, Plugins)

### VFX — Niagara (1 skill)
- `add_niagara_effect` — Add Niagara VFX effects (fire, smoke, water, rain) using Niagara Fluids simulation

### Audio (1 skill)
- `add_audio_ambient` — Add ambient audio using MetaSounds (outdoor, indoor, urban, forest environments)

### AI (2 skills)
- `setup_ai_character` — Set up AI with AIController, Behavior Tree, and Blackboard (basic, patrol, combat patterns)
- `add_navmesh` — Add NavMeshBoundsVolume for AI navigation pathfinding

### Optimization (2 skills)
- `optimize_scene` — Optimize scene for target FPS with Lumen, Nanite, and scalability settings
- `get_fps_optimization_profile` — Get optimization settings and recommendations for target FPS

### Cinematics (1 skill)
- `setup_cinematic` — Set up cinematic sequence using Sequencer with camera tracks

### Networking (1 skill)
- `get_multiplayer_pattern` — Get common networking patterns (replication, RPCs, dedicated servers)

### Master Knowledge (1 skill)
- `query_master_knowledge` — Search the master Docs 101-151 knowledge base (Editor Scripting, Virtual Production, Quixel/Landscape, Volumetrics, Rendering, Groom/VT, Performance, Physics, Source Control, API/Pipeline, Production)

### Environment — Master (4 skills)
- `setup_landscape` — Set up landscape with terrain presets (mountain, plains, desert, coastal) and Quixel Megascans
- `add_volumetric_clouds` — Add volumetric clouds and sky atmosphere for dynamic weather
- `add_height_fog` — Add exponential height fog with volumetric fog support
- `add_water_body` — Add water bodies (ocean, river, lake) with caustics and waves

### Rendering — Master (3 skills)
- `setup_reflections` — Configure reflection methods (indoor, outdoor, water, mirror, architectural)
- `setup_groom_system` — Configure Groom system for realistic hair and fur rendering
- `setup_rvt` — Set up Runtime Virtual Texturing for landscape and large environments

### Virtual Production (1 skill)
- `setup_virtual_production` — Configure ICVFX, Live Link, MetaHuman, USD, or XR virtual production

### Physics — Master (2 skills)
- `setup_physics_constraints` — Add physics constraints (hinge, prismatic, ball_socket, spring)
- `add_chaos_vehicle` — Add Chaos Vehicle with realistic physics simulation

### Pipeline (1 skill)
- `setup_source_control` — Configure Perforce or Git source control integration

These skills make SuperNinja truly intelligent — it understands UE5 architecture, reasons about scenes, and makes informed decisions based on official best practices from 151 official documents.

### Safety Levels
- **SAFE** — Read-only or display-only, no scene changes (list_actors, get_scene_info, list_content, frame_viewport, undo, say, ask_user, chat, report_progress, explain_scene, suggest_improvements, query_knowledge, explain_ue5_concept, suggest_blueprint_pattern, get_actor_properties)
- **MODIFY** — Changes the scene (most spawn/move/rotate/light skills, set_actor_property, run_python_snippet)
- **DESTRUCTIVE** — Cannot be undone remotely (delete_actor, delete_duplicates)

## Knowledge Base

SuperNinja doesn't just send commands — it truly understands UE5. The intelligent brain uses a structured knowledge base extracted from 151 official UE5 documents, covering 46 knowledge categories across four tiers:

### UE5 Core Knowledge (Docs 1-20, 11 categories)
| Category | Contents |
|----------|----------|
| `class_hierarchy` | UObject → AActor → APawn → ACharacter, component types |
| `gameplay_framework` | GameInstance, GameMode, GameState, PlayerState, player lifecycle |
| `naming_conventions` | A-Actor, U-UObject, F-Struct, E-Enum, I-Interface prefixes |
| `editor_interface` | Viewport modes, content browser, details panel, world outliner |
| `blueprint_system` | Types, communication patterns, variables, events, debugging |
| `cpp_interop` | UCLASS, UPROPERTY, UFUNCTION macros, compilation, hot reload |
| `directory_structure` | /Content, /Source, /Plugins, .uproject, config files |
| `source_control` | SVN, Git, Perforce integration, revision control workflow |
| `slate_ui` | Widget construction, UMG, binding, responsive design |
| `python_patterns` | unreal module API, editor scripting, automation |
| `key_concepts` | Levels, sublevels, data layers, PAK files, references |

### UE5 Advanced Knowledge (Docs 21-60, 14 categories)
| Category | Contents |
|----------|----------|
| `gameplay_ability_system` | GAS framework, abilities, attributes, effects, Lyra starter game |
| `lighting` | Light types, mobility, intensity units, color temperature, best practices |
| `lumen` | Global illumination, surface cache, screen traces, performance tuning |
| `shadows` | Virtual Shadow Maps, cascaded shadows, contact shadows, ray-traced shadows |
| `exposure` | Auto exposure, eye adaptation, EV100, metering modes |
| `lightmass` | Baked lighting, lightmap UVs, build settings, GI quality |
| `materials` | PBR properties, instances, layers, subsurface scattering, shading models |
| `rendering` | Post-process, color grading, Nanite, TSR, virtual texturing, forward/deferred |
| `level_design` | PCG, foliage, modeling mode, World Partition, Data Layers |
| `animation` | Skeletal mesh, AnimBP, Control Rig, IK, motion warping |
| `physics` | Collision, Chaos physics, destruction, cloth simulation |
| `niagara` | VFX system, emitters, renderers, common effect recipes |
| `performance` | Lighting/material/rendering performance guidelines, target FPS |
| `scene_workflow` | Lighting workflow order, material workflow, common mistakes |

### UE5 Expert Knowledge (Docs 61-100, 9 categories)
| Category | Contents |
|----------|----------|
| `niagara_advanced` | Niagara Fluids (2D/3D gas/liquid simulation), custom modules, data channels, simulation stages |
| `audio` | MetaSounds, Sound Cues, spatial audio, attenuation, sound classes, concurrency |
| `ui` | UMG, Widget Blueprints, Common UI, Slate, Widget Components, responsive design |
| `ai_system` | Behavior Trees, EQS, Navigation Mesh, AI Perception, State Tree, Smart Objects |
| `networking` | Replication, RPCs, dedicated servers, online subsystem, session management, network drivers |
| `optimization` | Lumen performance, Unreal Insights, Nanite technical details, Virtual Texturing, scalability groups |
| `packaging` | Build tool, target settings, DLC/patching, Pak files, encryption, compression |
| `cinematics` | Sequencer, Movie Render Queue, Take Recorder, camera animation, render passes |
| `plugins` | Content Examples, Valley of the Ancient, plugin structure, module loading |

### UE5 Master Knowledge (Docs 101-151, 12 categories)
| Category | Contents |
|----------|----------|
| `editor_scripting` | Editor Utility Widgets, Python scripting, batch operations, editor utilities, automation |
| `virtual_production` | MetaHuman, Live Link, ICVFX, nDisplay, green screen compositing, light cards, LED volumes |
| `quixel_landscape` | Quixel Bridge, Megascans, Landscape tool, terrain sculpting, Water system, biomes |
| `volumetrics` | Volumetric Clouds, Sky Atmosphere, Exponential Height Fog, atmospheric scattering, god rays |
| `rendering_master` | Mesh Painting, Decals, Light Functions, Reflections (SSR/SSAO), Distance Fields, Planar Reflections |
| `groom_vt` | Groom system (hair/fur), card/mesh/strand rendering, Runtime Virtual Texturing, VT landscapes |
| `performance_tools` | HLOD, Replication Graph, Network Profiler, Stat commands, Session Frontend |
| `content_creation` | Console commands, shader development, texture optimization, material layers |
| `physics_advanced` | Physics Constraints, Chaos Vehicles, suspension, engine simulation, damage system |
| `source_control` | Perforce, Git LFS, console SDKs, certification, platform-specific development |
| `api_pipeline` | C++ API, UE 5.4 features, asset pipeline, Datasmith, FBX/USD import |
| `production` | Editor extensibility, profiling, localization, crash reporting, analytics, release pipeline |

### Intelligent Reasoning
The `IntelligentBrain` class provides knowledge-aware analysis:
- **Lighting Design** — Understands why a single directional light creates harsh contrast; suggests fill lights and sky lights based on UE5 best practices
- **Composition** — Applies rule of thirds, depth layering, and camera height rules with reasoning
- **Performance** — Detects too many dynamic lights, missing lightmobility settings, Nanite/Lumen warnings
- **Scene Hygiene** — Finds duplicate actors, bad naming, unused actors, and suggests cleanup
- **Niagara VFX** — Detects fire, smoke, water elements and recommends Niagara Fluids simulations (2D/3D gas/liquid)
- **Audio** — Recommends MetaSounds for ambient audio, spatial sound with attenuation, room tone for enclosed spaces
- **AI Systems** — Checks for characters without AI controllers, missing NavMesh, recommends Behavior Tree patterns
- **Networking** — Detects multiplayer goals and recommends replication setup, RPCs, and server architecture
- **Optimization** — Deep Lumen performance analysis, Nanite verification, scalability group recommendations per FPS target
- **Cinematics** — Recommends Sequencer workflow, CineCameraActor for film shots, Movie Render Queue for final output
- **Editor Scripting** — Detects repetitive tasks and recommends Editor Utility Widgets or Python scripting for automation
- **Virtual Production** — Checks for ICVFX, Live Link, MetaHuman requirements and recommends VP camera and compositing setup
- **Landscape** — Analyzes terrain needs and recommends Quixel Megascans, landscape presets (mountain/plains/desert/coastal), and water bodies
- **Volumetrics** — Checks for clouds, sky atmosphere, fog, and recommends volumetric effects for atmospheric depth
- **Advanced Rendering** — Analyzes reflection needs, recommends SSR/SSAO, Planar Reflections, Distance Fields, Decals, and Light Functions
- **Groom/VT** — Detects hair/fur requirements and recommends Groom system; checks for large texture sets that benefit from Runtime Virtual Texturing
- **Performance Tools** — Recommends HLOD for high mesh counts, Replication Graph for multiplayer, profiling tools for optimization
- **Physics Advanced** — Checks for physics constraint needs and recommends Chaos Vehicles for vehicle simulation

### Lighting Presets
| Preset | Description | Key Values |
|--------|------------|------------|
| `golden_hour` | Warm low-angle sunlight | 3500K, intensity 3.5, long shadows |
| `midday_sun` | Harsh overhead sunlight | 6500K, intensity 10.0, short shadows |
| `overcast` | Soft diffused sky | 7500K, intensity 1.5, no shadows |
| `blue_hour` | Cool twilight ambient | 9000K, intensity 0.8, subtle fog |
| `film_noir` | High-contrast dramatic | 3200K, intensity 8.0, hard shadows |
| `neon_city` | Colorful urban night | Mixed temps, multi-colored point lights |
| `studio_3point` | Professional 3-point setup | Key + fill + rim, controlled ratios |
| `horror` | Eerie unsettling atmosphere | 2500K, intensity 0.5, deep shadows |
| `interior_office` | Fluorescent office lighting | 4000K, intensity 1.2, even coverage |

### Composition Rules
- **Rule of Thirds** — Place key subjects at grid intersection points
- **Depth Layers** — Foreground, midground, background separation
- **Camera Heights** — Eye (170cm), Low (50cm), High (300cm), Bird (1000cm)
- **Framing Techniques** — Natural framing, leading lines, negative space

### Scene Templates
- `empty_outdoor` — Clean outdoor scene with sky and sun
- `dark_alley` — Film noir alley with fog and spot lights
- `showroom` — Product showcase with 3-point lighting
- `neon_street` — Cyberpunk street with neon accents and fog

## Quick Start

### On SuperNinja Cloud

```bash
# 1. Start the command server
python superninja_cloud_command_server.py

# 2. Start Cloudflare tunnel (or use expose-port)
cloudflared tunnel --url http://127.0.0.1:8791

# 3. Note the tunnel URL (e.g., https://something.trycloudflare.com)
```

### On Windows PC

```bash
# 1. Install requests
pip install requests

# 2. Update the CLOUD_URL in sn_companion_phase2.py to your tunnel URL

# 3. Start the local bridge
python sn_local_bridge_phase2.py

# 4. Start the companion
python sn_companion_phase2.py

# 5. In Unreal Editor (Output Log > Python mode), run:
exec(open(r"C:\Users\sbcam\OneDrive\Desktop\sn_unreal_nonblocking_phase2.py", "r", encoding="utf-8-sig").read())
```

### Or use the batch file:
```cmd
sn_start_all.bat
```

## Using the AI Brain

```python
from sn_ai_brain import SuperNinjaBrain

brain = SuperNinjaBrain("https://your-tunnel.trycloudflare.com")

# See the scene
brain.analyze_scene()
brain.take_screenshot()

# Light the scene with a preset
brain.light_scene("cinematic")   # cinematic, studio, outdoor, moody, interior

# Place objects
brain.spawn_shape("Cube", location=[0, 0, 100], name="MyCube")

# Clean up duplicates
brain.cleanup_duplicates(prefix="PHX_", dry_run=True)

# Talk to the user
brain.chat("Hey! I'm going to improve the lighting in your scene.", "excited")
brain.report_progress("Adding key light...", step=1, total=3)

# Query UE5 knowledge
brain.query_knowledge("how does GameMode work")
brain.explain_ue5_concept("Blueprint Interfaces")
brain.suggest_blueprint_pattern("I need two actors to talk to each other without direct reference")

# Advanced knowledge (Docs 21-60)
brain.query_advanced("lumen performance")
brain.get_lighting_setup("outdoor_golden_hour", mood="cinematic")
brain.get_surface_recipe("concrete")
brain.advanced_analysis(goal="cinematic outdoor scene")

# Expert knowledge (Docs 61-100)
brain.query_expert("niagara fluids fire simulation")
brain.get_fps_profile(target_fps=60)
brain.get_multiplayer_pattern("replication")
brain.expert_analysis(goal="multiplayer game with AI enemies")
brain.analyze_vfx_needs()
brain.analyze_audio_needs()
brain.analyze_ai_needs()
brain.analyze_optimization()

# Master knowledge (Docs 101-151)
brain.query_master("volumetric clouds")
brain.analyze_virtual_production()
brain.analyze_landscape()
brain.analyze_volumetrics()
brain.analyze_rendering_master()
brain.analyze_performance_tools()
brain.get_landscape_preset("mountain")
brain.get_reflection_recommendation("indoor")

# Full autonomous cycle (with intelligent reasoning)
brain.see_think_act(goal="Make the scene look like a film noir alley")
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/status` | Queue stats, allowed commands |
| GET | `/poll` | Companion picks up next command |
| GET | `/result?id=XXX` | Get command result |
| GET | `/screenshot` | List available screenshots |
| GET | `/screenshot?id=XXX` | Get screenshot metadata + base64 |
| GET | `/screenshot_image?id=XXX` | Get raw PNG image |
| POST | `/enqueue` | Enqueue a command |
| POST | `/result` | Post a result back |
| POST | `/upload_screenshot` | Upload screenshot image data |

## Current Status

- **Phase 1** ✅ Complete — Full command round-trip
- **Phase 2** ✅ Complete — Screenshot capability
- **Phase 3** ✅ Complete — 29 skills + AI brain with knowledge base
- **Phase 4** ✅ Complete — Skill executor, conversational narration, real Unreal API code
- **Phase 5** ✅ Complete — Documentation & cleanup
- **Phase 6** ✅ Complete — Intelligent brain with UE5 knowledge base (39 skills, 10 categories)
- **Phase 8** ✅ Complete — Advanced knowledge from Docs 21-60 (42 skills, 11 categories, 25 knowledge categories)
- **Phase 9** ✅ Complete — Expert knowledge from Docs 61-100 (51 skills, 17 categories, 34 knowledge categories)
- **Phase 10** ✅ Complete — Master knowledge from Docs 101-151 (64 skills, 20 categories, 46 knowledge categories)
- **Next**: Run end-to-end with real Unreal Editor, add LLM-powered scene understanding

## Cloud Endpoint (Live)

```
https://rated-heart-experience-super.trycloudflare.com
```

> Note: Cloudflare quick tunnel URLs are ephemeral — they change on each restart.