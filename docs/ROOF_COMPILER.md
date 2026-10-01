# Roof Compiler

Whole-building compilation can generate style-aware roof massing after module placement.

## Supported roof languages

- flat / mechanical flat
- gable / steep gable / low gable / swept gable
- hip
- mansard
- shed
- butterfly
- sawtooth
- pagoda / tiered
- dome / dome-flat
- vaulted mass
- terraced / green terrace
- ruined
- none

Style profiles provide a default roof language, material, overhang and step/run. Project briefs may override these globally or per module.

## Rules

- Roofs are project-scale massing, not a substitute for hand-authored hero ceilings.
- Large roof planes should read as large structural ideas first.
- Courtyards, terraces, caves and stacked lower modules may opt out.
- Semantic roof names map to deterministic coarse geometry rather than decorative noise.
- Project-specific hero roofs can remain authored modules and bypass the generic pass.

The compiler should eventually reason about roof intersections, dormers, towers, valleys and drainage as graph-level relationships rather than independent module hats.
