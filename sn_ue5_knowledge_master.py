"""
SuperNinja UE5 Master Knowledge Base — Documents 101-151

This module contains the final tier of UE5 knowledge extracted from
49 official documents (101-151), covering advanced production topics
including editor scripting, virtual production, environment systems,
advanced rendering, networking tools, and production pipeline.

Combined with Core (1-20), Advanced (21-60), and Expert (61-100),
SuperNinja now has knowledge from 151 official UE5 documents.

Knowledge Categories:
  1. editor_scripting    — Editor Utility Widgets, Python scripting, automation
  2. virtual_production  — MetaHuman, Live Link, ICVFX, USD, XR
  3. quixel_landscape    — Quixel Bridge, Landscape, Water System
  4. volumetrics         — Volumetric Clouds, Sky Atmosphere, Height Fog
  5. rendering_master    — Mesh Painting, Decals, Light Functions, Reflections, SSR, SSAO, Distance Fields, Planar Reflections
  6. groom_vt            — Groom/Hair Rendering, Runtime Virtual Texturing
  7. performance_tools   — HLOD, Replication Graph, Network Profiler
  8. content_creation    — Shaders, Textures, Console Commands
  9. physics_advanced    — Physics Constraints, Chaos Vehicles
 10. source_control      — Perforce, Git, Console Development
 11. api_pipeline        — C++ API Reference, Release Notes, Asset Pipeline
 12. production          — Editor Extensibility, Profiling, Localization, Crash Reporting
"""

# =========================================================================
# 1. EDITOR SCRIPTING (Docs 101-102)
# =========================================================================
EDITOR_SCRIPTING = {
    "description": "Editor scripting and automation using Python and Editor Utility Widgets",
    "editor_utility_widgets": {
        "description": "Custom Editor UI tabs using UMG-based widgets",
        "purpose": "Modify the Unreal Editor UI by adding custom tabs accessible from the Windows menu",
        "creation": [
            "Right-click in Content Browser > Editor Utilities > Editor Utility Widget",
            "Name the asset and double-click to open Widget Blueprint editor",
            "Edit the Widget Blueprint as needed",
            "Right-click the asset > Run Editor Utility Widget to open as Editor tab",
        ],
        "features": {
            "based_on_umg": "Uses same UMG system as in-game UI",
            "dockable_tabs": "Tabs dock with Level Editor tabs",
            "tools_menu": "Appears in Tools > Editor Utility Widgets after first run",
            "beta_feature": "Beta feature — use with caution in production",
        },
        "use_cases": [
            "Custom asset batch processing UI",
            "Editor tool dashboards",
            "Content validation interfaces",
            "Pipeline automation panels",
        ],
    },
    "python_scripting": {
        "description": "Python scripting for Unreal Editor automation",
        "why_python": [
            "De facto language for production pipelines in media/entertainment",
            "Wide range of 3D application support for interoperability",
            "Easy for new programmers to learn",
            "Complex UI creation through PySide and other modules",
            "Large community with free modules",
        ],
        "setup": [
            "Enable Python Editor Script Plugin in Edit > Plugins",
            "Configure Python settings in Project Settings > Python",
            "Additional paths for custom scripts",
            "Remote execution for external IDE integration",
        ],
        "execution_methods": {
            "output_log": "Type Python commands in Output Log (set cmd mode to Python)",
            "python_console": "Use the Python Console window",
            "script_files": "Place .py files in Content/Python or configured paths",
            "remote_execution": "Send Python commands from external IDE/tools via UDP",
            "startup_scripts": "Configure init_unreal.py to run on editor startup",
        },
        "key_apis": {
            "unreal_module": "Main module providing access to all Unreal types and functions",
            "editor_level_library": "Actor spawning, level operations, selection",
            "editor_asset_library": "Content browser operations, asset management",
            "editor_dialog": "Message dialogs, file dialogs, asset picker dialogs",
            "system_library": "Console commands, delay, timers",
        },
        "best_practices": [
            "Use unreal.EditorAssetLibrary for content operations",
            "Use unreal.EditorLevelLibrary for level operations",
            "Always wrap operations in try/except for error handling",
            "Use log functions for debugging (unreal.log, unreal.log_warning)",
            "Place utility scripts in Content/Python for auto-discovery",
        ],
    },
}

