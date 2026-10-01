# BuildWright Roadmap

## DROP 0001C — Repository Foundation
Complete.

## DROP 0002 — Vanilla Pack Foundations
Complete.

## DROP 0003 — Microblock Pack Foundations
Complete.

## DROP 0004 — Compiled Asset Fixtures
Complete.

## DROP 0005 — Composition Compiler
Complete in this drop:

- room/module brief contract;
- 11 reusable spatial templates;
- 8 shape-preserving composition palettes;
- deterministic fixture selection and repeat penalties;
- style-profile weighting;
- connector and keepout protection;
- collision-safe placement;
- shell construction and connector re-carve;
- vanilla + Astra microblock fixture assembly;
- palette remapping;
- canonical composed-module source;
- composition manifest/provenance;
- top-down SVG plans;
- Litematic compile + independent readback;
- 7 committed example modules;
- deterministic example recompilation gate;
- composition schemas, tools and tests.


## DROP 0005B — Composition Compiler Reproducibility Hotfix
Complete in this hotfix:
- canonical UTF-8/LF generated JSON and SVG outputs;
- Git LF attributes for committed composition examples;
- regression test for cross-platform line endings;
- byte-for-byte validation remains strict.

## DROP 0007 — Whole-Building Compiler
Complete in this major direct-repo update. The earlier DROP 0006 graph design is folded into this implementation.

- module-to-module connector graph;
- cardinal and explicit up/down ports;
- direct shared-wall attachment;
- floor-to-floor alignment;
- collision rejection for illegal room overlaps;
- deterministic straight corridor compilation;
- whole-building coordinate normalization;
- canonical solved project source;
- project manifest and SVG graph plan;
- facade exposure analysis;
- Gothic/classic/industrial/modern facade profiles;
- plinth, pier, window, sill/header and cornice passes;
- flat/gable/hip/mansard roof massing;
- per-module roof overrides;
- lightweight ground/site assembly;
- deterministic committed whole-building examples;
- master Litematic export + independent readback;
- whole-building tests and strict recompilation gate.

## DROP 0008 — Universal Style & Exterior System

Complete in this major direct-repo update:

- 35 project-neutral architectural profiles across 14 style families;
- semantic material roles for wall, structure, trim, accent, glass, plinth and roof;
- primary/secondary style blending with explicit material overrides;
- hero/primary/secondary/service/courtyard/blind facade zoning;
- broader facade rhythm, depth, verticality and ornament controls;
- expanded window languages for historic, modern, industrial, cultural, fantasy, ruin and organic builds;
- expanded roof languages including shed, butterfly, sawtooth, pagoda/tiered, dome, vault, terrace and ruin modes;
- style-aware site character and vegetation intent;
- deterministic style registry generator and validator;
- 37 committed cross-style showcase compiles (35 core styles + 2 blend demonstrations);
- living human-readable CATALOG.md plus machine-readable catalog/catalog.json;
- deterministic catalogue generation and validation.

## DROP 0008B — Visual Catalogue

Complete in this follow-up:

- picture-first GitHub asset browser;
- 64 fixture previews integrated into browsable galleries;
- deterministic isometric Litematic renderer with simplified material colors;
- automatic cutaway views for room/module interiors;
- 7 rendered room/module examples;
- 3 rendered whole-building regression projects;
- all 35 core style profiles rendered;
- 2 hybrid style demonstrations rendered;
- overview contact sheets for fixtures, rooms, projects and styles;
- machine-readable visual manifest;
- visual-catalog validation integrated into the repository gate.

## DROP 0008C — Vanilla Baseline Separation

Complete in this corrective follow-up:

- main visual catalogue is vanilla-only;
- Astra assets retained but moved to a separate optional refinement catalogue;
- hybrid microblock proof removed from the vanilla room gallery;
- style showcase renders explicitly relabeled as vanilla style baselines;
- vanilla-first progression locked in documentation and agent rules;
- validator scans baseline Litematics and fails on any Astra namespace leakage.

## DROP 0009 — Complete Vanilla Detail Layer

Complete:

- 45 new compiled vanilla detail fixtures; 85 vanilla fixtures total;
- 10 deterministic room-role detail profiles;
- secondary architecture passes: perimeter/crown trim, restrained beams and floor accents;
- functional furniture and furnishing passes;
- decor and storytelling population;
- vanilla lighting fixtures and whole-building exterior lighting rhythm;
- vegetation / garden / planter detail;
- industrial and workshop service-detail passes;
- deterministic collision-aware fallback placement and anti-repetition density control;
- 10 committed VANILLA_DETAIL_COMPLETE room-role regressions;
- whole-building vanilla finishing engine for entrances, planting, roof/service detail and context cues;
- 3 committed VANILLA_DETAIL_COMPLETE whole-building regressions;
- catalogue/visual separation between BASELINE and VANILLA_DETAIL_COMPLETE;
- hard Astra-namespace scan across both vanilla baselines and detail-complete outputs;
- microblock work remains downstream and optional.

## DROP 0010 — Structural & Site Intelligence

Complete:

- deterministic routed orthogonal corridors that preserve explicit module origins;
- stair-flight generation between unequal floor elevations;
- reusable tower, porch, balcony, buttress-run and dormer-row graph nodes;
- terrain/elevation-aware foundation engine with perimeter, pier and solid modes;
- project-scale path, road, plaza, wall, fence, retaining-wall and site-stair networks;
- richer site statistics and structural provenance in project manifests;
- 3 deterministic pure-vanilla structural/site regression projects;
- visual catalogue integration for structural/site projects;
- strict byte-for-byte recompilation and Astra-namespace exclusion.

## DROP 0011 — Style-Specific Finish & Reference Fitting

Next major priority:

- style-family-specific vanilla finishing profiles beyond generic room-role defaults;
- facade zoning by story/elevation and urban frontage context;
- terrain/profile ingestion and better grade-aware site solving;
- richer project-scale vegetation/landscape graphs;
- measured-reference facade fitting for real-world reconstruction;
- reference/image → structured project graph assistance;
- stronger circulation QA across large campuses/estates;
- project-aware roof intersection and tower/dormer reconciliation.

## Later

- Fabric-side automated whole-building smoke tests;
- Axiom-assisted placement workflows;
- Build Studio adapter;
- registry-aware palette/material resolver;
- project-level vanilla → microblock diff planner.
