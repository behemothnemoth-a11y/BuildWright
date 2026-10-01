# Universal Style & Exterior System

BuildWright 0.8 deliberately separates the **build engine** from any one project or architectural style.

Wayne Manor, industrial campuses, modern houses, fantasy fortresses, temples, ruins and organic builds all use the same project-graph/compiler layer. A style profile supplies architectural language; it does not change the fundamental graph, circulation, fixture, validation or Litematic pipeline.

## Style profile contract

Each profile defines:

- architectural family and display name;
- semantic material roles: wall, structure, trim, accent, glass, plinth, roof;
- facade rhythm and symmetry bias;
- bay spacing and facade depth;
- window language and proportions;
- ornament density and vertical emphasis;
- default roof language;
- project-scale massing biases;
- site character and vegetation intent;
- facade-zone presets.

The current registry contains **35 profiles across 14 architectural families**.

## Style blending

A project may declare a primary and secondary style. BuildWright blends numeric architectural biases while keeping the primary profile's categorical language unless explicitly overridden.

This avoids meaningless block-ID interpolation. Material changes are handled through explicit semantic material-role overrides.

Example intent:

    primary: japanese_traditional
    secondary: modern
    blend: 0.30
    glass role: tinted glass

The result remains recognizably Japanese-led rather than becoming an arbitrary average of two palettes.

## Facade zoning

Exterior sides can be marked:

- hero
- primary
- secondary
- service
- courtyard
- blind

Zones change depth, ornament, window scale and banding without changing the underlying style profile. A service elevation therefore does not receive the same treatment as the principal entrance facade.

## Window languages

The facade compiler understands multiple broad window languages including pointed/lancet, arched, horseshoe, mullioned, factory grid, curtain wall, ribbon, slot, shoji/lattice, storefront, balcony group, organic arch and broken/ruin openings.

These are coarse architectural languages, not final handcrafted tracery.

## Roof languages

The roof compiler now supports semantic roof modes including:

- flat / mechanical flat
- gable / steep gable / low gable / swept gable
- hip
- mansard
- shed
- butterfly
- sawtooth
- pagoda / tiered
- dome / dome-flat
- vaulted mass
- terraced
- ruined

These are whole-building massing tools. Interior hero ceilings remain independently refinable.

## Site language

Style profiles also carry site intent such as formal grounds, courtyard, garden, mountain, farm, desert, dense urban, hardscape, temple garden, overgrown ruin, or submerged.

The current site compiler remains intentionally restrained: it establishes ground, paths and sparse edge language. Dedicated terrain and vegetation passes remain separate future layers.

## Project neutrality

Core style profile IDs must describe architecture, not a named BuildWright project.

Project-specific decisions belong in project briefs and overrides. This prevents one regression project from becoming an accidental default for every future build.
