# BuildWright

BuildWright is a reusable Minecraft architecture system for building, refining, composing, validating and releasing high-detail projects.

The system now has six concrete layers:

1. **Vanilla Build Language** — 68 reusable families / 567 variants plus builder techniques, palettes and style profiles.
2. **Microblock Implementation** — 75 families / 606 variants, 40 cell primitives, detail tiers and Astra-aware translation planning.
3. **Compiled Fixture Library** — 40 real vanilla `.litematic` fixtures, 24 real Astra-host fixtures and a 32-case transform corpus with editable canonical source.
4. **Composition Compiler** — room/module briefs → deterministic fixture selection → connector-aware placement → palette remap → canonical module source → validated `.litematic`.
5. **Whole-Building Compiler** — compiled modules → graph solve → shared-wall/vertical alignment → corridors → facade/roof/site passes → master `.litematic`.
6. **Universal Style & Exterior System** — project-neutral architectural language profiles, facade zoning, semantic material roles, style blending, window families, roof families and site intent.

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

## Whole-building quick start

```powershell
python tools/compile_project.py examples/projects/wayne_manor_phase_a.json `
  --output .buildwright/generated/wayne-phase-a
```

BuildWright 0.8.1 keeps the compiler project-neutral: the same graph/composition engine can drive Gothic, classical, modern, industrial, vernacular, East Asian, desert, speculative, fantasy, ancient and organic architectures. The universal library contains 35 core style profiles across 14 architectural families, plus style blending and facade zoning.

Start with [VISUAL_CATALOG.md](VISUAL_CATALOG.md) for the picture-first asset browser, or [CATALOG.md](CATALOG.md) for the full inventory and history.

Core docs: `docs/UNIVERSAL_STYLE_SYSTEM.md`, `docs/PROJECT_GRAPH_COMPILER.md`, `docs/EXTERIOR_ENVELOPE_AND_FACADE.md`, `docs/ROOF_COMPILER.md`, `docs/SITE_ASSEMBLY.md`, `docs/COMPOSITION_COMPILER.md`, `VANILLA_BUILD_LANGUAGE.md`, and `MICROBLOCK_IMPLEMENTATION.md`.