# =========================================================================
# 2. VIRTUAL PRODUCTION (Docs 103-107)
# =========================================================================
VIRTUAL_PRODUCTION = {
    "description": "Virtual production pipeline: MetaHuman, Live Link, ICVFX, USD, XR",
    "metahuman": {
        "description": "MetaHuman Framework for creating high-fidelity digital humans",
        "components": {
            "meta_human_creator": "Cloud-based application for creating MetaHuman characters",
            "meta_human_identity": "Convert real-world photos to MetaHuman likenesses",
            "meta_human_animator": "Performance capture and animation transfer",
            "dna_calibration": "Programmatic control over MetaHuman DNA and rig",
        },
        "workflow": [
            "Create character in MetaHuman Creator (web-based)",
            "Download to project via Quixel Bridge",
            "Use MetaHuman Identity for photo-based likeness transfer",
            "Animate using Control Rig, Live Link, or motion capture",
        ],
        "key_features": [
            "High-fidelity facial rigging (600+ blend shapes)",
            "Built-in grooming (hair, eyebrows, lashes)",
            "Auto-rigging and body morphing",
            "Compatible with Sequencer and animation workflows",
        ],
    },
    "live_link": {
        "description": "Real-time streaming of animation data from external sources",
        "purpose": "Connect motion capture, animation tools, and custom sources to Unreal",
        "sources": {
            "mocap": "Motion capture systems (OptiTrack, Vicon, etc.)",
            "face_ar": "iPhone ARKit face tracking via Live Link Face app",
            "maya": "Autodesk Maya animation curves",
            "blender": "Blender animation data via Live Link plugin",
            "custom": "Any source implementing the Live Link interface",
        },
        "setup": [
            "Enable Live Link plugin in Edit > Plugins",
            "Open Live Link window (Window > Live Link)",
            "Add source (e.g., Live Link Face, mocap system)",
            "Map Live Link subject to skeletal mesh in scene",
            "Assign Live Link controller to animation blueprint",
        ],
        "key_concepts": {
            "subject": "A single tracked entity (e.g., one performer's face)",
            "role": "Defines how Live Link data maps to animation (e.g., Face, Body)",
            "frame": "Single frame of data from the source",
            "static_data": "Subject data that doesn't change per frame (bone names)",
            "frame_data": "Per-frame animation data (transforms, curve values)",
        },
    },
    "icvfx": {
        "description": "In-Camera VFX for virtual production stages",
        "purpose": "Render photorealistic environments on LED walls surrounding a physical set",
        "components": {
            "led_volume": "Curved LED wall displaying the virtual environment",
            "n_display": "Multi-display rendering configuration for LED walls",
            "inner_frustum": "Camera-tracked rendering for the physical camera view",
            "outer_frustum": "Background rendering visible to the naked eye",
            "color_correct_regions": "Per-region color correction for LED wall blending",
        },
        "workflow": [
            "Set up nDisplay configuration for LED wall layout",
            "Configure inner frustum (tracked camera) rendering",
            "Set up green screen or LED wall color keying",
            "Add ICVFX camera with lens settings",
            "Configure color correction regions for blending",
            "Run virtual production shoot with live tracking",
        ],
    },
    "usd": {
        "description": "Universal Scene Description for interop and pipeline",
        "purpose": "Industry-standard format for scene interchange between DCC tools",
        "features": {
            "stage": "USD scene graph root — equivalent to UE level",
            "prim": "USD scene graph entry — maps to actors/components",
            "attribute": "Per-prim data (transforms, materials, custom data)",
            "composition": "Layer-based composition (sublayers, references, payloads, variants)",
            "purpose": "Render/Proxy/Guide visibility semantics",
            "variants": "Variant sets for switching between options",
        },
        "ue5_integration": [
            "Enable USD Importer plugin in Edit > Plugins",
            "Import USD stages as UE levels",
            "Export UE levels to USD format",
            "Live-sync between USD and UE changes",
        ],
    },
    "xr": {
        "description": "XR (VR/AR) development in Unreal Engine",
        "vr_features": {
            "motion_controllers": "Hand controllers with position/rotation tracking",
            "hand_tracking": "Controller-free hand tracking (Quest, PCVR)",
            "haptics": "Controller/rumble haptic feedback",
            "passthrough": "Mixed reality passthrough (Quest Pro, etc.)",
            "stereo_layers": "Stereoscopic rendering layers for UI",
        },
        "ar_features": {
            "plane_detection": "Detect real-world surfaces (floors, tables, walls)",
            "point_clouds": "Real-world 3D point data",
            "image_tracking": "Detect and track known 2D images",
            "face_tracking": "AR face mesh with blend shapes",
            "geo_anchors": "Geo-located AR anchors",
        },
        "setup": [
            "Enable XR plugins (OpenXR, Oculus, etc.)",
            "Configure VR mode in Project Settings",
            "Set up player pawn with VR camera and motion controllers",
            "Configure tracking origin (Floor, Eye, Stage)",
        ],
    },
}

# =========================================================================
# 3. QUIXEL & LANDSCAPE (Docs 108-110)
# =========================================================================
QUIXEL_LANDSCAPE = {
    "description": "Quixel Megascans integration, Landscape system, and Water system",
    "quixel_bridge": {
        "description": "Bridge between Quixel Megascans library and Unreal Engine",
        "features": {
            "megascans_library": "World's largest photogrammetry asset library",
            "auto_lod": "Automatic LOD generation for imported meshes",
            "auto_materials": "Auto-generated master materials with PBR properties",
            "nanite_ready": "All meshes Nanite-compatible by default",
            "atmosphere_integration": "Assets designed for Lumen and atmospheric rendering",
        },
        "workflow": [
            "Open Quixel Bridge (standalone or in-editor)",
            "Browse/search Megascans library",
            "Select assets and configure export settings",
            "Import directly to project Content Browser",
            "Assets auto-configure with correct materials and LODs",
        ],
        "asset_types": {
            "3d_assets": "Scanned 3D models (rocks, props, buildings, etc.)",
            "surfaces": "Tiling surface materials (ground, walls, floors, etc.)",
            "3d_plants": "Botanical assets (trees, bushes, grass, flowers)",
            "decals": "Surface detail decals (stains, cracks, weathering)",
            "imposters": "Billboard-based imposters for distant vegetation",
        },
    },
    "landscape": {
        "description": "Large-scale terrain system with sculpting and painting",
        "components": {
            "landscape_actor": "The terrain mesh with LOD system",
            "landscape_material": "Auto-Layer material with height-based blending",
            "landscape_layers": "Paint layers for different ground types (grass, dirt, rock, snow)",
            "foliage_system": "Procedural foliage spawning on landscape",
            "splines": "Roads, paths, rivers on the landscape surface",
            "world_partition": "Large world loading and streaming",
        },
        "creation_methods": [
            "Create new landscape from scratch (blank)",
            "Import from heightmap (16-bit or 8-bit grayscale)",
            "Import from FBX mesh",
            "Use landscape blueprint for procedural generation",
        ],
        "sculpting_tools": {
            "sculpt": "Raise/lower terrain",
            "smooth": "Smooth terrain height differences",
            "flatten": "Flatten to target height",
            "ramp": "Create inclined surface between two points",
            "erosion": "Simulate hydraulic/thermal erosion",
            "noise": "Add procedural noise to terrain",
        },
        "performance_tips": [
            "Use Landscape instead of StaticMesh for terrain",
            "Keep component size at 63x63 or 127x127 quads",
            "Use LOD for distant landscape sections",
            "Limit visible components with World Partition",
            "Use Nanite on landscape grass and foliage meshes",
        ],
    },
    "water_system": {
        "description": "Water body system with oceans, rivers, lakes",
        "components": {
            "water_body_ocean": "Infinite ocean with waves and underwater",
            "water_body_river": "Flowing river with spline-based path",
            "water_body_lake": "Enclosed lake with custom shoreline",
            "water_info": "Simulation data for fluid interactions",
            "buoyancy": "Physics-based buoyancy for floating objects",
        },
        "setup": [
            "Enable Water plugin in Edit > Plugins",
            "Add Water Body actor to level",
            "Select type (Ocean, River, Lake)",
            "Configure water material and wave settings",
            "Add spline points for rivers and lake shapes",
        ],
        "key_features": {
            "gerstner_waves": "Physically-based wave generation",
            "underwater_post_process": "Automatic underwater rendering (color shift, fog, caustics)",
            "fluid_surface": "Interactive fluid surface simulation",
            "single_layer_water": "Optimized single-layer water material for rivers",
        },
    },
}

