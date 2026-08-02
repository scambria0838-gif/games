# Shared — Input map generalization (keyboard + gamepad)

## Master-list row

> **Input map (keyboard + optional gamepad)** | Shared systems (all hustles) | was **PARTIAL**

## Status proposal

**PARTIAL-candidate** — MD-B already samples keyboard into `{ lean, brakeDrag, swingMelee }`. Recipe generalizes to semantic actions + gamepad axes + hustle context layers without replacing the fixed-step command shape.

## Source

- Input pipeline: `C:\Users\steve\Desktop\GAME-SKILLS-UNIQUE\by-name\RESEARCH_INDEX__2b8b84b5.md` (physical → semantic → fixed-tick command; rebinding; device hotplug)
- Local HAVE: `apps/play/src/meter-driveby/input.ts` — KeyA/D/S, Arrow*, Space/click swing
- ForgePlay need: Vending walk/sprint/interact will collide with MD-B lean/brake if raw keys stay hardcoded

## Apply note (Three.js fixed-step / GameSpec)

1. Split layers: **PhysicalSample** (keydown/gamepad) → **SemanticActions** (per context map) → **SimInput** (hustle-specific struct sampled once per fixed tick).
2. Contexts: `menu`, `meter_driveby`, `vending_heist`, … Only one gameplay context active; menu always overlays for pause.
3. Preserve digital edges across rAF → fixed-step: edge buffer for `swing`, `interactStart`, `interactEnd` so 60 Hz sim never misses a click between frames.
4. Gamepad: left stick X → lean or strafe; LT/RT or A → brake/sprint; face button → swing/interact. Deadzone `0.15–0.25`.
5. Default bindings table (versioned) lives in shared JSON; MD-B keeps exporting current `SimInput` shape so `stepRun` unchanged.
6. Replay: record **semantic** commands (or final SimInput), not scancodes — already checksum-friendly.
7. Remap UI writes immutable compiled table; swap on pause exit (see accessibility note).
8. Do not put bindings in GameSpec prompts; GameSpec may only declare which **actions** a hustle requires (`requiredActions: ["lean","brake","swing"]`).

## Proposed knobs

| Knob | Range | Notes |
|------|-------|-------|
| `stickDeadzone` | 0.1–0.35 | default 0.18 |
| `axisLeanExp` | 1–2.5 | stick response curve |
| `edgeBufferTicks` | 1–4 | digital edge hold |
| `gamepadEnabled` | bool | default true |
| `context` | enum | active action map |
| `requiredActions` | string[] | GameSpec hustle contract |

## Dependencies

- **Agent C:** GameSpec `controls.requiredActions` (per template)
- **Agent B:** none
- **Coding:** extract `InputMap` → shared package or `apps/play/src/input/` used by all hustles
