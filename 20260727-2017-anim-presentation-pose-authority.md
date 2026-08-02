# Skill — Animation as feel (presentation pose authority)

## Master-list row

> Feel / camera / juice — cart lean, swing pose, carry lean (Agent A)

## Status proposal

**HAVE-candidate feel recipe** — gameplay owns timing; animation/presentation poses never write HP/speed (Mythology animation sync baseline; portable Three.js).

## Source

- `C:\Users\steve\Documents\BACKUP\operation-mythology-animation-20260727-013104.md` — gameplay authority outside pose graph; presentation-only events; defer motion matching / full-body IK
- Cross-link: `1-skills/20260727-1915-meter-lean-brake-smash-combo-juice.md`; cart-push/carry feel

## Apply note (Three.js fixed-step / GameSpec)

1. Sim outputs: lean, brake, swingPhase, carryLoad, stunned — immutable snapshot per tick.
2. Presentation: lerp cart tilt / arm swing / bob from snapshot; Reduce Motion → scale to 0.
3. Hit enable windows come from sim action timeline, not clip callbacks.
4. No root-motion authority for arcade hustles; root motion deferred.
5. Knobs: `leanVisualDeg`, `swingPoseBlend`, `carryTiltDeg`.

## Proposed knobs

| Knob | Range | Notes |
|------|-------|-------|
| `leanVisualDeg` | 4–18 | |
| `swingPoseBlend` | 0.1–0.5 | s |
| `carryTiltDeg` | 2–12 | |

## Dependencies

- Existing combo/carry feel skills; Agent D locomotion
