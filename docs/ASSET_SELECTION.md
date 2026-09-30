# Asset Selection

Use a room brief to select relevant families and variants.

Example:

```powershell
python tools/select_assets.py --brief examples/briefs/grand_hall.json --limit 12
```

The selector scores style-tag overlap, requested category/family, scale compatibility and context. Treat the output as a shortlist. Human/agent composition still decides which assets belong in the room and how much negative space remains.
