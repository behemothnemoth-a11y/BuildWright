# Pack System

DROP 0002 turns the pack skeleton into a reusable catalog with **567 vanilla variants across 68 family packs**.

## Principle: family, not prefab

A pack describes a family of related compositions. Repeated use should vary rotation, mirror state, dimensions, palette, wear, clutter and local context.

## Asset anatomy

Every asset declares:

- category and family;
- compatible style tags;
- scale classes and dimension hints;
- material roles instead of project-specific blocks;
- recommended builder techniques;
- placement and clearance rules;
- variation knobs;
- a parameterized recipe grammar;
- anti-patterns and QA checks.

`packs/registry.json` lists families. `packs/index.json` flattens all assets for search/selection.

## Categories

- architecture
- vegetation
- furniture
- decor
- lighting
- techniques
- palettes
- style profiles

## Selection

Use `tools/select_assets.py` with a room brief. A selector result is a starting palette of families, never a command to place every returned asset.
