# Style-Specific Vanilla Finish & Reference Fitting

BuildWright 0.11 adds two project-neutral systems on top of the complete vanilla-detail pipeline:

1. **style-family finishing**, so Gothic, industrial, Japanese, classical, modern, fantasy, ancient, etc. do not receive the same generic exterior polish;
2. **measured-reference fitting**, so reconstruction projects can express dimensions and anchor targets as machine-checkable constraints.

## Style-family finishing

The family finishing layer is defined in `project_graph/style_finish_profiles.json`.

Current coverage is one profile for each of the 14 universal architectural families:

- ancient
- classical
- desert
- east_asian
- fantasy
- gothic
- historic_european
- industrial
- mediterranean
- modern
- modern_historic
- organic
- speculative
- vernacular

Each family controls deterministic biases such as:

- facade/body band placement;
- projecting corner structure;
- eave rhythm;
- exterior lighting rhythm;
- foundation planting;
- service runs;
- parapets;
- roof/corner finials.

The layer inherits semantic material roles from the active style profile, so a Japanese finish and an industrial finish can use the same finishing engine without sharing the same blocks or silhouette language.

If `vanilla_finish.enabled` is true, style-family finishing enables automatically unless explicitly overridden with `style_finish.enabled=false`.

The compiler records a `style_finish` object in canonical project source and manifests. A successful pass is marked `VANILLA_STYLE_FINISH_COMPLETE`.

## Reference fitting

A project brief may include a `reference_fit` object.

Supported constraints:

- whole-project target size;
- module origin;
- module size;
- named port world coordinate;
- facade length;
- facade height.

Every target may use a block tolerance. The project can run in:

- **advisory mode** — record drift but continue compiling;
- **strict mode** — fail compilation when any measured target exceeds tolerance.

Reference fitting is evaluated against the solved project graph before decorative/roof/site geometry expands the final Litematic envelope. This makes the measurements describe architectural control geometry rather than incidental decoration.

### Injecting measured module origins

For reconstruction work, `reference_fit.apply_module_origins=true` can inject measured origins into modules that do not already define one.

Example:

```json
{
  "reference_fit": {
    "enabled": true,
    "strict": true,
    "apply_module_origins": true,
    "tolerance": 1,
    "target_size": [120, 28, 86],
    "module_targets": [
      {"module": "main_hall", "origin": [0, 0, 0], "size": [45, 18, 61]},
      {"module": "east_wing", "origin": [44, 0, 15]}
    ],
    "port_targets": [
      {"module": "main_hall", "port": "front_entry", "target": [22, 1, 60]}
    ],
    "facade_targets": [
      {"module": "main_hall", "side": "south", "length": 45, "height": 18}
    ]
  }
}
```

## Regression corpus

BuildWright includes 14 committed style-family finish regressions under:

- `examples/style_finish/`
- `project_graph/style_finish_examples/`

The classical regression also exercises strict zero-tolerance reference fitting.

## Vanilla-only guarantee

Style-family finish and reference fitting are part of the vanilla pipeline. Their regression outputs are scanned for the `astra_microblocks:` namespace and must remain clean.

Microblocks remain an optional downstream refinement after the completed vanilla build has passed player-eye review.

## Maturity

A successful style finish or reference-fit compile remains an offline result. It does not imply that the build has been visually approved in Minecraft.
