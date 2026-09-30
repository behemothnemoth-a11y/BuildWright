# BuildWright

BuildWright is a repository for building, refining, validating, and releasing high-detail Minecraft architectural projects.

The project deliberately separates two build stages:

1. **Vanilla Build Language** — every project must first become a strong, player-scale, fully vanilla Minecraft build using high-end builder techniques, reusable architecture packs, furniture/decor packs, vegetation packs, controlled gradients, depth, negative space, and in-game QA.
2. **Microblock Implementation** — only after the vanilla master is strong may selected geometry be translated into microblocks for finer contour, carving, lattice, trim, sculptural transitions, furniture refinement, and hero details.

Wayne Manor + Batcave is the first full project using this system.

## Core principles

- Strong architecture before ornament.
- Player scale before spectacle.
- Large readable forms before micro-detail.
- Depth before random texture.
- Controlled gradients instead of block noise.
- Negative space is part of detailing.
- Reusable packs should provide families and variation, not copy-pasted prefabs.
- Vanilla remains a first-class release target.
- Microblocks refine strong vanilla architecture; they do not rescue weak architecture.
- Every significant build change should be tested from player eye level in Minecraft.

## Repository layout

```text
BuildWright/
├─ AGENTS.md
├─ PROJECT_STATE.md
├─ VANILLA_BUILD_LANGUAGE.md
├─ MICROBLOCK_IMPLEMENTATION.md
├─ ROADMAP.md
├─ docs/
├─ packs/
├─ projects/
├─ releases/
├─ references/
├─ schemas/
└─ tools/
```

See `docs/BUILD_PIPELINE.md` for the full workflow.
