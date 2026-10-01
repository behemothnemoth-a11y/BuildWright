# Compiled Fixture System

DROP 0004 turns BuildWright's design vocabulary into executable assets.

## Current corpus

- **40 vanilla `.litematic` fixtures** compiled from canonical sparse block sources.
- **24 Astra Microblocks `.litematic` fixtures** with real 16×16×16 host occupancy NBT.
- **32 rotation/mirror corpus files** covering all eight horizontal Astra orientations for asymmetric shapes.
- Source JSON, SHA-256 identity, previews and independent readback validation for every core fixture.

The source JSON is the editable source of truth. `.litematic` files are derived artifacts.

## Required lifecycle

```text
pack recipe / design intent
→ fixture source JSON
→ deterministic compiler
→ litematic artifact
→ independent readback
→ preview
→ transform corpus where relevant
→ in-game smoke test
→ APPROVED fixture
```

Fixtures in DROP 0004 are **SERIALIZATION_VALIDATED / LIVE_GAME_PENDING** unless a project records an in-game review.

## Do not confuse fixtures with finished compositions

A fixture is a reusable construction unit. BuildWright still expects composition, scale, palette adaptation, negative space and player-eye QA at project level.

## Vanilla finishing fixtures

DROP 0009 expands the compiled vanilla fixture library to 85 fixtures. Forty-five are tagged `detail_fixture: true` and are reserved for the vanilla finishing layer by default.

Primary composition searches exclude detail fixtures unless a selector explicitly requests `include_detail_fixtures`. This keeps architectural baselines stable as the finishing library grows. The finishing compiler may place detail fixtures directly from their canonical vanilla sources after primary architecture is established.
