"""
SuperNinja UE5 Expert Knowledge Base
======================================
Structured knowledge extracted from UE5 Training Corpus Documents 61-100.
Covers: Niagara Advanced, Audio, UI, AI, Networking, Optimization,
        Packaging, Cinematics, and Plugins.

This module provides the expert-level domain knowledge that powers SuperNinja's
advanced reasoning for production-quality UE5 work.
"""

# ============================================================================
# NIAGARA ADVANCED (Docs 61-65)
# ============================================================================

NIAGARA_ADVANCED = {
    "fluids": {
        "description": "Plugin for 2D and 3D fluid simulations using Niagara",
        "features": [
            "2D and 3D Gas Simulations — fire, smoke, heat haze",
            "2D and 3D Liquid Simulations — water, splashes, flowing liquids",
            "Real-time Simulation — during gameplay or cinematic playback",
            "GPU-based Computation — high performance on GPU",
            "Collision Support — collide with static geometry",
            "Lighting Integration — interact with scene lighting",
        ],
        "setup": [
            "Enable NiagaraFluids plugin in Edit > Plugins",
            "Restart the editor",
            "Create new Niagara System using Niagara Fluids template",
        ],
        "simulation_types": {
            "2D Gas (Grid2D)": "Fire, smoke, heat haze on a 2D plane",
            "3D Gas (Grid3D)": "Volumetric smoke, explosions, atmospheric effects",
            "2D Liquid": "Water surfaces, splashes, flowing liquids (planar)",
            "3D Liquid": "Pouring water, splashing, volumetric liquid interactions",
        },
        "important_notes": [
            "Must run in Play in Editor (PIE) mode to see dynamics",
            "Keep GPU drivers updated for best performance",
            "Quality vs performance adjustable via simulation resolution",
        ],
    },
    "editor_reference": {
        "system_editor": {
            "toolbar": "Compile, save, undo/redo, playback controls",
            "viewport": "Real-time preview of particle effect",
            "timeline": "Simulation timing and looping behavior",
            "system_overview": "Hierarchy of emitters in the system",
            "emitter_panel": "Modules and settings for selected emitter",
            "parameters_panel": "All parameters available in the system",
            "scratch_pad": "Prototyping area for custom modules",
        },
        "script_editor": "Node-based interface for custom GPU/CPU simulation logic",
        "module_categories": [
            "Emitter Spawn — control when/how particles spawn",
            "Emitter Update — per-frame emitter logic",
            "Particle Spawn — per-particle initialization",
            "Particle Update — per-frame particle logic",
            "Render — how particles are drawn (sprites, meshes, ribbons)",
            "Event — send/receive events between emitters",
        ],
    },
    "creating_vfx": {
        "workflow": [
            "1. Create Niagara System (Content Browser > FX > Niagara System)",
            "2. Choose template (Fountain, Fire, Smoke, etc.)",
            "3. Add/modify emitters and modules",
            "4. Adjust parameters (spawn rate, lifetime, size, color)",
            "5. Add renderers (Sprite, Mesh, Ribbon, Light)",
            "6. Test in viewport and in-level",
        ],
        "key_concepts": {
            "system": "Top-level asset containing one or more Emitters",
            "emitter": "Individual particle source with spawn/update/render stages",
            "module": "Reusable function that modifies particle behavior",
            "parameter": "Named value that can be overridden per-instance",
            "stage": "Execution phase (Spawn, Update, Render, Event)",
        },
    },
    "custom_modules": {
        "description": "Create custom Niagara modules for reusable VFX logic",
        "languages": {
            "niagara_script": "Node-based visual scripting in Niagara Editor",
            "hlsl": "Custom HLSL for GPU simulation modules",
        },
        "use_cases": [
            "Custom force fields and attractors",
            "Complex particle behaviors not possible with built-in modules",
            "Optimized GPU compute for large particle counts",
            "Data-driven effects using Niagara Parameters",
        ],
    },
    "data_channels": {
        "description": "Share data between Niagara systems and external systems",
        "types": {
            "point_array": "Share point data (position, velocity, color) between systems",
            "mesh_surface": "Sample mesh surface data for particle placement",
            "texture": "Read/write texture data in Niagara simulations",
        },
        "use_cases": [
            "Couple fluid simulations with particle effects",
            "Drive Niagara from gameplay data",
            "Create GPU-computed data for other systems to consume",
        ],
    },
}

# ============================================================================
# AUDIO (Docs 66-70)
# ============================================================================

