# Microblock Pack Authoring Guide

DROP 0003 contains 75 families and 606 variants. Add new families only when an existing family cannot express the design through parameters/variation.

Every asset must define:
- source vanilla family;
- candidate class;
- allowed/default resolution tier;
- material roles;
- shape primitives;
- translation intent;
- complexity limits;
- variation knobs;
- anti-patterns;
- QA.

Use `packs/microblock/templates/`. Run `python tools/validate_microblocks.py` and `python tools/build_microblock_index.py --check` before committing.
