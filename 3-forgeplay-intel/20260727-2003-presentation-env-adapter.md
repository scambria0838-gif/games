# Presentation env adapter (GameSpec ↔ Three.js)

## Context

Codex graphics corpus is AAA-heavy; portable slice is the **renderer adapter boundary** from the time/weather gameplay contract.

## Contract

1. Sim/GameSpec owns `dayFrac` / wetness / visibility class.
2. Three.js sky/HDRI/post is a consumer (`envPresentation.followSimDayFrac`).
3. Quality gate may assert `followSimDayFrac === true` when night pressure recipe present.
4. No render-graph / DLSS / IES requirements for Dumpster Diving.

## Cross-links

- `20260727-2000-gamespec-time-phase-env.md`
- `1-skills/20260727-2004-graphics-env-snapshot-three.md`
- Project skills: `three-sky-env`, `polyhaven-sky-import`