# =========================================================================
# 4. VOLUMETRICS (Docs 111-112)
# =========================================================================
VOLUMETRICS = {
    "description": "Volumetric rendering: clouds, sky atmosphere, height fog",
    "volumetric_clouds": {
        "description": "Real-time volumetric cloud rendering with ray-marching",
        "component": "Volumetric Cloud component on a Cloud Actor",
        "features": {
            "ray_marched": "True volumetric ray-marched clouds (not billboards)",
            "lighting": "Lit by directional light with multi-scatter approximation",
            "phase_function": "Mie and Rayleigh phase functions for realistic scattering",
            "altitude_control": "Cloud layer altitude and thickness control",
            "wind": "Wind-driven cloud movement and shape evolution",
            "precipitation": "Rain and snow from cloud layers",
        },
        "properties": {
            "cloud_material": "Material with cloud sample and view resources",
            "altitude": "Cloud layer base altitude (typically 1000-5000m)",
            "density": "Cloud density multiplier",
            "view_distance": "Maximum cloud rendering distance",
            "sample_count": "Ray marching sample count (affects quality/performance)",
        },
        "tips": [
            "Use low sample count (32-64) for real-time, high (128+) for cinematics",
            "Configure Sky Atmosphere for correct lighting interactions",
            "Use Cloud Capture actors for local cloud density control",
            "Disable Temporal AA for crisp cloud edges (but increases noise)",
        ],
    },
    "sky_atmosphere": {
        "description": "Physically-based sky and atmosphere rendering",
        "features": {
            "rayleigh_scattering": "Air molecule scattering (blue sky)",
            "mie_scattering": "Aerosol scattering (sun halos, red sunset)",
            "absorption": "Ozone absorption for color accuracy",
            "multi_scatter": "Multi-scattering for realistic indirect sky light",
            "altitude_control": "Sky changes based on camera altitude (space to ground)",
        },
        "properties": {
            "mie_scattering_scale": "Controls haze/sun halo intensity",
            "rayleigh_scattering_scale": "Controls blue sky intensity",
            "planet_radius": "Planet radius for horizon calculation",
            "atmosphere_height": "Atmosphere layer height (default ~100km)",
            "air_density": "Air density at sea level",
        },
    },
    "height_fog": {
        "description": "Exponential Height Fog for atmospheric depth",
        "features": {
            "exponential": "Fog density decreases exponentially with height",
            "fog_color": "Base fog color (tinted by lights in-scattering)",
            "second_fog_layer": "Optional second density for layered fog effects",
            "volumetric_fog": "Optional volumetric fog for light shafts and scattering",
        },
        "properties": {
            "fog_density": "Global fog density",
            "fog_height_falloff": "How quickly fog thins with altitude",
            "fog_max_opacity": "Maximum fog opacity (0-1)",
            "start_distance": "Distance from camera where fog begins",
            "fog_inscattering_color": "Color of light scattered through fog",
        },
        "tips": [
            "Use with Volumetric Fog enabled for light shafts",
            "Set Fog Max Opacity < 1.0 to avoid completely hiding distant objects",
            "Use second fog layer for complex atmospheric effects",
            "Pair with Sky Atmosphere for consistent outdoor scenes",
        ],
    },
}

