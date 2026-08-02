# Meter Drive-By — Expose lean / brake / health / melee knobs in GameSpec

## Master-list row

> **Expose lean/brake/health/melee knobs in GameSpec** | I Meter Drive-By | was **NEED**

## Status proposal

**HAVE-candidate** — values already live and work in `packages/shared/src/meter-driveby/tuning.json`; GameSpec today only exposes `melee` id + course/env. Recipe: optional `feel` / `combat` override block merged into TUNING at run start (clamped), not a second physics system.

## Source

- Local HAVE: `tuning.json` — `leanAuthorityBase`, `brakeFrictionBonus`, `brakeStabilityDrain`, `stabilityRecover`, `healthMax`, `melee.*.arcRad/reach/cooldownTicks`, `hardHitDamage`, `guardDamage`
- Local gap: `packages/shared/src/forge-play/spec.ts` — `GameSpecSchema` has `melee`, `courseOverrides`, `env` only
- Intel: AI-INBOX session log contracts-seeds (strict GameSpec, bounded overrides)

## Apply note (Three.js fixed-step / GameSpec)

1. Add optional Zod block `feelOverrides` (name TBD with Agent C) with **narrow ranges** around TUNING defaults — never unbounded.
2. At course/run init: `effectiveTuning = clampMerge(TUNING, spec.feelOverrides)`; pass into `stepRun` or set module tuning once per run (deterministic for replay seed).
3. Map prompt tags → mild presets only, e.g. `wet` already scales `frictionScale`; add `tanky` → `healthMax`↑, `twitchy` → `leanAuthorityBase`↑, `slugger` → melee reach↑ cooldown↑.
4. Do **not** expose every TUNING key — ship the feel-facing set below; keep µ tables / FIXED_DT / course length internal.
5. Melee weapon id stays top-level `melee`; overrides tweak **active** weapon’s arc/reach/cooldown or both loadouts.
6. Graphics feel (shake, FOV) stays presentation-side; optional `shakeScale` can mirror accessibility `motionScale` but default 1.
7. Quality gate: checksum replay with same seed+overrides must match; document overrides in run header.
8. Cross-link Agent C: extend `GameSpecSchema`; Agent A: document which feel knobs read from overrides vs presentation.

## Proposed knobs (GameSpec `feelOverrides`)

| Knob | Range | Default (approx) |
|------|-------|------------------|
| `leanAuthorityBase` | 2.5–5.0 | 3.7 |
| `brakeFrictionBonus` | 1.5–4.0 | 2.8 |
| `brakeStabilityDrain` | 0.1–0.5 | 0.28 |
| `stabilityRecover` | 0.1–0.5 | 0.28 |
| `healthMax` | 60–150 | 100 |
| `hardHitDamage` | 10–30 | 18 |
| `meleeArcRad` | 0.5–2.0 | per weapon |
| `meleeReach` | 1.6–3.2 | per weapon |
| `meleeCooldownTicks` | 12–36 | per weapon |
| `ramThresholdFrac` | 0.35–0.7 | 0.5 |

## Dependencies

- **Agent C:** add `feelOverrides` (or `meterFeel`) to GameSpec + prompt → preset mapping
- **Agent B:** none
- **Coding:** merge helper + thread effective tuning into step/course init
