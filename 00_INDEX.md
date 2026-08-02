# AI-INBOX — Dumpster Diving multi-AI research

**Status:** create-inbox **executed** (2026-07-27). Folders + master lists + PROMPTS on disk. Do **not** start Cursor Automation from this folder alone — paste Agent A/B/C/D manually unless you open an Automation later.

## Purpose

Shared drop zone for research agents filling asset and mechanics gaps across all five Dumpster Diving hustles + ForgePlay. Coding agents import only after rows move from NEED → HAVE-candidate → true HAVE.

## Agent map

| Agent | Role | Output folder |
|-------|------|---------------|
| **A** | Skills / feel recipes | `1-skills\` |
| **B** | CC0 assets vs asset master list | `2-assets\` |
| **C** | ForgePlay / GameSpec intel | `3-forgeplay-intel\` |
| **D** | Mechanics / controls / feel systems | `4-mechanics\` |

Non-CC0 / unclear licence finds go in `_quarantine-licence\` (never import until cleared).

## Cadence

**Default: NOT continuous search.** Each Agent A/B/C/D run is **one manual paste session** that fills NEED rows, then **stops**.

**Optional scheduled loop** (only if you open Cursor Automation later): every **30 minutes for 24 hours** (**48 ticks**). Rotate agents per tick: **A → B → C → D → A…** Or focus the agent whose master list has the most NEED. Do **not** invent a daemon — document only; user opts in.

## Master lists & prompts

| File | Path |
|------|------|
| Asset checklist | `C:\Users\steve\Desktop\AI-INBOX\ASSET_MASTER_LIST.md` |
| Mechanics checklist | `C:\Users\steve\Desktop\AI-INBOX\MECHANICS_MASTER_LIST.md` |
| Paste-ready prompts | `C:\Users\steve\Desktop\AI-INBOX\PROMPTS.md` |

## Priority order for research

1. **Shared** systems & world assets (pause, a11y, audio bus, input map; trash/crates; UI font/icons; lot SFX)
2. **Meter Drive-By** NEED (GameSpec lean/brake/health/melee; guard AI variety; smash combo; guard mesh; CC0 cars)
3. **Vending Heist** (walk/pry/crowbar/noise/escape + machine/pickups/facade)
4. **Homeless Hustle** (cart push/dive/stash/redeem/fatigue + tent/blanket/redeemables)
5. **Day Labor** (carry/stack/tools/timer/hazards + truck/tools/lumber)
6. **Copper Wire** (crouch/snip/spark/coil/nav/detection + coil/interior/tools)
7. **ForgePlay meta** (mechanics recipe, shared locomotion/interact, thumbnails, stingers, credits)

## Session log (preserved)

- 2026-07-27 | intel | 20260727-185910_contracts-seeds-course-gates.md | Five small-scope rules for strict GameSpec, bounded seeded courses, fixed-step simulation, presentation damping, and deterministic quality gates.
- 2026-07-27 | assets | 20260727-190205_priority_gap_assets.md | 10 new CC0 candidates for crates/bags, guard, parked cars, urban/industrial dressing, prompt glyphs, and UI/chime audio.
- 2026-07-27 | mechanics | 10 notes in 4-mechanics\ (1913–1923) | Shared pause/a11y/audio/input; MD-B GameSpec feel knobs, guard AI, smash combo; Vending walk/pry/crowbar/noise → HAVE-candidate (input PARTIAL-candidate).
- 2026-07-27 | assets | 2-assets/20260727-1915…1927 (13 notes) + INDEX.md | Shared soft props/SFX/UI + MD-B guard/cars + Vending machine/crowbar/cam → HAVE-candidate; 3 quarantine licence notes.
- 2026-07-27 | forgeplay-intel | 1913–1917 ×5 | feelOverrides; systems pause/a11y/audio; hustle recipe; locomotion/interact/hit modules; qualityGate asserts.

- 2026-07-27 | skills | 8 feel recipes in 1-skills\ (shared cam/hit/pause-a11y; MD-B combo+guard; vending pry; cart-push/carry; copper flashlight) + INDEX.md
- 2026-07-27 | mechanics | Mythology Mechanics Research triage → 22 notes (1930–1951) + MYTHOLOGY-MECHANICS-SOURCE.md | Vending remaining NEED; Homeless core; Day Labor core; Copper crouch/snip/spark; ForgePlay recipe/locomotion/interact; shared hit-cue + win/fail → HAVE-candidate. Source folder read-only.
2026-07-27 | intel | 20260727-193155_realization-manifests-adapters-scaling.md | Five implementation contracts for capability receipts, reproducible manifests, measured course difficulty, tiny hustle adapters, and presentation-only scaling.
- 2026-07-27 | backup-ingest | BACKUP-RESEARCH-SOURCE.md + unique notes 2015/2017–2020 | Triaged Documents\BACKUP mythology reports + dated folders; filled remaining hustle NEED via parallel Codex canonicals (deduped); BACKUP-unique fixed-step / anim feel / Three.js graphics / SimReady gates / clock overrides. Dated folders skipped (VIPGrant/Slack/Kimi/voice). No production code.
- 2026-07-27 | codex-ingest | CODEX-2026-07-27-SOURCE.md + notes 2000–2014 / skills 2000–2005 / intel 2000–2003 / xrefs 2021–2022 | Triaged 8 Codex folders (2 empty); Mythology leftovers NEED→HAVE-candidate (homeless night/social/cart-stolen; daylabor fatigue/hazard/boss/payday/fail; copper coil/extract/detect/nav/fail); soft/hard+HUD PARTIAL-candidate; GameSpec time/fail/quality/env; no assets invented; no production code.
- 2026-07-27 | assets-import | Agent B HAVE-candidate → HAVE | Imported+wired 11 GLBs into `apps/play` (bags/pile/crate/cone/curb/barrier/guard/sedan/suv/crowbar/cam); left itch vending + Freesound SFX + Kenney fonts/icons as HAVE-candidate.
- 2026-07-27 | coding | feelOverrides landed | GameSpec `feelOverrides` (+ optional `systems` schema hooks) → `mergeFeelTuning` / createRun / stepRun; prompt keywords tanky/wobbly/twitchy/slugger/tight-brake; MECHANICS row lean/brake/health/melee → HAVE. Pause/a11y/audio play shell not wired.
- 2026-07-27 | forge3d-data | 2-assets/FORGE3D-DATA-STAGED.md | Staged CC0+project meshes/images into forge3d data\ (play GLBs/textures; PH cam/trash/crates/bag; Kenney curb+cars); 3 PLYs pre-existing; itch/Poly Pizza blockers noted.