AUDIO_SYSTEM = {
    "overview": {
        "description": "UE5 audio system built on MetaSound architecture",
        "key_components": ["MetaSounds", "Sound Cues", "Audio Volumes", "Spatial Audio", "Sound Attenuation"],
    },
    "metasounds": {
        "description": "Next-generation audio system replacing Sound Cues for new projects",
        "features": [
            "Node-based graph interface for audio programming",
            "Full programmability — create any audio behavior",
            "Real-time parameter control from Blueprints/C++",
            "Generator nodes for procedural audio synthesis",
            "Wave Player nodes for sample playback",
            "Mixing, effects, and routing all in the graph",
        ],
        "vs_sound_cues": "MetaSounds are more powerful and flexible, but Sound Cues still supported for backward compatibility",
        "use_cases": [
            "Dynamic music that responds to gameplay",
            "Procedural sound generation (engines, wind, footsteps)",
            "Complex audio routing and mixing",
            "Real-time audio parameter control",
        ],
    },
    "sound_cues": {
        "description": "Legacy node-based audio asset system",
        "node_types": {
            "Wave Player": "Play a .wav sound file",
            "Mixer": "Mix multiple sounds together",
            "Random": "Randomly select from multiple sounds",
            "Concatenator": "Play sounds in sequence",
            "Attenuation": "Apply distance-based volume falloff",
            "Modulator": "Pitch/volume modulation",
            "Oscillator": "Generate simple waveforms",
            "Delay": "Add delay effect",
        },
    },
    "spatial_audio": {
        "description": "Position audio in 3D space for immersive soundscapes",
        "features": {
            "spatialization": "3D positioning using HRTF or panning",
            "attenuation": "Volume falloff with distance",
            "occlusion": "Sound blocked by geometry",
            "reverb": "Environment-based echo and reverb zones",
            "air_absorption": "Frequency-dependent distance filtering",
        },
        "settings": {
            "spatialization_method": "Panning (simple) or HRTF (headphone 3D)",
            "distance_algorithm": "Linear, Inverse, Logarithmic attenuation curves",
            "occlusion_method": "Raycast-based or geometry-based occlusion",
        },
    },
    "sound_attenuation": {
        "description": "Controls how sound fades with distance",
        "key_settings": {
            "attenuation_shape": "Sphere, Box, Capsule, Cone shape for falloff",
            "inner_radius": "Distance within which sound is at full volume",
            "falloff_distance": "Distance over which sound fades to zero",
            "attenuation_method": "Linear, Logarithmic, Inverse, Custom curve",
            "spatialization": "Enable 3D positioning",
            "occlusion": "Enable geometry-based sound blocking",
            "reverb": "Apply reverb send when attenuated",
            "air_absorption": "Low-pass filter at distance for realism",
        },
        "presets": {
            "close_range": "Inner radius=100, falloff=800, for footsteps/UI sounds",
            "mid_range": "Inner radius=300, falloff=3000, for dialogue/weapon sounds",
            "long_range": "Inner radius=500, falloff=10000, for explosions/ambience",
            "music": "No attenuation, 2D spatialization for music tracks",
        },
    },
}

# ============================================================================
# UI (Docs 71-75)
# ============================================================================

