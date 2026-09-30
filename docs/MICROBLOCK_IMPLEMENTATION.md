# Microblock Implementation

This is Buildwright Pass B. It starts only from an approved or explicitly designated vanilla master.

## Core rule

> Full blocks establish architecture. Microblocks refine contour and fine detail.

Microblocks are not permission to replace sound massing, circulation or structural hierarchy.

## 1. Pipeline

```text
APPROVED VANILLA MASTER
        ↓
CANDIDATE ANALYSIS
        ↓
TARGET CLASSIFICATION
        ↓
MICROBLOCK CONVERSION
        ↓
DETAIL / CONTOUR PASS
        ↓
PERFORMANCE + NAVIGATION QA
        ↓
HYBRID REVIEW CANDIDATE
        ↓
APPROVED MICROBLOCK EDITION
```

## 2. Responsibility split

### Keep primarily full-block

- room mass;
- circulation;
- floors;
- primary walls;
- main stair treads;
- major roof planes;
- structural cave mass;
- primary load-bearing-looking forms;
- large furniture bodies where full blocks already work.

### Strong microblock targets

- Gothic tracery and mullions;
- clustered pier profiles;
- capitals and bases;
- arch contouring;
- cornices and molding;
- corbels and hammerbeam brackets;
- balusters and thin rails;
- window lattice;
- fireplace carving;
- wall panel molding;
- picture/portrait frames;
- chandelier frames;
- furniture legs, arms, edges and handles;
- crests and heraldic relief;
- gargoyles and small sculpture;
- machinery contour where it materially improves readability.

## 3. Candidate classification

Every potential conversion is assigned one of:

- `KEEP_VANILLA`
- `GOOD_MICROBLOCK_TARGET`
- `OPTIONAL_MICROBLOCK`
- `DO_NOT_CONVERT`

Example:

| Feature | Class |
|---|---|
| Stone floor field | KEEP_VANILLA |
| Main staircase treads | KEEP_VANILLA |
| Gothic window tracery | GOOD_MICROBLOCK_TARGET |
| Wall molding | GOOD_MICROBLOCK_TARGET |
| Bookshelf body | KEEP_VANILLA |
| Bookshelf trim | OPTIONAL_MICROBLOCK |
| Structural cave wall | DO_NOT_CONVERT |

## 4. Detail tiers

- **Tier 0 — Vanilla only:** no conversion.
- **Tier 1 — Large trim:** simple depth/edge improvement.
- **Tier 2 — Architectural contour:** arches, piers, rails, roof brackets.
- **Tier 3 — Furniture/decor:** refined furniture and ornament.
- **Tier 4 — Hero detail:** crests, statues, focal carvings, showcase machinery.

Tier 4 should be rare.

## 5. Performance discipline

Do not maximize subdivision everywhere.

Prefer:

- the coarsest resolution that achieves the intended silhouette;
- repeated microblock geometry only where its repetition is visible and worthwhile;
- full-block hidden/backing volumes behind microblock faces;
- explicit budgets for large modules;
- hero detail around focal areas and player-eye zones rather than inaccessible surfaces.

## 6. Conversion recipes

Buildwright will eventually store reusable conversion recipes. Initial intended families:

### Clustered Gothic pier

Vanilla: full-block core + stairs/walls  
Microblock: central shaft + attached shafts + stepped base + recessed channels + capital transition.

### Gothic window

Vanilla: blocky pointed arch + panes  
Microblock: thin surround + lancet contour + mullions + tracery + recessed glass plane.

### Hammerbeam roof

Vanilla: logs/stairs/slabs define the structural bay  
Microblock: tapered braces + carved shoulder + thin decorative edges + refined joint transitions.

### Furniture

Vanilla: strong body and usable scale  
Microblock: legs, arms, trim, handles, carved edges, thin shelves, upholstery contour.

## 7. Preservation contract

Microblock translation must preserve, unless explicitly changed:

- module footprint;
- connector coordinates;
- stair destinations;
- door/corridor clearances;
- major sightlines;
- approved room purpose;
- vanilla master artifact.

## 8. Output separation

Projects keep independent release lines:

```text
releases/vanilla/
releases/microblock/
```

The microblock edition never silently replaces the vanilla recovery/reference artifact.
