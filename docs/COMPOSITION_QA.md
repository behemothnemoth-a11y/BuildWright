# Composition QA

Offline composition validation proves deterministic assembly and file structure. It does not prove that a room looks good in Minecraft.

## Offline gates

- brief references an existing template/palette;
- all required slots resolve;
- selected fixtures fit declared bounds;
- fixture occupied bounds do not collide;
- fixture placements do not block connector keepouts;
- connectors are open in the final source;
- every output block lies within module bounds;
- Litematic readback non-air count matches source;
- compiled examples reproduce byte-for-byte;
- composition index reproduces;
- unit tests pass.

## Required in-game review

Review at player eye level:

1. entrance / first impression;
2. every connector and circulation route;
3. furniture clearance;
4. corners and side bays;
5. upward ceiling view;
6. repeated fixtures from several angles;
7. lighting and darkness;
8. visual hierarchy and negative space.

If a compiled room is technically valid but visually busy, sparse, repetitive, oversized or awkward, it is not approved.
