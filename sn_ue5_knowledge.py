"""
SuperNinja UE5 Knowledge Base — Extracted from Official UE5 Training Corpus
20 Documents covering: Engine Architecture, Editor, Blueprints, C++, and Coding Standards

This module gives SuperNinja deep understanding of HOW Unreal Engine works,
not just what commands to send. It knows the class hierarchy, naming conventions,
Blueprint patterns, C++ interop, and editor workflows.
"""

# =============================================================================
# SECTION 1: UE5 CLASS HIERARCHY & ARCHITECTURE
# =============================================================================

UE5_CLASS_HIERARCHY = {
    "UObject": {
        "description": "Base class for all Unreal objects. Provides garbage collection, reflection, serialization, and automatic editor integration.",
        "benefits": [
            "Garbage Collection — Automatic memory management",
            "Reference Updating — Pointers auto-update when objects are destroyed",
            "Reflection — Runtime introspection of class members",
            "Serialization — Automatic saving/loading",
            "Editor Integration — Exposed to editor and Blueprints automatically",
            "Network Replication — Properties can replicate across network",
        ],
        "children": {
            "AActor": {
                "description": "Spawnable in world. Everything placed in a level is an Actor.",
                "children": {
                    "APawn": {
                        "description": "Can be possessed by a Controller. Has Collision, Movement, and Mesh components.",
                        "children": {
                            "ACharacter": {
                                "description": "Pawn subclass with CharacterMovementComponent, SkeletalMeshComponent, and CapsuleComponent.",
                            }
                        },
                    },
                    "AController": {
                        "description": "Non-physical. Directs Pawns to perform actions.",
                        "children": {
                            "APlayerController": "Processes human input, displays HUD, possesses Pawns.",
                            "AAIController": "Dictates actions using Behavior Trees, State Trees, Navigation.",
                        },
                    },
                    "AGameModeBase": "Server-based manager. Instantiated on level load. Sets rules and creates framework actors.",
                    "AGameStateBase": "Non-physical. Replicates game state (scores, objectives, player list) to all clients.",
                    "AHUD": "Handles heads-up display rendering.",
                },
            },
            "UActorComponent": {
                "description": "Base component. No transform.",
                "children": {
                    "USceneComponent": {
                        "description": "Has a transform (position, rotation, scale). Can be attached to other SceneComponents.",
                        "children": {
                            "UPrimitiveComponent": {
                                "description": "Visual representation. Renders in the world.",
                                "children": {
                                    "UStaticMeshComponent": "Renders a static mesh. Most common visual component.",
                                    "USkeletalMeshComponent": "Renders an animated skeletal mesh.",
                                },
                            },
                            "UCameraComponent": "Represents a camera viewpoint.",
                        },
                    },
                    "UInputComponent": "Binds input events to actions and axes.",
                },
            },
            "UStruct": "Value type. Not garbage collected. Used for FVector, FRotator, FTransform, etc.",
        },
    }
}

# =============================================================================
# SECTION 2: GAMEPLAY FRAMEWORK — HOW A GAME IS STRUCTURED
# =============================================================================