UI_SYSTEM = {
    "umg_quick_start": {
        "description": "Unreal Motion Graphics (UMG) is the visual UI authoring tool",
        "workflow": [
            "1. Create Widget Blueprint (Content Browser > UI > Widget Blueprint)",
            "2. Design layout in the Designer tab (drag-and-drop widgets)",
            "3. Add logic in the Graph tab (Blueprint scripting)",
            "4. Create Widget in player Blueprint and Add to Viewport",
        ],
        "key_widgets": {
            "Canvas Panel": "Absolute positioning layout",
            "Horizontal Box": "Arrange children horizontally",
            "Vertical Box": "Arrange children vertically",
            "Grid Panel": "Grid-based layout",
            "Uniform Grid Panel": "Equal-size cells grid",
            "Overlay": "Stack widgets on top of each other",
            "Scale Box": "Scale content to fit",
            "Size Box": "Constrain content size",
            "Button": "Clickable button with text/icon",
            "Text Block": "Display text",
            "Image": "Display texture/material",
            "Progress Bar": "Fill bar for health/progress",
            "Slider": "Draggable value selector",
            "Editable Text": "Text input field",
        },
    },
    "widget_blueprints": {
        "description": "Blueprint class for creating UI screens and HUD elements",
        "components": {
            "designer_tab": "Visual layout editor with drag-and-drop",
            "graph_tab": "Blueprint scripting for widget behavior",
            "bindings": "Bind widget properties to variables/functions",
            "animations": "Widget animations (fade, slide, scale)",
            "events": "OnClicked, OnHovered, OnPressed, etc.",
        },
        "best_practices": [
            "Use anchors for responsive layout across screen sizes",
            "Use Size Boxes to constrain widget dimensions",
            "Use Validated properties for user input",
            "Cache widget references instead of repeated Get calls",
            "Use Data Binding instead of manual updates",
        ],
    },
    "common_ui": {
        "description": "Plugin for building UI that works across platforms (PC, Console, Mobile)",
        "features": [
            "CommonButton — Styled button with input-action binding",
            "CommonBorder — Styled container with focus visualization",
            "CommonText — Localized text with platform-specific styling",
            "Template/UserWidget Architecture for reusable UI patterns",
            "Game-specific UI tag system for navigation",
        ],
        "use_cases": "Any multi-platform project where UI must work with keyboard, mouse, gamepad, and touch",
    },
    "slate": {
        "description": "Low-level C++ UI framework (what UMG is built on top of)",
        "when_to_use": [
            "Editor tools and custom panels",
            "Performance-critical HUD elements",
            "Custom widget types for UMG",
            "In-game UI that needs maximum performance",
        ],
        "vs_umg": "Slate = C++ code, fast, complex. UMG = Visual designer, slower, easier.",
        "key_concepts": {
            "SWidget": "Base class for all Slate widgets",
            "SCompoundWidget": "Widget composed of other widgets",
            "SLeafWidget": "Widget with no children (image, text)",
            "Slot": "Layout properties of a child in its parent",
            "Attribute": "Bindable property that can auto-update",
            "DECLARE_SLATE_WIDGET": "Macro to declare a new Slate widget",
        },
    },
    "widget_components": {
        "description": "3D in-world UI using Widget Components",
        "use_cases": [
            "Interactive screens and monitors in the world",
            "Billboards and signs with dynamic text",
            "VR interaction panels",
            "Health bars floating above characters",
        ],
        "settings": {
            "Draw Size": "Resolution of the widget texture",
            "Pivot": "Anchor point for positioning",
            "Tick Mode": "When the widget updates (Always, When Visible, Never)",
            "Space": "World (3D) or Screen (always faces camera)",
        },
    },
}

# ============================================================================
# AI SYSTEM (Docs 76-80)
# ============================================================================

AI_SYSTEM = {
    "behavior_trees": {
        "description": "Tree-based decision system for AI agent behavior",
        "components": {
            "BTAsset": "Behavior Tree asset defining the decision tree",
            "Blackboard": "Key-value store shared between BT nodes",
            "BTTask": "Leaf node that performs an action (move to, wait, custom)",
            "BTComposite": "Group node (Selector: try children until one succeeds; Sequence: try all children in order)",
            "BTDecorator": "Conditional check that allows/blocks node execution",
            "BTService": "Background task that runs while its parent node is active",
        },
        "patterns": {
            "patrol": "Sequence: MoveTo(PatrolPoint1) - Wait - MoveTo(PatrolPoint2) - Wait - Loop",
            "chase_player": "Selector: Decorator(CanSeePlayer) - Sequence: MoveTo(Player) - Attack",
            "idle_alert": "Sequence: Wait(Random 2-5s) - Rotate - Service: UpdatePerception",
        },
        "tips": [
            "Use Blackboard for all shared state between nodes",
            "Keep trees shallow — deep nesting is hard to debug",
            "Use Decorators for conditions, not Tasks that return failure",
            "Services are great for periodic perception/environment checks",
        ],
    },
    "eqs": {
        "description": "Environment Query System — find best location/item for AI decisions",
        "how_it_works": "Generate candidate points, score them with tests, return best option",
        "query_components": {
            "generators": "Create candidate points (Grid, PointsAroundCircle, ActorOfClass)",
            "tests": "Score candidates (Distance, Trace, Pathfinding, Dot, ItemType)",
            "context": "Reference point for tests (Querier, EnvQueryContext_Blueprint)",
        },
        "use_cases": [
            "Find best cover position near AI agent",
            "Find nearest health pickup",
            "Find optimal sniping position",
            "Find valid patrol point with line of sight to player",
        ],
    },
    "navigation": {
        "description": "NavMesh-based pathfinding system",
        "components": {
            "NavMeshBoundsVolume": "Defines area where NavMesh is generated",
            "RecastNavMesh": "Navigation mesh data asset with settings",
            "NavLinkProxy": "Custom navigation link (jump, drop, ladder)",
            "NavModifier": "Modify navigation area properties (cost, area class)",
        },
        "settings": {
            "cell_size": "Resolution of NavMesh grid (smaller = more precise but more memory)",
            "cell_height": "Height resolution of NavMesh",
            "agent_radius": "Navigation agent size",
            "agent_height": "Navigation agent height",
        },
        "tips": [
            "Build NavMesh with 'Build Navigation' or it auto-builds on save",
            "Use NavLinkProxies for jumps, drops, ladders, and custom traversal",
            "NavModifiers change area cost — water might be expensive to path through",
            "Use Runtime Generation: Dynamic for moving obstacles",
        ],
    },
    "ai_perception": {
        "description": "Sensory system for AI agents (sight, hearing, damage, touch)",
        "senses": {
            "AISense_Sight": "See actors in vision cone (angle, range, lose sight delay)",
            "AISense_Hearing": "Hear noise events from NoiseEmitter component",
            "AISense_Damage": "React to damage events",
            "AISense_Touch": "React to physical contact",
            "AISense_Prediction": "Predict where a moving target will be",
            "AISense_Team": "Detect friend/foe team members",
        },
        "setup": [
            "Add AIPerceptionComponent to AI Controller",
            "Configure senses (sight config, hearing config, etc.)",
            "Handle OnTargetPerceptionUpdated in Blueprint/C++",
            "Add AIPerceptionStimuliSource to actors AI should perceive",
        ],
    },
    "state_tree": {
        "description": "Hierarchical state machine replacing Behavior Trees for complex AI",
        "advantages": [
            "More flexible than Behavior Trees for complex state transitions",
            "Supports transition conditions on any state",
            "Built-in tree hierarchy for state composition",
            "Better performance for large state spaces",
        ],
        "vs_behavior_trees": "State Trees are better for complex state logic; BTs are better for action selection",
        "components": {
            "state": "Node with enter/exit/transition logic",
            "task": "Action performed within a state",
            "transition": "Condition that moves between states",
            "evaluator": "Compute values used by transitions",
        },
    },
}

