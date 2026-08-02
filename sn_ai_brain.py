"""
SuperNinja AI Brain — Phase 3

The autonomous decision engine that:
1. SEES — Captures screenshot, analyzes scene data
2. THINKS — Interprets what's in the scene, what's missing, what needs fixing
3. PLANS — Selects the right skills and sequences them
4. ACTS — Enqueues commands through the cloud endpoint
5. VERIFIES — Takes another screenshot to confirm changes

This runs on the SuperNinja cloud side and communicates
with Unreal through the command pipeline.

Usage:
    from sn_ai_brain import SuperNinjaBrain
    brain = SuperNinjaBrain(cloud_url="https://your-tunnel.trycloudflare.com")
    brain.analyze_scene()
    brain.light_scene(style="cinematic")
    brain.cleanup_duplicates(prefix="PHX_")
"""

import json
import time
import base64
import requests
from typing import Optional, Dict, List, Any

from sn_intelligent_brain import IntelligentBrain

class SuperNinjaBrain:
    """AI decision engine for Unreal Editor control, powered by UE5 knowledge."""

    def __init__(self, cloud_url: str):
        self.cloud_url = cloud_url.rstrip("/")
        self.history = []  # Track all actions taken
        self.scene_state = {}  # Current understanding of the scene
        self.last_screenshot_id = None
        self._last_scene = {}  # Cached scene data for analysis methods
        self.intelligent = IntelligentBrain()  # UE5 knowledge-powered reasoning

    # ------------------------------------------------------------------
    # LOW-LEVEL: Cloud API communication
    # ------------------------------------------------------------------
    def _enqueue(self, skill: str, args: dict = None, cmd_id: str = None) -> str:
        """Enqueue a command and return its ID."""
        if cmd_id is None:
            cmd_id = f"sn-{int(time.time()*1000)}"
        payload = {
            "id": cmd_id,
            "command": skill,
            "args": args or {},
        }
        resp = requests.post(f"{self.cloud_url}/enqueue", json=payload, timeout=15)
        data = resp.json()
        if data.get("status") == "enqueued":
            self.history.append({"id": cmd_id, "skill": skill, "args": args, "enqueued_at": time.time()})
            return cmd_id
        else:
            raise Exception(f"Enqueue failed: {data}")

    def _get_result(self, cmd_id: str, timeout: float = 30.0) -> dict:
        """Wait for and retrieve a command result."""
        start = time.time()
        while time.time() - start < timeout:
            resp = requests.get(f"{self.cloud_url}/result", params={"id": cmd_id}, timeout=10)
            data = resp.json()
            if "result" in data:
                return data["result"]
            time.sleep(1.0)
        raise TimeoutError(f"Result not received for {cmd_id} within {timeout}s")

    def _get_screenshot(self, cmd_id: str, timeout: float = 30.0) -> Optional[dict]:
        """Retrieve a screenshot by command ID."""
        start = time.time()
        while time.time() - start < timeout:
            resp = requests.get(f"{self.cloud_url}/screenshot", params={"id": cmd_id}, timeout=10)
            data = resp.json()
            if "screenshot" in data:
                return data["screenshot"]
            time.sleep(1.0)
        return None

    def _enqueue_and_wait(self, skill: str, args: dict = None, timeout: float = 30.0) -> dict:
        """Enqueue a command and wait for the result."""
        cmd_id = self._enqueue(skill, args)
        return self._get_result(cmd_id, timeout)

    # ------------------------------------------------------------------
    # SEE: Scene observation
    # ------------------------------------------------------------------
    def take_screenshot(self, filename: str = None) -> Optional[str]:
        """Capture the Unreal viewport. Returns the screenshot command ID."""
        args = {}
        if filename:
            args["filename"] = filename
        cmd_id = self._enqueue("screenshot", args)
        self.last_screenshot_id = cmd_id
        return cmd_id

    def get_screenshot_image(self, cmd_id: str = None) -> Optional[bytes]:
        """Get the raw PNG bytes of a screenshot."""
        if cmd_id is None:
            cmd_id = self.last_screenshot_id
        if cmd_id is None:
            return None

        # Wait for screenshot to be uploaded
        shot = self._get_screenshot(cmd_id, timeout=45.0)
        if shot and "data_b64" in shot:
            return base64.b64decode(shot["data_b64"])
        return None

    def analyze_scene(self) -> dict:
        """Get a complete analysis of the current scene."""
        result = self._enqueue_and_wait("get_scene_info")
        self.scene_state = result
        return result

    def list_actors(self, filter_type: str = "", filter_name: str = "") -> list:
        """List actors in the scene."""
        args = {"filter_type": filter_type, "filter_name": filter_name, "include_transform": True}
        result = self._enqueue_and_wait("list_actors", args, timeout=30.0)
        return result

    def list_assets(self, path: str = "/Game/", filter_type: str = "") -> list:
        """List assets in the content browser."""
        args = {"path": path, "filter_type": filter_type}
        result = self._enqueue_and_wait("list_content", args, timeout=30.0)
        return result

    # ------------------------------------------------------------------
    # ACT: Scene modification skills
    # ------------------------------------------------------------------
    def add_sun(self, intensity: float = 3.0, angle: list = None,
                color_temp: float = 6500.0, shadows: bool = True) -> str:
        """Add a directional light (sun) to the scene."""
        args = {
            "intensity": intensity,
            "temperature": color_temp,
            "shadow_enabled": shadows,
        }
        if angle:
            args["rotation"] = angle
        return self._enqueue("add_directional_light", args)

    def add_point_light(self, location: list, intensity: float = 3000.0,
                        color: list = None, radius: float = 1000.0) -> str:
        """Add a point light at a location."""
        args = {
            "location": location,
            "intensity": intensity,
            "attenuation_radius": radius,
        }
        if color:
            args["light_color"] = color
        return self._enqueue("add_point_light", args)

    def add_spot_light(self, location: list, rotation: list = None,
                       intensity: float = 5000.0, inner_cone: float = 15.0,
                       outer_cone: float = 45.0) -> str:
        """Add a spot light."""
        args = {
            "location": location,
            "intensity": intensity,
            "inner_cone_angle": inner_cone,
            "outer_cone_angle": outer_cone,
        }
        if rotation:
            args["rotation"] = rotation
        return self._enqueue("add_spot_light", args)

    def add_sky_light(self, intensity: float = 1.0) -> str:
        """Add a sky light for ambient illumination."""
        return self._enqueue("add_sky_light", {"intensity": intensity})

    def add_fog(self, density: float = 0.02, color: list = None,
                height_falloff: float = 0.2) -> str:
        """Add exponential height fog."""
        args = {"fog_density": density, "fog_height_falloff": height_falloff}
        if color:
            args["fog_color"] = color
        return self._enqueue("add_exponential_height_fog", args)

    def add_sky_atmosphere(self) -> str:
        """Add sky atmosphere."""
        return self._enqueue("add_sky_atmosphere")

    def spawn_shape(self, shape: str = "Cube", location: list = None,
                    scale: list = None, name: str = None) -> str:
        """Spawn a basic shape."""
        args = {"shape": shape}
        if location:
            args["location"] = location
        if scale:
            args["scale"] = scale
        if name:
            args["name"] = name
        return self._enqueue("spawn_actor", args)

    def move_actor(self, name: str, location: list, relative: bool = False) -> str:
        """Move an actor."""
        return self._enqueue("move_actor", {"actor_name": name, "location": location, "relative": relative})

    def rotate_actor(self, name: str, rotation: list) -> str:
        """Rotate an actor."""
        return self._enqueue("rotate_actor", {"actor_name": name, "rotation": rotation})

    def scale_actor(self, name: str, scale: list, uniform: bool = True) -> str:
        """Scale an actor."""
        return self._enqueue("scale_actor", {"actor_name": name, "scale": scale, "uniform": uniform})

    def delete_actor(self, name: str) -> str:
        """Delete an actor. Requires confirmation."""
        return self._enqueue("delete_actor", {"actor_name": name, "confirm": True})

    def apply_material(self, actor_name: str, material_path: str, slot: int = 0) -> str:
        """Apply a material to an actor."""
        return self._enqueue("apply_material", {
            "actor_name": actor_name, "material_path": material_path, "material_slot": slot
        })

    def frame_camera(self, location: list = None, distance: float = 1000.0,
                     pitch: float = -30.0, yaw: float = 45.0,
                     actor_name: str = "") -> str:
        """Frame the viewport camera."""
        args = {"distance": distance, "pitch": pitch, "yaw": yaw}
        if location:
            args["location"] = location
        if actor_name:
            args["actor_name"] = actor_name
        return self._enqueue("frame_viewport", args)

    def save_level(self) -> str:
        """Save the current level."""
        return self._enqueue("save_level")

    def undo(self) -> str:
        """Undo the last action."""
        return self._enqueue("undo")

    # ------------------------------------------------------------------
    # CONVERSATIONAL: Talk to the user through Unreal
    # ------------------------------------------------------------------
    def say(self, message: str, style: str = "info") -> str:
        """Say something to the user in Unreal's Output Log."""
        return self._enqueue("say", {"message": message, "style": style})

    def ask(self, question: str, options: list = None, context: str = "") -> str:
        """Ask the user a question. Response comes back as a new command."""
        args = {"question": question, "context": context}
        if options:
            args["options"] = options
        return self._enqueue("ask_user", args)

    def report_progress(self, action: str, step: int = 0, total: int = 0, status: str = "working") -> str:
        """Report what you're doing to the user."""
        return self._enqueue("report_progress", {
            "action": action, "step": step, "total_steps": total, "status": status
        })

    def explain_scene(self, analysis: str = "") -> str:
        """Explain your understanding of the scene to the user."""
        return self._enqueue("explain_scene", {"analysis": analysis})

    def suggest_improvements(self, focus: str = "general") -> str:
        """Suggest what could make the scene look better."""
        return self._enqueue("suggest_improvements", {"focus": focus})

    def chat(self, text: str, mood: str = "friendly") -> str:
        """Send a conversational message with a mood/tone."""
        return self._enqueue("chat", {"text": text, "mood": mood})

    # ------------------------------------------------------------------
    # KNOWLEDGE: UE5 knowledge queries (powered by training corpus)
    # ------------------------------------------------------------------
    def query_knowledge(self, query: str, category: str = "") -> dict:
        """Search the UE5 knowledge base for information."""
        # Use the intelligent brain locally for the answer
        local_result = self.intelligent.query_ue5_knowledge(query)
        # Also enqueue the command so Unreal logs it
        self._enqueue("query_knowledge", {"query": query, "category": category})
        return local_result

    def explain_ue5_concept(self, concept: str) -> str:
        """Explain a UE5 concept using the training corpus knowledge."""
        explanation = self.intelligent.explain_ue5_concept(concept)
        self._enqueue("explain_ue5_concept", {"concept": concept})
        return explanation

    def suggest_blueprint_pattern(self, use_case: str) -> dict:
        """Suggest the right Blueprint communication pattern for a use case."""
        suggestion = self.intelligent.suggest_blueprint_pattern(use_case)
        self._enqueue("suggest_blueprint_pattern", {"use_case": use_case})
        return suggestion

    def get_actor_properties(self, name: str, include_components: bool = True,
                             include_materials: bool = True) -> str:
        """Get detailed properties of an actor."""
        return self._enqueue("get_actor_properties", {
            "name": name,
            "include_components": include_components,
            "include_materials": include_materials,
        })

    def set_actor_property(self, name: str, property_name: str, value: str) -> str:
        """Set a specific property on an actor."""
        return self._enqueue("set_actor_property", {
            "name": name,
            "property": property_name,
            "value": value,
        })

    def find_actors_advanced(self, filter_class: str = "", filter_tag: str = "",
                             filter_mobility: str = "", filter_material: str = "",
                             spatial_center: str = "", spatial_radius: float = 1000.0,
                             max_results: int = 50) -> str:
        """Advanced actor search with multiple filters."""
        return self._enqueue("find_actors_advanced", {
            "filter_class": filter_class,
            "filter_tag": filter_tag,
            "filter_mobility": filter_mobility,
            "filter_material": filter_material,
            "spatial_center": spatial_center,
            "spatial_radius": spatial_radius,
            "max_results": max_results,
        })

    def run_python(self, code: str, description: str = "") -> str:
        """Execute a Python snippet inside Unreal Editor. Use with caution."""
        return self._enqueue("run_python_snippet", {
            "code": code,
            "description": description,
        })

    # ------------------------------------------------------------------
    # ADVANCED: Knowledge from Docs 21-60 (Lighting, Materials, Rendering, etc.)
    # ------------------------------------------------------------------
    def query_advanced(self, query: str) -> dict:
        """Search the advanced UE5 knowledge base (Docs 21-60: Lumen, Materials, etc.)."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.query_advanced_knowledge(query)

    def get_lighting_setup(self, scene_type: str, mood: str = None) -> dict:
        """Get a complete lighting setup recommendation for a scene type and mood.
        
        Scene types: outdoor_day, outdoor_golden_hour, interior_office, night_exterior
        Moods: moody, dramatic, cheerful, horror, cinematic
        """
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.get_lighting_setup(scene_type, mood)

    def get_surface_recipe(self, surface_type: str) -> dict:
        """Get PBR material recipe for a surface type.
        
        Types: concrete, metal_brushed, wood, glass, plastic, skin, fabric, car_paint, marble, foliage
        """
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.get_surface_recipe(surface_type)

    def advanced_analysis(self, goal: str = None) -> dict:
        """Run advanced analysis on current scene using Docs 21-60 knowledge.
        Covers: Lumen, shadows, materials, rendering, Nanite, level design."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.get_advanced_scene_analysis(scene_data, goal)

    def query_expert(self, query: str) -> dict:
        """Search the expert UE5 knowledge base (Docs 61-100: Niagara, Audio, UI, AI, Networking, Optimization, Cinematics)."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.query_expert_knowledge(query)

    def expert_analysis(self, goal: str = None) -> dict:
        """Run expert analysis on current scene using Docs 61-100 knowledge.
        Covers: Niagara VFX, audio, UI, AI systems, networking, optimization, cinematics."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.get_expert_scene_analysis(scene_data, goal)

    def get_fps_profile(self, target_fps: int) -> dict:
        """Get optimization settings for a target FPS.
        
        Targets: 30 (budget), 60 (standard), 120 (high-end)
        Returns Lumen budget, shadow settings, scalability recommendations."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.get_fps_optimization_profile(target_fps)

    def get_multiplayer_pattern(self, pattern_name: str) -> dict:
        """Get networking/multiplayer implementation patterns.
        
        Patterns: replication, rpc, dedicated_server, session_management"""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.get_multiplayer_pattern(pattern_name)

    def analyze_vfx_needs(self, goal: str = None) -> dict:
        """Analyze Niagara VFX needs for current scene.
        Detects fire, smoke, water elements and recommends Niagara Fluids simulations."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_niagara_needs(scene_data, goal)

    def analyze_audio_needs(self, goal: str = None) -> dict:
        """Analyze audio needs for current scene.
        Recommends MetaSounds, spatial audio, and ambient sound setups."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_audio_needs(scene_data, goal)

    def analyze_ai_needs(self, goal: str = None) -> dict:
        """Analyze AI system needs for current scene.
        Checks for characters, NavMesh, Behavior Trees, and EQS."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_ai_needs(scene_data, goal)

    def analyze_optimization(self, goal: str = None) -> dict:
        """Deep optimization analysis for current scene.
        Checks dynamic lights, Nanite, scalability, Lumen budget."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_optimization_needs(scene_data, goal)

    # ======================================================================
    # MASTER KNOWLEDGE (Docs 101-151): VP, Landscape, Volumetrics, etc.
    # ======================================================================

    def query_master(self, query: str) -> dict:
        """Search the master UE5 knowledge base (Docs 101-151: Editor Scripting, Virtual Production, Quixel, Landscape, Volumetrics, Rendering, Groom/VT, Performance, Physics, Source Control, API/Pipeline)."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.query_master_knowledge(query)

    def master_analysis(self, goal: str = None) -> dict:
        """Run master analysis on current scene using Docs 101-151 knowledge.
        Covers: Editor Scripting, Virtual Production, Quixel/Landscape, Volumetrics, Rendering, Groom/VT, Performance, Physics, Source Control."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.get_master_scene_analysis(scene_data)

    def analyze_virtual_production(self, goal: str = None) -> dict:
        """Analyze virtual production needs for current scene.
        Checks for ICVFX, Live Link, MetaHuman, USD, XR setup requirements."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_virtual_production_needs(scene_data)

    def analyze_landscape(self, goal: str = None) -> dict:
        """Analyze Quixel/Landscape needs for current scene.
        Checks for terrain, water bodies, and Megascans integration."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_quixel_landscape_needs(scene_data)

    def analyze_volumetrics(self, goal: str = None) -> dict:
        """Analyze volumetric effects needs for current scene.
        Checks for clouds, sky atmosphere, fog, and atmospheric scattering."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_volumetrics_needs(scene_data)

    def analyze_rendering_master(self, goal: str = None) -> dict:
        """Analyze advanced rendering needs for current scene.
        Checks reflections, decals, light functions, distance fields, SSR/SSAO."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_rendering_master_needs(scene_data)

    def analyze_performance_tools(self, goal: str = None) -> dict:
        """Analyze performance tool needs for current scene.
        Checks HLOD, Replication Graph, profiling requirements."""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        scene_data = self._last_scene or {}
        return brain.analyze_performance_tools_needs(scene_data)

    def get_landscape_preset(self, preset_name: str) -> dict:
        """Get landscape configuration preset.
        Presets: mountain, plains, desert, coastal"""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.get_landscape_preset_recommendation(preset_name)

    def get_reflection_recommendation(self, scenario: str) -> dict:
        """Get reflection method recommendation for a scenario.
        Scenarios: indoor, outdoor, water_surface, mirror, architectural"""
        from sn_intelligent_brain import IntelligentBrain
        brain = self.intelligent
        return brain.get_reflection_setup_recommendation(scenario)

    # ------------------------------------------------------------------
    # HIGH-LEVEL: Intelligent scene building
    # ------------------------------------------------------------------
    def light_scene(self, style: str = "cinematic"):
        """Add a complete lighting setup based on a style preset.

        Styles:
          - "cinematic": Dramatic sun + fill + rim + sky + fog
          - "studio": Clean 3-point lighting + sky light
          - "outdoor": Sun + sky light + atmosphere + fog
          - "moody": Low sun + warm point lights + fog
          - "interior": Multiple point/spot lights + no sun
        """
        style = style.lower()
        cmds = []

        if style == "cinematic":
            # Dramatic golden hour sun
            cmds.append(self.add_sun(intensity=5.0, angle=[-25, 160, 0], color_temp=4500, shadows=True))
            # Cool fill from opposite side
            cmds.append(self.add_directional_light_args(
                intensity=0.8, angle=[-20, -30, 0], color_temp=9000,
                shadows=False, name="SN_Fill"
            ))
            # Sky light
            cmds.append(self.add_sky_light(intensity=0.5))
            # Subtle fog
            cmds.append(self.add_fog(density=0.015, color=[0.7, 0.65, 0.6]))
            # Atmosphere
            cmds.append(self.add_sky_atmosphere())

        elif style == "studio":
            # Key light (main)
            cmds.append(self.add_spot_light(
                location=[-300, 0, 500], rotation=[-45, 0, 0],
                intensity=8000, inner_cone=20, outer_cone=50
            ))
            # Fill light (softer, opposite side)
            cmds.append(self.add_point_light(
                location=[300, 200, 300], intensity=2000,
                color=[0.9, 0.95, 1.0], radius=2000
            ))
            # Rim/back light
            cmds.append(self.add_spot_light(
                location=[0, -400, 400], rotation=[-60, 180, 0],
                intensity=6000, inner_cone=15, outer_cone=40
            ))
            # Ambient
            cmds.append(self.add_sky_light(intensity=0.3))

        elif style == "outdoor":
            cmds.append(self.add_sun(intensity=4.0, angle=[-45, 45, 0], color_temp=5500))
            cmds.append(self.add_sky_light(intensity=1.0))
            cmds.append(self.add_sky_atmosphere())
            cmds.append(self.add_fog(density=0.01, color=[0.75, 0.8, 0.85]))

        elif style == "moody":
            # Low warm sun
            cmds.append(self.add_sun(intensity=2.0, angle=[-10, 200, 0], color_temp=3000))
            # Warm point lights
            cmds.append(self.add_point_light(
                location=[0, 0, 200], intensity=5000,
                color=[1.0, 0.7, 0.3], radius=1500
            ))
            cmds.append(self.add_point_light(
                location=[300, -200, 150], intensity=3000,
                color=[0.9, 0.5, 0.2], radius=800
            ))
            # Thick fog
            cmds.append(self.add_fog(density=0.04, color=[0.4, 0.35, 0.3]))
            cmds.append(self.add_sky_light(intensity=0.2))

        elif style == "interior":
            # Multiple point lights simulating indoor
            cmds.append(self.add_point_light(location=[0, 0, 300], intensity=4000, color=[1.0, 0.9, 0.75], radius=1200))
            cmds.append(self.add_point_light(location=[400, 300, 250], intensity=2000, color=[0.95, 0.9, 0.85], radius=800))
            cmds.append(self.add_point_light(location=[-400, -300, 250], intensity=2000, color=[0.95, 0.9, 0.85], radius=800))
            # Accent spot
            cmds.append(self.add_spot_light(
                location=[0, -500, 400], rotation=[-50, 0, 0],
                intensity=6000, inner_cone=20, outer_cone=45
            ))
            cmds.append(self.add_sky_light(intensity=0.1))

        return cmds

    def add_directional_light_args(self, intensity=3.0, angle=None, color_temp=6500,
                                    shadows=True, name="SN_Sun2"):
        """Helper for light_scene to add a second directional light."""
        args = {
            "intensity": intensity,
            "temperature": color_temp,
            "shadow_enabled": shadows,
            "name": name,
        }
        if angle:
            args["rotation"] = angle
        return self._enqueue("add_directional_light", args)

    def cleanup_duplicates(self, prefix: str = "", dry_run: bool = True) -> str:
        """Find and optionally delete duplicate actors (e.g., PHX_ duplicates)."""
        args = {"prefix": prefix, "dry_run": dry_run, "confirm": not dry_run}
        return self._enqueue("delete_duplicates", args)

    def scatter_props(self, source_name: str, count: int = 10,
                      center: list = None, radius: float = 500.0) -> str:
        """Scatter copies of an actor around a point."""
        args = {
            "source_name": source_name,
            "count": count,
            "radius": radius,
        }
        if center:
            args["center"] = center
        return self._enqueue("scatter_actors", args)

    # ------------------------------------------------------------------
    # AUTONOMY: Full see-think-act loop
    # ------------------------------------------------------------------
    def see_think_act(self, goal: str = None):
        """Run one full autonomous cycle with conversational updates:
        1. GREET: Say hi, explain what we're doing
        2. SEE: Take screenshot + get scene info
        3. THINK: Analyze what's there, explain findings
        4. ACT: Make improvements, narrate each step
        5. VERIFY: Take another screenshot, report results
        """
        print(f"\n{'='*60}")
        print(f"  SuperNinja Autonomous Cycle")
        print(f"  Goal: {goal or 'General scene improvement'}")
        print(f"{'='*60}\n")

        # STEP 0: GREET
        if goal:
            self.chat(f"Hey! I'm going to work on: {goal}. Let me take a look at what we've got...", "excited")
        else:
            self.chat("Hey! Let me take a look at your scene and see what I can improve.", "friendly")

        # STEP 1: SEE
        print("[1/5] SEE — Capturing scene state...")
        self.report_progress("Scanning the scene...", step=1, total=5, status="working")
        self.analyze_scene()
        print(f"  Scene: {self.scene_state}")

        screenshot_id = self.take_screenshot()
        print(f"  Screenshot requested: {screenshot_id}")

        # Explain what we see
        self.explain_scene()

        # STEP 2: THINK
        print("\n[2/5] THINK — Analyzing scene with UE5 knowledge...")
        self.report_progress("Analyzing what needs improvement using UE5 expertise...", step=2, total=5, status="thinking")
        analysis = self._analyze_scene_state(goal)
        print(f"  Analysis: {analysis['summary']}")
        print(f"  Issues: {analysis.get('issues', [])}")

        # Share reasoning with the user — explain WHY we're making each decision
        reasoning = analysis.get("reasoning", [])
        if reasoning:
            for r in reasoning[:3]:  # Top 3 reasons
                self.say(r[:200], "info")

        # Suggest improvements conversationally
        if analysis.get("issues"):
            self.say(f"I found {len(analysis['issues'])} thing(s) I can improve. Here's my plan...", "info")
        else:
            self.chat("Your scene looks pretty good already! But let me see if I can fine-tune anything.", "proud")

        # Share suggestions from the intelligent brain
        for suggestion in analysis.get("suggestions", [])[:2]:
            self.say(f"💡 {suggestion}", "info")

        # STEP 3: PLAN
        print(f"\n[3/5] PLAN — {len(analysis.get('actions', []))} actions planned")
        actions = analysis.get("actions", [])
        self.report_progress(f"Planning {len(actions)} improvements...", step=3, total=5, status="working")

        # STEP 4: ACT
        print(f"\n[4/5] ACT — Executing {len(actions)} actions...")
        for i, action in enumerate(actions):
            skill = action.get("skill")
            args = action.get("args", {})
            print(f"  [{i+1}/{len(actions)}] {skill}: {args}")

            # Narrate each action conversationally
            narration = self._narrate_action(skill, args)
            if narration:
                self.say(narration, "info")

            self.report_progress(f"Step {i+1}/{len(actions)}: {skill}", step=i+1, total=len(actions), status="working")

            cmd_id = self._enqueue(skill, args)
            print(f"      → Enqueued as {cmd_id}")
            time.sleep(0.5)

        # STEP 5: VERIFY
        print(f"\n[5/5] VERIFY — Taking post-action screenshot...")
        self.report_progress("Checking my work...", step=5, total=5, status="working")
        time.sleep(3)
        verify_id = self.take_screenshot()
        print(f"  Verification screenshot: {verify_id}")

        # Wrap up conversationally
        self.chat("Done! I've made the improvements. Want me to take another look or adjust anything?", "proud")

        print(f"\n{'='*60}")
        print(f"  Cycle complete. {len(actions)} actions taken.")
        print(f"{'='*60}\n")

        return {
            "scene_state": self.scene_state,
            "analysis": analysis,
            "screenshot_id": screenshot_id,
            "verify_screenshot_id": verify_id,
            "actions_taken": len(actions),
        }

    def _narrate_action(self, skill: str, args: dict) -> str:
        """Generate a conversational narration for an action, using knowledge-aware descriptions."""
        return self.intelligent.get_narration_for_action(skill, args)

    def _analyze_scene_state(self, goal: str = None) -> dict:
        """Analyze current scene state using the UE5 knowledge-powered engine.
        
        Delegates to IntelligentBrain which understands:
        - UE5 class hierarchy and gameplay framework
        - Lighting design principles and presets
        - Composition rules and camera techniques
        - Blueprint communication patterns
        - Performance best practices
        - Scene hygiene and naming conventions
        """
        scene = self.scene_state
        
        if not scene or "error" in scene:
            # Fall back to basic scene info request
            return {
                "summary": "Could not read scene state",
                "issues": ["No scene data available"],
                "actions": [{"skill": "get_scene_info", "args": {}}],
                "reasoning": ["No scene data available — requesting scene info first"],
            }
        
        # Use the intelligent brain for deep analysis
        result = self.intelligent.analyze_scene(scene, goal)
        
        # Log the reasoning for transparency
        for r in result.get("reasoning", []):
            print(f"  💡 {r[:120]}...")
        
        return result


# ---------------------------------------------------------------------------
# CLI interface for direct testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    cloud_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8791"

    brain = SuperNinjaBrain(cloud_url)

    print("SuperNinja AI Brain — Interactive Mode")
    print(f"Cloud URL: {cloud_url}")
    print(f"Available methods: analyze_scene, light_scene, take_screenshot, etc.")
    print()

    # Quick test
    print("Testing connection...")
    try:
        result = brain.analyze_scene()
        print(f"Scene analysis: {result}")
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure the cloud server and tunnel are running.")