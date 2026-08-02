# Agent B Asset Scout — Priority Gap Batch

**Date:** 2026-07-27  
**Scope:** Meter Drive-By, Vending Heist, Homeless Hustle, Day Labor, Copper Wire, and ForgePlay meta assets  
**Download policy:** Catalogue only; no binaries downloaded.

| name | URL | licence | format | path hint | hustle fit |
|---|---|---|---|---|---|
| Plastic Crate 02 | https://polyhaven.com/a/plastic_crate_02 | CC0 | Blend, glTF, USD, FBX, textures; 6K tris, 0.5 m wide | `Shared/Props/Containers/Crate_Plastic_02`; prefer glTF/GLB at 1K–2K textures and generate simple box collision | Shared world real crate; Vending store/warehouse; Day Labor site storage |
| Cardboard Box 01 | https://polyhaven.com/a/cardboard_box_01 | CC0 | Blend, glTF, USD, FBX, textures; 17K tris, 0.5 m wide | `Shared/Props/Trash/Cardboard_Box_01`; import glTF, create 2–4K hero and decimated dressing LOD | Homeless shelter/alley soft prop; store stock; dumpster-cluster dressing |
| Compost Bags | https://polyhaven.com/a/compost_bags | CC0 | Download archive with PBR texture maps; 19K tris, 1.8 m-wide set | `Shared/Props/Bags/Bag_Stack_Compost`; inspect archive format, split variants if practical, decimate for repeated alley use | Real bag/soft-prop stand-in; Homeless cart/tarp cluster; Day Labor landscaping pile |
| Handsaw Wood | https://polyhaven.com/a/handsaw_wood | CC0 | Blend, glTF, USD, FBX, textures; 3K tris, 0.6 m long | `DayLabor/Tools/Handsaw_Wood`; glTF preferred, add simple pickup collision and hand socket | Day Labor tool pickup/worksite prop |
| Universal Base Characters | https://quaternius.com/packs/universalbasecharacters.html | CC0 | FBX, OBJ, glTF; rigged humanoids, about 13K tris average | `Shared/Characters/UniversalBase`; test humanoid retarget, use one regular-proportion variant as guard prototype | Meter guard mesh; optional Vending clerk silhouette; later NPC workers |
| Car Kit | https://kenney.nl/assets/car-kit | CC0 | Kenney 3D download archive; 45 files; verify included interchange formats before import | `MeterDriveBy/Environment/ParkedCars/KenneyCarKit`; select a small dressing subset, remove gameplay scripts, generate cheap collision/LODs | CC0 parked cars for Meter Drive-By dressing; later urban lots |
| Downtown City MegaKit | https://quaternius.com/packs/downtowncitymegakit.html | CC0 | FBX, glTF; free tier contains roughly 60–70% of 300+ models | `Shared/Environment/Urban/QuaterniusDowntown`; catalogue/select only storefront, curb, barrier, alley, and street modules—do not import entire pack | Vending facade; curb/barrier gaps; alley and city-block dressing |
| Factory Kit | https://kenney.nl/assets/factory-kit | CC0 | Kenney 3D download archive; 140 files; animated/variation assets; verify included formats | `Shared/Environment/Industrial/KenneyFactory`; select only panels, conveyors, warehouse/site props after visual audit | Copper junction/interior dressing; Vending stock-room; Day Labor industrial site |
| Input Prompts | https://kenney.nl/assets/input-prompts | CC0 | SVG and PNG, 64 px and 128 px variants; 1,500 files | `ForgePlay/UI/InputPrompts/Kenney`; keep vector source, import only active device families, bind by semantic action | ForgePlay prompt UI; rebinding/device-switch glyph coverage |
| Interface Sounds | https://kenney.nl/assets/interface-sounds | CC0 | Audio download archive; 100 files; verify WAV/OGG contents and loudness after download | `ForgePlay/Audio/UI/KenneyInterface`; audition a small subset for chime/win/fail candidates and normalize non-destructively | Vending chime; ForgePlay win/fail stingers; prompt/menu feedback |

## Licence verification

- Every listed asset page explicitly states Creative Commons CC0.
- Kenney’s support page additionally states that assets on its asset pages are public-domain/CC0 and may be used commercially without attribution: https://kenney.nl/support
- No NC, attribution-only, editorial-only, or ambiguous assets are included.
- No quarantine entry was required in this batch.

## Import triage

1. First-pass downloads, if approved by the human: Plastic Crate 02, Cardboard Box 01, Handsaw Wood, Universal Base Characters, Car Kit, and Input Prompts.
2. Treat Downtown City MegaKit and Factory Kit as selection libraries. Do not bulk-import either archive into the project.
3. Confirm exact archive formats for Kenney 3D/audio packs after download because the public asset pages list file counts and licence but not every contained extension.
4. Use glTF/GLB where offered; generate Unreal-ready collision and LODs instead of shipping raw high-resolution dressing assets.
5. Record the included licence file and source URL alongside any later imported subset.

