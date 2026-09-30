# BuildWright

BuildWright is a reusable Minecraft architecture and detailing system for producing, refining, validating and releasing high-detail builds.

The project has two explicit stages:

1. **Vanilla Build Language** — establish strong, player-scale architecture using reusable technique, architecture, vegetation, furniture, decor and lighting packs.
2. **Microblock Implementation** — refine selected vanilla geometry only after the vanilla master is strong.

## DROP 0002 catalog

- **68** reusable vanilla pack families
- **567** asset variants
- **22** builder-technique cards
- **16** material palettes
- **16** style profiles

These assets are parameterized composition recipes and selection metadata, not one-off project prefabs. The same catalog is intended for manor builds, castles, cities, taverns, modern houses, ruins, caves, industrial builds, fantasy builds and more.

## Core commands

```powershell
python tools/validate_repo.py
python tools/validate_packs.py
python tools/build_pack_index.py --check
python tools/report_pack_coverage.py
python tools/select_assets.py --brief examples/briefs/grand_hall.json --limit 12
```

See `docs/PACK_SYSTEM.md` and `docs/PACK_AUTHORING_GUIDE.md`.
