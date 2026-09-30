# Microblock Implementation

This file defines BuildWright Stage B.

Stage B begins only after a strong vanilla master exists.

## Pipeline

```text
VALIDATED VANILLA MASTER
→ MICROBLOCK CANDIDATE ANALYSIS
→ TARGET CLASSIFICATION
→ RESOLUTION / DETAIL TIER
→ MICROBLOCK CONVERSION
→ MICROBLOCK DETAIL PASS
→ PERFORMANCE + CIRCULATION QA
→ FINAL HYBRID BUILD
```

## Core rule

Full blocks define mass, circulation, room scale, primary structure, floors, major stairs, and large wall/roof planes.

Microblocks refine:

- contour
- trim
- carving
- lattice
- molding
- thin structural elements
- window tracery
- sculptural transitions
- furniture detail
- ornamental depth

## Candidate classification

Every possible conversion must be labeled:

- **KEEP_VANILLA** — full block form is already correct or performance-sensitive.
- **GOOD_MICROBLOCK_TARGET** — clear geometric benefit.
- **OPTIONAL_MICROBLOCK** — improvement exists but is not essential.
- **DO_NOT_CONVERT** — conversion would add cost/noise without meaningful form improvement.

## Suggested detail tiers

- **TIER 0** — vanilla only
- **TIER 1** — large microblock trim
- **TIER 2** — architectural contour
- **TIER 3** — furniture / decorative detail
- **TIER 4** — hero detail only

Do not make everything Tier 4.

## Typical targets

### Architecture

- clustered Gothic columns
- carved capitals / bases
- lancet and pointed arch refinement
- mullions and tracery
- cornices and molding
- corbels
- hammerbeam brackets
- balusters and railings
- fireplace surrounds
- door surrounds

### Furniture

- chair arms / legs
- desks and cabinets
- bed framing
- shelf edges
- display cases

### Decor

- chandeliers
- picture frames
- crests
- statues
- armor mounts
- candle holders

## Example conversions

### Clustered pier

```text
VANILLA
full blocks + stairs + walls

MICROBLOCK
central shaft
+ attached smaller shafts
+ stepped base
+ recessed channels
+ carved capital transition
```

### Gothic window

```text
VANILLA
full-block pointed arch + glass panes

MICROBLOCK
thin surround
+ smoother lancet curvature
+ narrow mullions
+ tracery
+ recessed glass plane
```

### Hammerbeam roof

```text
VANILLA
logs / stairs / slabs establish structure

MICROBLOCK
preserve primary beam mass
+ taper braces
+ carved shoulders
+ thin decorative edges
+ refined bosses / joints
```

## Performance discipline

Do not microblock large invisible masses, cave walls, broad floors, simple backing walls, or other geometry where vanilla blocks are already visually sufficient.

## Release discipline

Preserve both editions:

```text
releases/vanilla/
releases/microblock/
```

The microblock edition must never erase the vanilla master.