# =========================================================================
# 5. RENDERING MASTER (Docs 113-120)
# =========================================================================
RENDERING_MASTER = {
    "description": "Advanced rendering features: mesh painting, decals, light functions, reflections",
    "mesh_painting": {
        "description": "Paint colors, textures, and vertex weights directly on meshes",
        "modes": {
            "paint_colors": "Paint vertex colors on mesh faces",
            "paint_weights": "Paint texture blending weights",
            "paint_textures": "Paint textures directly on mesh surface (requires UV)",
        },
        "tools": [
            "Brush size, strength, and falloff",
            "Paint/erase/smooth modes",
            "Fill entire mesh with color",
            "Copy/paste vertex colors between meshes",
        ],
    },
    "decals": {
        "description": "Project materials onto surfaces for detail",
        "use_cases": [
            "Surface details (stains, cracks, posters)",
            "Bullet holes and impact marks",
            "Wetness and moisture effects",
            "Road markings and signs",
        ],
        "types": {
            "mesh_decal": "Decal actor with DBuffer or Deferred Decal material",
            "decal_actor": "Placeable decal with sort order and fade",
            "decal_material": "Material domain set to Deferred Decal",
        },
        "performance": [
            "DBuffer decals modify GBuffer (higher quality, more cost)",
            "Deferred decals don't modify GBuffer (lower quality, less cost)",
            "Limit overlap of multiple decals",
            "Use decal fade distance for culling",
        ],
    },
    "light_functions": {
        "description": "Material-based light projection for pattern and texture",
        "ies_profiles": {
            "description": "IES light profiles for physically accurate light distribution",
            "format": "Standard IES photometric file format",
            "use": "Assign to Light > IES Texture on any light type",
            "benefit": "Accurate real-world light distribution patterns",
        },
        "light_function_materials": {
            "description": "Custom material projected through a light",
            "use": "Assign material to Light > Light Function",
            "effects": ["Window light patterns", "Shadow patterns from blinds", "Gobo/cookie effects", "Animated light flicker"],
            "limitations": [
                "Only works with Stationary and Movable lights",
                "Not supported in Lumen GI (only direct light)",
                "Use Lightmass for baked light functions",
            ],
        },
    },
    "reflections": {
        "description": "Reflection systems in UE5",
        "types": {
            "lumen_reflections": "Default in UE5, screen-space + trace-based, best quality",
            "ssr": "Screen Space Reflections — fast, limited to what's on screen",
            "planar_reflections": "Capture a view for perfect planar mirror reflections",
            "reflection_probes": "Cube map captures for parallax-correct reflections",
            "sky_light_reflections": "Sky reflection captured from HDRI or atmosphere",
        },
        "lumen_vs_ssr": {
            "lumen_advantages": ["Handles off-screen reflections", "Works with all surfaces", "Physically accurate"],
            "lumen_cost": "More expensive than SSR, traced per-pixel",
            "ssr_advantages": ["Lower cost than Lumen reflections", "Good for smooth surfaces"],
            "ssr_limitations": ["No off-screen reflections", "Screen-space artifacts at edges", "Doesn't reflect characters/vehicles behind camera"],
        },
        "reflection_environment": {
            "description": "Placed Reflection Capture actors for specular reflection",
            "sphere_capture": "Captures 360-degree cube map for local reflections",
            "box_capture": "Captures parallax-corrected cube map for interiors",
            "tips": [
                "Place captures in key locations (rooms, corridors)",
                "Adjust influence radius to avoid bleed",
                "Update captures after significant scene changes",
            ],
        },
    },
    "ssr": {
        "description": "Screen Space Reflections — fast, limited reflection method",
        "quality_settings": {
            "high": "Full-resolution, multi-pass (most expensive)",
            "medium": "Half-resolution with temporal smoothing",
            "low": "Quarter-resolution for maximum performance",
        },
        "limitations": [
            "Cannot reflect objects behind camera",
            "Screen-space artifacts at edges",
            "No reflections of off-screen geometry",
            "Inaccurate for rough surfaces",
        ],
    },
    "ssao": {
        "description": "Screen Space Ambient Occlusion for contact shadow depth",
        "purpose": "Darken areas where surfaces are close together (corners, crevices)",
        "settings": {
            "intensity": "AO darkening strength",
            "radius": "Distance to check for occlusion",
            "power": "Exponent for AO falloff",
            "bias": "Prevent self-occlusion artifacts",
        },
        "lumen_ao": "Lumen provides its own ambient occlusion that replaces SSAO when enabled",
    },
    "distance_fields": {
        "description": "Global Distance Fields for ambient occlusion and shadows",
        "purpose": "Represent scene geometry as signed distance fields for GPU queries",
        "uses": [
            "Lumen scene representation and tracing",
            "Distance Field Ambient Occlusion (DFAO)",
            "Shadow casting from dynamic objects",
            "Mesh Distance Fields for collision queries",
        ],
        "generation": [
            "Auto-generated from mesh geometry",
            "Stored in Signed Distance Field volume textures",
            "Composited into Global Distance Field per object",
        ],
        "limitations": [
            "Requires mesh to have valid distance field (complex shapes may fail)",
            "Memory cost for distance field volumes",
            "Thin geometry can cause artifacts",
        ],
    },
    "planar_reflections": {
        "description": "Perfect mirror reflections for flat surfaces",
        "use_cases": ["Floor mirrors", "Water surface reflections", "Glass/steel reflections"],
        "setup": [
            "Add Planar Reflection component",
            "Position at reflection surface",
            "Configure screen percentage (lower = better performance)",
        ],
        "cost": "Very expensive — renders the scene again from the reflection view",
    },
}

