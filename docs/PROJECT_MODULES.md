# Project Modules

Large builds should be decomposed into independently reviewable modules.

A module can represent architecture or a major subcomponent, for example:

```text
Grand Hall
├─ GH-ARCH      shell and primary room architecture
├─ GH-STAIR     staircase and connector circulation
├─ GH-CEIL      roof / ceiling structure
├─ GH-GALLERY   galleries and balustrades
├─ GH-WALL-*    major wall compositions
└─ GH-DETAIL    furniture, decor and player-eye clutter
```

## Module rules

- Changes should be scoped to named modules whenever practical.
- Connector coordinates belong to the project contract and must not drift accidentally.
- A ceiling refinement should not silently redesign stair exits.
- Module versions may progress independently.
- Approved modules can be merged into project master releases.

## Maturity

`CONCEPT -> BLOCKOUT -> ARCHITECTURE -> DETAILING -> REVIEW_CANDIDATE -> APPROVED -> MERGED`
