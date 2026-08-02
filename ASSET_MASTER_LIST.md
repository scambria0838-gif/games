# ASSET_MASTER_LIST — Dumpster Diving / ForgePlay

**Agent B source of truth.** Fill NEED rows. Prefer **CC0**. Status values: `HAVE` | `NEED` | `PARTIAL` | `OPTIONAL` | `HAVE-candidate`.

## Agent B instructions

1. Read this file first; skim `MECHANICS_MASTER_LIST.md` for assets that unlock mechanics.
2. Write one note per find into `2-assets\` as `YYYYMMDD-HHMM-<hustle>-<asset-slug>.md`.
3. Each note: exact row name + hustle, URL, licence, status proposal (`HAVE-candidate` only — coding agent marks true `HAVE` after import).
4. Update this list to **HAVE-candidate** when you drop a matching note.
5. Non-CC0 / unclear licence → copy path note into `_quarantine-licence\` and do **not** mark HAVE-candidate.
6. End session with a short INDEX bullet list of files written; then **stop** (manual paste session, not continuous).

---

## Shared world

| Asset | Status | Notes |
|-------|--------|-------|
| Night / urban HDRI | HAVE | Poly Haven / play textures |
| Asphalt PBR | HAVE | asphalt_02 set |
| Concrete PBR | PARTIAL | barriers / some maps; expand set |
| Brick PBR | HAVE / PARTIAL | alley brick + normals/rough |
| Metal PBR | PARTIAL | dumpster/metal cues; need reusable set |
| Street lamp | HAVE | street props / corridor kit |
| Dumpster | HAVE | dumpster.glb + texture |
| Trash bags | HAVE | Quaternius Poly Pizza CC0 — `trash_bags.glb` + `trash_pile.glb` wired in play scrap dressing |
| Crates | HAVE | Quaternius Poly Pizza CC0 — `crate.glb` wired for soft obstacles |
| Traffic cones | HAVE | Kenney City Kit Roads `construction-cone` → `traffic_cone.glb` (jamesdev itch zip blocked / no direct URL) — `2-assets/20260727-1917-shared-traffic-cones.md` |
| Modular curb / barrier | HAVE | Kenney City Kit Roads CC0 — `curb.glb` + `barrier.glb` dressing + hard-obstacle barrier mesh |
| Lot / alley SFX bed | HAVE-candidate | felix.blume Freesound CC0 — no direct CDN without auth; leave for audio-bus pass — `2-assets/20260727-1919-shared-lot-alley-sfx.md` |
| UI font (display + HUD) | HAVE-candidate | Kenney Fonts CC0 — not wired this pass (3D mesh priority) — `2-assets/20260727-1920-shared-ui-font.md` |
| Hustle icons (×5 + ForgePlay) | HAVE-candidate | Kenney Game Icons CC0 — not wired this pass — `2-assets/20260727-1921-shared-hustle-icons.md` |

---

## I Meter Drive-By

| Asset | Status | Notes |
|-------|--------|-------|
| Cart + rider kit | HAVE | cart.glb + rider seat |
| Plain cart | HAVE | cart_plain.glb |
| Parking meter | HAVE | meter.glb |
| Flamingo mace | HAVE | flamingo_mace.glb |
| Yard sign bat | HAVE | yard_sign.glb |
| Nail bat | HAVE | nail_bat.glb |
| Radio | HAVE | radio.glb |
| Street props pack | HAVE | street_props.glb |
| Tire smoke / sparks / rain VFX | HAVE | vfx textures + feel hooks |
| Guard character mesh | HAVE | Quaternius Business Man CC0 — `guard.glb` wired in `makeGuard()` (decorative AI mesh) |
| CC0 parked cars | HAVE | Kenney Car Kit CC0 — `sedan.glb` + `suv.glb` replace procedural parked cars |
| Extra soft props | HAVE | bags/crates/cones imported + wired — `2-assets/20260727-1927-meter-driveby-extra-soft-props.md` |

---

## II Vending Heist

| Asset | Status | Notes |
|-------|--------|-------|
| Vending machine | HAVE-candidate | Valentin Laffitte itch CC0 — itch paywall/download flow; no direct zip URL this pass — `2-assets/20260727-1924-vending-machine.md` |
| Snack / can pickups | NEED | loot spill props |
| Crowbar | HAVE | CreativeTrio Poly Pizza CC0 — `crowbar.glb` lot dressing (pry AI later) |
| Store facade / aisle kit | NEED | facade textures exist; aisle mesh NEED |
| Security cam | HAVE | Poly Haven security_camera_01 CC0 — `security_cam.glb` pole dressing |
| Spill VFX + chime SFX | NEED | loot burst feedback |
| Clerk character | OPTIONAL | can be silhouette / off-screen |

---

## III Homeless Hustle

| Asset | Status | Notes |
|-------|--------|-------|
| Cart + tarp | PARTIAL | cart HAVE; tarp dressing NEED |
| Tent / cardboard shelter | NEED | overnight / stash beat |
| Blanket / clothes piles | NEED | scavenge props |
| Bottle / can redeemables | NEED | turn-in items |
| Dumpster extras | PARTIAL | dumpster HAVE; dive contents NEED |
| Alley SFX | NEED | night pressure bed |

---

## IV Day Labor

| Asset | Status | Notes |
|-------|--------|-------|
| Truck / work van | NEED | site dressing / payday beat |
| Cone / sawhorse / caution tape | NEED | hazards + placeables |
| Hammer / shovel / tool belt | NEED | tool swing |
| Lumber / pallet / drywall | NEED | carry / stack props |
| Hard hat | NEED | identity + optional armor cue |
| Porta-potty | OPTIONAL | comedy dressing |
| Construction SFX | NEED | hammer, truck reverse, site bed |

---

## V Copper Wire

| Asset | Status | Notes |
|-------|--------|-------|
| Copper coil / pipe | NEED | carry weight prop |
| Junction box | NEED | snip / spark interact |
| Abandoned interior kit | NEED | rooms / doors / nav |
| Snips / pliers | NEED | cut tool |
| Flashlight + spark VFX | NEED | crouch light + hazard |
| Buzz / spark SFX | NEED | detection + stun |

---

## ForgePlay meta

| Asset | Status | Notes |
|-------|--------|-------|
| Prompt UI chrome | PARTIAL | forge-play app shell |
| Hustle thumbnails ×5 | NEED | picker / cards |
| Win / fail stingers | NEED | short SFX |
| Credits / licence template | NEED | Poly Haven + CC0 rollup |

---

## Status legend

| Status | Meaning |
|--------|---------|
| HAVE | In repo / playable import |
| HAVE-candidate | Agent B found; awaiting coding import |
| PARTIAL | Some pieces exist; gap remains |
| NEED | Missing; research priority |
| OPTIONAL | Nice-to-have; skip if blocked |