# =========================================================================
# 6. GROOM & VIRTUAL TEXTURING (Docs 121-122)
# =========================================================================
GROOM_VT = {
    "description": "Groom hair/fur rendering and Runtime Virtual Texturing",
    "groom": {
        "description": "Hair and fur rendering system for characters and creatures",
        "components": {
            "groom_asset": "Alembic-based hair description (curves, guides)",
            "groom_binding": "Links groom to skeletal mesh with deformation",
            "hair_material": "Material with hair shading model (anisotropic)",
        },
        "creation": [
            "Create groom in external tool (Houdini, XGen, etc.)",
            "Export as Alembic (.abc) cache",
            "Import Alembic as Groom asset in UE5",
            "Create Groom Binding to link with skeletal mesh",
            "Apply hair material with anisotropic shading",
        ],
        "rendering": {
            "strand": "Individual hair strands (high quality, most expensive)",
            "card": "Geometry cards with hair texture (balanced quality/cost)",
            "mesh": "Hair mesh geometry (lowest cost, static styles)",
        },
        "features": [
            "Physical-based hair rendering with multiple scattering",
            "Card and mesh LODs for performance scaling",
            "Simulation via Niagara integration",
            "Group-based LOD and culling",
        ],
    },
    "runtime_virtual_texturing": {
        "description": "Runtime Virtual Texturing for automatic texture streaming and blending",
        "purpose": "Dynamically composite and blend materials at runtime, avoiding texture resolution limits",
        "use_cases": [
            "Landscape material blending (no UV tiling artifacts)",
            "Automatic texture streaming for large surfaces",
            "Complex material layer blending at runtime",
            "Eliminating visible texture tiling on large meshes",
        ],
        "setup": [
            "Create Runtime Virtual Texture asset",
            "Add Runtime Virtual Texture Volume to level",
            "Set material to output to RVT",
            "Bind material to the RVT volume",
        ],
        "types": {
            "rvt": "Runtime Virtual Texture — generated at runtime",
            "svt": "Streaming Virtual Texture — pre-baked, streamed from disk",
        },
        "performance": [
            "RVT renders on-demand, only visible pages are computed",
            "Cache system avoids recomputation for static views",
            "Higher initial cost than regular textures, lower per-frame cost for complex blending",
            "Use with landscape for best results",
        ],
    },
}

# =========================================================================
# 7. PERFORMANCE TOOLS (Docs 123-125)
# =========================================================================
PERFORMANCE_TOOLS = {
    "description": "HLOD, Replication Graph, and Network Profiler for performance",
    "hlod": {
        "description": "Hierarchical Level of Detail for distant geometry",
        "purpose": "Combine multiple static meshes into single proxy meshes at distance",
        "workflow": [
            "Configure HLOD settings in World Settings",
            "Set HLOD layers (distance thresholds)",
            "Build HLOD (creates proxy meshes and materials)",
            "Enable HLOD in viewport to preview",
        ],
        "proxy_methods": {
            "simplify_mesh": "Generate simplified geometry from source meshes",
            "merge_mesh": "Merge source meshes into single proxy",
            "custom": "Use manually created proxy meshes",
        },
        "tips": [
            "Use for outdoor scenes with many distant buildings/objects",
            "Combine with Nanite for automatic LOD instead of HLOD",
            "HLOD is still useful for non-Nanite meshes",
            "Set appropriate screen size for switching",
        ],
    },
    "replication_graph": {
        "description": "Server-side replication optimization for multiplayer",
        "purpose": "Reduce network bandwidth by only replicating relevant actors to each client",
        "how_it_works": [
            "Groups actors into spatial grid cells",
            "Tracks which cells each client can see",
            "Only replicates actors in visible cells",
            "Supports dependency chains (player → inventory → items)",
        ],
        "node_types": {
            "grid_spatialization": "Spatial grid for actors that move in the world",
            "cell_manager": "Manages grid cells and client visibility",
            "always_relevant": "Actors always replicated (GameMode, PlayerState)",
            "dependent_actors": "Actors that replicate only when their dependent actor does",
            "dormancy_node": "Dormancy system to skip unchanged actors",
        },
        "benefits": [
            "Significant bandwidth reduction in large worlds",
            "Automatic spatial culling of irrelevant actors",
            "Dependency tracking for related actors",
        ],
    },
    "network_profiler": {
        "description": "Profiling tool for network performance",
        "features": {
            "bandwidth_tracking": "Track bytes sent/received per actor",
            "rpc_monitoring": "Monitor RPC frequency and size",
            "replication_graph_view": "Visualize replication graph state",
            "packet_analysis": "Analyze network packet composition",
        },
        "usage": [
            "Enable Net Logging in session settings",
            "Play multiplayer session",
            "Open Network Profiler from Window > Developer Tools",
            "Analyze bandwidth hotspots and RPC storms",
        ],
        "tips": [
            "Profile early and often during multiplayer development",
            "Watch for actors with high replication frequency",
            "Use Replication Graph to reduce bandwidth",
            "Set NetUpdateFrequency appropriately per actor",
        ],
    },
}

