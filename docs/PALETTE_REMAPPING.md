# Palette Remapping

Composition palettes are not random texture filters.

They remap fixture materials while preserving topology and block-state properties wherever the current compiler has a safe shape-family mapping.

For example, the Massive Gothic Manor palette can translate:

```text
stone bricks                -> tuff bricks
stone brick stairs          -> tuff brick stairs
stone brick slabs           -> tuff brick slabs
polished blackstone bricks  -> deepslate tiles
spruce / oak wood family    -> dark oak family
```

The facing/axis/connection properties on the resulting state are retained.

## Why shape families matter

Replacing `stone_brick_stairs` with `tuff_bricks` would destroy a fixture. The compiler therefore maps a source material family and its shape separately.

## Current safe families

DROP 0005 contains explicit shape mappings for the fixture library's current masonry and wood families. Unknown states remain unchanged rather than being guessed.

## Shell palette

Each composition palette also defines default floor, wall and ceiling materials. A room brief may override any shell material without changing fixture remapping.

## Future work

A later registry-aware material resolver can expand this beyond the current known family set and validate replacement states against the live Minecraft registry.
