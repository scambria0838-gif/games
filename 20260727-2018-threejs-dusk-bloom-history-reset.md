# Skill — Three.js dusk/bloom + history-reset (graphics apply)

## Master-list row

> Graphics feel — portable Three.js only (Agent A / C). **No new CC0 asset URLs.**

## Status proposal

**HAVE-candidate feel/intel** — keep MD-B HDRI/bloom/dusk knobs; from Mythology graphics take only history-reset / cam-cut discipline. Defer TAA/DirectSR/vendor upscalers (Unreal/D3D12).

## Source

- `C:\Users\steve\Documents\BACKUP\operation-mythology-graphics-20260727-012826.md` — temporal history validity + explicit history-reset; motion correctness as engine duty
- Existing play sky/env skills; `duskBias` / bloom already in MD-B GameSpec path

## Apply note (Three.js fixed-step / GameSpec)

1. On camera cut / teleport / pause→resume large dt: set `needsHistoryReset` for any future TAA; today = clear trail/smoke sticky buffers.
2. Dusk/rain remain presentation multipliers on exposure/fog/bloom — not friction unless GameSpec says so.
3. Do not invent Poly Haven / CC0 URLs here; Agent B owns assets.
4. Pixel ratio + bloom intensity stay quality-gate bounded.
5. Knobs: `bloomIntensity`, `duskBias`, `resetTrailsOnCut`.

## Proposed knobs

| Knob | Range | Notes |
|------|-------|-------|
| `bloomIntensity` | 0–1.2 | |
| `duskBias` | 0–1 | |
| `resetTrailsOnCut` | bool | default true |

## Dependencies

- three-sky-env / polyhaven skills (existing); quality gate
