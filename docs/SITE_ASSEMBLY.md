# Site Assembly

The project compiler can add a lightweight site layer around the assembled building.

Current site operations:
- configurable ground plane;
- project margin;
- deterministic orthogonal paths;
- independent site palette.

Site compilation happens after building assembly and before final coordinate normalization.

The site layer is intentionally conservative. It establishes a usable terrain pad and circulation skeleton without pretending to replace a dedicated landscape design pass.

Future work can attach compiled vegetation fixtures, retaining walls, gardens, drives, courtyards, stairs, water features and terrain gradients through the same graph/fixture system.
