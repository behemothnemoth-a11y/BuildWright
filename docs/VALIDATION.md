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

## Visual catalogue validation

DROP 0008B adds coverage checks for the picture-first catalogue:

- every catalogued fixture preview must exist;
- every rendered room/project/style image must exist;
- every visual card must point to a real source artifact;
- all 35 core universal styles must have a rendered showcase;
- gallery pages, overview contact sheets and the visual manifest must exist;
- room/module imagery uses cutaway renders where exterior shells would hide the interior.

The visual catalogue is a browsing aid, not an approval gate. A generated preview can still represent a LIVE_GAME_PENDING artifact.

## Vanilla baseline separation

DROP 0008C adds a hard vanilla-baseline gate. Every artifact classified as a vanilla room baseline, whole-building baseline, or style baseline is read back and scanned for the `astra_microblocks:` namespace in both block-state palettes and block entities. Any match fails repository validation.

The main visual catalogue must also contain only vanilla fixtures and vanilla-classified room/project/style entries. Optional Astra fixtures and hybrid proof artifacts are retained in `MICROBLOCK_CATALOG.md` and are intentionally downstream of vanilla completion.

## Complete vanilla detail validation

DROP 0009 adds a deterministic completion gate above the vanilla architectural baseline:

- all 45 detail fixtures must compile from canonical vanilla-only sources;
- all 10 room-role detail profiles must exist and remain deterministic;
- all 10 VANILLA_DETAIL_COMPLETE room regressions must reproduce byte-for-byte;
- all 3 VANILLA_DETAIL_COMPLETE whole-building regressions must reproduce byte-for-byte;
- detail-complete artifacts must record their finishing statistics and detail maturity;
- every baseline and detail-complete vanilla Litematic is scanned for the `astra_microblocks:` namespace;
- visual-catalog coverage must include both BASELINE and VANILLA_DETAIL_COMPLETE examples;
- fixture/detail placement may skip conflicting optional content, but must never break authoritative connector/circulation keepouts.

`VANILLA_DETAIL_COMPLETE` is an offline finishing milestone, not APPROVED. Minecraft/player-eye review remains required.

## Structural and site validation

DROP 0010 adds project-scale circulation/structure/site regression gates:

- structural/site example briefs must recompile byte-for-byte;
- routed connections must generate player-scale route geometry while preserving explicitly positioned modules;
- elevation stair connections must generate vertical circulation and preserve connector clearances;
- structural nodes must reference valid modules and supported node types;
- foundations must respond deterministically to declared grade and module elevation;
- roads, plazas, walls, fences, retaining walls and site stairs must produce deterministic network statistics;
- all structural/site outputs must remain free of the `astra_microblocks:` namespace;
- generated structural/site projects remain LIVE_GAME_PENDING until loaded and reviewed in Minecraft.

## Style-family finish and reference-fit validation

DROP 0011 adds two additional vanilla gates.

Style-family finish validation requires:

- all 14 architectural families to have committed regression projects;
- each regression to add meaningful style-family finish geometry;
- family finish signatures to remain diverse rather than collapsing to one generic treatment;
- all style-family finish outputs to remain free of the `astra_microblocks:` namespace.

Reference-fit validation requires:

- strict zero-tolerance reference regressions to pass exactly;
- project/module/facade/port targets to record measured error and tolerance;
- strict mode to fail compilation when a target exceeds tolerance;
- measured-origin injection to preserve explicitly authored module origins and only fill missing origins when opted in.

Reference-fit PASS proves dimensional/anchor agreement only. It does not prove photographic likeness or in-game approval.
