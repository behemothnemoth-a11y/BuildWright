# Structural & Site Intelligence

BuildWright 0.10 adds project-scale structural and site systems on top of the vanilla-detail-complete pipeline.

## Circulation

Project connections can now use deterministic routed circulation when a straight corridor is not appropriate. Routed connections preserve the declared room origins and build a player-scale orthogonal path between named ports.

Vertical connections can compile stair flights between unequal module elevations instead of requiring perfectly aligned floor planes.

## Structural nodes

Project briefs may attach reusable structural nodes to named modules:

- tower
- porch
- balcony
- buttress_run
- dormer_row

These are project-graph structures, not project-specific hard-coded geometry. They inherit the active style/material profile unless explicitly overridden.

Structural nodes are intentionally coarse enough to remain readable and to leave room for later vanilla finishing. They are not microblock substitutes.

## Foundations

Modules elevated above the site grade can receive deterministic foundations:

- perimeter
- piers
- solid

Foundation placement bridges the module base to the declared site/ground elevation. The engine records maximum drop and generated block count in the project manifest.

## Site networks

The site compiler can now carry explicit project-scale networks:

- path
- road
- plaza
- wall
- fence
- retaining_wall
- stairs

Networks use ordered control points and declared widths/heights. This lets a whole building compile with meaningful approach roads, service routes, plazas, perimeter walls, fences and grade-control structures instead of a single flat pad.

## Validation

Structural/site regression projects must:

- reproduce byte-for-byte;
- remain free of Astra namespace content;
- preserve explicitly positioned modules;
- generate valid routed circulation;
- preserve player-scale corridor/stair clearance;
- keep foundations and retaining geometry deterministic;
- remain LIVE_GAME_PENDING until loaded and reviewed in Minecraft.

The current regression corpus includes a routed Gothic estate, a terraced hillside compound and a modern campus network.
