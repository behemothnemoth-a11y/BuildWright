# Deterministic Variation

BuildWright needs variation without becoming unreproducible.

DROP 0005 therefore uses seeded deterministic selection.

A slot can be optional and can offer multiple fixture families or preferred variants. Candidate scores consider:

- explicit preferred IDs;
- requested category/family;
- the active style profile's preferred architecture families;
- style tokens inferred from fixture IDs;
- repeat penalties;
- fit and collision feasibility;
- a very small seeded tie-break value.

The planner also tracks repeat counts so one prefab does not automatically dominate a room.

## Reproducibility contract

Identical:

- repository version;
- brief;
- seed;
- fixture registry;
- compiler version;

should produce identical plan and compiled output.

Changing the seed is a deliberate request for a new arrangement, not a substitute for architectural judgment.
