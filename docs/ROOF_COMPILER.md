# Roof Compiler

Whole-building compilation can generate roof massing after room placement.

Supported first-pass roof styles:
- flat
- gable
- hip
- mansard
- none

Roof configuration is global with per-module overrides.

## Rules

- Roofs are added after module composition and facade exposure is resolved.
- Large roof planes should read as large shapes first.
- Individual modules may opt out when they represent courtyards, terraces, cave spaces or an upper floor under another module.
- Gable-end closure is generated so roofs read as actual exterior volumes.

The roof compiler is for coherent whole-building massing. Interior hero ceilings such as Wayne Manor's Grand Hall hammerbeam roof remain hand-refinable modules and should not be overwritten blindly.
