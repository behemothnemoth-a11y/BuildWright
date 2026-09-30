# BuildWright Agent Rules

These rules apply to ChatGPT, Codex, and any automated contributor working in this repository.

## Source of truth

The repository is the source of truth. Do not silently replace approved project geometry, connector coordinates, maturity states, or pack contracts.

## Required workflow

1. Read `PROJECT_STATE.md` and the target project's state file before changing geometry.
2. Determine whether the task is VANILLA or MICROBLOCK stage.
3. Keep changes bounded to the requested module whenever possible.
4. Preserve declared connectors, circulation, placement origin, Minecraft target, and export profile.
5. Produce a new candidate; do not overwrite an approved release unless explicitly instructed.
6. Validate the artifact after export.
7. Record what changed and what remains unverified in-game.

## Architecture rules

- Never confuse complexity with detail.
- Avoid continuous repeated modules that create visual noise.
- Prefer primary silhouette, secondary structure, tertiary trim, then micro-detail.
- Important walls should usually have depth: foreground, face, recess, backing.
- Concentrate player-scale detail around eye level while preserving landmark scale above it.
- Circulation is functional architecture. Stairs, portals, halls, and landings must connect to usable destinations when declared as connectors.
- Preserve negative space.

## Vanilla-first rule

Do not introduce microblocks until the vanilla version reaches an approved or explicit microblock-ready state.

## Microblock rule

Classify candidates as:

- KEEP_VANILLA
- GOOD_MICROBLOCK_TARGET
- OPTIONAL_MICROBLOCK
- DO_NOT_CONVERT

Microblocks should primarily refine contour, trim, carving, lattice, molding, thin elements, sculptural transitions, furniture detail, and hero ornament.

## Completion honesty

Use maturity states honestly:

CONCEPT → BLOCKOUT → ARCHITECTURE → DETAILING → REVIEW_CANDIDATE → APPROVED → MERGED

Do not call something FINAL or APPROVED without the required in-game review.
