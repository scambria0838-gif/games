# MECHANICS_MASTER_LIST â€” Dumpster Diving / ForgePlay

**Agent D source of truth.** You do **not** write production code. Research movement, turning, walk, hit/interact, AI, win/fail, and feel systems. Fill NEED rows; mark **HAVE-candidate** only when you drop a matching note in `C:\Users\steve\Desktop\AI-INBOX\4-mechanics\`. Coding agent marks true HAVE after implement.

## Agent D instructions (summary)

1. Read this file first; skim `ASSET_MASTER_LIST.md` and existing `4-mechanics\` notes.
2. One markdown file per find: `4-mechanics\YYYYMMDD-HHMM-<hustle>-<mechanic-slug>.md`.
3. Each file: exact row + hustle, status proposal, source, 5â€“10 line Three.js / GameSpec apply note, proposed knobs, Agent B/C dependencies.
4. Priority: Shared NEED â†’ Meter Drive-By NEED â†’ Vending â†’ Homeless â†’ Day Labor â†’ Copper â†’ ForgePlay meta.
5. Prefer portable recipes; Unreal/Unity OK only with Three.js / shared-sim apply path. No engine rewrites, shipping code, exploits, or malware.
6. End session with a short INDEX.md bullet list; then **stop** (manual paste session).

Status: `HAVE` | `NEED` | `PARTIAL` | `OPTIONAL` | `HAVE-candidate` | `PARTIAL-candidate`.

---

## Shared systems (all hustles)

| Mechanic | Status | Notes |
|----------|--------|-------|
| Fixed-step sim / deterministic tick | PARTIAL-candidate | MD-B shared sim; `4-mechanics/20260727-2015-shared-fixed-step-generalization.md` |
| Input map (keyboard + optional gamepad) | PARTIAL-candidate | MD-B keys; see `4-mechanics/20260727-1916-shared-input-map.md` |
| Camera follow + damping | PARTIAL | MD-B chase damped; per-hustle variants |
| Hit / impact feedback (cam shake, flash, SFX hook) | HAVE-candidate | `4-mechanics/20260727-1950-shared-hit-impact-cue-bus.md` |
| Soft vs hard collision | PARTIAL-candidate | `4-mechanics/20260727-2013-shared-soft-hard-collision-contract.md` |
| Score / cash / timer HUD contract | PARTIAL-candidate | `4-mechanics/20260727-2014-shared-score-hud-contract.md` |
| Win / fail / retry loop | HAVE-candidate | `4-mechanics/20260727-1951-shared-win-fail-retry.md` |
| Pause / settings | HAVE-candidate | `4-mechanics/20260727-1913-shared-pause-settings.md` |
| Accessibility (remap, reduce motion) | HAVE-candidate | `4-mechanics/20260727-1914-shared-accessibility.md` |
| Audio bus (SFX / bed / stinger) | HAVE-candidate | hooks only; `4-mechanics/20260727-1915-shared-audio-bus-hooks.md` |

---

## I Meter Drive-By

Grounded in `packages/shared/src/meter-driveby/` + `apps/play` (other hustles = enum/roadmap only).

| Mechanic | Status | Notes |
|----------|--------|-------|
| Fixed 60 Hz sim + replay checksum | HAVE | live sim |
| Grade / vmax / corridor clamp | HAVE | |
| Surfaces (asphalt/concrete/grass/paint) + Âµ | HAVE | |
| Lean steer (authority falls with speed) | HAVE | |
| Brake scrub + stability drain/recover | HAVE | |
| Ram meters (speed threshold) + jackpot | HAVE | |
| Melee swing (flamingo / sign loadout) | HAVE | |
| Soft scrub vs hard hit damage | HAVE | |
| Act III patrol guard + melee bowl | HAVE | |
| Dock win / wreck lose | HAVE | |
| Chase cam feel (shake, FOV, smoke, sparks) | HAVE | |
| Course density / spacing / traps | HAVE | GameSpec partial |
| Friction / rain / dusk bias | HAVE | GameSpec |
| Expose lean/brake/health/melee knobs in GameSpec | HAVE | `feelOverrides` on GameSpec → mergeFeelTuning / createRun; `4-mechanics/20260727-1917-meter-driveby-gamespec-feel-knobs.md` |
| Guard AI variety (paths, aggro curve) | HAVE-candidate | `4-mechanics/20260727-1918-meter-driveby-guard-ai-variety.md` |
| Combo / streak smash bonuses | HAVE-candidate | `4-mechanics/20260727-1919-meter-driveby-smash-combo.md` |
| Near-miss meter tease | OPTIONAL | |
| Ghost / replay path for player | OPTIONAL | checksum exists |

---

## II Vending Heist

| Mechanic | Status | Notes |
|----------|--------|-------|
| On-foot walk / strafe / sprint | HAVE-candidate | `4-mechanics/20260727-1920-vending-walk-strafe-sprint.md` |
| Interact / hold-to-pry vending | HAVE-candidate | `4-mechanics/20260727-1921-vending-hold-to-pry.md` |
| Crowbar swing / hit machine | HAVE-candidate | `4-mechanics/20260727-1922-vending-crowbar-hit.md` |
| Spill / loot burst + pickup magnet | HAVE-candidate | `4-mechanics/20260727-1930-vending-spill-loot-magnet.md` |
| Stealth / noise meter (cam / clerk) | HAVE-candidate | `4-mechanics/20260727-1923-vending-noise-stealth.md` |
| Aisle collision + cover | HAVE-candidate | `4-mechanics/20260727-1933-vending-aisle-collision-cover.md` |
| Escape timer after alarm | HAVE-candidate | `4-mechanics/20260727-1931-vending-escape-timer.md` |
| Carry capacity / drop | HAVE-candidate | `4-mechanics/20260727-1932-vending-carry-capacity-drop.md` |
| Fail: caught / timeout | HAVE-candidate | `4-mechanics/20260727-1934-vending-fail-caught-timeout.md` |

---

## III Homeless Hustle

| Mechanic | Status | Notes |
|----------|--------|-------|
| Cart push (walk-coupled or ride toggle) | HAVE-candidate | `4-mechanics/20260727-1935-homeless-cart-push.md` |
| Scavenge interact (dumpster dive hold) | HAVE-candidate | `4-mechanics/20260727-1936-homeless-scavenge-dive.md` |
| Inventory / stash on cart | HAVE-candidate | `4-mechanics/20260727-1937-homeless-cart-stash.md` |
| Redeemables turn-in (bottle/can) | HAVE-candidate | `4-mechanics/20260727-1938-homeless-redeemables-turnin.md` |
| Fatigue / stamina while pushing | HAVE-candidate | `4-mechanics/20260727-1939-homeless-fatigue-stamina.md` |
| Territory / turf claim | OPTIONAL | |
| Night cycle pressure | HAVE-candidate | `4-mechanics/20260727-2000-homeless-night-cycle-pressure.md` |
| Soft social bump (NPCs) | HAVE-candidate | `4-mechanics/20260727-2001-homeless-soft-social-bump.md` |
| Fail: cart stolen / busted | HAVE-candidate | `4-mechanics/20260727-2002-homeless-fail-cart-stolen.md` |

---

## IV Day Labor

| Mechanic | Status | Notes |
|----------|--------|-------|
| Walk + carry heavy object | HAVE-candidate | `4-mechanics/20260727-1940-daylabor-walk-carry.md` |
| Place / stack job props (pallet, lumber) | HAVE-candidate | `4-mechanics/20260727-1941-daylabor-place-stack.md` |
| Tool swing / hit (hammer nail, shovel dig) | HAVE-candidate | `4-mechanics/20260727-1942-daylabor-tool-swing.md` |
| Job checklist / shift timer | HAVE-candidate | `4-mechanics/20260727-1943-daylabor-checklist-shift-timer.md` |
| Fatigue + rest break | HAVE-candidate | `4-mechanics/20260727-2003-daylabor-fatigue-rest.md` |
| Site hazard (cone trip, falling board) | HAVE-candidate | `4-mechanics/20260727-2004-daylabor-site-hazard.md` |
| Boss / foreman callout pressure | HAVE-candidate | `4-mechanics/20260727-2005-daylabor-boss-foreman-callout.md` |
| Payday cash settle | HAVE-candidate | `4-mechanics/20260727-2006-daylabor-payday-cash-settle.md` |
| Fail: injury / fired | HAVE-candidate | `4-mechanics/20260727-2007-daylabor-fail-injury-fired.md` |

---

## V Copper Wire

| Mechanic | Status | Notes |
|----------|--------|-------|
| Walk / crouch / flashlight cone | HAVE-candidate | `4-mechanics/20260727-1944-copper-crouch-flashlight.md` |
| Snip / cut interact on coils | HAVE-candidate | `4-mechanics/20260727-1945-copper-snip-cut.md` |
| Spark hazard on live wire (hit/stun) | HAVE-candidate | `4-mechanics/20260727-1946-copper-spark-hazard.md` |
| Carry coil weight slow | HAVE-candidate | `4-mechanics/20260727-2008-copper-coil-carry-weight.md` |
| Extraction / stash drop point | HAVE-candidate | `4-mechanics/20260727-2009-copper-extraction-stash.md` |
| Detection (buzz, light sweep) | HAVE-candidate | `4-mechanics/20260727-2010-copper-detection-buzz-light.md` |
| Interior nav (rooms, doors) | HAVE-candidate | `4-mechanics/20260727-2011-copper-interior-nav.md` |
| Fail: electrocute / caught | HAVE-candidate | `4-mechanics/20260727-2012-copper-fail-electrocute-caught.md` |

---

## ForgePlay meta-mechanics

| Mechanic | Status | Notes |
|----------|--------|-------|
| Prompt â†’ GameSpec template pick | PARTIAL | |
| Per-hustle override knobs (density, friction, timer) | PARTIAL-candidate | `3-forgeplay-intel/20260727-2020-clock-domains-hustle-overrides.md` |
| Mechanics recipe block in GameSpec | HAVE-candidate | `4-mechanics/20260727-1947-forgeplay-mechanics-recipe-block.md` (+ `3-forgeplay-intel/20260727-1915-hustle-recipe-block.md`) |
| Shared locomotion module switch (cart vs walk) | HAVE-candidate | `4-mechanics/20260727-1948-forgeplay-shared-locomotion-module.md` (+ `3-forgeplay-intel/20260727-1916-locomotion-interact-modules.md`) |
| Shared interact / hit module | HAVE-candidate | `4-mechanics/20260727-1949-forgeplay-shared-interact-hit-module.md` (+ Agent C sibling) |
| Quality-gate checklist for generated feel | PARTIAL-candidate | `3-forgeplay-intel/20260727-1917-quality-gate-fields.md` + `…/2001-quality-gate-perf-regression.md` + `…/2019-quality-gate-simready-fields.md` |