# ============================================================================
# NETWORKING (Docs 81-85)
# ============================================================================

NETWORKING_SYSTEM = {
    "overview": {
        "description": "UE5 multiplayer built on client-server architecture with server authority",
        "architecture": "Server is authoritative — clients send inputs, server validates and replicates state",
        "key_concepts": {
            "server": "Authoritative session host that validates all gameplay",
            "client": "Connects to server, sends inputs, receives replicated state",
            "listen_server": "Server that also acts as a client (host-player model)",
            "dedicated_server": "Headless server with no local player",
        },
    },
    "replication": {
        "description": "Automatic synchronization of Actor state from server to clients",
        "replicated_properties": {
            "Replicated": "Server pushes value to all clients",
            "ReplicatedUsing": "Server pushes value, client runs OnRep function on change",
            "NotReplicated": "Local only, not synchronized",
        },
        "rpcs": {
            "Server RPC": "Client calls, server executes (client requests action)",
            "Client RPC": "Server calls, specific client executes (server tells client to do something)",
            "NetMulticast": "Server calls, ALL clients execute (e.g., explosion effects)",
        },
        "replication_rules": [
            "Only server can modify replicated properties",
            "Clients must use Server RPCs to request changes",
            "OnRep functions handle client-side reactions to replicated changes",
            "Multicast RPCs are for cosmetic effects only (spawns, particles, sounds)",
        ],
    },
    "performance_tips": {
        "bandwidth": [
            "Use ReplicatedUsing instead of polling for property changes",
            "Mark only essential properties as Replicated",
            "Use NetUpdateFrequency to control replication rate",
            "Use Conditional Replication (only replicate when relevant to client)",
            "Use RepNotify instead of polling in Tick",
        ],
        "optimization": [
            "Use NetConnection MaxPacketSize wisely",
            "Limit RPC frequency (don't call every frame)",
            "Use relevancy checking to avoid replicating distant actors",
            "Compress large data structures before replication",
            "Profile with 'stat net' and Network Emulator",
        ],
    },
    "dedicated_servers": {
        "description": "Headless server build for production multiplayer",
        "setup": [
            "Build target as Server configuration",
            "Use Unreal Build Tool with -server flag",
            "Configure DefaultEngine.ini for server settings",
            "Set up matchmaking and session management via Online Subsystem",
        ],
    },
    "online_subsystem": {
        "description": "Abstraction layer for platform-specific online services",
        "interfaces": {
            "Session": "Matchmaking, creating/joining game sessions",
            "Leaderboards": "Score tracking and ranking",
            "Achievements": "Unlocking achievements/trophies",
            "Voice": "Voice chat integration",
            "Friends": "Friends list and presence",
        },
        "platforms": {
            "Null": "No online services (local/LAN play)",
            "EOS": "Epic Online Services (cross-platform)",
            "Steam": "Steamworks integration",
            "PS/Xbox/Nintendo": "Console-specific SDKs",
        },
    },
}