# =========================================================================
# 8. CONTENT CREATION (Docs 126-128)
# =========================================================================
CONTENT_CREATION = {
    "description": "Console commands, shader development, and texture editing",
    "console_commands": {
        "description": "Runtime console commands for debugging and configuration",
        "categories": {
            "rendering": [
                "r.Lumen.DiffuseIndirect.Allow 0/1 — Toggle Lumen GI",
                "r.ScreenPercentage [value] — Set render resolution",
                "r.AntiAliasingMethod 0-4 — Set AA method",
                "r.Shadow.Quality [0-5] — Shadow quality level",
                "r.Nanite 0/1 — Toggle Nanite rendering",
                "r.VirtualTexturing 0/1 — Toggle VT",
            ],
            "performance": [
                "stat fps — Show FPS counter",
                "stat unit — Show frame time breakdown",
                "stat GPU — Show GPU timing",
                "stat SceneRendering — Show rendering stats",
                "ProfileGPU — Capture single frame GPU profile",
                "UnrealInsights — Launch Unreal Insights profiler",
            ],
            "ai": [
                "ai.debug.eqs — EQS debugging",
                "Navigation.DebugDraw 0/1 — NavMesh visualization",
            ],
            "networking": [
                "Net.PktLoss 0/1 — Simulate packet loss",
                "Net.PktLag [ms] — Simulate network latency",
            ],
        },
    },
    "shader_development": {
        "description": "Custom shader development in Unreal Engine",
        "approaches": {
            "material_editor": "Node-based visual shader authoring",
            "usf_files": "Unreal Shader Files for custom vertex/pixel shaders",
            "ush_files": "Unreal Shader Headers for shared code",
            "slang": "Slang shading language for compute shaders",
        },
        "key_concepts": {
            "material_domain": "Surface, Deferred Decal, Light Function, Post Process, User Interface",
            "blend_mode": "Opaque, Masked, Translucent, Additive, Modulate",
            "shading_model": "Unlit, Default Lit, Subsurface, Clear Coat, Two-Sided Foliage, Hair, Cloth, Eye",
            "compilation": "Shaders compile on-demand; use Shader Compile Farm for distributed compilation",
        },
        "tips": [
            "Use Material Editor for 95% of shader needs",
            "Custom USF only needed for truly custom rendering passes",
            "Test on multiple platforms early (DX12, Vulkan, Metal)",
            "Use Shader Complexity view mode to spot expensive shaders",
        ],
    },
    "texture_editing": {
        "description": "Texture asset editor and management",
        "features": {
            "import_formats": "PNG, TGA, BMP, JPEG, EXR, HDR, DDS",
            "compression": "BC1-BC7 (DXT), ASTC, ETC2, PVRTC per platform",
            "mip_maps": "Automatic mip generation with settings",
            "virtual_texturing": "Build as Virtual Texture for large textures",
            "srgb": "sRGB for color textures, Linear for data (normals, roughness, masks)",
        },
        "best_practices": [
            "Use power-of-two dimensions for optimal compression",
            "Set sRGB correctly (color=on, data=off)",
            "Use compression appropriate to platform",
            "Enable Virtual Texturing for textures > 2048px",
            "Use Texture Groups for LOD and streaming control",
        ],
    },
}

# =========================================================================
# 9. PHYSICS ADVANCED (Docs 129-130)
# =========================================================================
PHYSICS_ADVANCED = {
    "description": "Physics constraints and Chaos Vehicles",
    "physics_constraints": {
        "description": "Joints and constraints for physics simulation",
        "types": {
            "hinge": "Rotation around single axis (door, wheel)",
            "ball_and_socket": "Free rotation around point (chain link, pendulum)",
            "prismatic": "Linear movement along axis (piston, slider)",
            "d6": "6-DOF constraint with per-axis limits",
            "cone_limit": "Angular limit in a cone shape",
            "twist_limit": "Angular limit around primary axis",
        },
        "setup": [
            "Add Physics Constraint component to actor",
            "Set Component Name 1 (first body)",
            "Set Component Name 2 (second body)",
            "Configure linear and angular limits",
            "Enable collision between constrained bodies if needed",
        ],
        "properties": {
            "linear_limit": "Linear movement limit along each axis",
            "angular_limit": "Rotation limit around each axis",
            "drive": "Motor/force drive for powered joints",
            "breakable": "Force threshold to break the constraint",
            "projection": "Correct constraint drift for stability",
        },
    },
    "chaos_vehicles": {
        "description": "Chaos Vehicle System for cars, trucks, and other vehicles",
        "components": {
            "wheeled_vehicle": "Main vehicle pawn with physics simulation",
            "wheel_components": "Individual wheels with suspension and tire model",
            "vehicle_animation": "Animation blueprint for wheel and steering animation",
        },
        "setup": [
            "Enable Chaos Vehicles plugin",
            "Create WheeledVehiclePawn class",
            "Import vehicle mesh with proper rigging",
            "Configure wheel colliders and suspension",
            "Set up vehicle input bindings",
        ],
        "physics": {
            "engine_torque": "Engine torque curve vs RPM",
            "transmission": "Gear ratios, automatic/manual shift",
            "differential": "Drive type (FWD, RWD, AWD)",
            "suspension": "Spring rate, damping, ride height",
            "tire_model": "Pacejka or simple tire friction model",
        },
    },
}

# =========================================================================
# 10. SOURCE CONTROL (Docs 131-133)
# =========================================================================
SOURCE_CONTROL = {
    "description": "Version control and console development setup",
    "perforce": {
        "description": "Perforce integration for enterprise version control",
        "setup": [
            "Install Perforce client (P4V)",
            "Configure connection in Edit > Source Control",
            "Select Perforce as provider",
            "Enter server, workspace, and user credentials",
        ],
        "best_practices": [
            "Use Streams for project organization",
            "Set up .p4ignore for excluding build artifacts",
            "Use exclusive checkout for binary assets",
            "Configure workspace options (allwrite, clobber)",
        ],
    },
    "git": {
        "description": "Git integration for version control",
        "setup": [
            "Install Git and Git LFS",
            "Enable Git Source Control plugin",
            "Configure in Edit > Source Control",
            "Select Git as provider, set repository path",
        ],
        "best_practices": [
            "Use Git LFS for binary assets (meshes, textures)",
            "Configure .gitignore for Build/, Intermediate/, DerivedDataCache/",
            "Commit .uproject and Config/ files",
            "Use .gitattributes for LFS tracking patterns",
        ],
    },
    "console_development": {
        "description": "Developing for consoles (PlayStation, Xbox, Switch)",
        "prerequisites": [
            "Register as platform developer with console holder",
            "Sign NDA and access agreements",
            "Obtain development hardware (dev kits, test kits)",
            "Access platform-specific SDK",
        ],
        "porting_steps": [
            "Strip out non-console features",
            "Hard-code quality levels per platform",
            "Configure rendering settings for certification",
            "Test with platform-specific validation tools",
        ],
        "certification": [
            "Follow platform holder certification requirements (TCR/TRC)",
            "Use SDK validation tools",
            "Test on target hardware extensively",
            "Submit for certification review",
        ],
    },
}

