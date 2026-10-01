# Project Graph Compiler

BuildWright 0.7 adds a whole-building layer above the room/module composition compiler.

## Pipeline

\`\`\`text
compiled modules
→ named ports
→ graph solve
→ module transforms
→ shared-wall alignment
→ connector carve
→ optional corridors
→ facade pass
→ roof pass
→ site pass
→ normalization
→ master .litematic
→ readback validation
\`\`\`

Modules may use connectors inherited from their composition source or project-scoped custom ports.
Custom ports can face north/south/east/west/up/down, which makes floor-to-floor alignment explicit instead of inferred.

## Connection modes

- attach: boundary planes or floor/ceiling planes align directly.
- corridor: modules remain separated by a declared gap and a player-scale corridor is compiled between them.

Shared boundary planes may overlap by one block. Larger volumetric intersections are rejected.

## Project source

Each compiled project emits:
- a canonical project JSON with solved module origins;
- a provenance/QA manifest;
- an SVG graph plan;
- a final Litematica.

The project JSON records both pre-normalized and normalized coordinates so a build can be merged into a larger master later.

## Approval

A successful compile is OFFLINE_COMPILED, not APPROVED.
Player-eye review in Minecraft remains mandatory before a generated building becomes project canon.
