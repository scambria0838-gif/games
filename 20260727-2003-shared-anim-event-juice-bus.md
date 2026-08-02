# Shared — Animation event → juice bus (lean / swing / carry)

## Supports

- Animation-as-feel for MD-B lean/melee and hustle carry/tool swings (not full rig/motion matching)

## Source

- `4-animation-rigging-act-as-lead\work\operation-mythology-animation-20260727-024516.md` — cooked animation events; presentation side-effect journal; fixed-step sync
- Defer: facial, motion matching, full FBIK, GPU deformation reports in same folder

## Apply path (Three.js)

1. Author sparse events on clips/timelines: `swingConnect`, `footPlant`, `carryPick`, `toolImpact`.
2. On crossing (sim-scheduled or presentation sample with ack id): emit cue-bus intents already used for hits.
3. Cart lean remains procedural pose from sim lean axis (existing MD-B) — events optional for scrub accents.
4. Rollback-safe: events carry `tick` + `requestId`; presentation journal is non-authoritative.
5. Do not evaluate hero face rigs or motion matching for arcade hustles.

## Cross-links

- Hit cue bus skills + mechanics `1950`
- MD-B lean/brake/smash juice skill
