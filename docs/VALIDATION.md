# Validation

## Repository validation

`tools/validate_repo.ps1` checks required foundation files and JSON syntax.

## Schematic validation

Every generated schematic should record at minimum:

- Minecraft target
- DataVersion
- Litematic version/subversion
- region count
- bounds
- palette validity
- block count
- readback status

File-level readback is not the same as in-game approval.

## In-game validation

Check:

- file loads
- block states appear correctly
- player-scale circulation
- staircase destinations
- sightlines
- ceiling readability
- facade depth
- lighting
- interior usability
- excessive detail/noise

## Whole-building validation

DROP 0007 adds project-graph validation on top of module validation. The offline gate checks:

- every module source resolves;
- every named port exists;
- connected ports face compatible directions;
- all graph nodes resolve to deterministic origins;
- illegal volumetric module intersections are rejected;
- direct attachments share only a legal boundary plane;
- corridor endpoints align at player floor elevation;
- facade/roof/site passes remain inside the final normalized project envelope;
- master Litematic non-air count and block-entity count survive readback;
- committed project examples reproduce byte-for-byte, including JSON/SVG LF serialization.

Offline project validation still does not prove that the assembled building is aesthetically successful. Whole-building outputs remain `LIVE_GAME_PENDING` until loaded and walked in Minecraft.

## Universal style validation

DROP 0008 adds strict style/catalog gates:

- all registered style profiles must exist and have unique IDs;
- universal profiles must define complete semantic material roles;
- massing biases must remain normalized;
- default roof languages must be supported by the roof compiler;
- the style registry must regenerate byte-for-byte;
- committed style showcases must regenerate byte-for-byte;
- style profiles must stay project-neutral rather than naming a regression project;
- the living catalogue must regenerate byte-for-byte from repository state.

The style showcase corpus is an offline diversity/regression test. It proves that very different architectural languages can traverse the same compiler; it does not prove aesthetic approval in Minecraft.
