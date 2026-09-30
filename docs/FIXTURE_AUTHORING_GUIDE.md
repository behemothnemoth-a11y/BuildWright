# Fixture Authoring Guide

1. Start from an existing pack family and variant.
2. Keep one clear purpose per fixture.
3. Declare anchor, size, family, source stage and QA gates.
4. Use vanilla source blocks for Stage A fixtures.
5. For Astra fixtures, use 16³ cell occupancy and a supported host material; never fabricate unsupported provider behavior.
6. Compile deterministically with `tools/compile_fixtures.py`.
7. Run `tools/validate_fixtures.py` and `tools/build_fixture_index.py --check`.
8. Inspect the preview and then perform a real Minecraft test before promoting to APPROVED.

### Fixture sizing
Small reusable elements beat enormous prefab rooms. Whole-room fixtures are allowed only when their circulation/connector contract is explicit.

### Variation
Create related source fixtures, not copy-paste mutations with no meaningful design difference.