# ============================================================================
# OPTIMIZATION (Docs 86-90)
# ============================================================================

OPTIMIZATION_SYSTEM = {
    "lumen_performance": {
        "description": "Performance tuning for Lumen GI and reflections",
        "key_settings": {
            "lumen_quality": "Quality level directly impacts performance; Medium is good balance",
            "software_lumen": "Faster on most hardware, use unless HW RT quality needed",
            "hardware_lumen": "Higher quality reflections, requires RT cores (RTX/RX)",
            "surface_cache_resolution": "Lower = faster but less accurate indirect light",
            "max_trace_distance": "Reduce for indoor/enclosed scenes to save performance",
            "final_gather_quality": "Controls indirect lighting quality vs cost",
        },
        "console_vars": {
            "r.Lumen.ScreenProbeGather.TracingOctahedronResolution": "Lower for faster probes (default 8)",
            "r.Lumen.ScreenSpaceBentNormal": "Enable for better AO (small cost)",
            "r.Lumen.DiffuseIndirect.Allow": "Disable Lumen GI entirely for testing",
            "r.Lumen.Reflections.ScreenSpaceReconstruction": "Enable for better reflections",
            "r.Lumen.ScreenProbeGather.DownsampleFactor": "Higher = faster but less detail",
        },
        "target_fps": {
            "30fps_cinematic": "Lumen Epic, HW RT reflections, full GI quality",
            "60fps_balanced": "Lumen Medium-High, Software Lumen, reduced trace distance",
            "120fps_competitive": "Lumen Low or disabled, baked lighting preferred",
        },
    },
    "unreal_insights": {
        "description": "UE5's profiling and performance analysis tool",
        "features": [
            "CPU timing traces — see exactly where frame time is spent",
            "GPU timing — render pass breakdown",
            "Loading insights — asset loading and streaming analysis",
            "Memory insights — allocation tracking and leaks",
            "Network insights — replication and bandwidth analysis",
        ],
        "how_to_use": [
            "1. Launch Unreal Insights from Engine/Binaries or Window > Developer Tools",
            "2. Start a Trace session (or use -trace= command line)",
            "3. Play the game/session to capture data",
            "4. Stop trace and analyze in Insights window",
        ],
        "key_counters": [
            "stat unit — overall frame breakdown (Game, Draw, RHI, GPU)",
            "stat GPU — detailed GPU timing",
            "stat SceneRendering — draw calls and primitive counts",
            "stat Streaming — texture/streaming info",
            "stat Net — network performance",
        ],
    },
    "nanite_technical": {
        "description": "Deep technical details of Nanite virtualized geometry",
        "how_it_works": {
            "cluster_generation": "Mesh is split into small clusters (~128 triangles)",
            "lod_selection": "Cluster LODs selected based on screen-space error",
            "visibility_buffer": "Renders cluster ID + triangle ID to visibility buffer",
            "material_pass": "Deferred material shading using visibility buffer data",
            "streaming": "Cluster data streamed based on camera distance",
            "culling": "Frustum, occlusion, and small-feature culling per cluster",
        },
        "limitations": [
            "No Skeletal Mesh support (as of 5.4)",
            "Limited masked/translucent material support",
            "No hardware tessellation (use material displacement instead)",
            "Not compatible with all mesh modifiers",
            "World Position Offset has special handling requirements",
        ],
        "performance_tips": [
            "Enable Nanite on ALL eligible static meshes for maximum benefit",
            "Use Nanite Visualization to identify expensive meshes",
            "Fallback meshes needed for translucent/masked materials",
            "Reduce Nanite MaxPixelsPerEdge for performance at slight quality cost",
            "Monitor with stat Nanite for cluster counts and rendering stats",
        ],
    },
    "virtual_texturing_advanced": {
        "description": "Advanced virtual texturing for large textures",
        "benefits": [
            "Consistent memory usage regardless of texture resolution",
            "Only loads visible tiles at needed resolution",
            "Supports textures of virtually any size",
            "Reduces texture streaming stalls",
        ],
        "setup_steps": [
            "1. Right-click texture > Convert to Virtual Texture",
            "2. In Material, change texture sample to Virtual Texture Sample",
            "3. Configure VT pool size in Project Settings",
            "4. Monitor with stat VirtualTexture and stat VirtualTextureMemory",
        ],
    },
    "scalability": {
        "description": "Engine scalability settings for quality/performance tradeoffs",
        "groups": {
            "Resolution Quality": "Screen resolution scale (50-100%)",
            "View Distance": "Far LOD draw distance",
            "Anti-Aliasing": "MSAA/TAA quality level",
            "Shadow Quality": "Shadow map resolution, cascade count",
            "Post Process Quality": "Bloom, DoF, motion blur quality",
            "Texture Quality": "Max texture LOD level",
            "Visual Effects Quality": "Particle, Niagara quality",
            "Foliage Quality": "Foliage density and draw distance",
            "Shading Quality": "Material quality, subsurface, SSR",
            "Global Illumination": "Lumen quality level",
            "Reflections": "Lumen reflection quality",
        },
        "console_commands": {
            "scalability low": "sg.ShadowQuality 0, sg.TextureQuality 0, etc.",
            "scalability medium": "sg.ShadowQuality 1, sg.TextureQuality 1, etc.",
            "scalability high": "sg.ShadowQuality 2, sg.TextureQuality 2, etc.",
            "scalability epic": "sg.ShadowQuality 3, sg.TextureQuality 3, etc.",
            "scalability cinematic": "sg.ShadowQuality 4, sg.TextureQuality 4, etc.",
        },
    },
}

