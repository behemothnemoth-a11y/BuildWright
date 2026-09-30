# BuildWright

BuildWright is a reusable Minecraft architecture system for building, refining, validating and releasing high-detail projects.

The system now has three concrete layers:

1. **Vanilla Build Language** — 68 reusable families / 567 variants plus techniques, palettes and style profiles.
2. **Microblock Implementation** — 75 families / 606 variants, 40 cell primitives, detail tiers and Astra-aware translation planning.
3. **Compiled Fixture Library** — 40 real vanilla `.litematic` fixtures, 24 real Astra-host `.litematic` fixtures and 32 transform-corpus files with editable source JSON, previews and offline readback validation.

## Core rules
- Strong architecture before ornament.
- Player scale before spectacle.
- Vanilla remains a first-class release target.
- Microblocks refine contour/trim/thinness; they do not replace primary massing.
- Prefer the coarsest microblock tier that reads correctly.
- Functional behavior beats geometric cleverness.
- Negative space is part of detail.
- Source JSON is canonical; compiled `.litematic` files are derived artifacts.
- Serialization validation is not the same as an in-game test.

See `VANILLA_BUILD_LANGUAGE.md`, `MICROBLOCK_IMPLEMENTATION.md`, `docs/FIXTURE_SYSTEM.md`, and `docs/BUILD_PIPELINE.md`.
