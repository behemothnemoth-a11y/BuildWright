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

## DROP 0007 whole-building rules

- Treat module ports as hard contracts. Do not move, close, shrink, or decorate across them unless the project brief explicitly changes the port.
- Direct room attachments may share one boundary plane; volumetric room collisions are invalid.
- Vertical `up`/`down` ports are authoritative for floor-to-floor alignment.
- Corridor generation must preserve declared player width/height and must not silently tunnel through unrelated modules.
- Exterior facade passes operate only on exposed sides. Interior shared walls and circulation openings take priority over facade rhythm.
- Roof massing is a project-scale envelope pass. Do not overwrite hand-authored hero ceilings blindly.
- Prefer a few strong exterior bays, towers, roof forms, and facade zones over continuous repeated micro-detail.
- Whole-building compilation must remain deterministic from the same project brief.
- A successful offline whole-building compile is `LIVE_GAME_PENDING`, never automatically APPROVED.
- Generated Wayne Manor examples are compiler regression fixtures, not canon replacements for hand-refined Wayne geometry.

## DROP 0008 universal-style rules

- Core BuildWright logic must remain project-neutral. Do not bake Wayne Manor, Blackglass, Cthulhu, or any other named project into universal style defaults.
- A style profile describes architectural language: massing bias, facade rhythm, window language, material roles, roof language, ornament density, site character and related constraints.
- Project-specific story, layout, dimensions and hero geometry belong in project briefs/overrides, not reusable style profiles.
- Material roles are semantic. Override wall/structure/trim/accent/glass/plinth/roof roles explicitly; never interpolate block IDs.
- Hybrid styles retain a primary architectural language and blend numeric biases from a secondary profile. Avoid incoherent fifty-fifty style soup.
- Facade zones distinguish hero, primary, secondary, service, courtyard and blind elevations. Do not detail every exterior face equally.
- Roof language is style-aware but remains a massing pass. Hand-authored hero roofs/ceilings can opt out.
- Universal style additions require registry validation and at least one representative compile path.
- The living catalogue must be regenerated when a major reusable system, compiled artifact family, style corpus, or project regression set changes.

## DROP 0008B visual-catalogue rules

- The visual catalogue is picture-first. A catalogue entry without a usable preview is incomplete.
- Fixture cards should use canonical fixture previews. Room/project/style cards should render from the compiled Litematic, not from unrelated concept art.
- Room/module previews should use cutaway views when an exterior shell would hide the content being catalogued.
- Generated isometric renders are geometry proofs with simplified material colors; never present them as Minecraft screenshots or shader output.
- Every core universal style profile must have a rendered showcase card.
- Regenerate both CATALOG.md and VISUAL_CATALOG.md whenever compiled catalogue coverage changes.

## DROP 0008C vanilla-baseline separation

- BuildWright's authoritative base output is vanilla-only.
- The required progression is: vanilla massing/base → complete vanilla architecture/detail/furnishing/lighting/landscape → in-game review → optional microblock refinement.
- Astra Microblocks must never be required to make a baseline build read correctly.
- Main catalogues and default examples must exclude Astra-host assets. Optional microblock assets live in a clearly separate refinement catalogue.
- Style showcase renders are baseline architectural-language tests, not finished vanilla-detail builds.
- A hybrid/microblock proof may be retained for testing, but it must never be presented as a base example.
- Validation must fail if an Astra namespace block or block entity leaks into any artifact classified as a vanilla baseline.
