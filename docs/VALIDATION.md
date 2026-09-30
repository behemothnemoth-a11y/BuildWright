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
