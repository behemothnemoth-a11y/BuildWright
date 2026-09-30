# Rotation and Mirroring

Reusable BuildWright micro-assets must be transform-safe.

- Transform occupied cells inside every host.
- Transform host placement.
- Transform directional material axes/states where supported.
- Transform attachment sockets and connector normals.
- Do not apply the same transform twice after save/reload.
- Mirror asymmetric wear/clutter deliberately; do not assume a mirrored hero ornament remains semantically correct.

Astra Microblocks 0.4.0 supports sculpture rotation/mirroring and Litematica-aware transformations; BuildWright plans should preserve those semantics.