GAMEPLAY_FRAMEWORK = {
    "game_instance": {
        "class": "UGameInstance",
        "lifecycle": "Created on engine launch, destroyed on engine shutdown",
        "purpose": "Persistent manager across level loads. Track data, run code, manage subsystems.",
        "key_points": [
            "Not replicated — exists independently on server and all clients",
            "Anything persisting between level loads goes here",
            "Good place for save game systems",
            "Manages game instance subsystems",
        ],
    },
    "game_mode": {
        "class": "AGameModeBase",
        "lifecycle": "Instantiated after level load. Not persistent across levels.",
        "purpose": "Server-based manager for rules and session structure.",
        "key_points": [
            "First actor to instantiate on level load",
            "Can be set per-map",
            "Manages overall rules of a gameplay session",
            "Instantiates remaining framework actors upon creation",
        ],
    },
    "game_state": {
        "class": "AGameStateBase",
        "lifecycle": "Created by GameMode. Persists for duration of game session.",
        "purpose": "Non-physical actor tracking the state of the game.",
        "key_points": [
            "Replicates state information between server and all clients",
            "Contains: team scores, objectives, list of all players and their states",
        ],
    },
    "player_state": {
        "class": "APlayerState",
        "lifecycle": "Created when player joins or enters a level.",
        "purpose": "Non-physical actor tracking individual player state.",
        "key_points": [
            "Replicates between server and clients",
            "Contains: health, ammo, inventory",
        ],
    },
    "player_controller": {
        "class": "APlayerController",
        "purpose": "Processes human input, displays HUD, possesses Pawns.",
        "key_points": ["Non-physical — no manifestation in the game world"],
    },
    "ai_controller": {
        "class": "AAIController",
        "purpose": "Controls AI using Behavior Trees, State Trees, Navigation.",
        "key_points": ["Non-physical — possesses Pawns to direct them"],
    },
}

# =============================================================================
# SECTION 3: NAMING CONVENTIONS (from Epic Coding Standard)
# =============================================================================

UE5_NAMING_CONVENTIONS = {
    "class_prefixes": {
        "A": "Actor classes (AActor, APawn, ACharacter)",
        "U": "UObject-derived classes (UActorComponent, USceneComponent)",
        "F": "Structs and non-UObject classes (FVector, FRotator, FTransform)",
        "E": "Enums (EVisibility, ECollisionChannel)",
        "T": "Templates (TArray, TMap, TSet)",
        "S": "Slate widget classes (SButton, SSlider)",
        "I": "Interface classes (IInteractable)",
    },
    "variable_rules": {
        "naming": "PascalCase, no underscores between words (Health, MovementSpeed)",
        "booleans": "Prefix with b (bIsAlive, bHasWeapon, bCanJump)",
        "scope": "Larger scope = more descriptive name. Avoid over-abbreviation.",
        "declaration": "One variable per line for commenting",
    },
    "function_rules": {
        "booleans": "Ask true/false question: IsVisible(), ShouldClearBuffer(), HasAmmo()",
        "procedures": "Strong verbs: RemoveItem(), ClearList(), SpawnActor()",
        "avoid": "Don't start with 'Handle' or 'Process' — too ambiguous",
    },
    "file_rules": {
        "naming": "No prefixes in filenames (Scene.cpp, not UnScene.cpp)",
        "headers": "Use #pragma once after copyright notice",
        "includes": "Include as specifically as possible. Use forward declarations.",
    },
    "bp_variable_naming": {
        "variables": "Use nouns (PlayerHealth, MovementSpeed)",
        "functions": "Use verbs (TakeDamage, OpenDoor)",
        "booleans": "Prefix with Is/Has/Can (IsAlive, HasKey, CanFire)",
        "events": "Descriptive phrases (OnHealthChanged, OnDoorOpened)",
    },
}

# =============================================================================
# SECTION 4: EDITOR INTERFACE KNOWLEDGE
# =============================================================================

