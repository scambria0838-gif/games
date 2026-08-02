# Forge3D training data — staged 2026-07-27

Staging agent: curated **CC0 + project-owned** mesh/image/pointcloud exemplars into Forge3D `data/` (not GDD research, not weights).

**Data root:** `C:\Cambria\sovereign-ai\services\forge3d\data\`  
**Fallback path:** not used (forge3d `data\` exists).

## Counts (after this session)

| Bucket | Count | Path |
|--------|------:|------|
| Meter Drive-By GLBs | 9 | `meshes/meter_driveby/` |
| Poly Haven mesh kits (1k glTF) | 15 | `meshes/polyhaven/` |
| Kenney CC0 curated GLBs | 30 | `meshes/kenney_cc0/` |
| Images — meter_driveby project | 16 (+credits) | `images/meter_driveby/` |
| Images — urban_lot | 5 (+credits) | `images/urban_lot/` |
| Images — polyhaven PBR/HDRI kits | 8 dirs | `images/polyhaven/` (pre-existing) |
| Synthetic PLYs | 3 | `pointclouds/synthetic/` (pre-existing; not regenerated) |

**This session added:** 2 project GLBs, 5 Poly Haven kits, 30 Kenney GLBs, 16 project textures, 5 urban_lot texture/HDRI refs. Updated `data/MANIFEST.json`.

---

## Newly staged — project-owned (Dumpster Diving / Meter Drive-By)

| Staged path | Licence | Source |
|-------------|---------|--------|
| `meshes/meter_driveby/cart_plain.glb` | Project | `apps/play/public/models/cart_plain.glb` |
| `meshes/meter_driveby/nail_bat.glb` | Project | `apps/play/public/models/nail_bat.glb` |
| `images/meter_driveby/*.webp` (cart, dumpster, bats, crate, facade, alley brick/painted, barrier) | Project | `apps/play/public/textures/` |
| `images/urban_lot/asphalt_02_*.jpg` | CC0 (Poly Haven) | play copy of asphalt_02 |
| `images/urban_lot/sky_lot_dusk.hdr` | CC0 (Poly Haven / play credits) | `apps/play/public/textures/sky_lot_dusk.hdr` |
| `images/urban_lot/modern_buildings_night_1k.hdr` | CC0 (Poly Haven) | `apps/play/public/textures/modern_buildings_night_1k.hdr` |

Already present (unchanged): `cart.glb`, `meter.glb`, `dumpster.glb`, `yard_sign.glb`, `flamingo_mace.glb`, `radio.glb`, `street_props.glb`.

---

## Newly staged — CC0 downloads (B notes / same themes)

| Staged path | Licence | Source URL / note |
|-------------|---------|-------------------|
| `meshes/polyhaven/security_camera_01/` | CC0 | https://polyhaven.com/a/security_camera_01 (B: vending cam) |
| `meshes/polyhaven/trashbag/` | CC0 | https://polyhaven.com/a/trashbag (B: trash-bags theme) |
| `meshes/polyhaven/wooden_crate_02/` | CC0 | https://polyhaven.com/a/wooden_crate_02 (B: crates theme) |
| `meshes/polyhaven/plastic_crate_01/` | CC0 | https://polyhaven.com/a/plastic_crate_01 |
| `meshes/polyhaven/cement_bag/` | CC0 | https://polyhaven.com/a/cement_bag (soft bag family) |
| `meshes/kenney_cc0/city_kit_roads/` (16 GLBs) | CC0 | https://kenney.nl/assets/city-kit-roads (B: modular curb) — curated curb/barrier/road subset |
| `meshes/kenney_cc0/car_kit/` (11 GLBs) | CC0 | https://kenney.nl/assets/car-kit (B: parked cars) — sedan/van/truck/suv subset |

Each Kenney subset folder has `LICENCE.txt`.

---

## Pointclouds

Pre-existing synthetic ASCII PLYs left as-is (prior pattern present; no new generation):

- `pointclouds/synthetic/unit_sphere_2k.ply`
- `pointclouds/synthetic/lot_plane_6k.ply`
- `pointclouds/synthetic/cart_bbox_3k.ply`

---

## Blockers / not staged (quarantine or no stable download)

| Candidate (B note) | Why skipped |
|--------------------|-------------|
| Quaternius trash bags / crates / Ultimate Modular Men (Poly Pizza / pack page) | No stable machine download API this session; licence CC0 but fetch path manual |
| jamesdev Traffic Road Assets (itch, ~51 MB) | No durable CDN URL without itch auth/page scrape |
| Valentin Laffitte retro vending machine (itch `.rar`) | Manual itch download |
| CreativeTrio crowbar (Poly Pizza) | No stable API |
| Quarantine notes under `2-assets/_quarantine-licence/` | Unclear / non-CC0 — do not import |

---

## Rules observed

- No model weights under `data/` or play `public/`
- No game code changes; no git commit
- No training run
- CC0 / project-owned only
