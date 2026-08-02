# Shared — Accessibility (remap, reduce motion)

## Master-list row

> **Accessibility (remap, reduce motion)** | Shared systems (all hustles) | was **NEED**

## Status proposal

**HAVE-candidate** — minimal a11y profile (rebind + reduce-motion + hold alternatives) that all hustles can read from one settings blob. Not a full compliance suite; ship the knobs ForgePlay can honor.

## Source

- Accessibility baseline: `C:\Users\steve\Desktop\GAME-SKILLS-UNIQUE\by-name\RESEARCH_INDEX__2b8b84b5.md` (versioned accessibility profiles; remapping; multimodal cues; photosensitivity / motion)
- Input semantic actions: same index (physical → semantic → fixed-tick command)
- MD-B today: hard-coded `KeyA`/`KeyD` lean, `KeyS` brake, click/space melee in `apps/play/src/meter-driveby/input.ts` — no remap, no reduce-motion gate on cam shake/FOV

## Apply note (Three.js fixed-step / GameSpec)

1. Store a versioned profile: `{ version, bindings, reduceMotion, holdToToggle, contrastHud }`.
2. Remap edits **semantic actions** (`leanLeft`, `leanRight`, `brake`, `swing`, `interact`, `sprint`, `pause`) — not raw `code` strings scattered in gameplay.
3. Reduce motion gates **presentation only**: cam shake amp ×0, FOV punch ×0, screen flash ×0; sim lean/brake/ram unchanged (fairness + replay).
4. Sustained-hold alternatives: `brake` and Vending `pry` expose `holdMs` vs `toggleOnPress` (accessibility guidance: alternatives to sustained holds).
5. Apply reduce-motion in graphics sync (`graphics.ts` shake/FOV paths) via one `a11y.motionScale` multiplier (0 or 1, or 0–1 slider).
6. First-run: offer “Reduce motion?” before first hustle if `prefers-reduced-motion: reduce` media query is set.
7. Captions/stingers: hook only — when audio bus lands, critical cues (alarm, caught, dock win) also pulse HUD color (see audio-bus note).
8. Agent A cross-link: feel recipes must document which layers are motion-gated vs sim-authoritative.

## Proposed knobs

| Knob | Range | Notes |
|------|-------|-------|
| `reduceMotion` | bool \| 0–1 | 0 = full feel, 1 = gated |
| `motionScale` | 0–1 | derived; shake/FOV/flash × |
| `holdToToggleInteract` | bool | pry/dive/carry holds |
| `remapEnabled` | bool | default true |
| `colorblindHud` | `off` \| `deuter` \| `prot` | optional; HUD tint only |
| `flashCapIntensity` | 0–1 | photosensitivity ceiling |

## Dependencies

- **Agent C:** GameSpec `a11y` block optional overrides (usually player-local, not prompt-generated)
- **Agent B:** none for core; optional high-contrast HUD glyphs (shared UI font NEED)
- **Shared input-map note:** bindings table lives there; this note owns motion/hold policy
