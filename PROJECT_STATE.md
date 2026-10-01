# BuildWright Project State

## Platform

- Minecraft target: Java 26.2
- Primary schematic target: Litematica
- DataVersion target: 4903
- Vanilla-first: LOCKED
- Selective microblock second pass: LOCKED
- In-game player-eye review required for approval: YES

## System maturity after DROP 0008C

- Vanilla pack foundation: IMPLEMENTED — 68 families / 567 variants
- Microblock pack foundation: IMPLEMENTED — 75 families / 606 variants
- Microblock shape primitives: IMPLEMENTED — 40
- Compiled vanilla fixture library: IMPLEMENTED — 40 fixtures
- Compiled Astra microblock fixture library: IMPLEMENTED — 24 fixtures
- Rotation/mirror corpus: IMPLEMENTED — 32 cases
- Composition templates: IMPLEMENTED — 11
- Composition palettes: IMPLEMENTED — 8
- Deterministic room/module composition compiler: IMPLEMENTED
- Whole-building project graph solver: IMPLEMENTED
- Cardinal + explicit up/down connector alignment: IMPLEMENTED
- Shared-wall/floor attachment and collision QA: IMPLEMENTED
- Straight deterministic corridor compiler: IMPLEMENTED
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
- Vanilla visual assets: IMPLEMENTED — 40 fixtures + 6 room baselines + 3 project baselines + 37 style baselines
- Optional Astra visual assets: RETAINED SEPARATELY — 24 fixtures + 1 hybrid proof room
- Automatic room cutaway rendering: IMPLEMENTED
- Vanilla-baseline Astra namespace validation: IMPLEMENTED
- Deterministic project/style/catalog validation gates: IMPLEMENTED
- Visual catalogue coverage validation: IMPLEMENTED
- Complete vanilla detail/furnishing layer across style baselines: NOT YET SYSTEMATIZED
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

## Next major priority

Build the **complete vanilla detail layer** before expanding microblock usage: project-scale vanilla trim, furniture/decor population, lighting, landscape fixtures, service/detail zones, controlled clutter/storytelling, and style-specific finishing passes. Microblocks remain available, but they are downstream and optional.
