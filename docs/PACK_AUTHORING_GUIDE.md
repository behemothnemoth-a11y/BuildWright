# Pack Authoring Guide

1. Choose a broad reusable family, not a project-specific object.
2. Add at least four meaningfully different variants.
3. Describe scale and material roles.
4. Add placement constraints and variation knobs.
5. Reference relevant technique IDs.
6. Keep recipe grammar parameterized.
7. Add anti-patterns and QA.
8. Run `python tools/validate_packs.py`.
9. Rebuild the index with `python tools/build_pack_index.py`.
10. Test selection with at least one example brief.
