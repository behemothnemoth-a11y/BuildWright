# Microblock Translation Pipeline

## Gate 0 — Vanilla master
No microblock work begins from a rough blockout. The source module must have usable circulation, readable primary/secondary shapes and a documented vanilla maturity state.

## Gate 1 — Candidate analysis
Classify source features as KEEP_VANILLA, GOOD_MICROBLOCK_TARGET, OPTIONAL_MICROBLOCK, or DO_NOT_CONVERT. Functional behavior, provider limits, performance and negative-space value all outrank the desire to add detail.

## Gate 2 — Provider capability
Current provider profile is Astra Microblocks 0.4.0 for Minecraft 26.2, using a 16×16×16 cell host. Validate actual supported material states at compile time.

## Gate 3 — Detail profile
Choose one of the profiles in `packs/microblock/detail_profiles/`. Large builds should begin with `performance_guarded` or `architectural_standard`; TIER 4 is never a default coverage mode.

## Gate 4 — Translation plan
Use `tools/plan_microblock_translation.py` to map vanilla family IDs to one or more microblock families. The plan is reviewable before geometry is compiled.

## Gate 5 — Coarse-to-fine pass
1. TIER 1 silhouette repair.
2. TIER 2 structural contour.
3. TIER 3 eye-level detail only where it earns its cost.
4. TIER 4 focal sculpture only.

## Gate 6 — QA
Compare against the vanilla source. A successful translation should improve silhouette, thinness, contour or readable craftsmanship without making the scene busier, shrinking circulation or flattening material hierarchy.
