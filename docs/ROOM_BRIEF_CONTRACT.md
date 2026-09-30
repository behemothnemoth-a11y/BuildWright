# Room Brief Contract

A composition brief describes *constraints and intent*, not every block.

Minimum example:

```json
{
  "schema_version": 1,
  "id": "library_west",
  "stage": "vanilla",
  "template": "library",
  "size": [45, 15, 33],
  "style_profile": "style.massive_gothic_manor",
  "palette": "composition.massive_gothic_manor",
  "seed": 42
}
```

## Important fields

### `size`

`[width, height, depth]` in whole Minecraft blocks. The compiler never silently expands a room to fit a fixture.

### `template`

A reusable spatial grammar such as `library`, `grand_hall`, or `industrial_lab`.

### `style_profile`

Existing BuildWright style weighting. It influences fixture-family scoring but does not override functional constraints.

### `palette`

A shape-preserving remap preset. Palettes should change material language without turning stairs into full blocks or destroying fixture topology.

### `seed`

All optional selection is deterministic. The same repo, brief, seed and compiler version should produce byte-identical output.

### `fixture_policy`

Controls density, repeat limits, allowlists and exclusions. Density affects optional slots only. Required slots never disappear because of density.

### `connectors`

Functional doors, passages or future-module interfaces. These reserve keepout space before selection and are re-carved after placement.

### `keepouts`

Explicit boxes where fixtures may not be placed. Use them for circulation, sightlines, elevator shafts, stair continuation, future doors, redstone access, or protected landmarks.

### `slots`

Project-specific additions or overrides. They use the same selection grammar as template slots.

## Rule

A brief is allowed to be sparse. If every asset position is manually hard-coded into every brief, the composition system has failed to provide reusable architecture.