UE5_EDITOR_INTERFACE = {
    "main_toolbar": {
        "save": "Save current level",
        "modes": {
            "select": "Default selection and transformation",
            "landscape": "Terrain editing",
            "foliage": "Paint vegetation",
            "mesh_paint": "Paint on meshes",
            "fracture": "Geometry destruction",
            "brush_editing": "CSG brush editing",
        },
        "play_controls": {
            "play": "Launch game in viewport",
            "skip": "Skip to next sequence",
            "stop": "Stop play session",
            "eject": "Detach camera from player",
        },
    },
    "level_viewport": {
        "perspective": "3D view from any angle",
        "orthographic": "2D view along axes: Top, Front, Side",
        "focusing": "Press F to focus on selected actor",
    },
    "outliner": {
        "description": "Hierarchical view of everything in the level",
        "features": [
            "Up to 4 Outliner panels simultaneously",
            "Eye icon to hide/show actors",
            "Right-click for context menu",
            "Organize actors into folders",
            "Attach/detach parent-child relationships",
            "Lock actors to prevent accidental selection",
        ],
    },
    "details_panel": {
        "description": "Properties for selected actor. Context-sensitive.",
        "common_properties": [
            "Transform — Position, Rotation, Scale",
            "Static Mesh — Mesh asset reference",
            "Materials — Material assignments",
            "Physics — Collision and physics settings",
            "Rendering — Visibility, shadows, LOD settings",
            "Lighting — Lightmap resolution, mobility",
            "Tags — Actor identification tags",
        ],
        "features": [
            "Property search/filter",
            "Property copying/pasting",
            "Multiple actor selection support",
            "Category collapse/expand",
            "Favorites for frequently-changed properties",
        ],
    },
    "content_browser": {
        "description": "Primary area for creating, importing, organizing, viewing, and managing assets",
        "access": [
            "Window menu in top menu bar",
            "Create menu on Main Toolbar",
            "Content Drawer button on bottom toolbar (Ctrl+Space)",
        ],
        "capabilities": [
            "Browse all project assets",
            "Drag assets into levels",
            "Migrate assets between projects",
            "Create, organize, and manage folders",
            "Advanced search syntax with filters",
            "Up to 4 instances simultaneously",
        ],
    },
    "specialized_editors": [
        "Blueprint Editor", "Material Editor", "Niagara Editor",
        "Skeletal Mesh Editor", "Animation Editor", "Physics Asset Editor",
        "Static Mesh Editor", "Sound Cue Editor", "Level Sequence Editor",
        "Behavior Tree Editor", "Environment Query Editor", "UMG UI Editor",
    ],
    "project_settings": {
        "access": "Edit > Project Settings",
        "storage": "INI files (DefaultEngine.ini, DefaultGame.ini, DefaultInput.ini)",
        "categories": {
            "project": "Name, company, homepage, copyright, licensing, description",
            "game": "Default GameMode, Pawn, PlayerController, HUD, GameState, PlayerState, Default Maps, Input mappings",
            "engine": "Collision presets, Rendering, Navigation mesh, Network replication",
            "editor": "Undo buffer, Blueprint debugging, Source control integration",
            "platforms": "Platform-specific settings for Windows, macOS, Linux, iOS, Android, consoles",
            "plugins": "Plugin-specific configuration options",
        },
    },
}

# =============================================================================
# SECTION 5: BLUEPRINT SYSTEM KNOWLEDGE
# =============================================================================

