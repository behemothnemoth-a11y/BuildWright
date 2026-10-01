# Microblock Implementation

BuildWright Stage B begins only after the vanilla master is structurally strong and has passed its vanilla review gate.

DROP 0003 provides **75 reusable microblock families / 606 variants**, a 16-grid shape grammar, provider profile, translation map, detail profiles, planners and validators.

## Core law

**Microblocks refine a strong vanilla build. They do not replace architectural thinking.**

Use full vanilla blocks for primary massing, circulation, major floors, structural volumes and behavior-sensitive blocks. Use microblocks for contour, trim, carving, lattice, molding, thin members, sculptural transitions, furniture refinement and localized hero detail.

## Required pipeline

```text
approved vanilla candidate
→ candidate classification
→ provider/material capability gate
→ detail-profile budget
→ translation plan
→ coarse-to-fine microblock pass
→ transform/material validation
→ player-eye QA
→ hybrid candidate
```

## Candidate classes

- `KEEP_VANILLA` — already reads well or behavior/quiet surface should remain vanilla.
- `GOOD_MICROBLOCK_TARGET` — contour/depth clearly benefits.
- `OPTIONAL_MICROBLOCK` — use only if focal composition or style requires it.
- `DO_NOT_CONVERT` — functional/provider-incompatible/performance-critical geometry.

## Resolution tiers

- **TIER 0** — vanilla only.
- **TIER 1** — coarse quarter-block trim and contour.
- **TIER 2** — architectural eighth-block contour.
- **TIER 3** — fine 1/16 detail, localized.
- **TIER 4** — hero sculptural detail, sparse.

Always prefer the coarsest tier that reads correctly from the intended viewing distance.

## Noise-control rule

Microblocks make it easy to produce technically impressive but visually noisy work. The build hierarchy remains:

```text
primary mass
→ secondary architecture
→ tertiary trim/furniture
→ micro detail
```

If microblocks obscure that hierarchy, simplify.

See `docs/MICROBLOCK_TRANSLATION_PIPELINE.md` and `packs/microblock/registry.json`.

## DROP 0009 gate

Microblock candidate analysis is downstream of `VANILLA_DETAIL_COMPLETE` and player-eye review. Astra Microblocks may refine localized contour, thinness or hero sculptural detail; they are not permitted to compensate for incomplete vanilla furnishing, lighting, landscaping, service detail or storytelling.
