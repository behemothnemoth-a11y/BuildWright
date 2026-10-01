# BuildWright Project State

## Platform

- Minecraft target: Java 26.2
- Primary schematic target: Litematica
- DataVersion target: 4903
- Vanilla-first: LOCKED
- Selective microblock second pass: LOCKED
- In-game player-eye review required for approval: YES

## System maturity after DROP 0010

- Vanilla pack foundation: IMPLEMENTED — 68 families / 567 variants
- Microblock pack foundation: IMPLEMENTED — 75 families / 606 variants
- Microblock shape primitives: IMPLEMENTED — 40
- Compiled vanilla fixture library: IMPLEMENTED — 85 fixtures
- Vanilla finishing/detail fixtures: IMPLEMENTED — 45 fixtures
- Compiled Astra microblock fixture library: IMPLEMENTED — 24 fixtures
- Rotation/mirror corpus: IMPLEMENTED — 32 cases
- Composition templates: IMPLEMENTED — 11
- Composition palettes: IMPLEMENTED — 8
- Deterministic room/module composition compiler: IMPLEMENTED
- Whole-building project graph solver: IMPLEMENTED
- Cardinal + explicit up/down connector alignment: IMPLEMENTED
- Shared-wall/floor attachment and collision QA: IMPLEMENTED
- Straight deterministic corridor compiler: IMPLEMENTED
- Routed orthogonal corridor compiler: IMPLEMENTED
- Elevation stair compiler: IMPLEMENTED
- Structural graph nodes: IMPLEMENTED — tower / porch / balcony / buttress_run / dormer_row
- Foundation engine: IMPLEMENTED — perimeter / piers / solid
- Project-scale site networks: IMPLEMENTED — path / road / plaza / wall / fence / retaining_wall / stairs
- Structural/site regression corpus: IMPLEMENTED — 3 pure-vanilla projects
- Universal architectural style profiles: IMPLEMENTED — 35 profiles / 14 families
- Semantic material-role system: IMPLEMENTED
- Primary/secondary style blending: IMPLEMENTED
- Facade zoning: IMPLEMENTED — hero / primary / secondary / service / courtyard / blind
- Broad window-language compiler: IMPLEMENTED
- Expanded roof-language compiler: IMPLEMENTED
- Site-character language: IMPLEMENTED
- Compiled style regression corpus: IMPLEMENTED — 37 showcases (35 core + 2 hybrids)
- Whole-building regression corpus: IMPLEMENTED — 3 projects
- Living inventory catalogue: IMPLEMENTED — CATALOG.md + catalog/catalog.json
- Main picture-first catalogue: IMPLEMENTED — VISUAL_CATALOG.md — VANILLA ONLY
- Optional refinement catalogue: IMPLEMENTED — MICROBLOCK_CATALOG.md
- Vanilla room-role detail profiles: IMPLEMENTED — 10
- VANILLA_DETAIL_COMPLETE room regressions: IMPLEMENTED — 10
- Whole-building vanilla finishing engine: IMPLEMENTED
- VANILLA_DETAIL_COMPLETE project regressions: IMPLEMENTED — 3
- Vanilla visual assets: IMPLEMENTED — 85 fixtures + 6 room baselines + 10 detailed rooms + 3 project baselines + 3 detailed projects + 3 structural/site projects + 37 style baselines
- Optional Astra visual assets: RETAINED SEPARATELY — 24 fixtures + 1 hybrid proof room
- Automatic room cutaway rendering: IMPLEMENTED
- Vanilla-output Astra namespace validation: IMPLEMENTED
- Deterministic project/style/detail/catalog validation gates: IMPLEMENTED
- Visual catalogue coverage validation: IMPLEMENTED
- Real Minecraft/Fabric/Litematica whole-building/style smoke gate: PENDING

## Universal engine rule

BuildWright is a general-purpose architecture/build system. Named projects such as Wayne Manor are regression/use-case projects, not universal defaults. Core profiles and compiler behavior must remain usable across historical, modern, industrial, vernacular, East Asian, desert, speculative, fantasy, ancient, organic, real-world reconstruction and experimental builds.

## Current project — Wayne Manor + Batcave

- Wayne Manor vanilla master remains the project source of truth.
- Grand Hall architecture: active refinement.
- Grand Hall split stair connectors remain functional circulation into future rooms.
- Grand Hall roof/ceiling: active refinement; visual-noise control remains a priority.
- Batcave: blockout / early detailing.
- Wayne Manor microblock edition: NOT STARTED as a project-wide conversion.
- The generated wayne_manor_phase_a artifact remains a compiler proof, not approved canon.

## Vanilla-first implementation rule

The style/showcase and whole-building outputs currently catalogued are **vanilla baselines**. They establish architecture, massing, palette, facade rhythm, roof language and basic site intent. They are not the final vanilla detail layer.

The required order is now explicit:

1. vanilla massing / structural base;
2. complete vanilla architecture and circulation;
3. complete vanilla detailing, furnishing, lighting, vegetation and storytelling;
4. player-eye / in-game review;
5. optional localized Astra Microblocks refinement.

## DROP 0009 status

The reusable **complete vanilla detail layer is implemented**. Ten room-role profiles now cover secondary architecture, furnishing, decor/storytelling, lighting, vegetation and service detail. Whole-building finishing adds restrained entrances, exterior lighting, planting, roof/service details and context cues.

`VANILLA_DETAIL_COMPLETE` is an offline compiler maturity state, not automatic approval. In-game/player-eye review is still mandatory.

## DROP 0010 status

Structural and site intelligence is implemented on top of the completed vanilla pipeline. Project briefs can now express routed corridors, elevation stairs, reusable structural nodes, terrain-aware foundations, and explicit site networks. Three deterministic pure-vanilla regression projects exercise those systems.

These remain offline regression outputs. They still require in-game/player-eye review before any project-specific geometry is approved.

## Next major priority

Deepen **style-specific vanilla finishing and real-world fitting**: frontage/story zoning, style-family finishing profiles beyond generic room roles, measured-reference facade fitting, terrain/profile ingestion, richer landscape graphs, and better automated circulation QA. Microblocks remain downstream and optional.