BLUEPRINT_SYSTEM = {
    "overview": "Complete gameplay scripting system using node-based interface. Defines object-oriented classes in the engine.",
    "types": {
        "blueprint_class": {
            "editor": "Full Blueprint Editor with Viewport, Components, My Blueprint, Graph, Details, Toolbar",
            "has_construction_script": True,
            "description": "Standard Blueprint that can be placed in the world as an Actor",
        },
        "level_blueprint": {
            "editor": "Simplified editor — no Viewport or Components panel",
            "has_construction_script": False,
            "description": "Level-specific scripting. Only one per level.",
        },
        "blueprint_interface": {
            "editor": "Simplified — only function signatures, no implementation",
            "description": "Contract: 'If you implement this, you promise to implement these functions'",
        },
        "macro_library": {
            "editor": "Specialized for creating reusable macro graphs",
            "description": "Reusable graph snippets usable across Blueprints",
        },
        "animation_blueprint": {
            "editor": "Specialized editor integrated with Animation system",
            "description": "Controls skeletal mesh animation logic",
        },
    },
    "communication_methods": {
        "direct_communication": {
            "relationship": "One-to-one",
            "best_for": "Two Actors in level that need to talk to each other",
            "requires": "Reference variable to target Actor (set as Editable)",
            "how_to": "Create reference variable → Set type to target Blueprint → Expose as Editable → Assign in Level Editor → Drag getter into graph → Access functions/variables",
        },
        "event_dispatchers": {
            "relationship": "One-to-many",
            "best_for": "Broadcasting events to multiple listeners",
            "requires": "Event Dispatcher in sender, Bind Event in receivers",
            "example": "Boss calls OnDied → Character celebrates, Door opens, HUD flashes message",
            "how_to": "Create Dispatcher in sender → Call it on event → In receivers, Bind to it → Implement response",
        },
        "blueprint_interfaces": {
            "relationship": "Many-to-many",
            "best_for": "Common functionality across different Blueprint types",
            "requires": "Interface asset, implementation on each Blueprint",
            "example": "Flamethrower uses ElementalDamage → Tree burns, Snowman melts (different reactions)",
            "how_to": "Create Interface → Add functions → Implement on target BPs → Call Interface Message from trigger BP",
        },
        "blueprint_casting": {
            "relationship": "One-to-one with type checking",
            "best_for": "Accessing specialized versions of Blueprints",
            "requires": "Cast node with proper target type",
            "warning": "Excessive casting creates tight coupling. Use Interfaces or Dispatchers instead.",
        },
    },
    "construction_script": {
        "description": "Runs after Components list when Blueprint instance is created",
        "timing": "Runs in the EDITOR (not just during play)",
        "key_facts": [
            "Only Blueprint Classes have them — Level Blueprints do NOT",
            "Re-runs when properties are changed on the instance",
            "Heavy logic slows down the editor",
        ],
        "use_cases": [
            "Adaptive objects — light changes mesh based on ground type",
            "Procedural placement — fence traces to determine length",
            "Dynamic materials — change based on environment",
            "Procedural generation — spawn components based on parameters",
        ],
    },
    "best_practices": {
        "organization": [
            "Use comments and comment boxes to group related nodes",
            "Align nodes neatly using alignment tools",
            "Use reroute nodes to straighten wires",
            "Break large graphs into functions or macros",
            "Use consistent naming conventions",
        ],
        "performance": [
            "AVOID Event Tick — use timers, events, or timelines instead",
            "If tick is necessary: keep logic simple, use gates/branches to disable when not needed",
            "Use C++ for performance-critical code (AI, physics, complex calculations)",
            "Create dynamic material instances at BeginPlay, not every frame",
            "Use Construction Script wisely — it runs on every move in editor",
            "Use Timelines for time-based operations (lerping, animating, fading)",
            "Use built-in nodes — they're highly optimized",
        ],
        "architecture": [
            "Prefer composition over inheritance (add components, don't create deep hierarchies)",
            "Use Blueprint Interfaces for loose coupling",
            "Use Event Dispatchers for one-to-many communication",
            "Avoid circular dependencies — use Interfaces or Dispatchers",
            "Use Enums instead of multiple booleans for states",
            "Keep variable scope minimal — only expose when necessary",
            "Use local variables in functions when value doesn't need to persist",
        ],
        "debugging": [
            "Print String for quick debugging (remove before shipping!)",
            "Breakpoints: F9 or right-click → Add Breakpoint",
            "Blueprint Debugger: Window > Blueprint Debugger",
            "Watch variables: Click eye icon in My Blueprint panel",
            "Pin value inspection: Hover over pin at breakpoint",
        ],
    },
}

# =============================================================================
# SECTION 6: C++ & BLUEPRINT INTEROP
# =============================================================================

