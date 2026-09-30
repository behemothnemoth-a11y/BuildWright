# BuildWright

BuildWright is a reusable Minecraft architecture system for building, refining, validating and releasing high-detail projects.

The pipeline is deliberately two-stage:

1. **Vanilla Build Language** — strong player-scale vanilla architecture, palettes, furniture, vegetation, lighting and builder technique packs.
2. **Microblock Implementation** — selective high-resolution refinement after the vanilla master is already good.

DROP 0002 established **68 vanilla families / 567 variants**. DROP 0003 adds **75 microblock families / 606 variants**, 40 reusable shape primitives, 10 detail profiles and a provider-aware vanilla→microblock planning layer.

## Core rules
- Strong architecture before ornament.
- Player scale before spectacle.
- Vanilla remains a first-class release target.
- Microblocks refine contour/trim/thinness; they do not replace primary massing.
- Prefer the coarsest microblock tier that reads correctly.
- Functional behavior beats geometric cleverness.
- Negative space is part of detail.
- Every significant result needs in-game player-eye review.

See `VANILLA_BUILD_LANGUAGE.md`, `MICROBLOCK_IMPLEMENTATION.md`, and `docs/BUILD_PIPELINE.md`.
