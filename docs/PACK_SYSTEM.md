# Pack System

Reusable detail should be authored once, tested, then reused with variation.

## Pack families

### Vanilla

- architecture
- vegetation
- furniture
- decor
- lighting

### Microblocks

- architecture
- furniture
- decor

## A pack is not a single prefab

Each pack should define:

- purpose;
- compatible Minecraft/profile;
- scale range;
- variants;
- rotation/mirroring rules;
- placement constraints;
- palette assumptions;
- player-clearance requirements;
- optional story/weathering variants;
- microblock tier where applicable.

## Examples

### Vegetation

`manor_oak` should eventually include multiple trunk/canopy forms, rotations, age variants and placement spacing rules.

### Furniture

`gothic_armchair` should include standard, ornate, worn and compact variants rather than one chair copied everywhere.

### Architecture

`hammerbeam_roof` should include small, medium, monumental, narrow-hall and asymmetrical-old-manor families with clear span and height constraints.

## Registry

`packs/registry.json` is the machine-readable index. Individual pack folders may later contain their own `pack.json`, schematics, reference previews, placement masks and validation fixtures.

## Authoring rule

Pack geometry must not assume a project-specific story fact unless the pack is explicitly project-scoped.