# =========================================================================
# 11. API & PIPELINE (Docs 136-137)
# =========================================================================
API_PIPELINE = {
    "description": "C++ API reference and UE 5.4 release notes",
    "api_reference": {
        "description": "Unreal Engine C++ API documentation",
        "sections": {
            "class_hierarchy": "Complete class hierarchy of all Engine classes",
            "classes": "All documented classes",
            "constants": "Alphabetical list of all constants",
            "developer_modules": "Index of developer-facing modules",
            "editor_modules": "Index of editor modules",
            "enums": "All documented enumerations",
            "functions": "Alphabetical list of functions",
            "plugin_modules": "Index of plugin modules",
            "runtime_modules": "Index of runtime modules",
            "quick_start": "Most commonly used types and patterns",
        },
        "common_classes": {
            "UObject": "Base class for all Unreal objects",
            "AActor": "Base class for all actors in the world",
            "APawn": "Actor that can be possessed by a controller",
            "ACharacter": "Pawn with character movement and collision",
            "UActorComponent": "Component that can be added to actors",
            "USceneComponent": "Component with transform in the world",
            "UPrimitiveComponent": "Component with rendering and collision",
            "USkeletalMeshComponent": "Component for animated skeletal meshes",
            "UStaticMeshComponent": "Component for static meshes",
        },
    },
    "release_54": {
        "description": "Unreal Engine 5.4 release highlights",
        "features": {
            "animation": [
                "Layered Control Rig system",
                "Animation Authoring improvements",
                "New Gizmos for translation/rotation/scale",
                "Constraints 2.0 with improved evaluation",
                "Anim Details 2.0 / Channel Box",
            ],
            "rendering": [
                "Nanite improvements (programmatic rasterization)",
                "Lumen improvements (better quality and performance)",
                "TSR improvements (reduced ghosting)",
                "Virtual Shadow Map improvements",
            ],
            "worldbuilding": [
                "PCG framework improvements",
                "Modeling tool enhancements",
                "Water system improvements",
            ],
            "virtual_production": [
                "ICVFX improvements",
                "nDisplay enhancements",
                "Lens calibration improvements",
            ],
            "simulation": [
                "Chaos physics improvements",
                "Vehicle dynamics updates",
                "Cloth simulation improvements",
            ],
        },
    },
}

# =========================================================================
# 12. PRODUCTION (Docs 138-151)
# =========================================================================
PRODUCTION = {
    "description": "Production pipeline: asset management, extensibility, profiling, localization, crash reporting",
    "asset_pipeline": {
        "description": "Asset management and processing pipeline",
        "stages": [
            "Import raw assets (FBX, USD, Alembic)",
            "Process in Editor (materials, LODs, collisions)",
            "Validate assets (content audit, texture sizes)",
            "Version control commit",
            "Cook and package for platform",
        ],
        "automation": [
            "Python scripting for batch operations",
            "Editor Utility Widgets for custom tools",
            "Asset Actions for content processing",
            "Scriptable asset import settings",
        ],
    },
    "editor_extensibility": {
        "description": "Extending the Unreal Editor with custom tools and workflows",
        "methods": {
            "plugins": "Create custom plugins with modules and content",
            "editor_subsystems": "Add global editor systems",
            "detail_customizations": "Custom property editors in Details panel",
            "graph_extensions": "Custom Blueprint/Animation graph nodes",
            "asset_actions": "Right-click content browser actions",
            "toolbar_extensions": "Add buttons to editor toolbars",
        },
    },
    "profiling": {
        "description": "Performance profiling and optimization workflow",
        "tools": {
            "unreal_insights": "Frame-by-frame CPU/GPU timing analysis",
            "stat_commands": "Runtime stat commands for quick profiling",
            "profilegpu": "Single-frame GPU profile",
            "shader_complexity": "View mode for shader cost visualization",
            "nanite_visualization": "Nanite cluster and triangle visualization",
        },
        "workflow": [
            "1. Identify problem (stat fps, stat unit)",
            "2. Determine scope (GPU or CPU bound)",
            "3. Profile with appropriate tool (Insights, GPU Profiler)",
            "4. Find hotspots (highest-cost functions)",
            "5. Optimize (reduce draw calls, simplify materials, adjust LODs)",
            "6. Verify improvement (re-profile)",
        ],
    },
    "localization": {
        "description": "Multi-language support and localization pipeline",
        "workflow": [
            "1. Mark all user-facing strings for gathering",
            "2. Gather strings using Localization Dashboard",
            "3. Export to translation files (.po, .csv)",
            "4. Translate strings in target languages",
            "5. Import translated strings back",
            "6. Package with localized assets",
        ],
        "key_concepts": {
            "culture": "Language/region code (en, fr-FR, ja, zh-Hans)",
            "text_namespace": "Logical grouping of localized strings",
            "string_table": "Centralized string management for UI",
            "localization_dashboard": "Editor tool for managing translations",
        },
    },
    "crash_reporting": {
        "description": "Crash reporting and diagnostics for shipped games",
        "features": {
            "auto_report": "Automatic crash report on application crash",
            "callstack": "Error type and callstacks",
            "system_info": "System information and build configuration",
            "log_output": "Log output at moment of crash",
            "custom_context": "Custom game context key/value pairs",
            "user_comments": "User-entered crash description",
        },
        "setup": [
            "Enable in Project Settings > Packaging > Include Crash Reporter",
            "Configure CrashReportClient in DefaultGame.ini",
            "Set DataRouterUrl for third-party crash service",
            "Add custom context via FPlatformCrashContext::SetGameData",
        ],
    },
}

