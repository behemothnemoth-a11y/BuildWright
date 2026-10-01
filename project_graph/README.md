# BuildWright Project Graph

This package assembles compiled BuildWright modules into complete multi-room / multi-floor projects.

## Files

- `model.py` — project/module/port contracts
- `solver.py` — connector alignment and collision solving
- `assembler.py` — module merge, connection carving, corridor construction
- `facade.py` — exposed-side facade pass
- `roof.py` — project/module roof massing
- `site.py` — lightweight ground and path assembly
- `compiler.py` — complete project compile + master Litematic
- `preview.py` — deterministic project graph SVG

## Important distinction

The project graph is a structural compiler, not an approval engine. Its job is to preserve room geometry, circulation contracts and coherent whole-building massing. A generated building is still `LIVE_GAME_PENDING` until tested at player eye level in Minecraft.

## Source of truth

Project briefs live under `examples/projects/` or project-specific folders. Generated files under `project_graph/compiled_examples/` are deterministic regression artifacts and should reproduce byte-for-byte.