CPP_BLUEPRINT_INTEROP = {
    "core_macros": {
        "UCLASS": {
            "purpose": "Expose a C++ class to the Unreal reflection system",
            "common_specifiers": [
                "Blueprintable — Can be used as parent class for Blueprints",
                "BlueprintType — Can be used as variable type in Blueprints",
            ],
            "example": "UCLASS(Blueprintable, BlueprintType)\nclass MYPROJECT_API UMyClass : public UObject\n{ GENERATED_BODY() };",
        },
        "UPROPERTY": {
            "purpose": "Expose a property to the reflection system and Blueprints",
            "access_specifiers": [
                "EditAnywhere — Edit in defaults AND instances",
                "EditDefaultsOnly — Edit only in Blueprint defaults",
                "EditInstanceOnly — Edit only on placed instances",
                "VisibleAnywhere — Read-only everywhere",
                "VisibleDefaultsOnly — Read-only in defaults",
                "VisibleInstanceOnly — Read-only on instances",
            ],
            "blueprint_specifiers": [
                "BlueprintReadWrite — Get and Set in Blueprints",
                "BlueprintReadOnly — Get only in Blueprints",
            ],
            "example": 'UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="MyCategory")\nfloat MyFloatProperty;',
        },
        "UFUNCTION": {
            "purpose": "Expose a function to the reflection system and Blueprints",
            "specifiers": [
                "BlueprintCallable — Can be called from Blueprints",
                "BlueprintPure — Like Callable but has no execution pin (getter/calculator)",
                "BlueprintImplementableEvent — Implemented in Blueprint, not C++",
                "BlueprintNativeEvent — C++ default implementation, overridable in Blueprint",
            ],
            "examples": {
                "callable": 'UFUNCTION(BlueprintCallable, Category="MyGame|Weapons")\nvoid FireWeapon();',
                "pure": 'UFUNCTION(BlueprintPure, Category="MyGame|Health")\nfloat GetHealthPercent() const;',
                "implementable_event": 'UFUNCTION(BlueprintImplementableEvent, Category="MyGame|Events")\nvoid OnPlayerScored(int32 Points);',
                "native_event": '// Header:\nUFUNCTION(BlueprintNativeEvent, Category="MyGame|Events")\nvoid OnItemCollected();\n// C++ implementation (note _Implementation suffix):\nvoid AMyActor::OnItemCollected_Implementation()\n{ /* default C++ behavior */ }',
            },
        },
    },
    "class_declaration": {
        "syntax": "UCLASS([specifier, specifier, ...], [meta(key=value, ...)])\nclass ClassName : public ParentName\n{ GENERATED_BODY() }",
        "constructor_basics": {
            "simple": "UMyObject::UMyObject() { /* Initialize CDO properties */ }",
            "with_initializer": "UMyObject::UMyObject(const FObjectInitializer& ObjectInitializer)\n    : Super(ObjectInitializer) { /* Init */ }",
        },
        "component_creation": {
            "pattern": "CreateDefaultSubobject<USceneComponent>(TEXT(\"ComponentName\"));",
            "example": """AWindPointSource::AWindPointSource()
{
    WindPointSource = CreateDefaultSubobject<UWindPointSourceComponent>(TEXT("WindPointSourceComponent0"));
    if (RootComponent == nullptr) { RootComponent = WindPointSource; }
    DisplaySphere = CreateDefaultSubobject<UDrawSphereComponent>(TEXT("DrawSphereComponent0"));
    DisplaySphere->AttachTo(RootComponent);
}""",
        },
    },
    "coding_standard": {
        "braces": "Always on new line (Allman style). Always use braces for single-statement blocks.",
        "indentation": "Tabs (4 characters). Spaces only for alignment.",
        "null_pointer": "Use nullptr, never NULL",
        "auto": "Do NOT use auto except: lambda bindings, verbose iterators, template code",
        "range_for": "Prefer range-based for loops",
        "enums": "Always use enum class (strongly-typed). Blueprint-exposed enums must be uint8.",
        "const": "Use const wherever possible. Place at end for pointer-to-const: T* const Ptr",
        "namespaces": "Use UE:: as root namespace. No 'using' in global scope.",
        "default_initializers": "Prefer default member initializers over constructor initialization",
    },
}

# =============================================================================
# SECTION 7: UE5 DIRECTORY STRUCTURE
# =============================================================================

