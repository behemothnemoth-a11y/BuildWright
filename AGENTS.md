# BuildWright Agent Rules

## Compiled fixture rules added by DROP 0004
- Treat `fixtures/sources/` as canonical. Do not hand-edit compiled `.litematic` bytes.
- Recompile and revalidate after source changes.
- Do not promote `SERIALIZATION_VALIDATED` to `APPROVED` without a real Minecraft review.
- Prefer small reusable fixtures to giant opaque prefabs.
- Preserve fixture anchors and connector semantics when substituting variants.
- For Astra fixtures, preserve provider grid order (X fastest, then Z, then Y) and orientation contract.
- Use asymmetric geometry in transform tests.
- A preview is an inspection aid, not proof of in-game appearance.
- Keep fixture composition subordinate to the vanilla/microblock design language and player-scale rules.
