# Astra Microblocks Fixture Provider

BuildWright DROP 0004 targets Astra Microblocks 0.4.x on Minecraft 26.2.

## Host model
- one host block contains a 16×16×16 occupancy grid;
- grid indexing is X-fastest, then Z, then Y;
- occupancy is persisted as `grid_0` … `grid_63` longs;
- legacy two-material compatibility uses `oak_0` … `oak_63`;
- `grid_format_v1=true`, `materials_v2=true`;
- block entity id: `astra_microblocks:test_host`;
- host blocks: `astra_microblocks:test_host` and `astra_microblocks:oak_host`;
- block state property `orientation=0..7` represents the eight horizontal symmetries.

## Transform test strategy
Fixture tile NBT stores `astra_orientation=0`. Transform-corpus files vary the host block state's orientation. Astra's load path computes the orientation delta and transforms the cell grid, which tests the same mechanism used by Litematica rotation/mirror placement.

## Important limitation
DROP 0004 validates file structure and provider NBT offline. Live Fabric/Litematica behavior remains a separate smoke-test gate.