# ============================================================================
# PACKAGING (Docs 91-94)
# ============================================================================

PACKAGING_SYSTEM = {
    "overview": {
        "description": "Build and package your UE5 project for distribution",
        "platforms": ["Windows", "Mac", "Linux", "iOS", "Android", "Console (with SDK)"],
    },
    "packaging_workflow": [
        "1. Set Default Map in Project Settings > Maps and Modes",
        "2. Configure packaging settings (compression, optimization)",
        "3. Select target platform in Platforms menu",
        "4. Build > Package Project or use command line",
        "5. Test the packaged build thoroughly",
    ],
    "settings": {
        "use_pak_file": "Package assets into .pak files (recommended for distribution)",
        "create_compressed_pak": "Compress pak files (smaller but slower to load)",
        "build_configuration": "Development (debuggable) or Shipping (optimized)",
        "full_rebuild": "Rebuild all code from scratch (slower but cleaner)",
        "cook_all": "Cook all content (vs only referenced content)",
    },
    "build_configurations": {
        "Debug": "Full debugging, no optimization, very slow",
        "DebugGame": "Game code debuggable, engine optimized",
        "Development": "Some optimization, basic profiling, console commands work",
        "Shipping": "Full optimization, no debug, fastest performance",
        "Test": "Shipping with some profiling support",
    },
    "unreal_build_tool": {
        "description": "Build system that compiles C++ code and manages dependencies",
        "target_files": {
            ".Build.cs": "Module definition — dependencies, include paths, compile settings",
            ".Target.cs": "Build target — platform, configuration, module list",
        },
        "key_properties": {
            "PublicDependencyModuleNames": "Modules your code links against publicly",
            "PrivateDependencyModuleNames": "Modules linked privately (not exposed to dependents)",
            "bUseRTTI": "Enable C++ RTTI (default: off)",
            "bEnableExceptions": "Enable C++ exceptions (default: off)",
        },
    },
    "dlc_patching": {
        "description": "Downloadable content and patching system",
        "approaches": {
            "pak_based": "Ship new .pak file with only changed/added assets",
            "chunk_based": "Split content into chunks that can be individually updated",
            "patch_size": "Patches contain only deltas — much smaller than full rebuild",
        },
    },
}

# ============================================================================
# CINEMATICS (Docs 97-99)
# ============================================================================

