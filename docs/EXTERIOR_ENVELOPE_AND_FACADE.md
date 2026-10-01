# Exterior Envelope and Facade Compiler

The facade pass turns exposed module boundary faces into coherent project-scale exteriors without replacing module interiors.

BuildWright 0.8 no longer treats Gothic/classic/industrial/modern as the main four targets. The universal style registry contains **35 project-neutral profiles across 14 architectural families**. See `docs/UNIVERSAL_STYLE_SYSTEM.md` and `project_graph/style_registry.json`.

## Current operations

- plinth/base zone
- projecting structural piers and variable bay rhythm
- facade depth bias
- vertical accent spines
- multiple window-shape languages
- glazing
- mullions/transoms for gridded families
- sill/header trim
- body/crown bands
- cornice bands
- restrained balcony projection
- connector exclusion zones
- facade zoning: hero / primary / secondary / service / courtyard / blind
- per-side facade overrides

Doors, room connections and circulation ports always win over decorative rhythm.

## Design rule

Facade detail must reinforce massing hierarchy rather than cover every block. The engine uses a few legible zones and rhythms, then leaves room for fixture-based hero details and project-specific refinement.

## Style neutrality

Universal profiles describe architecture, not named projects. Project-specific facade decisions belong in the project brief through style blends, material-role overrides, facade-zone assignments and side overrides.

Future exterior work can add tower/dormer/buttress/porch/balcony graph nodes, story-aware zoning, urban frontage rules and reference-fitted real-world facades.