UE5_DIRECTORY_STRUCTURE = {
    "engine": {
        "Binaries/": "Compiled binaries",
        "Build/": "Build scripts and configuration",
        "Config/": "Engine configuration files",
        "Content/": "Engine content assets",
        "Extras/": "Additional tools and utilities",
        "Intermediate/": "Temporary build files",
        "Plugins/": "Engine plugins",
        "Saved/": "Logs, crashes, and user settings",
        "Source/": {
            "Runtime/": "Runtime engine modules",
            "Editor/": "Editor-only modules",
            "Developer/": "Development tools",
        },
        "Templates/": "Project templates",
    },
    "project": {
        "Binaries/": "Compiled game binaries",
        "Config/": {
            "DefaultEngine.ini": "Core engine configuration",
            "DefaultGame.ini": "Game-specific configuration",
            "DefaultInput.ini": "Input bindings and mappings",
            "DefaultEditor.ini": "Editor preferences",
            "[Platform]/": "Platform-specific configs",
        },
        "Content/": {
            "Collections/": "Asset collections",
            "Developers/": "Developer-specific content",
            "Maps/": "Level files",
        },
        "Intermediate/": "Temporary build files",
        "Saved/": {
            "AutoSave/": "Auto-saved levels",
            "Config/": "Local user config overrides",
            "Logs/": "Log files",
            "Screenshots/": "Captured screenshots",
        },
        "Source/": {
            "[ProjectName]/": {
                "[ProjectName].Build.cs": "Build configuration",
                "[ProjectName].Target.cs": "Target configuration",
                "Private/": "Private implementation",
                "Public/": "Public headers",
            },
        },
        "[ProjectName].uproject": "Project descriptor file",
    },
}

# =============================================================================
# SECTION 8: SOURCE CONTROL & OFPA
# =============================================================================

SOURCE_CONTROL_KNOWLEDGE = {
    "ofpa": {
        "name": "One File Per Actor",
        "description": "UE5 stores each actor in a level as a separate file",
        "benefit": "Dramatically reduces merge conflicts when multiple people work on the same level",
    },
    "operations": {
        "check_out": "Right-click asset → Source Control > Check Out",
        "check_in": "Right-click asset → Source Control > Check In → Enter description → Check In",
        "sync": "Click Source Control button → Sync to Latest",
        "revert": "Right-click asset → Source Control > Revert",
    },
    "best_practices": [
        "Check in early, check in often — reduces conflicts",
        "Write meaningful check-in descriptions",
        "Sync before starting work",
        "Avoid checking in broken content",
        "Use exclusive check-out for binary files (they can't be merged)",
        "Organize with clear folder structure",
        "Configure ignore rules for unnecessary files",
    ],
}

# =============================================================================
# SECTION 9: SLATE UI ARCHITECTURE (for understanding editor internals)
# =============================================================================

SLATE_UI_KNOWLEDGE = {
    "description": "Unreal Engine's cross-platform UI framework for editor tools and in-game interfaces",
    "data_flow": {
        "pattern": "Polling data flow with delegates",
        "concept": "UIs visualize and manipulate Models. Slate uses delegates as flexible conduits.",
        "read": "Widgets read Model data when displaying it",
        "write": "Widgets invoke write delegates when users perform actions",
    },
    "layout": {
        "pass_1": "Cache Desired Size — figure out how much space each widget wants (bottom-up)",
        "pass_2": "ArrangeChildren — arrange children within parent's allotted area",
    },
    "key_functions": {
        "ComputeDesiredSize()": "Responsible for desired size",
        "ArrangeChildren()": "Responsible for arrangement of children",
        "OnPaint()": "Responsible for appearance",
        "OnSomething handlers": "Event handlers invoked by Slate at various times",
    },
}

# =============================================================================
# SECTION 10: QUICK REFERENCE — COMMON UE5 PYTHON API PATTERNS
# =============================================================================

