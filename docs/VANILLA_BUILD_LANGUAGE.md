# Vanilla Build Language

This is Buildwright Pass A. Every project should become a strong, complete vanilla Minecraft build before microblock translation begins.

## 1. Transformation pipeline

```text
SOURCE / REFERENCE / ROUGH SCHEMATIC
        ↓
VANILLA NORMALIZATION
        ↓
SCALE + PROPORTION
        ↓
PRIMARY ARCHITECTURE
        ↓
BUILDER-TECHNIQUE PASS
        ↓
MATERIAL / GRADIENT PASS
        ↓
FURNITURE + DECOR
        ↓
VEGETATION
        ↓
LIGHTING + ATMOSPHERE
        ↓
CLUTTER / STORYTELLING
        ↓
PLAYER-EYE QA
        ↓
APPROVED VANILLA MASTER
```

## 2. Vanilla normalization

Before detailing, remove or quarantine:

- mod-only blocks;
- microblocks;
- invalid/unsupported states;
- temporary markers and placeholder palettes;
- decorative hacks that do not survive the target export/runtime.

The resulting module must stand on its own in vanilla Minecraft.

## 3. Four readable scales

Every finished area should work at four levels:

1. **Primary** — silhouette, room mass, roof mass, stair mass, major axis.
2. **Secondary** — bays, galleries, arches, columns, wall recesses, large furniture groups.
3. **Tertiary** — trim, paneling, railings, furniture variation, lighting fixtures.
4. **Micro** — books, pots, buttons, candles, desk clutter, small wear and storytelling.

Do not let tertiary or micro detail obscure primary and secondary reads.

## 4. Player scale

Player-scale correctness is a release requirement.

- Circulation must be navigable without decorative obstruction.
- Important corridors should normally remain at least 2 blocks high and deliberately wide enough for their role.
- Furniture must leave believable movement space.
- Eye-level detail should concentrate roughly within the first several blocks above floors.
- Monumental rooms may be tall, but usable subspaces, landings, furniture, railings, and doors must still read at human scale.
- Decorative stairs must never replace stairs that are supposed to connect to other rooms.

## 5. Depth before decoration

Important walls should rarely be a single flat plane.

Use combinations of:

- recessed wall bays;
- projecting piers;
- layered door surrounds;
- recessed windows;
- foreground trim / wall / recess / backing planes;
- 1–3 block depth changes on major facades when scale allows.

A flat wall covered in random detail is still a flat wall.

## 6. Shape language

Use vanilla partial blocks intentionally:

- stairs for stepped cornices, arch transitions, furniture shaping, roof contour;
- slabs for ledges, ceiling transitions, beams, shelves, molding;
- walls/fences for thin vertical rhythm where structurally believable;
- trapdoors/signs for paneling and thin decorative layers;
- buttons/pressure plates for restrained micro accents;
- chains, rods, candles, pots, heads and other small vanilla shapes only where they serve the composition.

Do not spam partial blocks simply to make an area look complicated.

## 7. Material gradients

Gradients are controlled value/composition tools, not random noise.

Preferred logic:

- darkest values in deep recesses and structural shadow;
- midtones on primary wall fields;
- lighter/exposed materials on edges, highlights and worn faces;
- localized aging/weathering based on water, traffic, heat, age or story;
- repeatable palette families with room for hand-tuned exceptions.

Avoid evenly distributed random block substitutions.

## 8. Negative space

A finished build needs quiet areas.

Do not:

- detail every block;
- repeat one ornament every few blocks across an entire room;
- fill every ceiling bay with equal complexity;
- turn every support into a hero object.

Large calm surfaces give important architecture room to read.

## 9. Controlled asymmetry

Use asymmetry for life and history:

- varied books and shelf contents;
- slightly different furniture groupings;
- plant growth;
- worn or repaired areas;
- localized clutter;
- room-specific bay treatment.

Primary structural symmetry may remain where the architecture calls for it.

## 10. Reusable pack categories

Buildwright vanilla packs are organized into:

- `architecture`
- `vegetation`
- `furniture`
- `decor`
- `lighting`

A pack is a **family** with variants and placement rules, not a single prefab copied repeatedly.

## 11. Composition anti-patterns

Avoid:

- identical columns at short fixed intervals with no hierarchy;
- giant empty rooms used to simulate grandeur;
- roofs made from hundreds of equally important ribs;
- random texture noise;
- furniture placed as isolated objects without composition;
- decorative geometry that blocks movement;
- over-lighting every surface;
- micro-detail before room proportions are correct.

## 12. Vanilla approval gate

A module may become `APPROVED` only after:

- format/readback validation;
- player-scale circulation check;
- player-eye screenshots or walkthrough;
- primary/secondary readability review;
- lighting review;
- no known blocking defects.

The approved vanilla artifact remains preserved even after microblock work begins.
