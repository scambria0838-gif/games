# Homeless + Day Labor — cart-push & carry weight feel (portable)

## Supports

- **MECHANICS_MASTER_LIST · III Homeless Hustle:** `Cart push (walk-coupled or ride toggle)` — Status NEED
- **MECHANICS_MASTER_LIST · III Homeless Hustle:** `Fatigue / stamina while pushing` — Status NEED
- **MECHANICS_MASTER_LIST · III Homeless Hustle:** `Scavenge interact (dumpster dive hold)` — Status NEED
- **MECHANICS_MASTER_LIST · IV Day Labor:** `Walk + carry heavy object` — Status NEED
- **MECHANICS_MASTER_LIST · IV Day Labor:** `Place / stack job props` / `Fatigue + rest break` — Status NEED
- **ASSET_MASTER_LIST · III:** `Cart + tarp` PARTIAL; **IV:** `Lumber / pallet / drywall` NEED
- **ASSET_MASTER_LIST · I:** `Cart + rider kit` / `Plain cart` HAVE (reuse meshes)

## Source

- Character controller walk base: `GAME SKILLS\2026-07-27_physics-character-controller-fp-tp.md`
- Interaction hold offers: `EXTRA SKILS\...\operation-mythology-mechanics-20260727-015215.md`
- Carry as capability / locomotion modifier spirit: downed/carry interfaces in `operation-mythology-mechanics-20260727-180820.md` (portable: weight slows move; presentation follows)
- MD-B cart orientation skill for mesh reuse: `meter-driveby-rider-cam`

## Apply path (Three.js / shared locomotion)

1. **Cart-push mode:** walk intent applies force to cart proxy; player stays at handle end (reuse MD-B rider seating idea without ride physics). Toggle Ride only if sim allows.
2. Feel while pushing: FOV slight pinch when stamina low, nose-dip on start/stop, tarp/cloth sway cosmetic, tire scrub SFX ∝ speed.
3. Fatigue: stamina drain on push/sprint; below threshold → desat vignette + slower accel (sim owns rates); rest break recovers with warm UI pulse.
4. **Dumpster dive:** same hold-to-interact as Vending pry (shared module); progress radial + muffled audio bed duck.
5. **Carry heavy:** attach prop to hands socket; moveSpeed × `carrySlow`; camera height −ε; footsteps heavier SFX; jump disabled.
6. Place/stack: on Interact release near snap volume → short settle juice (dust puff + thud cue); bad place → reject shake (low intensity).
7. Soft social bump (Homeless): use soft-collision cue (meter bump cousin), not wreck.
8. All weight/fatigue numbers from sim/GameSpec; presentation only scales juice.

## Cross-links

- **Agent B:** cart tarp, tent/blanket piles, redeemables; lumber/pallet/drywall; cone/sawhorse; construction SFX.
- **Agent D:** cart-push vs walk toggle, fatigue clocks, carry capacity, stack snap volumes.
- **Agent C:** `locomotion: cartPush | walkCarry`, `stamina.drain`, `stamina.recover`, `carry.slowMult`, `dive.holdSec`.
