# Vanilla Build Language

This file defines BuildWright Stage A: creating an excellent fully vanilla Minecraft build before any microblock translation.

## Pipeline

```text
SOURCE / REFERENCE
→ VANILLA NORMALIZATION
→ SCALE + PROPORTION
→ PRIMARY ARCHITECTURE
→ BUILDER-TECHNIQUE PASS
→ MATERIAL / GRADIENT PASS
→ FURNITURE + DECOR PACKS
→ VEGETATION / TREE PACKS
→ LIGHTING + ATMOSPHERE
→ CLUTTER / STORYTELLING
→ PLAYER-EYE QA
→ VALIDATED VANILLA MASTER
```

## 1. Vanilla normalization

Every Stage A artifact must use supported vanilla blocks and vanilla block states.

Check for and remove or replace:

- mod blocks
- microblocks
- unsupported entities
- invalid block states
- barriers / structure blocks used as placeholders
- temporary marker wool or concrete
- decorative hacks that do not survive export

Use vanilla substitutions intentionally, not mechanically.

## 2. Player scale

Player scale is mandatory even in monumental architecture.

- Doors and corridors must feel traversable.
- Furniture must be usable at Steve scale.
- Side rooms should not become giant empty boxes merely because the exterior is monumental.
- Grand halls may be tall, but eye-level architecture must remain legible.
- Keep clear walking paths and usable landings.

## 3. Primary / secondary / tertiary / micro hierarchy

Every finished area should read at four scales:

1. **PRIMARY** — room silhouette, roof, major massing.
2. **SECONDARY** — bays, stairs, galleries, arches, major piers.
3. **TERTIARY** — trim, wall depth, furniture, railings, fireplaces.
4. **MICRO** — clutter, candles, books, pots, buttons, small asymmetry.

Do not jump directly from a giant room to micro-clutter.

## 4. Depth

Important walls should rarely be a single plane.

Use combinations of:

- projecting piers
- recessed windows
- deep door surrounds
- foreground trim
- 1–3 block facade depth
- shadow gaps
- wall / recess / backing layers

## 5. Shaping techniques

Use vanilla partial blocks to create intentional silhouettes:

- stairs and upside-down stairs
- slabs
- walls
- fences
- trapdoors
- signs where appropriate
- buttons
- pressure plates
- pots / candles
- connected glass panes and iron bars

Use these because they improve shape, not merely because they add complexity.

## 6. Gradients

Use controlled material transitions.

Good gradient behavior:

- darker blocks in recesses
- lighter or cleaner blocks on exposed faces
- localized weathering
- restrained cracked / mossy blocks
- coherent warm/cool or rough/smooth transitions

Avoid random palette noise.

## 7. Repetition and asymmetry

Architectural rhythm is good. Copy-paste fatigue is not.

- Repeat major bays when the architecture requires rhythm.
- Vary furniture, books, clutter, plants, weathering, and individual wall-bay personality.
- Break perfect symmetry selectively.
- Use families of assets rather than one prefab repeatedly.

## 8. Negative space

Do not detail every block.

Large quiet surfaces, broad roof fields, open wall panels, and breathing room between focal points make detailed areas read better.

## 9. Ceilings and roofs

Large roofs should read as a few strong structural ideas, not a barcode of beams.

Preferred hierarchy:

```text
roof plane
→ major landmark trusses
→ ridge / primary purlins
→ restrained secondary structure
→ chandeliers / focal ornament
```

If the viewer cannot immediately understand the structural system, simplify it.

## 10. Furniture and decor

Use asset packs as compositional ingredients.

A room is not finished because it contains a table.

Example study composition:

```text
desk
+ offset chair
+ books / papers
+ candle or lamp
+ shelving or portrait behind
+ localized clutter
+ intentional lighting
```

## 11. Vegetation

Vegetation packs must contain variants.

Never create an estate by stamping one identical tree every fixed number of blocks.

Vary:

- silhouette
- rotation
- canopy density
- age
- spacing
- undergrowth
- relation to architecture

## 12. Anti-patterns

Do not:

- detail every surface
- repeat one decorative module continuously
- use identical columns every few blocks without hierarchy
- spam stairs, walls, trapdoors, or fences solely to increase complexity
- randomly mix palette blocks
- use enormous rooms to compensate for weak detailing
- block circulation with ornament
- make ceilings visually louder than the room beneath them without a deliberate reason

## 13. Required vanilla QA

Review from:

- main entrance / first impression
- standing player eye level
- major circulation paths
- stairs and landings
- room corners
- upward ceiling view
- exterior approach where applicable

A vanilla master is ready for microblock analysis only after the architecture and player-scale composition are strong without microblocks.