UE5_PYTHON_PATTERNS = {
    "actor_operations": {
        "spawn": "actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)",
        "get_all": "actors = unreal.EditorLevelLibrary.get_all_level_actors()",
        "get_by_label": "actor = unreal.EditorLevelLibrary.find_actor_at_location(unreal.Vector(0,0,0), 100)",
        "delete": "unreal.EditorLevelLibrary.destroy_actor(actor)",
        "move": "actor.set_actor_location(unreal.Vector(x, y, z))",
        "rotate": "actor.set_actor_rotation(unreal.Rotator(pitch, yaw, roll))",
        "scale": "actor.set_actor_scale3d(unreal.Vector(sx, sy, sz))",
        "get_label": "name = actor.get_actor_label()",
        "set_label": "actor.set_actor_label('MyActor')",
        "get_transform": "transform = actor.get_actor_transform()",
    },
    "light_operations": {
        "get_light_component": "light_comp = actor.get_component_by_class(unreal.DirectionalLightComponent)",
        "set_intensity": "light_comp.set_intensity(3.0)",
        "set_temperature": "light_comp.set_light_color(unreal.LinearColor(r, g, b))",
        "set_mobility": "light_comp.set_mobility(unreal.ComponentMobility.STATIC)",
        "toggle_shadows": "light_comp.set_cast_shadows(True)",
    },
    "material_operations": {
        "get_material": "mat = mesh_component.get_material(slot_index)",
        "set_material": "mesh_component.set_material(slot_index, material_asset)",
        "create_dynamic": "dyn_mat = unreal.MaterialEditingLibrary.create_material_instance(material)",
    },
    "content_browser": {
        "list_assets": "assets = unreal.EditorAssetLibrary.list_assets('/Game/')",
        "load_asset": "asset = unreal.EditorAssetLibrary.load_asset('/Game/MyAsset')",
        "import_asset": "unreal.ImportAssetUtils.import_assets(file_paths, destination_path)",
    },
    "level_operations": {
        "save": "unreal.EditorLevelLibrary.save_current_level()",
        "get_level_actors": "actors = unreal.EditorLevelLibrary.get_all_level_actors()",
        "get_selected": "selected = unreal.EditorLevelLibrary.get_selected_level_actors()",
        "select": "unreal.EditorLevelLibrary.set_selected_level_actors([actor])",
    },
    "viewport_operations": {
        "screenshot": "unreal.SystemLibrary.execute_console_command(None, 'HighResShot 1')",
        "console_cmd": "unreal.SystemLibrary.execute_console_command(None, 'command')",
    },
    "logging": {
        "info": "unreal.log('[SN] Message')",
        "warning": "unreal.log_warning('[SN] Warning')",
        "error": "unreal.log_error('[SN] Error')",
    },
}

# =============================================================================
# SECTION 11: UE5 CONCEPTS SUPERNOVA SHOULD KNOW
# =============================================================================

UE5_KEY_CONCEPTS = {
    "actors": "Objects that can be placed in levels. EVERYTHING in a level is an Actor.",
    "components": "Reusable pieces of functionality added to Actors. The building blocks of Actor behavior.",
    "pawns": "Actors that can be possessed by Controllers. Have collision, movement, and mesh components.",
    "characters": "Pawn subclass with advanced movement (CharacterMovementComponent), skeletal mesh, and capsule collision.",
    "game_mode": "Server-side rules manager. Created per-level. Defines how the game session works.",
    "game_state": "Replicated game state. Team scores, objectives, player list. Everyone sees the same state.",
    "player_state": "Per-player state. Health, ammo, inventory. Replicates to all clients.",
    "controllers": "Non-physical directors. PlayerController for humans, AIController for AI. They possess Pawns.",
    "construction_script": "Runs in the EDITOR when Actor is placed/modified. Use for procedural setup. Heavy logic = slow editor.",
    "event_tick": "FIRES EVERY FRAME. Avoid for performance. Use timers, events, timelines instead.",
    "blueprint_interfaces": "Contracts — 'implement these functions'. Enables loose coupling between Blueprints.",
    "event_dispatchers": "One-to-many communication. Sender broadcasts, all bound receivers react independently.",
    "ofpa": "One File Per Actor — each actor saved separately. Reduces merge conflicts in team workflows.",
    "lumen": "UE5's dynamic global illumination system. No lightmaps needed for dynamic scenes.",
    "nanite": "UE5's virtualized geometry system. Automatically handles mesh LOD. Use for high-poly meshes.",
    "uproperty": "C++ macro that exposes properties to reflection, serialization, Blueprints, and the editor.",
    "ufunction": "C++ macro that exposes functions to reflection, Blueprints, and the console.",
    "uclass": "C++ macro that registers a class with the Unreal reflection system.",
}