CINEMATICS_SYSTEM = {
    "sequencer": {
        "description": "UE5's timeline-based animation and cinematic editor",
        "features": [
            "Multi-track timeline for keyframe animation",
            "Camera animation and cuts",
            "Actor property animation (transform, material, visibility)",
            "Event tracks for triggering gameplay events",
            "Sub-sequences for nested cinematic clips",
            "Audio tracks for sound and dialogue",
        ],
        "key_concepts": {
            "Level Sequence": "Asset containing the cinematic timeline and tracks",
            "Binding": "Link between sequencer track and scene actor",
            "Keyframe": "Specific property value at a point in time",
            "Track": "Sequence of keyframes for one property",
            "Sub-Sequence": "Nested Level Sequence within another",
        },
        "workflow": [
            "1. Create Level Sequence asset in Content Browser",
            "2. Add actors and cameras as tracks",
            "3. Keyframe transforms, properties, and events",
            "4. Set up camera cuts for shot sequencing",
            "5. Add audio and event tracks",
            "6. Preview in viewport and fine-tune timing",
        ],
    },
    "movie_render_queue": {
        "description": "High-quality movie rendering pipeline for final output",
        "features": [
            "Render at any resolution (8K, 16K for film)",
            "Anti-aliasing accumulation for pixel-perfect frames",
            "Motion blur with precise shutter angle control",
            "Deferred renderer passes (separate passes for compositing)",
            "Custom export formats (EXR, PNG, video codecs)",
            "Job queue for rendering multiple sequences",
        ],
        "settings": {
            "resolution": "Output resolution (1920x1080, 3840x2160, custom)",
            "anti_aliasing": "Temporal sample count for anti-aliasing (4-64)",
            "motion_blur": "Shutter angle and sample count",
            "output_format": "EXR (HDR compositing), PNG (preview), MP4 (quick review)",
        },
    },
    "take_recorder": {
        "description": "Record live gameplay or performance for cinematics",
        "features": [
            "Record actor transforms, animations, and properties",
            "Record from multiple sources simultaneously",
            "Live-link support for motion capture and virtual production",
            "Review and edit takes in Sequencer",
        ],
        "use_cases": [
            "Record gameplay for trailers",
            "Motion capture sessions",
            "Virtual production recording",
            "Iterative performance capture",
        ],
    },
}

# ============================================================================
# PLUGINS & SAMPLES (Docs 95-96, 100)
# ============================================================================

PLUGINS_SYSTEM = {
    "content_examples": {
        "description": "Sample project demonstrating UE5 features with example levels",
        "sections": [
            "Animation examples",
            "Audio examples",
            "Blueprint communication examples",
            "Landscape and foliage examples",
            "Lighting examples (Lumen, ray tracing)",
            "Material examples (PBR, SSS, layered)",
            "Niagara examples (fire, smoke, fluids)",
            "Physics examples (Chaos, destruction)",
            "Rendering examples (Nanite, TSR, VSM)",
        ],
        "use": "Great reference for learning implementation patterns and best practices",
    },
    "valley_of_the_ancient": {
        "description": "Sample game showcasing UE5 features",
        "features": [
            "Large open world with World Partition",
            "Nanite geometry for detailed environments",
            "Lumen GI and reflections",
            "Virtual Shadow Maps",
            "Chaos destruction system",
            "MetaHuman characters",
        ],
    },
    "plugins": {
        "description": "Plugin system for extending Unreal Engine functionality",
        "plugin_types": {
            "Engine Plugin": "Ships with UE5, available to all projects",
            "Project Plugin": "Specific to a project, stored in project's Plugins folder",
            "Marketplace Plugin": "Distributed via Unreal Marketplace",
            "Custom Plugin": "Developed in-house for specific needs",
        },
        "creating_plugins": [
            "1. Edit > Plugins > New Plugin",
            "2. Choose template (Blank, Editor Tool, etc.)",
            "3. Plugin creates .uplugin file and module structure",
            "4. Add code/assets to the plugin module",
            "5. Other projects can enable the plugin",
        ],
        "plugin_structure": {
            ".uplugin": "Plugin descriptor file",
            "Resources/": "Icon and plugin resources",
            "Source/": "C++ module source code",
            "Content/": "Plugin assets (Blueprints, materials, etc.)",
        },
    },
}

# ============================================================================
# SEARCH AND QUERY FUNCTIONS
# ============================================================================

_ALL_EXPERT_CATEGORIES = {
    "niagara_advanced": NIAGARA_ADVANCED,
    "audio": AUDIO_SYSTEM,
    "ui": UI_SYSTEM,
    "ai_system": AI_SYSTEM,
    "networking": NETWORKING_SYSTEM,
    "optimization": OPTIMIZATION_SYSTEM,
    "packaging": PACKAGING_SYSTEM,
    "cinematics": CINEMATICS_SYSTEM,
    "plugins": PLUGINS_SYSTEM,
}

def get_expert_category(name: str) -> dict:
    """Get a specific expert knowledge category by name."""
    return _ALL_EXPERT_CATEGORIES.get(name, {})

def get_all_expert_categories() -> list:
    """Get list of all expert knowledge category names."""
    return list(_ALL_EXPERT_CATEGORIES.keys())

def search_expert_knowledge(query: str, max_results: int = 10) -> list:
    """Search all expert knowledge categories for matching content."""
    query_lower = query.lower()
    results = []
    
    for cat_name, cat_data in _ALL_EXPERT_CATEGORIES.items():
        _search_recursive(cat_data, cat_name, query_lower, results, "")
    
    results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
    return results[:max_results]