# =========================================================================
# CATEGORY INDEX
# =========================================================================
_ALL_MASTER_CATEGORIES = {
    "editor_scripting": EDITOR_SCRIPTING,
    "virtual_production": VIRTUAL_PRODUCTION,
    "quixel_landscape": QUIXEL_LANDSCAPE,
    "volumetrics": VOLUMETRICS,
    "rendering_master": RENDERING_MASTER,
    "groom_vt": GROOM_VT,
    "performance_tools": PERFORMANCE_TOOLS,
    "content_creation": CONTENT_CREATION,
    "physics_advanced": PHYSICS_ADVANCED,
    "source_control": SOURCE_CONTROL,
    "api_pipeline": API_PIPELINE,
    "production": PRODUCTION,
}

MASTER_KNOWLEDGE_SUMMARY = {
    "total_categories": len(_ALL_MASTER_CATEGORIES),
    "categories": list(_ALL_MASTER_CATEGORIES.keys()),
    "total_documents_covered": "101-151",
    "topics": [
        "Editor Utility Widgets, Python Scripting, Automation",
        "MetaHuman, Live Link, ICVFX, USD, XR (VR/AR)",
        "Quixel Bridge, Landscape, Water System",
        "Volumetric Clouds, Sky Atmosphere, Height Fog",
        "Mesh Painting, Decals, Light Functions, Reflections, SSR, SSAO, Distance Fields",
        "Groom/Hair Rendering, Runtime Virtual Texturing",
        "HLOD, Replication Graph, Network Profiler",
        "Console Commands, Shader Development, Textures",
        "Physics Constraints, Chaos Vehicles",
        "Perforce, Git, Console Development",
        "C++ API Reference, UE 5.4 Release Notes",
        "Asset Pipeline, Editor Extensibility, Profiling, Localization, Crash Reporting",
    ],
}


def get_master_category(name: str) -> dict:
    """Get a specific master knowledge category by name."""
    return _ALL_MASTER_CATEGORIES.get(name, {})


def get_all_master_categories() -> list:
    """Return list of all master category names."""
    return list(_ALL_MASTER_CATEGORIES.keys())


def search_master_knowledge(query: str, max_results: int = 10) -> list:
    """Search all master knowledge categories for a query string."""
    results = []
    query_lower = query.lower()
    for cat_name, cat_data in _ALL_MASTER_CATEGORIES.items():
        _search_recursive(cat_data, cat_name, query_lower, results, "")
    results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
    return results[:max_results]


def _search_recursive(data, cat_name, query, results, path):
    """Recursively search knowledge data for matching terms."""
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if query in key.lower():
                snippet = str(value)[:200] if not isinstance(value, (dict, list)) else str(value)[:200]
                results.append({
                    "category": cat_name,
                    "key": new_path,
                    "snippet": snippet,
                    "relevance": 2.0 if query == key.lower() else 1.0,
                })
            _search_recursive(value, cat_name, query, results, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, str) and query in item.lower():
                results.append({
                    "category": cat_name,
                    "key": f"{path}[{i}]",
                    "snippet": item,
                    "relevance": 1.0,
                })
            elif isinstance(item, dict):
                _search_recursive(item, cat_name, query, results, f"{path}[{i}]")


def get_landscape_preset(preset_name: str) -> dict:
    """Get landscape configuration presets."""
    presets = {
        "flat_plains": {
            "description": "Flat terrain for open fields and plains",
            "resolution": "1009x1009",
            "components": "1x1",
            "layers": ["grass", "dirt"],
        },
        "rolling_hills": {
            "description": "Gentle rolling terrain",
            "resolution": "1009x1009",
            "components": "2x2",
            "layers": ["grass", "dirt", "rock"],
        },
        "mountains": {
            "description": "Dramatic mountain terrain",
            "resolution": "2017x2017",
            "components": "4x4",
            "layers": ["grass", "dirt", "rock", "snow"],
        },
        "coastal": {
            "description": "Coastal terrain with water meeting land",
            "resolution": "1009x1009",
            "components": "2x2",
            "layers": ["sand", "grass", "rock"],
        },
    }
    return presets.get(preset_name, {"error": f"Preset '{preset_name}' not found. Available: {list(presets.keys())}"})


def get_reflection_recommendation(surface_type: str) -> dict:
    """Get reflection method recommendation for a surface type."""
    recommendations = {
        "water": {"method": "Lumen + Planar Reflection", "roughness": 0.0, "note": "Use Planar Reflection for perfect mirror water"},
        "mirror": {"method": "Planar Reflection", "roughness": 0.0, "note": "Only planar reflections give perfect mirror"},
        "metal_polished": {"method": "Lumen Reflections", "roughness": 0.1, "note": "Lumen handles smooth metal well"},
        "metal_brushed": {"method": "Lumen Reflections", "roughness": 0.3, "note": "Rougher metal doesn't need planar"},
        "glass": {"method": "Lumen Reflections", "roughness": 0.05, "note": "Low roughness glass with Lumen"},
        "floor_marble": {"method": "Lumen + Planar Reflection", "roughness": 0.1, "note": "Highly reflective floor benefits from planar"},
        "concrete": {"method": "Reflection Captures", "roughness": 0.9, "note": "Rough surfaces only need basic cube captures"},
        "wood": {"method": "Reflection Captures", "roughness": 0.7, "note": "Wood is diffuse enough for basic captures"},
    }
    return recommendations.get(surface_type, {"method": "Lumen Reflections", "roughness": 0.5, "note": "Lumen works for most surfaces"})