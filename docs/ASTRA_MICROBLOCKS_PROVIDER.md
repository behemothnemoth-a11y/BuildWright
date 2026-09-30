# Astra Microblocks Provider Profile

BuildWright's initial provider is `astra_microblocks_0_4_0`.

Snapshot used by DROP 0003:
- Minecraft 26.2 / Fabric;
- 16×16×16 cells per host (4096 cells);
- multi-material cells;
- reusable sculpture items;
- X/Y/Z rotation and mirroring;
- Litematica transform-aware sculpture data;
- current README reports 235 vanilla blocks / 325 supported states.

BuildWright does **not** copy the entire provider material whitelist. The mod remains authoritative, and compile/export tooling must validate requested states against the provider in use.

Functional behavior caveat: a sculpted host preserves cell shape/material appearance, not every behavior of the original vanilla block. Keep behavior-sensitive blocks vanilla unless a future provider contract explicitly supports them.
