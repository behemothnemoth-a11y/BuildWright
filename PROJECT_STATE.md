# BuildWright Project State

## Platform

- Minecraft target: Java 26.2
- Primary schematic target: Litematica
- DataVersion target: 4903
- Vanilla-first: LOCKED
- Selective microblock second pass: LOCKED
- In-game player-eye review required for approval: YES

## System maturity after DROP 0007

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
- Cardinal connector alignment: IMPLEMENTED
- Explicit up/down floor connector alignment: IMPLEMENTED
- Shared-wall attachment and collision QA: IMPLEMENTED
- Straight deterministic corridor compiler: IMPLEMENTED
- Exterior facade exposure analysis: IMPLEMENTED
- Facade profiles: IMPLEMENTED — massive Gothic manor / classic manor / industrial / modern
- Roof massing compiler: IMPLEMENTED — flat / gable / hip / mansard / per-module overrides
- Lightweight site/ground compiler: IMPLEMENTED
- Canonical solved-project source + manifest + SVG plan + master Litematic: IMPLEMENTED
- Committed whole-building regression corpus: IMPLEMENTED — 3 projects
- Whole-building deterministic recompilation gate: IMPLEMENTED
- Real Minecraft/Fabric/Litematica whole-building smoke gate: PENDING

## Current project — Wayne Manor + Batcave

- Wayne Manor vanilla master remains the project source of truth.
- Grand Hall architecture: active refinement.
- Grand Hall split stair connectors remain functional circulation into future rooms.
- Grand Hall roof/ceiling: active refinement; visual-noise control remains a priority.
- Batcave: blockout / early detailing.
- Wayne Manor microblock edition: NOT STARTED as a project-wide conversion.
- BuildWright now includes a generated `wayne_manor_phase_a` regression project, but it is a compiler proof and is NOT an approved replacement for the hand-refined manor.
- Whole-building generated outputs remain `LIVE_GAME_PENDING` until loaded and reviewed in Minecraft.

## DROP 0007 direction

The earlier DROP 0006 graph design has been folded into this major update. BuildWright can now compile a room graph into a coherent master schematic with circulation, facade, roof and site passes. The next priority is to increase exterior intelligence rather than merely add more decoration: facade zoning, towers, dormers, buttresses, balconies, roof intersections, terrain-aware foundations and project-scale vegetation.
