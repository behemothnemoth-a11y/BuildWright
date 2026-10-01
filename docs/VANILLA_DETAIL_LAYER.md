# Complete Vanilla Detail Layer

BuildWright 0.9 adds a reusable finishing stage between the architectural baseline and any optional microblock work.

## Locked order

```text
vanilla massing / room graph
→ primary vanilla architecture
→ secondary vanilla architecture
→ vanilla furnishing
→ vanilla decor + storytelling
→ vanilla lighting
→ vanilla vegetation / landscape
→ vanilla service + functional detail
→ VANILLA_DETAIL_COMPLETE
→ in-game / player-eye review
→ optional localized Astra Microblocks refinement
```

Microblocks are not a substitute for this stage. A build that only reads correctly after microblock conversion has failed the vanilla stage.

## Room-role profiles

The module detail compiler currently has ten profiles:

- default
- bedroom
- dining
- gallery
- garden
- hall
- industrial
- library
- tavern
- workshop

Profiles are stored in `composition/detail_profiles.json`. A profile controls surface passes, deterministic fixture recipes, density, and style-specific reductions.

A composition brief enables the layer with:

```json
{
  "vanilla_detail": {
    "enabled": true,
    "density": 0.92
  }
}
```

The role is inferred from the spatial template unless explicitly supplied.

## Finishing passes

### Secondary architecture

Examples include perimeter trim, crown trim, restrained ceiling beams, floor inlays, wall-panel fixtures, doorway trim, window seats, and picture rails.

The same anti-noise rule used elsewhere in BuildWright applies: one readable architectural idea is better than continuous trim spam.

### Furniture

The detail library adds supporting furniture that is intentionally missing from the architectural blockout: wardrobes, dressers, nightstands, dining chairs/tables, lounge seating, kitchen counters/islands, workshop benches, tavern furniture and utility storage.

Placement is deterministic. Requested design zones are tried first; if they collide with existing architecture or circulation, the compiler searches outward for a nearby free pocket rather than forcing geometry through the room.

### Decor and storytelling

Rugs, paintings, banners, books, pottery, candles and restrained display pieces populate lived-in zones. Optional pieces may disappear when there is no safe placement.

### Lighting

The vanilla layer includes wall sconces, hanging lantern rows, table/floor lamps and recessed light strips. Whole-building finishing can add exterior lantern markers.

### Vegetation

Indoor plants, shrub clusters, flower beds, planters and vines provide vanilla landscape/detail coverage before any microblock vegetation refinement is considered.

### Service detail

Industrial/workshop profiles can add utility shelving, tool walls, valve banks, pallets, crate stacks and cable drops.

## Whole-building finishing

Project briefs can enable the project-scale finishing layer:

```json
{
  "vanilla_finish": {
    "enabled": true
  }
}
```

Current project finishing covers:

- exterior entrance pads and marker lighting;
- exposed-facade lighting rhythm;
- foundation planting for landscape-oriented site characters;
- style-family roof details such as chimneys or restrained service vents;
- industrial/speculative service storytelling.

The pass is deterministic and runs after facade, roof and site compilation.

## Detail fixtures

DROP 0009 adds 45 new vanilla detail fixtures, bringing the compiled vanilla fixture library to 85.

The detail fixtures remain ordinary Minecraft blocks and states. They are validated by the same Litematic readback/registry system as the original fixture library.

## Maturity

`VANILLA_DETAIL_COMPLETE` means the offline compiler has executed the complete vanilla finishing contract and the artifact passes structural/readback validation.

It does **not** mean APPROVED. The artifact is still `LIVE_GAME_PENDING` until it has been loaded, walked, viewed at player scale and accepted.

## Regression corpus

DROP 0009 commits:

- 10 detailed room-role examples;
- 3 detailed whole-building projects;
- the original 6 vanilla room baselines;
- the original 3 whole-building baselines;
- 37 style-language baselines.

The visual catalogue keeps BASELINE and VANILLA_DETAIL_COMPLETE artifacts visibly separate.
