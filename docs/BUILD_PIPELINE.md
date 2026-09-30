# Build Pipeline

## Composition layer — reusable module assembly

1. Register reference/project intent.
2. Define a bounded room/module brief.
3. Lock room size, style profile, palette, connectors and keepouts.
4. Choose a spatial template or use `freeform`.
5. Plan fixture slots deterministically.
6. Reject collisions and connector conflicts.
7. Compile canonical module source + manifest + Litematic.
8. Run independent readback.
9. Review the module in Minecraft.
10. Refine the brief/template/fixtures rather than hand-corrupting compiled bytes.

## Stage A — Vanilla

1. Establish player scale and envelope.
2. Build primary architecture.
3. Resolve circulation and connectors.
4. Apply builder-technique pass.
5. Apply controlled palette/gradient pass.
6. Add furniture, decor, lighting and vegetation packs.
7. Review from player eye level.
8. Export and validate vanilla schematic.
9. Mark REVIEW_CANDIDATE only after appropriate review.
10. Approve only after in-game review.

## Stage B — Microblock

1. Freeze the approved/selected vanilla source.
2. Identify conversion candidates.
3. Classify each candidate.
4. Choose detail tier.
5. Convert only approved targets.
6. Recheck circulation and silhouette.
7. Validate export and transform behavior.
8. Compare vanilla and microblock editions in-game.

## Iteration loop

```text
reference / brief
→ plan
→ module candidate
→ schematic
→ Minecraft test
→ screenshot/video
→ critique
→ bounded refinement
→ candidate
```

Prefer bounded module refinement over rebuilding an entire project for every change.
