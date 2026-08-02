# Shared camera damping + comfort (Arcade recipe)

## Supports

- **MECHANICS_MASTER_LIST · Shared systems:** `Camera follow + damping` — Status PARTIAL — “MD-B chase damped; per-hustle variants”
- **MECHANICS_MASTER_LIST · Shared systems:** `Accessibility (remap, reduce motion)` — Status NEED (comfort half)
- **ASSET_MASTER_LIST:** no new mesh; uses existing chase/presentation path

## Source

- `C:\Users\steve\Desktop\EXTRA SKILS\Operation Mythology Mechanics\operation-mythology-mechanics-20260727-020119.md` (FP/TP camera, damping, comfort)
- Microsoft XAG 117 (FOV / bob / shake / sway / roll adjustable to zero) via that report
- Local: `C:\Users\steve\Desktop\skill\meter-driveby-rider-cam\SKILL.md`, `meter-driveby-feel\SKILL.md`
- Live ref: `apps/play/src/meter-driveby/graphics.ts` chase FOV lerp + shake/kick

## Apply path (Three.js / Meter Drive-By → shared)

1. Keep **sim authority** on cart/pawn pose only; camera is presentation — never write heading/speed from cam.
2. Ideal chase pose = subject − heading × `back` + height; look-at = subject + heading × `lookAhead` (rider chest for MD-B).
3. Soft-follow with independent exponential damps: `posAlpha`, `lookAlpha`, `fovAlpha` (MD-B already lerps FOV ~0.12 — expose as knobs).
4. Stack **bounded modifiers** (priority + duration + dedupe id): brake FOV pinch, speed FOV stretch, hit kick, lean lateral offset — sum then clamp; do not hard-set camera.
5. Run modifiers in **render dt**, not fixed 60 Hz sim (matches Operation Mythology: damping/shake stay off rollback cost).
6. Add `CameraComfortProfile`: `shakeScale`, `fovKickScale`, `bobScale`, `rollScale` ∈ [0..1]; Reduce Motion → all 0, keep readable framing.
7. Persist comfort in local settings only; never checksum / replay camera state.
8. Per-hustle rig variants later: chase (MD-B), over-shoulder walk (Vending/Homeless/Day Labor), crouch cone cam (Copper) — same damper + comfort bus.

## Cross-links

- **Agent B:** none required (no mesh). Optional later: separate FP/TP kit only if walk hustles need distinct FOV presets in UI art.
- **Agent D:** generalize MD-B chase into shared `CameraFollow` contract; keep soft vs hard collision independent of boom collision.
- **Agent C (GameSpec):** knobs `cam.back`, `cam.height`, `cam.lookAhead`, `cam.posAlpha`, `cam.lookAlpha`, `cam.fovBase`, `cam.fovSpeedGain`, `cam.fovBrakePinch`, `comfort.shakeScale`.
