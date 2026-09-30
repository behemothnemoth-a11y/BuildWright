# BuildWright Agent Rules

These rules apply to ChatGPT, Codex, and automated contributors.

## 1. Source of truth

- Read `PROJECT_STATE.md` and the target project's state before changing geometry.
- Preserve approved connectors, circulation, placement origin, target Minecraft version and exporter profile.
- Do not silently replace approved geometry or maturity states.

## 2. Vanilla-first architecture

- Strong architecture comes before microblocks.
- Maintain primary → secondary → tertiary → micro hierarchy.
- Player clearance and room function override decorative cleverness.
- Use controlled gradients and depth, not random block noise.
- Preserve negative space; do not detail every surface.

## 3. Microblock implementation

- Read `packs/microblock/providers/` before assuming provider capabilities.
- Use a translation plan; never blanket-convert a module.
- Default to TIER 1–2. TIER 3 needs visible benefit; TIER 4 needs focal justification.
- Preserve behavior-sensitive vanilla blocks and circulation.
- For monumental ceilings/roofs, keep broad quiet fields and refine only meaningful structure.

## 4. Fixture source contract

- `fixtures/sources/` is canonical. Do not hand-edit compiled fixture `.litematic` bytes.
- Recompile and revalidate after fixture-source changes.
- Preserve fixture anchors when substituting or transforming variants.
- For Astra fixtures, preserve X-fast → Z → Y microcell ordering and provider transform rules.

## 5. Composition compiler rules

- A room brief defines constraints and intent, not arbitrary block spam.
- Declared connectors are authoritative. No fixture may silently close one.
- Keepout volumes protect circulation, future modules, sightlines, machinery lanes and hero spaces.
- Required slots must resolve or compilation/planning fails review.
- Optional slots may disappear because of density, fit or collision; that is normal variation.
- Prefer fixture families and variants; avoid manually hard-coding every asset position into every project brief.
- Use deterministic seeds. Re-running the same brief on the same BuildWright version must not drift.
- Palette remapping must preserve block shape/state where supported; unknown states remain unchanged rather than guessed.
- Do not confuse collision-free assembly with good design. Player-eye QA is still mandatory.

## 6. Completion honesty

Use maturity states honestly. A module that has only passed offline compilation/readback remains `LIVE_GAME_PENDING` until Minecraft has actually loaded and reviewed it.

Never call a preview or structural readback proof of final in-game appearance.