# =============================================================================
# EXPORT HELPER — Get knowledge by category
# =============================================================================

def get_knowledge(category: str) -> dict:
    """Get a specific knowledge category."""
    categories = {
        "class_hierarchy": UE5_CLASS_HIERARCHY,
        "gameplay_framework": GAMEPLAY_FRAMEWORK,
        "naming_conventions": UE5_NAMING_CONVENTIONS,
        "editor_interface": UE5_EDITOR_INTERFACE,
        "blueprint_system": BLUEPRINT_SYSTEM,
        "cpp_interop": CPP_BLUEPRINT_INTEROP,
        "directory_structure": UE5_DIRECTORY_STRUCTURE,
        "source_control": SOURCE_CONTROL_KNOWLEDGE,
        "slate_ui": SLATE_UI_KNOWLEDGE,
        "python_patterns": UE5_PYTHON_PATTERNS,
        "key_concepts": UE5_KEY_CONCEPTS,
    }
    return categories.get(category, {})

def get_all_categories() -> list:
    """List all available knowledge categories."""
    return [
        "class_hierarchy", "gameplay_framework", "naming_conventions",
        "editor_interface", "blueprint_system", "cpp_interop",
        "directory_structure", "source_control", "slate_ui",
        "python_patterns", "key_concepts",
    ]

def search_knowledge(query: str) -> dict:
    """Search all knowledge categories for a term. Returns matching entries."""
    query_lower = query.lower()
    results = {}
    
    all_data = {
        "class_hierarchy": UE5_CLASS_HIERARCHY,
        "gameplay_framework": GAMEPLAY_FRAMEWORK,
        "naming_conventions": UE5_NAMING_CONVENTIONS,
        "editor_interface": UE5_EDITOR_INTERFACE,
        "blueprint_system": BLUEPRINT_SYSTEM,
        "cpp_interop": CPP_BLUEPRINT_INTEROP,
        "directory_structure": UE5_DIRECTORY_STRUCTURE,
        "source_control": SOURCE_CONTROL_KNOWLEDGE,
        "slate_ui": SLATE_UI_KNOWLEDGE,
        "python_patterns": UE5_PYTHON_PATTERNS,
        "key_concepts": UE5_KEY_CONCEPTS,
    }
    
    def _search_recursive(data, path=""):
        matches = []
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                if query_lower in str(key).lower():
                    matches.append({"path": current_path, "key": key, "value": value})
                matches.extend(_search_recursive(value, current_path))
        elif isinstance(data, (list, str)):
            if query_lower in str(data).lower():
                matches.append({"path": path, "value": data})
        return matches
    
    for category, data in all_data.items():
        matches = _search_recursive(data, category)
        if matches:
            results[category] = matches
    
    return results


if __name__ == "__main__":
    print("=== SuperNinja UE5 Knowledge Base ===")
    print(f"Categories: {len(get_all_categories())}")
    for cat in get_all_categories():
        print(f"  - {cat}")
    
    print("\n=== Search Test: 'pawn' ===")
    results = search_knowledge("pawn")
    for cat, matches in results.items():
        print(f"\n[{cat}]")
        for m in matches[:3]:
            print(f"  {m['path']}")
    
    print("\n=== Search Test: 'blueprint' ===")
    results = search_knowledge("blueprint")
    print(f"Found in {len(results)} categories")