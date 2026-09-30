# Vanilla Asset Contract

Reusable assets must remain project-agnostic, vanilla-only, player-readable and variation-safe.

## Required

- unique stable ID;
- family identity;
- vanilla stage;
- dimension hints;
- material roles;
- placement constraints;
- variation knobs;
- recipe grammar;
- QA checks.

## Forbidden

- hidden project lore in general packs;
- one exact prefab represented as a whole family;
- mandatory mod blocks;
- ornament that assumes inaccessible or fake circulation;
- random texture as the only source of visual interest.

## Connectors

Architecture recipes should expose or preserve doors, landings, corridors, stair exits and service access. Asset adaptation may reshape trim but must not silently close declared connectors.
