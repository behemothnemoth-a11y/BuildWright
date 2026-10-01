# DROP 0007 — Whole-Building Compiler

Major direct-repository update. This folds the earlier DROP 0006 graph design into one implemented whole-building layer.

## Added

- named module graph with cardinal and up/down ports
- direct shared-wall / shared-floor attachment
- illegal-overlap rejection
- deterministic straight corridor compilation
- project coordinate normalization
- solved-project source + provenance manifest + SVG graph plan
- exposed-side facade compiler
- four first-pass facade profiles
- flat / gable / hip / mansard roof massing
- per-module roof overrides
- lightweight ground and path site assembly
- three committed deterministic project examples
- strict project-example recompilation check
- whole-building unit tests
- master Litematic readback validation

## Maturity

All generated whole-building examples remain OFFLINE_COMPILED / LIVE_GAME_PENDING until reviewed in Minecraft.