def _search_recursive(data, cat_name, query, results, path):
    """Recursively search nested dicts for query matches."""
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if query in key.lower():
                results.append({
                    "category": cat_name,
                    "key": current_path,
                    "snippet": str(value)[:200] if isinstance(value, (str, int, float)) else str(value)[:200],
                    "relevance": 2.0,
                })
            elif isinstance(value, str) and query in value.lower():
                results.append({
                    "category": cat_name,
                    "key": current_path,
                    "snippet": value[:200],
                    "relevance": 1.0,
                })
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and query in item.lower():
                        results.append({
                            "category": cat_name,
                            "key": current_path,
                            "snippet": item[:200],
                            "relevance": 1.0,
                        })
                        break
            elif isinstance(value, dict):
                _search_recursive(value, cat_name, query, results, current_path)

def get_optimization_profile(target_fps: int) -> dict:
    """Get recommended settings for a target FPS."""
    profiles = {
        30: {
            "name": "Cinematic 30fps",
            "lumen": "Epic",
            "nanite": "Enabled",
            "shadow_quality": 4,
            "texture_quality": 4,
            "post_process": "Full",
            "anti_aliasing": "TSR Epic",
            "note": "Maximum visual quality for pre-rendered or cinematic use",
        },
        60: {
            "name": "Balanced 60fps",
            "lumen": "Medium-High",
            "nanite": "Enabled",
            "shadow_quality": 3,
            "texture_quality": 3,
            "post_process": "Reduced",
            "anti_aliasing": "TSR Medium",
            "note": "Good balance for most games",
        },
        90: {
            "name": "VR 90fps",
            "lumen": "Low or Baked",
            "nanite": "Enabled",
            "shadow_quality": 1,
            "texture_quality": 2,
            "post_process": "Minimal",
            "anti_aliasing": "MSAA",
            "note": "VR requirements — low latency critical",
        },
        120: {
            "name": "Competitive 120fps",
            "lumen": "Disabled",
            "nanite": "Enabled",
            "shadow_quality": 1,
            "texture_quality": 2,
            "post_process": "Minimal",
            "anti_aliasing": "TAA Low",
            "note": "Use baked lighting, minimize GPU overhead",
        },
    }
    return profiles.get(target_fps, profiles[60])

def get_networking_pattern(pattern_name: str) -> dict:
    """Get common networking implementation patterns."""
    patterns = {
        "replicated_health": {
            "description": "Standard health replication pattern",
            "cpp_pattern": "UPROPERTY(ReplicatedUsing=OnRep_Health) float Health;",
            "onrep": "UFUNCTION() void OnRep_Health() — update UI on clients",
            "server_setter": "Server_SetHealth() — client requests, server validates",
        },
        "projectile": {
            "description": "Projectile spawning pattern",
            "server_spawns": "Server RPC spawns the projectile with authority",
            "replicated_movement": "Projectile movement component handles replication",
            "multicast_impact": "NetMulticast for impact effects (particles, sounds)",
        },
        "pickups": {
            "description": "Pickup item pattern",
            "server_authority": "Server validates pickup (collision, inventory)",
            "client_predict": "Optional: client predicts pickup for responsiveness",
            "multicast_cosmetics": "NetMulticast removes visual + plays sound",
        },
    }
    return patterns.get(pattern_name, NETWORKING_SYSTEM.get(pattern_name, {"error": f"Pattern '{pattern_name}' not found. Available patterns: {list(patterns.keys()) + list(NETWORKING_SYSTEM.keys())}"}))

# Export summary
EXPERT_KNOWLEDGE_SUMMARY = {
    "total_categories": len(_ALL_EXPERT_CATEGORIES),
    "categories": list(_ALL_EXPERT_CATEGORIES.keys()),
    "total_documents_covered": "61-100",
    "topics": [
        "Niagara Fluids, Editor, Custom Modules, Data Channels",
        "Audio, MetaSounds, Sound Cues, Spatial Audio, Attenuation",
        "UMG, Widget Blueprints, Common UI, Slate, Widget Components",
        "Behavior Trees, EQS, Navigation, AI Perception, State Tree",
        "Networking, Replication, Performance, Dedicated Servers, Online Subsystem",
        "Lumen Performance, Unreal Insights, Nanite Technical, Scalability",
        "Packaging, Build Tool, DLC/Patching",
        "Sequencer, Movie Render Queue, Take Recorder",
        "Content Examples, Valley of the Ancient, Plugins",
    ],
}