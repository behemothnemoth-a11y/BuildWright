# BuildWright

BuildWright is a reusable Minecraft architecture system for building, refining, composing, validating and releasing high-detail projects.

The system now has four concrete layers:

1. **Vanilla Build Language** — 68 reusable families / 567 variants plus builder techniques, palettes and style profiles.
2. **Microblock Implementation** — 75 families / 606 variants, 40 cell primitives, detail tiers and Astra-aware translation planning.
3. **Compiled Fixture Library** — 40 real vanilla `.litematic` fixtures, 24 real Astra-host fixtures and a 32-case transform corpus with editable canonical source.
4. **Composition Compiler** — room/module briefs → deterministic fixture selection → connector-aware placement → palette remap → canonical module source → validated `.litematic`.

## Core rules

- Strong architecture before ornament.
- Player scale before spectacle.
- Vanilla remains a first-class release target.
- Microblocks refine contour/trim/thinness; they do not replace primary massing.
- Prefer the coarsest microblock tier that reads correctly.
- Functional behavior beats geometric cleverness.
- Connectors and circulation are authoritative constraints, not decoration.
- Negative space is part of detail.
- Canonical source is editable; compiled `.litematic` files are derived artifacts.
- Seeded variation must remain reproducible.
- Serialization/composition validation is not the same thing as an in-game test.

## Composition quick start

```powershell
python tools/plan_composition.py examples/composition/gothic_library_demo.json `
  --svg .buildwright/generated/library-plan.svg

python tools/compile_module.py examples/composition/gothic_library_demo.json `
  --output-dir .buildwright/generated/library
```

See `docs/COMPOSITION_COMPILER.md`, `docs/ROOM_BRIEF_CONTRACT.md`, `VANILLA_BUILD_LANGUAGE.md`, `MICROBLOCK_IMPLEMENTATION.md`, and `docs/FIXTURE_SYSTEM.md`.


BuildWright 0.5.1 makes composition example serialization byte-stable across Windows/Linux by canonicalizing generated text to UTF-8 LF.
