# Meter Drive-By — guard pressure feel

## Supports

- **MECHANICS_MASTER_LIST · I Meter Drive-By:** `Act III patrol guard + melee bowl` — Status HAVE
- **MECHANICS_MASTER_LIST · I Meter Drive-By:** `Guard AI variety (paths, aggro curve)` — Status NEED
- **MECHANICS_MASTER_LIST · Shared systems:** `Hit / impact feedback` — Status PARTIAL
- **ASSET_MASTER_LIST · I Meter Drive-By:** `Guard character mesh` — Status NEED
- **ASSET_MASTER_LIST · I Meter Drive-By:** `Tire smoke / sparks / rain VFX` — Status HAVE (threat juice reuse)

## Source

- `C:\Users\steve\Desktop\GAME SKILLS\2026-07-28_gameplay-ai-decision-perception.md` (stimulus channels, acquisition/retention hysteresis, threat facts)
- Local: `meter-driveby-feel` — “Guard close → Threat ring”
- Live: `guard_hit` / `guard_down` events; `guardRing` in `graphics.ts`

## Apply path (Three.js / MD-B)

1. Keep guard **sim-authoritative** (pos, down, damage). Presentation reads distance / LOS facts each render frame.
2. **Pressure bands** (hysteresis, not flap): `aware` > `chase` > `melee` with enter/exit radii (perception report pattern).
3. Feel per band:
   - aware: ring visible, low pulse, subtle bed duck
   - chase: ring scales/opacity up, cam slight pull-back, heartbeat SFX hook
   - melee: red rim flash, stronger shake on `guard_hit`, hit-stop short
4. On `guard_down`: camKick + popFlash (existing) + pressure bus clear; optional slow-mo presentClock 150–250ms (a11y-scaled).
5. Variety without new brain yet: GameSpec curves for `guardSpeed`, `guardRadius`, aggro ramp time, leash radius — same feel adapters, different timing.
6. Placeholder mesh OK: silhouette + emissive vest; Agent B mesh swaps in without changing cue IDs.
7. Never let ring/VFX deal damage; only sim `guardDamage` / radius.
8. Reduce Motion: keep ring + HUD “GUARD” chip; zero pulse/shake.

## Cross-links

- **Agent B:** `Guard character mesh` NEED — CC0 humanoid / stylized patrol; ring/VFX stay procedural.
- **Agent D:** Guard AI variety paths + aggro curve; emit optional `guard_state` events for feel.
- **Agent C:** `guard.aggroEnter`, `guard.aggroExit`, `guard.speed`, `guard.radius`, `feel.guardRingPulse`, `feel.guardCamPull`.
