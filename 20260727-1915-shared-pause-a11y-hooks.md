# Shared pause + accessibility hooks (feel)

## Supports

- **MECHANICS_MASTER_LIST · Shared systems:** `Pause / settings` — Status NEED
- **MECHANICS_MASTER_LIST · Shared systems:** `Accessibility (remap, reduce motion)` — Status NEED
- **MECHANICS_MASTER_LIST · Shared systems:** `Input map (keyboard + optional gamepad)` — Status PARTIAL
- **ASSET_MASTER_LIST · Shared world:** `UI font (display + HUD)` — Status NEED (settings readability)

## Source

- `C:\Users\steve\Desktop\EXTRA SKILS\Operation Mythology Mechanics\operation-mythology-mechanics-20260727-022147.md` (a11y profile, hold/toggle, pause, photosensitivity)
- `C:\Users\steve\Desktop\EXTRA SKILS\Operation Mythology Mechanics\operation-mythology-mechanics-20260727-023155.md` (semantic actions, Pause, hold triggers)
- RESEARCH_INDEX game-flow note: platform pause ≠ game pause; explicit clock domains
- Local feel skill: keep juice readable when motion reduced (`meter-driveby-feel`)

## Apply path (Three.js / Meter Drive-By → all hustles)

1. Semantic action `Pause` (Esc / Start) toggles **game pause** — stop consuming sim ticks / freeze presentation clock; do not rely on `document.hidden` alone.
2. Separate clocks: `simClock`, `presentClock`, `uiClock`. Pause freezes sim+present; UI stays live for settings.
3. First settings panel must expose before “unskippable” juice: Reduce Motion, remapping, volume buses (SFX/bed/stinger), shake scale.
4. Hold→Toggle alternatives for Brake, Lean-assist (if any), Interact/Pry, Flashlight, Crouch — same semantic action, different activation policy (XAG 107).
5. Reduce Motion profile: zero cam shake/FOV kick/hit-stop; keep brake glow, meter halo, threat ring, HUD flashes at readable (non-strobe) levels.
6. Persist a11y profile in `localStorage` (local user lifetime); never bake into course seed / replay checksum.
7. On blur/suspend: auto-pause local single-player; show “paused” affordance; resume only on explicit Confirm.
8. ForgePlay quality gate: generated hustles must declare pause + reduce-motion hooks or fail checklist.

## Cross-links

- **Agent B:** UI font NEED; hustle icons for settings rows; optional caption-safe HUD glyphs.
- **Agent D:** own Pause / settings + Accessibility rows; shared input map must list semantic actions not keycodes.
- **Agent C:** GameSpec `a11y.reduceMotion`, `a11y.holdToToggle[]`, `flow.pauseOnBlur`; recipe block `mechanics.feel.a11y`.
